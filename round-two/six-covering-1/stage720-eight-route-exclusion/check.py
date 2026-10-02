"""Reconstruct every original phase capacity; no solver or external input."""
import argparse
from collections import Counter
import json
from math import gcd
from pathlib import Path

N = 720
LABELS = [m for m in range(8, N + 1) if N % m == 0]
FREE = [m for m in LABELS if m not in (8, 9)]
ANCHORS = [[9,8],[16,9],[10,9],[15,8],[20,9],[40,9],[80,9],[45,8]]
PAIRS = [[FREE[i], FREE[i+1]] for i in range(0,14,2)] + [[m] for m in FREE[14:]]
FULL = (1 << N) - 1
MASKS = {m: [sum(1 << x for x in range(a,N,m)) for a in range(m)] for m in LABELS}
FIXED = MASKS[8][5] | MASKS[9][6]


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def capacities(R, partition):
    flat = [m for group in partition for m in group]
    require(sorted(flat) == FREE, 'partition repeats or omits an original label')
    caps, combinations = [], 0
    for group in partition:
        require(len(group) in (1,2), 'invalid resource group')
        if len(group) == 1:
            masks = MASKS[group[0]]
        else:
            masks = (p | q for p in MASKS[group[0]] for q in MASKS[group[1]])
        maximum = 0
        for mask in masks:
            combinations += 1
            maximum = max(maximum, (mask & R).bit_count())
        caps.append(maximum)
    return caps, combinations


def replay(c):
    require(c['schema'] == 1 and c['agent'] == 'six-covering-1' and c['role'] == 'researcher',
            'wrong evidence schema or actual authorship')
    require(c['period'] == N and c['target_moduli'] == [18,8] and c['labels'] == LABELS and
            c['fixed'] == [[8,5],[9,6]], 'wrong period, target or original labels/phases')
    require(c['anchors'] == ANCHORS and c['pair_partition'] == PAIRS,
            'wrong sequential anchors or resource partition')
    raw, present, loss = sum(N//m for m in LABELS), {8}, 0
    for m,n in ANCHORS:
        require(m not in present and n in present and gcd(m,n) == 1,
                'forced deduction does not belong to a new original label')
        loss += N//(m*n)
        present.add(m)
    hole_lower = N - raw + loss
    require((raw,loss,hole_lower) == (c['raw_mass'],c['forced_overlap'],c['hole_lower']) ==
            (654,38,104), 'wrong sequential union bound')
    require(c['case_columns'] == ['a18','c8','reason','allowed_holes','demand','capacity','capacities'],
            'wrong case format')
    require(len(c['cases']) == 144, 'incomplete eighteen-by-eight target domain')
    counts, seen, phase_combinations, pair_rows, scalar_gaps = Counter(), set(), 0, [], []
    for row in c['cases']:
        require(type(row) is list and len(row) == 7, 'malformed target row')
        a,c8,reason,allowed,demand,capacity,caps = row
        require(type(a) is int and 0 <= a < 18 and type(c8) is int and 0 <= c8 < 8 and
                (a,c8) not in seen, 'noncanonical or duplicated target pair')
        seen.add((a,c8))
        U = sum(1 << x for x in range(N) if x%18 == a or x%8 == c8)
        R = FULL & ~(FIXED | U)
        require(allowed == (U & ~FIXED).bit_count() and demand == R.bit_count(),
                'declared literal target/residual counts differ')
        if reason == 'hole_mass':
            require(allowed < hole_lower and capacity is None and caps == [],
                    'hole-mass comparison does not exclude')
        else:
            require(reason in ('singleton','pairs'), 'unknown exclusion type')
            partition = [[m] for m in FREE] if reason == 'singleton' else PAIRS
            actual, combinations = capacities(R,partition)
            require(caps == actual and capacity == sum(actual) and capacity < demand,
                    'exact original-phase capacity does not strictly exclude')
            phase_combinations += combinations
            if reason == 'pairs':
                pair_rows.append([a,c8,demand,capacity])
            else:
                scalar_gaps.append(demand-capacity)
        counts[reason] += 1
    require(seen == {(a,b) for a in range(18) for b in range(8)}, 'missing target pair')
    require(dict(counts) == {'hole_mass':56,'singleton':80,'pairs':8}, 'wrong case counts')
    require(sorted(pair_rows) == [[a,1,440,437] for a in (0,2,4,8,10,12,14,16)],
            'wrong final paired target domain or exact capacities')
    return {'agent':'six-covering-1','role':'researcher','status':'CHECKED',
            'period':N,'target_moduli':[18,8],'original_labels':LABELS,
            'raw_mass':raw,'sequential_forced_overlap':loss,'universal_hole_lower':hole_lower,
            'target_pairs':len(seen),'case_counts':dict(sorted(counts.items())),
            'original_phase_combinations':phase_combinations,
            'paired_target_rows':sorted(pair_rows),'minimum_singleton_gap':min(scalar_gaps),
            'minimum_pair_gap':min(d-c for _,_,d,c in pair_rows),
            'solver_status_used':False,'global_L_min_8_bound_changed':False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate',type=Path,default=Path(__file__).with_name('certificate.json'))
    ap.add_argument('--expected',type=Path)
    args = ap.parse_args()
    evidence = replay(json.loads(args.certificate.read_text()))
    if args.expected:
        require(evidence == json.loads(args.expected.read_text()), 'frozen complete evidence differs')
    print(json.dumps(evidence,sort_keys=True))
