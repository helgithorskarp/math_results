"""Independent complete point maps from the four blocks through the mark."""
from collections import Counter
from hashlib import sha256
from itertools import combinations,permutations,product
from pathlib import Path
import argparse
import json
from marked import packing,model,instance,canonical,require

def unique_object(items):
    out={}
    for key,value in items:
        require(key not in out,'duplicate JSON key');out[key]=value
    return out

def image(blocks,mapping):
    return tuple(sorted(tuple(sorted(mapping[x] for x in q)) for q in blocks))

def mark_structure(blocks,mark):
    data=packing(blocks,mark);H=data['high']-{mark}
    require(len(H)==4 and all(sum(x in p for p in data['core'])==2 for x in H),'high core is not C4')
    partners={}
    for q in blocks:
        if mark in q:
            high=H&set(q);require(len(high)==1,'mark block does not have one other high point')
            h=next(iter(high));require(h not in partners,'high point occurs twice through mark')
            partners[h]=tuple(sorted(set(q)-{mark,h}))
    require(set(partners)==H and all(data['reps'][x]==5 for pair in partners.values() for x in pair),'invalid mark-star cohorts')
    covered=set().union(*(set(q) for q in blocks if mark in q))
    leave_neighbors=tuple(sorted(set(range(17))-covered))
    require(len(leave_neighbors)==4 and all(data['reps'][x]==5 for x in leave_neighbors),'invalid mark-leave cohort')
    return data,partners,leave_neighbors

def maps(first,second,mark1=14,mark2=14):
    source,pa,la=mark_structure(first,mark1);target,pb,lb=mark_structure(second,mark2)
    H=tuple(sorted(source['high']-{mark1}));K=tuple(sorted(target['high']-{mark2}))
    output=[];candidates=0
    for moved in permutations(K):
        base=dict(zip(H,moved));base[mark1]=mark2
        if {tuple(sorted(base[x] for x in p)) for p in source['core']}!=set(target['core']):continue
        for choices in product(*(tuple(permutations(pb[base[h]])) for h in H)):
            partial=dict(base)
            for h,pair in zip(H,choices):partial.update(zip(pa[h],pair))
            for rest in permutations(lb):
                mapping=dict(partial);mapping.update(zip(la,rest))
                require(set(mapping)==set(range(17)) and len(set(mapping.values()))==17,'not a point bijection')
                point_map=tuple(mapping[x] for x in range(17));candidates+=1
                if all(tuple(sorted(point_map[x] for x in q)) in set(target['blocks']) for q in first):
                    output.append(point_map)
    require(candidates==3072 and len(output)==len(set(output)),'incomplete or repeated mark-star maps')
    return tuple(sorted(output)),candidates

def anchor_group(data):
    cells=data['cells'];lookup={c:x for x,c in enumerate(cells)};out=set()
    for perm in permutations(range(4)):
        for transpose,swap in product((False,True),repeat=2):
            moved=tuple(lookup[(perm[c],perm[r]) if transpose else (perm[r],perm[c])] for r,c in cells)
            moved+=((13,12) if swap else (12,13))+(14,)+((16,15) if transpose else (15,16))
            require(set(moved)==set(range(17)) and image(data['anchors'],moved)==tuple(sorted(data['anchors'])),'invalid anchor map')
            out.add(moved)
    require(len(out)==96 and all(tuple(a[b[x]] for x in range(17)) in out for a in out for b in out),'incomplete anchor group')
    return tuple(sorted(out))

