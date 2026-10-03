"""Full physical/set reconstruction of the pass128 coupling record.

No import of the producer. Five-label subsets, followed by a pair/triple
partition, replace its pair-first enumeration. Exact physical APs replace
its product formula. Every mathematical field is compared, not just maxima.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(record):
    return sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def rebuild():
    ds = sorted({d for d in range(1,316) if 315 % d == 0})
    unused = ds[1:]
    period = set(range(2520))
    for modulus, phase in ((8,0),(9,0),(10,1),(14,0),(12,10),(28,4)):
        period.difference_update(range(phase,2520,modulus))
    parents = {r:{x for x in period if x % 8 == r} for r in range(1,8)}
    require([len(parents[r]) for r in range(1,8)] == [224,150,224,200,224,150,224],
            'Literal six-BASE shadows changed')
    phase_rows = []
    maxima = {}
    for r in range(1,8):
        for d in ds:
            counts = [len(parents[r].intersection(range(a,2520,d))) for a in range(d)]
            phase_rows.append([r,d,counts])
            maxima[r,d] = max(counts)
    C = {d:maxima[2,d] for d in ds}
    require(C == {d:maxima[6,d] for d in ds}, 'Marked shadows differ')
    rows = []
    for labels in combinations(unused,5):
        for pair in combinations(labels,2):
            triple = sorted(set(labels).difference(pair))
            for r in (1,3,4,5,7):
                shadow = maxima[r,lcm(*pair)]
                marked = sum(C[d] for d in triple)
                rows.append([r,*pair,*triple,shadow,marked,shadow+marked])
    rows.sort(key=lambda row:row[:6])
    require(len(rows) == 5*462*10 == 23100, 'Five-label partitions incomplete')
    coupled = {str(r):max(row[-1] for row in rows if row[0] == r) for r in (1,3,4,5,7)}
    require(coupled == {'1':166,'3':166,'4':165,'5':166,'7':166}, 'Coupling changed')

    controls = []
    for r in (1,3,4,5,7):
        x = min(parents[r])
        lifts = [x+2520*k for k in range(4)]
        for types in ('HHH','HHQ','HQQ','QQQ'):
            domains = [(0,5,10) if t == 'H' else (0,1,2,4,8) for t in types]
            for states in product(*domains):
                physical_union = set()
                observed = []
                for d, kind, state in zip((3,5,7),types,states):
                    two = {'H':16,'Q':32}[kind]
                    first_lift = next((i for i in range(4) if state & (1 << i)),0)
                    binary = lifts[first_lift] % two
                    odd = (x+int(state == 0)) % d
                    phase = next(binary+two*j for j in range(d) if (binary+two*j) % d == odd)
                    ap = set(range(phase,10080,two*d))
                    observed.append(sum(1 << k for k,y in enumerate(lifts) if y in ap))
                    physical_union.update(ap)
                require(observed == list(states), 'Actual AP state construction changed')
                covered = set(lifts).issubset(physical_union)
                if covered:
                    if types == 'HHH':
                        require({5,10}.issubset(states), 'Three-half coverage condition missing')
                    elif types == 'HHQ':
                        require(set(states[:2]) == {5,10}, 'Quarter repairs equal/inactive halves')
                    elif types == 'HQQ':
                        require(0 not in states, 'Mixed three-class active condition missing')
                    else:
                        raise ValueError('Three quarter classes cover four physical lifts')
                controls.append([r,types,list(states),covered])
    require(len(controls) == 1360, 'Unmarked controls incomplete')
    S1 = max(C[d] for d in unused)
    S2 = max(sum(C[d] for d in pair) for pair in combinations(unused,2))
    I2 = max(C[lcm(*pair)] for pair in combinations(unused,2))
    I3 = max(C[lcm(*triple)] for triple in combinations(unused,3))
    require((S1,S2,I2,I3) == (90,120,30,18), 'Imported local capacities changed')
    cases = []
    for r in (1,3,4,5,7):
        pair = max(maxima[r,lcm(*labels)] for labels in combinations(unused,2))
        type_rows = {
            '2+4+2': [('HHQ',coupled[str(r)]),('HQQ',S2+pair),('QQQ',S1+I3+pair)],
            '3+3+2': [('HH / HQ',coupled[str(r)]),('HQ / HQ',S2+pair),('QQ / HQ',I2+S1+pair)],
            '2+3+3': [('HHH',S2+2*pair),('HHQ',S2+pair),('HQQ',S2+pair)]}
        for counts, inventory in type_rows.items():
            for types, bound in inventory:
                cases.append([r,counts,types,bound])
    require(len(cases) == 45 and max(row[-1] for row in cases) == 176,
            'Complete three-parent capacity changed')
    return {
        'agent':'six-covering-2','role':'researcher',
        'status':'AUTHOR-CHECKED two-parent reduction; not part of actual9978',
        'full_marked_prefix':[[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]],
        'essential_originals_explicit':[16,32],
        'whole_physical_phase_rows':phase_rows,
        'all_global_five_extra_H_coupling_rows':rows,'coupled_maxima':coupled,
        'complete_literal_three_class_controls':controls,
        'all_three_parent_eight_tail_cases':cases,
        'maximum_three_parent_eight_tail_BASE_holes':176,
        'BASE_holes_lower_bound_imported_from_public9934':177,
        'exactly_eight_productive_TAILs_imply_exactly_two_hole_parents':True,
        'remaining_two_parent_counts':[[2,6],[3,5],[4,4],[5,3]],
        'capacity_sharpness_claimed':False,'ordinary_proof_formalized':False,
        'independent_reviewer':False,'global_bound_changed':False}


def audit(candidate):
    reference = rebuild()
    require(candidate == reference, 'Whole record differs from independent physical reconstruction')
    # Damage a full already-rebuilt reference; restoration is checked each time.
    damages = []
    def probe(name, change, restore):
        change()
        require(candidate != reference, 'Semantic corruption was accepted: '+name)
        damages.append(name)
        restore()
        require(candidate == reference, 'Record not restored after: '+name)

    for field, replacement in (
        ('full_marked_prefix',[[8,0],[9,0],[10,1],[14,1],[12,10],[16,2],[28,4],[32,6]]),
        ('essential_originals_explicit',[16]),
        ('remaining_two_parent_counts',[[2,6],[3,5],[4,4]]),
        ('maximum_three_parent_eight_tail_BASE_holes',175),
        ('global_bound_changed',True)):
        old = candidate[field]
        probe(field,lambda f=field,v=replacement:candidate.__setitem__(f,v),
              lambda f=field,v=old:candidate.__setitem__(f,v))
    for field, label in (
        ('whole_physical_phase_rows','last-phase'),
        ('all_global_five_extra_H_coupling_rows','last-five-label-row'),
        ('all_three_parent_eight_tail_cases','last-allocation')):
        row = candidate[field][-1]
        if field == 'whole_physical_phase_rows':
            row = row[-1]
        old = row[-1]
        probe(label,lambda row=row,old=old:row.__setitem__(-1,old+1),
              lambda row=row,old=old:row.__setitem__(-1,old))
    row = candidate['complete_literal_three_class_controls'][0]
    old = row[-1]
    probe('inactive-classes-cover',lambda:row.__setitem__(-1,True),lambda:row.__setitem__(-1,old))
    row = candidate['all_global_five_extra_H_coupling_rows']
    old = row[-1]
    probe('omitted-label-partition',lambda:row.pop(),lambda:row.append(old))
    return {'agent':'six-covering-2','role':'researcher',
            'every_full_mathematical_field_compared':True,
            'whole_record_sha256':digest(reference),'phase_entries':4368,
            'five_label_allocation_rows':23100,'literal_three_class_controls':1360,
            'complete_case_rows':45,'coupled_maxima':reference['coupled_maxima'],
            'maximum_three_parent_eight_tail_BASE_holes':176,
            'semantic_damages_rejected':damages,'valid_record_accepted_again':True,
            'independent_reviewer':False,'global_bound_changed':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('record',type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(json.loads(args.record.read_text())),sort_keys=True))
