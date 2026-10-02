"""Physical/MRV audit of one-Q boundary, all-Q maps and all normalized69s.

six-code-2, researcher. Imports no producer. Literal subset buckets and
adaptive physical domains supply independent algorithms by this author;
external-person review and ordinary proof bridges remain separate.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time
from point_helpers import encoded, literal, point_set, require


def core_family(cap, old, hole_ids, q, guard):
    domains = {i: tuple(old[i] - {p} for p in sorted(old[i] & cap)
                       if len((old[i] - {p}) & q) <= 1)
               for i in range(len(old)) if i not in hole_ids and len(old[i] & cap) >= 3}
    require(all(len(t) == 4 and len(t & cap) <= 2 for ts in domains.values() for t in ts),
            'physical required-tail domain')
    keys, nodes = set(), 0

    def visit(assignment):
        nonlocal nodes
        nodes += 1
        if nodes % 2048 == 0:
            guard('physical-MRV')
        if len(assignment) == len(domains):
            keys.add(tuple((i, literal(t)) for i, t in sorted(assignment.items())))
            return
        available = {i: tuple(t for t in ts if all(len(t & u) <= 1 for u in assignment.values()))
                     for i, ts in domains.items() if i not in assignment}
        next_i = min(available, key=lambda i: (len(available[i]), i))
        for tail in available[next_i]:
            visit(assignment | {next_i: tail})

    visit({})
    return keys, nodes, len(domains)


def check_core_keys(actual, expected):
    require(actual == expected, 'physical complete core keys differ')


def check_color(colors, i, j):
    require(colors[i] != colors[j], 'same-color physical edge')


def check_map(p, old, q, stated):
    require(sorted(p) == list(range(18)) and p[17] == 17, 'invalid Q point map')
    require({frozenset(p[v] for v in w) for w in old} == set(old), 'Q map fails wholeD')
    target = literal(frozenset(p[v] for v in q))
    require(target == stated, 'Q map target differs')
    return target


def check_packing(words, expected_size):
    require(len(words) == len(set(words)) == expected_size, 'positive distinct word count')
    require(all(type(w) is int and 0 <= w < 1 << 18 and w.bit_count() == 5 for w in words),
            'positive weight-five domain')
    ps = tuple(frozenset(v for v in range(18) if w >> v & 1) for w in words)
    require(all(len(a & b) <= 2 for a, b in combinations(ps, 2)), 'positive physical collision')
    triples = [t for w in ps for t in combinations(sorted(w), 3)]
    require(len(triples) == len(set(triples)) == 10 * expected_size, 'positive triple ownership')
    return ps


def check_boundary(words, old, q, size):
    ps = check_packing(words, size)
    R = len(set(old) - set(ps))
    caps = tuple(w for w in ps if 17 not in w and w not in old)
    contained = tuple(w - {17} for w in ps if 17 in w and any(w - {17} <= b for b in old))
    noncontained = tuple(w - {17} for w in ps if 17 in w and not any(w - {17} <= b for b in old))
    require(noncontained == (q,) and R == len(contained) + 4 and len(caps) == size - 65,
            'positive boundary normal form differs')
    return {'size':size, 's':len(caps), 'a':len(contained), 't':1, 'R':R,
            'pair_checks':size * (size-1) // 2, 'owned_triples':10*size}


def rejection(label, callback, expected):
    try:
        callback()
    except ValueError as error:
        require(str(error) == expected, 'control rejected for unintended reason: ' + label)
        return label
    raise ValueError('semantic damage accepted: ' + label)


def main():
    parser = argparse.ArgumentParser()
    for name in ('carrier','graph','maps','colors','witness-dir','baseline69','work'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.work.exists(), 'fresh one-Q point audit required')
    args.work.mkdir(parents=True)
    begin = time.monotonic()

    def guard(stage):
        require(time.monotonic()-begin < 60, 'INCOMPLETE initial60s one-Q audit: '+stage)

    raw = args.carrier.read_bytes()
    d = json.loads(raw)
    old = tuple(point_set(w,5) for w in d['parent_words'])
    require(len(old) == len(set(old)) == 68, 'literal68D')
    dt = [t for w in old for t in combinations(sorted(w),3)]
    require(len(dt) == len(set(dt)) == 680 and set(dt) == set(combinations(range(17),3)),
            'literal680-tripleD')
    q = point_set(d['noncontained_q'],4)
    require(not any(q <= w for w in old), 'Q is contained')
    hole_ids = {i for i,b in enumerate(old) if len(b & q) >= 3}
    holes = {old[i] for i in hole_ids}
    require(len(holes) == 4 and all(len(q & h) == 3 for h in holes) and
            holes == {point_set(w,5) for w in d['hole_words']}, 'all four physical Q blockers')
    caps = tuple(frozenset(ps) for ps in combinations(range(17),5)
                 if frozenset(ps) not in old and len(frozenset(ps) & q) <= 2 and
                 all(len(frozenset(ps) & b) <= 3 for i,b in enumerate(old) if i not in hole_ids))
    require([r['cap'] for r in d['caps']] == [literal(c) for c in caps], 'complete cap carrier/order')
    cap_domain, actual, core_caps, core_tails = set(caps), defaultdict(set), [], []
    for c in d['cores']:
        cap = point_set(c['cap'],5)
        require(cap in cap_domain, 'core cap outside physical domain')
        ids, tails = c['parents'], c['tails']
        require(len(ids) == len(set(ids)) == len(tails) and set(ids) ==
                {i for i,b in enumerate(old) if i not in hole_ids and len(cap & b) >= 3},
                'physical required-parent carrier')
        ts = tuple(point_set(t,4) for t in tails)
        require(all(t <= old[i] and len(t & q) <= 1 and len(t & cap) <= 2
                    for i,t in zip(ids,ts)) and all(len(a & b) <= 1 for a,b in combinations(ts,2)),
                'physical required-tail compatibility')
        key = tuple(sorted(zip(ids,tails)))
        require(key not in actual[cap], 'duplicate core')
        actual[cap].add(key); core_caps.append(cap); core_tails.append(ts)
    key_digest, mr_nodes, offset, hist = hashlib.sha256(),0,0,Counter()
    for cap,entry in zip(caps,d['caps']):
        expected,nodes,parents = core_family(cap,old,hole_ids,q,guard)
        mr_nodes += nodes
        require(mr_nodes <= 2_000_000, 'INCOMPLETE initial two-million MRV states')
        check_core_keys(actual[cap],expected)
        count = len(expected)
        require(entry['first_core'] == offset and entry['core_count'] == count and
                all(c['cap'] == literal(cap) for c in d['cores'][offset:offset+count]),
                'zero/positive cap-prefix coverage')
        offset += count
        key_digest.update(encoded([literal(cap),sorted(expected)]))
        hist[tuple(len(cap & point_set(w,5)) for w in d['hole_words'])+(parents,count)] += 1
        guard('complete-cap-keys')
    require(offset == len(d['cores']), 'full core prefix differs')
    cap_occ,tail_occ = defaultdict(int),defaultdict(int)
    for i,(cap,ts) in enumerate(zip(core_caps,core_tails)):
        cap_occ[cap] |= 1 << i
        for t in ts:tail_occ[t] |= 1 << i
    cap3,tail3,tail2 = defaultdict(int),defaultdict(int),defaultdict(int)
    for cap,bits in cap_occ.items():
        for t in combinations(sorted(cap),3):cap3[t] |= bits
    for tail,bits in tail_occ.items():
        for t in combinations(sorted(tail),3):tail3[t] |= bits
        for t in combinations(sorted(tail),2):tail2[t] |= bits
    cap_bad,tail_bad = {},{}
    for cap in cap_occ:
        bad = 0
        for t in combinations(sorted(cap),3):bad |= cap3[t] | tail3[t]
        cap_bad[cap] = bad
    for tail in tail_occ:
        cb,pb = 0,0
        for t in combinations(sorted(tail),3):cb |= cap3[t]
        for t in combinations(sorted(tail),2):pb |= tail2[t]
        tail_bad[tail] = cb | (pb & ~tail_occ[tail])
    gr = args.graph.read_bytes();g = json.loads(gr)
    color_raw=args.colors.read_bytes();color_data=json.loads(color_raw);colors=color_data['colors']
    n=len(core_caps)
    require(g['vertices']==n and len(g['adjacency_hex'])==n and
            g['core_carrier_sha256']==hashlib.sha256(raw).hexdigest(), 'graph input scope')
    require(len(colors)==n and all(type(c) is int and 0<=c<color_data['color_count'] for c in colors)
            and color_data['graph_sha256']==hashlib.sha256(gr).hexdigest(), 'color domain/scope')
    all_bits=(1 << n)-1; rows_digest=hashlib.sha256(); neighbors=[];degrees=Counter()
    for i,(cap,ts) in enumerate(zip(core_caps,core_tails)):
        bad=cap_bad[cap]
        for t in ts:bad |= tail_bad[t]
        row=all_bits & ~bad
        require(not row >> i & 1 and row==int(g['adjacency_hex'][i],16), 'complete physical row differs')
        rows_digest.update(encoded([i,format(row,'x')]));degrees[row.bit_count()]+=1
        nb=set()
        while row:
            bit=row & -row;row^=bit;j=bit.bit_length()-1
            check_color(colors,i,j);nb.add(j)
        neighbors.append(nb)
        if i%256==0:guard('complete-physical-graph')
    require(sum(k*v for k,v in degrees.items())==2*g['edges'] and
            all(i in neighbors[j] for i,row in enumerate(neighbors) for j in row), 'edge/symmetry mismatch')
    tri_inc=four_inc=five_inc=edge_tests=triple_tests=five_tests=0
    cliques=set()
    for i,row in enumerate(neighbors):
        for j in sorted(v for v in row if v>i):
            edge_tests+=1;common=row & neighbors[j];tri_inc+=len(common)
            for k in common:
                triple_tests+=1;ck=common & neighbors[k];four_inc+=len(ck)
                for ell in ck:cliques.add(tuple(sorted((i,j,k,ell))))
                for ell,m in combinations(sorted(ck),2):
                    five_tests+=1
                    if m in neighbors[ell]:five_inc+=1
            require(edge_tests+triple_tests+five_tests<=2_000_000, 'INCOMPLETE initial clique audit states')
        if i%128==0:guard('clique-incidences')
    require(tri_inc%3==four_inc%12==five_inc%30==0 and len(cliques)==four_inc//12,
            'clique incidence mismatch')
    covers=json.loads(args.maps.read_bytes())
    require(covers['canonical_q']==literal(q), 'canonicalQ differs')
    physical_qs={literal(frozenset(ps)) for ps in combinations(range(17),4)
                 if not any(frozenset(ps)<=b for b in old)}
    targets=set()
    for entry in covers['maps']:
        target=check_map(entry['point_map'],old,q,entry['target_q'])
        require(target not in targets, 'repeatedQ target');targets.add(target)
    require(targets==physical_qs and len(targets)==2040, 'all physicalQ map cover differs')
    positives=[]
    for size in range(65,71):
        p=args.witness_dir/f'WITNESS{size}.json'
        if p.exists():positives.append(check_boundary(json.loads(p.read_bytes())['words'],old,q,size))
    normal_forms=[];normal_words=set()
    for ids in sorted(cliques):
        removed=holes | {old[p] for i in ids for p in d['cores'][i]['parents']}
        cs={core_caps[i] for i in ids};ts={t for i in ids for t in core_tails[i]}
        ps=(set(old)-removed) | cs | {t|{17} for t in ts} | {q|{17}}
        words=tuple(sorted(literal(w) for w in ps))
        decode=check_boundary(words,old,q,69)
        require(words not in normal_words, 'duplicate normalized69');normal_words.add(words)
        normal_forms.append({'core_ids':ids,'words':words,'decoded':decode})
    require(len(normal_forms)==10 and color_data['color_count']==4 and five_inc==0,
            'computed boundary expectation differs; no generalized claim')
    first69=json.loads((args.witness_dir/'WITNESS69.json').read_bytes())['words']
    require(tuple(sorted(first69)) in normal_words, 'positive69 outside normalized census')
    baseline_raw=args.baseline69.read_bytes();lines=baseline_raw.decode().splitlines()
    require(len(lines)==69 and all(len(s)==18 and set(s)<={'0','1'} for s in lines), 'baseline69 literal binary domain')
    baseline=[int(s,2) for s in lines];baseline_ps=check_packing(baseline,69)
    target_cap=next(c for c in caps if actual[c]);expected,_,_=core_family(target_cap,old,hole_ids,q,guard)
    damaged=set(actual[target_cap]);damaged.pop()
    controls=[rejection('omitted-valid-core',lambda:check_core_keys(damaged,expected),'physical complete core keys differ')]
    bad_map=list(covers['maps'][0]['point_map']);bad_map[0]=bad_map[1]
    controls.append(rejection('nonbijective-Q-map',lambda:check_map(bad_map,old,q,covers['maps'][0]['target_q']),'invalid Q point map'))
    i=next(i for i,row in enumerate(neighbors) if row);j=min(neighbors[i]);damaged_colors=list(colors);damaged_colors[j]=colors[i]
    controls.append(rejection('same-color-physical-edge',lambda:check_color(damaged_colors,i,j),'same-color physical edge'))
    damaged_words=list(first69[:-1])+[first69[0]]
    controls.append(rejection('duplicate-positive69-word',lambda:check_packing(damaged_words,69),'positive distinct word count'))
    first_ps=sorted(check_packing(first69,69)[0]);four=first_ps[:4]
    collision=next(literal(four)|(1 << p) for p in range(18) if p not in first_ps and (literal(four)|(1 << p)) not in first69)
    collided=list(first69[:-1])+[collision]
    controls.append(rejection('distinct-weight-five-collision',lambda:check_packing(collided,69),'positive physical collision'))
    normal_packet={'agent':'six-code-2','role':'researcher','canonical_q':literal(q),
        'status':'ALL10_NORMALIZED69_FIXED_Q_PACKINGS_PHYSICALLY_CHECKED',
        'normal_forms':normal_forms,'scope':'Optional contained tails outside all blockers restored toD. Actual packings with such optional tails need not be one of these literal codes.'}
    nb=encoded(normal_packet);(args.work/'NORMAL_FORMS69.json').write_bytes(nb)
    degree_hist=lambda ps:sorted(Counter(sum(v in w for w in ps) for v in range(18)).items())
    record={'agent':'six-code-2','role':'researcher','status':'COMPLETE_PHYSICAL_Q_BOUNDARY_SHARP69_ALL2040_MAPS_POSITIVE4COLORS_AND_ALL10_NORMAL_FORMS',
        'noncontained_q':literal(q),'empty_holes':d['hole_words'],'prospective_caps':len(caps),
        'zero_core_caps':sum(not actual[c] for c in caps),'partial_cores':n,'adaptive_MRV_nodes':mr_nodes,
        'physical_core_key_sha256':key_digest.hexdigest(),'physical_graph_row_sha256':rows_digest.hexdigest(),
        'complete_physical_rows':n,'edges':g['edges'],'triangles':tri_inc//3,'four_cliques':four_inc//12,'five_cliques':five_inc//30,
        'edge_tests':edge_tests,'triangle_neighborhood_tests':triple_tests,'five_pair_tests':five_tests,
        'proper_color_count':color_data['color_count'],'color_classes':sorted(Counter(colors).items()),
        'degree_histogram':sorted(degrees.items()),'cap_core_histogram':[list(k)+[v] for k,v in sorted(hist.items())],
        'all_Q_maps':len(targets),'wholeD_images_checked':68*len(targets),'positive_witnesses':positives,
        'normalized69_count':len(normal_forms),'normalized69_sha256':hashlib.sha256(nb).hexdigest(),
        'normalized69_degree_histograms':[degree_hist(check_packing(r['words'],69)) for r in normal_forms],
        'known_baseline69_sha256':hashlib.sha256(baseline_raw).hexdigest(),'known_baseline69_pairs':2346,
        'known_baseline69_triples':690,'known_baseline69_degree_histogram':degree_hist(baseline_ps),
        'isomorphism_or_novel69_claim':False,'semantic_damage_rejections':controls,'external_review':'pending; same author algorithms',
        'formalized':False,'ordinary_bridge':'t1,R=a+4: four empty Q blockers, exact core restriction/pairwise gluing/optional-tail restoration and actual wholeD point transport. Sharp69; not global endpoint or new lower bound.'}
    guard('complete-one-Q-audit')
    rb=encoded(record);(args.work/'EXACT_RESULT.json').write_bytes(rb)
    ex={'agent':'six-code-2','role':'researcher','seconds':time.monotonic()-begin,
        'peak_RSS_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'initial_whole_guard_seconds':60,
        'initial_MRV_and_clique_state_guard':2_000_000,'exact_bytes':len(rb),'exact_sha256':hashlib.sha256(rb).hexdigest(),
        'normal_forms_bytes':len(nb),'normal_forms_sha256':hashlib.sha256(nb).hexdigest()}
    (args.work/'EXECUTION.json').write_bytes(encoded(ex));print(json.dumps(ex,sort_keys=True),flush=True)


if __name__=='__main__':main()
