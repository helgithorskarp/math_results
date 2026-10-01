"""Exact two-anchor reductions and complete pair/quota solution fibers."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import resource
import time

from common import Guard, Incomplete, WORK, bits, digest, encoded, require


def anchors_model(name):
    if name == "isolated":
        n = 4
        cells = tuple((i,j) for i in range(n) for j in range(n) if i != j)
        anchors = ((12,13,15,16),)
        anchors += tuple(tuple(sorted((15,)+tuple(x for x,c in enumerate(cells) if c[0] == i)))
                         for i in range(n))
        anchors += tuple(tuple(sorted((16,)+tuple(x for x,c in enumerate(cells) if c[1] == i)))
                         for i in range(n))
    else:
        n = 5
        if name == "cycle10":
            missing = {(i,j) for i in range(n) for j in (i,(i+1)%5)}
        else:
            require(name == "cycle6_cycle4", "unknown anchor model")
            missing = {(i,j) for i in (0,1) for j in (0,1)}
            missing |= {(i,j) for i in (2,3,4) for j in (i,2+(i-1)%3)}
        cells = tuple((i,j) for i in range(n) for j in range(n) if (i,j) not in missing)
        anchors = tuple(tuple(sorted((15,)+tuple(x for x,c in enumerate(cells) if c[0] == i)))
                        for i in range(n))
        anchors += tuple(tuple(sorted((16,)+tuple(x for x,c in enumerate(cells) if c[1] == i)))
                         for i in range(n))
    used = Counter(e for q in anchors for e in combinations(q,2))
    require(set(used.values()) == {1}, "anchor pair repetition")
    eligible = tuple(e for e in combinations(range(15),2) if e not in used)
    pool = tuple(q for q in combinations(range(15),4) if set(combinations(q,2)) <= set(eligible))
    index = {c:x for x,c in enumerate(cells)}
    maps = set()
    for rows in permutations(range(n)):
        for cols in permutations(range(n)):
            for transpose in (False,True):
                images = tuple((rows[j],cols[i]) if transpose else (rows[i],cols[j]) for i,j in cells)
                if set(images) != set(cells):
                    continue
                cell_map = tuple(index[c] for c in images)
                for swap in ((False,True) if name == "isolated" else (False,)):
                    p = cell_map + (((13,12) if swap else (12,13))+(14,) if name == "isolated" else ())
                    p += (16,15) if transpose else (15,16)
                    require(len(p) == 17 and len(set(p)) == 17 and
                            {tuple(sorted(p[x] for x in q)) for q in anchors} == set(anchors),
                            "point map changes anchors")
                    maps.add(p)
    maps = tuple(sorted(maps))
    require(len(maps) == {"isolated":96,"cycle10":20,"cycle6_cycle4":48}[name], "anchor group order")
    require(all(tuple(a[b[x]] for x in range(17)) in maps for a in maps for b in maps), "group closure")
    return {"name":name,"cells":cells,"anchors":anchors,"eligible":eligible,"pool":pool,"maps":maps}


def quota_inputs(model):
    eligible, pool, maps = model["eligible"], model["pool"], model["maps"]
    used = set(e for q in model["anchors"] for e in combinations(q,2))
    raw = []
    if model["name"] == "isolated":
        raw = list(combinations(range(14),4))
    else:
        # Every labeled high triple and its uniquely differently deficient point.
        for high in combinations(range(15),3):
            for special in high:
                for pattern in ("311","221"):
                    raw.append((pattern,high,special))
    unseen = set(raw)
    records = []
    for value in sorted(raw):
        if value not in unseen:
            continue
        if model["name"] == "isolated":
            orbit = {tuple(sorted(p[x] for x in value)) for p in maps}
            high = set(value)
            R = sum(e in used for e in combinations(value,2))
            quota = tuple((2 if x in high else 3) if x < 12 else
                          (3 if x in high else 4) if x < 14 else 4 for x in range(15))
            mandatory = tuple(e for e in eligible if not set(e) & (high | {14}) or
                              (14 in e and set(e) <= high | {14}))
            columns = tuple(q for q in pool if len(tuple(combinations(tuple(x for x in q if x in high),2))) <= 2-R)
            direct = R > 2
        else:
            pattern, hs, special = value
            orbit = {(pattern,tuple(sorted(p[x] for x in hs)),p[special]) for p in maps}
            high = set(hs)
            deficits = {x:(3 if x == special else 1) if pattern == "311" else
                        (1 if x == special else 2) for x in high}
            R = sum(e in used for e in combinations(hs,2))
            quota = tuple(3-deficits.get(x,0) for x in range(15))
            mandatory = tuple(e for e in eligible if not set(e) & high)
            columns = tuple(q for q in pool if len(set(q) & high) <= 1)
            direct = R > 0
        require(orbit <= unseen, "orbit escape or overlap")
        unseen -= orbit
        record = {"key":value,"orbit":sorted(orbit),"quota":quota,"mandatory":mandatory,
                  "columns":columns,"direct":direct,"anchor_high_pairs":R}
        require(sum(quota) == (44 if model["name"] == "isolated" else 40), "quota sum")
        records.append(record)
    require(not unseen and sum(len(r["orbit"]) for r in records) == len(raw), "carrier not exhaustive")
    return records


def all_covers(eligible, columns, quota, mandatory, nodes=200000, seconds=10):
    require(len(quota) == 15 and all(type(n) is int and n >= 0 for n in quota), "invalid point quota")
    require(len(set(columns)) == len(columns), "duplicate column")
    index = {e:i for i,e in enumerate(eligible)}
    required = set(mandatory)
    require(required <= set(eligible), "invalid mandatory pair")
    pair_rows, point_rows = [0]*len(eligible), [0]*15
    masks = []
    for i,q in enumerate(columns):
        require(tuple(sorted(set(q))) == q and len(q) == 4 and all(0 <= x < 15 for x in q), "bad quadruple")
        edges = tuple(combinations(q,2))
        require(set(edges) <= set(eligible), "column repeats an anchor pair")
        require(bool(set(edges) & required), "column has no mandatory pair")
        masks.append(sum(1 << index[e] for e in edges))
        for x in q:
            point_rows[x] |= 1 << i
        for e in edges:
            pair_rows[index[e]] |= 1 << i
    conflicts = []
    for mask in masks:
        value = 0
        for e in bits(mask):
            value |= pair_rows[e]
        conflicts.append(value)
    guard, output = Guard(nodes,seconds), []
    available = (1 << len(columns))-1
    for x,n in enumerate(quota):
        if not n:
            available &= ~point_rows[x]

    def visit(left, need, active, chosen):
        guard.tick()
        if not need:
            if not any(left):
                output.append(tuple(sorted(chosen)))
            return
        if any((active & point_rows[x]).bit_count() < n for x,n in enumerate(left)):
            return
        _,pivot = min(((active & pair_rows[e]).bit_count(),e) for e in bits(need))
        for i in bits(active & pair_rows[pivot]):
            after,zero = list(left),0
            for x in columns[i]:
                after[x] -= 1
                require(after[x] >= 0, "quota exceeded")
                if after[x] == 0:
                    zero |= point_rows[x]
            visit(tuple(after),need & ~masks[i],active & ~conflicts[i] & ~zero,chosen+(i,))

    visit(tuple(quota),sum(1 << index[e] for e in mandatory),available,())
    require(len(set(output)) == len(output), "cover duplicated")
    return sorted(output),guard.nodes


def check_packing(blocks,replication):
    require(len(blocks) == 20 and len(set(blocks)) == 20, "wrong packing size")
    require(all(tuple(sorted(set(q))) == q and len(q) == 4 and all(0 <= x < 17 for x in q) for q in blocks), "bad block")
    reps = Counter(x for q in blocks for x in q)
    pairs = Counter(e for q in blocks for e in combinations(q,2))
    require(set(pairs.values()) == {1} and all(reps[x] == replication[x] for x in range(17)), "packing incidence failure")
    return set(combinations(range(17),2))-set(pairs)


def leave_maps(first,second):
    """All leave maps fixing the unique isolated high point14."""
    leaves = [set(combinations(range(17),2))-set(e for q in f for e in combinations(q,2)) for f in (first,second)]
    reps = [Counter(x for q in f for x in q) for f in (first,second)]
    highs = [tuple(x for x in range(17) if rep[x] == 4 and x != 14) for rep in reps]
    cohorts = [{h:tuple(x for x in range(17) if rep[x] == 5 and tuple(sorted((h,x))) in leave)
                for h in hs+(14,)} for hs,rep,leave in zip(highs,reps,leaves)]
    output=[]
    for images in permutations(highs[1]):
        base = dict(zip(highs[0],images));base[14]=14
        if any(((x,y) in leaves[0]) != (tuple(sorted((base[x],base[y]))) in leaves[1])
               for x,y in combinations(sorted(base),2)):
            continue
        order=tuple(sorted(base))
        for arrangements in product(*(permutations(cohorts[1][base[h]]) for h in order)):
            mapping=dict(base)
            for h,targets in zip(order,arrangements):
                mapping.update(zip(cohorts[0][h],targets))
            require(set(mapping) == set(range(17)) and len(set(mapping.values())) == 17,"leave map not bijective")
            output.append(tuple(mapping[x] for x in range(17)))
    require(len(output) == 3072 and len(set(output)) == len(output),"leave map count")
    return sorted(output)


def historical_fixture():
    # Stanton--Street1987, Case VII(f), p213. A,...,P=0,...,15; infinity16.
    words = "ABCD EFGH IJKL MNOP AEIM BFJN CGKO DHLP AHJO BGIP CFLM DEKN AGLN BHKM CEJP DFIO AFKP BELO CHIN DGJM".split()
    blocks={tuple(sorted(ord(c)-65 for c in w)) for w in words}
    for old,new in (("ABCD","BCD"),("EFGH","FGH"),("AFKP","AKP"),("BELO","ELO")):
        blocks.remove(tuple(sorted(ord(c)-65 for c in old)))
        blocks.add(tuple(sorted(tuple(ord(c)-65 for c in new)+(16,))))
    return tuple(sorted(blocks))


def run():
    models,summary={},{}
    iso_packings=[]
    for name in ("cycle10","cycle6_cycle4","isolated"):
        model=anchors_model(name)
        records=quota_inputs(model)
        total_nodes,positive=0,0
        for r in records:
            if r['direct']:
                covers,nodes=[],0
            else:
                covers,nodes=all_covers(model['eligible'],r['columns'],r['quota'],r['mandatory'])
            r['solutions']=covers
            r['nodes']=nodes
            total_nodes+=nodes
            if covers:
                require(name=='isolated',"forbidden three-high packing found")
                positive+=1
                high=set(r['key'])|{14}
                target=tuple(4 if x in high else 5 for x in range(17))
                packings=[]
                for cover in covers:
                    blocks=tuple(sorted(model['anchors']+tuple(r['columns'][i] for i in cover)))
                    leave=check_packing(blocks,target)
                    require(not any(14 in e and set(e)<=high for e in leave),"marked point not isolated")
                    packings.append(blocks)
                stabilizer=tuple(p for p in model['maps'] if {p[x] for x in r['key']}==set(r['key']))
                unseen=set(packings)
                prefix_classes=[]
                while unseen:
                    representative=min(unseen)
                    orbit={tuple(sorted(tuple(sorted(p[x] for x in b)) for b in representative)) for p in stabilizer}
                    require(orbit<=unseen,"packing orbit missing or overlapping")
                    unseen-=orbit
                    prefix_classes.append({'blocks':representative,'orbit_size':len(orbit)})
                r['prefix_classes']=prefix_classes
                iso_packings.extend(c['blocks'] for c in prefix_classes)
        model['cases']=records
        models[name]=model
        summary[name]={'raw_inputs':sum(len(r['orbit']) for r in records),'orbits':len(records),
                       'direct_orbits':sum(r['direct'] for r in records),'quota_cases':sum(not r['direct'] for r in records),
                       'raw_quota_inputs':sum(len(r['orbit']) for r in records if not r['direct']),
                       'group_order':len(model['maps']),'candidate_quadruples':len(model['pool']),
                       'positive_orbits':positive,'solutions':sum(len(r['solutions']) for r in records),
                       'primary_nodes':total_nodes}
    require(len(iso_packings)==2,"unexpected positive-prefix class count")
    canonical=iso_packings[0]
    isomorphisms=[]
    for blocks in iso_packings:
        maps=leave_maps(blocks,canonical)
        actual=[p for p in maps if {tuple(sorted(p[x] for x in b)) for b in blocks}==set(canonical)]
        require(len(actual)==8,"marked packing map count")
        isomorphisms.append(actual)
    aut=isomorphisms[0]
    require(all(tuple(a[b[x]] for x in range(17)) in aut for a in aut for b in aut),"marked aut group closure")
    leave=check_packing(canonical,tuple(4 if x in {0,1,3,6,14} else 5 for x in range(17)))
    old=historical_fixture()
    oldhighs={0,1,4,5,16}
    oldleave=check_packing(old,tuple(4 if x in oldhighs else 5 for x in range(17)))
    require(len([e for e in oldleave if set(e)<=oldhighs])==4 and
            not any(16 in e and set(e)<=oldhighs for e in oldleave),"historical isolated fixture failure")
    move=list(range(17));move[14],move[16]=16,14
    old_moved=tuple(sorted(tuple(sorted(move[x] for x in b)) for b in old))
    old_maps=[p for p in leave_maps(old_moved,canonical)
              if {tuple(sorted(p[x] for x in b)) for b in old_moved}==set(canonical)]
    require(len(old_maps)==8,"historical fixture not in classified marked class")
    result={'agent':'six-code-3','role':'researcher','status':'COMPLETE',
            'models':models,'isolated_canonical':canonical,'isolated_isomorphisms':isomorphisms,
            'marked_automorphisms':aut,'historical_fixture':old,'historical_swap14_16_maps':old_maps}
    instances=[{k:model[k] for k in ('name','cells','anchors','eligible','pool','maps')} |
               {'cases':[{k:r[k] for k in ('key','orbit','quota','mandatory','columns','direct','anchor_high_pairs')}
                         for r in model['cases']]} for model in models.values()]
    solution_fibers=[{'name':name,'cases':[(r['key'],r['solutions']) for r in model['cases']]}
                     for name,model in models.items()]
    expected={'models':summary,'input_fiber_sha256':digest(models),'actual_instances_sha256':digest(instances),
              'actual_solution_fibers_sha256':digest(solution_fibers),'isolated_canonical':canonical,
              'marked_automorphism_order':len(aut),'canonical_sha256':digest(canonical),
              'historical_fixture_sha256':digest(old),'marked_isomorphism_classes':1,
              'near71_pair_deficit_counts_1_2_5':[[9,8,0],[12,4,1],[15,0,2]],
              'near71_saturated_deficit_graph_edges':30,'near71_uncovered_triples_sat':60,
              'near71_uncovered_triples_through_unique_unsaturated':46}
    return result,expected


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-expected',action='store_true')
    args=parser.parse_args()
    started=time.monotonic()
    try:
        result,expected=run()
    except Incomplete as error:
        print(json.dumps({'status':'INCOMPLETE','reason':str(error)}));raise SystemExit(3)
    WORK.mkdir(parents=True,exist_ok=True)
    (WORK/'producer.json').write_bytes(encoded(result))
    path=Path(__file__).resolve().parent/'expected.json'
    if args.write_expected:
        path.write_text(json.dumps(expected,indent=2)+'\n')
    else:
        require(json.loads(path.read_text())==json.loads(encoded(expected)),"expected record mismatch")
    metrics={'status':'COMPLETE','seconds':time.monotonic()-started,
             'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'summary':expected}
    (WORK/'producer_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    print(json.dumps(metrics))


if __name__=='__main__':
    main()
