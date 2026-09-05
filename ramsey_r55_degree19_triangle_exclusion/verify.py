#!/usr/bin/env python3
"""Exact audits for the degree-19 triangle-neighborhood exclusion.

No solver, numerical library, or graph catalog is used for the new theorem.
The optional parent replay checks the inherited cumulative candidate totals.
"""
import argparse
from collections import Counter
import csv
from functools import lru_cache
from hashlib import sha256
from itertools import combinations,permutations,product
import json
from math import comb
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
COUNTS='0,1,3,39,0,0,0'
DEGREES=(19,20,20,20)
PINS={
 'ramsey_r55_signature_union_cuts/SUMMARY.tsv':'286258e842b2272da7787e74be41db6ac5f5b26921777202deff699a81143ffa',
 'ramsey_r55_signature_union_cuts/CERTIFICATE.tsv':'94448b3282ad4d5966303a01624f0cfddb78d966751830ffb8160598300f0bd3',
 'ramsey_r55_signature_union_cuts/verify_certificate.py':'fde3e7c93450f93692da542ddcbfa5bb6bee397b1fa0e8176c9f18948e723135',
 'ramsey_r55_coupled_signature_counts/SUMMARY.tsv':'cce4476cf875ff5d086a2f4fe3a830ddd6ba74e119cb4f9e049f14bfd2f3c511',
 'ramsey_r55_exceptional_signature_capacity/CENSUS.tsv':'08a4a09b677031faf9dc7c7dc403e8e06e3245e39d13ca260b251a5c34ed5363',
 'ramsey_r55_exceptional_degree_sieve/PROFILES.tsv':'a8bd3a7def8d719947e74601f410255856a309e7f66af0ee16227370b9a4f3fa',
}

def require(test,detail):
    if not test: raise ValueError(detail)

def graph(n,edges):
    near=[set() for _ in range(n)]
    for a,b in edges: near[a].add(b);near[b].add(a)
    return near

def adjacency(mask,n):
    return graph(n,[e for bit,e in enumerate(combinations(range(n),2)) if mask>>bit&1])

def has_clique(near,vertices,size,red=True):
    return any(all((b in near[a])==red for a,b in combinations(q,2))
               for q in combinations(vertices,size))

@lru_cache(None)
def upper(p,q):
    if min(p,q)==1:return 1
    a,b=upper(p-1,q),upper(p,q-1)
    return a+b-int(a%2==b%2==0)

def vertices(mask,n):return {i for i in range(n) if mask>>i&1}

def root_rows(near):
    k=len(near)
    for word in product(range(3),repeat=k):
        A={i for i,v in enumerate(word) if v==1};B={i for i,v in enumerate(word) if v==2}
        if not A|B:continue
        if any(j not in near[i] for i,j in combinations(A,2)):continue
        if any(j in near[i] for i,j in combinations(B,2)):continue
        fixed=[v for v in range(k) if v not in A|B and all(i in near[v] for i in A)
               and all(i not in near[v] for i in B)]
        a=sum(1<<v for v in A);b=sum(1<<v for v in B)
        yield a,b,upper(5-len(A),5-len(B))-1-len(fixed)

def weighted_signatures():
    return [x for x in range(16) if 2*int(bool(x&1))+sum(x>>i&1 for i in (1,2,3))>=2]

