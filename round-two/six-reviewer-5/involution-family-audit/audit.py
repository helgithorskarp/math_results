"""Independent complete raw carrier, positive transports and literal graphs.

Imports only the byte-pinned, previously reviewed generic normalizer.
No swapped-pair researcher module or solver is imported.
"""
from collections import Counter
from itertools import combinations, permutations, product
import importlib.util
import json
from pathlib import Path
import time
from core import HERE, G, code_check, digest, image, mask, pin_inputs, points, require
from clique import maximum, twins

def partitions(items, fixed):
    """Every involution on a finite literal set with exactly fixed singletons."""
    items=tuple(items)
    if fixed < 0 or fixed > len(items) or (len(items)-fixed)%2: return
    if not items:
        yield ()
        return
    a=items[0]
    if fixed:
        for rest in partitions(items[1:],fixed-1): yield ((a,),)+rest
    for j,b in enumerate(items[1:],1):
        remaining=items[1:j]+items[j+1:]
        for rest in partitions(remaining,fixed): yield ((a,b),)+rest

def actual_maps(quads, mate, multiplicity):
    tails=sorted(tuple(v for v in q if v!=mate) for q in quads if mate in q)
    used={v for t in tails for v in t}
    require(len(tails)==multiplicity and len(used)==3*multiplicity,'common-tail partition')
    complement=sorted(set(range(17))-{mate}-used)
    require(len(complement)==16-3*multiplicity,'tail complement')
    maps=set()
    for fixed_tails in range(3):
        for tail_partition in partitions(range(multiplicity),fixed_tails):
            choices=[]
            for cell in tail_partition:
                if len(cell)==1:
                    t=tails[cell[0]]
                    # For a fixed three-tail, choose its only fixed vertex.
                    choices.append([tuple((v,v) if v==f else (v,next(z for z in t if z not in (v,f))) for v in t) for f in t])
                else:
                    ta,tb=(tails[k] for k in cell)
                    choices.append([tuple(pair for a,b in zip(ta,image) for pair in ((a,b),(b,a))) for image in permutations(tb)])
            for chosen in product(*choices):
                for outside in partitions(complement,2-fixed_tails):
                    q=list(range(18));q[17],q[mate]=mate,17
                    for mapping in chosen:
                        for a,b in mapping:q[a]=b
                    for cell in outside:
                        if len(cell)==2:q[cell[0]],q[cell[1]]=cell[1],cell[0]
                    require(sorted(q)==list(range(18)) and all(q[q[v]]==v for v in range(18)) and sum(q[v]==v for v in range(18))==2,'raw involution domain')
                    require({frozenset(q[v] for v in t) for t in tails}=={frozenset(t) for t in tails},'raw common-tail action')
                    maps.add(tuple(q))
    require(len(maps)=={3:5670,4:1620}[multiplicity],'complete involution-partition product')
    return tuple(sorted(maps))

def raw_carrier(quads, multiplicity):
    star = tuple(mask(q) | 1 << 17 for q in quads)
    require(len(star) == 20, 'complete star size')
    degrees = code_check(star)
    valid, counts, raw_hashes = {}, [], []
    for mate in range(17):
        if degrees[mate] != multiplicity:
            continue
        started = time.monotonic()
        maps = actual_maps(quads, mate, multiplicity)
        raw_hashes.append((mate, digest(maps)))
        private = tuple(tuple(q) for q in quads if mate not in q)
        private_masks = tuple(mask(q) for q in private)
        accepted = 0
        for g in maps:
            moved = tuple(mask(g[v] for v in q) for q in private)
            if any((a & b).bit_count() > 2 for a in private_masks for b in moved):
                continue
            words = tuple(sorted(set(star) | {image(w, g) for w in star}))
            reps = code_check(words, g)
            require(len(words) == 40-multiplicity and reps[17] == reps[mate] == 20 and
                    sum(w >> mate & 1 and w >> 17 & 1 for w in words) == multiplicity, 'positive star union')
            valid[(mate, g)] = words
            accepted += 1
        require(time.monotonic() - started < 30, 'INCOMPLETE per-mate guard')
        counts.append((mate, len(maps), accepted))
    return valid, counts, raw_hashes

def fixture_groups(quads, normalizer):
    q = normalizer.blocks(quads)
    k = normalizer.key(q)
    maps = sorted(set(p for target, p in normalizer.normalized(q) if target == k))
    require(all(sorted(p) == list(range(17)) and
                tuple(sorted(tuple(sorted(p[v] for v in b)) for b in q)) == q for p in maps),
            'nonactual fixture map')
    return tuple(p + (17,) for p in maps)

