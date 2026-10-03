"""PRIVATE independent univariate rational field and balanced n2 physical forms.

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
    # Separate simplified scalar formulas and closed aggregate physical frames.
    if type(h) is int:h=F(h)
    s=3*h+2;N=12*h+4;ell=6*h+1
    a=9*h*h/(ell*s*(h-1));b=-2*a;c=27*h/(ell*s)
    mu=h-F(1,3)-(3*h+1)/(ell*ell)-162*h*h/(ell*ell*s*(h-1))
    alpha=2*s*(1-2*(2*h-3)*c*c/(3*(h-1)))
    beta=2*s/3-108*h*h*(h+3)/(ell*ell*s*(h-1))
    nu=2*h*mu/(2*h-1)
    grams={};frames={}
    G=zero(2);G[0][0]=2*s;G[1][1]=alpha
    S=[[2*s*s*(1+c*c),-s*c*alpha],[-s*c*alpha,alpha*alpha/2]]
    grams['anti']=G;frames['anti']=S
    G=zero(4)
    for i,z in enumerate((2*s/3,12*s,2*beta,2*nu)):G[i][i]=z
    S=zero(4)
    for row,mult in [([s/3,s,0,0],4),([s/3,-2*s,0,0],2),([a*s/3,c*s,-beta/2,nu],4),([b*s/3,2*c*s/(h-1),beta,nu],2)]:
        for i in range(4):
            for j in range(4):S[i][j]+=mult*row[i]*row[j]
    grams['standard']=G;frames['standard']=S
    G=zero(4)
    for i,z in enumerate((F(1),3*h,12*h*s,2*h*beta)):G[i][i]=z
    S=zero(4);S[0][0]=3+1/ell;S[0][1]=S[1][0]=3*h*(1+1/ell)
    S[1][1]=9*h*h+6*h+9*h*h/ell
    S[2][2]=12*h*s*s*(1+c*c);S[2][3]=S[3][2]=-6*h*c*s*beta;S[3][3]=3*h*beta*beta
    grams['fixed-even']=G;frames['fixed-even']=S
    G=zero(4)
    for i,z in enumerate((3*h,12*h*s,2*h*beta,2*h*nu)):G[i][i]=z
    S=zero(4);S[0][0]=18*h*h+6*h
    S[1][1]=12*h*s*s*(1+c*c);S[1][2]=S[2][1]=-6*h*c*s*beta;S[2][2]=3*h*beta*beta;S[3][3]=6*h*nu*nu
    grams['fixed-odd']=G;frames['fixed-odd']=S
    caps={name:[[(N-1)*G[i][j]-frames[name][i][j] for j in range(len(G))] for i in range(len(G))] for name,G in grams.items()}
    return dict(alpha=[[alpha]],beta=[[beta]],mu=[[mu]])|caps
