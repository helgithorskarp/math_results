"""General-k original two-test certificate; stdlib exact arithmetic only.

Credits:9424 supplies the clipped profile and k2 mechanism;9201/9245 supply
the earlier CENTERED near-middle scope. PROOF.md supplies all-order bridges.
"""
from fractions import Fraction as Q
from math import comb
from model import parameters,require

def domain(n,k):
    parameters(n)
    require(type(k) is int and 2<=k<=(n-2)//2,'Disjoint low/bulk/high domain')

def profile(n,k):
    domain(n,k)
    v={a:max(Q(0),Q(5,4)-Q((2*a-n)**2,4*n)) for a in range(k+1,n-k)}
    mu=Q((2*n-5)**2,16)
    f={a:Q(a)-v[a] for a in v}
    deficit={a:mu-f[a]*f[n-a] for a in v}
    require(all(deficit[a]>=0 and f[a]>0 for a in v),'Complement/positive signs')
    require(all(f[a]<f[a+1] for a in range(k+1,n-k-1)),'Monotone f')
    return v,mu,f,deficit

def tests(n,k):
    domain(n,k);N,s,h=parameters(n);v,mu,f,deficit=profile(n,k);aa=list(range(1,n-1))
    lower=[Q(0) if a<=k else Q(2) if a>=n-k else Q(1) for a in aa]
    upper=[Q(a) if a<=k else Q(s*(n-a),h) if a>=n-k else v[a] for a in aa]
    return aa,lower,upper,mu

def pair_count(n,a,b):
    require(1<=a<=b<=n-2 and a+b<=n,'Unordered disjoint original class')
    return comb(n,a)*comb(n-a,b)//(2 if a==b else 1)

def weights(n,k):
    v,mu,f,deficit=profile(n,k);out={}
    for a in v:
        for b in range(a,n-k):
            if a+b<n:
                rho=1-f[a]*f[b]/mu
                require(0<rho<1,'Strict positive original normalized weight')
                out[a,b]=rho
    return out

def constant(n,k):
    domain(n,k);N,s,h=parameters(n);q=comb(n,2);v,mu,f,deficit=profile(n,k)
    tail=sum(a*a*comb(n,a) for a in range(3,k+1))
    A=4*q+tail;S=sum(comb(n,a)*v[a]**2 for a in v)
    C=n*h-2*q*s+(Q(h)-Q(s*s,h))*A+(n-1)*S
    eta=C+mu*(4*s-4)
    return {'n':n,'k':k,'N':N,'s':s,'h':h,'mu':mu,'weighted_tail':tail,
            'low_squared_moment':A,'bulk_norm2':S,'upper_constant':C,
            'eta':eta,'positive_mass_floor':-eta/(2*h*mu)}

def tail_condition(n,k):
    domain(n,k);N,s,h=parameters(n)
    B=sum(a*a*comb(n,a) for a in range(3,k+1));D=s-12*n*n
    return {'B':B,'D':D,'holds':n>=12 and 6*B<=D}

def certified_cutoff(n):
    """Greatest k certified by this sufficient scalar criterion, not optimality."""
    N,s,h=parameters(n);require(n>=12,'Positive sufficient-tail domain')
    B=0;best=2
    for k in range(3,(n-2)//2+1):
        B+=k*k*comb(n,k)
        if 6*B>s-12*n*n:break
        best=k
    return best

def identity_rhs(n,k,B):
    rec=constant(n,k);s=rec['s'];v,mu,f,deficit=profile(n,k)
    Z=sum(comb(n,a)*deficit[a]*(s-B[a][n-a]) for a in v)
    omitted=sum(2*pair_count(n,a,b)*mu*rho*B[a][b] for (a,b),rho in weights(n,k).items())
    return rec['eta']-Z+omitted

def k2_tail_bound(n):
    N,s,h=parameters(n)
    return s*(-Q(3*n,4)+Q(15,4)+Q(1,4*n))+4*n**3-Q(23*n*n,4)+Q(11*n,2)-6