def normalize(words, g, mate):
    p = [-1] * 18
    p[17], p[mate] = 0, 1
    pairs = [(v, g[v]) for v in range(18) if v < g[v] and v not in (17, mate)]
    fixed = [v for v in range(18) if g[v] == v]
    require(len(pairs) == 7 and len(fixed) == 2, 'normalizing cycle structure')
    for i, (a, b) in enumerate(pairs, 1):
        p[a], p[b] = 2 * i, 2 * i + 1
    for i, a in enumerate(fixed, 16):
        p[a] = i
    require(sorted(p) == list(range(18)) and all(p[g[v]] == G[p[v]] for v in range(18)),
            'false conjugacy')
    normalized = tuple(sorted(image(w, p) for w in words))
    require(code_check(normalized, G)[:2] == (20, 20), 'normalized centers')
    return normalized

def rooted_cover(valid, group):
    remaining, roots, coverage = set(valid), [], []
    while remaining:
        mate, g = min(remaining)
        anchor = valid[(mate, g)]
        reached = {}
        for p in group:
            conjugate = [-1] * 18
            for v in range(18):
                conjugate[p[v]] = p[g[v]]
            key = (p[mate], tuple(conjugate))
            require(key in valid, 'fixture map left complete positive carrier')
            if key not in reached:
                moved = tuple(sorted(image(w, p) for w in anchor))
                require(moved == valid[key], 'false positive literal transport')
                reached[key] = p
        require(set(reached) <= remaining and (mate, g) in reached, 'overlapping/incomplete orbit cover')
        roots.append({'mate': mate, 'mapping': g, 'words': anchor,
                      'normalized': normalize(anchor, g, mate), 'orbit_size': len(reached)})
        for key, transport in sorted(reached.items()):
            coverage.append((key[0], key[1], len(roots) - 1, transport))
        remaining -= set(reached)
    require({(m, g) for m, g, root, p in coverage} == set(valid) and len(coverage) == len(valid),
            'positive coverage equality')
    return roots, coverage

def residual_universe():
    words = tuple(mask(w) for w in combinations(range(2, 18), 5))
    all_orbits = {tuple(sorted({w, image(w, G)})) for w in words}
    orbits = tuple(sorted(o for o in all_orbits if len(o) == 1 or (o[0] & o[1]).bit_count() <= 2))
    require({w for o in all_orbits for w in o} == set(words), 'incomplete whole-word orbits')
    owners, resources = {}, []
    for i, orbit in enumerate(orbits):
        triples = tuple(mask(t) for w in orbit for t in combinations(points(w), 3))
        require(len(triples) == len(set(triples)), 'internally invalid orbit')
        resources.append(triples)
        for t in triples:
            owners[t] = owners.get(t, 0) | 1 << i
    conflicts = []
    for ts in resources:
        occupied = 0
        for t in ts:
            occupied |= owners[t]
        conflicts.append(occupied)
    return orbits, owners, tuple(conflicts)

def residual_graph(anchor, universe):
    orbits, owners, conflicts = universe
    forbidden = 0
    for w in anchor:
        for t in combinations(points(w), 3):
            forbidden |= owners.get(mask(t), 0)
    selected = [i for i in range(len(orbits)) if not forbidden >> i & 1]
    local = tuple(orbits[i] for i in selected)
    rows = tuple(sum(1 << j for j, b in enumerate(selected) if i != j and not conflicts[a] >> b & 1)
                 for i, a in enumerate(selected))
    require(all((w & a).bit_count() <= 2 for o in local for w in o for a in anchor),
            'invalid eligible residual orbit')
    # The physical triple-incidence encoding is checked against every literal edge.
    require(all(bool(rows[i] >> j & 1) == all((a & b).bit_count() <= 2
                for a in local[i] for b in local[j])
                for i in range(len(local)) for j in range(i)), 'literal edge differs')
    return local, rows

