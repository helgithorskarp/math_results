"""Independent full unfiltered two-star audit; six-reviewer-5.

No researcher executable is imported. The already published reviewer raw
carrier and unweighted clique algorithm are explicitly credited byte inputs.
All reported maxima require completed search, with positive literal witnesses.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time

import raw_carrier as raw
from clique import maximum

HERE = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def digest(value):
    return sha256(encode(value)).hexdigest()

def inputs(base=HERE):
    pins = json.loads((base/'INPUTS.json').read_text())
    for name, pin in pins.items():
        need(sha256((base/name).read_bytes()).hexdigest() == pin, 'changed input '+name)
    return (json.loads((base/'TWENTY_STARS.json').read_text()),
            json.loads((base/'SEED_CERTIFICATES.json').read_text()),
            json.loads((base/'BRIDGE.json').read_text()),
            json.loads((base/'AUTHOR_COLORS.json').read_text()))

def points(mask):
    return frozenset(p for p in range(18) if mask>>p & 1)

def image(mask, permutation):
    return sum(1<<permutation[p] for p in points(mask))

def packing(masks):
    need(type(masks) in (tuple, list) and len(set(masks)) == len(masks), 'duplicate word')
    need(all(type(w) is int and 0 < w < 1<<18 and w.bit_count() == 5 for w in masks), 'word domain')
    literal = [points(w) for w in masks]
    need(all(len(a&b) <= 2 for a,b in combinations(literal, 2)), 'literal packing collision')
    return literal

def roles(masks, u, y, v):
    words = packing(masks)
    x = 17
    need(len({x,u,y,v}) == 4, 'distinct marked roles')
    lam = lambda p,q: sum({p,q} <= w for w in words)
    covered = lambda p,q,t: any({p,q,t} <= w for w in words)
    need(sum(x in w for w in words) == sum(y in w for w in words) == 20, 'complete centers')
    need(lam(x,y) == 4 and lam(x,v) == 5 and not covered(x,y,v), 'assumption1')
    need(lam(x,u) in (3,4) and all(lam(x,p) in (4,5) for p in range(18) if p not in (x,u)), 'first pair row')
    deficient = {p for p in range(18) if p != x and lam(x,p) < 5}
    need(all(covered(x,u,p) for p in deficient-{u}), 'isolated deficient hub')
    need(lam(y,u) == lam(y,v) == 5 and all(lam(y,p) in (4,5) for p in range(18) if p != y), 'second pair row')
    triangles = [p for p in range(18) if p not in (x,u,y,v) and lam(x,p) == lam(y,p) == 4 and not covered(x,y,p)]
    return lam(x,u), triangles

def domain(core, y):
    # Complete lexicographic universe. This is a fresh pair-intersection
    # decoder, independent of the researcher's owned-triple filter.
    need(type(y) is int and 0 <= y < 17, 'second center')
    result = []
    for q in combinations([p for p in range(18) if p not in (17,y)], 5):
        m = sum(1<<p for p in q)
        if all((m&w).bit_count() <= 2 for w in core):
            result.append(m)
    return result

def graph(candidates):
    # Construct conflicts by physical triple incidence, then independently
    # compare every adjacency entry with literal intersections.
    n = len(candidates)
    owners = {}
    for i,w in enumerate(candidates):
        for t in combinations(sorted(points(w)), 3):
            owners[t] = owners.get(t,0) | (1<<i)
    conflict = [0]*n
    for bits in owners.values():
        rest = bits
        while rest:
            b = rest & -rest
            conflict[b.bit_length()-1] |= bits ^ b
            rest ^= b
    adjacency = [((1<<n)-1) & ~conflict[i] & ~(1<<i) for i in range(n)]
    for i,j in combinations(range(n), 2):
        need(bool(adjacency[i]>>j & 1) == (len(points(candidates[i])&points(candidates[j])) <= 2), 'triple/literal graph mismatch')
    return adjacency

def coloring(candidates, adjacency, colors, capacity):
    need(type(capacity) is int and 0 < capacity <= len(candidates), 'capacity domain')
    need(type(colors) is list and len(colors) == len(candidates), 'color population')
    need(all(type(c) is int and 0 <= c < capacity for c in colors) and set(colors) == set(range(capacity)), 'color labels')
    for i,j in combinations(range(len(candidates)), 2):
        if adjacency[i]>>j & 1:
            need(colors[i] != colors[j], 'improper color')

def representatives(data, bridge, certificate, deadline=None):
    rows, entries = bridge['raw_positive_maps'], certificate['entries']
    need(len(rows) == len(entries) == 34, 'representative population')
    need({e['index'] for e in entries} == set(range(34)), 'certificate index cover')
    by_index = {e['index']: e for e in entries}
    output, records, witnesses = [], [], []
    for k,row in enumerate(rows):
        need(deadline is None or time.monotonic() <= deadline, 'whole audit deadline: incomplete')
        i,(u,v,y) = row['first']; j,(su,sv,sx,sb) = row['second']
        phi = row['point_map']; core = row['word_masks']; e = by_index[k]
        need(len(phi) == 17 and all(type(p) is int for p in phi) and set(phi) == set(range(18))-{y}, 'literal relative bijection')
        need((phi[su],phi[sv],phi[sx]) == (u,v,17), 'relative role images')
        Q,P = data['stars'][i], data['stars'][j]
        decoded = sorted({sum(1<<p for p in w)+(1<<17) for w in Q} | {sum(1<<phi[p] for p in w)+(1<<y) for w in P})
        need(decoded == core and len(core) == 36, 'literal two-star decode')
        degree, triangles = roles(core,u,y,v)
        need(triangles == row['triangle_points'], 'triangle attribution')
        candidates = domain(core,y); adjacency = graph(candidates)
        coloring(candidates,adjacency,e['colors'],e['capacity'])
        edges = sum(a.bit_count() for a in adjacency)//2
        need((e['product_index'],e['first_fixture'],e['candidate_count'],e['candidate_sha256'],e['edges'],e['triangle_count'],e['upper_bound']) ==
             (row['product_index'],i,len(candidates),digest(candidates),edges,len(triangles),36+e['capacity']), 'entrywise researcher certificate mismatch')
        chosen,nodes = maximum(adjacency)
        completion = sorted(core+[candidates[a] for a in chosen])
        need(len(chosen) <= e['capacity'], 'clique exceeds checked coloring')
        need(roles(completion,u,y,v) == (degree,triangles), 'positive completion changed marked hypotheses')
        record = {'index': k, 'first_fixture': i, 'product_index': row['product_index'],
                  'lambda_xu': degree, 'triangle_count': len(triangles),
                  'candidates': len(candidates), 'candidate_sha256': digest(candidates),
                  'edges': edges, 'colors': e['capacity'], 'exact_residual': len(chosen),
                  'exact_total': len(completion), 'nodes': nodes, 'completion_sha256': digest(completion)}
        records.append(record)
        witnesses.append({'index': k, 'marks': {'x':17,'u':u,'y':y,'v':v}, 'lambda_xu':degree, 'word_masks':completion})
        output.append({'row':row, 'candidates':candidates,'adjacency':adjacency,'certificate':e,'degree':degree})
    return output,records,witnesses

def transports(data, positives, reps, deadline=None):
    actual, records = {}, []
    lookup = {}
    for k,r in enumerate(reps):
        i,(u,v,y)=r['row']['first']
        key=(i,u,y,v,tuple(r['row']['word_masks']))
        need(key not in lookup, 'duplicate normalized marked core')
        lookup[key]=k
    for q in positives:
        need(deadline is None or time.monotonic() <= deadline, 'whole audit deadline: incomplete')
        i,u,y,v=q['first']; matches=[]
        for h in data['groups'][i]:
            g=tuple(h)+(17,)
            if (i,g) not in actual:
                need(len(g)==18 and set(g)==set(range(18)), 'transport point domain')
                Q={frozenset(w) for w in data['stars'][i]}
                need({frozenset(g[p] for p in w) for w in Q} == Q, 'transport not actual star automorphism')
                actual[i,g]=True
            family=tuple(sorted(image(w,g) for w in q['family']))
            key=(i,g[u],g[y],g[v],family)
            if key in lookup:
                matches.append((lookup[key],g))
        need(len(matches)==1, 'raw positive transport missing or ambiguous')
        k,g=matches[0]; rep=reps[k]
        degree, triangles=roles(q['family'],u,y,v)
        need(degree==rep['degree'] and sorted(g[p] for p in triangles)==rep['row']['triangle_points'], 'transported local invariants')
        cs=domain(q['family'],y)
        image_to_color={w:c for w,c in zip(rep['candidates'],rep['certificate']['colors'])}
        need({image(w,g) for w in cs}==set(rep['candidates']), 'whole residual-domain transport')
        colors=[image_to_color[image(w,g)] for w in cs]
        edges=0
        for a,b in combinations(range(len(cs)),2):
            if (cs[a]&cs[b]).bit_count()<=2:
                need(colors[a]!=colors[b], 'transported color collision')
                edges+=1
        need(edges==rep['certificate']['edges'], 'transported edge count')
        records.append({'first':q['first'],'second':q['second'],'point_map':q['point_map'],
                        'representative':k,'transport':g,'family_sha256':digest(q['family']),
                        'candidate_sha256':digest(cs),'colors_sha256':digest(colors),
                        'lambda_xu':degree,'edges':edges})
    need({r['representative'] for r in records}==set(range(34)), 'representative never reached')
    return records

def run():
    started=time.monotonic()
    data,seeds,bridge,cert=inputs()
    carrier=raw.run(data,seeds)
    need(carrier['exact']==json.loads((HERE/'RAW_EXPECTED.json').read_text()), 'previous frozen raw carrier changed')
    reps,records,witnesses=representatives(data,bridge,cert,started+240)
    positive=carrier['_positives']
    # Every claimed normalized map must occur with the same two stars, exact
    # relative point map, full literal family, and triangle list in raw output.
    keys={(q['first'],q['second'],q['point_map'],q['family'],tuple(q['triangles'])) for q in positive}
    for row in bridge['raw_positive_maps']:
        i,(u,v,y)=row['first'];j,marks=row['second']
        key=((i,u,y,v),(j,*marks),tuple(row['point_map']),tuple(row['word_masks']),tuple(row['triangle_points']))
        need(key in keys, 'normalized researcher row absent from independent carrier')
    ts=transports(data,positive,reps,started+240)
    need(time.monotonic()-started<=240, 'whole audit budget hit: incomplete')
    exact={'status':'PASS_COMPLETE_UNFILTERED_AUDIT','agent':'six-reviewer-5','role':'independent mathematical reviewer',
           'raw_carrier':carrier['exact'],'representatives':records,'transports':len(ts),
           'transport_sha256':digest(ts),'transport_representation_census':dict(sorted(Counter(r['representative'] for r in ts).items())),
           'candidate_domains_sha256':digest([r['candidates'] for r in reps]),
           'total_representative_candidates':sum(r['candidates'] for r in records),
           'total_representative_edges':sum(r['edges'] for r in records),
           'exact_total_census':dict(sorted(Counter(r['exact_total'] for r in records).items())),
           'maximum_total':max(r['exact_total'] for r in records),
           'maximum_lambda4_total':max(r['exact_total'] for r in records if r['lambda_xu']==4),
           'total_clique_nodes':sum(r['nodes'] for r in records),
           'witnesses_sha256':digest(witnesses)}
    return json.loads(encode(exact)),witnesses,ts,time.monotonic()-started
