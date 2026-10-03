"""Exact QQ(h) balanced triangle recipe at the fixed old cube q=4.

The ordinary old-cube Gram is credited to9361. This private adaptation
addresses its additional upper cap, not new ordinary rank attainment.
"""
from fractions import Fraction as F
from exact import require

def recipe(h):
    if type(h) is int:h=F(h)
    require(not isinstance(h,float),'exact parameter')
    s=3*h+4;w=s-1;N=12*h+8;ell=6*h+1;B2=s*(h-1)/(3*h)
    a=3*h*(3*h-1)/(ell*s*(h-1));b=-2*a;c=9*(3*h-1)/(ell*s)
    common=(3+15*h)/(ell*ell)
    etaL=w-common-a*a*B2-2*s*c*c/3
    etaF=w-common-b*b*B2-2*s*c*c/(3*(h-1))
    pair=-1-common-a*b*B2
    mu=(2*pair+etaF)/3;alpha=2*(2*etaL-pair-etaF);beta=etaF-mu;nu=2*h*mu/(2*h-1)
    require(2*a+b==0,'facet-mean B cancellation')
    require(-3/ell+a*B2-c*s/3==-1,'both private leaf support identities')
    require(-3/ell+b*B2==-1,'all three private full support identities')
    require(mu+alpha/4+beta/4==etaL and mu+beta==etaF and mu-beta/2==pair,'all original W within-facet constraints')
    return dict(h=h,s=s,w=w,N=N,ell=ell,B2=B2,a=a,b=b,c=c,common=common,etaL=etaL,etaF=etaF,pair=pair,mu=mu,alpha=alpha,beta=beta,nu=nu)
