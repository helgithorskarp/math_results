"""Independent integer evaluations/Fraction Gaussian proof of every fixed determinant.

No generator polynomial arithmetic is imported. Complete degree-bounded
Cartesian grids prove characteristic-zero polynomial identities; finite
evaluations without their explicit degree bound are not used as proof.
"""
from fractions import Fraction as F
from itertools import product,permutations
from math import prod

def require(ok,message):
    if not ok:raise ValueError(message)

def decode(data,positive=False):
    den=data['denominator'];require(type(den) is int and den>0,'positive coefficient denominator')
    terms={}
    require(len(data['terms'])<=512,'unchanged512 coefficient guard')
    for ex,value in data['terms']:
        ex=tuple(ex);value=int(value)
        require(len(ex)==3 and all(type(e) is int and e>=0 for e in ex),'three nonnegative exponents')
        require(ex not in terms and value,'unique nonzero coefficient')
        terms[ex]=value
    if positive:
        require(terms.get((0,0,0),0)>0 and all(v>=0 for v in terms.values()),'strict coefficientwise positivity')
    return terms,den

def degrees(p):
    return tuple(max((ex[j] for ex in p[0]),default=0) for j in range(3))

def value(p,point):
    terms,den=p
    maxdeg=degrees(p);powers=[[x**d for d in range(maxdeg[j]+1)] for j,x in enumerate(point)]
    result=sum(co*powers[0][ex[0]]*powers[1][ex[1]]*powers[2][ex[2]] for ex,co in terms.items())
    return F(result,den)

def add_degrees(*xs):
    return tuple(sum(x[j] for x in xs) for j in range(3))

def factors_degree(xs):
    return tuple(sum(degrees(p)[j]*e for p,e in xs) for j in range(3))

def factors_value(xs,point):
    return prod(value(p,point)**e for p,e in xs)

def determinant(a):
    a=[[F(x) for x in row] for row in a];answer=F(1)
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];answer=-answer
        answer*=a[j][j]
        for i in range(j+1,len(a)):
            c=a[i][j]/a[j][j]
            for k in range(j+1,len(a)):a[i][k]-=c*a[j][k]
    return answer

def shift_identity(original,shifted):
    bounds=tuple(max((ex[j]+ex[2] if j<2 else ex[2] for ex in original[0]),default=0) for j in range(3))
    require(all(degrees(shifted)[j]<=bounds[j] for j in range(3)),'exact separate substitution degree bound')
    count=0
    for point in product(*(range(b+1) for b in bounds)):
        u,v,w=point
        require(value(original,(3+u,2+v,12+4*u+4*v+w))==value(shifted,point),'complete polynomial quadrant substitution identity')
        count+=1
    return bounds,count

def check_row(row):
    k=row['order'];require(type(k) is int and 1<=k<=4,'leading minor order')
    original=decode(row['original']);shifted=decode(row['shifted'],True)
    shift_bounds,shift_points=shift_identity(original,shifted)
    denominators=[];factor_shift_points=0
    for f in row['denominator_factors']:
        old,new=decode(f['original']),decode(f['shifted'],True)
        require(type(f['power']) is int and f['power']>0,'positive denominator exponent')
        _,count=shift_identity(old,new);factor_shift_points+=count
        denominators.append((new,f['power']))
    a=[[decode(p) for p in v] for v in row['cleared_matrix']]
    require(len(a)==k and all(len(v)==k for v in a),'whole principal-prefix matrix')
    domains=[];removed=[]
    require(len(row['positive_row_domains'])==len(row['positive_removed_row_factors'])==len(row['positive_row_constants'])==k,'whole row clearing data')
    for group in row['positive_row_domains']:
        domains.extend((decode(p,True),e) for p,e in group)
    for group in row['positive_removed_row_factors']:
        removed.extend((decode(p,True),e) for p,e in group)
    require(all(type(e) is int and e>0 for p,e in domains+removed),'clearing exponent')
    constants=[F(z) for z in row['positive_row_constants']]
    require(all(z>0 for z in constants),'positive row multiplier')
    determinant_degrees=[0,0,0]
    for order in permutations(range(k)):
        if any(not a[i][order[i]][0] for i in range(k)):continue
        ds=add_degrees(*(degrees(a[i][order[i]]) for i in range(k)))
        determinant_degrees=[max(determinant_degrees[j],ds[j]) for j in range(3)]
    lhs=add_degrees(tuple(determinant_degrees),factors_degree(denominators),factors_degree(removed))
    rhs=add_degrees(degrees(shifted),factors_degree(domains))
    bounds=tuple(max(lhs[j],rhs[j]) for j in range(3))
    count=0
    for point in product(*(range(d+1) for d in bounds)):
        matrix=[[value(p,point) for p in v] for v in a]
        left=determinant(matrix)*factors_value(denominators,point)*factors_value(removed,point)
        right=value(shifted,point)*factors_value(domains,point)*prod(constants)
        require(left==right,'FULL degree-bounded Gaussian determinant identity')
        count+=1
    return {'order':k,'positive_coefficients':len(shifted[0]),'full_identity_bounds':bounds,
            'full_identity_points':count,'full_shift_bounds':shift_bounds,
            'full_shift_points':shift_points,'full_factor_shift_points':factor_shift_points,
            'coefficient_denominator':shifted[1]}

def check(data):
    require([r['order'] for r in data['rows']]==[1,2,3,4],'all four complete leading minors')
    return [check_row(row) for row in data['rows']]
