"""Exact rational interval Horner bounds on complete closed rectangles.

Dense coefficients are translated to each rectangle's lower corner.
Nested interval Horner on nonnegative offsets retains coefficient signs.
This does not use Bernstein weights or an absolute centered-Taylor bound.
"""
from fractions import Fraction as F
from math import comb


def add(u, v):
    return u[0]+v[0], u[1]+v[1]


def multiply(u, v):
    products = [x*y for x in u for y in v]
    return min(products), max(products)


def shift(coefficients, left_t, left_z):
    n = max((i for i,j in coefficients),default=0)
    m = max((j for i,j in coefficients),default=0)
    translated = [[F(0) for j in range(m+1)] for i in range(n+1)]
    for (i,j),value in coefficients.items():
        for k in range(i+1):
            for l in range(j+1):
                translated[k][l] += value*comb(i,k)*comb(j,l)*left_t**(i-k)*left_z**(j-l)
    return translated


def horner(translated, t_width, z_width):
    rows = []
    for coefficients in translated:
        interval = (F(0),F(0))
        for c in reversed(coefficients):
            interval = add(multiply(interval,(F(0),z_width)),(c,c))
        rows.append(interval)
    interval = (F(0),F(0))
    for row in reversed(rows):
        interval = add(multiply(interval,(F(0),t_width)),row)
    return interval


def bound(coefficients, box):
    ta,tb,za,zb = map(F,box)
    if ta>tb or za>zb:
        raise ValueError('reversed closed interval')
    return horner(shift(coefficients,ta,za),tb-ta,zb-za)


def complete_sign(coefficients, box, sign):
    if sign not in (-1,1):
        raise ValueError('strict sign required')
    ta,tb,za,zb = map(F,box)
    # This is a fixed finite resource ceiling, not a claim about missing cases.
    for n in (1,2,4,8,16,32):
        rows=[]
        for i in range(n):
            for j in range(n):
                cell=(ta+(tb-ta)*i/n,ta+(tb-ta)*(i+1)/n,
                      za+(zb-za)*j/n,za+(zb-za)*(j+1)/n)
                lo,hi=bound(coefficients,cell)
                rows.append((cell,lo,hi))
        if all((lo>0 if sign==1 else hi<0) for cell,lo,hi in rows):
            return {'subdivisions_each_axis':n,'complete_closed_cells':n*n,
                    'global_lower':str(min(lo for cell,lo,hi in rows)),
                    'global_upper':str(max(hi for cell,lo,hi in rows)),
                    'all_rows':[[[str(x) for x in cell],str(lo),str(hi)] for cell,lo,hi in rows]}
    raise RuntimeError('fixed closed-cover sign search incomplete; no conclusion')