def audit(work):
    pin_inputs()
    work=Path(work);work.mkdir(parents=True,exist_ok=True)
    started=time.monotonic()
    spec=importlib.util.spec_from_file_location('reviewed_generic_normalizer',HERE/'inputs/generic_star_audit.py')
    normalizer=importlib.util.module_from_spec(spec);spec.loader.exec_module(normalizer)
    fixtures=json.loads((HERE/'inputs/fixtures.json').read_text())['stars']
    expected_groups=json.loads((HERE/'GROUP_DIGESTS.json').read_text())
    require(len(fixtures)==len(expected_groups)==23,'fixture/group cover')
    groups=[]
    for i,quads in enumerate(fixtures):
        group=fixture_groups(quads,normalizer)
        require(len(group)==expected_groups[i]['order'] and normalizer.digest(tuple(p[:-1] for p in group))==expected_groups[i]['sha256'],'reviewed actual group digest')
        groups.append(group)
    universe=residual_universe();result={}
    for multiplicity in (3,4):
        author=json.loads((HERE/('AUTHOR_THREE.json' if multiplicity==3 else 'AUTHOR_FOUR.json')).read_text())
        roots,summaries,proof,raw_proof=[],[],[],[]
        for i,quads in enumerate(fixtures):
            require(time.monotonic()-started<240,'INCOMPLETE whole audit deadline')
            valid,counts,hashes=raw_carrier(quads,multiplicity)
            representatives,coverage=rooted_cover(valid,groups[i])
            for root in representatives:root['fixture']=i
            proof.extend((i,m,g,len(roots)+ri,p) for m,g,ri,p in coverage)
            roots.extend(representatives);raw_proof.append((i,hashes))
            summaries.append({'fixture':i,'eligible_mates':len(counts),'raw_maps':sum(c[1] for c in counts),'valid_maps':len(valid),'roots':len(representatives),'mate_counts':counts})
            # Compare every author's fixture record, including zero-valid ones.
            a=author['raw_summary']['fixtures'][i]
            require(all(a[k]==summaries[-1][k] for k in ('fixture','eligible_mates','raw_maps','valid_maps')),'entrywise author carrier discrepancy')
        cases=[]
        for ri,root in enumerate(roots):
            require(time.monotonic()-started<240,'INCOMPLETE whole audit deadline')
            anchor=root['normalized'];old=author['weighted_records'][ri]
            require(tuple(w for w in old['witness'] if w&3)==anchor,'entrywise author rooted anchor discrepancy')
            orbits,adjacency=residual_graph(anchor,universe)
            expanded,carriers=twins(adjacency,tuple(map(len,orbits)))
            chosen,nodes=maximum(expanded)
            selected=set(carriers[v] for v in chosen)
            extension={w for j in selected for w in orbits[j]}
            words=tuple(sorted(set(anchor)|extension))
            require(len(extension)==len(chosen) and len(words)==40-multiplicity+len(chosen),'complete true-twin expansion')
            degrees=code_check(words,G)
            require(degrees[:2]==(20,20) and sum(w&3==3 for w in words)==multiplicity,'literal maximum scoped witness')
            require((old['fixture'],old['vertices'],old['fixed_vertices'],old['paired_vertices'],old['residual_weight'])==(root['fixture'],len(orbits),sum(len(o)==1 for o in orbits),sum(len(o)==2 for o in orbits),len(chosen)),'entrywise author completion discrepancy')
            # The author's weighted hash is a physical vertex/bit-row record.
            order=tuple(sorted(range(len(orbits)),key=lambda i:(-len(orbits[i]),-adjacency[i].bit_count(),i)))
            ordered_orbits=tuple(orbits[i] for i in order)
            ordered_rows=tuple(sum(1<<j for j,b in enumerate(order) if adjacency[a]>>b&1) for a in order)
            require(digest({'vertices':ordered_orbits,'adjacency':ordered_rows})==old['graph_sha256'],'whole physical author weighted graph differs after explicit vertex bijection')
            neighbor_lists=tuple(tuple(j for j in range(len(expanded)) if row>>j&1) for row in expanded)
            native=author['native_records'][ri]
            require(digest(neighbor_lists)==native['literal_expansion_sha256'] and native['expanded_vertices']==len(expanded),'whole physical author true-twin graph differs')
            case={'root':ri,'fixture':root['fixture'],'anchor_sha256':digest(anchor),'orbit_vertices':len(orbits),'fixed_orbits':sum(len(o)==1 for o in orbits),'expanded_vertices':len(expanded),'residual_maximum':len(chosen),'full_maximum':len(words),'nodes':nodes,'graph_sha256':digest({'orbits':orbits,'adjacency':adjacency}),'witness_sha256':digest(words)}
            cases.append(case)
            (work/('m%d-case-%02d.json'%(multiplicity,ri))).write_text(json.dumps({'summary':case,'words':words,'involution':G},indent=2))
        require(len(cases)==len(roots)==len(author['weighted_records']),'complete root/case cover')
        result[str(multiplicity)]={'fixtures':summaries,'raw_maps':sum(r['raw_maps'] for r in summaries),'eligible_mates':sum(r['eligible_mates'] for r in summaries),'valid_maps':len(proof),'rooted_cases':len(roots),'raw_sha256':digest(raw_proof),'positive_transports_sha256':digest(proof),'roots_sha256':digest(roots),'cases':cases,'maximum_code_size':max(c['full_maximum'] for c in cases),'nodes':sum(c['nodes'] for c in cases),'max_nodes':max(c['nodes'] for c in cases)}
        (work/('m%d-positive-cover.json'%multiplicity)).write_text(json.dumps({'roots':roots,'coverage':proof}))
    require(time.monotonic()-started<240,'INCOMPLETE whole audit deadline')
    require(result['3']['maximum_code_size']==56 and result['4']['maximum_code_size']==58,'claimed scoped maximum discrepancy')
    return json.loads(json.dumps({'status':'PASS_COMPLETE_MULTIPLICITY_THREE_AND_FOUR','agent':'six-reviewer-5','role':'independent mathematical reviewer','scopes':result},sort_keys=True)),time.monotonic()-started
