"""Reconstruct every proof premise from integer APs, without a model/encoder."""
import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

from check_rup_lrat import verify


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(certificate, builddir):
    began = time.monotonic()
    data = json.loads(certificate.read_text())
    word = data['base_halfword']
    require(len(word) == 309 and set(word) <= {'0', '1'}, 'invalid reference halfword')
    require(hashlib.sha256((word + '\n').encode()).hexdigest() ==
        'd177ade34d896ae4ef2563f1719e42601110ee98002a17d7df59472f4095d366', 'different reference word')
    bits = list(map(int, word))
    frozen = data['frozen_residues']
    require(frozen == sorted(set(frozen)) and all(type(r) is int and 0 <= r < 103 for r in frozen), 'invalid frozen support')
    frozen = set(frozen)
    phases = []
    for r in range(103):
        possible = [p for p in range(6) if all(bits[t] == int((t - p) % 6 >= 3) for t in range(r, 309, 103))]
        require(len(possible) == 1, 'reference is not a unique six-state phase word')
        phases.append(possible[0])
    clauses = []
    truth_cases = 0
    used_frozen = set()
    required_colors = {}
    APs = []
    for entry in data['rows']:
        ap = entry['AP']
        a, d = ap['start'], ap['difference']
        require(type(a) is int and type(d) is int and a >= 1 and d >= 1 and a + 6 * d <= 3704, 'invalid nonconstant integer AP')
        positions = [a + j * d for j in range(7)]
        if 'positions' in ap:
            require(ap['positions'] == positions, 'AP position mismatch')
        # A phase coloring is anti-periodic at 309. A term is a signed
        # occurrence of its halfword bit; this uses only the actual AP.
        raw = [(t % 309 + 1) * (1 if t % 618 < 309 else -1) for t in [n - 1 for n in positions]]
        require(not any(-v in raw for v in raw), 'tautological AP cannot be a premise')
        row = sorted(set(raw))
        reported = entry.get('signed_NAE_row')
        if reported is not None:
            require(reported == row or reported == sorted(-v for v in row), 'signed AP mismatch')
        moving = sorted({abs(v) for v in row if (abs(v) - 1) % 103 not in frozen})
        fixed_colors = {bits[abs(v) - 1] ^ (v < 0) for v in row if (abs(v) - 1) % 103 in frozen}
        require(len(fixed_colors) == 1 and moving, 'core premise must have one fixed color and free terms')
        b = next(iter(fixed_colors))
        expected = sorted(v * (1 if b == 0 else -1) for v in row if abs(v) in moving)
        require(sorted(entry['projected_clause']) == expected, 'wrong AP-to-clause premise')
        require(len(set(expected)) == len(expected), 'repeated projected literal')
        for choices in itertools.product([0, 1], repeat=len(moving)):
            assignment = dict(zip(moving, choices))
            # Direct colors at the seven integer terms, with no NAE model.
            colors = [(assignment.get(t % 309 + 1, bits[t % 309]) ^ int(t % 618 >= 309))
                      for t in [n - 1 for n in positions]]
            require((len(set(colors)) > 1) == any(assignment[abs(v)] ^ (v < 0) for v in expected),
                    'direct seven-term truth table disagrees')
            truth_cases += 1
        clauses.append(entry['projected_clause'])
        used_frozen.update((abs(v) - 1) % 103 for v in row if (abs(v) - 1) % 103 in frozen)
        for n in positions:
            t = n - 1
            r = t % 103
            if r in frozen:
                color = bits[t % 309] ^ int(t % 618 >= 309)
                required_colors[(r, t % 6)] = color
        APs.append((a, d))
    require(used_frozen == frozen, 'frozen support contains unused or missing columns')
    require(len(APs) == len(set(APs)), 'duplicate AP premise')
    allowed = {r: [p for p in range(6) if all(int((y - p) % 6 >= 3) == color
                for (s, y), color in required_colors.items() if s == r)] for r in sorted(frozen)}
    require(all(phases[r] in allowed[r] and allowed[r] for r in frozen), 'empty or incorrect permissive phase domain')
    family_size = 6 ** (103 - len(frozen))
    for permitted in allowed.values():
        family_size *= len(permitted)
    builddir.mkdir(parents=True, exist_ok=True)
    cnf = builddir / 'direct-core.cnf'
    proof = builddir / 'direct-core.lrat'
    cnf.write_text(f'p cnf 309 {len(clauses)}\n' + ''.join(' '.join(map(str, row)) + ' 0\n' for row in clauses))
    proof.write_text(data['RUP_proof_text'])
    if 'CNF_sha256' in data:
        require(sha(cnf) == data['CNF_sha256'], 'different reconstructed CNF')
    if 'RUP_proof_sha256' in data:
        require(sha(proof) == data['RUP_proof_sha256'], 'different reconstructed proof')
    verdict = verify(cnf, proof)
    require(truth_cases <= 200000 and time.monotonic() - began < 30, 'operational check budget')
    return {'agent': 'six-vdw-1', 'role': 'researcher',
        'status': 'INTEGER_AP_PREMISES_AND_COMPACT_RUP_INDEPENDENTLY_VERIFIED',
        'certificate_sha256': sha(certificate), 'frozen_columns': len(frozen), 'arbitrary_phase_columns': 103 - len(frozen),
        'AP_premises': len(clauses), 'direct_seven_term_truth_cases': truth_cases,
        'base_phase_function': phases, 'frozen_residues': sorted(frozen), 'RUP_verdict': verdict,
        'allowed_phase_sets': allowed,
        'fixed_residue_color_conditions': [{'residue': r, 'y_mod6': y, 'color': color}
                                           for (r, y), color in sorted(required_colors.items())],
        'excluded_phase_family_size': family_size,
        'claim': 'No phase coloring with a phase from the displayed allowed set at each constrained residue can be AP-free on [1,3704]; phases at every other residue are arbitrary. Keeping the exact reference phases is a subfamily.',
        'no_new_W_bound': True, 'seconds': time.monotonic() - began,
        'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate', type=Path)
    ap.add_argument('--builddir', type=Path, required=True)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    try:
        result = check(args.certificate, args.builddir)
    except (ValueError, KeyError, IndexError, TypeError) as error:
        print(json.dumps({'status': 'REJECTED', 'reason': str(error), 'mathematical_exclusion': False}))
        raise SystemExit(2)
    result['checked_at'] = datetime.now(timezone.utc).isoformat()
    if args.output:
        require(not args.output.exists(), 'output already exists')
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
