"""Exact adaptive sufficient region; matrix allocation is a separate API."""
import bootstrap
from fractions import Fraction as F
from math import isqrt
from exact import require


def minimum_q(k):
    require(type(k) is int and k>=1,'literal integer k>=1 required')
    return max(4,(6*k-7+isqrt(28*k*k-36*k+17))//2+1)


def frontier(q,k):
    require(type(q) is int and type(k) is int and q>=4 and 1<=k<=q,
            'literal integer q>=4, 1<=k<=q required')
    N=(q*q+13*q+16)//2-k;s=3*q+4
    B0=F(q*q+(7-6*k)*q+2*k*k-12*k+8,2)
    require(B0==N-(k+1)*s+k*(k-1),'frontier polynomial identity')
    require((B0>0)==(q>=minimum_q(k)),'exact integer frontier cutoff')
    return N,s,B0


def parameters(q,k):
    N,s,B0=frontier(q,k)
    require(B0>0,'B0>0 sufficient premise fails; no H conclusion')
    g=N-2*s;h=F(1,3*q+5)
    alpha=F(q*(q+1),2)+3*(q+1)*h
    B=N-s-k
    D=2*k*g*(1-h)+(alpha-2*k+2)*B
    E=k*g*(1-h)**2+(alpha-k+1)*B
    require(min(g,B,D,E)>0,'positive denominator premises')
    # Corroborates the written unbounded strict-monotonicity argument.
    identity=k*g*(1-h)*(2-(1-h)/4)+(3*alpha-7*(k-1))*B/4
    require(D-E/4==identity and identity>0 and N>=38,'scalar monotonicity premises')
    kappa=min(F(1,8),N*B0/(2*D))
    chi=k*g*(N-kappa+kappa*h)**2-((k-1)*(N-kappa)+kappa*alpha)*(N-kappa)*B
    require(chi==N*N*B0-kappa*N*D+kappa*kappa*E,'exact chi expansion')
    require(chi>=N*N*B0/2>0,'adaptive positive chi bound')
    gamma=g*chi/(N*(N-kappa)**2*B)
    return {'q':q,'k':k,'N':N,'s':s,'g':g,'B0':B0,'h':h,'alpha':alpha,
            'D':D,'E':E,'kappa':kappa,'chi':chi,'gamma':gamma,
            'tau':min(kappa/24,gamma/4),'minimum_q':minimum_q(k)}


def record(q,k):
    return {key:str(value) if isinstance(value,F) else value
            for key,value in parameters(q,k).items()}


def checks():
    samples=[record(q,k) for q,k in ((4,1),(7,2),(12,3),(18,4),(24,5),(29,6),(600,100),(1000000,100000))]
    valid=0;prior=0
    for q in range(4,81):
        for k in range(1,q+1):
            N,s,B0=frontier(q,k)
            if B0>0:parameters(q,k);valid+=1
            g=N-2*s;h=F(1,3*q+5);alpha=F(q*(q+1),2)+3*(q+1)*h
            chi_old=k*g*(N-F(1,2)+h/2)**2-((k-1)*(N-F(1,2))+alpha/2)*(N-F(1,2))*(N-s-k)
            if chi_old>0:
                require(B0>0,'old fixed-parameter region containment');prior+=1
    return {'samples':samples,'valid_small_pairs':valid,'old_certified_small_pairs':prior,
            'cutoffs_first_twelve':[minimum_q(k) for k in range(1,13)],
            'unbounded_proof':'exact algebraic expansion and inequalities in PROOF.md; sampling is corroboration'}
