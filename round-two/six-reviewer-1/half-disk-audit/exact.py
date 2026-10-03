"""Independent standard-library rational polynomial arithmetic. No author imports."""
from fractions import Fraction as Q
from math import comb, factorial

def require(condition, message):
    if not condition:
        raise ValueError(message)

def add(p, q):
    r = [Q(0)] * max(len(p), len(q))
    for i, x in enumerate(p): r[i] += x
    for i, x in enumerate(q): r[i] += x
    return r

def scale(p, c): return [x*c for x in p]

def mul(p, q):
    r = [Q(0)] * (len(p)+len(q)-1)
    for i, x in enumerate(p):
        for j, y in enumerate(q): r[i+j] += x*y
    return r

def power(p, n):
    r = [Q(1)]
    for _ in range(n): r = mul(r, p)
    return r

def integrate(p): return sum((x/Q(i+1) for i,x in enumerate(p)), Q(0))

def bernstein(p, degree):
    require(len(p) <= degree+1, 'degree overflow')
    return [sum((p[k]*Q(comb(i,k),comb(degree,k))
                 for k in range(min(i,len(p)-1)+1)), Q(0))
            for i in range(degree+1)]

def binomial_integral(a, b, degree, extra=0):
    return sum((Q(comb(degree,j))*a**(degree-j)*b**j/Q(j+extra+1)
                for j in range(degree+1)), Q(0))

def partitions(total, least=2):
    if total == 0:
        yield ()
    for k in range(least,total+1):
        for tail in partitions(total-k,k): yield (k,)+tail

def newton_constants():
    c = [Q(1),Q(0)]
    for n in range(2,9): c.append(sum(c[n-k] for k in range(2,n+1))/n)
    alternate = [Q(1),Q(0)]
    for n in range(2,9):
        s = Q(0)
        for partition in partitions(n):
            denominator=1
            for k in set(partition):
                count=partition.count(k)
                denominator *= k**count * factorial(count)
            s += Q(1,denominator)
        alternate.append(s)
    require(c == alternate, 'complete cycle partition constants')
    return c

def encode(value):
    if isinstance(value,Q): return str(value)
    if isinstance(value,dict): return {k:encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [encode(x) for x in value]
    if isinstance(value,(str,int,bool)) or value is None: return value
    raise TypeError(type(value).__name__)
