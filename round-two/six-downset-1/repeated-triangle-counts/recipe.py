"""Exact original rational recipe for h heavy triangles and one light."""
from fractions import Fraction as F

def require(p,msg):
 if not p:raise ValueError(msg)

def recipe(h,q):
 if type(h) is int:h=F(h)
 if type(q) is int:q=F(q)
 require(not isinstance(h,float) and not isinstance(q,float),'exact parameter types')
 s=q+3*h;w=s-1;N=2*q+6*h+6;ell=3*h+4
 rho=(q-1)/(q+3*h-4);E2=q/(3*h)+rho*rho*(q+3*h-3)/3
 common=(ell*q+6*h-16)/(ell*ell)
 FF=(q-8)/(ell*rho*(q+3*h-3));G=-3*FF;A=FF/(2*h)
 cL=-4*(q-8)/(ell*s);b=3*h*(q-ell-1)/(ell*s*(h-1));a=-b/2
 cH=-9*(q-ell-1)/(2*ell*s)+A*q/(h*s);B2=s*(h-1)/(3*h)
 etaHL=w-common-A*A*E2-a*a*B2-2*s*cH*cH/3
 etaHF=w-common-b*b*B2-2*s*cH*cH/(3*(h-1))-2*s*cL*cL/(3*h*h)
 etaLL=w-common-FF*FF*E2-2*s*cL*cL/3;etaLF=w-common-9*FF*FF*E2
 pairH=-1-common-a*b*B2;pairL=-1-common+3*FF*FF*E2
 muH=(2*pairH+etaHF)/3;muL=(2*pairL+etaLF)/3
 alphaH=2*(2*etaHL-pairH-etaHF);betaH=etaHF-muH
 alphaL=2*(2*etaLL-pairL-etaLF);betaL=etaLF-muL
 nu=(h*muH-muL/h)/(h-1)
 require(2*h*A+2*FF+G==0 and 2*a+b==0,'whole projection E/B balance')
 require(-(q-1)/ell+(A*q+a*s*(h-1)-h*cH*s)/(3*h)==-1,'heavy private leaf support')
 require(-(q-1)/ell+b*B2==-1,'heavy private full support')
 require(-(q+3*h-4)/ell-FF*rho*(q+3*h-3)/3-cL*s/3==-1,'light private leaf support')
 require(-(q+3*h-4)/ell-G*rho*(q+3*h-3)/3==-1,'light private full support')
 return locals()
