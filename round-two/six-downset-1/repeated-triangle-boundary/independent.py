"""PRIVATE independent univariate rational field and q2 physical forms.

Standard library only. Imports no producer, factored polynomial engine,
recipe, model or sector module. The geometric interpretation is ordinary
unformalized mathematics, not a proof assistant or external review.
"""
from fractions import Fraction as F
from functools import lru_cache

def require(ok,msg):
    if not ok:raise ValueError(msg)

def poly(a):
    a=list(map(F,a))
    while a and not a[-1]:a.pop()
    require(len(a)<=512,'unchanged512 coefficient guard')
    return tuple(a)

def padd(a,b):return poly([(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0)) for i in range(max(len(a),len(b)))])
def pneg(a):return tuple(-z for z in a)
def psub(a,b):return padd(a,pneg(b))
def pmul(a,b):
    if not a or not b:return ()
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return poly(out)
def pdiv(a,b):
    require(bool(b),'nonzero independent divisor')
    a=list(a);out=[F(0)]*max(0,len(a)-len(b)+1)
    while a and len(a)>=len(b):
        k=len(a)-len(b);v=a[-1]/b[-1];out[k]+=v
        for j,z in enumerate(b):a[k+j]-=v*z
        while a and not a[-1]:a.pop()
    return poly(out),poly(a)
def pquot(a,b):
    q,r=pdiv(a,b);require(not r,'independent exact polynomial division');return q
@lru_cache(maxsize=8192)
def pgcd(a,b):
    while b:a,b=b,pdiv(a,b)[1]
    return tuple(z/a[-1] for z in a) if a else ()
def pvalue(a,h):
    value=F(0)
    for z in reversed(a):value=value*h+z
    return value

class Rat:
    def __init__(self,num=0,den=(F(1),)):
        if isinstance(num,Rat):self.num,self.den=num.num,num.den;return
        if not isinstance(num,(tuple,list)):num=(F(num),)
        num,den=poly(num),poly(den);require(bool(den),'nonzero rational field denominator')
        if not num:self.num,self.den=(),(F(1),);return
        if len(den)>1 and len(num)>1:
            g=pgcd(num,den)
            if len(g)>1:num,den=pquot(num,g),pquot(den,g)
        lead=den[-1];self.num=tuple(z/lead for z in num);self.den=tuple(z/lead for z in den)
    def __bool__(self):return bool(self.num)
    def __neg__(self):return Rat(pneg(self.num),self.den)
    def __add__(self,b):
        b=Rat(b)
        if self.den==b.den:return Rat(padd(self.num,b.num),self.den)
        common=pgcd(self.den,b.den);x=pquot(self.den,common);y=pquot(b.den,common)
        return Rat(padd(pmul(self.num,y),pmul(b.num,x)),pmul(self.den,y))
    __radd__=__add__
    def __sub__(self,b):return self+-Rat(b)
    def __rsub__(self,b):return Rat(b)+-self
    def __mul__(self,b):
        b=Rat(b)
        if not self or not b:return Rat(0)
        g=pgcd(self.num,b.den);v=pgcd(b.num,self.den)
        return Rat(pmul(pquot(self.num,g),pquot(b.num,v)),pmul(pquot(self.den,v),pquot(b.den,g)))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=Rat(b);require(bool(b),'nonzero exact rational divisor');return self*Rat(b.den,b.num)
    def __rtruediv__(self,b):return Rat(b)/self
    def __pow__(self,n):
        require(type(n) is int and n>=0,'nonnegative rational exponent');out=Rat(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,b):
        b=Rat(b);return pmul(self.num,b.den)==pmul(b.num,self.den)
    def value(self,h):return pvalue(self.num,h)/pvalue(self.den,h)

def zero(n):return [[F(0) for j in range(n)] for i in range(n)]
def e(n,i):return [F(i==j) for j in range(n)]
def add(*rows):return [sum(values,F(0)) for values in zip(*rows)]
def scale(a,row):return [a*z for z in row]
def mv(A,row):return [sum((a*b for a,b in zip(values,row)),F(0)) for values in A]

