#!/usr/bin/env python3
"""Whole degree-nine four-level angular author certificate.

Actual author six-sendov-2, researcher. Exact rational trace identities,
closed polygon/fan coverage, continuous Bernstein bounds and independent
full-compression controls. Standard library only; no campaign import,
external solver or floating proof input. Kernel openly adapts the author's
four-double source. Written spectral and asymptotic bridges remain outside
a formal system; independent review of this extension is pending.
"""
from fractions import Fraction as F
from itertools import product, combinations, combinations_with_replacement
from math import comb
from pathlib import Path
import argparse, hashlib, json

CHECKS=0
def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(message)

class P:
    """Sparse exact Q[x0,x1,x2]; exponent order is explicit and fixed."""
    def __init__(self, value=0):
        if isinstance(value, P):
            value = value.t
        if isinstance(value, (int, F)):
            value = {(0, 0, 0): F(value)}
        self.t = {tuple(e): F(c) for e, c in value.items() if c}
        if any(len(e) != 3 or any(k < 0 for k in e) for e in self.t):
            raise ValueError('invalid polynomial exponent')

    def __add__(self, other):
        out = dict(self.t)
        for e, c in P(other).t.items():
            out[e] = out.get(e, F(0)) + c
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.t.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        out = {}
        for e, c in self.t.items():
            for h, b in P(other).t.items():
                k = tuple(x+y for x, y in zip(e, h))
                out[k] = out.get(k, F(0)) + c*b
        return P(out)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1/F(scalar))

    def __pow__(self, n):
        if n < 0:
            raise ValueError('negative polynomial power')
        out, a = P(1), self
        while n:
            if n & 1:
                out *= a
            a *= a
            n //= 2
        return out

    def __eq__(self, other):
        return self.t == P(other).t

    def dump(self):
        return [[*e, str(c)] for e, c in sorted(self.t.items())]

def subst(poly, variables):
    powers = []
    for axis, v in enumerate(variables):
        degree = max((e[axis] for e in poly.t), default=0)
        row = [P(1)]
        for _ in range(degree):
            row.append(row[-1]*P(v))
        powers.append(row)
    out = P(0)
    for e, c in poly.t.items():
        term = P(c)
        for axis, k in enumerate(e):
            term *= powers[axis][k]
        out += term
    return out

def scalar(poly, values):
    out = subst(poly, values)
    require(not any(any(e) for e in out.t), 'evaluation is scalar')
    return out.t.get((0, 0, 0), F(0))

def derivative(poly, axis):
    return P({tuple(k-1 if i == axis else k for i, k in enumerate(e)):
              e[axis]*c for e, c in poly.t.items() if e[axis]})

def remove_monomial(poly, axis, power, name):
    require(all(e[axis] >= power for e in poly.t), name+' divisibility')
    reduced = P({tuple(k-power if i == axis else k for i, k in enumerate(e)):
                 c for e, c in poly.t.items()})
    variable = (X, H, U)[axis]
    require(reduced*variable**power == poly, name+' reconstruction')
    return reduced

def prod(values):
    out = P(1)
    for v in values:
        out *= v
    return out

