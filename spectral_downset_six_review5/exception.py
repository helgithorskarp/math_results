"""Independent exact exceptional certificate and polynomial identity checks."""
from fractions import Fraction as F
from itertools import permutations, combinations
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
FACETS=[7,11,21,26,28,38,41,44,49,50]
SPEC=[(1,2,2),(1,6,-1),(1,12,4),(1,26,1),(3,12,0),(3,20,1),(3,28,5)]

def need(c,m):
    if not c:raise ValueError(m)

def mul(a,b):
    bt=list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col)) for col in bt] for row in a]

def identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]

def polynomial_matrix(coefficients,a):
    n=len(a);result=[[0]*n for _ in range(n)]
    for c in coefficients:
        result=mul(result,a)
        for i in range(n):result[i][i]+=c
    return result

def quadratic(a,v):return sum(v[i]*a[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))

def congruence(a):
    """Diagonal congruence through explicit transformations, including witnesses."""
    n=len(a);b=[list(map(F,row)) for row in a];transform=[list(map(F,row)) for row in identity(n)]
    pivots=[]
    for k in range(n):
        j=max(range(k,n),key=lambda i:b[i][i])
        if j!=k:
            b[k],b[j]=b[j],b[k]
            for row in b:row[k],row[j]=row[j],row[k]
            for row in transform:row[k],row[j]=row[j],row[k]
        d=b[k][k]
        need(d>=0,'negative PSD pivot')
        if d==0:
            need(all(b[i][j]==0 for i in range(k,n) for j in range(k,n)),'zero diagonal with nonzero block')
            break
        pivots.append(d)
        factors=[b[k][j]/d for j in range(k+1,n)]
        for j,factor in zip(range(k+1,n),factors):
            for i in range(n):transform[i][j]-=factor*transform[i][k]
        for i in range(k+1,n):
            for j in range(i,n):
                b[i][j]-=b[i][k]*b[k][j]/d;b[j][i]=b[i][j]
        for j in range(k+1,n):b[k][j]=b[j][k]=0
    # An explicit congruence identity authenticates the entire elimination.
    diagonal=mul(list(zip(*transform)),mul(a,transform))
    need(all(diagonal[i][j]==(pivots[i] if i==j and i<len(pivots) else 0)
             for i in range(n) for j in range(n)),'diagonal congruence identity')
    return pivots,None

def build():
    members=sorted({a for t in FACETS for a in range(64) if a&t==a});need(len(members)==32,'family size')
    facets={a for a in members if not any(a!=b and a&b==a for b in members)}
    need(facets==set(FACETS),'facet identity')
    need([sum(bool(a&(1<<i)) for a in members) for i in range(6)]==[11]*6,'stars')
    need(all(sum(t&p==p for t in FACETS)==2 for p in members if p.bit_count()==2),'design incidences')
    need(not any((a&b)==0 for a,b in combinations(FACETS,2)),'disjoint facets')
    group=[]
    for p in permutations(range(6)):
        action=[sum(1<<p[i] for i in range(6) if a&(1<<i)) for a in range(64)]
        if {action[t] for t in FACETS}==facets:group.append(action)
    need(len(group)==60,'automorphism group')
    values={};orbit_sizes=[]
    for a,b,value in SPEC:
        edges={tuple(sorted((g[a],g[b]))) for g in group}
        need(not values.keys()&edges,'overlapping declared orbits');orbit_sizes.append(len(edges))
        for edge in edges:values[edge]=value
    allowed={(a,b) for a,b in combinations(members[1:],2) if a&b==0}
    need(values.keys()==allowed,'incomplete declared orbits')
    q=[]
    for a in members:
        row=[]
        for b in members:
            if a==b==0:x=30
            elif a==0 or b==0:x={1:-9,2:1,3:3}[(a|b).bit_count()]
            elif a&b:x=0
            else:x=values[tuple(sorted((a,b)))]
            row.append(x)
        q.append(row)
    need(all(q[i][j]==q[j][i] for i in range(32) for j in range(32)),'asymmetric Q')
    need(all(sum(row)==21 for row in q),'row normalization')
    need(all(q[i][j]==0 for i,a in enumerate(members) for j,b in enumerate(members) if a&b),'support')
    return members,q,orbit_sizes

def matchings(items):
    if not items:yield ();return
    a=items[0]
    for b in items[1:]:
        for rest in matchings([x for x in items if x!=a and x!=b]):yield ((1<<a)|(1<<b),)+rest

