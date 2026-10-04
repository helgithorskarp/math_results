"""Exact envelope of ALL anchored q16 repair coefficients, no seed PSD audit.

The positive corner becomes this nonnegative symmetric matrix after
flipping the anchor sign. Thus its Perron root is the sharp uniform
operator-norm constant. Integer weights certify an upper bound without
floating-point eigenvalues or an imported sector decoder.
"""
import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def type_of(v):
    return (v & 7, ((v >> 3) & 255).bit_count(), (v >> 11).bit_count())


def certify_weights(envelope, weights, bound):
    require(len(weights) == len(envelope) and all(type(w) is int and w > 0 for w in weights),
            'every original weight is a strictly positive integer')
    image = [sum(a*b for a, b in zip(row, weights)) for row in envelope]
    require(all(x < bound*w for x, w in zip(image, weights)),
            'EVERY original strictly positive weighted row certificate')
    return image


def expected_failure(name, work):
    try:
        work()
    except ValueError:
        return name
    raise ValueError('Damaged mathematical condition escaped: ' + name)


def run(certificate):
    # Direct proper-member predicate, independent of bind.py's union generator.
    proper = [v for v in range(1, 1 << 19) if v.bit_count() <= 2 or
        (v.bit_count() == 3 and (v & 7).bit_count() >= 2 and
         not ((v & 6) == 6 and ((v >> 3) & 255)))]
    require(len(proper) == 231 and proper[0] == 1, 'entire original proper carrier')
    star = [i for i, v in enumerate(proper) if v & 1]
    nonstar = [i for i, v in enumerate(proper) if not v & 1]
    m = {i: sum(not proper[i] & proper[j] for j in star[1:]) for i in nonstar}
    envelope = [[0] * len(proper) for _ in proper]
    corner = [[0] * len(proper) for _ in proper]
    free = []
    for i in range(1, len(proper)):
        for j in range(i + 1, len(proper)):
            if proper[i] & proper[j]:
                continue
            require(not (i in star and j in star), 'no disjoint star/star free entry')
            free.append((i, j))
            corner[i][j] = corner[j][i] = 1
            if j in star:
                corner[i][0] -= 1
                corner[0][i] -= 1
            if i in star:
                corner[j][0] -= 1
                corner[0][j] -= 1
            envelope[i][j] = envelope[j][i] = 1
    for i, count in m.items():
        envelope[i][0] = envelope[0][i] = count
    require(all(envelope[i][j] == corner[i][j] * (-1 if (i == 0) ^ (j == 0) else 1)
                for i in range(231) for j in range(231)), 'EVERY corner-to-envelope congruence entry')
    require(all(sum(row[j] for j in star) == 0 for row in corner), 'EVERY positive-corner star action')
    require(all(i == 0 or j == 0 or not proper[i] & proper[j]
                for i, row in enumerate(envelope) for j, x in enumerate(row) if x),
            'EVERY original envelope support entry')
    histogram = sorted(Counter(m.values()).items())
    sum_m2 = sum(x*x for x in m.values())
    frobenius2 = sum(x*x for row in envelope for x in row)
    require(len(free) == 20103 and histogram == [(15,8),(16,1),(31,32),(33,2),(45,120),(48,16)]
            and sum_m2 == 314850 and frobenius2 == 2*(len(free)+sum_m2) == 669906,
            'complete literal envelope and credited Frobenius budget')
    types = sorted({type_of(v) for v in proper})
    pools = [[i for i, v in enumerate(proper) if type_of(v) == t] for t in types]
    quotient = [[sum(envelope[p[0]][j] for j in q) for q in pools] for p in pools]
    require(len(types) == 23 and sum(map(len, pools)) == 231, 'complete indicator partition')
    require(all(sum(envelope[i][j] for j in q) == quotient[a][b]
                for a, p in enumerate(pools) for i in p for b, q in enumerate(pools)),
            'ALL original equitable row sums')
    mass = list(map(len, pools))
    require(all(mass[i]*quotient[i][j] == mass[j]*quotient[j][i]
                for i in range(23) for j in range(23)), 'complete physical weighted symmetry')

    # The weights are proposed data. Their provenance (integer iteration,
    # then rounding) is unnecessary for soundness of the full row checks.
    require(certificate['actual_N'] == 232 and certificate['actual_s'] == 52 and
            certificate['types'] == [list(t) for t in types], 'entire weight/carrier/type binding')
    weights = certificate['positive_integer_weights']
    require(len(weights) == 23 and all(type(w) is int and w > 0 for w in weights),
            'entire strictly positive 23-type weight table')
    bound = certificate['strict_integer_upper']
    require(type(bound) is int and bound == 641, 'claimed envelope budget')
    image = [sum(a*b for a, b in zip(row, weights)) for row in quotient]
    upper = max(Fraction(v, w) for v, w in zip(image, weights))
    lower = Fraction(sum(n*w*v for n, w, v in zip(mass, weights, image)),
                     sum(n*w*w for n, w in zip(mass, weights)))
    require(bound-1 < lower <= upper < bound < 819, 'strict exact integer enclosure and improvement')
    w_original = [weights[types.index(type_of(v))] for v in proper]
    original_image = certify_weights(envelope, w_original, bound)
    require(Fraction(sum(w*v for w, v in zip(w_original, original_image)),
                     sum(w*w for w in w_original)) == lower, 'complete original Rayleigh lower certificate')

    def changed_corner_anchor():
        damaged = [row[:] for row in corner]
        damaged[nonstar[0]][0] += 1
        require(all(sum(row[j] for j in star) == 0 for row in damaged),
                'complete damaged-corner star action')

    def lowered_anchor_weight():
        damaged = w_original[:]
        damaged[0] = 1
        certify_weights(envelope, damaged, bound)

    def omitted_basis_edge():
        damaged = [row[:] for row in corner]
        i, j = free[0]
        damaged[i][j] = damaged[j][i] = 0
        require(all(envelope[a][b] == damaged[a][b] * (-1 if (a == 0) ^ (b == 0) else 1)
                    for a in range(231) for b in range(231)), 'complete corner congruence after a missing free direction')

    def wrong_support():
        damaged = [row[:] for row in corner]
        i, j = next((i, j) for i in range(1, 231) for j in range(i+1, 231) if proper[i] & proper[j])
        damaged[i][j] = damaged[j][i] = 1
        require(all(not proper[a] & proper[b] for a, row in enumerate(damaged)
                    for b, x in enumerate(row) if x), 'complete changed intersection support')

    damages = [
        expected_failure('nonpositive_original_weight', lambda: certify_weights(envelope, [0]+w_original[1:], bound)),
        expected_failure('insufficient_anchor_weight', lowered_anchor_weight),
        expected_failure('wrong_positive_corner_anchor', changed_corner_anchor),
        expected_failure('omitted_free_basis_edge', omitted_basis_edge),
        expected_failure('intersecting_free_entry', wrong_support),
        expected_failure('underclaimed_operator_budget_640', lambda: certify_weights(envelope, w_original, 640)),
    ]
    record = dict(agent='six-downset-2',role='researcher', proper=proper, star=star,
        nonstar=nonstar, star_neighbour_counts=[[proper[i], m[i]] for i in nonstar],
        complete_envelope=envelope, positive_corner=corner,
        types=[list(t) for t in types], physical_type_masses=mass,
        entire_equitable_quotient=quotient, positive_integer_weights=weights,
        weighted_original_image=original_image, rayleigh_lower=str(lower),
        weighted_row_upper=str(upper), strict_integer_upper=bound,
        rejected_mathematical_damages=damages)
    summary = dict(agent='six-downset-2',role='researcher', original_members=231,
        free_coordinates=len(free), corner_congruence_entries=231**2,
        equitable_original_row_sums=231*23, complete_weighted_original_rows=231,
        star_neighbour_histogram=histogram, sum_star_neighbour_squares=sum_m2,
        frobenius_squared=frobenius2, strict_Perron_root_integer_interval=[bound-1,bound],
        smallest_strict_integer_row_slack=min(bound*w-x for w,x in zip(w_original,original_image)),
        sharp_operator_envelope='largest eigenvalue of the complete nonnegative proper envelope',
        conditional_radius=str(Fraction(1,256*bound)),
        radius_factor_over_independent_Frobenius_box=str(Fraction(819,bound)),
        radius_factor_over_original_author_box=str(Fraction(2*20103,bound)),
        parent_PSD_and_gaps_reaudited=False, independently_reviewed=False,
        rejected_mathematical_damages=damages,
        sharp_envelope_does_not_claim_optimal_feasible_radius=True)
    return record, summary


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--weights', type=Path, default=Path(__file__).with_name('ENVELOPE_CERTIFICATE.json'))
    ap.add_argument('--record', type=Path, required=True)
    args=ap.parse_args()
    raw_input=args.weights.read_bytes()
    record, summary=run(json.loads(raw_input))
    raw=(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n').encode()
    args.record.write_bytes(raw)
    summary.update(record_bytes=len(raw),record_sha256=hashlib.sha256(raw).hexdigest(),
                   weights_sha256=hashlib.sha256(raw_input).hexdigest())
    print(json.dumps(summary,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
