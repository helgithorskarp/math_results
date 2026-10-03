"""Independent definition-level Gaussian and full nine-phase controls.
Arbitrary algebraic configurations: NO original-disk feasibility or F cut asserted.
"""
from fractions import Fraction as F
import core as c
import json

def ga(a=0,b=0): return F(a),F(b)
def add(*zs): return sum((z[0] for z in zs),F(0)),sum((z[1] for z in zs),F(0))
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def scale(z,s): return z[0]*s,z[1]*s
def cj(z): return z[0],-z[1]
def norm(z): return z[0]**2+z[1]**2
def inv(z): return scale(cj(z),1/norm(z))
def power(z,n):
    if n<0:return power(inv(z),-n)
    out=ga(1)
    for _ in range(n):out=mul(out,z)
    return out
def polynomial(roots):
    p=[ga(1)]
    for z in roots:
        q=[ga() for _ in range(len(p)+1)]
        for j,a in enumerate(p):
            q[j]=add(q[j],scale(mul(a,z),-1));q[j+1]=add(q[j+1],a)
        p=q
    return p
def at(p,z): return add(*(mul(a,power(z,j)) for j,a in enumerate(p)))
def embed(z): return c.fs(c.phase(0),z[0]),c.fs(c.phase(0),z[1])
def ea(z,w): return c.fa(z[0],w[0]),c.fa(z[1],w[1])
def em(z,w): return c.fa(c.fm(z[0],w[0]),c.fs(c.fm(z[1],w[1]),-1)),c.fa(c.fm(z[0],w[1]),c.fm(z[1],w[0]))
def es(z,q): return c.fs(z[0],q),c.fs(z[1],q)
def ep(n): return c.phase(n),(F(0),)*6
def ec(z): return c.fc(z[0]),c.fs(c.fc(z[1]),-1)
def er(z): return es(ea(z,ec(z)),F(1,2))
def encoded(z): return [list(map(str,z[0])),list(map(str,z[1]))]

def build(damage=None):
    tuples=[
        [ga()]*8,
        [ga(0,k) for k in (1,1,1,1,1,1,1,-7)],
        [ga(1,2),ga(-2,1),ga(3,-1),ga(-1,-3),ga(2,0),ga(-3,2),ga(0,-1),ga(0,0)],
        [ga(k) for k in (2,2,-1,-1,-1,-1,0,0)],
        [ga(k) for k in (7,-1,-1,-1,-1,-1,-1,-1)],
    ]
    records=[]
    for index,roots in enumerate(tuples):
        c.need(add(*roots)==ga(),'zero sum controls')
        nu=[scale(z,F(1,1000)) for z in roots]
        mean=ga(F(3,100000),F(-1,100000));a=F(11999,12000);u=add(ga(a),scale(mean,-1))
        V=sum((norm(z) for z in nu),F(0));T=add(*(power(z,2) for z in nu));U=add(*(power(z,3) for z in nu))
        product=polynomial(nu)
        primitive=[ga()]+[scale(a,F(9,j+1)) for j,a in enumerate(product)]
        primitive[0]=scale(at(primitive,u),-1)
        c.need(primitive[8]==ga(),'absent centered degree8')
        c.need(primitive[7]==scale(T,F(-9,14)),'Newton degree7')
        c.need(primitive[6]==scale(U,F(-1,2)),'Newton degree6')
        c.need(at(primitive,u)==ga(),'exact marked zero')
        c.need([scale(primitive[j],j) for j in range(1,10)]==[scale(z,9) for z in product],'full derivative')
        S4=sum((norm(z)**2 for z in nu),F(0))
        sos=sum((norm(nu[j])*sum((norm(add(nu[k],scale(nu[l],-1))) for k in range(8) for l in range(k+1,8) if j not in (k,l)),F(0)) for j in range(8)),F(0))
        c.need(7*V*V-8*S4==sos,'quartic control')
        EE=sum((z[0]**2 for z in nu),F(0));A=F(4,5);beta=F(6,5)
        R=sum((z[0]*(A*z[0]**2-beta*z[1]**2) for z in nu),F(0))
        c.need(R*R<=EE*(F(3,4)*beta**2*V**2+beta*(A+beta)*EE*(V-EE)/4),'joint cubic control')
        rotated=mul(T,mul(cj(u),inv(u)))
        c.need(norm(rotated)<=V*V,'Gram control')
        phases=[]
        for k in range(9):
            # Entire p(u*w) via every degree; unlike a selected top-degree jet.
            value=embed(primitive[0])
            for j in range(1,10):
                value=ea(value,em(embed(mul(primitive[j],power(u,j))),ep(k*j)))
            raw=em(es(value,F(-1,9)),em(embed(power(u,-8)),ep(-8*k)))
            derived=embed(ga())
            for j in range(1,8):
                if damage=='drop_d3' and j==3:continue
                term=em(embed(mul(scale(primitive[j],F(-1,9)),power(u,j-8))),
                        ea(ep(k*(j-8)),es(ep(k),-1)))
                derived=ea(derived,term)
                # Direct normal from delta_j and base versus simplified full normal.
                base=em(embed(cj(u)),ep(-k))
                actual=er(em(base,term))
                factor=mul(scale(primitive[j],F(-1,9)),mul(cj(u),power(u,j-8)))
                simple=er(em(embed(factor),ea(ep(k*j),es(ep(0),-1))))
                c.need(actual==simple,'each full principal coefficient normal')
            c.need(raw==derived,'whole principal displacement all degrees')
            phases.append(encoded(raw))
        records.append({'control':index,'centered_roots':[[str(x),str(y)]for x,y in nu],
                        'mean':[str(x)for x in mean],'u':[str(x)for x in u],
                        'V':str(V),'T':[str(x)for x in T],'U3':[str(x)for x in U],
                        'product':[[str(x),str(y)]for x,y in product],
                        'primitive':[[str(x),str(y)]for x,y in primitive],
                        'all9_principal_displacements':phases,'quartic_sos':str(sos)})
    return records

if __name__=='__main__':
    print(json.dumps(build(),indent=2,sort_keys=True))
