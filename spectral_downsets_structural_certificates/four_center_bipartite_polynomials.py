"""Exact rational four-center certificates; complete scope in FOUR_CENTER_BIPARTITE.md."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import sys,json
from dense_cone_polynomials import constant,var,add,scale,mul,records
from bipartite_cone_polynomials import det,RationalPolynomial as RF
from verify import require
import clique_bipartite_face as face
import four_center_bipartite as cone

C=constant
P=add
def T(*args):
    out=C(1)
    for a in args:out=mul(out,a if isinstance(a,dict) else C(a))
    return out


def build(u,v):
    h=P(u,v);um1=P(u,C(-1));vm1=P(v,C(-1))
    Z=P(T(4,u,u),T(20,u),T(21,v),C(-33),T(-12,u,v))
    DL=T(4,u,um1);DR=T(4,v,vm1);D=T(4,u,v,um1,vm1)
    L13=P(T(-16,u,u,v),T(24,v),T(32,u))
    L23=T(4,u,P(u,C(1),T(-1,v,um1)))
    L=[[T(16,u,P(T(um1,P(h,C(1))),C(-6))),T(-4,DL),L13],
       [T(-4,DL),T(DL,P(h,C(3))),L23],
       [L13,L23,P(T(DL,v,P(u,C(5))),scale(-1,Z))]]
    R13=P(T(-4,u,DR),T(-4,v,P(T(4,u),C(1))))
    R23=P(T(-1,u,DR),T(17,v),C(-9))
    R=[[P(T(4,DR,P(h,C(1))),T(-24,v)),T(-4,DR),R13],
       [T(-4,DR),P(T(DR,P(h,C(4))),T(-9,vm1)),R23],
       [R13,R23,P(T(DR,u,P(v,C(5))),scale(-1,Z))]]
    S=[[P(T(2,u),v,C(12)),P(v,C(-12)),T(-2,u)],
       [P(v,C(-12)),P(T(4,u),T(6,v),C(12)),T(-4,u)],
       [T(-2,u),T(-4,u),T(2,u,P(v,C(3)))]]
    K=[[P(T(16,u),T(40,v),C(-96)),P(C(48),T(-12,v)),T(-16,u),{},T(-24,v)],
       [P(C(48),T(-12,v)),P(T(24,u),T(12,v),C(-24)),T(-48,u),T(8,u),T(8,v)],
       [T(-16,u),T(-48,u),T(16,u,P(v,C(7))),T(-16,u),T(24,v)],
       [{},T(8,u),T(-16,u),T(4,u,P(h,C(3))),{}],
       [T(-24,v),T(8,v),T(24,v),{},P(T(P(T(4,u),C(25)),v),C(-9))]]
    aux=dict(
       constant_trace=P(T(4,u,u,v,v),T(-15,u,v),T(-1,u,P(T(4,u),C(11))),T(-21,v),C(33)),
       center_trace=P(T(2,u,v),T(4,h),C(-13)),
       left_trace=P(T(4,u,v,um1,P(T(u,v),T(2,u),T(3,v),C(1))),T(24,u,v),Z),
       right_trace=P(T(4,u,v,vm1,P(T(u,v),T(3,u),T(2,v))),T(6,u,v),T(9,u,vm1),Z),
       left_scalar=P(T(um1,P(h,C(5))),C(2)),
       left_scalar_upper=P(T(um1,P(T(u,v),T(4,h),C(5))),C(-2)),
       right_scalar=P(T(2,vm1,P(h,C(5))),C(1)),
       right_scalar_upper=P(T(2,vm1,P(T(u,v),T(4,h),C(5))),C(-1)),
       edge=P(T(D,P(h,C(5))),Z),
       edge_upper=P(T(D,P(T(u,v),T(4,h),C(5))),scale(-1,Z)),
       center_edge_kernel=P(T(2,u),v,C(10)),
       center_edge_kernel_upper=P(T(2,u,v),T(8,u),T(9,v),C(10)))
    return dict(left=L,right=R,center_active=S,constant_active=K),aux


def raw(u,v):
    """Derive rational Grams from the affine equations, rather than build()."""
    h=u+v;d=h+3;eta=-v/2;jL=RF(0);jR=F(3,4)
    kL=2/(u-1);kR=1/(2*(v-1));tR=3/(2*u);bR=-1+9/(4*v);qR=F(-3,2)
    qAF=2-eta-u*jL-v*jR;pL=2-2*jL-(u-1)*kL;pR=2-2*jR-(v-1)*kR
    bA=1-2*qAF-u*pL-v*pR;qA=-(3-3*qAF+v*qR)/(u*v)
    rL=RF(F(1,3));rR=(1-u*tR-qR)/3
    wL=(v-2+3*jL-v*tR)/(v*(u-1));wR=(u-2+3*jR)/(u*(v-1))
    qF=(2-(u-1)*wL-(v-1)*wR-qA)/3
    cL=-(u+3-6*rL)/(v*(u-1));cR=-(v+3-6*rR+(v-1)*bR)/(u*(v-1))
    z=(6*qF-3-(u-1)*cL-(v-1)*cR)/((u-1)*(v-1))
    def leaf(q,k,b,w,c):
        return [[4*(h+1-3*k),RF(-4),-4*q*(1+w)],
                [RF(-4),d-b,-q*(1+c)],
                [-4*q*(1+w),-q*(1+c),q*(h+5+z-(1+z)*q)]]
    L=leaf(v,kL,0,wL,cL);R=leaf(u,kR,bR,wR,cR)
    S=[[d-bA,-2*(1+qAF),-u*(1+pL)],
       [-2*(1+qAF),2*(h+3-eta),-2*u*(1+jL)],
       [-u*(1+pL),-2*u*(1+jL),u*(h+5-u-(u-1)*kL)]]
    K=[[4*(d+3*bA),4*(-3+3*qAF),4*u*(-1+3*pL),RF(0),4*v*qR],
       [4*(-3+3*qAF),6*(h-1+eta),6*u*(-2+2*jL),6*u*rL,6*v*rR],
       [4*u*(-1+3*pL),6*u*(-2+2*jL),4*u*(h+1-u+3*(u-1)*kL),-4*u,4*u*v*tR],
       [RF(0),6*u*rL,-4*u,u*d,RF(0)],
       [4*v*qR,6*v*rR,4*u*v*tR,RF(0),v*(d+(v-1)*bR)]]
    return dict(left=L,right=R,center_active=S,constant_active=K),dict(z=z,kL=kL,kR=kR,eta=eta)


def clearing_identities():
    pu=P(var(0),C(2));pv=P(pu,var(1));u=RF(pu);v=RF(pv)
    matrices,aux=build(pu,pv);r,w=raw(u,v);checked=0
    factors=dict(left=4*u*(u-1),right=4*v*(v-1),center_active=2,constant_active=4)
    for name,M in matrices.items():
        for i,row in enumerate(M):
            for j,p in enumerate(row):
                require(RF(p)==factors[name]*r[name][i][j],'Independent Gram clearing failed: '+str((name,i,j)))
                checked+=1
    def expand(A,G):
        return [[sum(A[i][a]*G[a][b]*A[j][b] for a in range(len(G)) for b in range(len(G)))
                 for j in range(len(A))] for i in range(len(A))]
    def trace(G,norms):return sum(G[i][i]/norms[i] for i in range(len(G)))
    S=expand([[1,0,0],[0,1,0],[0,0,1],[-1,-1,-1]],r['center_active'])
    K=expand([[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[-1,-2,-1,0,0],
              [0,0,0,1,0],[0,0,0,0,1],[0,1,0,-1,-1]],r['constant_active'])
    h=u+v;m=10+5*h+u*v;D=4*u*v*(u-1)*(v-1)
    lamL=h+5+w['kL'];lamR=h+5+w['kR'];lamE=h+5+w['z'];lamF=h+5+w['eta']
    targets=dict(constant_trace=4*u*v*(m-trace(K,(4,6,4*u,4*v,u,v,u*v))),
                 center_trace=2*(m-trace(S,(1,2,u,v))),
                 left_trace=4*u*v*(u-1)*(m-trace(r['left'],(4,1,v))),
                 right_trace=4*u*v*(v-1)*(m-trace(r['right'],(4,1,u))),
                 left_scalar=(u-1)*lamL,left_scalar_upper=(u-1)*(m-lamL),
                 right_scalar=2*(v-1)*lamR,right_scalar_upper=2*(v-1)*(m-lamR),
                 edge=D*lamE,edge_upper=D*(m-lamE),
                 center_edge_kernel=2*lamF,center_edge_kernel_upper=2*(m-lamF))
    require(set(targets)==set(aux),'Trace/scalar scope mismatch')
    for name,p in aux.items():
        require(RF(p)==targets[name],'Independent trace/scalar clearing failed: '+name);checked+=1
    return checked


def certificate(u,v):
    mats,aux=build(u,v);out={};failures=[]
    for name,M in mats.items():
        out[name]=[]
        for n in range(1,len(M)+1):
            p=det([row[:n] for row in M[:n]]);out[name].append(records(p))
            negatives=records({k:c for k,c in p.items() if c<0})
            if p.get((0,0,0),0)<=0 or negatives:
                failures.append(dict(name=name,minor=n,constant=str(p.get((0,0,0),0)),negative_terms=negatives))
    for name,p in aux.items():
        out[name]=records(p)
        negatives=records({k:c for k,c in p.items() if c<0})
        if p.get((0,0,0),0)<=0 or negatives:
            failures.append(dict(name=name,constant=str(p.get((0,0,0),0)),negative_terms=negatives))
    terms=sum(sum(len(p) for p in out[name]) for name in mats)+sum(len(out[name]) for name in aux)
    return dict(positive_coefficients=not failures,failures=failures,positive_terms=terms,
                coefficient_sha256=sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest(),coefficients=out)


def pivots(matrix):
    a=[[F(x) for x in row] for row in matrix];n=len(a);out=[]
    require(all(len(row)==n for row in a),'Nonsquare finite block')
    require(all(a[i][j]==a[j][i] for i in range(n) for j in range(n)),'Nonsymmetric finite block')
    for k in range(n):
        p=a[k][k];require(p>=0,'Negative finite boundary pivot');out.append(str(p))
        if not p:
            require(all(not a[k][j] for j in range(k+1,n)),'Zero finite pivot with nonzero residual row')
            continue
        for i in range(k+1,n):
            for j in range(i,n):
                a[i][j]-=a[i][k]*a[k][j]/p;a[j][i]=a[i][j]
    return out


def boundary_certificates():
    out=[]
    for u,v in [(2,v) for v in range(3,21)]+[(3,3)]:
        w=cone.parameters(u,v);b=face.blocks(4,u,v,w);N=11+5*(u+v)+u*v
        def cap(G,norms,J=False):
            return [[(N-1)*norms[i]*(i==j)-(norms[i]*norms[j] if J else 0)-G[i][j]
                     for j in range(len(G))] for i in range(len(G))]
        tables={name:pivots(b[name]) for name in ('left','right','center_active','constant_active')}
        require(all(F(x)>0 for values in tables.values() for x in values),'Boundary active Gram is not positive definite')
        tables.update(left_upper_minus_I=pivots(cap(b['left'],(4,1,v))),
                      right_upper_minus_I=pivots(cap(b['right'],(4,1,u))),
                      center_upper_minus_I=pivots(cap(b['center'],b['center_norms'])),
                      constant_upper_minus_I=pivots(cap(b['constant'],b['constant_norms'],True)))
        require(all(0<x<N-1 for x in b['scalars']),'Boundary scalar/cap failed')
        out.append(dict(u=u,v=v,pivots=tables,scalars=list(map(str,b['scalars']))))
    return out


def rational_substitutions():
    parameters=[(2,21),(2,50),(3,4),(3,50),(4,4),(4,5),(5,5),(10,100),(100,10000)]
    checked=0;aux_checked=0
    for u,v in parameters:
        mats,aux=build(C(u),C(v));b=face.blocks(4,u,v,cone.parameters(u,v))
        factors=dict(left=4*u*(u-1),right=4*v*(v-1),center_active=2,constant_active=4)
        for name,M in mats.items():
            for i,row in enumerate(M):
                for j,p in enumerate(row):
                    require(p.get((0,0,0),0)==factors[name]*b[name][i][j],'Numeric clearing differs');checked+=1
        trace=lambda G,norms:sum(G[i][i]/norms[i] for i in range(len(G)))
        h=u+v;m=10+5*h+u*v;D=4*u*v*(u-1)*(v-1);ll,lr,le,lf=b['scalars']
        targets=dict(constant_trace=4*u*v*(m-trace(b['constant'],b['constant_norms'])),
            center_trace=2*(m-trace(b['center'],b['center_norms'])),
            left_trace=4*u*v*(u-1)*(m-trace(b['left'],(4,1,v))),
            right_trace=4*u*v*(v-1)*(m-trace(b['right'],(4,1,u))),
            left_scalar=(u-1)*ll,left_scalar_upper=(u-1)*(m-ll),
            right_scalar=2*(v-1)*lr,right_scalar_upper=2*(v-1)*(m-lr),
            edge=D*le,edge_upper=D*(m-le),center_edge_kernel=2*lf,center_edge_kernel_upper=2*(m-lf))
        for name,p in aux.items():
            require(p.get((0,0,0),0)==targets[name],'Numeric trace/scalar differs');aux_checked+=1
    return dict(parameters=[list(pair) for pair in parameters],entry_comparisons=checked,trace_scalar_comparisons=aux_checked)


def verify_certificate():
    regimes={};counts={};digests={}
    for name,u,v in [('u_ge_4',P(var(0),C(4)),P(var(0),C(4),var(1))),
                     ('u3_v_ge_4',C(3),P(var(1),C(4))),
                     ('u2_v_ge_21',C(2),P(var(1),C(21)))]:
        result=certificate(u,v)
        require(result['positive_coefficients'],'Uniform positive coefficient certificate failed: '+name)
        regimes[name]=result['coefficients'];counts[name]=result['positive_terms'];digests[name]=result['coefficient_sha256']
    fixture=dict(regimes=regimes,boundary_cores=boundary_certificates())
    summary=dict(cleared_identities=clearing_identities(),leading_minors_per_regime=14,
                 trace_scalar_certificates_per_regime=12,positive_terms=counts,regime_sha256=digests,
                 finite_centered_boundaries=len(fixture['boundary_cores']),rational_substitutions=rational_substitutions(),
                 canonical_certificate_sha256=sha256(json.dumps(fixture,sort_keys=True,separators=(',',':')).encode()).hexdigest())
    return summary,fixture


if __name__=='__main__':
    summary,fixture=verify_certificate()
    print(json.dumps(summary,sort_keys=True,indent=2))
