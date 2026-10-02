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
        require(len(ex)==2 and all(type(e) is int and e>=0 for e in ex),'two nonnegative exponents')
        require(ex not in terms and value,'unique nonzero coefficient')
        terms[ex]=value
    if positive:
        require(terms.get((0,0),0)>0 and all(v>=0 for v in terms.values()),'strict coefficientwise positivity')
    return terms,den

def degrees(p):
    return tuple(max((ex[j] for ex in p[0]),default=0) for j in range(2))

def value(p,point):
    terms,den=p
    maxdeg=degrees(p);powers=[[x**d for d in range(maxdeg[j]+1)] for j,x in enumerate(point)]
    result=sum(co*powers[0][ex[0]]*powers[1][ex[1]] for ex,co in terms.items())
    return F(result,den)

def add_degrees(*xs):
    return tuple(sum(x[j] for x in xs) for j in range(2))

def factors_degree(xs):
    return tuple(sum(degrees(p)[j]*e for p,e in xs) for j in range(2))

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
    bounds=(max((ex[0]+ex[1] for ex in original[0]),default=0),max((ex[1] for ex in original[0]),default=0))
    require(all(degrees(shifted)[j]<=bounds[j] for j in range(2)),'exact separate substitution bounds')
    count=0
    for point in product(*(range(b+1) for b in bounds)):
        u,v=point
        require(value(original,(2+u,8+4*u+v))==value(shifted,point),'complete quadrant polynomial identity')
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
        denominators.append((old,f['power']))
    a=[[decode(p) for p in v] for v in row['cleared_original_matrix']]
    require(len(a)==k and all(len(v)==k for v in a),'whole principal-prefix matrix')
    domains=[];removed=[];clearing_shift_points=0
    require(len(row['positive_row_domains'])==len(row['positive_removed_row_factors'])==len(row['positive_row_constants'])==k,'whole row clearing data')
    for group in row['positive_row_domains']:

        for f in group:
            old,new=decode(f['original']),decode(f['shifted'],True)
            _,points=shift_identity(old,new);clearing_shift_points+=points;domains.append((old,f['power']))
    for group in row['positive_removed_row_factors']:

        for f in group:
            old,new=decode(f['original']),decode(f['shifted'],True)
            _,points=shift_identity(old,new);clearing_shift_points+=points;removed.append((old,f['power']))
    require(all(type(e) is int and e>0 for p,e in domains+removed),'clearing exponent')
    constants=[F(z) for z in row['positive_row_constants']]
    require(all(z>0 for z in constants),'positive row multiplier')
    determinant_degrees=[0,0]
    for order in permutations(range(k)):
        if any(not a[i][order[i]][0] for i in range(k)):continue
        ds=add_degrees(*(degrees(a[i][order[i]]) for i in range(k)))
        determinant_degrees=[max(determinant_degrees[j],ds[j]) for j in range(2)]
    lhs=add_degrees(tuple(determinant_degrees),factors_degree(denominators),factors_degree(removed))
    rhs=add_degrees(degrees(original),factors_degree(domains))
    bounds=tuple(max(lhs[j],rhs[j]) for j in range(2))
    count=0
    for point in product(*(range(d+1) for d in bounds)):
        matrix=[[value(p,point) for p in v] for v in a]
        left=determinant(matrix)*factors_value(denominators,point)*factors_value(removed,point)
        right=value(original,point)*factors_value(domains,point)*prod(constants)
        require(left==right,'FULL degree-bounded Gaussian determinant identity')
        count+=1
    return {'order':k,'positive_coefficients':len(shifted[0]),'full_identity_bounds':bounds,
            'full_identity_points':count,'full_shift_bounds':shift_bounds,
            'full_shift_points':shift_points,'full_factor_shift_points':factor_shift_points,'full_clearing_factor_shift_points':clearing_shift_points,
            'coefficient_denominator':shifted[1]}

def check(data):
    expected=[(name,1) for name in ('mu','alpha','beta','etaP','nuT')]
    expected +=[(name,k) for name in ('anti','triangle','final') for k in (1,2)]
    expected += [('augmented',k) for k in range(1,5)]
    require([(r['group'],r['order']) for r in data['rows']]==expected,'all15 complete scalar/minor obligations')
    return [dict(check_row(row),group=row['group']) for row in data['rows']]
