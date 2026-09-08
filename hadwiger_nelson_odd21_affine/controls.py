"""Finite controls for the metric, degeneracy, and source-colouring checks."""
from itertools import combinations,product
from fractions import Fraction as F
from math import isqrt,lcm
import json
import verify as v
import full_audit as g
from source_check import colour,check


def require(test,label):
    if not test:raise ValueError(label)


def main():
    # An independently rounded rational interval for the physical sqrt(85).
    scale=10**30;lo=isqrt(85*scale*scale);hi=lo+1
    signs=0
    for a,b in product(range(-20,21),repeat=2):
        left=a*scale+min(b*lo,b*hi);right=a*scale+max(b*lo,b*hi)
        exact=right<0 or left>0 or (a,b)==(0,0)
        require(exact,'sign interval unresolved')
        sg=(left>0)-(right<0)
        require(g.sign((a,b))==sg,'integer field sign')
        require(v.positive((F(a),F(b)))==(sg>0),'rational field sign')
        signs+=1
    require(v.points()==g.points(),'independent source coordinates')
    source_pairs=0
    p=v.points();q=g.points()
    for i,j in combinations(range(21),2):
        dx,dy=(g.sub(q[i][k],q[j][k]) for k in (0,1));xy=g.mul(dx,dy)
        integer=(g.mul(dx,dx),(2*xy[0],2*xy[1]),g.mul(dy,dy))
        require(v.row(p[i],p[j])==integer,'independent source pair')
        source_pairs+=1
    # Prescribed SPD forms and three prescribed independent directions.
    metric_fixtures=0
    for a,b,c in [(2,0,3),(5,1,7),(13,-2,1),(1,0,1)]:
        form=((F(a),F(0)),(F(b),F(0)),(F(c),F(0)))
        # Gaussian recovery is checked with arbitrary right sides by scaling
        # rows, so these fixtures need not correspond to source point pairs.
        raw=[((F(1),F(0)),v.ZERO,v.ZERO),
             (v.ZERO,v.ZERO,(F(1),F(0))),
             ((F(1),F(0)),(F(2),F(0)),(F(1),F(0)))]
        rows=[]
        for r in raw:
            z=v.ZERO
            for x,y in zip(r,form):z=v.plus(z,v.times(x,y))
            rows.append(tuple(v.divide(x,z) for x in r))
        require(v.gaussian(rows)==form,'metric recovery')
        den=lcm(*(z.denominator for r in rows for x in r for z in x))
        integral=[tuple((int(x[0]*den),int(x[1]*den)) for x in r) for r in rows]
        scaled=tuple((x[0]/den,x[1]/den) for x in form)
        require(g.metric(*integral)==v.canonical(scaled),'two metric methods')
        metric_fixtures+=1
    graphs=0;subset_checks=0
    for n in range(6):
        pairs=list(combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            es=[e for j,e in enumerate(pairs) if mask>>j&1]
            expected=True
            for selected in range(1,1<<n):
                subset_checks+=1
                ds=[sum(selected>>u&1 for a,b in es for u in ([b] if a==z else [a] if b==z else []))
                    for z in range(n) if selected>>z&1]
                if min(ds)>=4:expected=False
            word=v.peel(n,es)
            require((word is not None)==expected,'induced-subset degeneracy definition')
            if word is not None:require(all(word[a]!=word[b] for a,b in es),'peeling word')
            # A five-clique is the only non-four-colourable graph through 5.
            found,_=colour(n,es,4)
            require((found is None)==(n==5 and len(es)==10),'small colouring search')
            graphs+=1
    # Three explicit faults: parallel/inconsistent metric rows, a five-clique,
    # and incorrectly including the source's long edges as unit edges.
    r=((F(1),F(0)),v.ZERO,v.ZERO)
    require(v.gaussian([r,r,tuple(v.plus(x,x) for x in r)]) is None,'singular metric')
    require(v.peel(5,list(combinations(range(5),2))) is None,'K5 rejection')
    rr={(i,j):v.row(p[i],p[j]) for i,j in combinations(range(21),2)}
    physical=(1,0,0,0,3,0,65536)
    require(len(v.edges(physical,rr))==7,'unit/odd distance distinction')
    require(check()['source_odd_edges']==55,'odd source distinction')
    print(json.dumps({'verified':True,'field_sign_fixtures':signs,
          'independent_source_pairs':source_pairs,'metric_recovery_fixtures':metric_fixtures,
          'simple_graphs_through_order_five':graphs,'induced_subset_checks':subset_checks,
          'explicit_fault_controls':3},indent=2,sort_keys=True))


if __name__=='__main__':main()
