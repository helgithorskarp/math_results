"""Check the compact necessary-domain evidence for the ordinary P>=7 proof.

No star/certificate completeness theorem is proved here. The stated external
generic unit coverage and shared-hub pair lemmas are explicit premises.
All arithmetic is exact; failure/incompletion never means nonexistence.
"""
from collections import Counter
import copy
import hashlib
import itertools
import json
from pathlib import Path
import sys
from row_types import (check_two_hub_charge, necessary_rows, need,
                       statistics, unit_graphs)

ROOT = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()


def check_pair_cases():
    found = set()
    for a,b,c in itertools.product(range(6),repeat=3):
        if a+b+c != 6:
            continue
        D = (13-c,5-b,5-a)
        if all(15-D[i]-D[j] <= 3*m
               for i,j,m in ((0,1,a),(0,2,b),(1,2,c))):
            found.add((min(a,b),max(a,b),c))
    need(found == {(1,1,4),(1,2,3)}, 'low-pair reduction')
    return sorted(found)


def aggregate_cases(types,bases):
    exceptional = [r for r in types if r[3]+r[4] > 0]
    all_records = []
    cases = []
    for a,b,c in check_pair_cases():
        D = (13-c,5-b,5-a)
        for t in (0,1):
            counts = Counter()
            records = []
            for k in range(4):
                for extra in itertools.combinations_with_replacement(exceptional,k):
                    if sum(r[3]+r[4] for r in extra) > 3-t:
                        continue
                    remaining = tuple(D[j]-sum(r[j] for r in extra) for j in range(3))
                    if min(remaining) < 0 or sum(remaining) > 15-k:
                        continue
                    z = 15-k-sum(remaining)
                    rows = list(extra)
                    for d,n in zip(((0,0,0),(1,0,0),(0,1,0),(0,0,1)),(z,)+remaining):
                        rows.extend([next(r for r in bases if r[:3] == d)]*n)
                    need(len(rows) == 15, 'aggregate row count')
                    E = sum(r[3] for r in rows)
                    Q = sum(r[4] for r in rows)
                    EH = sum(sum(max(d-1,0) for d in r[:3]) for r in rows)
                    if (E-EH) % 2 or 3-t-E-Q < 0 or (3-t-E-Q) % 2:
                        counts['parity'] += 1
                        continue
                    X = (E-EH)//2
                    need(X >= 0, 'negative excess')
                    counts['budget_valid'] += 1
                    low = tuple(sum(r[i] == r[j] == 0 for r in rows)
                                for i,j in ((0,1),(0,2),(1,2)))
                    good = tuple(sum(r[5] for r in rows if r[6+j]) for j in range(3))
                    if any(n > cap for n,cap in zip(low,(3*a-t,3*b-t,3*c-t))):
                        reason = 'low_pair_cut'
                    elif any(n > 29-X for n in good):
                        reason = 'independent_cohort_cut'
                    else:
                        reason = 'survivor'
                    counts[reason] += 1
                    records.append(dict(exceptional_rows=extra,base_counts=(z,)+remaining,
                                        E=E,Q=Q,X=X,low_pair_counts=low,
                                        good_cohort_degrees=good,reason=reason))
            need(not counts['survivor'], 'a necessary inventory survives; no exclusion')
            cases.append(dict(pair_multiplicities=(a,b,c),t=t,cross_weights=D,
                              counts=dict(counts),inventory_sha256=digest(records)))
            all_records.append(dict(pair_multiplicities=(a,b,c),t=t,records=records))
    return cases,digest(all_records)


def controls(data):
    damaged = []
    d = copy.deepcopy(data);d['fixtures'][0]['quadruples'].pop();damaged.append(d)
    d = copy.deepcopy(data);d['fixtures'][0]['quadruples'][0][0]=17;damaged.append(d)
    d = copy.deepcopy(data);d['fixtures'][0]['quadruples'][0][0]=d['fixtures'][0]['quadruples'][0][1];damaged.append(d)
    d = copy.deepcopy(data);d['fixtures'][0]['quadruples'][1]=d['fixtures'][0]['quadruples'][0];damaged.append(d)
    d = copy.deepcopy(data);d['fixtures'].pop();damaged.append(d)
    d = copy.deepcopy(data);d['fixtures'][0]['original_fixture_index']=15;damaged.append(d)
    d = copy.deepcopy(data);d['fixtures'][6]['quadruples']=d['fixtures'][0]['quadruples'];damaged.append(d)
    for d in damaged:
        try:
            unit_graphs(d)
        except RuntimeError:
            pass
        else:
            raise RuntimeError('damaged semantic fixture accepted')
    # K3+K2 is not an allowed unit high leave: its two K2 hubs cost one.
    fake = {((0,1),(1,2),(0,2),(3,4))}
    try:
        check_two_hub_charge(fake)
    except RuntimeError:
        pass
    else:
        raise RuntimeError('false two-hub charge accepted')
    # An isolated unit-deficient hub in a mixed row with a DIFFERENT
    # deficit-two point is outside the shared mixed/unit theorem.
    mixed_other = statistics((2,1,1,1),((0,1),(1,2),(0,2)),(3,4,5))
    need(mixed_other[6:] == (0,0,0), 'extra-deficit mixed row counted as a good cohort')
    return dict(damaged_fixtures_rejected=7,false_unit_leave_rejected=1,
                extra_deficit_scope_control=True,all_eight_positive_unit_fixtures_pass=True)


def main():
    raw = (ROOT/'unit_fixtures.json').read_bytes()
    data = json.loads(raw)
    dep = json.loads((ROOT/'DEPENDENCIES.json').read_bytes())
    need(hashlib.sha256(raw).hexdigest() == dep['unit_subset_sha256'], 'fixture source pin changed')
    graphs = unit_graphs(data)
    types,bases = necessary_rows(graphs)
    cases,inventory_sha = aggregate_cases(types,bases)
    result = dict(status='COMPLETE NECESSARY-DOMAIN CHECK',actual_agent='six-code-1',role='researcher',
                  unit_fixtures=8,unit_graph_types=4,unit_graphs=sorted(graphs),
                  necessary_row_types=len(types),row_statistics_sha256=digest(types),
                  zero_cost_row_types=len(bases),exceptional_row_types=len(types)-len(bases),
                  cases=cases,all_inventories_sha256=inventory_sha,
                  budget_valid_inventories=sum(c['counts']['budget_valid'] for c in cases),
                  survivors=sum(c['counts'].get('survivor',0) for c in cases),controls=controls(data))
    if '--write-expected' in sys.argv:
        (ROOT/'EXPECTED.json').write_text(json.dumps(result,indent=2)+'\n')
    else:
        expected = json.loads((ROOT/'EXPECTED.json').read_bytes())
        need(json.loads(json.dumps(result)) == expected, 'stable expected fields differ')
    print(json.dumps(dict(status=result['status'],row_types=len(types),
                          budget_valid_inventories=result['budget_valid_inventories'],survivors=result['survivors'],
                          controls=result['controls'],stable_result_sha256=digest(result))))


if __name__ == '__main__':
    main()
