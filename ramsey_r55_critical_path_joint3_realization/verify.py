"""Literal audit of the joint-core graph, independent of CNF and solver code."""
import argparse
from collections import Counter
import hashlib
import itertools as it
import json
from pathlib import Path


def need(ok,msg):
    if not ok:raise ValueError(msg)


def audit(path,detailed=False):
    doc=json.loads(path.read_text())
    need(set(doc)=={'n','red_edges'} and type(doc['n']) is int and doc['n']==43,'schema')
    raw=doc['red_edges'];need(type(raw) is list,'edge list')
    need(all(type(e) is list and len(e)==2 and all(type(v) is int for v in e) and 0<=e[0]<e[1]<43 for e in raw),'edges')
    red={tuple(e) for e in raw};need(len(red)==len(raw) and raw==sorted(raw),'ordered unique edges')
    g=[set() for _ in range(43)]
    for u,v in red:g[u].add(v);g[v].add(u)
    deg=list(map(len,g));need(deg==[20]*3+[21]*40,'degrees')
    expected={(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),
              (3,4),(3,5),(3,6),(3,7),(4,5),(4,6),(4,8),(5,7),(5,8),(5,9),
              (6,7),(6,8),(6,10),(7,9),(7,10),(8,9),(8,10),(9,10)}
    need({e for e in red if e[1]<11}==expected,'literal K11')
    expected_signatures=[2]*9+[3]*4+[4]*9+[5]*4+[6]*4+[7]*2
    signatures=[sum(1<<u for u in range(3) if u in g[v]) for v in range(11,43)]
    need(signatures==expected_signatures,'outside root-signature labeling')
    types=[sum(1<<u for u in range(11) if u in g[v]) for v in range(11,43)]
    for sig in range(2,8):
        block=[t for t,s in zip(types,signatures) if s==sig]
        need(block==sorted(block),'W footprint order in cells')
    def mono(vs,c):return all((e in red)==c for e in it.combinations(vs,2))
    hist={'red':[0]*6,'blue':[0]*6};first={};checked=0;masks={'red':[],'blue':[]}
    for five in it.combinations(range(43),5):
        checked+=1
        for c,name in ((True,'red'),(False,'blue')):
            if mono(five,c):
                k=sum(v>=11 for v in five);hist[name][k]+=1;first.setdefault(f'{name}:{k}',five)
                masks[name].append(sum(1<<v for v in five))
    need(all(hist[c][k]==0 for c in hist for k in range(4)),'joint <=3-outside K5 layer')
    profiles=[];hard_bad=[]
    for u in range(43):
        R=sorted(g[u]);B=sorted(set(range(43))-{u}-g[u])
        tr=sum(e in red for e in it.combinations(R,2));tb=sum(e not in red for e in it.combinations(B,2))
        profiles.append([deg[u],tr,tb])
        if tr>(93 if u<3 else 100) or tb>(107 if u<3 else 100):hard_bad.append(u)
    need(not set(range(3))&set(hard_bad),'all three hard root caps')
    U=[[1]*6 for _ in range(6)]
    for a in range(2,6):
        for b in range(2,6):
            x,y=U[a-1][b],U[a][b-1];U[a][b]=x+y-int(x%2==y%2==0)
    cliques={c:[s for k in range(4) for s in it.combinations(range(11),k) if mono(s,c)] for c in (True,False)}
    rows=0;failures=[];root_data=[]
    for A in cliques[True]:
        for B in cliques[False]:
            if not(A or B) or set(A)&set(B):continue
            common=[v for v in range(43) if v not in A+B and all(a in g[v] for a in A) and all(b not in g[v] for b in B)]
            cap=U[5-len(A)][5-len(B)]-1;rows+=1
            root_data.append([sum(1<<v for v in A),sum(1<<v for v in B),sum(1<<v for v in common),cap])
            if len(common)>cap:failures.append({'A':A,'B':B,'common':common,'upper':cap})
    cells=Counter(sum(1<<u for u in range(3) if u in g[v]) for v in range(3,43))
    need(not failures,'all root-union counts')
    details={'k5_masks':{c:sorted(v) for c,v in masks.items()},'root_rows':sorted(root_data)}
    result={'status':'VERIFIED_JOINT_THREE_OUTSIDE_REALIZATION_NOT_RAMSEY','n':43,'red_edges':len(red),
            'degrees':deg,'cells':dict(sorted(cells.items())),'types':types,
            'repeated_types':{str(t):c for t,c in sorted(Counter(types).items()) if c>1},
            'k5_by_outside_count':hist,'first_obstructions':first,'five_sets_checked':checked,
            'profiles':profiles,'hard_cap_failures':hard_bad,'root_union_rows_checked':rows,
            'root_union_failures':failures,'graph_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'clique_set_sha256':hashlib.sha256(json.dumps(details['k5_masks'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'root_rows_sha256':hashlib.sha256(json.dumps(details['root_rows'],separators=(',',':')).encode()).hexdigest()}
    return (result,details) if detailed else result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--graph',type=Path,default=Path(__file__).with_name('GRAPH.json'));p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();need(not a.report.exists(),'fresh report');r=audit(a.graph)
    a.report.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('profiles','degrees','types','root_union_failures')}))
    print('root_union_failures',len(r['root_union_failures']))
