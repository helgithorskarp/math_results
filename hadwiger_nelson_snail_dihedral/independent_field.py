"""Independent exact arithmetic in the quadratic tower Q(a,b,c,e)."""
import json
from pathlib import Path

def require(condition,message):
    if not condition:
        raise ValueError(message)

ZERO = (0,)*16
ONE = (1,)+(0,)*15
A = (0,1)+(0,)*14
B = (0,0,1)+(0,)*13
C = (0,0,0,0,1)+(0,)*11
E = (0,)*8+(1,)+(0,)*7
D = 768
FACTORS = tuple((-3 if mask&1 else 1)*(-11 if mask&2 else 1)
                *(5 if mask&4 else 1) for mask in range(8))


def plus(x,y):
    return tuple(a+b for a,b in zip(x,y))


def minus(x,y):
    return tuple(a-b for a,b in zip(x,y))


def times(n,x):
    return tuple(n*a for a in x)


def product8(x,y):
    out = [0]*8
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(y):
                if b:
                    out[i^j] += a*b*FACTORS[i&j]
    return tuple(out)


def times_e_square(x):
    out = [-3320*a for a in x]
    for i,a in enumerate(x):
        out[i^3] += 632*a*FACTORS[i&3]
    return tuple(out)


def product(x,y):
    x0,x1,y0,y1 = x[:8],x[8:],y[:8],y[8:]
    return (plus(product8(x0,y0),times_e_square(product8(x1,y1)))
            +plus(product8(x0,y1),product8(x1,y0)))


def bar(x):
    return tuple((-a if ((i&1)+((i>>1)&1)+((i>>3)&1))%2 else a)
                 for i,a in enumerate(x))


def norm(x):
    return product(x,bar(x))


def linear(*terms):
    result = ZERO
    for n,x in terms:
        result = plus(result,times(n,x))
    return result


def exact_seed():
    rows = json.loads((Path(__file__).parent/'seed.json').read_text())['moser_rows']
    w2 = plus(ONE,A)
    v6 = plus(times(5,ONE),B)
    wv12 = product(w2,v6)
    p = plus(linear((2304,ONE),(816,w2),(-112,v6),(128,wv12)),
             product(C,linear((-192,ONE),(48,w2),(-16,v6),(16,wv12))))
    q = plus(linear((2112,ONE),(624,w2),(-16,v6),(128,wv12)),
             product(E,linear((-6,w2),(2,v6),(1,wv12))))
    result = [p,q]+[linear((768*a,ONE),(384*b,w2),(128*c,v6),(64*d,wv12))
                     for a,b,c,d in rows]
    require(len(result)==29 and len(set(result))==29,'exact seed shape')
    return result


def exact_addresses(seed,centre,axis):
    delta = minus(seed[axis],seed[centre])
    n = norm(delta)
    require(delta!=ZERO and n!=ZERO,'exact axis')
    relative = [minus(x,seed[centre]) for x in seed]
    direct = [product(n,x) for x in relative]
    delta2 = product(delta,delta)
    reflected = [product(delta2,bar(x)) for x in relative]
    # All positions are over2*D*n; these are twice the three rotations.
    rotations2 = [times(2,ONE),minus(A,ONE),times(-1,plus(ONE,A))]
    formal = [product(turn,x) for turn in rotations2
              for cloud in [direct,reflected] for x in cloud]
    target = times(4*D*D,product(n,n))
    return formal,target


def double_change_basis(x):
    """Twice x after substituting w=(1+a)/2, for entry-level comparison."""
    out = [0]*16
    for i,c in enumerate(x):
        if i&1:
            out[i^1] += c
            out[i] += c
        else:
            out[i] += 2*c
    return tuple(out)