def core_cases():
    require((19+3*20+39*21)//2==449,'global red edges')
    require(comb(23,2)-449+21*19==203,'degree-19 identity constant')
    require(comb(21,2)-449+21*21==202,'central identity constant')
    require(85+115==200 and 100+100==200,'explicit local caps')
    admissible=[]
    for mask in range(64):
        near=adjacency(mask,4)
        S=sum(DEGREES[j]-21 for j in near[0])
        if 203+S<=200:admissible.append(mask)
    require(admissible==[7,15,23,31,39,47,55,63],'all eight core possibilities')
    groups=Counter(sum(j in adjacency(mask,4)[i] for i,j in combinations((1,2,3),2)) for mask in admissible)
    require(groups=={0:1,1:3,2:3,3:1},'four complete core classes')
    signatures=weighted_signatures();require(len(signatures)==12,'all weighted signatures')
    # With independent low vertices, the singleton cell is a red clique of size <=3.
    require(all(2-x.bit_count()<=int(x==1) for x in signatures),'star cover inequality')
    require(2*39-(16+19+19+19)==5 and 5>3,'star contradiction')
    cases={15:([3,-1,-1,-1,-2],[(1,10),(1,12),(6,1)]),
           31:([2,-1,0,-1,-1],[(1,12),(6,1),(10,4)])}
    tables=[]
    for mask,(lam,roots) in cases.items():
        near=adjacency(mask,4);b=[39]+[d-len(s) for d,s in zip(DEGREES,near)]
        bounds={(a,bb):bound for a,bb,bound in root_rows(near)}
        require(all(bounds[root]==8 for root in roots),'root validity and bound eight')
        table=[]
        for x in signatures:
            left=lam[0]+sum(lam[i+1] for i in range(4) if x>>i&1)
            right=sum(x&a==a and not x&bb for a,bb in roots)
            require(left<=right,'pointwise core cover')
            table.append([x,left,right])
        lhs=sum(a*t for a,t in zip(lam,b));rhs=sum(bounds[root] for root in roots)
        require(lhs>rhs,'strict core contradiction')
        tables.append({'core_mask':mask,'lambda':lam,'roots':roots,'lhs':lhs,'rhs':rhs,'pointwise':table})
    return admissible,tables

def density_bound(n,s):
    require(0<=s<=n,'removed-set size')
    return 4*(n-s)+s*(n-s)+comb(s,2)

def triangle_case():
    # No cell enumeration is used: all H<=5 are covered by this argument.
    require(19-3==16,'central red neighbors')
    require(3*(20-3)==51 and 39-16==23,'low-to-central incidence total')
    Hmax=51-2*23;require(Hmax==5,'cross-incidence pigeonhole')
    bounds=[]
    for H in range(Hmax+1):
        low=85-3-H
        high=density_bound(16,H//3)
        require(low>high,'triangle-core edge-density contradiction')
        bounds.append([H,low,H//3,high])
    return bounds

def cell_vectors():
    near=adjacency(63,4);root=list(root_rows(near));result=[]
    # Brute force the bounded defect coordinates, not the proposed six answers.
    for e in product(range(3),repeat=3):
        E=sum(e)
        if E>2:continue
        for c in product(range(6),repeat=3):
            C=sum(c);d=5-C-2*E
            if not 0<=d<=3:continue
            y=[0]*16;y[1]=16-C-E;y[14]=d
            for i in range(1,4):
                y[1|1<<i]=c[i-1]
                y[15^(1<<i)]=e[i-1]
                y[14^(1<<i)]=6+c[i-1]+E-e[i-1]
            require(sum(y)==39 and all(sum(y[x] for x in range(16) if x>>i&1)==(16 if i==0 else 17)
                                      for i in range(4)),'parameterized exact margins')
            if any(sum(y[x] for x in range(16) if x&a==a and not x&b)>cap for a,b,cap in root):continue
            require(all(not value or x in weighted_signatures() and x!=15 for x,value in enumerate(y)),'admissible cells')
            # New common-neighborhood bounds imply the inherited per-cell boxes.
            require(all(value<=comb(7-x.bit_count(),4-x.bit_count())-1
                        for x,value in enumerate(y) if value),'inherited cell boxes')
            result.append(tuple(y))
    result=sorted(set(result));require(len(result)==6,'complete cell-vector count')
    def orbit(y):
        answers=set()
        for image in permutations((1,2,3)):
            p=(0,)+image;out=[0]*16
            for x,value in enumerate(y):out[sum(1<<p[i] for i in range(4) if x>>i&1)]=value
            answers.add(tuple(out))
        return answers
    reps=[y for y in result if min(orbit(y))==y]
    require(len(reps)==2 and all(len(orbit(y))==3 for y in reps),'cell relabeling orbits')
    return [{'orbit_size':3,'values':[[x,v] for x,v in enumerate(y) if v]} for y in reps]

def positive_and_negative_tests():
    # A literal Paley-17 fixture: no reliance on its name or a catalog.
    residues={a*a%17 for a in range(1,17)}
    near=graph(19,[(i,j) for i,j in combinations(range(17),2) if (j-i)%17 in residues]
               +[(17,j) for j in range(17)]+[(17,18)])
    require(all(len(near[i]&set(range(17)))==8 for i in range(17)),'eight-regular core fixture')
    require(not has_clique(near,range(19),5) and not has_clique(near,range(19),5,False),'literal 19-vertex positive fixture')
    require(sum(len(s&set(range(17))) for s in near[:17])//2==density_bound(17,0)==68,'sharp s=0 density test')
    checked=0
    for mask in range(1<<10):
        adj=adjacency(mask,5)
        if has_clique(adj,range(5),5) or has_clique(adj,range(5),5,False):continue
        for z,w in permutations(range(5),2):
            options=sorted(adj[z]-{w})
            for bits in range(1<<len(options)):
                J={v for i,v in enumerate(options) if bits>>i&1};Y=J&adj[w];W=J-Y
                require(not has_clique(adj,W,4) and not has_clique(adj,W,4,False),'rooted (4,4) property')
                edges=sum(b in adj[a] for a,b in combinations(J,2))
                require(edges<=density_bound(len(J),len(Y)),'deletion bound on literal graph')
                checked+=1
    # The no-K5 hypothesis cannot be dropped: root a red 10-clique this way.
    bad=graph(12,list(combinations(range(11),2))+[(10,11)])
    J=set(range(10));Y=J&bad[11]
    require(not Y and has_clique(bad,J,5),'negative fixture hypotheses')
    require(sum(b in bad[a] for a,b in combinations(J,2))>density_bound(10,0),'negative density fixture')
    return checked

def cumulative_totals():
    for name,digest in PINS.items():require(sha256((HERE.parent/name).read_bytes()).hexdigest()==digest,name)
    def read(name):
        with (HERE.parent/name).open() as stream:return list(csv.DictReader(stream,delimiter='\t'))
    globals_=read('ramsey_r55_exceptional_degree_sieve/PROFILES.tsv')
    marginal=read('ramsey_r55_exceptional_signature_capacity/CENSUS.tsv')
    coupled=read('ramsey_r55_coupled_signature_counts/SUMMARY.tsv')
    union=read('ramsey_r55_signature_union_cuts/SUMMARY.tsv')
    excluded={r['counts_18_to_24'] for r in marginal if not int(r['pass'])}
    excluded|={r['counts_18_to_24'] for r in coupled if not int(r['primal_cores'])}
    excluded|={r['counts_18_to_24'] for r in union if not int(r['primal_cores'])}
    old=[r for r in globals_ if r['status']=='feasible' and r['counts_18_to_24'] not in excluded]
    require(len(old)==68 and sum(int(r['split_count']) for r in old)==275,'inherited totals')
    removed=[r for r in old if r['counts_18_to_24']==COUNTS]
    require(len(removed)==1 and int(removed[0]['split_count'])==2,'new profile and two splits')
    new=[r for r in old if r not in removed]
    gc=Counter(int(r['M']) for r in new);sc=Counter()
    for r in new:sc[int(r['M'])]+=int(r['split_count'])
    return {'global_candidates':len(new),'anchored_split_candidates':sum(sc.values()),
            'global_M214_to_M220':[gc[m] for m in range(214,221)],
            'split_M214_to_M220':[sc[m] for m in range(214,221)]}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit-certificate',action='store_true')
    parser.add_argument('--replay-parent',action='store_true')
    args=parser.parse_args()
    require(upper(3,4)==9 and upper(4,3)==9,'self-contained Ramsey bound')
    masks,tables=core_cases()
    document={'profile':COUNTS,'red_edges':449,'core_masks':masks,
              'root_cover_cases':tables,'triangle_density_rows_H_lower_s_upper':triangle_case(),
              'union_feasible_cell_orbits':cell_vectors(),'cumulative':cumulative_totals()}
    text=json.dumps(document,sort_keys=True,indent=2)+'\n'
    if args.emit_certificate:print(text,end='');return
    require((HERE/'CERTIFICATE.json').read_text()==text,'certificate equality')
    tested=positive_and_negative_tests()
    if args.replay_parent:
        run=subprocess.run([sys.executable,'-O',str(HERE.parent/'ramsey_r55_signature_union_cuts/verify_certificate.py')],
                           check=True,capture_output=True,text=True)
        require('remaining_candidates=68 globals, 275 splits' in run.stdout,'parent replay totals')
    print('PASS all 64 exceptional graphs leave exactly eight cores in four classes')
    print('PASS star and both nontriangle cover contradictions: 5>3, 27>24, 26>24')
    print('PASS triangle core: at least 77 edges, at most 75 edges')
    print('PASS all six union-feasible cell vectors, exactly two relabeling orbits')
    print(f'PASS literal density audits: {tested} rooted subsets and a 19-vertex positive fixture')
    print('PASS pinned cumulative counts: 67 global candidates, 273 anchored splits')
    print('global_M214_to_M220='+','.join(map(str,document['cumulative']['global_M214_to_M220'])))
    print('split_M214_to_M220='+','.join(map(str,document['cumulative']['split_M214_to_M220'])))
    print('SCOPE hard-branch profile exclusion; not a 43-vertex target witness')
    print('certificate_sha256='+sha256(text.encode()).hexdigest())

if __name__=='__main__':main()
