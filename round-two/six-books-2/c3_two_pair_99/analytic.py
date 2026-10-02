"""Exact scalar checks for ordinary counting bridges, not a host census."""
from argparse import ArgumentParser
from itertools import product
from pathlib import Path
import json, resource, time


def choose2(value):
    return value * (value - 1) // 2


def balanced(total, columns=12):
    quotient, remainder = divmod(total, columns)
    return columns * choose2(quotient) + remainder * quotient


def derive():
    # Separate exact dynamic program over all twelve labeled column loads.
    # Loads are in 0..9, so it covers every total from 0 through 108.
    dp = {0: 0}
    for _ in range(12):
        new = {}
        for total, cost in dp.items():
            for load in range(10):
                new_total = total + load
                new[new_total] = min(new.get(new_total, 10**9), cost + choose2(load))
        dp = new
    if set(dp) != set(range(109)) or any(dp[t] != balanced(t) for t in dp):
        raise ValueError('Complete scalar balancing formula/DP mismatch')
    ordinary = []
    for low_count in range(3, 10):
        cases = []
        for h in range(12 - low_count, 14):
            cut = 72 - low_count - 2*h
            upper = 135 - 5*low_count - 5*h
            lower = dp[cut]
            if upper >= lower:
                raise ValueError('Ordinary low-neighborhood contradiction failed')
            cases.append(dict(H_edges=h, cut=cut, capacity_upper=upper,
                              overlap_lower=lower, gap=lower-upper))
        ordinary.append(dict(low_neighbors=low_count, cases=cases))

    h9 = []
    for low1, low2, high in product(range(4), repeat=3):
        if low1 + low2 + high != 6:
            continue
        common_total = 3*sum(choose2(v) for v in (low1, low2, high))
        cap = 84-9 + 3*(low1+low2-high) - common_total
        h9.append(dict(orbit_degrees=[low1, low2, high], capacity=cap))
    if len(h9) != 10 or max(r['capacity'] for r in h9) != 75:
        raise ValueError('Complete H9 local degree profiles differ')
    if max(r['capacity'] for r in h9) >= dp[51]:
        raise ValueError('L H9 contradiction failed')
    h12 = []
    for degrees in product(range(4), repeat=3):
        if sum(degrees) != 8:
            continue
        cap = 84-12 + 3*(degrees[0]+degrees[1]-degrees[2])
        cap -= 3*sum(choose2(v) for v in degrees)
        h12.append(dict(orbit_degrees=list(degrees), capacity=cap))
    if sorted((r['orbit_degrees'][2], r['capacity']) for r in h12) != [(2,63),(3,57),(3,57)]:
        raise ValueError('Complete H12 marked capacities differ')

    # These scalar identities audit the two ordinary equality arguments in
    # PROOF.md. They do not enumerate all local adjacency matrices by themselves.
    high_row_sum = 10-1-2
    low_row_sum = 8-1-3
    cut = 6*low_row_sum + 3*high_row_sum
    low_cut = 6*low_row_sum
    low_internal_edges = (6*3 - 3*2)//2
    low_common_lower = 6*choose2(2) + 3*choose2(2)
    low_capacity_upper = choose2(6) + low_internal_edges - low_common_lower
    quotient, remainder = divmod(cut, 12)
    high_norm_from_caps = 3*high_row_sum + 2*choose2(3)*5
    high_norm_from_columns = (12-remainder)*(quotient-2)**2 + remainder*(quotient+1-2)**2
    equality = dict(H_edges=12, K_edges=33, cut=cut,
                    all_pair_capacity=63, all_overlap_lower=dp[cut],
                    high_triangle_capacity=3*(2-1), high_overlap_lower=dp[3*high_row_sum],
                    low_internal_edges=low_internal_edges,
                    low_pair_capacity_upper=low_capacity_upper,
                    low_overlap_lower=dp[low_cut],
                    balanced_all_columns=[quotient]*(12-remainder)+[quotient+1]*remainder,
                    balanced_low_columns=[2]*12,
                    high_norm_from_tight_pair_caps=high_norm_from_caps,
                    high_norm_from_column_loads=high_norm_from_columns)
    if not (cut == 45 and dp[cut] == 63 and low_capacity_upper == dp[low_cut] == 12
            and equality['high_triangle_capacity'] < equality['high_overlap_lower']
            and high_norm_from_caps == 51 and high_norm_from_columns == 39):
        raise ValueError('L H12 equality obstruction failed')
    all_nine = dict(A_degrees=[9]*9, H_edges=12, K_edges=30,
                    B_orbit_degrees=[8,8,10,10], B_column_ranks=[3,3,5,5],
                    overlap=3*sum(choose2(v) for v in (3,3,5,5)),
                    capacity=108-12-3*(choose2(2)+2*choose2(3)))
    if all_nine['overlap'] <= all_nine['capacity']:
        raise ValueError('All-nine A contradiction failed')
    return dict(schema=1, agent='six-books-2', role='researcher',
                statement='Ordinary E<=99 root9 with r degree8 neighbors and 9-r degree9 neighbors is impossible for every 3<=r<=9, without symmetry or outside degree conditions.',
                all_109_balancing_totals_DP_equal=True, ordinary_low_neighborhoods=ordinary,
                A_all_nine=all_nine, A_8_8_10_H9=h9, A_8_8_10_H12=h12,
                L12_equality_obstruction=equality,
                trust='Exact scalar checks; ordinary counting and equality bridges are written in PROOF.md and remain unformalized. Not a complete host census.')


def main():
    parser = ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    work = parser.parse_args().work
    work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    record = derive()
    (work/'analytic.json').write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(dict(status='COMPLETE_TWO_PAIR_SCALAR_BRIDGES',
                         ordinary_cases=sum(len(r['cases']) for r in record['ordinary_low_neighborhoods']),
                         seconds=time.monotonic()-start,
                         peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss), indent=2))


if __name__ == '__main__':
    main()
