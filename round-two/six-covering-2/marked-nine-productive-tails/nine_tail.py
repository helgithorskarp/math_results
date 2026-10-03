"""Exact producer: full type/phase/inventory reduction and BASE gluing."""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm, prod
from pathlib import Path
import two_parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(record):
    return sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def build():
    ds = [d for d in range(1,316) if 315 % d == 0]
    unused = ds[1:]
    U = [y for y in range(315) if y % 9 != 0 and y % 3 != 1 and y % 7 != 0]
    masks = {d:[sum(1 << y for y in U if y % d == a) for a in range(d)] for d in ds}
    C = {d:max(m.bit_count() for m in ms) for d,ms in masks.items()}
    pairs = [[list(p),C[lcm(*p)]] for p in combinations(unused,2)]
    triples = [[list(p),C[lcm(*p)],sum(C[lcm(*q)] for q in combinations(p,2))]
               for p in combinations(unused,3)]
    q4 = [[list(p),sum(C[lcm(*q)] for q in combinations(p,3))] for p in combinations(unused,4)]
    q5 = [[list(p),sum(C[lcm(*q)] for q in combinations(p,3))] for p in combinations(unused,5)]
    I2 = max(row[1] for row in pairs)
    I3 = max(row[1] for row in triples)
    P3 = max(row[2] for row in triples)
    P4 = max(row[1] for row in q4)
    P5 = max(row[1] for row in q5)
    require((I2,I3,P3,P4) == (30,18,54,36), 'Q intersection constants changed')
    five = [[list(labels),sum(C[d] for d in labels)] for labels in combinations(unused,5)]
    high = [tuple(labels) for labels,total in five if total >=177]
    require(len(high) == 9, 'High five-H subset reduction changed')
    groups = {g for labels in high for n in range(1,5) for g in combinations(labels,n)}
    h3_labels = list(combinations(unused,3))
    groups.update(labels for labels in h3_labels if sum(C[d] for d in labels)>126)
    groups.update(combinations((3,5,9),2))
    phase_union = []
    UB = {}
    for labels in sorted(groups):
        counts = []
        for residues in product(*(range(d) for d in labels)):
            union = 0
            for d,a in zip(labels,residues):union |= masks[d][a]
            counts.append(union.bit_count())
        require(len(counts) == prod(labels), 'Raw phase union block incomplete')
        UB[labels] = max(counts)
        phase_union.append([list(labels),counts,UB[labels]])

    five_rows = []
    for labels in high:
        for k in range(1,5):
            for p2 in combinations(labels,k):
                p6 = sorted(set(labels)-set(p2))
                for n in range(1,len(p6)+1):
                    for opposite in combinations(p6,n):
                        same = sorted(set(p6)-set(opposite))
                        common = sum(C[lcm(a,b)] for a in opposite for b in same)
                        qs = [[q,min(C[q],sum(C[lcm(a,q)] for a in opposite))] for q in unused]
                        cap = UB[p2]+min(UB[opposite],common+max(row[1] for row in qs))
                        five_rows.append([list(labels),list(p2),list(opposite),same,
                                          UB[p2],UB[opposite],common,qs,cap])
    require(len(five_rows) == 1620 and max(row[-1] for row in five_rows) == 175,
            'Complete high five-H orientation bound changed')
    low5 = max(total for labels,total in five if total <177)
    F5 = max(low5,max(row[-1] for row in five_rows))
    require(F5 == 176, 'Whole five-H bound changed')
    h3 = [[list(labels),sum(C[d] for d in labels),
           UB[labels] if sum(C[d] for d in labels)>126 else sum(C[d] for d in labels)]
          for labels in h3_labels]
    require(max(row[-1] for row in h3) == 126, 'Three-H footprint bound changed')

    q4arms = []
    for labels in combinations(unused,4):
        for n in (1,2):
            for arm in combinations(labels,n):
                rest = tuple(d for d in labels if d not in arm)
                if n == 2 and arm>rest:continue
                cross = sum(C[lcm(a,b)] for a in arm for b in rest)
                cap = min(sum(C[a] for a in arm),sum(C[b] for b in rest),cross)
                q4arms.append([list(labels),list(arm),list(rest),cross,cap])
    require(len(q4arms) == 2310 and max(row[-1] for row in q4arms) == 66,
            'Four-Q binary arm upper bound changed')
    mixed = []
    for f in unused:
        for pair in combinations([d for d in unused if d != f],2):
            for opposite in ((pair[0],),(pair[1],),pair):
                same = [d for d in pair if d not in opposite]
                common = sum(C[lcm(a,b)] for a in opposite for b in same)
                qs = [[q,min(C[q],sum(C[lcm(a,q)] for a in opposite))] for q in unused]
                cap = C[f]+I2+min(sum(C[d] for d in opposite),common+max(row[1] for row in qs))
                mixed.append([f,list(pair),list(opposite),same,common,qs,cap])
    require(len(mixed) == 1485 and max(row[-1] for row in mixed) == 168,
            'HQQ/HHQ upper bound changed')
    special = []
    for f in (3,5,9):
        p2 = tuple(d for d in (3,5,9) if d != f)
        for pair in combinations(unused,2):
            for q in unused:
                if q in pair:continue
                cap = UB[p2]+C[lcm(*pair)]+C[lcm(f,q)]
                special.append([f,list(p2),list(pair),q,UB[p2],C[lcm(*pair)],C[lcm(f,q)],cap])
    survivors = [row for row in special if row[-1]>=177]
    require(len(special) == 1485 and survivors == [[5,[3,9],[3,9],5,120,30,30,180]],
            'Unique potentially177-reaching original inventory changed')
    cases = []
    def case(a,b,h,q,cap):cases.append([a,b,h,q,cap])
    for typ,cap in zip(('HHHHQ','HHHQQ','HHQQQ','HQQQQ','QQQQQ'),
                       (F5,175,150+I3,120+P4,90+P5)):case(2,6,'H',typ,cap)
    table = {'HH':(F5,175,150+I3,120+P4),
             'HQ':(175,150,120+I3,90+P4),
             'QQ':(I2+126,I2+120,I2+90+I3,I2+P4)}
    for h,caps in table.items():
        for q,cap in zip(('HHHQ','HHQQ','HQQQ','QQQQ'),caps):case(3,5,h,q,cap)
    table = {'HHH':(F5,175,150+I3),'HHQ':(175,150,120+I3),
             'HQQ':(168,120+I2,90+I2+I3),'QQQ':(P3+90,P3+90,P3+I3)}
    for h,caps in table.items():
        for q,cap in zip(('HHQ','HQQ','QQQ'),caps):case(4,4,h,q,cap)
    for h,cap in zip(('HHHH','HHHQ','HHQQ','HQQQ','QQQQ'),
                     (F5,175,180,120+P3,66+90)):case(5,3,h,'HQ',cap)
    require(len(cases) == 34 and [row for row in cases if row[-1]>=177] == [[5,3,'HHQQ','HQ',180]],
            'Complete two-parent type census changed')

    controls = []
    for r,placed,lengths in ((2,5,range(1,5)),(6,1,range(2,6))):
        for length in lengths:
            for h in range(length,-1,-1):
                types = 'H'*h+'Q'*(length-h)
                domains = [(0,5,10) if t == 'H' else (0,1,2,4,8) for t in types]
                for states in product(*domains):
                    union = placed
                    halves = 0
                    for t,state in zip(types,states):
                        union |= state
                        if t == 'H':halves |= state
                    covered = union == 15
                    H = [s for t,s in zip(types,states) if t == 'H']
                    Q = [s for t,s in zip(types,states) if t == 'Q']
                    if covered:
                        if r == 2:
                            require(any(H) or sum(bool(s) for s in Q)>=2, 'Half repair footprint condition missing')
                            if h == 0:require(2 in Q and 8 in Q, 'Quarter arms missing')
                        else:
                            require(any(H) or sum(bool(s) for s in Q)>=3, 'Quarter repair footprint condition missing')
                            if not Q:require(halves == 15, 'All-H deletion condition missing')
                            if len(Q) == 1:
                                require(10 in H and (5 in H or Q[0] != 0), 'O intersect(S orQ) missing')
                    controls.append([r,types,list(states),covered,halves == 15])

    def reduced_phase_block(r,cofactors,moduli,placed):
        oddrows = [a for a in range(cofactors) if (a % 9 != 0 and a % 3 != 1) or cofactors == 5]
        if cofactors == 5:oddrows = list(range(5))
        binaries = list(range(r,32,8))
        phase_lists = [list(range(r,m,8)) for m in moduli]
        class_masks = []
        for m,phases in zip(moduli,phase_lists):
            two = 16 if m % 32 else 32
            d = m//two
            class_masks.append([sum(1 << (4*i+j) for i,a in enumerate(oddrows) for j,b in enumerate(binaries)
                                    if a % d == phase % d and b % two == phase % two)
                                for phase in phases])
        placed_mask = sum(1 << (4*i+j) for i,a in enumerate(oddrows) for j,b in enumerate(binaries)
                          if b % placed[0] == placed[1])
        anchor = sum(1 << (4*i) for i in range(len(oddrows)))
        values = []
        good = []
        for inds in product(*(range(len(phases)) for phases in phase_lists)):
            union = placed_mask
            for masks,index in zip(class_masks,inds):union |= masks[index]
            count = (union & (union>>1) & (union>>2) & (union>>3) & anchor).bit_count()*30
            values.append(count)
            if count >= (147 if r == 2 else 27):
                good.append([phase_lists[i][j] for i,j in enumerate(inds)])
        return {'parent':r,'original_moduli':list(moduli),'phase_lists':phase_lists,
                'all_raw_phase_repair_counts':values,'qualifying_phase_tuples':good}
    p2block = reduced_phase_block(2,9,(48,144,96,288),(16,2))
    p6block = reduced_phase_block(6,5,(80,160),(32,6))
    require(len(p2block['all_raw_phase_repair_counts']) == 46656 and
            len(p2block['qualifying_phase_tuples']) == 4,'Full original parent2 phase block changed')
    require(len(p6block['all_raw_phase_repair_counts']) == 200 and
            len(p6block['qualifying_phase_tuples']) == 5,'Full original parent6 phase block changed')

    prefix = ((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
    R = [x for x in range(2520) if all(x % m != a for m,a in prefix)]
    index = {x:i for i,x in enumerate(R)}
    originals = [m for m in range(8,2521) if 2520 % m == 0 and m not in {m for m,a in prefix}]
    fullmask = (1 << len(R))-1
    gluing = []
    for c in range(5):
        shadow = sum(1 << i for i,x in enumerate(R) if x % 8 == 2 or (x % 8 == 6 and x % 5 == c))
        outside = fullmask ^ shadow
        phase_blocks = []
        for m in originals:
            values = []
            for a in range(m):
                ap = sum(1 << index[x] for x in range(a,2520,m) if x in index)
                values.append([(ap & shadow).bit_count(),(ap & outside).bit_count()])
            cap = max(needed for protected,needed in values if protected<=3)
            phase_blocks.append([m,values,cap])
        gluing.append({'c':c,'protected_shape':[x for i,x in enumerate(R) if shadow & (1 << i)],
                       'shape_size':shadow.bit_count(),'outside_holes':outside.bit_count(),
                       'all_original_phase_rows':phase_blocks,
                       'restricted_sum_max_outside':sum(row[-1] for row in phase_blocks)})
    require(all(row['shape_size'] == 180 and row['outside_holes'] == 1216 and
                row['restricted_sum_max_outside'] == 1156 for row in gluing), 'BASE gluing deficit changed')
    return {'agent':'six-covering-2','role':'researcher','status':'AUTHOR-CHECKED conditional nine-tail proof; independent review pending',
            'full_marked_prefix':[[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]],
            'essential_originals_explicit':[16,32],'minimum_modulus_exactly':8,
            'original_moduli_divide':10080,'actual_LCM_may_divide10080':True,
            'three_parent_reduction':two_parent.build(),
            'all_marked_odd_phase_population_rows':[[d,[m.bit_count() for m in masks[d]]] for d in ds],
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


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    result=build();args.out.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'whole_record_sha256':digest(result),'productivity_bound':9,
                      'H_raw_union_entries':sum(len(row[1]) for row in result['all_raw_H_union_phase_blocks']),
                      'binary_controls':len(result['complete_local_binary_controls']),
                      'Q_five_triple_sum':max(row[1] for row in result['Q_five_triple_sums']),
                      'gluing_phase_entries':sum(len(row[1]) for shape in result['all_five_BASE_gluing_shapes'] for row in shape['all_original_phase_rows'])}))
