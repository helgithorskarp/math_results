"""Whole independent literal-AP/set audit; imports no producer arithmetic.

Union phases use actual2520 residue sets; selected tail phases use complete
physical10080 four-lift incidences. BASE rows use residue histograms, rather
than the producer's per-phase AP bitsets. Alternative partition orders are
canonicalized only after every individual row has been reconstructed.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path
import parent_audit


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(record):
    return sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def rebuild():
    R = set(range(2520))
    fixed = {8:0,9:0,10:1,14:0,12:10,28:4}
    for modulus,phase in fixed.items():R.difference_update(range(phase,2520,modulus))
    U = {x for x in R if x % 8 == 2}
    ds = sorted({d for d in range(1,316) if 315 % d == 0})
    unused = ds[1:]
    sets = {d:[U.intersection(range(a,2520,d)) for a in range(d)] for d in ds}
    C = {d:max(map(len,phases)) for d,phases in sets.items()}
    pairs = [[list(p),C[lcm(*p)]] for p in combinations(unused,2)]
    triples = [[list(p),C[lcm(*p)],sum(C[lcm(*q)] for q in combinations(p,2))]
               for p in combinations(unused,3)]
    q4 = [[list(p),sum(C[lcm(*q)] for q in combinations(p,3))] for p in combinations(unused,4)]
    q5 = [[list(p),sum(C[lcm(*q)] for q in combinations(p,3))] for p in combinations(unused,5)]
    five = [[list(p),sum(C[d] for d in p)] for p in combinations(unused,5)]
    high = [tuple(p) for p,total in five if total>176]
    groups = set()
    for labels in high:
        for selection in range(1,31):
            groups.add(tuple(labels[i] for i in range(5) if selection & (1 << i)))
    h3labels = list(combinations(unused,3))
    groups.update(p for p in h3labels if sum(C[d] for d in p)>126)
    groups.update(combinations((3,5,9),2))
    phase_union = []
    UB = {}
    for labels in sorted(groups):
        values = [len(set.union(*chosen)) for chosen in product(*(sets[d] for d in labels))]
        UB[labels] = max(values)
        phase_union.append([list(labels),values,UB[labels]])
    five_rows = []
    for labels in high:
        for chosen in range(1,31):
            p2 = tuple(labels[i] for i in range(5) if chosen & (1 << i))
            p6 = tuple(d for d in labels if d not in p2)
            for arm in range(1,1 << len(p6)):
                opposite = tuple(p6[i] for i in range(len(p6)) if arm & (1 << i))
                same = tuple(d for d in p6 if d not in opposite)
                common = sum(C[lcm(a,b)] for a in opposite for b in same)
                qs = [[q,min(C[q],sum(C[lcm(a,q)] for a in opposite))] for q in unused]
                cap = UB[p2]+min(UB[opposite],common+max(row[1] for row in qs))
                five_rows.append([list(labels),list(p2),list(opposite),list(same),
                                  UB[p2],UB[opposite],common,qs,cap])
    five_rows.sort(key=lambda v:(v[0],len(v[1]),v[1],len(v[2]),v[2]))
    F5 = max(max(total for p,total in five if total<=176),max(row[-1] for row in five_rows))
    h3 = [[list(p),sum(C[d] for d in p),UB[p] if sum(C[d] for d in p)>126 else sum(C[d] for d in p)]
          for p in h3labels]
    q4arms = []
    for labels in combinations(unused,4):
        for arm_indices in range(1,15):
            left = tuple(labels[i] for i in range(4) if arm_indices & (1 << i))
            right = tuple(d for d in labels if d not in left)
            if len(left)>len(right) or (len(left)==len(right) and left>right):continue
            cross = sum(C[lcm(a,b)] for a in left for b in right)
            q4arms.append([list(labels),list(left),list(right),cross,
                           min(sum(C[a] for a in left),sum(C[b] for b in right),cross)])
    q4arms.sort(key=lambda v:(v[0],len(v[1]),v[1]))
    I2 = max(row[1] for row in pairs)
    I3 = max(row[1] for row in triples)
    P3 = max(row[2] for row in triples)
    P4 = max(row[1] for row in q4)
    P5 = max(row[1] for row in q5)
    A4 = max(row[-1] for row in q4arms)
    mixed = []
    for triple in h3labels:
        for f in triple:
            pair = tuple(d for d in triple if d != f)
            for opposite in ((pair[0],),(pair[1],),pair):
                same = [d for d in pair if d not in opposite]
                common = sum(C[lcm(a,b)] for a in opposite for b in same)
                qs = [[q,min(C[q],sum(C[lcm(a,q)] for a in opposite))] for q in unused]
                cap = C[f]+I2+min(sum(C[d] for d in opposite),common+max(row[1] for row in qs))
                mixed.append([f,list(pair),list(opposite),same,common,qs,cap])
    mixed.sort(key=lambda v:(v[0],v[1],len(v[2]),v[2]))
    special = []
    for qlabels in h3labels:
        for q in qlabels:
            pair = tuple(d for d in qlabels if d != q)
            for f in (3,5,9):
                p2 = tuple(d for d in (3,5,9) if d != f)
                cap = UB[p2]+C[lcm(*pair)]+C[lcm(f,q)]
                special.append([f,list(p2),list(pair),q,UB[p2],C[lcm(*pair)],C[lcm(f,q)],cap])
    special.sort(key=lambda v:(v[0],v[2],v[3]))
    survivors = [row for row in special if row[-1]>=177]
    S = {k:max(sum(C[d] for d in p) for p in combinations(unused,k)) for k in range(5)}
    threshold2 = {0:0,1:0,2:I2,3:P3,4:A4}
    threshold3 = {0:0,1:0,2:0,3:I3,4:P4,5:P5}
    cases = []
    for a in range(2,6):
        b = 8-a
        for h2 in range(a-1,-1,-1):
            l2 = a-1-h2
            if a == 2 and h2 != 1:continue
            for h6 in range(b-2,-1,-1):
                l6 = b-1-h6
                if b == 3 and (h6,l6) != (1,1):continue
                typ2 = 'H'*h2+'Q'*l2
                typ6 = 'H'*h6+'Q'*l6
                nh = h2+h6
                if nh == 5:cap = F5
                elif (typ2,typ6) == ('HHQQ','HQ'):cap = max(row[-1] for row in special)
                elif (typ2,typ6) == ('HQQ','HHQ'):cap = max(row[-1] for row in mixed)
                elif (typ2,typ6) == ('QQ','HHHQ'):cap = I2+max(row[-1] for row in h3)
                elif (typ2,typ6) == ('QQQ','HHQ'):cap = P3+max(C[d] for d in unused)
                else:cap = S[nh]+threshold2[l2]+threshold3[l6]
                cases.append([a,b,typ2,typ6,cap])
    require(len(cases) == 34 and [v for v in cases if v[-1]>=177] == [[5,3,'HHQQ','HQ',180]],
            'Independent complete type census failed')
    controls = []
    for r,lengths,placed in ((2,range(1,5),(16,2)),(6,range(2,6),(32,6))):
        x = min(y for y in R if y % 8 == r)
        lifts = [x+2520*k for k in range(4)]
        marked = {y for y in lifts if y % placed[0] == placed[1]}
        require(sum(1 << k for k,y in enumerate(lifts) if y in marked) == (5 if r == 2 else 1),
                'Placed literal half/quarter order differs')
        for length in lengths:
            for h in range(length,-1,-1):
                types = 'H'*h+'Q'*(length-h)
                domains = [(0,5,10) if t == 'H' else (0,1,2,4,8) for t in types]
                for states in product(*domains):
                    covered_points = set(marked)
                    halves = set()
                    observed = []
                    for d,kind,state in zip((3,5,7,9,15),types,states):
                        two = 16 if kind == 'H' else 32
                        first = next((i for i in range(4) if state & (1 << i)),0)
                        binary = lifts[first] % two
                        odd = (x+int(state == 0)) % d
                        phase = next(binary+two*j for j in range(d) if (binary+two*j) % d == odd)
                        ap = set(range(phase,10080,two*d))
                        touched = ap.intersection(lifts)
                        observed.append(sum(1 << k for k,y in enumerate(lifts) if y in touched))
                        covered_points.update(touched)
                        if kind == 'H':halves.update(touched)
                    require(observed == list(states), 'Full physical binary control differs')
                    controls.append([r,types,list(states),set(lifts).issubset(covered_points),
                                     set(lifts).issubset(halves)])

    def physical_phase_block(r,moduli,placed,minimum):
        shadow = sorted(x for x in R if x % 8 == r)
        phase_lists = [list(range(r,m,8)) for m in moduli]
        points = [x+2520*k for x in shadow for k in range(4)]
        anchor = sum(1 << (4*i) for i in range(len(shadow)))
        def bitmask(modulus,phase):
            ap = set(range(phase,10080,modulus))
            return sum(1 << i for i,y in enumerate(points) if y in ap)
        marked = bitmask(*placed)
        class_masks = [[bitmask(m,phase) for phase in phases] for m,phases in zip(moduli,phase_lists)]
        counts = []
        good = []
        for indices in product(*(range(len(phases)) for phases in phase_lists)):
            union = marked
            for masks,index in zip(class_masks,indices):union |= masks[index]
            count = (union & (union>>1) & (union>>2) & (union>>3) & anchor).bit_count()
            counts.append(count)
            if count>=minimum:good.append([phase_lists[i][j] for i,j in enumerate(indices)])
        return {'parent':r,'original_moduli':list(moduli),'phase_lists':phase_lists,
                'all_raw_phase_repair_counts':counts,'qualifying_phase_tuples':good}
    p2block = physical_phase_block(2,(48,144,96,288),(16,2),147)
    p6block = physical_phase_block(6,(80,160),(32,6),27)
    originals = sorted(m for m in range(8,2521) if 2520 % m == 0 and m not in fixed)
    gluing = []
    for c in range(5):
        shadow = {x for x in R if x % 8 == 2 or (x % 8 == 6 and x % 5 == c)}
        outside = R-shadow
        phase_blocks = []
        for m in originals:
            protected_counts = [0]*m
            needed_counts = [0]*m
            for x in shadow:protected_counts[x % m] += 1
            for x in outside:needed_counts[x % m] += 1
            values = [[protected_counts[a],needed_counts[a]] for a in range(m)]
            cap = max(needed_counts[a] for a in range(m) if protected_counts[a]<=3)
            phase_blocks.append([m,values,cap])
        gluing.append({'c':c,'protected_shape':sorted(shadow),'shape_size':len(shadow),
                       'outside_holes':len(outside),'all_original_phase_rows':phase_blocks,
                       'restricted_sum_max_outside':sum(row[-1] for row in phase_blocks)})
    return {'agent':'six-covering-2','role':'researcher','status':'AUTHOR-CHECKED conditional nine-tail proof; independent review pending',
            'full_marked_prefix':[[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]],
            'essential_originals_explicit':[16,32],'minimum_modulus_exactly':8,
            'original_moduli_divide':10080,'actual_LCM_may_divide10080':True,
            'three_parent_reduction':parent_audit.rebuild(),
            'all_marked_odd_phase_population_rows':[[d,list(map(len,sets[d]))] for d in ds],
            'Q_pairs':pairs,'Q_triples':triples,'Q_four_triple_sums':q4,'Q_five_triple_sums':q5,
            'all_five_H_cofactor_capacity_sums':five,'all_raw_H_union_phase_blocks':phase_union,
            'all_high_five_H_orientation_rows':five_rows,'all_three_H_union_bounds':h3,
            'all_four_Q_arm_bounds':q4arms,'all_HQQ_HHQ_bounds':mixed,
            'all_special_HHQQ_HQ_original_inventory_bounds':special,
            'special_inventory_rows_reaching177':survivors,'all_eight_two_parent_type_cases':cases,
            'complete_local_binary_controls':controls,
            'parent2_full_original_phase_block':p2block,'parent6_full_original_phase_block':p6block,
            'all_five_BASE_gluing_shapes':gluing,
            'BASE_holes_lower_bound_imported_from_public9934':177,
            'at_least_eight_productive_TAILs_imported_from_public9978':True,
            'new_productive_TAIL_lower_bound':9,'capacity_sharpness_claimed':False,
            'ordinary_proof_formalized':False,'independent_reviewer':False,'global_bound_changed':False}


def audit(candidate):
    reference = rebuild()
    require(candidate == reference, 'Entire nine-tail record differs from physical reconstruction')
    damages = []
    def probe(name,change,restore):
        change()
        require(candidate != reference, 'Semantic damage accepted: '+name)
        damages.append(name)
        restore()
        require(candidate == reference, 'Record not fully restored: '+name)
    for key,new in (('essential_originals_explicit',[16]),('minimum_modulus_exactly',9),
                    ('original_moduli_divide',15120),('new_productive_TAIL_lower_bound',10),
                    ('global_bound_changed',True)):
        old = candidate[key]
        probe(key,lambda k=key,v=new:candidate.__setitem__(k,v),lambda k=key,v=old:candidate.__setitem__(k,v))
    row = candidate['full_marked_prefix'][3];old = row[1]
    probe('wrong14phase',lambda:row.__setitem__(1,1),lambda:row.__setitem__(1,old))
    row = candidate['complete_local_binary_controls'][0];old = row[3]
    probe('inactive-extra-half-covers',lambda:row.__setitem__(3,True),lambda:row.__setitem__(3,old))
    for key in ('all_raw_H_union_phase_blocks','all_high_five_H_orientation_rows',
                'all_four_Q_arm_bounds','all_HQQ_HHQ_bounds',
                'all_special_HHQQ_HQ_original_inventory_bounds','all_eight_two_parent_type_cases'):
        block = candidate[key]
        old = block[-1]
        probe('omitted-last-'+key,lambda block=block:block.pop(),lambda block=block,old=old:block.append(old))
    row = candidate['parent2_full_original_phase_block']['all_raw_phase_repair_counts'];old = row[-1]
    probe('last-original-phase-count',lambda:row.__setitem__(-1,old+30),lambda:row.__setitem__(-1,old))
    row = candidate['all_five_BASE_gluing_shapes'][-1]['all_original_phase_rows'][-1][1][-1];old = row[-1]
    probe('last-BASE-raw-phase',lambda:row.__setitem__(-1,old+1),lambda:row.__setitem__(-1,old))
    row = candidate['all_five_BASE_gluing_shapes'][0];old = row['restricted_sum_max_outside']
    probe('false-BASE-margin',lambda:row.__setitem__('restricted_sum_max_outside',1216),
          lambda:row.__setitem__('restricted_sum_max_outside',old))
    row = candidate['three_parent_reduction']['all_global_five_extra_H_coupling_rows'][-1];old = row[-1]
    probe('last-prerequisite-coupling',lambda:row.__setitem__(-1,old+1),lambda:row.__setitem__(-1,old))
    return {'agent':'six-covering-2','role':'researcher','every_full_mathematical_field_compared':True,
            'whole_record_sha256':digest(reference),'new_productive_TAIL_lower_bound':9,
            'H_raw_union_entries':sum(len(row[1]) for row in reference['all_raw_H_union_phase_blocks']),
            'local_binary_controls':len(reference['complete_local_binary_controls']),
            'original_phase_counts_compared':46856,'BASE_raw_phase_rows_compared':46255,
            'complete_two_parent_type_cases':34,'five_H_high_orientations':1620,
            'semantic_damages_rejected':damages,'valid_record_accepted_again':True,
            'independent_reviewer':False,'global_bound_changed':False}


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('record',type=Path);args=parser.parse_args()
    print(json.dumps(audit(json.loads(args.record.read_text())),sort_keys=True))
