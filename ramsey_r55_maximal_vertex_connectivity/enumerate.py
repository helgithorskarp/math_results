#!/usr/bin/env python3
"""Exact marked-component enumeration. No graph catalog or numerical solver."""
from itertools import combinations,permutations
from collections import Counter
import argparse,hashlib,json
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)

def masks(n,k):
    return [sum(1<<v for v in q) for q in combinations(range(n),k)]

def independent(a,m):
    return all(not(a[v]&m) for v in range(len(a)) if m>>v&1)

def encode(a):
    return sum((a[u]>>v&1)<<i for i,(u,v) in enumerate(combinations(range(len(a)),2)))

def decode(n,code):
    a=[0]*n
    for i,(u,v) in enumerate(combinations(range(n),2)):
        if code>>i&1:a[u]|=1<<v;a[v]|=1<<u
    return a

def core_classes():
    frontier=[[]];counts=[];cores={}
    for n in range(8):
        nxt=[]
        for a in frontier:
            triples=[m for m in masks(n,3) if independent(a,m)]
            for m in range(1<<n):
                if independent(a,m) and all(m&t for t in triples):
                    nxt.append([a[v]|((1<<n) if m>>v&1 else 0) for v in range(n)]+[m])
        frontier=nxt;counts.append(len(frontier))
        if n+1<6:continue
        unseen={encode(a) for a in frontier}
        need(len(unseen)==len(frontier),'duplicate labeled core')
        rows=[]
        while unseen:
            code=min(unseen);a=decode(n+1,code)
            orbit={sum((a[p[u]]>>p[v]&1)<<i for i,(u,v) in enumerate(combinations(range(n+1),2))) for p in permutations(range(n+1))}
            need(orbit<=unseen,'overlapping/incomplete vertex-permutation orbit')
            unseen-=orbit
            rows.append({'code':code,'orbit_size':len(orbit)})
        cores[n+1]=rows
    return counts,cores

def marked_graphs(n,h,code):
    a=decode(h,code);q=n-h;full=(1<<h)-1
    need((n,h) in ((10,6),(10,7),(10,8),(11,7),(11,8)),'unsupported marked order')
    stars=[m for m in range(1<<h) if independent(a,m)]
    triples=[m for m in masks(h,3) if independent(a,m)]
    pairs=[m for m in masks(h,2) if independent(a,m)]
    compatible={x:{y for y in stars if all((x|y)&t for t in triples)} for x in stars}
    result=[]
    def extend(prefix,candidates):
        if len(prefix)==q:
            b=a[:]+prefix[:]
            for v in range(h):
                for j,s in enumerate(prefix):
                    if s>>v&1:b[v]|=1<<(h+j)
            result.append(encode(b));return
        for x in candidates:
            if any(not((x|y|z)&t) for y,z in combinations(prefix,2) for t in pairs):continue
            if len(prefix)==3 and (x|prefix[0]|prefix[1]|prefix[2])!=full:continue
            extend(prefix+[x],[y for y in candidates if y in compatible[x]])
    extend([],stars)
    need(len(result)==len(set(result)),'duplicate ordered marked extension')
    return sorted(result)

def witness(n,code):
    f=decode(n,code);full=(1<<n)-1
    red=[full^(1<<v)^f[v] for v in range(n)]
    triangles=[t for t in masks(n,3) if independent(f,t)]
    common={}
    for t in triangles:
        vs=[v for v in range(n) if t>>v&1]
        common[t]=(red[vs[0]]&red[vs[1]]&red[vs[2]]).bit_count()
    beta,t=min((1+sum(red[v].bit_count() for v in range(n) if tri>>v&1)-common[tri],tri) for tri in triangles)
    need(beta<=19 if n==10 else beta<=20,'marked triangle inequality failed')
    cover=[]
    if n==11 and beta>=19:
        fours=[t for t in masks(n,4) if independent(f,t)]
        special=[full^t for size in (3,4) for t in masks(n,size) if independent(f,t) and all(t&u for u in fours)]
        need(special,'mark must be special')
        for tri in triangles:
            if all(s&tri==tri for s in special):cover=[tri];break
        if not cover:
            for tri,u in combinations(triangles,2):
                if 8-common[tri]-common[u]<=6 and all(s&tri==tri or s&u==u for s in special):cover=[tri,u];break
        need(cover and sum(4-common[x] for x in cover)<=6,'no six-capacity triangle cover')
    return {'beta':beta,'triangle':t,'cover':cover}

def generate(directory):
    directory=Path(directory);directory.mkdir()
    counts,cores=core_classes();rows=[];jobs=[]
    with (directory/'witnesses.jsonl').open('w') as stream:
        for n in (10,11):
            for h in range(n-4,9):
                for c in cores[h]:
                    code=c['code'];jobs.append((n,h,code));hist=Counter();covers=0;digest=hashlib.sha256()
                    words=marked_graphs(n,h,code)
                    for word in words:
                        w=witness(n,word);record={'n':n,'h':h,'core':code,'code':word,**w}
                        line=json.dumps(record,sort_keys=True,separators=(',',':'))+'\n'
                        stream.write(line);digest.update(line.encode());hist[w['beta']]+=1;covers+=bool(w['cover'])
                    rows.append({'n':n,'h':h,'core':code,'marked_graphs':len(words),'beta_histogram':dict(sorted(hist.items())),'cover_certificates':covers,'witness_stream_sha256':digest.hexdigest()})
    summary={'status':'GENERATED_COMPLETE_MARKED_COMPONENT_CERTIFICATES','labeled_core_counts_n1_to_n8':counts,'core_orbits':cores,'rows':rows,'marked10':sum(r['marked_graphs'] for r in rows if r['n']==10),'marked11':sum(r['marked_graphs'] for r in rows if r['n']==11),'covers':sum(r['cover_certificates'] for r in rows),'catalog_completeness_required':False,'target_found':False}
    (directory/'SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    (directory/'jobs.txt').write_text(''.join(f'{n} {h} {code}\n' for n,h,code in jobs))
    print(json.dumps({k:summary[k] for k in ('status','marked10','marked11','covers')},sort_keys=True))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();generate(a.directory)
