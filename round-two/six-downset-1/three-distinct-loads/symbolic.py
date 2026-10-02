"""Exact defining formulas for the three-distinct-load invariant budget.

Every rational operation is over QQ(Q,D,t,v), with q=Q+4. Cofactor
identities used by the final certificate are checked in verify_generic.py.
"""
from itertools import combinations
import polynomial as engine
P,R=engine.P,engine.R
require,atom,det=engine.require,engine.atom,engine.det
def variables(kind):
    def x(i):return kind(P({tuple(int(i==j) for j in range(4)):1}))
    return x(0)+4,x(1),x(2),x(3)
def zero(n,m=None):return [[R() for _ in range(n if m is None else m)] for _ in range(n)]
def seed_factors():
    q,D,t,v=variables(P);loads=[D,t,v];m=D+t+v;w=q+D-1;h=2*q+2*m-1
    factors=[D,t,v,m-2,m-1,m,m+1,h,h-2*D,h-q-D,*[(m-1)*w-1+d for d in loads],(h-q-1)*(h-D)-D*(q-1)]
    for factor in factors:atom(factor)
    return len(factors)
def scalars():
    q,D,t,v=variables(R);loads=[D,t,v];m=D+t+v;w=q+D-1;h=2*q+2*m-1
    ci=[m*(w-d-m-1)/((m+1)*((m-1)*w-1+d)) for d in loads]
    normK=w+m*(q+D)-D**2-t**2-v**2-2*m
    csquare=sum((c*c*d*(q+D-d) for c,d in zip(ci,loads)),R())
    kc=sum((c*d*(w-d) for c,d in zip(ci,loads)),R())
    eta=[w-normK/(m+1)**2-c*c*w+2*c*c*(q+D-d)/m-csquare/m**2+2*c*(w-d)/(m+1)-2*kc/(m*(m+1)) for c,d in zip(ci,loads)]
    E=sum((d*e for d,e in zip(loads,eta)),R())
    zeta=[m/(m-2)*(e-E/(m*(m-1))) for e in eta]
    W=[[zeta[i]/loads[i]*int(i==j)-(zeta[i]+zeta[j])/m+sum((d*z for d,z in zip(loads,zeta)),R())/m**2 for j in range(2)] for i in range(2)]
    signs={name:z for name,z in zip(['zeta_D','zeta_t','zeta_v'],zeta)}
    signs.update({name:1-c*c*(q+D)/(h-q-D)-z/h for name,c,z in zip(['within_D','within_t','within_v'],ci,zeta)})
    return signs,{'q':q,'D':D,'loads':loads,'m':m,'w':w,'h':h,'ci':ci,'eta':eta,'zeta':zeta,'W':W}
def old_budget(s):
    q,D,loads,m,h=(s[k] for k in ['q','D','loads','m','h'])
    metric=zero(7);delta=(h-q-1)*(h-D)-D*(q-1)
    metric[0][0]=(q-1)*(h-D)/delta;metric[0][1]=metric[1][0]=D*(q-1)/delta;metric[1][1]=D*(h-q-1)/delta
    for i in range(3):
        for j in range(3):metric[2+i][2+j]=D*(q*int(i==j)-1)/(h-2*D)
    for i in range(1,3):metric[4+i][4+i]=(q+D)*(1/loads[i]-1/D)/h
    L=[]
    for i in range(3):
        l=[R() for _ in range(7)];l[1]=l[2+i]=1/D
        if i>0:l[4+i]=R(1)
        L.append(l)
    K=[R(1),m/D-1,*[d/D for d in loads],loads[1],loads[2]]
    updates=L+[K];weights=[*[1/d for d in loads],m+1]
    A=[[weights[i]*int(i==j)-sum((updates[i][a]*metric[a][b]*updates[j][b] for a in range(7) for b in range(7) if metric[a][b].num and updates[i][a].num and updates[j][b].num),R()) for j in range(4)] for i in range(4)]
    return A
def border(s):
    ci,loads,m,h,W=(s[k] for k in ['ci','loads','m','h','W'])
    B=[[ci[i]*int(i==j)-loads[i]*ci[i]/m for j in range(2)] for i in range(3)]+[[R(),R()]]
    X=[[-B[i][j]/loads[i] for j in range(2)] for i in range(3)]+[[R(),R()]]
    E=[[int(i==j)/loads[i]-1/m-W[i][j]/h+sum((B[l][i]*B[l][j]/loads[l] for l in range(3)),R()) for j in range(2)] for i in range(2)]
    return X,E
def cofactors(A):
    return [[(-1)**(i+j)*det([[A[a][b] for b in range(4) if b!=i] for a in range(4) if a!=j]) for j in range(4)] for i in range(4)]

def border_terms(A,d4,X,E,C):
    """Return Y, Compound, six factored determinant summands.

    The general identities are independently checked by verify_generic.py.
    Each displayed rational function stays within the raw polynomial guard;
    the sixth determinant's products are deliberately left unexpanded.
    """
    Y=[[sum((X[a][i]*C[a][b]*X[b][j] for a in range(3) for b in range(3)),R()) for j in range(2)] for i in range(2)]
    pairs=list(combinations(range(3),2))
    plucker={I:X[I[0]][0]*X[I[1]][1]-X[I[0]][1]*X[I[1]][0] for I in pairs}
    compound=R()
    for I in pairs:
        for J in pairs:
            minor=det([[A[a][b] for b in range(4) if b not in I] for a in range(4) if a not in J])
            compound+=plucker[I]*plucker[J]*(-1)**(sum(I)+sum(J))*minor
    terms=[[d4,E[0][0],E[1][1]],[-d4,E[0][1],E[1][0]],[-E[1][1],Y[0][0]],[-E[0][0],Y[1][1]],[2*E[0][1],Y[0][1]],[compound]]
    return Y,compound,terms

def common_numerator_factors(terms):
    """Exact cross cancellation, then common positive denominator factors.

    Only small polynomial factors are constructed here. Each numerator
    product is evaluated later as separate Q-coefficient polynomials.
    """
    common={};normalized=[]
    for row in terms:
        numerators=[r.num for r in row];den={}
        for r in row:
            for key,power in r.den.items():den[key]=den.get(key,0)+power
        for key in tuple(den):
            for i in range(len(numerators)):
                while den[key]:
                    divided=engine.div_if_possible(numerators[i],key)
                    if divided is None:break
                    numerators[i]=divided;den[key]-=1
            if not den[key]:del den[key]
        for key,power in den.items():common[key]=max(common.get(key,0),power)
        normalized.append((numerators,den))
    products=[]
    for nums,den in normalized:
        products.append(nums+[engine.ATOMS[key] for key,power in sorted(common.items()) for _ in range(power-den.get(key,0))])
    return products,common
