"""Resumable bounded certificate discovery. Open records never prove anything."""
import argparse
from collections import Counter
import json
from pathlib import Path
from time import monotonic
from weights import solve,divisors,populations,fractional_pairs
from normalization import normalize

ap=argparse.ArgumentParser();ap.add_argument('--prefix',default='8:0,9:0,10:1,14:1,12:3,16:0')
ap.add_argument('--seconds',type=float,default=180);ap.add_argument('--nodes',type=int,default=500)
ap.add_argument('--out',default='generated/tree.json');args=ap.parse_args()
L=10080;D=[m for m in divisors(L) if m>=8];start=monotonic();nodes=[];vectors=[];cuts=Counter();calls=0
A=tuple(tuple(map(int,s.split(':'))) for s in args.prefix.split(','))
saved=Path(args.out)
saved.parent.mkdir(parents=True,exist_ok=True)
if saved.exists():
    old=json.loads(saved.read_text())
    if tuple(tuple(v) for v in old['root_anchors'])!=A:raise ValueError('Resume root mismatch')
    nodes=old['nodes'];vectors=old['vectors'];cuts=Counter(old['cuts']);calls=old['lp_calls']
initial_nodes=len(nodes)

def visit(A,existing=None):
    global calls
    if existing is None:i=len(nodes);nodes.append({'anchors':A,'status':'open'})
    else:i=existing
    oldnode=nodes[i]
    if oldnode.get('type') in ('uniform','weighted') or oldnode.get('type')=='branch' and oldnode.get('complete'):
        return i,True
    if monotonic()-start>args.seconds or len(nodes)-initial_nodes>args.nodes:return i,False
    U=[int(all(x%m!=a for m,a in A)) for x in range(L)]
    if not any(U):nodes[i]['status']='cover';return i,False
    B=[m for m in D if m not in dict(A)]
    if oldnode.get('type')!='branch':
        demand=sum(U);cap=sum(max(populations(U,m)) for m in B)
        if demand>cap:
            nodes[i]={'type':'uniform','demand':demand,'capacity':cap};cuts['uniform']+=1;return i,True
        info,out=solve(L,A);calls+=1
        if out and info['gap2']>0:
            v=len(vectors);vectors.append(out[1]);nodes[i]={'type':'weighted','vector':v};cuts['single']+=1;return i,True
        if out and info['objective'] is not None and info['objective']<1.04:
            W,_=out
            pairs=fractional_pairs(W,B,k=12)
            if pairs:
                info,out=solve(L,A,pair_weights=pairs);calls+=1
                if out and info['gap2']>0:
                    v=len(vectors);vectors.append(out[1]);nodes[i]={'type':'weighted','vector':v};cuts['fractional' if any(c==1 for e,c in pairs) else 'paired']+=1;return i,True
    if monotonic()-start>args.seconds:return i,False
    candidates=[]
    for m in ([oldnode['modulus']] if oldnode.get('type')=='branch' else B[:7]):
        gains=populations(U,m);seen=set();reps=[]
        for a in range(m):
            if not gains[a]:continue
            k=normalize(A+((m,a),))
            if k not in seen:seen.add(k);reps.append(a)
        candidates.append((len(reps),m,reps))
    _,m,reps=min(candidates)
    children=[];complete=True;existing_children=dict(oldnode.get('children',[]))
    for a in reps:
        j,ok=visit(A+((m,a),),existing_children.get(a));children.append([a,j]);complete=complete and ok
        if monotonic()-start>args.seconds or len(nodes)-initial_nodes>args.nodes:
            children.extend([c for c in oldnode.get('children',[]) if c[0] not in dict(children)])
            complete=False;break
    nodes[i]={'type':'branch','modulus':m,'children':children,'complete':complete}
    if i%10==0:print(json.dumps({'node':i,'seconds':monotonic()-start,'nodes':len(nodes),'cuts':dict(cuts),'complete':complete}),flush=True)
    return i,complete

root,complete=visit(A,0 if nodes else None)
payload={'L':L,'minimum':8,'root_anchors':A,'nodes':nodes,'vectors':vectors,'complete':complete,'seconds':monotonic()-start,'lp_calls':calls,'cuts':dict(cuts)}
Path(args.out).write_text(json.dumps(payload,separators=(',',':'))+'\n')
print(json.dumps({k:v for k,v in payload.items() if k not in ('nodes','vectors')}),flush=True)

if not complete:raise SystemExit(2)
