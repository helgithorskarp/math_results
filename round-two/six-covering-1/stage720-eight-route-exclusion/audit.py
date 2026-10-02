"""Independent physical-set replay. Does not import the production checker."""
import argparse
from collections import Counter
import json
from math import gcd
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def replay(c):
    universe = set(range(720))
    labels = [m for m in range(8,721) if 720%m == 0]
    resources = [m for m in labels if m not in (8,9)]
    anchors = [[9,8],[16,9],[10,9],[15,8],[20,9],[40,9],[80,9],[45,8]]
    partition = [[10,12],[15,16],[18,20],[24,30],[36,40],[45,48],[60,72],
                 [80],[90],[120],[144],[180],[240],[360],[720]]
    require(c['schema'] == 1 and c['agent'] == 'six-covering-1' and c['role'] == 'researcher',
            'wrong evidence schema/authorship')
    require(c['period'] == 720 and c['target_moduli'] == [18,8] and c['labels'] == labels and
            c['fixed'] == [[8,5],[9,6]], 'incorrect literal problem')
    require(c['anchors'] == anchors and c['pair_partition'] == partition,
            'incorrect literal resource deductions or partition')
    require(sorted(m for group in partition for m in group) == resources,
            'partition omits/repeats original resources')
    phases = {m:[{x for x in universe if x%m == a} for a in range(m)] for m in labels}
    fixed = phases[8][5] | phases[9][6]
    raw = sum(len(phases[m][0]) for m in labels)
    present, loss, anchor_checks = {8}, 0, 0
    for m,n in anchors:
        require(m not in present and n in present and gcd(m,n) == 1,
                'sequential deduction is invalid')
        counts = {len(p&q) for p in phases[m] for q in phases[n]}
        require(counts == {720//(m*n)}, 'an actual anchor phase pair violates forced intersection')
        loss += counts.pop()
        present.add(m)
        anchor_checks += m*n
    lower = len(universe)-raw+loss
    require((raw,loss,lower) == (c['raw_mass'],c['forced_overlap'],c['hole_lower']) ==
            (654,38,104), 'wrong literal sequential mass bound')
    require(c['case_columns'] == ['a18','c8','reason','allowed_holes','demand','capacity','capacities'] and
            len(c['cases']) == 144, 'wrong or incomplete target table')
    counts, seen, combinations, pair_rows, gaps = Counter(), set(), 0, [], []
    for row in c['cases']:
        require(type(row) is list and len(row) == 7, 'malformed target evidence')
        a,b,reason,allowed,demand,capacity,caps = row
        require(type(a) is int and 0 <= a < 18 and type(b) is int and 0 <= b < 8 and
                (a,b) not in seen, 'target phases invalid or duplicated')
        seen.add((a,b))
        target = {x for x in universe if x%18 == a or x%8 == b}
        residual = universe - fixed - target
        require(allowed == len(target-fixed) and demand == len(residual), 'literal point count mismatch')
        if reason == 'hole_mass':
            require(allowed < lower and capacity is None and caps == [], 'invalid mass exclusion')
        else:
            require(reason in ('singleton','pairs'), 'invalid capacity reason')
            groups = [[m] for m in resources] if reason == 'singleton' else partition
            actual = []
            for group in groups:
                if len(group) == 1:
                    actual.append(max(len(p&residual) for p in phases[group[0]]))
                    combinations += group[0]
                else:
                    actual.append(max(len(residual & (p|q)) for p in phases[group[0]]
                                      for q in phases[group[1]]))
                    combinations += group[0]*group[1]
            require(actual == caps and sum(actual) == capacity < demand,
                    'physical actual-phase union bound fails')
            if reason == 'pairs':
                pair_rows.append([a,b,demand,capacity])
            else:
                gaps.append(demand-capacity)
        counts[reason] += 1
    require(seen == {(a,b) for a in range(18) for b in range(8)}, 'target table is incomplete')
    require(dict(counts) == {'hole_mass':56,'singleton':80,'pairs':8}, 'wrong exclusion totals')
    require(sorted(pair_rows) == [[a,1,440,437] for a in (0,2,4,8,10,12,14,16)],
            'incorrect terminal eight shapes')
    # All possible original8/9 phases admit the stated common translation.
    translations = 0
    for p in range(8):
        for q in range(9):
            shifts = [t for t in range(72) if (p+t)%8 == 5 and (q+t)%9 == 6]
            require(len(shifts) == 1, 'coprime normalization not unique')
            t = shifts[0]
            require({(x+t)%720 for x in phases[8][p]} == phases[8][5] and
                    {(x+t)%720 for x in phases[9][q]} == phases[9][6],
                    'literal normalization changes prescribed classes')
            translations += 1
    evidence = {'agent':'six-covering-1','role':'researcher','status':'CHECKED',
                'period':720,'target_moduli':[18,8],'original_labels':labels,
                'raw_mass':raw,'sequential_forced_overlap':loss,'universal_hole_lower':lower,
                'target_pairs':len(seen),'case_counts':dict(sorted(counts.items())),
                'original_phase_combinations':combinations,
                'paired_target_rows':sorted(pair_rows),'minimum_singleton_gap':min(gaps),
                'minimum_pair_gap':min(d-c for _,_,d,c in pair_rows),
                'solver_status_used':False,'global_L_min_8_bound_changed':False}
    return evidence, {'physical_anchor_phase_checks':anchor_checks,'anchor_translations':translations}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate',type=Path,default=Path(__file__).with_name('certificate.json'))
    ap.add_argument('--expected',type=Path)
    args = ap.parse_args()
    evidence, controls = replay(json.loads(args.certificate.read_text()))
    if args.expected:
        require(evidence == json.loads(args.expected.read_text()), 'frozen complete evidence differs')
    print(json.dumps({'evidence':evidence,'physical_controls':controls},sort_keys=True))
