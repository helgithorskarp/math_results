#!/usr/bin/env python3
"""Independent degree DFS, fixed-pair covers and binary conflict search."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import resource
import time
import argparse
import subprocess

SOURCE=Path(__file__).resolve().parent
ROOT=None


def graph_degree_dfs(n, allowed, degrees):
    allowed=set(allowed);answers=[];need=list(degrees);nodes=0;started=time.monotonic()
    def visit(v,edges):
        nonlocal nodes
        nodes+=1
        if nodes>200000 or time.monotonic()-started>10:raise RuntimeError('INCOMPLETE degree DFS guard')
        if v==n:
            if any(need):raise RuntimeError('nonzero terminal degree')
            answers.append(tuple(sorted(edges)));return
        neighbors=[u for u in range(v+1,n) if (v,u) in allowed and need[u]>0]
        if need[v]<0 or need[v]>len(neighbors):return
        want=need[v];need[v]=0
        for chosen in combinations(neighbors,want):
            for u in chosen:need[u]-=1
            good=not any(need[u]<0 or need[u]>sum((u,w) in allowed and need[w]>0 for w in range(u+1,n))
                         +sum((w,u) in allowed and need[w]>0 for w in range(v+1,u))
                         for u in range(v+1,n))
            if good:visit(v+1,edges+[(v,u) for u in chosen])
            for u in chosen:need[u]+=1
        need[v]=want
    visit(0,[])
    if len(answers)!=len(set(answers)):raise RuntimeError('duplicate degree graph')
    return sorted(answers),nodes


def closure(n,generators):
    known={tuple(range(n))};front=[tuple(range(n))]
    while front:
        p=front.pop()
        for q in generators:
            r=tuple(q[p[z]] for z in range(n))
            if r not in known:known.add(r);front.append(r)
    return sorted(known)


def image_graph(edges,p):return tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in edges))


def partition(graphs,maps):
    domain=set(graphs);covered=set();records=[]
    for g in graphs:
        if g in covered:continue
        orbit={image_graph(g,p) for p in maps}
        if orbit&covered or not orbit<=domain:raise RuntimeError('invalid graph partition')
        covered.update(orbit);records.append((g,len(orbit)))
    if covered!=domain:raise RuntimeError('missing graph')
    return records


def missing(shape):
    # Literal degree/attachment model, regenerated without generator imports.
    cores=[[(0,1),(0,2)],[(0,1),(1,2)],[(0,2),(1,2)],[(0,1),(0,2),(1,2),(15,16)]]
    cohorts=[[(3,8),(8,14),(14,17)],[(3,9),(9,14),(14,17)],
             [(3,9),(9,15),(15,17)],[(3,8),(8,13),(13,15)]]
    return set(cores[shape])|{(h,z) for h,(lo,hi) in enumerate(cohorts[shape]) for z in range(lo,hi)}


def from_graph(shape,g):
    if shape in (0,1):
        rows=[{0},{0},{0},{1},{1},{2},{2},{2},{1,2,3,4}]
        counters={(1,2):5,(0,2):8,(0,1):14}
        role=lambda v:0 if v<3 else 1 if v<5 else 2
        for a,b in g:
            key=(role(a),role(b));z=counters[key];counters[key]+=1
            rows[a].add(z);rows[b].add(z)
        if shape==1:
            point={0:1,1:0,2:2,**{z:z+6 for z in range(3,8)},**{z:z-5 for z in range(8,14)},
                   **{z:z for z in range(14,17)}}
            rows=[{point[z] for z in row} for row in rows]
    elif shape==3:
        rows=[{0,15},{0,16},{0},{1,15},{1,16},{1},{2,15},{2,16},{2},{2}]
        counters={(1,2):3,(0,2):8,(0,1):13}
        role=lambda v:0 if v<3 else 1 if v<6 else 2
        for a,b in g:
            key=(role(a),role(b));z=counters[key];counters[key]+=1
            rows[a].add(z);rows[b].add(z)
    else:raise RuntimeError('shape2 separately certified as the cube incidence model')
    if any(len(r)!=4 for r in rows):raise RuntimeError('wrong high-block width')
    return sorted(sum(1<<z for z in row) for row in rows)


def literal_star(shape,words):
    blocks=[frozenset(z for z in range(17) if w>>z&1) for w in words]
    if len(blocks)!=20 or len(set(blocks))!=20 or any(len(b)!=4 for b in blocks):raise RuntimeError('bad first star')
    if any(len(a&b)>1 for a,b in combinations(blocks,2)):raise RuntimeError('first-star intersection')
    pairs=set(combinations(range(17),2))
    actual=pairs-set().union(*(set(combinations(sorted(b),2)) for b in blocks))
    if actual!=missing(shape):raise RuntimeError('first-star leave')
    if [sum(z in b for b in blocks) for z in range(17)]!=[3,3,4]+[5]*14:raise RuntimeError('first-star degree')


def cover_fixed(shape,fixed):
    blocks=[frozenset(z for z in range(17) if w>>z&1) for w in fixed]
    used=set().union(*(set(combinations(sorted(b),2)) for b in blocks))
    target=set(combinations(range(17),2))-missing(shape)-used
    if any(p[0]<3 for p in target):raise RuntimeError('high pairs not yet fixed')
    candidates=[]
    for q in combinations(range(3,17),4):
        six=frozenset(combinations(q,2))
        if six<=target:candidates.append((sum(1<<z for z in q),six))
    answers=[];nodes=0;started=time.monotonic()
    def visit(left,chosen):
        nonlocal nodes
        nodes+=1
        if nodes>200000 or time.monotonic()-started>10:raise RuntimeError('INCOMPLETE fixed-pair cover guard')
        if not left:
            star=sorted(fixed+chosen);literal_star(shape,star);answers.append(star);return
        p=min(left)
        for mask,six in candidates:
            if p in six and six<=left:visit(left-six,chosen+[mask])
    visit(target,[])
    return sorted(answers),nodes


def first_star_check():
    first=json.loads((ROOT/'highstar_domain.json').read_text())
    allowed0=[(i,j) for i in range(8) for j in range(i+1,8)
              if (0 if i<3 else 1 if i<5 else 2)!=(0 if j<3 else 1 if j<5 else 2)]
    graphs0,n0=graph_degree_dfs(8,allowed0,[3]*8)
    generators=[]
    for a,b in [(0,1),(1,2),(3,4),(5,6),(6,7)]:
        p=list(range(8));p[a],p[b]=p[b],p[a];generators.append(tuple(p))
    maps0=closure(8,generators);reps0=partition(graphs0,maps0)
    allowed3=[(i,j) for i in range(10) for j in range(i+1,10)
              if (0 if i<3 else 1 if i<6 else 2)!=(0 if j<3 else 1 if j<6 else 2)
              and (i,j) not in [(0,3),(0,6),(3,6),(1,4),(1,7),(4,7)]]
    graphs3,n3=graph_degree_dfs(10,allowed3,[2,2,3,2,2,3,2,2,3,3])
    p=list(range(10))
    for a,b in [(0,1),(3,4),(6,7)]:p[a],p[b]=p[b],p[a]
    q=list(range(10));q[8],q[9]=q[9],q[8]
    maps3=closure(10,[tuple(p),tuple(q)]);reps3=partition(graphs3,maps3)
    # Enumerate the24 labeled cubic bipartite graphs instead of assuming uniqueness.
    cube,n2=graph_degree_dfs(8,[(i,j) for i in range(4) for j in range(4,8)],[3]*8)
    generators=[]
    for a,b in [(0,1),(2,3),(4,5),(5,6),(6,7)]:
        p=list(range(8));p[a],p[b]=p[b],p[a];generators.append(tuple(p))
    cube_maps=closure(8,generators)
    if len(cube)!=24 or len(partition(cube,cube_maps))!=1:raise RuntimeError('cube uniqueness replay failed')
    expected=[]
    for shape,reps in [(0,reps0),(1,reps0),(3,reps3)]:
        for i,(graph,size) in enumerate(reps):expected.append(dict(shape=shape,orbit=i,orbit_size=size,graph=[list(e) for e in graph],fixed=from_graph(shape,graph)))
    shape2=next(d for d in first['cases'] if d['shape']==2)
    # An untrusted chosen cube representative is accepted only by literal incidence.
    fixed=shape2['fixed'];blocks=[{z for z in range(17) if w>>z&1} for w in fixed]
    if len(blocks)!=9 or len({frozenset(b) for b in blocks})!=9 or any(len(b)!=4 for b in blocks) or any(
            len(a&b)>1 for a,b in combinations(blocks,2)):
        raise RuntimeError('invalid chosen cube high-blocks')
    used=set().union(*(set(combinations(sorted(b),2)) for b in blocks))
    required={p for p in combinations(range(17),2) if p[0]<3 and p not in missing(2)}
    if used&missing(2) or not required<=used:raise RuntimeError('cube model high-pair coverage differs')
    common=[b for b in blocks if {0,1}<=b]
    if common!=[{0,1,15,16}]:raise RuntimeError('bad cube common high-pair block')
    left=[b for h in [0,1] for b in blocks if h in b and b not in common]
    right=[b for b in blocks if 2 in b]
    if len(left)!=4 or len(right)!=4 or sorted(len(a&b) for a in left for b in right)!=[0]*4+[1]*12:
        raise RuntimeError('bad cube incidence')
    expected.append(shape2);expected.sort(key=lambda d:(d['shape'],d['orbit']))
    if expected!=first['cases']:raise RuntimeError('independently rebuilt high-block cases differ')
    stars=[];total=0;worst=0
    for d in expected:
        full,nodes=cover_fixed(d['shape'],d['fixed']);total+=nodes;worst=max(worst,nodes)
        source=json.loads((ROOT/f'highstar_s{d["shape"]}_{d["orbit"]:03d}.jsonl').read_text())
        actual=sorted(sorted(d['fixed']+c) for c in source['covers'])
        if full!=actual:raise RuntimeError('entrywise first-star covers differ')
        if full:stars.append(dict(shape=d['shape'],stars=full))
    return dict(degree_dfs_nodes=[n0,n2,n3],raw_graphs=[len(graphs0),len(cube),len(graphs3)],
                row_groups=[len(maps0),len(cube_maps),len(maps3)],cases=len(expected),
                fixed_pair_cover_nodes=total,max_case_nodes=worst,stars=stars)


def independent_set_at_least(conflicts,required,node_cap=200000):
    nodes=0;started=time.monotonic()
    def visit(active,want):
        nonlocal nodes
        nodes+=1
        if nodes>node_cap or time.monotonic()-started>10:raise RuntimeError('INCOMPLETE binary conflict-search guard')
        if want==0:return True
        if len(active)<want:return False
        # Partition into actual incompatibility cliques; at most one per class.
        remaining=set(active);classes=0
        while remaining:
            classes+=1;pool=set(remaining)
            while pool:
                v=max(pool,key=lambda z:(len(conflicts[z]&pool),-z))
                remaining.remove(v);pool.remove(v);pool.intersection_update(conflicts[v])
        if classes<want:return False
        v=max(active,key=lambda z:(len(conflicts[z]&active),-z))
        return visit(active-{v}-conflicts[v],want-1) or visit(active-{v},want)
    result=visit(set(range(len(conflicts))),required)
    return result,nodes


def residual_check():
    data=json.loads((ROOT/'joint_orbits.json').read_text())
    first=json.loads((ROOT/'first_star_templates.json').read_text())
    joint=[json.loads(s) for s in (ROOT/'brute.jsonl').read_text().splitlines()]
    def encode(s):return sum(1<<z for z in s)
    def decode(w):return frozenset(z for z in range(18) if w>>z&1)
    def im(words,p):return tuple(sorted(encode(p[z] for z in decode(w)) for w in words))
    for f,group in enumerate(data['groups']):
        domain={tuple(p) for p in group}
        if tuple(range(18)) not in domain:raise RuntimeError('missing first-star group identity')
        for p in group:
            if sorted(p)!=list(range(18)) or p[:3]!=[0,1,2] or p[17]!=17 or im(first[f]['star'],p)!=tuple(first[f]['star']):
                raise RuntimeError('bad actual first-star permutation')
            for q in group:
                if tuple(p[q[z]] for z in range(18)) not in domain:raise RuntimeError('first-star group not closed')
    domains={(r['first'],r['second']):{tuple(s) for s in r['stars']} for r in joint}
    covered={k:set() for k in domains};certs=[]
    old_candidates=list(combinations(range(1,17),5))
    for i,record in enumerate(data['cases']):
        key=record['first'],record['second'];star=tuple(record['star'])
        orbit={im(star,p) for p in data['groups'][record['first']]}
        if len(orbit)!=record['orbit_size'] or not orbit<=domains[key] or covered[key]&orbit:raise RuntimeError('bad joint-star orbit')
        covered[key].update(orbit)
        fixed={decode(w|(1<<17)) for w in first[key[0]]['star']}|{decode(w) for w in star}
        if len(fixed)!=37 or any(len(a&b)>2 for a,b in combinations(fixed,2)):raise RuntimeError('bad joint star literal check')
        candidates=[frozenset(q) for q in old_candidates if all(len(frozenset(q)&b)<=2 for b in fixed)]
        original=json.loads((ROOT/'capacity_domain.json').read_text())['cases'][record['capacity_index']]
        if list(map(encode,candidates))!=original['candidates'] or sorted(map(encode,fixed))!=original['fixed']:
            raise RuntimeError('entrywise residual-domain mismatch')
        containing={};conflicts=[set() for _ in candidates]
        for v,w in enumerate(candidates):
            for t in combinations(sorted(w),3):containing.setdefault(t,[]).append(v)
        for vertices in containing.values():
            for a,b in combinations(vertices,2):conflicts[a].add(b);conflicts[b].add(a)
        if any((b in conflicts[a])!=(len(candidates[a]&candidates[b])>2) for a,b in combinations(range(len(candidates)),2)):
            raise RuntimeError('wrong triple-incidence conflict edge')
        exists,nodes=independent_set_at_least(conflicts,22)
        if exists:raise RuntimeError('found residual22: upper58 disproved')
        certs.append(dict(index=i,first=key[0],second=key[1],candidates=len(candidates),nodes=nodes,
                          candidates_sha256=hashlib.sha256(json.dumps(list(map(encode,candidates)),separators=(',',':')).encode()).hexdigest()))
    if covered!=domains:raise RuntimeError('joint-star orbit cover incomplete')
    return dict(joint_orbits=len(certs),raw_joint_stars=sum(map(len,domains.values())),no_residual22=True,
                nodes=sum(c['nodes'] for c in certs),max_case_nodes=max(c['nodes'] for c in certs),cases=certs)


def witness_check():
    raw=json.loads((SOURCE/'witness58.json').read_text())
    words=raw['word_masks']
    blocks=[frozenset(z for z in range(18) if w>>z&1) for w in words]
    if len(blocks)!=58 or len(set(blocks))!=58 or any(len(b)!=5 or w<0 or w>=1<<18 for b,w in zip(blocks,words)) or any(
            len(a&b)>2 for a,b in combinations(blocks,2)):
        raise RuntimeError('invalid positive58-word witness')
    for x,y in [(17,0),(0,17)]:
        if sum(x in b for b in blocks)!=20 or sum({x,y}<=b for b in blocks)!=3:raise RuntimeError('witness pair condition differs')
        deficits=sorted([5-sum({x,z}<=b for b in blocks) for z in range(18) if z!=x],reverse=True)
        if [t for t in deficits if t]!=[2,2,1]:raise RuntimeError('witness deficit row differs')
    baseline=[frozenset(z for z in range(18) if int(row,2)>>z&1) for row in (SOURCE/'acl69.txt').read_text().splitlines()]
    if len(baseline)!=69 or len(set(baseline))!=69 or any(len(b)!=5 for b in baseline) or any(
            len(a&b)>2 for a,b in combinations(baseline,2)):raise RuntimeError('historical69 baseline invalid')
    return dict(attainment58=True,historical69_valid=True)


def main():
    global ROOT
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work-dir',type=Path,required=True)
    parser.add_argument('--check',type=Path,default=SOURCE/'expected.json');args=parser.parse_args()
    ROOT=args.work_dir.resolve();started=time.monotonic()
    manifest=json.loads(args.check.read_text());source_summary=json.loads((ROOT/'summary.json').read_text())
    if manifest!=source_summary:raise RuntimeError('production summary differs from compact manifest')
    result=dict(agent='six-code-3',role='researcher',first=first_star_check())
    templates=json.loads((ROOT/'first_star_templates.json').read_text())
    if len(templates)!=3 or len(result['first']['stars'])!=3:raise RuntimeError('incomplete template catalogue')
    for d,t in zip(result['first']['stars'],templates):
        if d['shape']!=t['shape'] or d['stars']!=[t['star'],t['second_star']]:raise RuntimeError('template entries differ')
        a,b=t['transposition'];p=list(range(17));p[a],p[b]=p[b],p[a]
        swapped=sorted(sum(1<<p[z] for z in range(17) if w>>z&1) for w in t['star'])
        if swapped!=t['second_star']:raise RuntimeError('template transposition is invalid')
    (ROOT/'scan.input').write_text('3\n'+'\n'.join(' '.join(map(str,t['star'])) for t in templates)+'\n')
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic',str(SOURCE/'scan.cpp'),'-o',str(ROOT/'scan')],check=True)
    completed=subprocess.run([str(ROOT/'scan'),str(ROOT/'scan.input'),str(ROOT/'brute.jsonl')],text=True,capture_output=True,timeout=60)
    (ROOT/'scan.log').write_text(completed.stdout+completed.stderr)
    if completed.returncode:raise RuntimeError('complete scan failed/incomplete: '+completed.stderr)
    primary=[json.loads(s) for s in (ROOT/'couple.jsonl').read_text().splitlines()]
    secondary=[json.loads(s) for s in (ROOT/'brute.jsonl').read_text().splitlines()]
    if len(primary)!=9 or len(secondary)!=9:raise RuntimeError('missing template pair')
    for a,b in zip(primary,secondary):
        for key in ['first','second','anchors','maps','stars']:
            if a[key]!=b[key]:raise RuntimeError('entrywise full transport mismatch at '+key)
    result['full_transport_maps']=sum(d['scanned'] for d in secondary)
    result['residual']=residual_check();result['fixtures']=witness_check()
    result.update(status='COMPLETE',seconds=round(time.monotonic()-started,6),max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  child_rss_kib_upper=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (ROOT/'independent_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='COMPLETE',first_cases=result['first']['cases'],fixed_pair_cover_nodes=result['first']['fixed_pair_cover_nodes'],
                         full_transport_maps=result['full_transport_maps'],joint_orbits=result['residual']['joint_orbits'],
                         no_residual22=True,attainment58=True,residual_nodes=result['residual']['nodes'],
                         seconds=result['seconds'],max_rss_kib=result['max_rss_kib'])))


if __name__=='__main__':main()
