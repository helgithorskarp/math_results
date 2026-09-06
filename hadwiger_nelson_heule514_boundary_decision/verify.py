#!/usr/bin/env python3
"""Independent exact local geometry, direct-enumeration audit and witnesses.

No import of the producer or inherited arithmetic/colouring implementations.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations,product
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
N=[[361,417,495,503,509],[418,498,506,508],[359,362,502],[358,416,507]]
B=sorted({0}|{v for row in N for v in row})


def need(ok,message):
    if not ok:raise ValueError(message)


def load(path):return json.loads(path.read_text())


def multiply(a,b):
    """Recursive quadratic tower: Q(sqrt3)(sqrt5)(sqrt11)."""
    if len(a)==1:return (a[0]*b[0],)
    h=len(a)//2; d={2:3,4:5,8:11}[len(a)]
    ac=multiply(a[:h],b[:h]);bd=multiply(a[h:],b[h:])
    ad=multiply(a[:h],b[h:]);bc=multiply(a[h:],b[:h])
    return tuple(x+d*y for x,y in zip(ac,bd))+tuple(x+y for x,y in zip(ad,bc))


def point(raw):
    need(len(raw)==2 and all(len(a)==8 for a in raw),'point domain')
    return tuple(tuple(Fraction(x) for x in a) for a in raw)


def norm(p,q):
    axes=[multiply(tuple(x-y for x,y in zip(p[a],q[a])),tuple(x-y for x,y in zip(p[a],q[a]))) for a in range(2)]
    return tuple(x+y for x,y in zip(*axes))


def geometry():
    for name,digest in load(HERE/'manifest.json').items():
        need(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input digest',name))
    old=load(REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json')
    labels=[v for v in range(553) if '510' in old['provenance'][v]]
    points=[point(old['coordinates'][str(labels[v])]) for v in B]
    pool=load(REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json')
    points += [point(next(r for r in pool if r['centre_index']==j)['coordinates']) for j in(170,436,1239,1527)]
    need(len(set(points))==20 and points[0]==((0,)*8,(0,)*8),'distinct local points and origin')
    edges=[(u,v) for u,v in combinations(range(20),2) if norm(points[u],points[v])==(1,)+(0,)*7]
    need(len(edges)==35,'local edge count')
    be=[(u,v) for u,v in edges if v<16];need(len(be)==13 and all(u!=0 for u,v in be),'induced boundary')
    need([(u,v) for u,v in edges if u>=16]==[(16,17),(17,18),(18,19)],'added path')
    for i,row in enumerate(N):
        need([B[u] for u,v in edges if v==16+i and u<16]==[0]+row,'complete old attachment')
    groups=[next((i for i,row in enumerate(N) if v in row),-1) for v in B]
    return edges,be,groups


def list_key(c):
    available=[]
    for neighbours in N:
        used={int(c[B.index(v)]) for v in neighbours}
        available.append(sum(1<<(x-1) for x in range(1,4) if x not in used))
    return sum(x<<(3*i) for i,x in enumerate(available))


def path_assignments(key):
    return [c for c in product(range(1,4),repeat=4)
            if all(key & (1<<(3*i+x-1)) for i,x in enumerate(c))
            and all(c[i]!=c[i+1] for i in range(3))]


def violated(key,kernel):
    return [j for j,row in enumerate(kernel) if not any(key & (1<<(x-5)) for x in row['clause'] if x>0)]


def verify(work):
    start=time.monotonic();edges,be,groups=geometry()
    g=load(work/'boundary.json')
    need(g['vertices']==B and g['groups']==groups and g['edges']==[list(e) for e in be],'entrywise boundary graph')
    raw=f'16 13 0\n'+''.join(f'{v} {group}\n' for v,group in zip(B,groups))+''.join(f'{u} {v}\n' for u,v in be)
    need((work/'boundary.txt').read_text()==raw,'actual C++ input file')
    direct=(work/'direct.counts').read_bytes();producer=(work/'profiles.counts').read_bytes()
    need(direct==producer,'entrywise independent full-profile stream, order and EOF')
    counts=[int(x) for x in direct.decode('ascii').splitlines()]
    need(len(counts)==4096 and all(x>=0 for x in counts),'complete profile count domain')
    need(direct==''.join(str(x)+'\n' for x in counts).encode('ascii'),'canonical count format')
    domain={sum(x<<(3*i) for i,x in enumerate(row)) for row in product(range(7),repeat=4)}
    need({i for i,x in enumerate(counts) if x}==domain,'every and only proper-subset list tuple is attainable')
    need(sum(counts)==12*36*756*84==27433728,'independent chromatic-polynomial product count')
    kernel=load(REPO/'hadwiger_nelson_heule514_path_projection/certificate.json')['obstructions']
    violations=Counter();profiles=Counter();extension_hist=Counter();rows=[0]*37;unique=[0]*37
    for key,count in enumerate(counts):
        bad=violated(key,kernel);extensions=path_assignments(key)
        need(bool(extensions)==(not bad),'independent full-path assignment/kernel equality')
        if count:
            violations[len(bad)]+=count;profiles[len(bad)]+=1;extension_hist[len(extensions)]+=count
            for j in bad:rows[j]+=count
            if len(bad)==1:unique[bad[0]]+=count
    result=load(work/'result.json');cert=load(work/'certificate.json')
    for key,value in dict(proper_boundary_colourings=sum(counts),attainable_list_profiles=len(domain),
                          extending_boundary_colourings=violations[0],nonextending_boundary_colourings=sum(counts)-violations[0],
                          attainable_extending_profiles=profiles[0],attainable_nonextending_profiles=len(domain)-profiles[0],
                          full_local_colourings=sum(k*v for k,v in extension_hist.items()),
                          profiles_sha256=sha256(direct).hexdigest(),profiles_bytes=len(direct),
                          violation_histogram={str(k):v for k,v in sorted(violations.items())},
                          profile_violation_histogram={str(k):v for k,v in sorted(profiles.items())},
                          extension_count_histogram={str(k):v for k,v in sorted(extension_hist.items())}).items():
        need(result[key]==value,('complete census result',key))
    need(result['attainable_obstruction_clauses']==result['individually_necessary_clauses']==list(range(37)),'all 37 actual boundary obstructions and unique violations')
    need(cert['boundary_order']==B and len(cert['clauses'])==37,'certificate indexing')
    witness_checks=0
    def check(c):
        nonlocal witness_checks
        need(len(c)==16 and c[0]=='0' and set(c)<=set('0123'),'boundary witness domain')
        need(all(c[u]!=c[v] for u,v in be),'boundary edge inequalities');witness_checks+=len(be)
        return list_key(c)
    for j,row in enumerate(cert['clauses']):
        need(row['clause']==j and row['boundary_colourings']==rows[j]>0,'clause weighted attainability')
        need(row['unique_violation_colourings']==unique[j]>0,'clause weighted unique violation')
        need(j in violated(check(row['witness']),kernel),'obstructed boundary witness')
        need(violated(check(row['unique_witness']),kernel)==[j],'individually necessary clause witness')
    bad=cert['nonextension'];key=check(bad['colouring'])
    need(bad['lists']==[(key>>(3*i))&7 for i in range(4)] and bad['violated_clauses']==violated(key,kernel),'counterexample lists')
    need(not path_assignments(key),'direct counterexample nonextension')
    proper_selections=0
    for mask in range(15):
        selected=[i for i in range(4) if mask & (1<<i)]
        works=False
        for colours in product(range(1,4),repeat=len(selected)):
            partial=dict(zip(selected,colours))
            if all(key & (1<<(3*i+c-1)) for i,c in partial.items()) and all(partial[i]!=partial[i+1] for i in range(3) if i in partial and i+1 in partial):
                works=True;break
        need(works,'counterexample extends to every proper selected subpath');proper_selections+=1
    good=cert['extension'];check(good['boundary_colouring']);full=good['boundary_colouring']+good['path_colouring']
    need(len(full)==20 and set(full)<=set('0123') and all(full[u]!=full[v] for u,v in edges),'proper 20-point graph witness');witness_checks+=len(edges)
    for name in('boundary.json','boundary.txt','certificate.json','result.json'):
        public=HERE/name
        if public.exists():need(public.read_bytes()==(work/name).read_bytes(),('public compact result',name))
    return dict(status='COMPLETE LOCAL BOUNDARY SATURATION AND NONEXTENSION VERIFIED',
                universal_extension=False,record_improvement=False,H514_family_closed=False,
                exact_point_pairs=190,local_vertices=20,local_unit_edges=35,boundary_unit_edges=13,
                origin_colour=0,boundary_colourings=sum(counts),all_and_only_proper_subset_list_tuples=True,
                attainable_profiles=2401,extending_boundary_colourings=violations[0],nonextending_boundary_colourings=sum(counts)-violations[0],
                extending_profiles=profiles[0],nonextending_profiles=2401-profiles[0],
                full_local_colourings=sum(k*v for k,v in extension_hist.items()),
                all_37_clauses_attainable_and_individually_necessary=True,
                counterexample_proper_path_selections_checked=proper_selections,
                independently_compared_profile_entries=4096,path_states_checked=4096,
                witness_edge_checks=witness_checks,profiles_sha256=sha256(direct).hexdigest(),
                native_graph_queries=0,seconds=time.monotonic()-start)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--report',type=Path);a=p.parse_args()
    r=verify(a.work)
    if a.report:a.report.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,sort_keys=True))
