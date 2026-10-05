"""Owned pass69 pure helpers only; no closed entry/continuity replay."""
import copy
import hashlib
import json
import math
import pathlib
import re
from fractions import Fraction as F
from fractions import Fraction as F
LOW, HIGH = F(2,3), F(27,40)
MINB, MAXB, MINAB, C = F(871,1600), F(5,9), F(23517,64000), F(197,360)
FLOOR, TMAX = F(40,67), F(40824,4489)
ROOT = tuple(map(F,("2/3","27/40","0","23/5","51/80","1","0","23/40")))
ROLES = {"scalar-product-origin","retained-mean-product-origin","standard-polar","joint-energy-polar"}
def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def add(*terms):
    out = [F(0)] * max(map(len, terms))
    for term in terms:
        for i, x in enumerate(term):
            out[i] += x
    return out

def scale(values, factor):
    return [factor * x for x in values]

def multiply(left, right):
    out = [F(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return out

def power(values, exponent):
    out = [F(1)]
    for _ in range(exponent):
        out = multiply(out, values)
    return out

def integral(values, weight=0):
    return sum((x / (i + weight + 1) for i, x in enumerate(values)), F(0))

def beta_integral(i, j):
    return F(math.factorial(i) * math.factorial(j), math.factorial(i + j + 1))

def binomial_linear(a, b, degree):
    return [math.comb(degree, i) * a ** (degree - i) * b ** i for i in range(degree + 1)]

def root_grid(x, grid, upward):
    require(x >= 0 and type(grid) is int and (grid > 0), 'root domain')
    floor = math.isqrt(x.numerator * grid ** 2 // x.denominator)
    result = floor + int(upward and F(floor, grid) ** 2 < x)
    if upward:
        require(F(result, grid) ** 2 >= x and (result == 0 or F(result - 1, grid) ** 2 < x), 'minimal upper root')
    else:
        require(F(result, grid) ** 2 <= x and F(result + 1, grid) ** 2 > x, 'maximal lower root')
    return F(result, grid)

def canonical_rational(value):
    require(type(value) is str and re.fullmatch('-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?', value) is not None, 'rational text type/syntax')
    number = F(value)
    require(str(number) == value, 'canonical rational text')
    return number

def decode_cover(raw):

    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs)

def cover_cells(cover):
    require(type(cover) is dict and set(cover) == {'root', 'splits', 'leaves'}, 'cover schema')
    require(type(cover['root']) is list and len(cover['root']) == 8, 'root schema')
    root = tuple(map(canonical_rational, cover['root']))
    require(root == ROOT, 'entire closed root')
    splits, leaves = (cover['splits'], cover['leaves'])
    require(type(splits) is dict and type(leaves) is dict, 'tree maps')
    require(not set(splits).intersection(leaves), 'internal/leaf disjointness')
    for path in list(splits) + list(leaves):
        require(type(path) is str and re.fullmatch('[01]*', path) is not None, 'binary path schema')
    for path, role in leaves.items():
        require(type(role) is str and role in ROLES, 'defining role')
    for path, split in splits.items():
        require(type(split) is dict and set(split) == {'axis', 'cut'}, 'split schema')
        require(type(split['axis']) is int and 0 <= split['axis'] < 4, 'axis integer/type/range')
        canonical_rational(split['cut'])
    seen, output = (set(), [])

    def visit(path, box):
        require(path not in seen, 'unique reachability')
        seen.add(path)
        if path in leaves:
            output.append(dict(path=path, role=leaves[path], raw_box=box))
            return
        require(path in splits, 'complete child coverage')
        split = splits[path]
        position, cut = (2 * split['axis'], canonical_rational(split['cut']))
        require(box[position] < cut < box[position + 1], 'strict interior cut')
        left, right = (list(box), list(box))
        left[position + 1], right[position] = (cut, cut)
        require(tuple(left[:position] + left[position + 2:]) == tuple(right[:position] + right[position + 2:]), 'unchanged coordinates')
        require(left[position] == box[position] and right[position + 1] == box[position + 1] and (left[position + 1] == right[position]), 'no cut gap')
        visit(path + '0', tuple(left))
        visit(path + '1', tuple(right))
    visit('', root)
    require(seen == set(splits).union(leaves), 'no unreachable tree entries')
    return (output, dict(internal_nodes=len(splits), leaves=len(leaves), reachable_nodes=len(seen), maximum_depth=max(map(len, seen))))

def tighten_mass_eight(raw):
    a, b, el, eh, ul, uh, wl, wh = raw
    rounds = []
    for _ in range(4):
        old = (a, b, el, eh, ul, uh, wl, wh)
        uh = min(uh, F(1))
        ul = max(ul, 1 - eh / 16)
        el = max(el, 2 * max(0, 8 - 8 * uh), 8 * ((1 - uh) ** 2 + wl))
        wh = min(wh, 1 - ul ** 2, eh / 8 - (1 - uh) ** 2)
        new = (a, b, el, eh, ul, uh, wl, wh)
        require(all((new[i] >= old[i] and new[i + 1] <= old[i + 1] for i in (0, 2, 4, 6))), 'enclosing endpoint monotonicity')
        require(all((new[i] <= new[i + 1] for i in (0, 2, 4, 6))), 'nonempty necessary enclosure')
        rounds.append(new)
    m = 1 / (1 + b)
    require(F(8) > 7 * m + 1, 'radius-budget monotonicity premise')
    tl = max(0, el - 16 + 16 * ul)
    tu = min(eh - 2 * max(0, 8 - 8 * uh), (7 - 7 * m) ** 2 + 7 * (m - 1) ** 2)
    require(0 <= tl <= tu <= TMAX, 'whole necessary T interval')
    return (rounds, (tl, tu))

def product_cap(box, t_interval):
    a, b, el, eh, ul, uh, wl, wh = box
    tl, tu = t_interval
    square_root = root_grid(F(7, 8) * tu, 4096, True)
    radius = max(F(1), min(8 - 7 / (1 + b), 1 + square_root))
    z = tl / (2 * radius)
    terms = [z ** i / math.factorial(i) for i in range(5)]
    horner = 1 + z * (1 + z * (F(1, 2) + z * (F(1, 6) + z / F(24))))
    require(sum(terms) == horner and radius >= 1 and (z >= 0), 'entire product exponential budget')
    return dict(upper_radius=radius, root_ceiling=square_root, exponent=z, all_five_terms=terms, product_upper_bound=1 / sum(terms))
