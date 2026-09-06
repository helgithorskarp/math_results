"""Bit-intersection cross-check of an explicit joint-core graph; no producer import."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def need(ok,msg):
    if not ok:raise ValueError(msg)


def bits(mask):
    while mask:
        bit=mask & -mask;mask-=bit;yield bit.bit_length()-1


def cliques(rows,candidates,size,prefix=0):
    if size==0:
        yield prefix;return
    while candidates.bit_count()>=size:
        bit=candidates & -candidates;candidates-=bit;v=bit.bit_length()-1
        yield from cliques(rows,candidates & rows[v],size-1,prefix|bit)


def audit(path,detailed=False):
    doc=json.loads(path.read_text());need(set(doc)=={'n','red_edges'} and type(doc['n']) is int and doc['n']==43,'schema')
    raw=doc['red_edges'];need(type(raw) is list,'edge list');rows=[0]*43;previous=(-1,-1)
    for pair in raw:
        need(type(pair) is list and len(pair)==2 and all(type(x) is int for x in pair),'pair schema')
        u,v=pair;need(0<=u<v<43 and (u,v)>previous,'pair order/range');previous=(u,v)
        rows[u]|=1<<v;rows[v]|=1<<u
    full=(1<<43)-1;K=(1<<11)-1;O=full^K
    blue=[full^r^(1<<v) for v,r in enumerate(rows)]
    degree=[r.bit_count() for r in rows];need(degree==[20]*3+[21]*40,'degrees')
    # Independent literal core row representation, not the generator's W mask.
    core_rows=[2046,1,1,241,361,921,1433,1641,1649,1441,961]
    need([r&K for r in rows[:11]]==core_rows,'literal core bitrows')
    signatures=[rows[v]&7 for v in range(11,43)]
    need(signatures==[2]*9+[3]*4+[4]*9+[5]*4+[6]*4+[7]*2,'signatures')
    types=[r&K for r in rows[11:]]
    for sig in range(2,8):
        block=[t for t,s in zip(types,signatures) if s==sig];need(block==sorted(block),'contact ordering')
    hist={};first={};masks={}
    for name,adj in (('red',rows),('blue',blue)):
        hist[name]=[0]*6
        masks[name]=[]
        for mask in cliques(adj,full,5):
            k=(mask&O).bit_count();hist[name][k]+=1;first.setdefault(f'{name}:{k}',list(bits(mask)))
            masks[name].append(mask)
    need(all(hist[c][k]==0 for c in hist for k in range(4)),'joint three-outside layer')
    profiles=[];bad=[]
    for v in range(43):
        tr=sum((rows[u]&rows[v]).bit_count() for u in bits(rows[v]))//2
        tb=sum((blue[u]&blue[v]).bit_count() for u in bits(blue[v]))//2
        profiles.append([degree[v],tr,tb])
        if tr>(93 if v<3 else 100) or tb>(107 if v<3 else 100):bad.append(v)
    need(not any(v<3 for v in bad),'hard root density')
    U=[[1,1,1,1,1],[1,2,3,4,5],[1,3,6,9,14],[1,4,9,18,31],[1,5,14,31,62]]
    core_cliques={name:[(k,m) for k in range(4) for m in cliques(adj,K,k)]
                  for name,adj in (('red',rows),('blue',blue))}
    checks=0;failures=[];root_data=[]
    for a,A in core_cliques['red']:
        for b,B in core_cliques['blue']:
            if not(A|B) or A&B:continue
            common=full^(A|B)
            for v in bits(A):common &= rows[v]
            for v in bits(B):common &= blue[v]
            checks+=1
            root_data.append([A,B,common,U[4-a][4-b]-1])
            if common.bit_count()>U[4-a][4-b]-1:failures.append([A,B,common])
    need(not failures,'all root-union counts')
    details={'k5_masks':{c:sorted(v) for c,v in masks.items()},'root_rows':sorted(root_data)}
    result={'status':'VERIFIED','graph_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'n':43,'red_edges':sum(degree)//2,'degrees':degree,'types':types,
            'profiles':profiles,'hard_cap_failures':bad,'root_union_rows_checked':checks,
            'root_union_failures':failures,'k5_by_outside_count':hist,'first_obstructions':first,
            'clique_set_sha256':hashlib.sha256(json.dumps(details['k5_masks'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'root_rows_sha256':hashlib.sha256(json.dumps(details['root_rows'],separators=(',',':')).encode()).hexdigest()}
    return (result,details) if detailed else result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--graph',type=Path,default=Path(__file__).with_name('GRAPH.json'));p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();need(not a.report.exists(),'fresh report');r=audit(a.graph)
    a.report.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({k:r[k] for k in ('status','k5_by_outside_count','hard_cap_failures','root_union_rows_checked')}))
