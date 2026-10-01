"""six-sendov-1, researcher: regenerated exact center and Gram identities.

Variables (b,r,x,t), s=4-3r, U=x+iY, Y^2=r^2-x^2.  No tensor,
large generated array, or previous source checkout is an input.
Generic complex polynomial patterns are credited in LITERATURE.md.
"""
from fractions import Fraction as F
from math import comb
import hashlib, json
import algebra as A

def cmul(A,p,q,Y2):
    return (A.add(A.mul(p[0],q[0]),A.scale(A.mul(Y2,A.mul(p[1],q[1])),-1)),
            A.add(A.mul(p[0],q[1]),A.mul(p[1],q[0])))
def cpower(A,p,n,Y2):
    out=(A.ONE,{})
    for _ in range(n):out=cmul(A,out,p,Y2)
    return out
def csum(A,items):return tuple(A.add(*(p[i] for p in items)) for i in range(2))
def cscale(A,p,v):return tuple(A.scale(q,v) for q in p)
def cmulreal(A,p,v):return tuple(A.mul(q,v) for q in p)

def substitute(A,p,axis,num):
    pw=[A.power(num,j) for j in range(max(e[axis] for e in p)+1)]
    out=[]
    for e,v in p.items():
        f=list(e);f[axis]=0
        out.append({tuple(i+j for i,j in zip(f,k)):v*c for k,c in pw[e[axis]].items()})
    return A.add(*out)

def horner(A,p,axis,num,den):
    degree=max(e[axis] for e in p);groups=[{} for _ in range(degree+1)]
    for e,v in p.items():
        f=list(e);f[axis]=0;groups[e[axis]][tuple(f)]=v
    out=groups[degree];dp=[A.power(den,j) for j in range(degree+1)]
    for k in range(degree-1,-1,-1):
        out=A.add(A.mul(out,num),A.mul(groups[k],dp[degree-k]))
    return out,degree


def require(ok,message):
    if not ok:raise ArithmeticError(message)
def digest(polys):
    return hashlib.sha256(json.dumps([A.canonical(p) for p in polys],separators=(',',':')).encode()).hexdigest()

