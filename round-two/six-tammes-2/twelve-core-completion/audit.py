"""Exact Gram identification and ordinary stability scalar checks.

This is an auxiliary implementation by the same author, not independent
researcher review. No active-plane predicate is repeated here.
"""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as Q
import hashlib
import json
import signal
import check as c
import field as f

HERE=Path(__file__).resolve().parent
def gram(points,H):
    normals=[f.matvec(H,p) for p in points]
    return [[f.dot(p,n) for n in normals] for p in points]
def run(data,plan):
    c.layout(data,plan)
    H,V,constraints,units,contacts,q,other=c.geometry(data)
    for a,b in combinations(units[0],2):
        squared=f.sub(f.scalar(2),f.scale(f.dot(a,f.matvec(H,b)),2))
        c.require(f.sign(f.sub(squared,f.scalar(Q(1,25))))>0,
                  'every two cut unit vertices separated by squared distance above1/25')
    squared=f.sub(f.scalar(2),f.scale(f.dot(units[1][0],f.matvec(H,units[1][1])),2))
    c.require(f.sign(f.sub(squared,f.scalar(Q(1,25))))>0,
              'last two exact alternatives separated by squared distance above1/25')
    c.require(f.sign(f.sub(f.dot(V[13],f.matvec(H,q)),f.scalar(Q(97,100))))>0,
              'strict incompatible pair margin above97/100')
    original=gram(V,H);cyclic_points=list(V);cyclic_points[14]=other
    cyclic=gram(cyclic_points,H)
    refs={'asymmetric':original,'cyclic':cyclic}
    records=data['candidate_gram_permutations']
    c.require(len(records)==4 and [r['case'] for r in records]==[
        ['p13','p14'],['p13','c14'],['q','p14'],['q','c14']],
        'all four original completion cases')
    identified=[]
    for record in records:
        points=list(V)
        if record['case'][0]=='q':points[13]=q
        if record['case'][1]=='c14':points[14]=other
        G=gram(points,H)
        for i,j in combinations(range(15),2):
            c.require(f.sign(f.sub(G[i][j],f.T))<=0,'every candidate is a genuine fifteen-point tau-code')
        c.require(len(record['heuristic_matches'])==1,'one proposed exact full-Gram identification')
        match=record['heuristic_matches'][0];reference=match['reference'];permutation=match['permutation']
        c.require(reference in refs and len(permutation)==15 and sorted(permutation)==list(range(15)),
                  'literal bijection of all fifteen points')
        J=refs[reference]
        c.require(all(G[i][j]==J[permutation[i]][permutation[j]] for i in range(15) for j in range(15)),
                  'complete exact Gram equality, not contact-graph isomorphism')
        identified.append({'case':record['case'],'reference':reference,'permutation':permutation})
    # Reconstruct the already known cyclic code, using the credited reflection architecture.
    r=f.mul(f.scale(f.T,2),f.inverse(f.add(f.ONE,f.T)))
    built={i:V[i] for i in (0,5,11,1,2,4)}
    steps=((6,0,11,5),(7,0,5,11),(9,5,11,0),(14,0,6,11),
           (12,5,7,0),(13,11,9,5),(3,1,4,2),(8,2,4,1),(10,1,2,4))
    for n,i,j,o in steps:
        built[n]=tuple(f.sub(f.mul(r,f.add(x,y)),z) for x,y,z in zip(built[i],built[j],built[o]))
    J=gram([built[i] for i in range(15)],H);permutation=data['known_cyclic_permutation']
    c.require(permutation==[1,0,11,7,5,4,10,3,9,8,6,2,14,13,12],'credited known cyclic map')
    c.require(all(cyclic[i][j]==J[permutation[i]][permutation[j]] for i in range(15) for j in range(15)),
              'cyclic alternative is exactly the known construction')
    delta=Q(1,10**7);cut_distance=2002;last_plane=2003;last_distance=1000
    c.require(400*delta<=Q(1,2),'short mass leaves a unit mass at least1/6')
    c.require(2*(100+150)*4+2==cut_distance,'three-unit cut stability coefficient')
    c.require(Q(97,100)-2*cut_distance*delta>Q(593,1000),
              'same unit or incompatible pair choices cannot pack even after relaxation')
    c.require(f.HI+delta<Q(593,1000),'relaxed pair parameter lies in the established cap-capacity band')
    c.require(last_plane==1+cut_distance and last_plane*delta<=Q(1,1000),
              'entry into either exact fourteen-core relaxed polytope')
    c.require(16*Q(1,1000)<=Q(1,2),'two-unit relaxed mass argument domain')
    c.require(2*(4+100)*4+2<=last_distance,'two-unit last-point distance coefficient')
    c.require(last_distance*last_plane<=2100000,'whole added-triple distance coefficient')
    return {'status':'CHECKED_EXACT_GRAM_AND_STABILITY',
            'four_labeled_completions':identified,'known_cyclic_gram_checked':True,
            'pair_bounds_checked':4*105,'literal_full_gram_equalities_checked':4*225+225,
            'all_unit_squared_distances_greater_than':'1/25',
            'incompatible_pair_product_greater_than':'97/100',
            'relaxation_max':'1/10000000','cut_unit_distance_constant':cut_distance,
            'whole_added_triple_distance_constant':2100000,
            'source_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in c.FROZEN}}

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second auxiliary guard')))
    signal.alarm(50)
    print(json.dumps(run(json.loads((HERE/'INPUT.json').read_text()),
                         json.loads((HERE/'PLAN.json').read_text())),sort_keys=True))
