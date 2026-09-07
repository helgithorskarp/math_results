"""Exact arithmetic and explicit colourings for two complete number fields.

Salem basis: 1,t,g,t*g,b,t*b,b*g,t*b*g,
 t^2=t+3, g^2=(1-t)/3, b^2=-3; conjugation fixes t,g and negates b.
Dyadic control basis: 1,h,i,h*i, h^2=h+1, i^2=-1.
All input coefficients are rational. No numerical coordinates are used.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import lcm


def qpair(a=0, b=0):
    return (Q(a), Q(b))


def fadd(x, y):
    return tuple(a+b for a,b in zip(x,y))


def fneg(x):
    return tuple(-a for a in x)


def fmul(x, y, constant=3):
    a,b=x;c,d=y
    return (a*c+constant*b*d, a*d+b*c+b*d)


def finv(x, constant=3):
    a,b=x;norm=a*a+a*b-constant*b*b
    if not norm:
        raise ZeroDivisionError('zero quadratic norm')
    return ((a+b)/norm,-b/norm)


U=qpair(Q(1,3),Q(-1,3))


def eadd(x,y):
    return tuple(a+b for a,b in zip(x,y))


def eneg(x):
    return tuple(-a for a in x)


def emul(x,y):
    a,b=x[:2],x[2:];c,d=y[:2],y[2:]
    return fadd(fmul(a,c),fmul(U,fmul(b,d))) + fadd(fmul(a,d),fmul(b,c))


def einv(x):
    a,b=x[:2],x[2:]
    denominator=fadd(fmul(a,a),fneg(fmul(U,fmul(b,b))))
    scale=finv(denominator)
    return fmul(a,scale)+fneg(fmul(b,scale))


ZERO=tuple(Q(0) for _ in range(8))
ONE=(Q(1),)+ZERO[1:]
T=(Q(0),Q(1))+ZERO[2:]
G=ZERO[:2]+(Q(1),)+ZERO[3:]
B=ZERO[:4]+(Q(1),)+ZERO[5:]
ALPHA=(Q(0),Q(1,2),Q(0),Q(0),Q(0),Q(0),Q(1,2),Q(0))
OMEGA=(Q(-1,2),Q(0),Q(0),Q(0),Q(1,2),Q(0),Q(0),Q(0))


def point(coefficients):
    if len(coefficients)!=8:
        raise ValueError('expected eight rational coefficients')
    return tuple(Q(x) for x in coefficients)


def add(x,y):
    if len(x)!=8 or len(y)!=8:
        raise ValueError('invalid field vector')
    return eadd(x,y)


def neg(x):
    return eneg(x)


def mul(x,y):
    a,b=x[:4],x[4:];c,d=y[:4],y[4:]
    ac,bd=emul(a,c),emul(b,d)
    return tuple(ac[i]-3*bd[i] for i in range(4))+eadd(emul(a,d),emul(b,c))


def conjugate(x):
    return x[:4]+eneg(x[4:])


def inverse(x):
    a,b=x[:4],x[4:]
    aa,bb=emul(a,a),emul(b,b)
    denominator=tuple(aa[i]+3*bb[i] for i in range(4))
    scale=einv(denominator)
    return emul(a,scale)+eneg(emul(b,scale))


def power(x,n):
    if n<0:
        return power(inverse(x),-n)
    out=ONE
    while n:
        if n&1:out=mul(out,x)
        x=mul(x,x);n//=2
    return out


def is_unit(x):
    return mul(x,conjugate(x))==ONE


def prime_exponent(n,p):
    if n==0:raise ValueError('zero has no finite valuation')
    e=0
    while n%p==0:n//=p;e+=1
    return e


@lru_cache(maxsize=None)
def hensel_t(exponent):
    """Unique root t=1 (mod 3) of t^2-t-3 modulo 3^exponent."""
    if type(exponent) is not int or exponent<1:
        raise ValueError('positive integer precision required')
    value,modulus=1,3
    while modulus<3**exponent:
        candidates=[value+j*modulus for j in range(3)
                    if ((value+j*modulus)**2-(value+j*modulus)-3)%(3*modulus)==0]
        if len(candidates)!=1:raise ValueError('Hensel uniqueness failed')
        value=candidates[0];modulus*=3
    return value


def colour_salem(x):
    if len(x)!=8:raise ValueError('expected eight rational coefficients')
    a,b=Q(x[0]),Q(x[1])
    denominator=lcm(a.denominator,b.denominator)
    e=prime_exponent(denominator,3)
    modulus=3**(e+1)
    aa=int(a*denominator);bb=int(b*denominator)
    residue=(aa+bb*hensel_t(e+1))*pow(denominator//3**e,-1,modulus)%modulus
    return residue//3**e


def digit_zero(x,p):
    x=Q(x);e=prime_exponent(x.denominator,p)
    modulus=p**(e+1)
    residue=x.numerator*pow(x.denominator//p**e,-1,modulus)%modulus
    return residue//p**e


def dmul(x,y):
    a,b=x[:2],x[2:];c,d=y[:2],y[2:]
    return fadd(fmul(a,c,1),fneg(fmul(b,d,1)))+fadd(fmul(a,d,1),fmul(b,c,1))


def dconjugate(x):
    return x[:2]+fneg(x[2:])


def dinverse(x):
    a,b=x[:2],x[2:]
    scale=finv(fadd(fmul(a,a,1),fmul(b,b,1)),1)
    return fmul(a,scale,1)+fneg(fmul(b,scale,1))


def colour_dyadic(x):
    if len(x)!=4:raise ValueError('expected four rational coefficients')
    return digit_zero(Q(x[0])-Q(x[2]),2)
