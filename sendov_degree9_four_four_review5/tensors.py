"""Independent fused affine/Bernstein matrices, applied last axis first.

Each rational univariate matrix is checked against its exact inverse basis
formula on EVERY monomial. No de Casteljau routine or author code is used.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, lcm, prod
import hashlib
from kernel import require


@lru_cache(None)
def matrix(n, lo, hi):
    width = hi-lo
    weights = [[sum(F(comb(k,j)*comb(i,j), comb(n,j))*lo**(k-j)*width**j
                    for j in range(min(i,k)+1)) for k in range(n+1)] for i in range(n+1)]
    for k in range(n+1):
        for j in range(n+1):
            inverse = comb(n,j)*sum((-1)**(j-i)*comb(j,i)*weights[i][k] for i in range(j+1))
            expected = comb(k,j)*lo**(k-j)*width**j if j<=k else 0
            require(inverse == expected, 'Univariate basis identity')
    den = lcm(*(v.denominator for row in weights for v in row))
    return [[(k, int(v*den)) for k, v in enumerate(row) if v] for row in weights], den


def convert(p, degrees, box):
    require(tuple(max(e[i] for e in p) for i in range(4)) == tuple(degrees), 'Tensor degrees')
    sizes = [n+1 for n in degrees]
    strides = [prod(sizes[i+1:]) for i in range(4)]
    den = lcm(*(a.denominator for a in p.values()))
    data = [0]*prod(sizes)
    for e, a in p.items():
        data[sum(e[i]*strides[i] for i in range(4))] = int(a*den)
    for axis in reversed(range(4)):
        weights, d = matrix(degrees[axis], *box[axis])
        step = strides[axis]
        block = step*sizes[axis]
        result = [0]*len(data)
        for start in range(0, len(data), block):
            for offset in range(step):
                line = data[start+offset:start+offset+block:step]
                for i, row in enumerate(weights):
                    result[start+offset+i*step] = sum(a*line[k] for k, a in row)
        data, den = result, den*d
    return data, den


def inventory(data, den, degrees):
    sizes = [n+1 for n in degrees]
    strides = [prod(sizes[i+1:]) for i in range(4)]
    require(len(data) == prod(sizes) and min(data)>=0, 'Incomplete/negative tensor')
    zeros, hasher = [], hashlib.sha256()
    cmin = xmin = None
    for index, value in enumerate(data):
        e = tuple((index//strides[j])%sizes[j] for j in range(4))
        if not value:
            zeros.append(e)
        if e[1] == 0:
            cmin = value if cmin is None else min(cmin, value)
        if e[2] == 0:
            xmin = value if xmin is None else min(xmin, value)
        hasher.update((str(F(value,den))+'\n').encode())
    return {'coefficients':len(data), 'minimum':str(F(min(data),den)),
            'minimum_positive':str(F(min(v for v in data if v>0),den)),
            'zeros':len(zeros), 'zeroth_c_minimum':str(F(cmin,den)),
            'zeroth_x_minimum':str(F(xmin,den)), 'sha256':hasher.hexdigest()}, zeros


def cover(boxes, predicate, axes=(1,2)):
    cuts = [sorted({v for b in boxes for v in b[j]}) for j in axes]
    for values in product(*[[(a+b)/2 for a,b in zip(c[:-1],c[1:])] for c in cuts]):
        hits = sum(all(b[j][0]<v<b[j][1] for j,v in zip(axes,values)) for b in boxes)
        require(hits == int(predicate(*values)), 'Domain coverage/overlap')
    # Closed cells cover all limiting boundary faces. The predicates below
    # describe closed domains, so open-rectangle checks suffice with endpoint
    # inventories separately required by the caller.
    for b in boxes:
        require(all(0<=lo<hi<=1 for lo,hi in b), 'Invalid closed cell')
        require(all(b[j]==(F(0),F(1)) for j in range(4) if j not in axes), 'Truncated free axis')
