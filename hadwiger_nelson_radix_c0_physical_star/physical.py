"""Direct exact physical A5 construction; no event-curve inventory is used.

A pair (a,b) denotes a+i*sqrt(3)*b with a,b in Q[s]/(q).
The q supplied by the algebraic verifier must be irreducible and have a real root.
"""
from itertools import product
from flint import fmpq, fmpq_poly


def polynomial(values):
    return fmpq_poly([fmpq(str(c)) for c in values])


def coefficients(p):
    return tuple(str(c) for c in p.coeffs())


def coordinates(component):
    q = polynomial(component['q'])
    zero, one = fmpq_poly([]), fmpq_poly([1])
    x, y = polynomial(component['x']) % q, polynomial(component['y']) % q

    def add(a, b):
        return (a[0]+b[0], a[1]+b[1])

    def multiply(a, b):
        return ((a[0]*b[0]-3*a[1]*b[1]) % q,
                (a[0]*b[1]+a[1]*b[0]) % q)

    powers = [(one, zero)]
    for _ in range(4):
        powers.append(multiply(powers[-1], (x, y)))
    digits = [(zero,zero), (one,zero), (fmpq_poly([fmpq(1,2)]),fmpq_poly([fmpq(1,2)]))]
    terms = [[multiply(d,p) for d in digits] for p in powers]
    points, lookup, label_to_point = [], {}, []
    for word in product(range(3), repeat=5):
        point = (zero,zero)
        for j,t in enumerate(word):
            point = add(point,terms[j][t])
        key = (coefficients(point[0]), coefficients(point[1]))
        if key not in lookup:
            lookup[key] = len(points)
            points.append(point)
        label_to_point.append(lookup[key])
    return points, label_to_point


def graph(component):
    points, label_to_point = coordinates(component)
    q = polynomial(component['q'])
    zero, one = fmpq_poly([]), fmpq_poly([1])
    edges = []
    for a,(ax,ay) in enumerate(points):
        for b in range(a):
            bx,by = points[b]
            dx,dy = ax-bx, ay-by
            if (dx*dx+3*dy*dy-one) % q == zero:
                edges.append([b,a])
    edges.sort()
    triangle = [label_to_point[i] for i in (0,81,162)]
    if len(set(triangle)) != 3 or any(sorted((a,b)) not in edges for a in triangle for b in triangle if a<b):
        raise ValueError('universal triangle missing')
    return points, label_to_point, edges, triangle


def check_word(word, n, edges):
    if not isinstance(word,list) or len(word)!=n or any(type(c)!=int or c not in (0,1,2) for c in word):
        raise ValueError('invalid three-colour word')
    if any(word[a]==word[b] for a,b in edges):
        raise ValueError('monochromatic physical unit edge')
