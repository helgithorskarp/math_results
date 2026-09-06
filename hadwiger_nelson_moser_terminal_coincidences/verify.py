"""No code imports: squarefree-radical audit of every new pair and list case."""
import argparse, hashlib, json, math, time
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'hadwiger_nelson_moser_all_terminal_contacts/certificate.json'
PRIOR_SHA = 'bddb9275204535cccce1d66bd2ad1415040a6807fdffb7902dec31fd57126a98'
RADICANDS = (1, 3, 11, 33)

def need(ok, message):
    if not ok:
        raise ValueError(message)

def norm(a, b):
    # Coordinates are numerator vectors over12. sqrt(r)*sqrt(s) equals
    # gcd(r,s)*sqrt(r*s/gcd(r,s)^2) for positive squarefree r,s.
    total = {r: 0 for r in RADICANDS}
    for axis in (0, 1):
        diff = [x - y for x, y in zip(a[axis], b[axis])]
        for i, r in enumerate(RADICANDS):
            for j, s in enumerate(RADICANDS):
                common = math.gcd(r, s)
                total[r*s // (common*common)] += diff[i] * diff[j] * common
    return [total[r] for r in RADICANDS]

def audit(cert, prior):
    need(cert['prior_sha256'] == PRIOR_SHA, 'wrong prior hash')
    need(cert['squared_distance_scale'] == 144 and cert['basis'] == ['1', 'sqrt3', 'sqrt11', 'sqrt33'], 'wrong field')
    M = prior['M']
    D = [prior['C'][i] for i in prior['D_indices']]
    need(len(M) == 7 and len(D) == 18, 'wrong inherited domains')
    actual = {
        'M_M': [[i, j, *norm(M[i], M[j])] for i, j in combinations(range(7), 2)],
        'M_D': [[i, j, *norm(M[i], D[j])] for i in range(7) for j in range(18)],
    }
    counts = {}
    for domain, rows in actual.items():
        need(cert[domain] == rows, domain + ' entry mismatch')
        counts[domain + '_pair_norms'] = len(rows)
        for label, squared in (('sqrt7', 7), ('distance3', 9)):
            hits = [row[:2] for row in rows if row[2:] == [144*squared, 0, 0, 0]]
            need(not hits, domain + ' has a forbidden long pair')
            counts[domain + '_' + label + '_pairs'] = len(hits)
    return counts

def palette_audit():
    palette = set(range(4))
    forbidden = [set()] + [{c} for c in range(4)]
    counts = {}
    for b in (1, 2):
        cases = 0
        minimum = 4
        for initial in forbidden:
            for anchors in product(range(4), repeat=b):
                remaining = palette - initial - set(anchors)
                need(len(remaining) >= 3-b > 2-b, 'anchored list surplus failed')
                minimum = min(minimum, len(remaining))
                cases += 1
        counts[str(b)] = {'cases': cases, 'minimum_list_size': minimum, 'maximum_auxiliary_degree': 2-b}
    # The singleton case must be accepted, not silently excluded by a
    # global at-least-two-lists premise.
    need(palette - {0} - {1, 2} == {3}, 'singleton boundary')
    return {'anchored_palette_cases': sum(v['cases'] for v in counts.values()),
            'by_anchored_B_multiplicity': counts, 'shared_endpoint_singleton_checked': True}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True)
    args = parser.parse_args()
    start = time.monotonic()
    prior_raw = PRIOR.read_bytes()
    need(hashlib.sha256(prior_raw).hexdigest() == PRIOR_SHA, 'inherited input changed')
    prior = json.loads(prior_raw)
    raw = (HERE / 'certificate.json').read_bytes()
    cert = json.loads(raw)
    result = {**audit(cert, prior), **palette_audit()}
    for label in ('pair_value', 'missing_pair', 'prior_hash'):
        bad = json.loads(raw)
        if label == 'pair_value':
            bad['M_D'][0][2] += 1
        elif label == 'missing_pair':
            bad['M_M'].pop()
        else:
            bad['prior_sha256'] = '0' * 64
        try:
            audit(bad, prior)
        except ValueError:
            pass
        else:
            raise ValueError('malformed certificate accepted: ' + label)
    result.update({'status': 'PASS', 'exact_pair_norms': 147,
                   'malformed_certificate_rejections': 3, 'native_solver_calls': 0,
                   'certificate_bytes': len(raw), 'certificate_sha256': hashlib.sha256(raw).hexdigest()})
    if (HERE / 'expected.json').exists():
        need(result == json.loads((HERE / 'expected.json').read_text()), 'expected mismatch')
    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    (work / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({**result, 'seconds': time.monotonic() - start}, sort_keys=True))

if __name__ == '__main__':
    main()
