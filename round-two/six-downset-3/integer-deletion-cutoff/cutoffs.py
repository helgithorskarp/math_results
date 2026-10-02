"""Exact proved integer cutoff for the specified capped ansatz, k>=5."""
from math import isqrt
def cutoff(k):
    if type(k) is not int or k<5:raise ValueError('Requires integer k>=5')
    if k==5:return 19
    radicand=28*k*k+36*k+81
    p=isqrt(radicand)
    if p*p<radicand:p+=1
    if p%2==0:p+=1
    return (6*k-25+p)//2
def norm(q,k):
    if type(q) is not int or type(k) is not int or k<5 or q<max(4,k):
        raise ValueError('Requires integers k>=5,q>=max(4,k)')
    return (2*q-6*k+25)**2-28*k*k-36*k
def feasible(q,k):
    rho=norm(q,k)
    return rho>=81 and (k,q)!=(5,18)