def classify(raw,expected):
    blocks=tuple(tuple(tuple(q) for q in p) for p in raw['packings'])
    require(len(blocks)==72 and len(set(blocks))==72,'missing raw positive census')
    reference=min(blocks);group,tries=maps(reference,reference)
    require(len(group)==8 and tuple(range(17)) in group and all(tuple(a[b[x]] for x in range(17)) in group for a in group for b in group),'full group fails')
    point_map_counts=[];total=tries
    for p in blocks:
        current,visited=maps(p,reference);total+=visited
        require(len(current)==8,'raw positive outside marked class')
        point_map_counts.append(len(current))
    target=tuple(tuple(q) for q in expected['isolated_canonical'])
    target_maps,visited=maps(reference,target);total+=visited;require(len(target_maps)==8,'target representative outside class')
    data=model();anchors=anchor_group(data);bucket={}
    for high in combinations(range(14),4):
        rep=min(tuple(sorted(a[x] for x in high)) for a in anchors)
        bucket.setdefault(rep,[]).append(high)
    require(len(bucket)==31 and sum(map(len,bucket.values()))==1001,'anchor orbit coverage')
    per_high={}
    for p in blocks:
        high=tuple(sorted(packing(p)['high']-{14}));per_high.setdefault(high,[]).append(p)
    reports=[]
    for high,orbit in sorted(bucket.items()):
        actual={tuple(sorted(a[x] for x in high)) for a in anchors}
        require(actual==set(orbit),'orbit carrier mismatch')
        case=instance(data,high);stabilizer=tuple(a for a in anchors if {a[x] for x in high}==set(high))
        require(len(orbit)*len(stabilizer)==96,'orbit-stabilizer mismatch')
        count=len(per_high.get(high,()))
        require(all(len(per_high.get(h,()))==count for h in orbit),'positive fiber mass differs under actual group')
        if count:
            fiber=set(per_high[high]);start=min(fiber)
            require({image(start,a) for a in stabilizer}==fiber,'multiple positive prefix classes')
        reports.append(dict(high=high,orbit_size=len(orbit),stabilizer_order=len(stabilizer),direct=case['direct'],completions=count))
    require(sum(r['direct'] for r in reports)==6 and sum(not r['direct'] for r in reports)==25,'target orbit counters differ')
    positive=[r for r in reports if r['completions']]
    require([(r['high'],r['orbit_size'],r['stabilizer_order'],r['completions']) for r in positive]
            ==[((0,1,3,6),12,8,4),((0,3,12,13),6,16,4)],'positive target fibers differ')
    H=tuple(sorted(packing(reference)['high']-{14}))
    restrictions={tuple(a[x] for x in H) for a in group}
    require(len(restrictions)==4,'unexpected high-cycle action')
    orders=[]
    for a in group:
        power=tuple(range(17))
        for n in range(1,9):
            power=tuple(a[x] for x in power)
            if power==tuple(range(17)):orders.append(n);break
        else:raise ValueError('invalid finite group order')
    _,_,Lp=mark_structure(reference,14);unseen=set(combinations(Lp,2));pair_orbits=[]
    while unseen:
        p=min(unseen);orbit={tuple(sorted(a[x] for x in p)) for a in group}
        require(orbit<=unseen,'overlapping leave-neighbor pair orbits');unseen-=orbit
        pair_orbits.append(len(orbit))
    low_action=len({tuple(a[x] for x in Lp) for a in group})
    require(sorted(pair_orbits)==[2,4] and low_action==4,'unexpected leave-neighbor action')
    require(all(tuple(a[b[x]] for x in range(17))==tuple(b[a[x]] for x in range(17)) for a in group for b in group)
            and Counter(orders)=={1:1,2:3,4:4},'group is not C4 times C2')
    identity=tuple(range(17));g=next(a for a,n in zip(group,orders) if n==4)
    cyclic={identity};power=identity
    for _ in range(4):
        power=tuple(g[x] for x in power);cyclic.add(power)
    h=next(a for a,n in zip(group,orders) if n==2 and a not in cyclic)
    require(len(cyclic)==4 and cyclic|{tuple(h[x] for x in a) for a in cyclic}==set(group),
            'explicit C4 times C2 generators fail')
    require(6*2*2*24//len(group)==len(blocks),'normalization mass crosscheck')
    return dict(marked_classes=1,full_automorphism_order=len(group),automorphisms=group,
                group_type='C4 times C2',high_cycle_action_order=len(restrictions),high_cycle_kernel_order=2,
                order_four_generator=g,independent_order_two_generator=h,
                marked_leave_action_order=low_action,marked_leave_kernel_order=2,
                element_order_counts=dict(Counter(orders)),mark_star_map_candidates=total,
                maps_from_each_raw_positive=point_map_counts,own_reference=reference,
                own_reference_sha256=sha256(canonical(reference)).hexdigest(),
                target_representative_maps=len(target_maps),anchor_group_order=96,
                anchor_orbit_records=reports,leave_neighbor_pair_orbit_sizes=sorted(pair_orbits),
                structural_normalized_count=6*2*2*24//8)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--raw',type=Path,required=True);parser.add_argument('--target',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=json.loads(args.raw.read_text(),object_pairs_hook=unique_object)
    expected=json.loads(args.target.read_text(),object_pairs_hook=unique_object)
    result=classify(raw,expected);args.output.write_bytes(canonical(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('own_reference','automorphisms','anchor_orbit_records','maps_from_each_raw_positive')},indent=2))
