"""Exact uniform coefficient/LDL certificate for three-center bipartite cones."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json,sys
from dense_cone_polynomials import constant,var,add,scale,mul,records,evaluate
from bipartite_cone_polynomials import det,RationalPolynomial as RF
from bipartite_cone_polynomials import pivots
from three_center_bipartite import parameters as production
from clique_bipartite_face import blocks


def build(u,v,two=False):
    one=constant(1);h=add(u,v);um1=add(u,constant(-1));vm1=add(v,constant(-1))
    u2=mul(u,u);D=scale(4,mul(u,v,um1,vm1))
    Z=add(scale(2,u2),scale(4,u),mul(add(constant(9),scale(-4,u)),v))
    W=add(mul(add(scale(2,u),constant(-3)),v),scale(-2,u))
    L13=scale(-3,mul(v,add(D,scale(2,mul(vm1,W)))))
    L23=scale(-1,mul(v,add(D,scale(-2,mul(u,vm1,add(scale(2,u),one))))))
    L=[[add(scale(3,mul(add(h,one),D)),scale(-48,mul(u,v,vm1))),scale(-3,D),L13],
       [scale(-3,D),mul(add(h,constant(2)),D),L23],
       [L13,L23,mul(v,add(mul(add(u,constant(4)),D),scale(-2,mul(vm1,Z))))]]
    R13=scale(-3,mul(u,add(D,scale(2,mul(v,um1,add(scale(2,u),constant(-1)))))))
    R23=scale(-1,mul(u,add(D,scale(-9,mul(v,um1)))))
    R=[[add(scale(3,mul(add(h,one),D)),scale(-36,mul(u,v,um1))),scale(-3,D),R13],
       [scale(-3,D),mul(add(h,constant(3)),D),R23],
       [R13,R23,mul(u,add(mul(add(v,constant(4)),D),scale(-2,mul(um1,Z))))]]
    S=[[add(scale(2,u),v,constant(6)),add(v,constant(-6)),scale(-2,u)],
       [add(v,constant(-6)),add(scale(2,h),constant(6)),scale(-2,u)],
       [scale(-2,u),scale(-2,u),scale(2,mul(u,add(v,constant(2))))]]
    K=[[add(scale(12,u),scale(24,v)),scale(-6,v),scale(-12,u),{},scale(-12,v)],
       [scale(-6,v),scale(12,h),scale(-24,u),scale(6,u),scale(3,v)],
       [scale(-12,u),scale(-24,u),scale(12,mul(u,add(v,constant(5)))),scale(-12,u),scale(18,v)],
       [{},scale(6,u),scale(-12,u),scale(4,mul(u,add(h,constant(2)))),{}],
       [scale(-12,v),scale(3,v),scale(18,v),{},scale(4,mul(v,add(u,constant(3))))]]
    n=add(constant(6),scale(4,h),mul(u,v))
    def upper(G,norms):
        return [[add(mul(n,D,norms[i]),scale(-1,G[i][j])) if i==j else scale(-1,G[i][j]) for j in range(3)] for i in range(3)]
    matrices=dict(left=L,right=R,center_active=S,constant_active=K,
                  left_upper_minus_I=upper(L,[constant(3),one,v]),
                  right_upper_minus_I=upper(R,[constant(3),one,u]))
    other=dict(edge=add(mul(add(h,constant(4)),D),scale(2,Z)),
               edge_upper=add(mul(add(mul(u,v),scale(3,h),constant(2)),D),scale(-2,Z)),
               center_trace=add(scale(2,mul(u,v)),scale(2,u),scale(3,v),constant(-9)),
               constant_trace=add(scale(2,mul(u2,v,v)),scale(-2,mul(u2,v)),scale(-2,mul(u,v,v)),
                                  scale(-20,mul(u,v)),scale(-2,u2),scale(-4,u),scale(-9,v)))
    if two:
        # The u=2 recipe replaces k_L=2 by 3/2, hence p_L=1/2.
        # Here u is the polynomial constant 2.
        if u!=constant(2):raise ValueError('The modified recipe requires u=2')
        L[0][0]=add(L[0][0],scale(3,D))
        matrices['left_upper_minus_I'][0][0]=add(matrices['left_upper_minus_I'][0][0],scale(-3,D))
        S[0][0]=add(S[0][0],constant(2));S[0][2]=S[2][0]=add(S[0][2],constant(-2));S[2][2]=add(S[2][2],constant(2))
        K[0][0]=add(K[0][0],constant(-24));K[0][2]=K[2][0]=add(K[0][2],constant(24));K[2][2]=add(K[2][2],constant(-24))
        other['center_trace']=add(other['center_trace'],constant(-3))
        other['constant_trace']=add(other['constant_trace'],scale(6,mul(u,v)))
    return matrices,other


def raw_symbolic(u,v,two):
    h=u+v;kL=RF(F(3,2)) if two else 2/(u-1);kR=3/(2*(v-1))
    jL=0;jR=RF(F(1,2));kT=aL=aR=tL=bL=bT=qL=0
    tR=3/(2*u);bR=qR=-1
    # Derive all forced entries from independent row/star equations.
    qAF=2-u*jL-v*jR
    pL=2-jL-(u-1)*kL-v*kT;pR=2-jR-(v-1)*kR-u*kT
    bA=1-qAF-u*pL-v*pR;qA=-(2-qAF+u*qL+v*qR)/(u*v)
    rL=(1-(u-1)*aL-v*tL-qL)/2;rR=(1-(v-1)*aR-u*tR-qR)/2
    wL=(v-1+jL-(u-1)*aL-v*tR)/(v*(u-1))
    wR=(u-1+jR-(v-1)*aR-u*tL)/(u*(v-1))
    qF=(2-(u-1)*wL-(v-1)*wR-qA)/2
    cL=-(u+2-3*rL+(u-1)*bL+v*bT)/(v*(u-1))
    cR=-(v+2-3*rR+(v-1)*bR+u*bT)/(u*(v-1))
    z=(3*qF-2-(u-1)*cL-(v-1)*cR)/((u-1)*(v-1))
    def leaf(q,k,b,w,c):
        return [[3*(h+1-2*k),RF(-3),-3*q*(1+w)],
                [RF(-3),h+2-b,-q*(1+c)],
                [-3*q*(1+w),-q*(1+c),q*(h+4+z-(1+z)*q)]]
    L=leaf(v,kL,bL,wL,cL);R=leaf(u,kR,bR,wR,cR)
    S=[[h+2-bA,-(1+qAF),-u*(1+pL)],
       [-(1+qAF),h+3,-u*(1+jL)],
       [-u*(1+pL),-u*(1+jL),u*(h+4-u-(u-1)*kL)]]
    K=[[3*(h+2+2*bA),3*(-2+qAF),3*u*(-1+2*pL),3*u*qL,3*v*qR],
       [3*(-2+qAF),3*h,3*u*(-2+jL),3*u*rL,3*v*rR],
       [3*u*(-1+2*pL),3*u*(-2+jL),3*u*(h+1-u+2*(u-1)*kL),-3*u,3*u*v*tR],
       [3*u*qL,3*u*rL,-3*u,u*(h+2+(u-1)*bL),u*v*bT],
       [3*v*qR,3*v*rR,3*u*v*tR,u*v*bT,v*(h+2+(v-1)*bR)]]
    n=6+4*h+u*v
    def upper(G,norms):return [[n*norms[i]-G[i][j] if i==j else -G[i][j] for j in range(3)] for i in range(3)]
    mats=dict(left=L,right=R,center_active=S,constant_active=K,
              left_upper_minus_I=upper(L,(3,1,v)),right_upper_minus_I=upper(R,(3,1,u)))
    def gram(T,M):return [[sum(T[i][a]*M[a][b]*T[j][b] for a in range(len(M)) for b in range(len(M))) for j in range(len(T))] for i in range(len(T))]
    H=gram([[1,0,0],[0,1,0],[0,0,1],[-1,-1,-1]],S)
    G=gram([[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[-1,-2,-1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,1,0,-1,-1]],K)
    center_trace=sum(H[i][i]/norm for i,norm in enumerate((1,1,u,v)))
    constant_trace=sum(G[i][i]/norm for i,norm in enumerate((3,3,3*u,3*v,u,v,u*v)))
    return mats,dict(edge=h+4+z,edge_upper=n-h-4-z,center_trace=2*(n-center_trace),constant_trace=2*u*v*(n-constant_trace))


def independent_clearing():
    checked=0
    for two in (False,True):
        pu=constant(2) if two else add(var(0),constant(3))
        pv=add(var(1),constant(3)) if two else add(pu,var(1))
        u=RF(pu);v=RF(pv);raw,aux=raw_symbolic(u,v,two)
        matrices,other=build(pu,pv,two);D=4*u*v*(u-1)*(v-1)
        for name,M in matrices.items():
            clear=2 if name=='center_active' else 4 if name=='constant_active' else D
            for i,row in enumerate(M):
                for j,P in enumerate(row):
                    if not RF(P)==clear*raw[name][i][j]:raise ValueError('Cleared entry failed:'+str(two)+':'+name+':'+str((i,j)))
                    checked+=1
        for name in other:
            clear=D if name in ('edge','edge_upper') else 1
            if not RF(other[name])==clear*aux[name]:raise ValueError('Auxiliary identity failed:'+str(two)+':'+name)
            checked+=1
    return checked


def compact(P):
    if any(k for i,j,k in P):raise ValueError('Unexpected third variable')
    return [[i,j,c] for (i,j,k),c in sorted(P.items())]


def check_positive(P,label):
    if P.get((0,0,0),0)<=0 or any(type(c) is not int or c<=0 for c in P.values()):
        raise ValueError('Nonpositive coefficient:'+label)
    return compact(P)


def numeric_data(u,v):
    b=blocks(3,u,v,production(u,v));n=6+4*(u+v)+u*v
    def upper(G,norms):return [[n*norms[i]*(i==j)-G[i][j] for j in range(3)] for i in range(3)]
    mats={name:b[name] for name in ('left','right','center_active','constant_active')}
    mats['left_upper_minus_I']=upper(b['left'],(3,1,v));mats['right_upper_minus_I']=upper(b['right'],(3,1,u))
    center_trace=sum(b['center'][i][i]/norm for i,norm in enumerate(b['center_norms']))
    constant_trace=sum(b['constant'][i][i]/norm for i,norm in enumerate(b['constant_norms']))
    aux=dict(edge=b['scalars'][2],edge_upper=n-b['scalars'][2],center_trace=2*(n-center_trace),constant_trace=2*u*v*(n-constant_trace))
    return mats,aux,b


def matrix_pivots(u,v,boundary=False):
    raw,_,b=numeric_data(u,v);n=6+4*(u+v)+u*v;norms=b['constant_norms']
    constant=[[n*norms[i]*(i==j)-norms[i]*norms[j]-b['constant'][i][j] for j in range(7)] for i in range(7)]
    diagonal=pivots(constant)
    if any(F(x)<=0 for x in diagonal[:-1]) or diagonal[-1]!='0':raise ValueError('Constant cap exception failed')
    result=dict(u=u,v=v,constant_upper_minus_I=diagonal)
    if boundary:
        raw['center_upper_minus_I']=[[n*b['center_norms'][i]*(i==j)-b['center'][i][j] for j in range(4)] for i in range(4)]
        result['pivots']={name:pivots(M) for name,M in raw.items()}
        if any(F(x)<=0 for row in result['pivots'].values() for x in row):raise ValueError('Boundary is not PD')
        if any(not 0<x<n for x in b['scalars'][:3]):raise ValueError('Boundary scalar failed')
        result['scalars']=list(map(str,b['scalars'][:3]))
    return result


def rational_substitutions():
    inputs=[(2,3),(2,11),(2,12),(2,20),(3,3),(3,7),(3,8),(4,4),(4,5),(4,6),(5,5),(6,11),(10,100),(100,10000)]
    checked=0
    for u,v in inputs:
        two=u==2;pu=constant(2) if two else add(var(0),constant(3));pv=add(var(1),constant(3)) if two else add(pu,var(1))
        matrices,other=build(pu,pv,two);raw,aux,_=numeric_data(u,v);A=0 if two else u-3;B=v-3 if two else v-u
        D=4*u*v*(u-1)*(v-1)
        for name,M in matrices.items():
            clear=2 if name=='center_active' else 4 if name=='constant_active' else D
            for i,row in enumerate(M):
                for j,P in enumerate(row):
                    if evaluate(P,A,B,0)!=clear*raw[name][i][j]:raise ValueError('Rational entry comparison failed')
                    checked+=1
        for name,P in other.items():
            if evaluate(P,A,B,0)!=(D if name in ('edge','edge_upper') else 1)*aux[name]:raise ValueError('Rational scalar comparison failed')
            checked+=1
    return dict(parameters=[list(x) for x in inputs],entry_comparisons=checked)


def verify_certificate():
    fixture=dict(regimes={},constant_trace={},constant_cap_exceptions=[],boundary_cores=[]);counts={}
    for name,u,v,two in [('u_ge_3',add(var(0),constant(3)),None,False),('u2_v_ge_3',constant(2),add(var(1),constant(3)),True)]:
        if v is None:v=add(u,var(1))
        matrices,other=build(u,v,two);rows={}
        for label,M in matrices.items():
            rows[label]=[check_positive(det([row[:n] for row in M[:n]]),name+':'+label+':'+str(n)) for n in range(1,len(M)+1)]
        for label in ('edge','edge_upper','center_trace'):rows[label]=check_positive(other[label],name+':'+label)
        fixture['regimes'][name]=rows
        counts[name]={k:[len(p) for p in row] if k in matrices else len(row) for k,row in rows.items()}
    for name,u,v,two in [('u_ge_5',add(var(0),constant(5)),None,False),('u2_v_ge_12',constant(2),add(var(0),constant(12)),True),('u3_v_ge_8',constant(3),add(var(0),constant(8)),False),('u4_v_ge_6',constant(4),add(var(0),constant(6)),False)]:
        if v is None:v=add(u,var(1))
        fixture['constant_trace'][name]=check_positive(build(u,v,two)[1]['constant_trace'],name+':trace')
    for u,vs in ((2,range(3,12)),(3,range(3,8)),(4,range(4,6))):
        for v in vs:fixture['constant_cap_exceptions'].append(matrix_pivots(u,v))
    fixture['boundary_cores'].append(matrix_pivots(2,2,True))
    summary=dict(cleared_polynomial_identities=independent_clearing(),positive_terms=counts,
                 trace_positive_terms={k:len(row) for k,row in fixture['constant_trace'].items()},
                 constant_cap_exceptions=16,boundary_cores=1,rational_substitutions=rational_substitutions())
    summary['canonical_certificate_sha256']=sha256(json.dumps(fixture,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return summary,fixture


if __name__=='__main__':
    summary,fixture=verify_certificate()
    print(json.dumps(dict(summary=summary,coefficient_certificate=fixture),indent=2,sort_keys=True))