def affine_power(poly, box):
    """Binomial affine substitution performed one axis at a time."""
    data = dict(poly.t)
    for axis, (a, b) in enumerate(box):
        out = {}
        for e, c in data.items():
            for k in range(e[axis]+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*comb(e[axis], k)*a**(e[axis]-k)*(b-a)**k
        data = {e: c for e, c in out.items() if c}
    return data

def bernstein(poly, box):
    degrees = tuple(max((e[i] for e in poly.t), default=0) for i in range(3))
    normalized = affine_power(poly, box)
    data = dict(normalized)
    for axis, degree in enumerate(degrees):
        out = {}
        for e, c in data.items():
            for k in range(e[axis], degree+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*F(comb(k, e[axis]), comb(degree, e[axis]))
        data = {e: c for e, c in out.items() if c}
    indices = list(product(*(range(n+1) for n in degrees)))
    coefficients = [data.get(e, F(0)) for e in indices]
    # Independent inverse basis identity in the normalized power coordinates.
    inverse = dict(data)
    for axis, degree in enumerate(degrees):
        out = {}
        for e, c in inverse.items():
            for k in range(e[axis], degree+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*comb(degree, k)*comb(k, e[axis])*(-1)**(k-e[axis])
        inverse = {e: c for e, c in out.items() if c}
    require(inverse == normalized, 'complete inverse Bernstein reconstruction')
    return coefficients, degrees

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def certificate(name, poly, box, strict=False):
    require(len(box) == 3 and all(a < b for a, b in box), name+' genuine box')
    coefficients, degrees = bernstein(poly, box)
    for value in coefficients:
        require(value > 0 if strict else value >= 0, name+' Bernstein sign')
    return {'name': name, 'box': [[str(a), str(b)] for a, b in box],
            'degrees': list(degrees), 'entries': len(coefficients),
            'zero': sum(c == 0 for c in coefficients), 'minimum': str(min(coefficients)),
            'polynomial_sha256': digest(poly.dump()),
            'coefficient_sha256': digest(list(map(str, coefficients)))}

def solve(a, b):
    n = len(b)
    a = [list(r)+[v] for r, v in zip(a, b)]
    for j in range(n):
        pivots = [i for i in range(j, n) if a[i][j]]
        require(bool(pivots), 'nonzero Gaussian pivot')
        i = pivots[0]
        a[j], a[i] = a[i], a[j]
        t = a[j][j]
        a[j] = [v/t for v in a[j]]
        for i in range(j+1, n):
            t = a[i][j]
            if t:
                a[i] = [u-t*v for u, v in zip(a[i], a[j])]
    out = [F(0)]*n
    for j in range(n-1, -1, -1):
        out[j] = a[j][-1]-sum(a[j][k]*out[k] for k in range(j+1, n))
    return out

def independent_rows(rows):
    pivots, selected = {}, []
    for original in rows:
        r = list(original)
        for j, b in sorted(pivots.items()):
            t = r[j]
            if t:
                r = [u-t*v for u, v in zip(r, b)]
        if any(r):
            j = next(j for j, v in enumerate(r) if v)
            t = r[j]
            pivots[j] = [v/t for v in r]
            selected.append(original)
    return selected

def pinching(theta):
    """Rational Frobenius projection of ww* to the symmetric commutant."""
    n = 8
    require(len(theta) == n and sum(theta) == 0, 'balanced definition control')
    a = [[(theta[i] if i == j else 0)-(theta[i]+theta[j])/n
          for j in range(n)] for i in range(n)]
    pairs = list(combinations_with_replacement(range(n), 2))
    weights = [F(1 if i == j else 2) for i, j in pairs]
    w = [theta[i]*theta[j]/n for i, j in pairs]
    all_rows = []
    for i in range(n):
        for j in range(i+1, n):
            row = []
            for h, k in pairs:
                v = (a[i][h] if k == j else 0)-(a[k][j] if i == h else 0)
                if h != k:
                    v += (a[i][k] if h == j else 0)-(a[h][j] if i == k else 0)
                row.append(v)
            all_rows.append(row)
    rows = independent_rows(all_rows)
    rhs = [sum(c*v for c, v in zip(row, w)) for row in rows]
    gram = [[sum(c*d/g for c, d, g in zip(row, other, weights))
             for other in rows] for row in rows]
    lam = solve(gram, rhs)
    projected = [v-sum(row[k]*b for row, b in zip(rows, lam))/weights[k]
                 for k, v in enumerate(w)]
    for row in all_rows:
        require(sum(c*v for c, v in zip(row, projected)) == 0,
                'original commutation constraint')
    residual = [u-v for u, v in zip(w, projected)]
    require(sum(g*u*v for g, u, v in zip(weights, projected, residual)) == 0,
            'Frobenius orthogonality')
    return sum(g*v*v for g, v in zip(weights, projected)), len(rows)

def interval_add(a, b):
    return a[0]+b[0], a[1]+b[1]

def interval_mul(a, b):
    values = [x*y for x in a for y in b]
    return min(values), max(values)

def interval_poly(coefficients, box):
    out = F(0), F(0)
    for c in reversed(coefficients):
        out = interval_add(interval_mul(out, box), (F(c), F(c)))
    return out
X,H,U=[P({tuple(int(i==j) for j in range(3)):1}) for i in range(3)]


def mm(a,b):
    return [[sum((a[i][j]*b[j][h] for j in range(3)),P(0))
             for h in range(3)] for i in range(3)]

def madd(a,b):
    return [[a[i][j]+b[i][j] for j in range(3)] for i in range(3)]

def scale(a,c):
    return [[v*c for v in row] for row in a]

def trace(a):
    return sum((a[i][i] for i in range(3)), P(0))

def det(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))

def adj(a):
    out=[]
    for i in range(3):
        row=[]
        for j in range(3):
            rows=[h for h in range(3) if h!=j]
            cols=[h for h in range(3) if h!=i]
            row.append((-1)**(i+j)*(a[rows[0]][cols[0]]*a[rows[1]][cols[1]]
                                     -a[rows[0]][cols[1]]*a[rows[1]][cols[0]]))
        out.append(row)
    return out

def exact_div(poly,divisor):
    """Exact lexicographic multivariate long division; check reconstruction."""
    divisor=P(divisor)
    if not divisor.t:
        raise ValueError('zero divisor')
    lead=max(divisor.t)
    q,out=P(0),P(poly)
    while out.t:
        e=max(out.t)
        if any(x<y for x,y in zip(e,lead)):
            raise ValueError('nonzero polynomial remainder')
        mon=P({tuple(x-y for x,y in zip(e,lead)):
               out.t[e]/divisor.t[lead]})
        q+=mon
        out-=mon*divisor
    if q*divisor!=poly:
        raise ValueError('division reconstruction')
    return q


from functools import cmp_to_key
Y=H

def pmul(a,b):
    out=[P(0)]*(len(a)+len(b)-1)
    for i,c in enumerate(a):
        for j,d in enumerate(b):out[i+j]+=c*d
    return out

def roots_poly(roots):
    out=[P(1)]
    for root in roots:out=pmul(out,[-P(root),P(1)])
    return out

def peval(coefficients,matrix):
    eye=[[P(int(i==j)) for j in range(3)] for i in range(3)]
    out=scale(eye,0)
    for coefficient in reversed(coefficients):
        out=madd(mm(out,matrix),scale(eye,coefficient))
    return out

def weighted_oracle(masses):
    m,n,h,l=masses
    levels=[P(-1),X,Y,(m-n*X-h*Y)/l]
    g=roots_poly(levels)
    q=[P(0)]*4
    for i,mass in enumerate(masses):
        term=roots_poly([root for j,root in enumerate(levels) if i!=j])
        q=[a+mass*b for a,b in zip(q,term)]
    require(q[-1]==8,'weighted active cubic leading8')
    require(sum((mass*root for mass,root in zip(masses,levels)),P(0))==0,
              'weighted balance')
    hp=roots_poly([root for mass,root in zip(masses,levels) for _ in range(mass)])
    inactive=roots_poly([root for mass,root in zip(masses,levels) for _ in range(mass-1)])
    derivative=[i*c for i,c in enumerate(hp) if i]
    require(derivative==pmul(inactive,q),'complete derivative factorization')
    matrix=[[P(0),P(0),-q[0]/8],[P(1),P(0),-q[1]/8],
            [P(0),P(1),-q[2]/8]]
    require(peval(q,matrix)==scale(matrix,0),'companion cubic relation')
    yp=peval([i*c for i,c in enumerate(q) if i],matrix)
    delta=q[2]**2*q[1]**2-32*q[1]**3-4*q[2]**3*q[0]-1728*q[0]**2+144*q[2]*q[1]*q[0]
    require(det(yp)==-delta/8,'discriminant / resultant')
    fp=scale(peval(g,matrix),-8)
    ad=adj(yp)
    eye=[[P(int(i==j)) for j in range(3)] for i in range(3)]
    require(mm(yp,ad)==scale(eye,-delta/8),'adjugate identity')
    cleared=64*trace(mm(mm(fp,fp),mm(ad,ad)))
    pn=exact_div(cleared,delta)
    require(cleared==delta*pn,'weighted trace discriminant cancellation')
    mu2=sum((mass*root**2 for mass,root in zip(masses,levels)),P(0))
    mu4=sum((mass*root**4 for mass,root in zip(masses,levels)),P(0))
    nn=(122*mu2*mu2+224*mu4)*delta-5760*pn
    dd=mu2*delta
    return nn,dd,pn,delta,levels,mu2,mu4

def determinant(a,b):return a[0]*b[1]-a[1]*b[0]

def polygon(masses):
    m,n,h,l=map(F,masses)
    lines=[(F(1),F(0),-F(1)),(F(1),F(0),F(1)),
           (F(0),F(1),-F(1)),(F(0),F(1),F(1)),
           (n,h,m-l),(n,h,m+l)]
    vertices=set()
    for (a,b,c),(d,e,f) in combinations(lines,2):
        det=a*e-b*d
        if not det:continue
        x,y=(c*e-b*f)/det,(a*f-c*d)/det
        z=(m-n*x-h*y)/l
        if max(abs(x),abs(y),abs(z))<=1:vertices.add((x,y))
    center=m/(8-m)
    if m==4:
        require(vertices=={(F(1),F(1))},'saturated mass4 is binary only')
        return (center,center),list(vertices)
    require(m<4 and abs(center)<1,'strictly interior fan center')
    def half(v):
        dx,dy=v[0]-center,v[1]-center
        return int(dy<0 or dy==0 and dx<0)
    def compare(a,b):
        if half(a)!=half(b):return -1 if half(a)<half(b) else 1
        cross=determinant((a[0]-center,a[1]-center),(b[0]-center,b[1]-center))
        return -1 if cross>0 else 1 if cross<0 else 0
    vertices=sorted(vertices,key=cmp_to_key(compare))
    require(len(vertices)>=3,'genuine complete rational polygon')
    for i,a in enumerate(vertices):
        b=vertices[(i+1)%len(vertices)]
        direction=(b[0]-a[0],b[1]-a[1])
        require(determinant(direction,(center-a[0],center-a[1]))>0,
                  'fan orientation / center interior')
        require(all(determinant(direction,(p[0]-a[0],p[1]-a[1]))>=0
                      for p in vertices),'all vertices on the inner edge side')
        require(any(aa*a[0]+bb*a[1]==cc==aa*b[0]+bb*b[1]
                      for aa,bb,cc in lines),'boundary edge is an exact original face')
    return (center,center),vertices

def fans(masses):
    center,vertices=polygon(masses)
    for i,a in enumerate(vertices):
        b=vertices[(i+1)%len(vertices)]
        yield i,center,a,b,[P(center[j])+X*((1-Y)*(a[j]-center[j])+Y*(b[j]-center[j]))
                             for j in range(2)]+[P(0)]


def coverage_tree(tree,box,pol,disc,moment,label):
    """Validate every closed child and recompute every coefficient sign."""
    if isinstance(tree,str):
        require(tree in ('trace','low_moment'),label+' allowed leaf type')
        if tree=='trace':
            records=[certificate(label+' bound',pol,box),
                     certificate(label+' discriminant',disc,box)]
        else:
            records=[certificate(label+' mu2<=6',moment,box)]
        area=(box[0][1]-box[0][0])*(box[1][1]-box[1][0])
        return records,area,1
    require(isinstance(tree,list) and len(tree)==3,label+' both children required')
    axis,left,right=tree
    require(type(axis) is int and axis in (0,1),label+' genuine two-dimensional split')
    a,b=box[axis]
    mid=(a+b)/2
    records=[]
    area=F(0)
    leaves=0
    for child,pair in ((left,(a,mid)),(right,(mid,b))):
        childbox=list(box)
        childbox[axis]=pair
        row,size,count=coverage_tree(child,childbox,pol,disc,moment,label)
        records.extend(row)
        area+=size
        leaves+=count
    require(area==(box[0][1]-box[0][0])*(box[1][1]-box[1][0]),
            label+' complete closed cover area')
    return records,area,leaves


def scalar_value(poly,point):
    return scalar(poly,[*point,0])


def control(masses,levels,point,nn,dd,pn,delta,label):
    theta=[scalar_value(root,point) for mass,root in zip(masses,levels)
           for _ in range(mass)]
    require(sum(theta)==0 and max(map(abs,theta))==1,label+' normalized balance')
    psi,rank=pinching(theta)
    mu2=sum(root*root for root in theta)
    mu4=sum(root**4 for root in theta)
    jj=(122*mu2*mu2+224*mu4-5760*psi)/mu2
    den=scalar_value(delta,point)
    if den:
        require(den>0 and scalar_value(pn,point)/den==psi,
                label+' full compression versus weighted trace')
        require(scalar_value(nn,point)/scalar_value(dd,point)==jj,
                label+' full compression versus angular oracle')
    else:
        require(len(set(theta))==2,label+' zero discriminant is an actual binary profile')
        require(psi==(mu2/8)**2 and jj==32*mu2+224*mu4/mu2,
                label+' direct singular pinching; no division')
        require(scalar_value(pn,point)==0 and scalar_value(nn,point)==0,
                label+' singular cleared polynomials vanish')
    require(jj<=780,label+' certified cohort control')
    return {'label':label,'point':list(map(str,point)),'theta':list(map(str,theta)),
            'Psi':str(psi),'J':str(jj),'commutant_rank':rank,'generic':bool(den)}


def build(data):
    initial_checks=CHECKS
    require(set(data)=={'format','cases'} and
            data['format']=='closed-unit-square-bisection-trees-v1',
            'exact coverage input schema')
    require(isinstance(data['cases'],list),'coverage list')
    lookup={}
    for row in data['cases']:
        require(set(row)=={'masses','fan','tree'},'exact coverage row fields')
        require(isinstance(row['masses'],list) and len(row['masses'])==4 and
                all(type(m) is int and m>0 for m in row['masses']) and
                sum(row['masses'])==8 and type(row['fan']) is int and row['fan']>=0,
                'integer positive multiplicities and genuine fan index')
        key=tuple(row['masses']),row['fan']
        require(key not in lookup,'no duplicated cohort/fan input')
        lookup[key]=row['tree']
    expected_partitions={(5,1,1,1),(4,2,1,1),(3,3,1,1),(3,2,2,1),(2,2,2,2)}
    all_partitions={tuple(sorted(p,reverse=True)) for p in
                    combinations_with_replacement(range(1,9),4) if sum(p)==8}
    require(all_partitions==expected_partitions,'all five four-part partitions of8')
    # Trace/moment cohorts are new; the two remaining nontrivial cohort
    # bounds and the value/orbit of J* are explicit credited proof inputs.
    classes=[(3,2,2,1),(4,2,1,1)]
    expected_keys=set()
    output=[]
    controls=[]
    total_entries=0
    total_leaves=0
    unit=(F(0),F(1))
    for partition in classes:
        for saturated in sorted(set(partition),reverse=True):
            remaining=list(partition)
            remaining.remove(saturated)
            masses=[saturated,*sorted(remaining,reverse=True)]
            center,vertices=polygon(masses)
            if saturated==4:
                require(vertices==[(F(1),F(1))],'saturated four is only4+4')
                continue
            nn,dd,pn,delta,levels,mu2,mu4=weighted_oracle(masses)
            label='-'.join(map(str,masses))
            item={'masses':masses,'center':list(map(str,center)),
                  'vertices':[list(map(str,p)) for p in vertices],
                  'oracle_sha256':{name:digest(poly.dump()) for name,poly in
                    zip(('n','d','Psi_numerator','discriminant','mu2','mu4'),
                        (nn,dd,pn,delta,mu2,mu4))},'fans':[]}
            polygon_twice=sum(determinant(a,vertices[(i+1)%len(vertices)])
                              for i,a in enumerate(vertices))
            triangle_twice=sum(determinant((a[0]-center[0],a[1]-center[1]),
                              (vertices[(i+1)%len(vertices)][0]-center[0],
                               vertices[(i+1)%len(vertices)][1]-center[1]))
                              for i,a in enumerate(vertices))
            require(polygon_twice>0 and polygon_twice==triangle_twice,
                    label+' complete positive-area fan')
            for i,c,a,b,chart in fans(masses):
                key=tuple(masses),i
                expected_keys.add(key)
                require(key in lookup,label+' every fan required')
                pol=remove_monomial(subst(780*dd-nn,chart),0,2,label+' fan bound')
                disc=remove_monomial(subst(delta,chart),0,2,label+' fan discriminant')
                moment=subst(6-mu2,chart)
                records,area,leaves=coverage_tree(lookup[key],[unit]*3,
                              pol,disc,moment,label+' fan'+str(i))
                require(area==1,label+' full fan parameter square')
                total_entries+=sum(row['entries'] for row in records)
                total_leaves+=leaves
                item['fans'].append({'fan':i,'start':list(map(str,a)),
                    'end':list(map(str,b)),'leaves':leaves,'certificates':records})
            # Definition controls: central triple collision, every polygon
            # vertex, and two varying generic directions, independent of
            # the cubic residue implementation.
            points=[center,*vertices]
            fan_rows=list(fans(masses))
            for fan_index,rho,v in ((0,F(1,2),F(1,3)),(-1,F(3,4),F(2,3))):
                chart=fan_rows[fan_index][-1]
                points.append(tuple(scalar(poly,[rho,v,0]) for poly in chart[:2]))
            for index,point in enumerate(points):
                controls.append(control(masses,levels,point,nn,dd,pn,delta,
                                        label+' control'+str(index)))
            output.append(item)
    require(set(lookup)==expected_keys,'no omitted or extra cohort/fan domains')
    require(len(expected_keys)==20 and total_leaves==30 and total_entries==3020,
            'complete continuous-domain certificate totals')
    require(F(5760,192)==30 and 122-30==92 and 92*6+224==776,
            'three-active-mode moment bound')
    require(F(8*3,5)==F(24,5) and 92*F(24,5)+224==F(3328,5)<780,
            'heavy5 cohort exclusion')
    require(32*8+224==480<780,'every actual binary profile is excluded')
    theta=[F(-1)]*4+[F(1)]*4
    psi,rank=pinching(theta)
    require(psi==1,'saturated4 definition pinching')
    jj=122*8+224-F(5760,8)
    require(jj==480,'saturated4 binary objective')
    controls.append({'label':'saturated4','theta':list(map(str,theta)),
                     'Psi':str(psi),'J':str(F(jj)),'commutant_rank':rank})
    theta=[F(1)]*3+[F(-1)]*3+[F(1,3),F(-1,3)]
    psi,rank=pinching(theta)
    mu2=sum(q*q for q in theta)
    mu4=sum(q**4 for q in theta)
    jj=(122*mu2*mu2+224*mu4-5760*psi)/mu2
    require(jj==F(5472,7)>780,'credited larger candidate definition control')
    controls.append({'label':'credited3+3+1+1 comparison','theta':list(map(str,theta)),
                     'Psi':str(psi),'J':str(jj),'commutant_rank':rank})
    require(len(controls)==37,'complete independent compression-control count')
    require(F(13,8)**4/F(10985,33554432)==F(106496,5),
            'credited original-root displacement normalization')
    return {'author':'six-sendov-2','role':'researcher',
            'scope':'all balanced max-normalized eight-vectors with at most four distinct levels',
            'proof_status':'ordinary author proof and exact certificate; independent review pending',
            'new_cohort_bound':'780','heavy5_bound':'3328/5',
            'partitions':[list(p) for p in sorted(expected_partitions,reverse=True)],
            'new_cohorts':output,'new_sign_coefficients':total_entries,
            'fans':len(expected_keys),'leaves':total_leaves,
            'full_compression_controls':controls,'checks':CHECKS-initial_checks,
            'credited_global_value_and_orbit':'J* from the full3+3+1+1 theorem; not rederived here'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cover',type=Path,default=Path(__file__).with_name('cover.json'))
    parser.add_argument('--manifest',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-manifest',action='store_true',help='author regeneration only')
    args=parser.parse_args()
    require(args.cover.is_file(),'required closed-domain cover is absent')
    if not args.write_manifest:
        require(args.manifest.is_file(),'required regression manifest is absent')
    result=build(json.loads(args.cover.read_text()))
    if args.write_manifest:
        args.manifest.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:
        require(result==json.loads(args.manifest.read_text()),'complete exact manifest equality')
    print(json.dumps({'status':'PASS','checks':CHECKS,
                      'new_sign_coefficients':result['new_sign_coefficients'],
                      'fans':result['fans'],'leaves':result['leaves'],
                      'full_compression_controls':len(result['full_compression_controls']),
                      'canonical_record_sha256':digest(result)},sort_keys=True))


if __name__=='__main__':main()
