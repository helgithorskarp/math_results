"""One serial bounded exact replay; whole EXPECTED comparison under normal/O."""
from pathlib import Path
from fractions import Fraction as F
import argparse
import json
import pins
from variance import require, bound, scalar_record, digest
from algebra import run as algebra
from entries import parameters, certificate
from point import run as point
from baseline import original, whole
from controls import run as controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit-candidate', action='store_true')
    args = parser.parse_args()
    finite = []
    for k in range(5, 19):
        for q in range(bound(k)-4, 6*k):
            r = scalar_record(q, k)
            if (q, k) != (24, 6):
                require(F(r['strict_scalar_margin']) > 0, 'every finite positive sufficient variance')
                parameters(q, k)
            finite.append(r)
    failures = [r for r in finite if F(r['strict_scalar_margin']) <= 0]
    require(len(finite) == 192 and [(r['q'], r['k']) for r in failures] == [(24, 6)],
            'complete finite closure and sole failed sufficient estimate')
    pell = []
    p, u = 8, 3
    for n in range(1, 9):
        require(p*p-7*u*u == 1, 'exact Pell norm')
        if n >= 2:
            k, b = u+1, 3*u+p
            require(bound(k) == b, 'credited actual Pell upper-root floor')
            for q in range(b-5, b+1):
                r = parameters(q, k)
                require(F(r['strict_scalar_margin']) > 0, 'each complete Pell-corridor variance cap')
                pell.append(r)
        p, u = 8*p+21*u, 3*p+8*u
    exception, state = point(return_state=True)
    baseline = [original(5, 3), original(8, 3)]
    wh = [whole(19, 5), whole(24, 6, state)]
    large = []
    for q, k in ((30, 5), (114, 19), (1000000, 100000)):
        p, entry = certificate(q, k)
        # At most two outside bits are examined, and no whole domain is allocated.
        require(entry(1, 1) == 0 and entry(1, 3) == 0 and entry(0, 1) == entry(1, 0),
                'large scalar/entry samples retain support and symmetry')
        large.append({'parameters': p, 'M_empty_empty': str(entry(0, 0)),
                      'M_empty_a': str(entry(0, 1)), 'sample_only': True})
    record = {'agent': 'six-downset-3', 'role': 'researcher',
              'domain': 'Every integer k>=5,q>=max(4,k), every deletion setZ',
              'positive_coverage': 'q>=b(k)-4; Pell n>=2 iff q>=b(k)-5; generic exact m>0 criterion',
              'maximum_remaining_threshold_width': 1,
              'uniform_threshold_sharpness': {'positive_bound_cannot_extend_to_b_minus5':
                                             'k6,q23 excluded by exact Q0 and all-real9434 premise',
                                             'negative_bound_cannot_extend_to_b_minus5':
                                             'every Pell n>=2 has a full positive certificate at b-5'},
              'finite_closure': finite, 'failed_sufficient_estimates': failures,
              'algebra': algebra(), 'Pell_calibrations_only': pell,
              'original_row_baselines': baseline, 'exceptional_point': exception,
              'whole_entry_baselines': wh, 'large_entry_calibrations_only': large,
              'controls': controls(state), 'pins': pins.PINS,
              'trust_boundary': 'Ordinary counting/Schur/norm/completeness/lift/Pell bridges;9195 full endpoints and lower repair,9478 negatives and9508 Pell identities credited; no B0-positive constructive-tail criterion used; unformalized and independently unreviewed'}
    record['record_sha256'] = digest(record)
    if not args.emit_candidate:
        expected = json.loads((Path(__file__).resolve().parent/'EXPECTED.json').read_text())
        require(record == expected, 'entire frozen mathematical record')
    print(json.dumps(record, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
