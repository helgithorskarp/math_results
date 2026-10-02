"""Explicit two-test certificate for every integer n>=11.

The unbounded real proof is PROOF.md, not a finite enumeration. All values
below are exact rationals. No solver, eigenvalue calculation or input corpus.
"""
from fractions import Fraction as Q
from math import comb
from model import parameters,require

def profile(n):
    parameters(n)
    v={a:max(Q(0),Q(5,4)-Q((2*a-n)**2,4*n)) for a in range(3,n-2)}
    mu=Q((2*n-5)**2,16)
    f={a:Q(a)-v[a] for a in v}
    k={a:mu-f[a]*f[n-a] for a in v}
    require(all(k[a]>=0 for a in k),'Nonnegative complement multipliers')
    require(all(f[a]>0 for a in f),'Positive f')
    require(all(f[a]<f[a+1] for a in range(3,n-3)),'Strictly increasing f')
    return v,mu,f,k

def tests(n):
    N,s,h=parameters(n);v,mu,f,k=profile(n);aa=list(range(1,n-1))
    lower=[Q(0) if a in (1,2) else Q(2) if a==n-2 else Q(1) for a in aa]
    upper=[Q(1) if a==1 else Q(2) if a==2 else Q(2*s,h) if a==n-2 else v[a] for a in aa]
    return aa,lower,upper,mu

def pair_count(n,a,b):
    require(1<=a<=b<=n-2 and a+b<=n,'Unordered disjoint original class')
    return comb(n,a)*comb(n-a,b)//(2 if a==b else 1)

def weights(n):
    v,mu,f,k=profile(n)
    out={}
    for a in range(3,n-2):
        for b in range(a,n-2):
            if a+b<n:
                rho=1-f[a]*f[b]/mu
                require(0<rho<1,'Strictly positive original normalized weight')
                out[a,b]=rho
    return out

def constant(n):
    N,s,h=parameters(n);q=comb(n,2);v,mu,f,k=profile(n);r=Q(2*s,h)
    S=sum(comb(n,a)*v[a]**2 for a in v)
    C=n*h+q*(h*(4+r*r)-s*(2+4*r))+(n-1)*S
    eta=C+mu*(4*s-4)
    return {'n':n,'N':N,'s':s,'h':h,'q':q,'mu':mu,'r':r,'bulk_norm2':S,
            'upper_constant':C,'eta':eta,'positive_mass_floor':-eta/(2*h*mu)}

def moment_bound(n):
    N,s,h=parameters(n)
    return (s+n)*(Q(9,4)-Q(1,4*n))

def tail_bound(n):
    N,s,h=parameters(n)
    return s*(-Q(3*n,4)+Q(15,4)+Q(1,4*n))+4*n**3-Q(23*n*n,4)+Q(11*n,2)-6

def identity_rhs(n,B):
    """Full star-only invariant face; all proper >=3 pairs retained."""
    rec=constant(n);s=rec['s'];h=rec['h'];v,mu,f,k=profile(n)
    deficit=sum(comb(n,a)*k[a]*(s-B[a][n-a]) for a in v)
    omitted=sum(2*pair_count(n,a,b)*rho*B[a][b]*mu
                for (a,b),rho in weights(n).items())
    return rec['eta']-deficit+omitted
