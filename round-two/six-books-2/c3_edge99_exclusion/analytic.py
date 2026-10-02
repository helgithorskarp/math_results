"""Integer checks for the new ordinary C3/E99 deficit and parity arguments.

Prior all-nine/one-pair/two-pair exclusions are explicit theorem premises,
not computations performed by this file. No graph enumeration proves the
new argument; PROOF.md supplies its ordinary counting bridges.
"""
from collections import Counter
from itertools import combinations_with_replacement, product
from math import factorial


def choose2(n):
    return n*(n-1)//2


def labeled_marks(counts):
    """All ordered degree marks, by remaining-multiplicity recursion."""
    out = []
    def visit(prefix, remaining):
        if len(prefix) == 7:
            if any(remaining.values()):
                raise ValueError('Nonempty terminal multiset')
            out.append(tuple(prefix))
            return
        for degree in sorted(remaining):
            if remaining[degree]:
                remaining[degree] -= 1
                visit(prefix+[degree], remaining)
                remaining[degree] += 1
    visit([], dict(counts))
    return out


def derive():
    histograms = []
    all_marks = []
    admissible = []
    for b in range(3):
        for a in range(4):
            if 2*a+3*b > 7:
                continue
            c = a+2*b
            n9 = 7-2*a-3*b
            counts = {7:b, 8:a, 9:n9, 10:c}
            variance = 6*a+18*b
            W = 33-9*a-27*b
            marks = labeled_marks(counts)
            expected_count = factorial(7)
            for value in counts.values():
                expected_count //= factorial(value)
            if len(marks) != expected_count or any(sum(m)!=63 for m in marks):
                raise ValueError('Degree composition coverage mismatch')
            all_marks.extend(marks)
            if W >= 0:
                admissible.extend(marks)
            histograms.append(dict(a=a, b=b, free_degree_counts={str(k):v for k,v in counts.items()},
                                   variance=variance, deficit_weight=W,
                                   ordered_placements=len(marks), retained=W>=0))

    new_placements = []
    for a,b in [(0,1),(3,0)]:
        histogram = next(r for r in histograms if r['a']==a and r['b']==b)
        marks = labeled_marks({int(k):v for k,v in histogram['free_degree_counts'].items()})
        patterns = Counter()
        rejection = Counter()
        for degrees in marks:
            D_A = 3*sum(degrees[:3])
            if D_A > 81:
                rejection['root_cut'] += 1
                continue
            root_deficit = 165-2*D_A
            if root_deficit > 6:
                rejection['root_budget'] += 1
                continue
            if D_A != 81 or root_deficit != 3:
                raise ValueError('New-profile root bridge failed')
            patterns[tuple(sorted(degrees[:3]))+tuple(sorted(degrees[3:]))] += 1
        new_placements.append(dict(a=a,b=b,ordered_placements=len(marks),
                                   rejected=dict(rejection),
                                   survivors=[dict(A=list(key[:3]),B=list(key[3:]),
                                                   ordered_placements=value)
                                              for key,value in sorted(patterns.items())]))

    local_degrees = [v for v in product(range(4), repeat=3) if sum(v)==8]
    if sorted(local_degrees) != [(2,3,3),(3,2,3),(3,3,2)]:
        raise ValueError('Complete local degree scalar domain')
    capacity_cases = []
    for degrees, ranks, W in [((7,10,10),(4,4,4,4),6),
                              ((8,9,10),(3,3,5,5),6)]:
        overlap = 3*sum(choose2(s) for s in ranks)
        for h in local_degrees:
            cap = 108-12-3*sum((d-9)*v for d,v in zip(degrees,h))
            cap -= 3*sum(choose2(v) for v in h)
            slack = cap-overlap
            if slack < 0:
                reason = 'capacity_below_actual_overlap'
            elif degrees[0]==7:
                if slack+3 <= W:
                    raise ValueError('Exceptional deficit contradiction failed')
                reason = 'A_pair_slack_plus_root_exceeds_total_budget'
            else:
                if h != (3,3,2) or slack != 0:
                    raise ValueError('Three-pair tightness failed')
                reason = 'all_A_pairs_tight_then_odd_column_parity'
            capacity_cases.append(dict(A=list(degrees),B_column_ranks=list(ranks),
                                       H_orbit_degrees=list(h),capacity=cap,
                                       actual_overlap=overlap,slack=slack,
                                       root_deficit=3,total_deficit=W,reason=reason))
    all_nine = dict(A=[9,9,9],B=[7,9,10,10],B_column_ranks=[2,4,5,5],
                    capacity=75,actual_overlap=81)
    if all_nine['capacity'] >= all_nine['actual_overlap']:
        raise ValueError('Exceptional all-nine contradiction failed')

    parity_cases = []
    for ell in [0,2]:
        for high_neighbors in range(4-ell):
            baseline = 8*(8-15)+(81-8)
            red_adjustment = ell-high_neighbors
            common_H_sum = 6-high_neighbors
            pair_capacity_sum = baseline+red_adjustment-common_H_sum
            gram_row_sum = 4+pair_capacity_sum
            if baseline != 17 or pair_capacity_sum != 11+ell:
                raise ValueError('Low-row capacity identity')
            if gram_row_sum%2 == 4%2:
                raise ValueError('Odd-column parity obstruction failed')
            parity_cases.append(dict(low_internal_neighbors=ell,
                                     high_neighbors=high_neighbors,
                                     pair_capacity_sum=pair_capacity_sum,
                                     tight_Gram_row_sum=gram_row_sum,
                                     odd_column_required_parity=0))

    record = dict(schema=1, agent='six-books-2',role='researcher',
                  histograms=histograms,total_ordered_degree_placements=len(all_marks),
                  retained_ordered_degree_placements=len(admissible),
                  new_profile_root_placements=new_placements,
                  exceptional_all_nine=all_nine,
                  marked_capacity_cases=capacity_cases,low_row_parity_cases=parity_cases,
                  premise_roles=['7526: classification-free lower7',
                                 '8012: classification-free upper10',
                                 '9453: all-nine C3 conditional exclusion',
                                 '9510: one-pair C3 conditional exclusion',
                                 '9554: two-pair C3 conditional exclusion',
                                 '8971: only for the e=102 family corollary'])
    return record, sorted(all_marks), sorted(admissible)
