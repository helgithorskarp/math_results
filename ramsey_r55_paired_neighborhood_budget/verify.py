#!/usr/bin/env python3
"""Exact audit of the paired-neighborhood budget and seven residual patterns.

Standard library only. Reuses pinned upstream core and union checkers, not
their numerical generators. Integer edge witnesses establish only the
precisely stated aggregate relaxation, not actual graphs.
"""
import argparse
from collections import Counter
import csv
from hashlib import sha256
import importlib.util
from itertools import combinations, combinations_with_replacement, permutations
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
DS=(19,19,20,20,20);M=217;PROFILE='0,2,3,38,0,0,0';MASK=443
PINS={
 'ramsey_r55_signature_union_cuts/verify_certificate.py':'fde3e7c93450f93692da542ddcbfa5bb6bee397b1fa0e8176c9f18948e723135',
 'ramsey_r55_signature_union_cuts/CERTIFICATE.tsv':'94448b3282ad4d5966303a01624f0cfddb78d966751830ffb8160598300f0bd3',
 'ramsey_r55_coupled_signature_counts/verify_certificate.py':'585ef332f3e07c7eae1a349a942ea2cce07c68f2d594f36c937864f517e91d76',
 'ramsey_r55_coupled_signature_counts/CERTIFICATE.tsv':'3903b439068cd87a37fc716541a365894fd2498afdbaee8bcfa7edc3ac0916e9',
}

def require(ok,message):
    if not ok:raise ValueError(message)

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def graph(n,edges):
    adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    return adj

def adjacency(mask,n):
    return graph(n,[e for j,e in enumerate(combinations(range(n),2)) if mask>>j&1])

def edge_count(adj,X,Y=None):
    if Y is None:return sum(b in adj[a] for a,b in combinations(X,2))
    require(not X&Y,'cross-set disjointness')
    return sum(b in adj[a] for a in X for b in Y)

def clique(adj,X,k,red=True):
    return any(all((b in adj[a])==red for a,b in combinations(S,2)) for S in combinations(X,k))

def inputs():
    for path,digest in PINS.items():require(sha256((HERE.parent/path).read_bytes()).hexdigest()==digest,path)
    old=load('paired_old_core',HERE.parent/'ramsey_r55_coupled_signature_counts/verify_certificate.py')
    union=load('paired_old_union',HERE.parent/'ramsey_r55_signature_union_cuts/verify_certificate.py')
    union.check_ramsey_table()
    return old,union

def replay_core(old,union):
    hist,universe=old.universe(DS,M)
    require(len(universe)==43,'target marginal core universe')
    with (HERE.parent/'ramsey_r55_coupled_signature_counts/CERTIFICATE.tsv').open() as stream:
        coupled=[r for r in csv.DictReader(stream,delimiter='\t') if r['counts_18_to_24']==PROFILE]
    coupled_seen=set();coupled_positive=set()
    for r in coupled:
        mask=int(r['red_mask']);orbit=old.orbit_with_maps(mask,DS);payload=old.read_payload(r,5)
        require(len(orbit)==int(r['orbit_size']) and min(orbit)==mask and not coupled_seen&orbit.keys(),'coupled core coverage')
        coupled_seen.update(orbit)
        for image,p in orbit.items():
            caps,b,near=universe[image]
            if r['kind']=='primal':
                old.check_primal({old.permute_signature(x,p):v for x,v in payload.items()},caps,b)
            else:
                moved=[payload[0]]+[0]*5
                for i in range(5):moved[p[i]+1]=payload[i+1]
                old.check_dual(moved,caps,b)
        if r['kind']=='primal':coupled_positive.update(orbit)
    require(coupled_seen==set(universe) and len(coupled_positive)==37,'complete coupled target replay')
    with (HERE.parent/'ramsey_r55_signature_union_cuts/CERTIFICATE.tsv').open() as stream:
        records=[r for r in csv.DictReader(stream,delimiter='\t') if r['counts_18_to_24']==PROFILE]
    require(len(records)==5,'five inherited core orbits')
    seen=set();surviving=set()
    for r in records:
        mask=int(r['red_mask']);kind=r['kind'];payload=json.loads(r['payload'])
        orbit=old.orbit_with_maps(mask,DS)
        require(min(orbit)==mask and len(orbit)==int(r['orbit_size']),'core relabeling count')
        require(not seen&orbit.keys(),'disjoint core orbits');seen.update(orbit)
        for image,p in orbit.items():
            caps,b,near=universe[image]
            union.verify(kind,union.move(kind,payload,p),caps,b,near)
        if kind=='primal':surviving.update(orbit)
        else:require(kind=='dual','only exact dual exclusions')
    require(seen==coupled_positive,'all 37 coupled-positive cores covered')
    require(surviving==set(old.orbit_with_maps(MASK,DS)) and len(surviving)==6,'sole residual core')
    return universe[MASK]

