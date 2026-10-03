"""PRIVATE exact QQ(q,h) balanced recipe; no all-q cap theorem assumed."""
from fractions import Fraction as F
from exact import require

def recipe(q,h):
    if type(q) is int:q=F(q)
    if type(h) is int:h=F(h)
    require(not isinstance(q,float) and not isinstance(h,float),'exact parameters')
    D=3*h;s=q+D;w=s-1;N=2*q+12*h;ell=6*h+1;B2=s*(h-1)/(3*h)
    a=3*h*(ell-q+1)/(2*ell*s*(h-1));b=-2*a;c=9*(ell-q+1)/(2*ell*s)
    common=(q-1+(2*q-3)*D)/(ell*ell)
    etaL=w-common-a*a*B2-2*s*c*c/3
    etaF=w-common-b*b*B2-2*s*c*c/(3*(h-1))
    pair=-1-common-a*b*B2
    mu=(2*pair+etaF)/3;alpha=2*(2*etaL-pair-etaF);beta=etaF-mu;nu=2*h*mu/(2*h-1)
    require(2*a+b==0,'facet-mean B cancellation')
    require(-(q-1)/ell+a*B2-c*s/3==-1,'both private leaf support identities')
    require(-(q-1)/ell+b*B2==-1,'all private full support identities')
    require(mu+alpha/4+beta/4==etaL and mu+beta==etaF and mu-beta/2==pair,'all within-facet W constraints')
    return dict(q=q,h=h,D=D,s=s,w=w,N=N,ell=ell,B2=B2,a=a,b=b,c=c,common=common,etaL=etaL,etaF=etaF,pair=pair,mu=mu,alpha=alpha,beta=beta,nu=nu)
