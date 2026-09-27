#!/usr/bin/env python3
"""Exact author controls; continuum proof and scope are in PROOF.md.

Sparse polynomial arithmetic adapted from the meridian precursor, graph6468.
No floating-point arithmetic, quadrature, optimizer or external dependency.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def norm2(a):
    return sum((x*x for x in a), Q(0))


def difference(a, b):
    return tuple(x-y for x,y in zip(a,b))


class Poly:
    """Sparse polynomial in twelve formally independent variables over Q."""
    dim = 12

    def __init__(self, terms=None):
        if isinstance(terms, (int, Q)):
            terms = {(0,)*self.dim: Q(terms)}
        self.terms = {k: Q(v) for k, v in (terms or {}).items() if v}

    def __add__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        out = dict(self.terms)
        for k, v in other.terms.items():
            out[k] = out.get(k, Q(0))+v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Poly) else -Q(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        out = {}
        for a, x in self.terms.items():
            for b, y in other.terms.items():
                k = tuple(i+j for i, j in zip(a, b))
                out[k] = out.get(k, Q(0))+x*y
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, k):
        require(isinstance(k, int) and k >= 0, 'Invalid polynomial exponent')
        out = Poly(1)
        for _ in range(k):
            out = out*self
        return out

    def diff(self, index):
        out = {}
        for a, x in self.terms.items():
            if a[index]:
                b = list(a)
                b[index] -= 1
                out[tuple(b)] = a[index]*x
        return Poly(out)

    @classmethod
    def var(cls, index):
        a = [0]*cls.dim
        a[index] = 1
        return cls({tuple(a): Q(1)})


def symbolic_checks():
    r,z,rho,zeta,s,w,sigma,eta,c,t,sn,omega = [Poly.var(i) for i in range(12)]
    A,B = r+t*(rho-r), s+t*(sigma-s)
    Z,W = z+t*(zeta-z), w+t*(eta-w)
    direct=A*A+B*B-2*A*B*c+(Z-W)**2
    radial=t*(1-t)*(r-rho-s+sigma)**2
    axial=t*(1-t)*(z-zeta-w+eta)**2
    direct=direct+radial+axial
    m0=(r-s)**2+(z-w)**2
    m1=(rho-sigma)**2+(zeta-eta)**2
    split=(1-t)*m0+t*m1+2*A*B*(1-c)
    require(not (direct-split).terms, 'Distance identity')
    K=(r-rho)*B+(s-sigma)*A
    expected=m1-m0-2*K*(1-c)+2*A*B*omega*sn
    actual=direct.diff(9)-omega*sn*direct.diff(8)
    require(not (actual-expected).terms, 'Phase derivative identity')
    # Three formally false constructions must be rejected.
    require(bool((direct-radial-split).terms), 'Missing radial auxiliary')
    require(bool((direct-axial-split).terms), 'Missing axial auxiliary')
    require(bool((actual-(expected-2*A*B*omega*sn)).terms), 'Missing phase term')

    # Collisions: epsilon regularization and time compression h=1-epsilon.
    eps=c
    h=1-eps
    re,ze=eps*r+h*rho,eps*z+h*zeta
    se,we=eps*s+h*sigma,eps*w+h*eta
    Me=m0-(re-se)**2-(ze-we)**2
    regular=h*(m0-m1)+eps*h*((r-s-rho+sigma)**2+(z-w-zeta+eta)**2)
    require(not (Me-regular).terms, 'Regularized meridian loss')
    Ae,Be=r+t*(re-r),s+t*(se-s)
    Ah,Bh=r+h*t*(rho-r),s+h*t*(sigma-s)
    require(not (Ae*Be-Ah*Bh).terms, 'Regularized P')
    require(not ((r-re)*Be+(s-se)*Ae-h*((r-rho)*Bh+(s-sigma)*Ah)).terms,
            'Regularized K')
    record=sorted((list(k),str(v)) for k,v in direct.terms.items())
    digest=hashlib.sha256(json.dumps(record,separators=(',',':')).encode()).hexdigest()
    return {'formal_variables':12,'universal_identities':5,
            'distance_monomials':len(direct.terms),'distance_sha256':digest,
            'damaged_formulas_rejected':3}


def phase_clock(t, rootq, rootc):
    q=rootq**2
    require(0<rootq<1 and rootq<=rootc<=1,'Clock domain')
    require(rootc**2==1-(1-q)*t,'Incorrect square root')
    lam=(1/rootc-1)/(1/rootq-1)
    speed=(1-q)/(2*(1/rootq-1)*rootc**3)
    return lam,speed


def allowance2(rootq,g):
    require(0<rootq<1 and 0<=g<1,'Uniform parameter domain')
    return 8*(1-g*g)*(1-rootq)/(rootq*rootq*(1+rootq))


def clock_checks():
    count=0
    for b,g in product([Q(1,8),Q(1,4),Q(1,2),Q(3,4)],[Q(1,2),Q(3,4)]):
        q=b*b
        require(allowance2(b,g)==8*(1-g*g)*(1/b-1)**2/(1-q),'Allowance identity')
        last=Q(-1)
        for v in [Q(j,8) for j in range(9)]:
            rootc=(1-v)+v*b
            t=(1-rootc**2)/(1-q)
            lam,speed=phase_clock(t,b,rootc)
            require(last<=lam<=1 and speed>0,'Phase normalization/monotonicity')
            require(rootc**6*speed**2==(1-q)**2/(4*(1/b-1)**2),'Clock invariant')
            last=lam
            count+=1
        require(phase_clock(Q(0),b,Q(1))[0]==0,'Initial phase')
        require(phase_clock(Q(1),b,b)[0]==1,'Final phase')
    return {'exact_clock_controls':count,'benchmark_allowance_squared':str(allowance2(Q(1,4),Q(9,16)))}


def main_map(p):
    r,z=p
    return (r/16,r/2+abs(z)/4),7*z


def coupled_control(p):
    # Finite control only: variable radial factors, a two-variable phase,
    # and zero target radius on a boundary. Not a second published theorem.
    r,z=p
    return (r*(1+z)/(32*(1+r)),r/2+abs(z)/4),3*r+6*z


def pair_data(p,sp,psi,v,sv,psiv,t):
    r,s=p[0],v[0]
    a,b=r-sp[0],s-sv[0]
    A,B=r-t*a,s-t*b
    M=norm2(difference(p,v))-norm2(difference(sp,sv))
    return M,A*B,a*B+b*A,psi-psiv


def controls(name, mapping, g, L2):
    rootq=Q(1,4);q=rootq**2
    require(L2<=allowance2(rootq,g),'Uniform input budget')
    points=[(Q(r,4),Q(z,2)) for r,z in product(range(5),range(-2,3))]
    labels=[(p,*mapping(p)) for p in points]
    for p,sp,psi in labels:
        require(0<=sp[0]<=q*p[0],'Transverse shrink condition')
    checks=axes=0
    cos_sin=[(Q(1),Q(0)),(Q(0),Q(1)),(Q(0),Q(-1)),(Q(-1),Q(0)),
             (Q(3,5),Q(4,5)),(Q(3,5),Q(-4,5))]
    for (p,sp,psi),(v,sv,psiv) in combinations(labels,2):
        mer=norm2(difference(p,v))
        require(norm2(difference(sp,sv))<=g*g*mer,'Meridian Lipschitz control')
        require((psi-psiv)**2<=L2*mer,'Phase Lipschitz control')
        for rootc in [Q(1),Q(7,8),Q(3,4),Q(5,8),Q(1,2),Q(3,8),Q(1,4)]:
            t=(1-rootc**2)/(1-q)
            lam,speed=phase_clock(t,rootq,rootc)
            M,P,K,d=pair_data(p,sp,psi,v,sv,psiv,t)
            budget=M*(M+4*K)-4*P*P*speed*speed*d*d
            require(M>=0 and K>=0 and budget>=0,'All-azimuth phase budget')
            if not p[0] or not v[0]:
                require(P==K==0,'Axis degeneracy')
                axes+=1
            if K:
                require(P*P/K<=rootc**6*p[0]*v[0]/(2*(1-q)),'Uniform P/K bound')
                require(M>=P*P*speed*speed*d*d/K,'Uniform sufficient bound')
            for c,sn in cos_sin:
                require(c*c+sn*sn==1,'Angle control')
                derivative=-M-2*K*(1-c)+2*P*speed*d*sn
                require(derivative<=0,'Signed derivative control')
            checks+=1
    return {'name':name,'meridian_labels':len(labels),'pairs':len(labels)*(len(labels)-1)//2,
            'all_azimuth_budget_controls':checks,'axis_controls':axes,
            'individual_azimuth_derivative_controls':checks*len(cos_sin)}


def matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def jacobian(u,rot,sign):
    return [[Q(rot,16),Q(0),-Q(7*rot*u[1],32)],
            [Q(0),Q(rot,16),Q(7*rot*u[0],32)],
            [Q(u[0],2),Q(u[1],2),Q(sign,4)]]


def determinant3(a):
    return sum(a[0][j]*(a[1][(j+1)%3]*a[2][(j+2)%3]-a[1][(j+2)%3]*a[2][(j+1)%3]) for j in range(3))


def scope_checks():
    directions=[(1,0),(0,1),(-1,0),(0,-1)]
    ds=[jacobian(u,a,b) for u,a,b in product(directions,(-1,1),(-1,1))]
    total=[[sum(d[i][j] for d in ds) for j in range(3)] for i in range(3)]
    require(total==[[0]*3 for _ in range(3)],'Mean Jacobian not zero')
    gs=[matmul(transpose(d),d) for d in ds]
    mean=[[sum(a[i][j] for a in gs)/len(ds) for j in range(3)] for i in range(3)]
    expected=[[Q(33,256),0,0],[0,Q(33,256),0],[0,0,Q(113,1024)]]
    require(mean==expected and all(mean[i][i]>0 for i in range(3)),'Mean Gram matrix')
    determinants=sorted(set(determinant3(d) for d in ds))
    require(determinants==[-Q(1,1024),Q(1,1024)],'Jacobian determinants')
    d1,d2=jacobian((1,0),1,1),jacobian((0,1),1,1)
    a,b=matmul(transpose(d1),d1),matmul(transpose(d2),d2)
    ab,ba=matmul(a,b),matmul(b,a)
    comm=[[ab[i][j]-ba[i][j] for j in range(3)] for i in range(3)]
    require(comm[0][1]==Q(4145,262144),'Noncommuting Gram matrices')
    return {'rational_jacobians':len(ds),'mean_jacobian_zero':True,
            'mean_gram_diagonal':[str(mean[i][i]) for i in range(3)],
            'jacobian_determinants':[str(x) for x in determinants],
            'gram_commutator':[[str(x) for x in row] for row in comm]}


def negative_controls():
    p,v=(Q(1),Q(0)),(Q(1),Q(1,8))
    sp,psi=main_map(p);sv,psiv=main_map(v)
    M,P,K,d=pair_data(p,sp,psi,v,sv,psiv,Q(0))
    linear=M*(M+4*K)-4*P*P*d*d
    require(linear<0,'Undetected invalid linear clock')
    M,P,K,d=pair_data(p,sp,2*psi,v,sv,2*psiv,Q(1))
    speed=phase_clock(Q(1),Q(1,4),Q(1,4))[1]
    excessive=M*(M+4*K)-4*P*P*speed*speed*d*d
    require(excessive<0,'Undetected excessive phase')
    rejected=0
    for rootq,g in [(Q(0),Q(1,2)),(Q(1),Q(1,2)),(Q(1,4),Q(1))]:
        try:
            allowance2(rootq,g)
        except ValueError:
            rejected+=1
    require(rejected==3,'Invalid parameter accepted')
    return {'linear_clock_budget':str(linear),'doubled_phase_budget':str(excessive),
            'invalid_parameters_rejected':rejected,'invalid_phase_schedules_rejected':2}


def run():
    return {'status':'PASS','arithmetic':'Python integers and Fraction; no floats',
            'symbolic':symbolic_checks(),'clock':clock_checks(),
            'families':[controls('folding helical benchmark',main_map,Q(9,16),Q(49)),
                        controls('variable-factor control',coupled_control,Q(3,5),Q(45))],
            'scope':scope_checks(),'negative_controls':negative_controls()}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--emit',action='store_true')
    args=parser.parse_args()
    record=run()
    data=json.dumps(record,sort_keys=True,indent=2)+'\n'
    expected=Path(__file__).with_name('EXPECTED.json')
    if args.emit:
        expected.write_text(data)
    else:
        require(expected.read_text()==data,'Deterministic record mismatch')
    print(json.dumps({'status':'PASS','record_sha256':hashlib.sha256(data.encode()).hexdigest(),
                      'universal_identities':record['symbolic']['universal_identities'],
                      'all_azimuth_budget_controls':sum(x['all_azimuth_budget_controls'] for x in record['families']),
                      'rational_jacobians':record['scope']['rational_jacobians']},sort_keys=True))


if __name__=='__main__':
    main()