def old_vectors(caps,b,near,union):
    weight=lambda x:2*(x&3).bit_count()+(x>>2).bit_count()
    require(sum((21-d)*r for d,r in zip(DS,b[1:]))-3*b[0]==2,'two-unit weighted slack')
    light={5,6,9,10,17,18,28}
    require({x for x in caps if weight(x)==3}==light,'complete weight-three alphabet')
    fours=[x for x in caps if weight(x)==4];fives=[x for x in caps if weight(x)==5]
    choices=[(x,) for x in fives]+list(combinations_with_replacement(fours,2))
    answer=set()
    for heavy in choices:
        y=Counter(heavy)
        r=[t-sum(v for x,v in y.items() if x>>i&1) for i,t in enumerate(b[1:])]
        w=b[0]-len(heavy)-r[0]-r[1]
        if w<0:continue
        y[28]=w;totals=[r[i]-w for i in (2,3,4)]
        if min(totals)<0:continue
        for a in range(totals[0]+1):
            for bb in range(totals[1]+1):
                cc=r[0]-a-bb
                if not 0<=cc<=totals[2]:continue
                for i,v,t in zip((2,3,4),(a,bb,cc),totals):y[1|1<<i]=v;y[2|1<<i]=t-v
                payload={'values':[[x,v] for x,v in sorted(y.items()) if v]}
                try:union.check_primal(payload,caps,b,near)
                except ValueError:continue
                answer.add(tuple(y[x] for x in range(32)))
    return sorted(answer)

def statistics(y):
    c=sum(v for x,v in enumerate(y) if x&3==3)
    D=sum(v for x,v in enumerate(y) if x&1 and not x&2 and x&16)
    D+=sum(v for x,v in enumerate(y) if x&2 and not x&1 and x&8)
    u=sum((x>>2).bit_count()*v for x,v in enumerate(y) if x&3==3)
    T=sum(v*(int(bool(x&1))*((x>>1&1)+(x>>2&1)+(x>>4&1))
             +int(bool(x&2))*((x&1)+(x>>2&1)+(x>>3&1))) for x,v in enumerate(y))
    require(y[28]==6+c and T==10+c+D+u,'symbolic pair identities')
    require(D<=24-2*c and c<=2,'incidence and slack bounds')
    return c,D,20+24*c+D

def normal_form(a,b):
    y=[0]*32
    for x,v in [(3,2),(5,a),(6,8-a),(9,b),(10,10-b),(17,14-a-b),(18,a+b-4),(28,8)]:y[x]=v
    return tuple(y)

