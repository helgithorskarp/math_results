"""Definition-level search/containment controls and geometric cover controls."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import copy,json,random
from graph import clique
from audit_sympy import pivoted_clique,dominate
from check import verify

def need(ok,message):
    if not ok:raise ValueError(message)

def definition(a,k,active):
    vertices=[i for i in range(len(a)) if active&(1<<i)]
    return any(all(a[i]&(1<<j) for i,j in combinations(z,2))
               for z in combinations(vertices,k))

def compare(a,k):
    active=(1<<len(a))-1;wanted=definition(a,k,active)
    found,_=clique(a,size=k);native,_=pivoted_clique(a,active,size=k)
    need((found is not None)==wanted==native,'two complete searches vs definition')
    reduced,trace=dominate(a)
    need(definition(a,k,reduced)==wanted,'domination preserves clique existence')
    alive=set(range(len(a)))
    for v,w in trace:
        need(v!=w and v in alive and w in alive and not a[v]&(1<<w),'live nonadjacent replacement')
        need(all(a[w]&(1<<j) for j in alive if a[v]&(1<<j)),'all current neighbors contained')
        alive.remove(v)
    need(reduced==sum(1<<i for i in alive),'trace final active set')
    if found is not None:
        need(len(set(found))==k and all(a[i]&(1<<j) for i,j in combinations(found,2)),'true clique witness')

def run():
    graphs=0;preservation_checks=0
    for n in (5,6):
        pairs=list(combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            a=[0]*n
            for k,(i,j) in enumerate(pairs):
                if mask&(1<<k):a[i]|=1<<j;a[j]|=1<<i
            compare(a,4);graphs+=1
            if n==5:
                reduced,_=dominate(a)
                for k in (2,3,4,5):
                    need(definition(a,k,(1<<n)-1)==definition(a,k,reduced),'all small clique sizes preserved')
                    preservation_checks+=1
    rng=random.Random(20260930);seven=0
    for case in range(1000):
        n=8;a=[0]*n
        for i,j in combinations(range(n),2):
            if rng.randrange(5)>0:a[i]|=1<<j;a[j]|=1<<i
        if case%3==0:
            for i,j in combinations(rng.sample(range(n),7),2):a[i]|=1<<j;a[j]|=1<<i
        compare(a,7);seven+=1
    for n in (6,7,8):
        compare([((1<<n)-1)^(1<<i) for i in range(n)],7);seven+=1
    # Removing every closed retained cell containing the chart origin must
    # leave an unprovable hole: -e1 is an actual admissible extra point.
    data=json.loads((Path(__file__).parent/'certificate.json').read_text())
    corrupt=[]
    z=copy.deepcopy(data);z['interval'][0]=[1,2];corrupt.append(z)
    z=copy.deepcopy(data);z['remaining_cover_cells'][0][0]=13;corrupt.append(z)
    z=copy.deepcopy(data);z['remaining_cover_cells'].append(z['remaining_cover_cells'][0]);corrupt.append(z)
    z=copy.deepcopy(data);z['remaining_cover_cells']=[c for c in z['remaining_cover_cells']
        if not (c[1]<=2**(c[0]-1)<=c[1]+1 and c[2]<=2**(c[0]-1)<=c[2]+1)];corrupt.append(z)
    rejected=0
    for z in corrupt:
        try:verify(z,details=True)
        except ValueError:rejected+=1
        else:raise ValueError('corrupt cover accepted')
    # A genuine pair at an interior t checks the elementary pair graph
    # accepts geometric feasibility. Both -e1,-e2 avoid all eight points.
    t=Q(57,100);r=2*t/(1+t)
    core=[(r*r-1,-r,r+r*r),(r,-1,r),(1,0,0),(r,r,-1),
          (r**3+r*r-r,r**3+2*r*r-1,-r-r*r),(r*r-1,r+r*r,-r),(0,1,0),(0,0,1)]
    def metric(a,b):return (1-t)*sum(x*y for x,y in zip(a,b))+t*sum(a)*sum(b)
    points=[(-Q(1),Q(0),Q(0)),(Q(0),-Q(1),Q(0))]
    need(all(metric(p,p)==1 for p in points) and metric(*points)==t,'exact separated sphere pair')
    need(all(metric(p,a)<=t for p in points for a in core),'pair avoids all core points')
    charts=[(Q(0),Q(0)),(-1/(1+t),Q(0))]
    def contains(c,p):
        d,i,j=c;h=Q(8,2**d)
        return -4+i*h<=p[0]<=-4+(i+1)*h and -4+j*h<=p[1]<=-4+(j+1)*h
    containing=[[tuple(c) for c in data['remaining_cover_cells'] if contains(c,p)] for p in charts]
    need(all(containing),'real points covered, including closed chart origin boundary')
    from model import exact_qmax,exact_rmin
    need(all(2*exact_qmax(a,b,Q(14,25)) >= (1-Q(29,50))*exact_rmin(a,Q(29,50))*exact_rmin(b,Q(29,50))
             for a in containing[0] for b in containing[1]),'every real-pair cell assignment compatible')
    return {'agent':'six-tammes-2','role':'researcher','status':'EXACT_SEARCH_DOMINATION_AND_COVER_CONTROLS',
            'exhaustive_four_clique_graphs':graphs,'all_small_clique_preservation_checks':preservation_checks,
            'seven_clique_controls':seven,'corrupt_covers_rejected':rejected,
            'feasible_geometric_pair_assignments':len(containing[0])*len(containing[1])}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
