"""Replay compact growth-family evidence with fresh, checked UNSAT traces.

One solver/checker runs at a time. Batches can use --start and --stop.
Generated formulas and proofs must be written to private scratch.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import subprocess
import time

from cover import build_cover, check_cover
from corona import check_witness, halo, orientations
from growth import generate_family, independent_family, serialization
from periodic import check_periodic


def decode_periodic(tile, compact):
    a, b, c = compact['lattice']
    variants = orientations(tile)
    copies = []
    for orientation, tx, ty in compact['poses']:
        if type(orientation) is not int or not 0 <= orientation < len(variants):
            raise ValueError('invalid orientation index')
        if type(tx) is not int or type(ty) is not int:
            raise ValueError('invalid translation')
        copies.append(tuple((x + tx, y + ty) for x, y in variants[orientation]))
    return {'a': a, 'b': b, 'c': c, 'copies': copies}


def fresh_decision(tile, radius, work, checker, need_unsat):
    from pysat.solvers import Solver
    circuit, candidates, stats = build_cover(tile, radius)
    cnf = work / 'case.cnf'
    proof = work / 'case.drat'
    circuit.write_dimacs(cnf)
    digest = hashlib.sha256(cnf.read_bytes()).hexdigest()
    with Solver(name='glucose4', bootstrap_with=circuit.clauses, with_proof=need_unsat) as solver:
        solver.conf_budget(10000)
        sat = solver.solve_limited()
        if sat is None:
            raise RuntimeError('UNKNOWN conflict budget 10000; verification incomplete')
        if need_unsat:
            if sat:
                raise ValueError('claimed upper obstruction is satisfiable')
            lines = solver.get_proof() or ['0']
            proof.write_text('\n'.join(lines) + '\n')
        else:
            if not sat:
                raise ValueError('claimed first-corona construction not reproduced')
            positive = {x for x in solver.get_model() if x > 0}
            patch = [tile] + [q['cells'] for q in candidates if q['variable'] in positive]
            check_cover(tile, radius, patch)
            if radius:
                # Trim the covering to copies that touch the prescribed root.
                # Every cell of its halo is still covered, so this is one corona.
                boundary = halo(tile)
                ranked = [{'level': 0, 'cells': tile}] + [
                    {'level': 1, 'cells': q} for q in patch[1:] if boundary.intersection(q)]
                check_witness(tile, 1, ranked, strict_disc=True, holes_last=True)
    if need_unsat:
        result = subprocess.run([str(checker), str(cnf), str(proof)],
                                capture_output=True, text=True, timeout=30)
        # DRAT-trim uses return code 1 for trivial input-CNF UNSAT.
        lines = result.stdout.replace('\r', '\n').splitlines()
        if result.returncode not in (0, 1) or 's VERIFIED' not in lines:
            raise RuntimeError('UNSAT proof not verified: ' + result.stdout[-1000:] + result.stderr[-1000:])
    return digest, stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    directory = Path(__file__).parent
    parser.add_argument('--manifest', type=Path, default=directory / 'growth20_manifest.json')
    parser.add_argument('--checker', type=Path, required=True, help='inspected DRAT-trim executable')
    parser.add_argument('--work-dir', type=Path, required=True)
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--stop', type=int)
    parser.add_argument('--independent-family', action='store_true')
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    seed = json.loads((directory / 'kaplan17.json').read_text())['cells']
    family, sizes = generate_family(seed, 3)
    if hashlib.sha256(serialization(family).encode()).hexdigest() != manifest['family_sha256']:
        raise ValueError('family hash mismatch')
    if args.independent_family:
        independent, _ = independent_family(seed, 3)
        if independent != family:
            raise ValueError('independent family enumeration mismatch')
    records = manifest['cases']
    if [r['i'] for r in records] != list(range(len(family))):
        raise ValueError('manifest must cover the whole ordered family exactly once')
    end = len(family) if args.stop is None else args.stop
    if not 0 <= args.start <= end <= len(family):
        raise ValueError('invalid batch range')
    work = args.work_dir.resolve()
    work.mkdir(parents=True, exist_ok=True)
    checker = args.checker.resolve()
    counts = collections.Counter()
    started = time.monotonic()
    for record in records[args.start:end]:
        tile = family[record['i']]
        if 'periodic' in record:
            cert = decode_periodic(tile, record['periodic'])
            checked = check_periodic(tile, cert)
            counts[f"periodic_{checked['copies']}_copies"] += 1
        else:
            radius = record['radius']
            digest, _ = fresh_decision(tile, radius, work, checker, need_unsat=True)
            if digest != record['cnf_sha256']:
                raise ValueError('upper-obstruction formula hash mismatch')
            lower_radius = record.get('lower_radius', radius - 1)
            fresh_decision(tile, lower_radius, work, checker, need_unsat=False)
            counts[f'Hh_upper_{radius-1}'] += 1
        if (record['i'] + 1) % 100 == 0:
            print(json.dumps({'through': record['i'], 'counts': dict(sorted(counts.items())),
                              'seconds': round(time.monotonic() - started, 3)}), flush=True)
    expected = collections.Counter()
    for record in records[args.start:end]:
        if 'periodic' in record:
            expected[f"periodic_{len(record['periodic']['poses'])}_copies"] += 1
        else:
            expected[f"Hh_upper_{record['radius']-1}"] += 1
    assert counts == expected
    print(json.dumps({'start': args.start, 'stop': end, 'counts': dict(sorted(counts.items())),
                      'all_upper_proofs_checked': True, 'all_periodic_certificates_checked': True,
                      'first_coronas_checked_for_positive_bounds': True,
                      'covering_lower_bounds_checked': True,
                      'seconds': round(time.monotonic() - started, 3)}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
