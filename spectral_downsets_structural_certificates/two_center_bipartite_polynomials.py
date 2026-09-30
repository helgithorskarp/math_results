"""Exact uniform polynomial/LDL certificates for two-center bipartite cones."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sys,time
from dense_cone_polynomials import constant,var,add,scale,mul,records,evaluate
from bipartite_cone_polynomials import det,RationalPolynomial as RF
import two_center_bipartite as cone
from bipartite_cone_polynomials import pivots


def build(u,v):
    h=add(u,v);one=constant(1);um1=add(u,constant(-1));vm1=add(v,constant(-1))
    u2=mul(u,u);v2=mul(v,v);u3=mul(u2,u)
    D=scale(3,mul(u2,v,um1,vm1))
    Du=scale(3,mul(u2,v,vm1));Dv=scale(3,mul(u2,v,um1))
    Z=add(scale(3,u3),scale(12,u2),mul(add(scale(-3,u2),scale(19,u),constant(-3)),v))
    CL13=scale(-6,mul(u,v2,vm1,add(u2,constant(-2))))
    CL23=add(scale(-1,mul(v,D)),mul(add(u,constant(2)),Du))
    L=[[add(scale(2,mul(add(h,one),D)),scale(-4,Du)),scale(-2,D),CL13],
       [scale(-2,D),add(mul(add(h,one),D),scale(3,mul(v2,um1,vm1))),CL23],
       [CL13,CL23,add(mul(v,add(u,constant(3)),D),scale(-1,mul(v,vm1,Z)))]]
    CR13=scale(-6,mul(u3,um1,add(v2,constant(-2))))
    Rc=add(scale(14,mul(u,v)),scale(-3,v),scale(-3,u))
    CR23=add(scale(-1,mul(u,D)),mul(u,um1,Rc))
    R=[[add(scale(2,mul(add(h,one),D)),scale(-4,Dv)),scale(-2,D),CR13],
       [scale(-2,D),add(mul(add(h,constant(2)),D),scale(-3,mul(u2,um1,vm1))),CR23],
       [CR13,CR23,add(mul(u,add(v,constant(3)),D),scale(-1,mul(u,um1,Z)))]]
    K=[[scale(6,mul(u,add(h,constant(2)))),scale(-6,u),scale(-6,u2),{},scale(-2,mul(u,v))],
       [scale(-6,u),scale(3,mul(u,add(h,one))),scale(-6,u2),scale(-3,u2),scale(-2,mul(u,v))],
       [scale(-6,u2),scale(-6,u2),scale(6,mul(u2,add(v,constant(3)))),scale(-6,u2),scale(12,mul(u,v))],
       [{},scale(-3,u2),scale(-6,u2),add(scale(3,mul(u2,add(h,one))),scale(-3,mul(v,um1))),scale(3,mul(v,um1))],
       [scale(-2,mul(u,v)),scale(-2,mul(u,v)),scale(12,mul(u,v)),scale(3,mul(v,um1)),scale(3,mul(u,add(mul(v,add(u,constant(3))),constant(-1))))]]
    n=add(constant(3),scale(3,h),mul(u,v))
    def upper(G,norms):
        return [[add(mul(n,D,norms[i]),scale(-1,G[i][j])) if i==j else scale(-1,G[i][j]) for j in range(3)] for i in range(3)]
    mats=dict(left=L,right=R,constant_active=K,left_upper_minus_I=upper(L,[constant(2),one,v]),right_upper_minus_I=upper(R,[constant(2),one,u]))
    other=dict(edge=add(mul(add(h,constant(3)),D),Z),edge_upper=add(mul(add(mul(u,v),scale(2,h)),D),scale(-1,Z)),
               trace=add(scale(3,mul(um1,add(u2,one),v2)),scale(-1,mul(add(scale(6,u3),scale(36,u2),scale(19,u),constant(-3)),v)),scale(-3,mul(u2,add(u,constant(3))))))
    return mats,other


def certificate_regime(name,u,v):
    matrices,other=build(u,v);data={};summary={}
    for label,M in matrices.items():
        data[label]=[];summary[label]=[]
        for n in range(1,len(M)+1):
            P=det([row[:n] for row in M[:n]])
            if P.get((0,0,0),0)<=0 or any(type(c) is not int or c<=0 for c in P.values()):
                raise ValueError('Nonpositive coefficient in '+name+':'+label+':'+str(n))
            data[label].append(records(P))
            summary[label].append(dict(terms=len(P),negative=sum(c<0 for c in P.values()),constant=P.get((0,0,0),0)))
    for label in ('edge','edge_upper'):
        P=other[label];data[label]=records(P)
        if P.get((0,0,0),0)<=0 or any(type(c) is not int or c<=0 for c in P.values()):
            raise ValueError('Nonpositive scalar coefficient in '+name+':'+label)
        summary[label]=dict(terms=len(P),negative=sum(c<0 for c in P.values()),constant=P.get((0,0,0),0))
    return dict(regime=name,summary=summary,coefficients=data)


def independent_clearing():
    pu=add(var(0),constant(2));pv=add(pu,var(1));u=RF(pu);v=RF(pv);h=u+v
    kL=2/(u-1);kR=2/(v-1);tL=2/v;tR=2/u;bL=-v/(u*u);bR=-1+1/v;bT=(u-1)/(u*u);qL=0;qR=RF(-1)/3
    pL=2-(u-1)*kL;pR=2-(v-1)*kR;bA=1-u*pL-v*pR
    qA=-(1+u*qL+v*qR)/(u*v)
    rL=1-v*tL-qL;rR=1-u*tR-qR
    wL=(v-v*tR)/(v*(u-1));wR=(u-u*tL)/(u*(v-1))
    qF=2-(u-1)*wL-(v-1)*wR-qA
    cL=-(u+qL+(u-1)*bL+v*(tL+bT))/(v*(u-1))
    cR=-(v+qR+(v-1)*bR+u*(tR+bT))/(u*(v-1))
    z=(qF-1-(u-1)*cL-(v-1)*cR)/((u-1)*(v-1))
    def leaf(q,k,b,w,c):
        return [[2*(h+1-k),RF(-2),-2*q*(1+w)],
                [RF(-2),h+1-b,-q*(1+c)],
                [-2*q*(1+w),-q*(1+c),q*(h+3+z-(1+z)*q)]]
    L=leaf(v,kL,bL,wL,cL);R=leaf(u,kR,bR,wR,cR)
    K=[[2*(h+1+bA),RF(-2),2*u*(pL-1),2*u*qL,2*v*qR],
       [RF(-2),h+1,-2*u,u*rL,v*rR],
       [2*u*(pL-1),-2*u,2*u*(h+1-u+(u-1)*kL),-2*u,2*u*v*tR],
       [2*u*qL,u*rL,-2*u,u*(h+1+(u-1)*bL),u*v*bT],
       [2*v*qR,v*rR,2*u*v*tR,u*v*bT,v*(h+1+(v-1)*bR)]]
    n=3+3*h+u*v
    def upper(G,norms):return [[n*norms[i]-G[i][j] if i==j else -G[i][j] for j in range(3)] for i in range(3)]
    raw=dict(left=L,right=R,constant_active=K,left_upper_minus_I=upper(L,[2,1,v]),right_upper_minus_I=upper(R,[2,1,u]))
    matrices,other=build(pu,pv);D=3*u*u*v*(u-1)*(v-1);count=0
    for name,M in matrices.items():
        d=3*u if name=='constant_active' else D
        for i,row in enumerate(M):
            for j,P in enumerate(row):
                if not RF(P)==d*raw[name][i][j]:raise ValueError('Clearing failed:'+name+':'+str((i,j)))
                count+=1
    if not RF(other['edge'])==D*(h+3+z):raise ValueError('Edge clearing failed')
    if not RF(other['edge_upper'])==D*(n-h-3-z):raise ValueError('Edge cap clearing failed')
    trace=5*u+4*v+15-v*(u-1)/(u*u)+(u+3)/v+19/(3*u)-1/(u*u)
    if not RF(other['trace'])==3*u*u*v*(n-trace):raise ValueError('Trace clearing failed')
    return count+3


def numeric_blocks(u,v,weights=None):
    w=cone.parameters(u,v) if weights is None else weights
    h=u+v
    def leaf(q,side):
        return [[2*(h+1-w['k'+side]),-2*(1+w['a'+side]),-2*q*(1+w['w'+side])],
                [-2*(1+w['a'+side]),h+1-w['b'+side],-q*(1+w['c'+side])],
                [-2*q*(1+w['w'+side]),-q*(1+w['c'+side]),q*(h+3+w['z']-(1+w['z'])*q)]]
    L=leaf(v,'L');R=leaf(u,'R')
    Kstd=[[h+1-w['bA'],-u*(1+w['pL'])],
          [-u*(1+w['pL']),u*(h+3+w['kL']-u*(1+w['kL']))]]
    Fstd=[[1,0],[0,1],[-1,-1]]
    Hstd=[[2*sum(F(Fstd[i][a])*Kstd[a][b]*Fstd[j][b] for a in range(2) for b in range(2)) for j in range(3)] for i in range(3)]
    K=[[2*(h+1+w['bA']),F(-2),2*u*(w['pL']-1),2*u*w['qL'],2*v*w['qR']],
       [F(-2),F(h+1),F(-2*u),u*w['rL'],v*w['rR']],
       [2*u*(w['pL']-1),F(-2*u),2*u*(h+1-u+(u-1)*w['kL']),2*u*(-1+(u-1)*w['aL']),2*u*v*w['tR']],
       [2*u*w['qL'],u*w['rL'],2*u*(-1+(u-1)*w['aL']),u*(h+1+(u-1)*w['bL']),u*v*w['bT']],
       [2*v*w['qR'],v*w['rR'],2*u*v*w['tR'],u*v*w['bT'],v*(h+1+(v-1)*w['bR'])]]
    Fc=[[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[-1,-2,-1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,1,0,-1,-1]]
    G=[[sum(F(Fc[i][a])*K[a][b]*Fc[j][b] for a in range(5) for b in range(5)) for j in range(7)] for i in range(7)]
    scalar=[h+3+w['kL'],h+3+w['kR'],h+3+w['z']]
    return L,R,Kstd,Hstd,K,G,list(map(F,(2,1,2*u,2*v,u,v,u*v))),scalar


def matrix_pivots(u,v,boundary=False):
    L,R,Kstd,Hstd,K,G,norms,scalars=numeric_blocks(u,v);N=4+3*(u+v)+u*v
    const=[[(N-1)*norms[i]*(i==j)-norms[i]*norms[j]-G[i][j] for j in range(7)] for i in range(7)]
    pv=pivots(const)
    if any(F(x)<=0 for x in pv[:-1]) or pv[-1]!='0':raise ValueError('Constant cap exception failed')
    result=dict(u=u,v=v,constant_upper_minus_I=pv)
    if boundary:
        matrices=dict(left=L,right=R,center_standard=Kstd,constant_active=K)
        matrices['left_upper_minus_I']=[[(N-1)*(2,1,v)[i]*(i==j)-L[i][j] for j in range(3)] for i in range(3)]
        matrices['right_upper_minus_I']=[[(N-1)*(2,1,u)[i]*(i==j)-R[i][j] for j in range(3)] for i in range(3)]
        matrices['center_standard_upper_minus_I']=[[(N-1)*(2,2*u,2*v)[i]*(i==j)-Hstd[i][j] for j in range(3)] for i in range(3)]
        result['pivots']={k:pivots(M) for k,M in matrices.items()}
        if any(F(x)<=0 for row in result['pivots'].values() for x in row):raise ValueError('Boundary block is not PD')
        if any(not 0<x<N-1 for x in scalars):raise ValueError('Boundary scalar/slack failed')
        result['scalars']=list(map(str,scalars))
    return result


def compact(rows):
    if any(row[2] for row in rows):raise ValueError('Unexpected third variable')
    return [[row[0],row[1],row[3]] for row in rows]


def rational_substitutions():
    pu=add(var(0),constant(2));pv=add(pu,var(1));matrices,_=build(pu,pv)
    inputs=[(2,5),(2,16),(2,20),(3,3),(3,10),(4,4),(4,8),(5,5),(5,6),(6,6),(7,13),(10,100),(100,10000)]
    checked=0
    for u,v in inputs:
        L,R,_,_,K,_,_,_=numeric_blocks(u,v);n=3+3*(u+v)+u*v
        def upper(G,norm):return [[n*norm[i]*(i==j)-G[i][j] for j in range(3)] for i in range(3)]
        raw=dict(left=L,right=R,constant_active=K,left_upper_minus_I=upper(L,(2,1,v)),right_upper_minus_I=upper(R,(2,1,u)))
        D=3*u*u*v*(u-1)*(v-1)
        for name,M in matrices.items():
            d=3*u if name=='constant_active' else D
            for i,row in enumerate(M):
                for j,P in enumerate(row):
                    if evaluate(P,u-2,v-u,0)!=d*raw[name][i][j]:raise ValueError('Rational entry substitution failed')
                    checked+=1
    return dict(parameters=[list(x) for x in inputs],entry_comparisons=checked)


def verify_certificate():
    fixture=dict(regimes={},constant_trace={},constant_cap_exceptions=[],boundary_cores=[]);counts={}
    for name,u,v in [('u_ge_3',add(var(0),constant(3)),None),('u2_v_ge_5',constant(2),add(var(1),constant(5)))]:
        if v is None:v=add(u,var(1))
        result=certificate_regime(name,u,v);fixture['regimes'][name]={}
        for key,rows in result['coefficients'].items():
            fixture['regimes'][name][key]=compact(rows) if key in ('edge','edge_upper') else [compact(p) for p in rows]
        counts[name]={k:[len(p) for p in rows] if k not in ('edge','edge_upper') else len(rows) for k,rows in fixture['regimes'][name].items()}
    for name,u,v in [('u_ge_6',add(var(0),constant(6)),None),('u2_v_ge_16',constant(2),add(var(0),constant(16))),('u3_v_ge_10',constant(3),add(var(0),constant(10))),('u4_v_ge_8',constant(4),add(var(0),constant(8))),('u5_v_ge_6',constant(5),add(var(0),constant(6)))]:
        if v is None:v=add(u,var(1))
        _,other=build(u,v);P=other['trace']
        if P.get((0,0,0),0)<=0 or any(type(c) is not int or c<=0 for c in P.values()):raise ValueError('Trace coefficient failed')
        fixture['constant_trace'][name]=compact(records(P))
    for u,vs in ((2,range(5,16)),(3,range(3,10)),(4,range(4,8)),(5,range(5,6))):
        for v in vs:fixture['constant_cap_exceptions'].append(matrix_pivots(u,v))
    for v in (2,3,4):fixture['boundary_cores'].append(matrix_pivots(2,v,True))
    summary=dict(cleared_polynomial_identities=independent_clearing(),positive_terms=counts,
                 trace_positive_terms={k:len(v) for k,v in fixture['constant_trace'].items()},
                 constant_cap_exceptions=23,boundary_cores=3,rational_substitutions=rational_substitutions())
    summary['canonical_certificate_sha256']=sha256(json.dumps(fixture,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return summary,fixture


if __name__=='__main__':
    summary,fixture=verify_certificate()
    print(json.dumps(dict(summary=summary,coefficient_certificate=fixture),sort_keys=True,indent=2))
