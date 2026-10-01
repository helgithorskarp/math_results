"""Explicit six-copy periodic tilings of all one-step endpoint-shift strips.

All coordinates and operations are exact integers. The infinite-parameter
proof is in proof.md; finite checks of these formulas are sanity checks.
"""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prototype(k):
    require(type(k) is int and k >= 1, 'The strip parameter must be an integer >=1')
    cells = {(0,0), (-2*k,k-1), (-2*k-1,k+1)}
    for r in range(k):
        cells.update((x,y) for x in (-2*r-1,-2*r-2) for y in (r+1,r+2))
    require(len(cells) == 4*k+3, 'Unexpected prototype area')
    return tuple(sorted(cells))


def affine(cells, g):
    require(len(g) == 6 and all(type(x) is int for x in g), 'Invalid integer motion')
    a,b,c,d,u,v = g
    return tuple(sorted((a*x+b*y+u,c*x+d*y+v) for x,y in cells))


def poses(k):
    prototype(k)
    # I, A, B, sigma, sigma A, sigma B; see the symbolic quotient proof.
    return ((1,0,0,1,0,0),
            (-1,0,1,1,-2*k,k-2),
            (1,0,-1,-1,1,3),
            (-1,0,0,-1,1-2*k,-5*k-1),
            (1,0,-1,-1,1,1-6*k),
            (-1,0,1,1,-2*k,-5*k-4))


def periods(k):
    prototype(k)
    return ((2,5),(0,12*k+9))


def quotient(point, k):
    x,y = point
    r = x % 2
    return r, (y-5*((x-r)//2)) % (12*k+9)


def predicted_first_cluster(k):
    prototype(k)
    L = 12*k+9
    even = {-3,-2,-1,0} | set(range(2,6*k+2)) | {6*k+3}
    odd = {-2} | set(range(3,6*k+5)) | {6*k+6}
    return ({z % L for z in even}, {z % L for z in odd})
