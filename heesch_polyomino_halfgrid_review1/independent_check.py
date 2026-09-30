#!/usr/bin/env python3
"""six-reviewer-1: direct packing enumeration, independent of SAT/author code."""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product, permutations
import json
from pathlib import Path
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load_prior(path):
    expected = '478a4620f2520f281eecaec0077819684a885cb5cff01c9164a13eef65decba8'
    need(sha256(path.read_bytes()).hexdigest() == expected, 'reviewer geometry source changed')
    spec = spec_from_file_location('reviewer_geometry', path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def double(tile):
    return tuple(sorted((2*x+u, 2*y+v) for x,y in tile for u,v in product((0,1),repeat=2)))


def inventory(tile, geometry):
    """Anchor every translated cell to every required cell, then test full footprints."""
    root = set(tile)
    required = sorted(geometry.halo(root)-root)
    candidates = []
    for shape in geometry.views(tile):
        translations = sorted({(x-u,y-v) for x,y in required for u,v in shape})
        for tx,ty in translations:
            footprint = tuple((x+tx,y+ty) for x,y in shape)
            if not root.isdisjoint(footprint):
                continue
            candidates.append((shape,tx,ty,footprint))
    need(len({c[3] for c in candidates})==len(candidates), 'duplicate physical candidate')
    return required,candidates


def enumerate_packings(tile, geometry, max_nodes=2_000_000, max_seconds=40):
    """Required columns exactly once; all footprint columns at most once."""
    need(type(max_nodes) is int and max_nodes>0 and max_seconds>0,'invalid resource guard')
    required, candidates = inventory(tile, geometry)
    posts = {}
    for j,(_,_,_,footprint) in enumerate(candidates):
        for p in footprint:
            posts[p] = posts.get(p,0) | (1<<j)
    columns = [posts.get(p,0) for p in required]
    target_index = {p:i for i,p in enumerate(required)}
    target_masks = []
    conflicts = []
    for _,_,_,footprint in candidates:
        mask = clash = 0
        for p in footprint:
            if p in target_index:
                mask |= 1<<target_index[p]
            clash |= posts[p]
        need(mask!=0, 'candidate misses every required cell')
        target_masks.append(mask)
        conflicts.append(clash)
    models = []
    nodes = cuts = 0
    digest = sha256()
    started = time.monotonic()
    def visit(uncovered, available, chosen):
        nonlocal nodes,cuts
        nodes += 1
        if nodes>max_nodes:
            raise RuntimeError('node guard: incomplete, no negative conclusion')
        if nodes%1024==0 and time.monotonic()-started>max_seconds:
            raise RuntimeError('time guard: incomplete, no negative conclusion')
        if not uncovered:
            model = tuple(sorted(j+1 for j in chosen))
            models.append(model)
            digest.update(('M:'+','.join(map(str,model))+'\n').encode())
            return
        bits = uncovered
        best = None
        while bits:
            low = bits & -bits
            i = low.bit_length()-1
            options = columns[i] & available
            count = options.bit_count()
            if best is None or count<best[0]:
                best=(count,i,options)
                if count==0:
                    break
            bits ^= low
        count,i,options = best
        digest.update((str(i)+':'+str(count)+'\n').encode())
        if not count:
            cuts += 1
        while options:
            low = options & -options
            j = low.bit_length()-1
            visit(uncovered & ~target_masks[j],available & ~conflicts[j],chosen+(j,))
            options ^= low
    visit((1<<len(required))-1,(1<<len(candidates))-1,())
    need(len(models)==len(set(models)), 'duplicate model path')
    return {'required_cells':len(required),'candidates':len(candidates),'nodes':nodes,
            'zero_column_cuts':cuts,'models':sorted(models),'search_sha256':digest.hexdigest()},candidates


def ordered_patterns(k):
    """Unordered set partitions, then all orders of their blocks."""
    if not k:
        yield ()
        return
    def partitions(i, blocks):
        if i==k:
            yield blocks
            return
        for j in range(len(blocks)):
            yield from partitions(i+1,blocks[:j]+(blocks[j]+(i,),)+blocks[j+1:])
        yield from partitions(i+1,blocks+((i,),))
    for blocks in partitions(0,()):
        for order in permutations(range(len(blocks))):
            labels = [0]*k
            for rank,j in enumerate(order,1):
                for i in blocks[j]:labels[i]=rank
            yield tuple(labels)


def poses_of(tile,candidates,model):
    poses=[(0,tile,F(0),F(0))]
    for j in model:
        shape,tx,ty,_=candidates[j-1]
        undoubled=tuple(sorted(set((x//2,y//2) for x,y in shape)))
        need(double(undoubled)==shape, 'unpaired pixels')
        poses.append((1,undoubled,F(tx,2),F(ty,2)))
    return poses


def lifts(poses):
    groups=[[i for i,p in enumerate(poses) if p[axis]%1] for axis in (2,3)]
    for labels in product(*(tuple(ordered_patterns(len(g))) for g in groups)):
        new=[list(p) for p in poses]
        for axis,indices,pattern in zip((2,3),groups,labels):
            for i,rank in zip(indices,pattern):
                new[i][axis]=F(poses[i][axis]//1)+F(rank,len(indices)+1)
        yield [tuple(p) for p in new]


def half(t,theta=F(1,2)):
    return F(t//1)+(theta if t%1 else 0)


def controls(g):
    small,candidates=enumerate_packings(double(((0,0),)),g)
    required=set(g.halo(double(((0,0),))))-set(double(((0,0),)))
    # Literal full-footprint subset test, independent of search conflicts/MRV.
    literal=[]
    for mask in range(1<<len(candidates)):
        occupied=set();selected=[];bad=False
        for j,(_,_,_,footprint) in enumerate(candidates):
            if mask>>j&1:
                if not occupied.isdisjoint(footprint):bad=True;break
                occupied.update(footprint);selected.append(j+1)
        if not bad and required<=occupied:literal.append(tuple(selected))
    need(sorted(literal)==small['models'] and len(literal)==7,'tiny full subset comparison failed')
    # Every candidate inventory also agrees with a bbox translation generator.
    inventory_checks=0
    for tile in (((0,0),),((0,0),(1,0)),((0,0),(1,0),(0,1))):
        for scale in (1,2):
            S=double(tile) if scale==2 else tile
            req,actual=inventory(S,g);root=set(S);bounding=set()
            for shape in g.views(S):
                for tx in range(min(x for x,y in req)-max(x for x,y in shape),max(x for x,y in req)+1):
                    for ty in range(min(y for x,y in req)-max(y for x,y in shape),max(y for x,y in req)+1):
                        R=tuple((x+tx,y+ty) for x,y in shape)
                        if root.isdisjoint(R) and not set(req).isdisjoint(R):bounding.add(R)
            need(bounding=={c[3] for c in actual},'small inventory mismatch')
            inventory_checks+=1
    pattern_counts=[]
    for k in range(7):
        actual=list(ordered_patterns(k));literal=set()
        if not k:literal.add(())
        for q in range(1,k+1):
            literal.update(t for t in product(range(1,q+1),repeat=k) if set(t)==set(range(1,q+1)))
        need(len(actual)==len(set(actual)) and set(actual)==literal,'ordered pattern mismatch')
        pattern_counts.append(len(actual))
    values=sorted({F(i,q) for q in (1,2,3,4) for i in range(-2*q,2*q+1)})
    thresholds=quadrants=0
    for theta in (F(1,3),F(1,2),F(2,3)):
        for a,b in product(values,repeat=2):
            for n in range(-2,3):
                need(not (a-b>=n) or half(a,theta)-half(b,theta)>=n,'weak separation lost')
                need(not (a-b<=n) or half(a,theta)-half(b,theta)<=n,'weak reverse separation lost')
                thresholds+=1
        for a,v,sign in product(values,range(-2,3),(-1,1)):
            before=a<=v<a+1 if sign==1 else a<v<=a+1
            b=half(a,theta)
            after=b<=v<b+1 if sign==1 else b<v<=b+1
            need(before==after,'integer star predicate lost');quadrants+=1
    # Exact seven-square surrounds. Floors lose them; one positive phase
    # per axis at any theta in(0,1) preserves the root's strict surround.
    squares=0;scope_failure=False
    S=((0,0),)
    for a in (F(1,5),F(1,3),F(1,2),F(4,5)):
        poses=[(0,S,F(0),F(0)),(1,S,F(-1),F(0)),(1,S,F(1),F(0))]
        poses +=[(1,S,F(dx)+a,F(y)) for dx,y in product((-1,0),(-1,1))]
        g.check(S,1,poses,True)
        for theta in (F(1,3),F(1,2),F(2,3)):
            snapped=[(k,shape,half(x,theta),half(y,theta)) for k,shape,x,y in poses]
            g.check(S,1,snapped,True);squares+=1
        if a==F(1,3):
            shifted=[(k,shape,x+F(1,4),y) for k,shape,x,y in poses]
            snapped=[(k,shape,half(x),half(y)) for k,shape,x,y in shifted]
            x0,y0=snapped[0][2:]
            snapped=[(k,shape,x-x0,y-y0) for k,shape,x,y in snapped]
            try:g.check(S,1,snapped,True)
            except ValueError as e:need('surround' in str(e),'wrong scope control failure');scope_failure=True
    need(scope_failure,'noninteger-root counterexample lost')
    try:enumerate_packings(double(S),g,max_nodes=1)
    except RuntimeError:pass
    else:raise ValueError('incomplete search was accepted')
    # Pinch and actual-hole distinctions use the previously independently
    # audited rank-grid geometry module, with literal small boundary controls.
    topology_checks=0
    for mask in range(512):
        cells={(i%3,i//3) for i in range(9) if mask>>i&1}
        need(g.topology(cells)['disc']==g.boundary_disc(cells),'small boundary topology mismatch')
        topology_checks+=1
    return {'tiny_subsets':1<<len(candidates),'tiny_primary_models':len(small['models']),
            'bbox_inventory_checks':inventory_checks,'ordered_pattern_counts':pattern_counts,
            'weak_threshold_checks':thresholds,'integer_quadrant_checks':quadrants,
            'rational_square_surrounds':squares,'noninteger_root_counterexample':True,
            'incomplete_search_refused':True,'topology_masks':topology_checks}


def pinned_json(path,digest):
    raw=path.read_bytes()
    need(sha256(raw).hexdigest()==digest,path.name+' input changed')
    return json.loads(raw)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    repo=Path(__file__).resolve().parent.parent
    ap.add_argument('--author-dir',type=Path,default=repo/'heesch_polyomino_halfgrid')
    ap.add_argument('--prior-checker',type=Path,default=repo/'heesch_polyomino_motion_review1'/'independent_check.py')
    ap.add_argument('--prior-data',type=Path,default=repo/'heesch_polyomino_euler_cnf')
    ap.add_argument('--record',type=Path,help='write complete expected evidence to the given path')
    ap.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    args=ap.parse_args()
    g=load_prior(args.prior_checker)
    fixtures=pinned_json(args.author_dir/'fractional_examples.json','a513de0247bf1df2fb2ca58e95c455e38413ac9961ffa765a51787626950bef6')['cases']
    expected={c['i']:c for c in pinned_json(args.author_dir/'closed_expected.json','196c7730f39bfddd69471afc85264884ef9410fe93a9dab3d14c55204debde87')['cases']}
    manifest=pinned_json(args.author_dir/'family_expected.json','beaf12e422763a0f5be3eec973d10e2f8b59e4defab605f0e12f757fbdf9b3a2')
    prior=pinned_json(args.prior_data/'growth20_manifest.json','8f96c536c15f739130b6ca7e5a67fcba1ff1e51fa4bbc18b16d652182c24ff85')
    seed=pinned_json(args.prior_data/'kaplan17.json','24ceb5aefe2e0843d16d7ab7ced16f17356789426a12607b00cf956df02dbe51')['cells']
    family,growth=g.growth_components(seed)
    family_hash=sha256((json.dumps(family,separators=(',',':'))+'\n').encode()).hexdigest()
    need(len(family)==1233 and family_hash==manifest['family_sha256']==prior['family_sha256'],'growth family mismatch')
    indices=[r['i'] for r in prior['cases'] if r.get('radius')==1]
    need(len(indices)==434 and indices==[r['i'] for r in manifest['cases']],'complete input subset mismatch')
    control_result=controls(g)
    rows=[];positive={}
    for i,want in zip(indices,manifest['cases']):
        raw,candidates=enumerate_packings(double(family[i]),g)
        need(raw['candidates']==want['candidates'],'candidate count differs at'+str(i))
        need(bool(raw['models'])==(want['decision']=='positive'),'decision differs at'+str(i))
        rows.append([i,raw['candidates'],raw['nodes'],raw['zero_column_cuts'],len(raw['models']),raw['search_sha256']])
        if raw['models']:positive[i]=(raw,candidates)
    need(set(positive)=={58,311,1022},'positive case set differs')
    result=[]
    for c in fixtures:
        tile=g.normal(c['cells'])
        need(tile==family[c['i']],'explicit example is not the indexed family tile')
        raw,candidates=positive[c['i']]
        # The author's CNF reserves variable1 as true; physical candidates
        # are numbered1..N here and2..N+1 in that manifest.
        want=sorted(tuple(v-1 for v in m['selected_variables']) for m in expected[c['i']]['models'])
        need(raw['models']==want,'complete physical model set differs')
        coarse,_=enumerate_packings(tile,g)
        need(not coarse['models'],'coarse obstruction contradicted')
        reasons=Counter();holes=Counter();phase_counts=Counter();lcount=0
        for model in raw['models']:
            poses=poses_of(tile,candidates,model)
            g.check(tile,1,poses,holes_last=True)
            counts=tuple(sum(bool(p[a]%1) for p in poses) for a in (2,3))
            phase_counts[str(counts)]+=1
            for p in lifts(poses):
                lcount+=1
                try:
                    checked=g.check(tile,1,p,holes_last=True)
                except ValueError as e:
                    reasons[str(e)]+=1
                else:
                    h=checked['prefixes'][-1]['holes']
                    need(h>0,'unexpected hole-free corona')
                    need(checked['prefixes'][-1]['foreground_components']==1,'disconnected relaxed surround')
                    holes[str(h)]+=1
                    reasons['invalid prefix topology']+=1
        wanted=expected[c['i']]
        need(lcount==wanted['canonical_lifts_checked_twice'],'lift count differs')
        need(dict(holes)==wanted['valid_relaxed_lifts_by_holes'],'entrywise hole counts differ')
        mapped={k.replace('incomplete strict surround','incomplete surround'):v for k,v in reasons.items()}
        need(mapped==wanted['rejected_by_arrangement_reason'],'every lift rejection census differs')
        example_poses=[(p['level'],tuple(map(tuple,p['shape'])),*(F(x) for x in p['translation'])) for p in c['placements']]
        shown=g.check(tile,1,example_poses,True)['prefixes'][-1]
        w,h=max(x for x,y in tile)+1,max(y for x,y in tile)+1;L=max(w,h)
        upper=((w+2+2*L)*(h+2+2*L))//len(tile)-1
        need(upper==c['conditional_unrestricted_upper'],'finite-upper arithmetic differs')
        record={'i':c['i'],'halfgrid':raw,'coarse_grid':coarse,'phase_counts':dict(phase_counts),
                'ordered_lifts':lcount,'rejected':dict(sorted(reasons.items())),
                'valid_relaxed_lifts_by_holes':dict(sorted(holes.items())),
                'explicit_patch':shown,'unrestricted_finiteness_upper':upper}
        result.append(record)
    output={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'scope':'All434 old grid-zero family members and the universal first-corona bridge;799 earlier positive statuses are not replayed',
            'family_sha256':family_hash,'growth':growth,'controls':control_result,
            'all434_complete':True,'family_row_fields':['family_index','candidates','nodes','zero_column_cuts','models','search_sha256'],
            'family_rows':rows,'total_family_nodes':sum(r[2] for r in rows),'total_family_cuts':sum(r[3] for r in rows),
            'total_candidates':sum(r[1] for r in rows),'negative_cases':431,'positive_cases':[58,311,1022],
            'exceptions':result}
    encoded=json.dumps(output,sort_keys=True,indent=2)+'\n'
    if args.record:args.record.write_text(encoded)
    else:need(json.loads(args.expected.read_text())==json.loads(encoded),'complete expected evidence differs')
    print(encoded,end='')


if __name__=='__main__':
    main()
