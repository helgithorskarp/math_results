"""Entire affine entry polyhedron of the fixed q19 four-coordinate template.

Type rows come from the original proper support and forced anchor equations.
Nothing here asserts PSD or completeness outside this template.
"""
from binding import check_current
check_current()
from fractions import Fraction as F
from functools import reduce
from math import gcd, lcm
import json
import resource
import time
from joint import model, table_at, PARENT


def scalar_rows(table):
    b = model.type_budgets(table, 9, 10)
    rows = {('proper',)+pair: 1+a for pair, a in table.items()}
    nn = [t for t in b['types'] if not t[0]&1]
    stars = [t for t in b['types'] if t[0]&1]
    for t in nn:
        val = F(b['s'])
        for u in stars:
            number = 0 if t[0]&u[0] else model.choose(9-t[1],u[1])*model.choose(10-t[2],u[2])
            if number:
                val -= number*(1+table[tuple(sorted((t,u)))])
        rows[('anchor',t)] = val
    for t in b['types']:
        rows[('empty',t)] = b['ell'][t]
    rows[('empty_anchor',)] = b['anchor']
    rows[('loop',)] = b['loop']
    return rows


def affine_rows(raw):
    coords = [(F(0),)*4]+[tuple(F(int(i==j)) for i in range(4)) for j in range(4)]
    values = [scalar_rows(table_at(raw,*x)[0]) for x in coords]
    model.require(all(set(v)==set(values[0]) for v in values), 'all scalar rows at all affine generators')
    out = {}
    for key, c in values[0].items():
        out[key] = (c,)+(tuple(values[i+1][key]-c-F(int(i==0)) for i in range(4)))
    # The domain is nonnegative masses and nonnegative release, with pY eliminated.
    p0 = model.type_budgets(model.comparison(raw,9,10),9,10)['P0']
    out[('domain_tau',)] = (F(0),F(1),F(0),F(0),F(0))
    out[('domain_pXX',)] = (F(0),F(0),F(1),F(0),F(0))
    out[('domain_pX',)] = (F(0),F(0),F(0),F(1),F(0))
    out[('domain_pY',)] = (p0,F(38),F(-1),F(-1),F(0))
    out[('domain_d',)] = (F(0),F(0),F(0),F(0),F(1))
    return out


def primitive(row):
    scale = lcm(*(x.denominator for x in row))
    z = tuple(int(x*scale) for x in row)
    divisor = reduce(gcd,z)
    return tuple(x//abs(divisor) for x in z) if divisor else z


def evaluate(row, coords):
    return row[0]+sum(a*b for a,b in zip(row[1:],coords))


def collect():
    start=time.monotonic()
    raw=model.coefficient_input(PARENT/'COEFFICIENTS.json')
    rows=affine_rows(raw)
    unique={}
    for key,row in rows.items():
        unique.setdefault(primitive(row),[]).append(key)
    const_positive=[];zero=[];variable=[]
    for row,keys in unique.items():
        record=dict(coefficients=list(row), original_rows=keys)
        if any(row[1:]): variable.append(record)
        elif row[0]>0: const_positive.append(record)
        elif row[0]==0:zero.append(record)
        else:raise ValueError('unconditional negative entry row')
    variables=sorted(variable,key=lambda r:tuple(r['coefficients']))
    return dict(agent='six-downset-2',role='researcher',
                coordinates=['1','tau','pXX','pX','d'],
                all_original_scalar_rows=len(rows)-5,domain_rows=5,
                unique_nonconstant_inequalities=variables,
                positive_constant_rows=const_positive,
                identically_zero_rows=zero,
                exact_entry_polyhedron_only=True,
                PSD_requires_all_twelve_complete_physical_forms=True,
                observed_seconds=time.monotonic()-start,
                peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__=='__main__':
    print(json.dumps(collect(),indent=2,sort_keys=True))
