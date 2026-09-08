"""Exact producer arithmetic in Q(w,b,c,e); see PROOF.md for the field."""
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path

SIZE = 16
D = 384
ZERO = (0,)*SIZE


def basis(i):
    return tuple(int(i == j) for j in range(SIZE))


ONE, W, B, C, E = (basis(i) for i in [0,1,2,4,8])


@lru_cache(None)
def reduce_monomial(exponents):
    """Reduce by the four defining equations; coefficients are integers."""
    a,b,c,e = exponents
    if a >= 2:
        terms = [(1,(a-1,b,c,e)),(-1,(a-2,b,c,e))]
    elif b >= 2:
        terms = [(-11,(a,b-2,c,e))]
    elif c >= 2:
        terms = [(5,(a,b,c-2,e))]
    elif e >= 2:
        terms = [(-3320,(a,b,c,e-2)),(-632,(a,b+1,c,e-2)),
                 (1264,(a+1,b+1,c,e-2))]
    else:
        return ((a+2*b+4*c+8*e,1),)
    out = [0]*SIZE
    for coefficient, powers in terms:
        for index,value in reduce_monomial(powers):
            out[index] += coefficient*value
    return tuple((i,v) for i,v in enumerate(out) if v)


PRODUCT = [[reduce_monomial(tuple(((i>>k)&1)+((j>>k)&1) for k in range(4)))
            for j in range(SIZE)] for i in range(SIZE)]


def add(x,y):
    return tuple(a+b for a,b in zip(x,y))


def sub(x,y):
    return tuple(a-b for a,b in zip(x,y))


def scale(x,n):
    return tuple(a*n for a in x)


def mul(x,y):
    out = [0]*SIZE
    xs = [(i,a) for i,a in enumerate(x) if a]
    ys = [(j,b) for j,b in enumerate(y) if b]
    for i,a in xs:
        for j,b in ys:
            ab = a*b
            for index,coefficient in PRODUCT[i][j]:
                out[index] += ab*coefficient
    return tuple(out)


def conjugate(x):
    out = [0]*SIZE
    for i,a in enumerate(x):
        sign = (-1)**(((i>>1)&1)+((i>>3)&1))
        if i&1:
            out[i^1] += sign*a
            out[i] -= sign*a
        else:
            out[i] += sign*a
    return tuple(out)


def norm(x):
    return mul(x,conjugate(x))


def lin(*terms):
    out = ZERO
    for n,x in terms:
        out = add(out,scale(x,n))
    return out


def seed():
    """Return384 times each complex point; labels are p,q,v1,...,v27."""
    data = json.loads((Path(__file__).parent/'seed.json').read_text())
    rows = data['moser_rows']
    if len(rows)!=27 or any(len(r)!=4 or any(type(x) is not int for x in r) for r in rows):
        raise ValueError('seed rows')
    v = add(scale(ONE,5),B)  # six times omega3
    wv = mul(W,v)
    p = add(lin((1152,ONE),(816,W),(-56,v),(128,wv)),
            mul(C,lin((-96,ONE),(48,W),(-8,v),(16,wv))))
    q = add(lin((1056,ONE),(624,W),(-8,v),(128,wv)),
            mul(E,lin((-6,W),(1,v),(1,wv))))
    result = [p,q]
    for a,b,c,d in rows:
        result.append(lin((384*a,ONE),(384*b,W),(64*c,v),(64*d,wv)))
    if len(set(result))!=29:
        raise ValueError('seed coincidence')
    return result


PRIME = 1000000411
ROOTS = (949605451,589799521,269028472,973233399)


def residue_basis():
    w,b,c,e = ROOTS
    if ((w*w-w+1)%PRIME or (b*b+11)%PRIME or (c*c-5)%PRIME
            or (e*e+3320+632*b-1264*w*b)%PRIME):
        raise ValueError('residue homomorphism')
    return tuple((pow(w,i&1,PRIME)*pow(b,(i>>1)&1,PRIME)
                  *pow(c,(i>>2)&1,PRIME)*pow(e,(i>>3)&1,PRIME))%PRIME
                 for i in range(SIZE))


RESIDUES = residue_basis()


def evaluate(x):
    return sum(a*b for a,b in zip(x,RESIDUES))%PRIME


def edges_exact(points, target):
    values = [evaluate(x) for x in points]
    bars = [evaluate(conjugate(x)) for x in points]
    goal = evaluate(target)
    edges = []
    for i,j in combinations(range(len(points)),2):
        if (values[i]-values[j])*(bars[i]-bars[j])%PRIME == goal:
            if norm(sub(points[i],points[j])) == target:
                edges.append((i,j))
    return edges


TURN = sub(W,ONE)  # exp(2*pi*i/3)
TURNS = (ONE,TURN,mul(TURN,TURN))


def case(points, centre, axis):
    """Exact D3 cloud; addresses ordered(k,reflection,seed label)."""
    d = sub(points[axis],points[centre])
    n = norm(d)
    if d == ZERO or n == ZERO:
        raise ValueError('degenerate axis')
    d2 = mul(d,d)
    relative = [sub(x,points[centre]) for x in points]
    direct = [mul(n,x) for x in relative]
    reflected = [mul(d2,conjugate(x)) for x in relative]
    formal = [mul(turn,x) for turn in TURNS for cloud in (direct,reflected) for x in cloud]
    unique = sorted(set(formal))
    ids = {x:i for i,x in enumerate(unique)}
    target = scale(mul(n,n),D*D)
    edges = edges_exact(unique,target)
    return {'points':unique,'address_ids':[ids[x] for x in formal],
            'edges':edges,'centre_id':ids[ZERO], 'scale_squared':target}
