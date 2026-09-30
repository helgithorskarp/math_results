"""Definition-level graph controls, false duals and a feasible sphere pair."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import copy,json,random
from graph import clique,verify_deletions
from certificates import Rows,verify_dual
from audit_sympy import pivoted_clique,cancellation,affine_rows,normalized_polynomials

def need(ok,message):
    if not ok:raise ValueError(message)

def definition(adjacency,size,active):
    vertices=[i for i in range(len(adjacency)) if active&(1<<i)]
    return any(all(adjacency[i]&(1<<j) for i,j in combinations(v,2))
               for v in combinations(vertices,size))

def compare(adjacency,size,active=None):
    if active is None:active=(1<<len(adjacency))-1
    want=definition(adjacency,size,active)
    found,_=clique(adjacency,size=size,active=active)
    native,_=pivoted_clique(adjacency,active,size=size)
    need((found is not None)==want==native,'two complete searches vs clique definition')
    if found is not None:
        need(len(found)==size and len(found)==len(set(found)),'distinct search witness')
        need(all(active&(1<<v) for v in found),'active search witness')
        need(all(adjacency[i]&(1<<j) for i,j in combinations(found,2)),'all witness edges')

def run():
    graphs=0;deletion_controls=0
    for n in (5,6):
        pairs=list(combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            adjacency=[0]*n
            for k,(i,j) in enumerate(pairs):
                if mask&(1<<k):adjacency[i]|=1<<j;adjacency[j]|=1<<i
            compare(adjacency,4);graphs+=1
            if n==5:
                for v in range(n):
                    for w in range(n):
                        if v==w or adjacency[v]&~adjacency[w]:continue
                        active=verify_deletions(adjacency,[[v,w]])
                        for size in (2,3,4,5):
                            need(definition(adjacency,size,(1<<n)-1)==definition(adjacency,size,active),'domination preserves all attainable clique sizes')
                        deletion_controls+=1
    rng=random.Random(20260930);seven_controls=0
    for case in range(1000):
        n=8;adjacency=[0]*n
        for i,j in combinations(range(n),2):
            if rng.randrange(5)>0:adjacency[i]|=1<<j;adjacency[j]|=1<<i
        if case%3==0:
            planted=rng.sample(range(n),7)
            for i,j in combinations(planted,2):adjacency[i]|=1<<j;adjacency[j]|=1<<i
        compare(adjacency,7);seven_controls+=1
    for n in (6,7,8):
        complete=[((1<<n)-1)^(1<<i) for i in range(n)]
        compare(complete,7);seven_controls+=1
    false_deletions=0
    for adjacency,trace in (([2,1],[[0,1]]),([0,0],[[0,0]]),([0,0],[[0,1],[0,1]]),([2,1,0],[[0,2]])):
        try:verify_deletions(adjacency,trace)
        except ValueError:false_deletions+=1
        else:raise ValueError('false domination accepted')
    data=json.loads((Path(__file__).parent/'certificate.json').read_text());kernel=Rows(Q(29,50),Q(593,1000))
    false_duals=0
    for kind in ('single_cells','conditioned_pairs'):
        original=data[kind][0]
        if kind=='single_cells':rows=kernel.single(original['cell']);native=affine_rows(normalized_polynomials(original['cell']),3)
        else:rows=kernel.pair(*original['cells']);native=affine_rows(normalized_polynomials(*original['cells']),5)
        need([(list(a),b) for a,b in rows]==native,'false-dual control rows agree')
        for mode in range(4):
            bad=copy.deepcopy(original)
            if mode==0:bad['weights'][0]=str(-Q(bad['weights'][0]))
            elif mode==1:bad['weights'][0]=str(Q(bad['weights'][0])+Q(1,1000000))
            elif mode==2:bad['negative_rhs']='0'
            else:bad['support'][0]=bad['support'][1]
            for check in (verify_dual,lambda r,z:cancellation(z,r)):
                try:check(rows,bad)
                except ValueError:false_duals+=1
                else:raise ValueError('false affine cancellation accepted')
    # Exact feasible -e1,-e2 pair at t=59/100; both avoid the eight core points.
    q=Q(59,100);r=2*q/(1+q)
    core=[(r*r-1,-r,r+r*r),(r,-1,r),(1,0,0),(r,r,-1),
          (r**3+r*r-r,r**3+2*r*r-1,-r-r*r),(r*r-1,r+r*r,-r),(0,1,0),(0,0,1)]
    def metric(a,b):return (1-q)*sum(x*y for x,y in zip(a,b))+q*sum(a)*sum(b)
    points=((-Q(1),Q(0),Q(0)),(Q(0),-Q(1),Q(0)))
    need(all(metric(p,p)==1 for p in points) and metric(*points)==q,'feasible geometric pair')
    need(all(metric(p,a)<=q for p in points for a in core),'control avoids core')
    rows=kernel.pair([10,512,512],[10,431,512]);x=(Q(7,13),-Q(1),-Q(1),-Q(1,159),-Q(1))
    need(all(sum(c*z for c,z in zip(a,x))<=b for a,b in rows),'all twenty-seven necessary rows admit control')
    return {'agent':'six-tammes-2','role':'researcher','status':'EXACT_DEFINITION_AND_GEOMETRIC_CONTROLS',
            'exhaustive_graphs':graphs,'domination_pairs':deletion_controls,'seven_clique_controls':seven_controls,
            'false_domination_traces':false_deletions,'false_duals_rejected':false_duals,'feasible_geometric_rows':27}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