def forms(h):
    """Direct q2 formulas, valid in QQ[h] or exact Fraction h>=2.

    In the fixed9 coordinates Ay=-Ax is substituted into every physical
    row before computing its pairings; this is not deletion of row data.
    """
    if type(h) is int:h=F(h)
    s=3*h+2;w=3*h+1;N=6*h+10;ell=3*h+4;d=3*h-2;t=3*h-1
    rho=1/d;E2=2/(3*h)+t/(3*d*d);c0=(12*h-8)/(ell*ell)
    FF=-6*d/(ell*t);A=-3*d/(h*ell*t);ccL=24/(ell*s)
    b=-9*h*(h+1)/(ell*s*(h-1));a=-b/2
    ccH=27*(h+1)/(2*ell*s)-6*d/(h*h*ell*t*s)
    B2=s*(h-1)/(3*h)
    etaHL=w-c0-A*A*E2-a*a*B2-2*s*ccH*ccH/3
    etaHF=w-c0-b*b*B2-2*s*ccH*ccH/(3*(h-1))-2*s*ccL*ccL/(3*h*h)
    etaLL=w-c0-FF*FF*E2-2*s*ccL*ccL/3;etaLF=w-c0-9*FF*FF*E2
    pairH=-1-c0-a*b*B2;pairL=-1-c0+3*FF*FF*E2
    muH=(2*pairH+etaHF)/3;muL=(2*pairL+etaLF)/3
    alphaH=2*(2*etaHL-pairH-etaHF);betaH=etaHF-muH
    alphaL=2*(2*etaLL-pairL-etaLF);betaL=etaLF-muL
    nu=(h*muH-muL/h)/(h-1)
    scalars=dict(alphaH=alphaH,betaH=betaH,alphaL=alphaL,betaL=betaL,nu=nu,muL=muL)
    grams={};frames={}
    for name,cc,alpha in [('antiH',ccH,alphaH),('antiL',ccL,alphaL)]:
        grams[name]=[[2*s,F(0)],[F(0),alpha]]
        frames[name]=[[2*s*s*(1+cc*cc),-s*cc*alpha],[-s*cc*alpha,alpha*alpha/2]]
    G=zero(4)
    for i,z in enumerate([2*s/3,12*s,2*nu,2*betaH]):G[i][i]=z
    S=zero(4)
    for row,m in [([s/3,s,0,0],4),([s/3,-2*s,0,0],2),([a*s/3,ccH*s,nu,-betaH/2],4),([b*s/3,2*s*ccH/(h-1),nu,betaH],2)]:
        for i in range(4):
            for j in range(4):S[i][j]+=m*row[i]*row[j]
    grams['standard']=G;frames['standard']=S
    G=zero(9)
    for i,z in enumerate([F(1),3*h,3*h,6*h*s,s*(h-1)/(3*h),6*s,h*betaH,betaL,muL]):G[i][i]=z
    unit=lambda i:e(9,i)
    hx=scale(1/(3*h),add(unit(1),unit(2)));hy=scale(1/(3*h),add(unit(1),scale(-1,unit(2))))
    vl=add(hy,unit(4));E=add(hx,scale(-rho,vl))
    K=add(unit(0),scale(-1,unit(1)),scale(3*h,hx),scale(3,hy),scale(3,unit(4)))
    common=scale(-1/ell,K)
    vhL=add(hx,scale(1/(6*h),unit(3)));vhF=add(hx,scale(-1/(3*h),unit(3)))
    vlL=add(vl,scale(F(1,6),unit(5)));vlF=add(vl,scale(F(-1,3),unit(5)))
    uhL=add(common,scale(A,E),scale(ccH/(6*h),unit(3)),scale(-1/(2*h),unit(6)),scale(1/h,unit(8)))
    uhF=add(common,scale(-ccH/(3*h),unit(3)),scale(-ccL/(3*h),unit(5)),scale(1/h,unit(6)),scale(1/h,unit(8)))
    ulL=add(common,scale(FF,E),scale(ccL/6,unit(5)),scale(F(-1,2),unit(7)),scale(-1,unit(8)))
    ulF=add(common,scale(-3*FF,E),unit(7),scale(-1,unit(8)))
    S=zero(9);S[0][0]=3;S[1][1]=9*h*h;S[0][1]=S[1][0]=3*h;S[2][2]=18*h*h
    for row,m in [(vhL,2*h),(vhF,h),(vlL,2),(vlF,1),(uhL,2*h),(uhF,h),(ulL,2),(ulF,1),(common,1)]:
        x=mv(G,row)
        for i in range(9):
            for j in range(9):S[i][j]+=m*x[i]*x[j]
    grams['fixed']=G;frames['fixed']=S
    caps={name:[[(N-1)*G[i][j]-frames[name][i][j] for j in range(len(G))] for i in range(len(G))] for name,G in grams.items()}
    return {name:[[z]] for name,z in scalars.items()}|caps
