"""Exact positive coefficient certificates for 2<=u<=v bipartite cones."""
from pathlib import Path
from itertools import permutations
from fractions import Fraction as F
from hashlib import sha256
import json,sys
from dense_cone_polynomials import constant,var,add,scale,mul,records,evaluate
import bipartite_cones as cone


def det(M):
    answer={};n=len(M)
    for p in permutations(range(n)):
        sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        answer=add(answer,scale(sign,mul(*(M[i][p[i]] for i in range(n)))))
    return answer


def build(u,v):
    one=constant(1);um1=add(u,constant(-1));vm1=add(v,constant(-1));h=add(u,v)
    u2=mul(u,u);u3=mul(u2,u);hp1=add(h,one)
    dL=mul(u2,um1);dR=mul(u,v,vm1)
    L=[[mul(dL,hp1),scale(-1,dL),scale(-1,add(mul(u,v,add(u2,constant(-1))),u2))],
       [scale(-1,dL),mul(add(mul(u2,h),v),um1),scale(-1,mul(u2,add(mul(um1,v),scale(-1,u))))],
       [scale(-1,add(mul(u,v,add(u2,constant(-1))),u2)),scale(-1,mul(u2,add(mul(um1,v),scale(-1,u)))),
        add(mul(dL,v,add(u,constant(2))),scale(-1,u3),scale(-1,mul(add(scale(2,u),constant(-1)),v)))]]
    R=[[mul(dR,hp1),scale(-1,dR),scale(-1,mul(u,add(mul(u,add(mul(v,v),constant(-1))),v)))],
       [scale(-1,dR),mul(dR,hp1),mul(v,add(scale(-1,mul(u2,vm1)),scale(2,u),constant(-1)))],
       [scale(-1,mul(u,add(mul(u,add(mul(v,v),constant(-1))),v))),mul(v,add(scale(-1,mul(u2,vm1)),scale(2,u),constant(-1))),
        add(mul(u2,v,vm1,add(v,constant(2))),scale(-1,u3),scale(-1,mul(add(scale(2,u),constant(-1)),v)))]]
    K=[[mul(u,h),scale(-1,u2),{},{}],
       [scale(-1,u2),mul(u2,add(v,one)),scale(-1,u2),mul(u,v)],
       [{},scale(-1,u2),add(mul(u2,h),scale(-1,mul(v,um1))),mul(v,um1)],
       [{},mul(u,v),mul(v,um1),mul(u,v,add(u,one))]]
    Nminus1=add(constant(1),scale(2,h),mul(u,v))
    def buffer(G,clear,norm):
        return [[add(mul(Nminus1,clear,norm[i]),scale(-1,G[i][j])) if i==j else scale(-1,G[i][j]) for j in range(3)] for i in range(3)]
    UL=buffer(L,dL,[one,one,v]);UR=buffer(R,dR,[one,one,u])
    D=mul(u2,v,um1,vm1);znum=add(u3,mul(add(scale(2,u),constant(-1)),v))
    edge=add(mul(add(h,constant(2)),D),znum)
    edge_upper=add(mul(add(mul(u,v),h,constant(-1)),D),scale(-1,znum))
    trace=add(mul(u2,v,v,um1),mul(v,v,um1),scale(-1,mul(u2,v,add(scale(2,u),constant(4)))),scale(-1,u3),scale(-1,mul(v,add(scale(2,u),constant(-1)))))
    return dict(left=L,right=R,constant_active=K,left_upper_minus_I=UL,right_upper_minus_I=UR),dict(edge=edge,edge_upper=edge_upper,trace=trace)


def coefficient_certificate():
    u=add(var(0),constant(2));v=add(u,var(1));matrices,other=build(u,v)
    output={}
    for name,M in matrices.items():
        output[name]=[]
        for n in range(1,len(M)+1):
            P=det([row[:n] for row in M[:n]])
            if P.get((0,0,0),0)<=0 or any(c<=0 for c in P.values()):
                raise ValueError('Nonpositive coefficient:'+name+':'+str(n))
            output[name].append(records(P))
    for name in ('edge','edge_upper'):
        P=other[name]
        if P.get((0,0,0),0)<=0 or any(c<=0 for c in P.values()):raise ValueError('Edge sign failed:'+name)
        output[name]=records(P)
    ubig=add(var(0),constant(5));_,big=build(ubig,add(ubig,var(1)))
    P=big['trace']
    if P.get((0,0,0),0)<=0 or any(c<=0 for c in P.values()):raise ValueError('Large trace sign failed')
    output['trace_u_ge_5']=records(P)
    for low,threshold in ((2,8),(3,6),(4,5)):
        _,small=build(constant(low),add(var(0),constant(threshold)))
        P=small['trace']
        if P.get((0,0,0),0)<=0 or any(c<=0 for c in P.values()):raise ValueError('Small-u trace sign failed')
        output['trace_u'+str(low)+'_v_ge_'+str(threshold)]=records(P)
    return dict(agent='six-downset-1',role='researcher',status='Exact integer coefficient certificates; see BIPARTITE_CONES.md for decoding and completeness',
                variables='u=2+U,v=u+V; trace uses u=5+U or fixed u and v=threshold+U',coefficients=output)