def build_even_skew():
    b,r,x,t=[A.variable(i) for i in range(4)]
    s=A.add(A.scale(A.ONE,4),A.scale(r,-3));s2=A.power(s,2)
    Y2=A.add(A.power(r,2),A.scale(A.power(x,2),-1))
    moments=[csum(A,[cscale(A,cmulreal(A,cpower(A,(x,A.ONE),j,Y2),A.power(b,j+l)),
                     F(9*(-1)**j*comb(6,j),j+l+1)) for j in range(7)]) for l in range(3)]
    # An endpoint-sum derivation, distinct from the binomial integral moments.
    H=(A.add(A.ONE,A.scale(A.mul(b,x),-1)),A.scale(b,-1))
    hp=[cpower(A,H,j,Y2) for j in range(7)]
    endpoint=[cscale(A,csum(A,hp),F(9,7)),
        cscale(A,cmulreal(A,csum(A,[cscale(A,p,j+1) for j,p in enumerate(hp)]),b),F(9,56)),
        cscale(A,cmulreal(A,csum(A,[cscale(A,p,(j+1)*(j+2)) for j,p in enumerate(hp)]),A.power(b,2)),F(1,56))]
    require(endpoint==moments,'Complete endpoint/binomial moments differ')
    AA,BB,CC=moments
    minus2tB=cmulreal(A,BB,A.scale(t,-2));s2C=cmulreal(A,CC,s2)
    J=[csum(A,[AA,minus2tB,s2C]),csum(A,[minus2tB,cscale(A,s2C,2)]),
       csum(A,[AA,minus2tB,cscale(A,s2C,-1)]),minus2tB]
    dot=lambda p,q:A.add(A.mul(p[0],q[0]),A.mul(Y2,A.mul(p[1],q[1])))
    norm=lambda p:dot(p,p)
    cross=lambda p,q:A.scale(A.add(A.mul(p[1],q[0]),A.scale(A.mul(p[0],q[1]),-1)),2)
    R=A.mul(A.power(r,12),A.power(s,4))
    E=[A.add(norm(J[0]),A.scale(R,-1)),A.add(A.scale(dot(J[0],J[2]),2),norm(J[1]),A.scale(R,-2)),
       A.add(norm(J[2]),A.scale(dot(J[1],J[3]),2),A.scale(R,-1)),norm(J[3])]
    O=[cross(J[0],J[1]),A.add(cross(J[0],J[3]),cross(J[2],J[1])),cross(J[2],J[3])]
    # Independent full eight-factor moment construction in powers of k:
    # (1+k^2)(1-2bt tau(1+ik)+b^2s^2tau^2(1+ik)^2/(1+k^2)).
    # Complex coefficients stored as (R_even,R_Y,I_even,I_Y).
    direct=[({}, {}, {}, {}) for _ in range(4)]
    for j in range(7):
        Uj=cpower(A,(x,A.ONE),j,Y2)
        for l in range(3):
            coefficients=[[(0,1,0),(2,1,0)],[(0,-2,0),(1,0,-2),(2,-2,0),(3,0,-2)],
                          [(0,1,0),(1,0,2),(2,-1,0)]][l]
            scale=[A.ONE,t,s2][l]
            Q=cscale(A,cmulreal(A,Uj,A.mul(A.power(b,j+l),scale)),F(9*(-1)**j*comb(6,j),j+l+1))
            for degree,real,imag in coefficients:
                v=(A.scale(Q[0],real),A.scale(Q[1],-imag),A.scale(Q[0],imag),A.scale(Q[1],real))
                direct[degree]=tuple(A.add(direct[degree][i],v[i]) for i in range(4))
    expected=[(p[0],{}, {},p[1]) if j%2==0 else ({},A.scale(p[1],-1),p[0],{}) for j,p in enumerate(J)]
    require(direct==expected,'Complete eight-factor center numerator differs')
    # Expand real^2+imag^2 independently, reducing only Y^2.
    direct_norm=[({}, {}) for _ in range(7)]
    for j,p in enumerate(direct):
        for k,q in enumerate(direct):
            even=A.add(A.mul(p[0],q[0]),A.mul(p[2],q[2]),
                       A.mul(Y2,A.add(A.mul(p[1],q[1]),A.mul(p[3],q[3]))))
            odd=A.add(A.mul(p[0],q[1]),A.mul(p[1],q[0]),A.mul(p[2],q[3]),A.mul(p[3],q[2]))
            v=direct_norm[j+k]
            direct_norm[j+k]=(A.add(v[0],even),A.add(v[1],odd))
    for degree,weight in [(0,1),(2,2),(4,1)]:
        old=direct_norm[degree];direct_norm[degree]=(A.add(old[0],A.scale(R,-weight)),old[1])
    require(direct_norm==[(E[j//2],{}) if j%2==0 else ({},O[j//2]) for j in range(7)],
            'Complete direct norm convolution differs from even/skew coefficients')
    require(E[3]==A.scale(A.mul(A.power(t,2),norm(BB)),4),'Leading even coefficient failed')
    return {'moments':moments,'J':J,'E':E,'O':O,'Y2':Y2,'s':s,'R':R}


def build():
    data = build_even_skew()
    even, skew, y2 = data['E'], data['O'], data['Y2']
    gram = []
    for degree in range(7):
        squares = A.add(*[A.mul(even[j], even[degree-j])
                          for j in range(4) if 0 <= degree-j < 4])
        product = A.mul(y2, A.add(*[A.mul(skew[j], skew[degree-1-j])
                                    for j in range(3) if 0 <= degree-1-j < 3])) if degree else {}
        gram.append(A.add(squares, A.scale(product, -1)))
    require(gram[0] == A.power(even[0], 2), 'Constant Gram identity failed')
    require(gram[6] == A.power(even[3], 2), 'Leading Gram identity failed')
    data['G'] = gram
    return data


def angular_control(data, key):
    """Return P_i with only its actual common positive t power removed."""
    family, index = key[0], int(key[1:])
    require(family in ('E', 'G'), 'Unknown control family')
    coefficients = data[family]
    degree = len(coefficients) - 1
    require(1 <= index <= degree, 'Control index out of range')
    t = A.variable(3)
    deficit = A.add(A.power(data['s'], 2), A.scale(A.power(t, 2), -1))
    polynomial = A.add(*[
        A.scale(A.mul(A.mul(coefficients[j], A.power(t, 2*(index-j))),
                      A.power(deficit, j)), F(comb(index, j), comb(degree, j)))
        for j in range(index+1)])
    common = tuple(min(e[j] for e in polynomial) for j in range(4))
    require(common[:3] == (0, 0, 0), 'Unexpected removed b/r/x powers')
    expected = {'E3': 2, 'G5': 2, 'G6': 4}.get(key, 0)
    require(common[3] == expected, 'Unexpected removed t power')
    polynomial = {tuple(e[j]-common[j] for j in range(4)): v
                  for e, v in polynomial.items()}
    return polynomial, common