def fractional(members):
    weight={a:F(a.bit_count()-1,3) for a in members if a}
    def cliques(start,used,total):
        yield total
        for i in range(start,len(members)):
            a=members[i]
            if a and not a&used:yield from cliques(i+1,a|used,total+weight[a])
    dual_max=max(cliques(1,0,F(0)));need(dual_max==1,'dual clique inequality')
    primal=[]
    for t in FACETS:
        for i in range(6):
            if not t&(1<<i):primal.append(((t,63^t^(1<<i),1<<i),F(1,3)))
    primal.extend((m,F(1,9)) for m in matchings(list(range(6))))
    for clique,w in primal:need(all(not a&b for a,b in combinations(clique,2)),'invalid primal clique')
    coverage={a:sum(w for clique,w in primal if a in clique) for a in weight}
    need(all(c>=1 for c in coverage.values()),'fractional cover missing member')
    dual=sum(weight.values());need(sum(w for clique,w in primal)==dual==F(35,3),'fractional optimum')
    bins=[(7,24,32),(4,26,33),(1,28,34),(11,16,36),(9,38),(2,21,40),
          (20,41),(18,44),(3,12,48),(6,8,49),(5,50),(10,17)]
    flat=[a for c in bins for a in c]
    need(sorted(flat)==members[1:] and all(not a&b for c in bins for a,b in combinations(c,2)),'12-bin cover')
    return {'dual':'35/3','primal':'35/3','primal_cliques':len(primal),'integral_cover':12,
            'coverage_by_rank':{str(k):sorted({str(coverage[a]) for a in coverage if a.bit_count()==k}) for k in (1,2,3)}}

def isolated_extensions(members,w):
    output=[]
    for r in (0,1,2,5,11):
        new=[1<<(6+i) for i in range(r)];sets=members+new;N=len(sets);den=N-11;m=N-1
        core=[[w[i][j] if i<31 and j<31 else 10*int(i==j)
               for j in range(m)] for i in range(m)]
        sums=list(map(sum,core))
        q=[[sum(sums)+1-11]+[1-a for a in sums]]
        for i,row in enumerate(core):q.append([1-sums[i]]+[a+1-11*int(i==j) for j,a in enumerate(row)])
        need(all(sum(row)==den for row in q),'extension rows')
        need(all(q[i][j]==0 for i,a in enumerate(sets) for j,b in enumerate(sets) if a&b),'extension support')
        need(max(sum(bool(a&(1<<i)) for a in sets) for i in range(6+r))==11,'extension stars')
        need(F(q[0][0],den)==F(30+10*r,21+r)>1,'extension empty loop')
        # The same primal cliques extended by all new singletons remain disjoint.
        primal=[]
        for t in FACETS:
            for i in range(6):
                if not t&(1<<i):primal.append(((t,63^t^(1<<i),1<<i,*new),F(1,3)))
        primal.extend(((*c,*new),F(1,9)) for c in matchings(list(range(6))))
        need(all(not a&b for c,weight in primal for a,b in combinations(c,2)),'extension primal clique')
        need(all(sum(weight for c,weight in primal if a in c)>=1 for a in sets if a),'extension fractional cover')
        need(sum(weight for c,weight in primal)==F(35,3),'extension fractional value')
        output.append({'r':r,'N':N,'s':11,'ground_size':6+r,'fractional_cover':'35/3',
                       'empty_loop':str(F(q[0][0],den))})
    return output

def main():
    members,q,orbits=build();w=[[q[i+1][j+1]+11*int(i==j)-1 for j in range(31)] for i in range(31)]
    # Use candidate polynomial coefficients only as untrusted proposed data.
    data=json.loads((HERE/'input.json').read_text())
    polynomial=data['W_annihilator_descending']
    need(len(polynomial)>1 and polynomial[0]>0 and all(isinstance(c,int) for c in polynomial),
         'annihilator must be a nonzero positive-leading integer polynomial')
    need(all((-1)**k*c>=0 for k,c in enumerate(polynomial)),'polynomial sign certificate')
    need(all(x==0 for row in polynomial_matrix(polynomial,w) for x in row),'annihilator identity')
    pivots,_=congruence(w);need(len(pivots)==24,'rank')
    lift=[[sum(map(sum,w))]+[-sum(row) for row in w]]
    for row in w:lift.append([-sum(row)]+row)
    need(all(lift[i][j]+1==q[i][j]+11*int(i==j) for i in range(32) for j in range(32)),'PSD lift')
    z=[1]+[0]*31
    delta=F(21*sum(x*x for x in z)-quadratic(q,z),21)
    need(delta==F(-3,7),'uncapped empty-loop quadratic witness')
    y=[32*int(bool(a&1))-11 for a in members]
    need(all(sum(q[i][j]*y[j] for j in range(32))==-11*y[i] for i in range(32)),'minimum eigenvector')
    product_form=352*sum(x*x for x in y)*delta
    need(product_form==672*F(quadratic(q,z),21)*F(-11*sum(x*x for x in y),21)
         +352*sum(x*x for x in z)*sum(x*x for x in y),'tensor form identity')
    result={'reviewer':'six-reviewer-5','N':32,'s':11,'family_mask':sum(1<<a for a in members),
            'automorphism_order':60,'orbit_sizes':orbits,'original_Q_sha256':sha256(json.dumps(q,separators=(',',':')).encode()).hexdigest(),
            'W_annihilator_descending':polynomial,'W_rank':len(pivots),'fractional':fractional(members),
            'uncapped_original_witness':z,'uncapped_quadratic':str(delta),
            'original_tensor_square_Hoffman_quadratic':str(product_form),
            'isolated_singleton_extensions':isolated_extensions(members,w)}
    need(result['original_Q_sha256']==data['original_Q_sha256'],'source matrix correspondence')
    return result

if __name__=='__main__':print(json.dumps(main(),indent=2)+'\n',end='')