class RationalPolynomial:
    """Exact rational functions, used only for independent clearing identities."""
    def __init__(self,num,den=None):
        self.num=num if isinstance(num,dict) else constant(num)
        if den is not None and not den:raise ValueError('Zero polynomial denominator')
        self.den=constant(1) if den is None or not self.num else den
        if not self.den:raise ValueError('Zero polynomial denominator')
    @staticmethod
    def convert(x):return x if isinstance(x,RationalPolynomial) else RationalPolynomial(x)
    def __add__(self,x):
        x=self.convert(x)
        return RationalPolynomial(add(mul(self.num,x.den),mul(x.num,self.den)),mul(self.den,x.den))
    __radd__=__add__
    def __neg__(self):return RationalPolynomial(scale(-1,self.num),self.den)
    def __sub__(self,x):return self+-self.convert(x)
    def __rsub__(self,x):return self.convert(x)+-self
    def __mul__(self,x):
        x=self.convert(x)
        return RationalPolynomial(mul(self.num,x.num),mul(self.den,x.den))
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.convert(x)
        if not x.num:raise ValueError('Zero rational polynomial divisor')
        return RationalPolynomial(mul(self.num,x.den),mul(self.den,x.num))
    def __rtruediv__(self,x):return self.convert(x)/self
    def __eq__(self,x):
        x=self.convert(x)
        return mul(self.num,x.den)==mul(x.num,self.den)


def clearing_identities():
    pu=add(var(0),constant(2));pv=add(pu,var(1))
    u=RationalPolynomial(pu);v=RationalPolynomial(pv);h=u+v
    # Derive the weights from the seven-parameter row/star equations,
    # independently of the hand-cleared polynomial entries in build().
    aL=aR=0;tL=1/v;tR=1/u;bL=-v/(u*u);bR=-1;bT=(u-1)/(u*u)
    pL=1-(u-1)*aL-v*tL;pR=1-(v-1)*aR-u*tR
    wL=(v+1-(u-1)*aL-v*tR)/(v*(u-1))
    wR=(u+1-(v-1)*aR-u*tL)/(u*(v-1))
    cL=-(u+(u-1)*bL+v*bT)/(v*(u-1))
    cR=-(v+(v-1)*bR+u*bT)/(u*(v-1))
    z=-cL/(v-1)-cR/(u-1)
    def gram(q,a,b,w,c):
        return [[h+1,-1-a,-q*(1+w)],[-1-a,h-b,-q*(1+c)],
                [-q*(1+w),-q*(1+c),q*(h+2+z-(1+z)*q)]]
    L=gram(v,aL,bL,wL,cL);R=gram(u,aR,bR,wR,cR)
    K=[[h,-u,u*pL,v*pR],[-u,u*(v+1),-u,u*v*tR],
       [u*pL,-u,u*(h+(u-1)*bL),u*v*bT],
       [v*pR,u*v*tR,u*v*bT,v*(h+(v-1)*bR)]]
    n=1+2*h+u*v
    def buffer(G,q):return [[n*(q if i==2 else 1)-G[i][j] if i==j else -G[i][j] for j in range(3)] for i in range(3)]
    literal=dict(left=L,right=R,constant_active=K,left_upper_minus_I=buffer(L,v),right_upper_minus_I=buffer(R,u))
    clear=dict(left=u*u*(u-1),right=u*v*(v-1),constant_active=u,
               left_upper_minus_I=u*u*(u-1),right_upper_minus_I=u*v*(v-1))
    matrices,other=build(pu,pv);checked=0
    for name,M in matrices.items():
        for i,row in enumerate(M):
            for j,entry in enumerate(row):
                if not RationalPolynomial(entry)==clear[name]*literal[name][i][j]:
                    raise ValueError('Cleared entry identity failed:'+name+':'+str((i,j)))
                checked+=1
    D=u*u*v*(u-1)*(v-1)
    if not RationalPolynomial(other['edge'])==D*(h+2+z):raise ValueError('Edge identity failed')
    if not RationalPolynomial(other['edge_upper'])==D*(u*v+h-1-z):raise ValueError('Edge cap identity failed')
    trace=4*u+3*v+5-v*(u-1)/(u*u)+u/v+(2*u-1)/(u*u)
    if not RationalPolynomial(other['trace'])==u*u*v*(n-trace):raise ValueError('Trace clearing identity failed')
    return checked+3