def edge_rows(y,near,union):
    """Rows lo <= row * edge_counts <= hi, from literal cell/root sets."""
    cells=[x for x,v in enumerate(y) if v];pairs=list(combinations_with_replacement(cells,2))
    caps=[y[a]*y[b] if a!=b else y[a]*(y[a]-1)//2 for a,b in pairs]
    rows=[]
    def add(name,row,lo,hi):rows.append((name,row,lo,hi))
    for x in cells:
        row=[int(a==x)+int(b==x) for a,b in pairs];target=(21-x.bit_count())*y[x]
        add(('degree',x),row,target,target)
    maximum={19:92,20:100,22:114,23:122}
    for i,d in enumerate(DS):
        fixed=edge_count(near,near[i])+sum(len(near[i]&{j for j in range(5) if x>>j&1})*v
                                        for x,v in enumerate(y) if x>>i&1)
        total=(42-d)*(41-d)//2-448+sum(DS[j] for j in near[i])+21*(d-len(near[i]))
        row=[int(bool(a&b&(1<<i))) for a,b in pairs]
        add(('local',i),row,total-(maximum[42-d]-7)-fixed,maximum[d]-7-fixed)
    for A,B,cap in union.all_roots(near):
        aset={i for i in range(5) if A>>i&1};bset={i for i in range(5) if B>>i&1}
        F={i for i in range(5) if i not in aset|bset and aset<=near[i] and not bset&near[i]}
        selected={x for x in cells if x&A==A and not x&B}
        n=len(F)+sum(y[x] for x in selected)
        if not selected:continue
        p,q=5-len(aset),5-len(bset);require(min(p,q)>=2,'nonempty root type')
        lower=max(0,n-union.RAMSEY[p-1][q-2]);upper=union.RAMSEY[p-2][q-1]-1
        for x in selected:
            fixed=sum(x>>i&1 for i in F)*y[x]
            row=[int(a==x and b in selected)+int(b==x and a in selected) for a,b in pairs]
            add(('root',A,B,x),row,lower*y[x]-fixed,upper*y[x]-fixed)
    return pairs,caps,rows

def check_edge_witness(y,e,near,union):
    pairs,caps,rows=edge_rows(y,near,union)
    require(type(e) is list and len(e)==len(pairs),'edge count dimension')
    require(all(type(v) is int and 0<=v<=c for v,c in zip(e,caps)),'integer edge boxes')
    for name,row,lo,hi in rows:require(lo<=sum(v*a for v,a in zip(e,row))<=hi,('edge constraint',name))
    return len(rows)

def deficiency_audit(near):
    totals=[(42-d)*(41-d)//2-448+sum(DS[j] for j in near[i])+21*(d-len(near[i]))
            for i,d in enumerate(DS)]
    require(totals==[200,200,197,200,200],'exceptional local sums')
    require(210-448+441==203,'central local constant')
    choices=[(t,k,(4156+t-k)//3,(8595-4156-t+k)//3)
             for t in range(90,94) for k in range(3) if (4156+t-k)%3==0]
    require(choices==[(90,1,1415,1450),(91,2,1415,1450),(92,0,1416,1449),(93,1,1416,1449)],
            'four triangle-count allocations')
    require(36*200+2*199+sum(totals)==8595,'all local sums')
    require((1247-2*12-3*3)//2-86*7==5,'global excess deficiency')
    return choices

def pair_audit(adj,z,w,C,Fz,Fw):
    J=adj[z]&C;K=adj[w]&C;P=J-K;Q=K-J;U=J&K
    require(not ({z,w}&C) and not ((Fz|Fw)&C),'root/central disjointness')
    require(Fz<=adj[z]-adj[w]-{w} and Fw<=adj[w]-adj[z]-{z},'external opposite roots')
    lhs=2*(edge_count(adj,J)+edge_count(adj,K))
    correction=edge_count(adj,P,Fz)+edge_count(adj,Q,Fw)
    budget=sum(len(adj[v]&C) for v in U)
    rhs=8*(len(P)+len(Q))-correction+2*budget
    # Independently count every term in the exact decomposition.
    require(edge_count(adj,J)+edge_count(adj,K)==edge_count(adj,P)+edge_count(adj,Q)
            +edge_count(adj,U,P|Q)+2*edge_count(adj,U),'edge decomposition')
    require(lhs<=rhs,'paired bound on literal Ramsey graph')
    require(all(len(adj[v]&(P|Fz))<=8 for v in P) and all(len(adj[v]&(Q|Fw))<=8 for v in Q),'rooted degree eight')
    return lhs,rhs,len(U)

def literal_audit():
    checked=0;overlap=0
    for mask in range(1024):
        adj=adjacency(mask,5)
        if clique(adj,range(5),5) or clique(adj,range(5),5,False):continue
        for z,w in permutations(range(5),2):
            rest=sorted(set(range(5))-{z,w})
            for bits in range(8):
                C={v for j,v in enumerate(rest) if bits>>j&1};outside=set(rest)-C
                Fz=(adj[z]-adj[w])&outside;Fw=(adj[w]-adj[z])&outside
                _,_,s=pair_audit(adj,z,w,C,Fz,Fw);checked+=1;overlap+=int(s>0)
    residues={x*x%17 for x in range(1,17)}
    adj=graph(19,[(a,b) for a,b in combinations(range(17),2) if (b-a)%17 in residues]
              +[(17,v) for v in range(17)]+[(17,18)])
    require(not clique(adj,range(19),5) and not clique(adj,range(19),5,False),'19-vertex Ramsey fixture')
    require(pair_audit(adj,17,18,set(range(17)),set(),set())==(136,136,0),'sharp disjoint case')
    large=0
    for z,w in permutations(range(19),2):
        rest=set(range(19))-{z,w}
        for omitted in sorted(rest):
            C=rest-{omitted};outside={omitted}
            pair_audit(adj,z,w,C,(adj[z]-adj[w])&outside,(adj[w]-adj[z])&outside);large+=1
    bad=graph(12,list(combinations(range(11),2))+[(10,11)])
    try:pair_audit(bad,10,11,set(range(10)),set(),set())
    except ValueError as e:require(e.args[0]=='paired bound on literal Ramsey graph','negative fixture failed for wrong reason')
    else:raise ValueError('Ramsey hypothesis omitted')
    return checked,overlap,large

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay-parent',action='store_true')
    parser.add_argument('--emit-summary',action='store_true')
    parser.add_argument('--edge-witnesses',type=Path,default=HERE/'EDGE_WITNESSES.json')
    args=parser.parse_args();old,union=inputs();caps,b,near=replay_core(old,union)
    ys=old_vectors(caps,b,near,union);require(len(ys)==29,'29 prior count vectors')
    retained=[y for y in ys if statistics(y)[2]>=76]
    target=[normal_form(a,bb) for a in range(3,6) for bb in range(2,5) if 6<=a+bb<=8]
    require(set(retained)==set(target) and len(retained)==7,'complete seven-pattern reduction')
    require(all(y[3]==2 and y[28]==8 for y in retained),'forced common-neighbor cells')
    # Literal core relabelings: no automorphism assumption on a hypothetical G.
    perms=[p for p in permutations(range(5)) if all(DS[i]==DS[p[i]] for i in range(5))
           and all((j in near[i])==(p[j] in near[p[i]]) for i,j in combinations(range(5),2))]
    require(len(perms)==2,'core stabilizer order')
    def orbit(y):
        answers=set()
        for p in perms:
            moved=[0]*32
            for x,v in enumerate(y):moved[sum(1<<p[i] for i in range(5) if x>>i&1)]=v
            answers.add(tuple(moved))
        return answers
    orbit_sizes=[len(orbit(y)) for y in retained if min(orbit(y))==y]
    require(sorted(orbit_sizes)==[1,1,1,2,2],'five normal-form relabeling classes')
    records=json.loads(args.edge_witnesses.read_text())
    require([r['a'] for r in records]==[[y[5],y[9],y[17]] for y in retained],'ordered witness coverage')
    counts=[check_edge_witness(y,r['edge_counts'],near,union) for y,r in zip(retained,records)]
    deficiency_audit(near)
    bad=records[0]['edge_counts'].copy();bad[0]+=1
    try:check_edge_witness(retained[0],bad,near,union)
    except ValueError:pass
    else:raise ValueError('mutated edge witness accepted')
    if args.emit_summary:
        print('a2\ta3\ta4\tb2\tb3\tb4\tcommon\tlow_triple\tpaired_rhs\tedge_rows')
        for y,n in zip(retained,counts):print('\t'.join(map(str,[y[5],y[9],y[17],y[6],y[10],y[18],y[3],y[28],statistics(y)[2],n])))
        return
    checked,overlap,large=literal_audit()
    if args.replay_parent:
        result=subprocess.run([sys.executable,'-O',str(HERE.parent/'ramsey_r55_degree19_triangle_exclusion/verify.py'),'--replay-parent'],capture_output=True,text=True,check=True)
        require('67 global candidates, 273 anchored splits' in result.stdout,'unchanged cumulative totals')
    print('PASS all 1024 exceptional graphs replayed: 43 marginal, 37 coupled, six residual cores in one class')
    print('PASS complete old count census: 29 vectors; paired degree budget retains exactly seven')
    print('PASS common cell has two vertices; low-triple cell has eight; 36 central vertices are doubly exact')
    print('PASS excess deficiency supported on three vertices; four triangle-count allocations')
    print('PASS seven normal forms in five relabeling classes, sizes 1,1,1,2,2')
    print('PASS seven exact integer edge-count witnesses and altered-witness rejection')
    print(f'PASS literal paired inequality: {checked} small cases ({overlap} with overlap), {large} larger cases')
    print('PASS sharp 19-vertex fixture and negative no-Ramsey-hypothesis fixture')
    print('SCOPE aggregate structural normal form, not graph realizations; totals remain 67 globals and 273 splits')
    print('edge_witness_sha256='+sha256(args.edge_witnesses.read_bytes()).hexdigest())

if __name__=='__main__':main()