def numeric_blocks(u,v):
    w=cone.parameters(u,v);h=u+v
    def gram(q,part):
        return [[F(h+1),-1-w['a'+part],-q*(1+w['w'+part])],
                [-1-w['a'+part],h-w['b'+part],-q*(1+w['c'+part])],
                [-q*(1+w['w'+part]),-q*(1+w['c'+part]),q*(h+2+w['z']-(1+w['z'])*q)]]
    L=gram(v,'L');R=gram(u,'R')
    K=[[F(h),F(-u),u*w['pL'],v*w['pR']],
       [F(-u),F(u*(v+1)),u*(-1+(u-1)*w['aL']),u*v*w['tR']],
       [u*w['pL'],u*(-1+(u-1)*w['aL']),u*(h+(u-1)*w['bL']),u*v*w['bT']],
       [v*w['pR'],u*v*w['tR'],u*v*w['bT'],v*(h+(v-1)*w['bR'])]]
    factor=[[1,0,0,0],[0,1,0,0],[-1,-1,0,0],[0,0,1,0],[0,0,0,1],[0,0,-1,-1]]
    G=[[sum(F(factor[i][a])*K[a][b]*factor[j][b] for a in range(4) for b in range(4)) for j in range(6)] for i in range(6)]
    return L,R,K,G,list(map(F,(1,u,v,u,v,u*v)))


def pivots(A):
    a=[[F(x) for x in row] for row in A];answer=[]
    for k in range(len(a)):
        p=a[k][k];answer.append(str(p))
        if p<0 or (not p and any(a[k][j] for j in range(k+1,len(a)))):raise ValueError('Non-PSD small buffer')
        if not p:continue
        for i in range(k+1,len(a)):
            for j in range(i,len(a)):
                a[i][j]-=a[i][k]*a[j][k]/p;a[j][i]=a[i][j]
    return answer


def small_constant_certificates():
    answer=[]
    for u,vs in ((2,range(2,8)),(3,range(3,6)),(4,range(4,5))):
        for v in vs:
            _,_,_,G,norms=numeric_blocks(u,v);n=1+2*(u+v)+u*v
            U=[[(n*norms[i] if i==j else 0)-norms[i]*norms[j]-G[i][j] for j in range(6)] for i in range(6)]
            diagonal=pivots(U)
            if diagonal[-1]!='0' or any(F(p)<=0 for p in diagonal[:-1]):raise ValueError('Unexpected small-buffer rank')
            answer.append(dict(u=u,v=v,pivots=diagonal))
    return answer


def rational_substitutions():
    u=add(var(0),constant(2));v=add(u,var(1));matrices,_=build(u,v)
    inputs=[(2,2),(2,8),(2,20),(3,3),(3,6),(3,9),(4,4),(4,5),(5,5),(6,11),(10,10),(20,100),(100,10000)]
    checked=0
    for u,v in inputs:
        L,R,K,_,_=numeric_blocks(u,v);n=1+2*(u+v)+u*v
        buffer=lambda G,q:[[(n*(q if i==2 else 1) if i==j else 0)-G[i][j] for j in range(3)] for i in range(3)]
        literal=dict(left=L,right=R,constant_active=K,left_upper_minus_I=buffer(L,v),right_upper_minus_I=buffer(R,u))
        factors=dict(left=u*u*(u-1),right=u*v*(v-1),constant_active=u,left_upper_minus_I=u*u*(u-1),right_upper_minus_I=u*v*(v-1))
        for name,M in matrices.items():
            G=literal[name];clear=factors[name]
            for i,row in enumerate(M):
                for j,P in enumerate(row):
                    if evaluate(P,u-2,v-u,0)!=clear*G[i][j]:raise ValueError('Rational entry comparison failed')
                    checked+=1
    return dict(parameters=[list(x) for x in inputs],entry_comparisons=checked)


def verify_certificate():
    data=coefficient_certificate();raw=data['coefficients']
    blocks=('left','right','constant_active','left_upper_minus_I','right_upper_minus_I')
    def compact(rows):
        if any(r[2] for r in rows):raise ValueError('Unexpected third variable')
        return [[r[0],r[1],r[3]] for r in rows]
    fixture={k:[compact(p) for p in rows] if k in blocks else compact(rows) for k,rows in raw.items()}
    fixture['small_constant_buffers']=small_constant_certificates()
    summary=dict(cleared_polynomial_identities=clearing_identities(),rational_substitutions=rational_substitutions(),
                 positive_coefficient_terms={k:[len(p) for p in rows] if k in blocks else len(rows) for k,rows in raw.items()},
                 small_constant_cases=len(fixture['small_constant_buffers']))
    summary['canonical_certificate_sha256']=sha256(json.dumps(fixture,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return summary,fixture


if __name__=='__main__':
    summary,fixture=verify_certificate()
    print(json.dumps(dict(summary=summary,coefficient_certificate=fixture),sort_keys=True,indent=2))
