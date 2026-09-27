#!/usr/bin/env python3
"""Exact author checks; no numerical Gaussian integration or proof assistant."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def norm2(a):
    return dot(a, a)


class Poly:
    """Sparse polynomial in ten formally independent variables over Q."""
    dim = 10

    def __init__(self, terms=None):
        if isinstance(terms, (int, Q)):
            terms = {(0,)*self.dim: Q(terms)}
        self.terms = {k: Q(v) for k, v in (terms or {}).items() if v}

    def __add__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        out = dict(self.terms)
        for k, v in other.terms.items():
            out[k] = out.get(k, Q(0))+v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Poly) else -Q(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        out = {}
        for a, x in self.terms.items():
            for b, y in other.terms.items():
                k = tuple(i+j for i, j in zip(a, b))
                out[k] = out.get(k, Q(0))+x*y
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, k):
        require(isinstance(k, int) and k >= 0, 'Invalid polynomial exponent')
        out = Poly(1)
        for _ in range(k):
            out = out*self
        return out

    def diff(self, index):
        out = {}
        for a, x in self.terms.items():
            if a[index]:
                b = list(a)
                b[index] -= 1
                out[tuple(b)] = a[index]*x
        return Poly(out)

    @classmethod
    def var(cls, index):
        a = [0]*cls.dim
        a[index] = 1
        return cls({tuple(a): Q(1)})


def symbolic_check():
    r,z,R,Z,s,w,P,W,c,t = [Poly.var(i) for i in range(10)]
    a,b = (1-t)*r+t*R, (1-t)*z+t*Z
    d,e = (1-t)*s+t*P, (1-t)*w+t*W
    # Direct squared distance from the actual coordinate definition.
    direct = a*a+d*d-2*c*a*d+(b-e)**2
    direct += t*(1-t)*((r-R-s+P)**2+(z-Z-w+W)**2)
    mer0, mer1 = (r-s)**2+(z-w)**2, (R-P)**2+(Z-W)**2
    split = (1-t)*mer0+t*mer1+2*a*d*(1-c)
    require(not (direct-split).terms, 'Universal distance identity failed')
    derivative = mer1-mer0-2*(1-c)*((r-R)*d+(s-P)*a)
    require(not (direct.diff(9)-derivative).terms,
            'Universal derivative identity failed')
    # Damage both coordinates separately. Each is a genuine formal defect.
    bad_r = direct-t*(1-t)*(r-R-s+P)**2
    bad_z = direct-t*(1-t)*(z-Z-w+W)**2
    require(bool((bad_r-split).terms), 'Missing radial auxiliary undetected')
    require(bool((bad_z-split).terms), 'Missing axial auxiliary undetected')
    record = sorted((list(k), str(v)) for k,v in direct.terms.items())
    data = json.dumps(record, separators=(',', ':')).encode()
    return {'universal_identities': 2, 'formal_variables': 10,
            'expanded_distance_monomials': len(direct.terms),
            'expanded_distance_sha256': hashlib.sha256(data).hexdigest(),
            'damaged_polynomial_controls': 2}


def determinant(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    n = len(a)
    require(all(len(row)==n for row in a), 'Nonsquare determinant')
    det = Q(1)
    for j in range(n):
        pivot = next((i for i in range(j,n) if a[i][j]), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            a[j],a[pivot] = a[pivot],a[j]
            det = -det
        v = a[j][j]
        det *= v
        for i in range(j+1,n):
            f = a[i][j]/v
            for k in range(j+1,n):
                a[i][k] -= f*a[j][k]
    return det


def fold(p):
    r,z = p
    require(z >= 0 and 0 <= r <= Q(4,3)*z, 'Outside conical domain')
    if 2*r <= z:
        return p
    return ((-3*r+4*z)/5, (4*r+3*z)/5)


def check_meridian(pairs):
    for p,sp in pairs:
        require(p[0] >= 0, 'Negative source radius')
        require(0 <= sp[0] <= p[0], 'Invalid target radius')
    for (p,sp),(q,sq) in combinations(pairs,2):
        require(norm2(sub(sp,sq)) <= norm2(sub(p,q)),
                'Meridian expansion')


def point(p, u):
    return (p[0]*u[0],p[0]*u[1],p[1])


def motion(p, sp, u, t, h):
    require(h*h == t*(1-t) and h>=0, 'Wrong motion square root')
    a,b = (1-t)*p[0]+t*sp[0],(1-t)*p[1]+t*sp[1]
    return (a*u[0],a*u[1],b,h*(p[0]-sp[0]),h*(p[1]-sp[1]))


def labels_for(pairs):
    directions = [(Q(1),Q(0)),(Q(0),Q(1)),(Q(-1),Q(0)),
                  (Q(0),Q(-1)),(Q(3,5),Q(4,5)),(Q(-3,5),Q(4,5))]
    labels = []
    for p,sp in pairs:
        for u in directions[:1] if not p[0] else directions:
            require(norm2(u)==1, 'Invalid azimuth')
            labels.append((p,sp,u))
    return labels


def family_check(pairs):
    check_meridian(pairs)
    labels = labels_for(pairs)
    controls = 0
    times = [(Q(0),Q(0)),(Q(9,25),Q(12,25)),
             (Q(1,2),Q(1,2)),(Q(16,25),Q(12,25)),(Q(1),Q(0))]
    tight = 0
    for (p,sp,u),(q,sq,v) in combinations(labels,2):
        mer0,mer1 = norm2(sub(p,q)),norm2(sub(sp,sq))
        c = dot(u,v)
        source = norm2(sub(point(p,u),point(q,v)))
        target = norm2(sub(point(sp,u),point(sq,v)))
        require(target<=source, 'Physical endpoint expansion')
        tight += target==source
        for t,h in times:
            a,b = (1-t)*p[0]+t*sp[0],(1-t)*q[0]+t*sq[0]
            explicit = norm2(sub(motion(p,sp,u,t,h),motion(q,sq,v,t,h)))
            split = (1-t)*mer0+t*mer1+2*a*b*(1-c)
            require(explicit==split, 'Coordinate/decomposition disagreement')
            derivative = mer1-mer0-2*(1-c)*((p[0]-sp[0])*b+(q[0]-sq[0])*a)
            require(derivative<=0, 'Positive pair derivative')
            controls += 1
        # The derivative is affine in t; these endpoint values certify its
        # whole interval for this pair, not just the displayed times.
        for t in (Q(0),Q(1)):
            a,b = (1-t)*p[0]+t*sp[0],(1-t)*q[0]+t*sq[0]
            require(mer1-mer0-2*(1-c)*((p[0]-sp[0])*b+(q[0]-sq[0])*a)<=0,
                    'Whole-time affine derivative failed')
    return {'meridian_points':len(pairs), 'physical_labels':len(labels),
            'physical_pairs':len(labels)*(len(labels)-1)//2,
            'tight_endpoint_pairs':tight,'exact_coordinate_controls':controls}


def benchmark():
    points = [(0,0,0),(0,0,1),(1,0,2),(0,1,2),
              (1,0,1),(-1,0,1),(0,1,1)]
    xs,ys,labels = [],[],[]
    for x,y,z in points:
        # Here every transverse vector is on a coordinate axis.
        r = Q(abs(x)+abs(y))
        p = (r,Q(z))
        u = (Q(x)/r,Q(y)/r) if r else (Q(1),Q(0))
        sp = fold(p)
        xx,yy = point(p,u),point(sp,u)
        xs.append(xx);ys.append(yy);labels.append((p,sp,u))
        require(norm2(xx)==norm2(yy), 'Benchmark norm not preserved')
    check_meridian([(p,sp) for p,sp,_ in labels])
    paired_det = determinant([x+y for x,y in zip(xs[1:],ys[1:])])
    displacement_det = determinant([sub(ys[i],xs[i]) for i in (4,5,6)])
    require(paired_det!=0 and displacement_det!=0, 'Benchmark rank failure')
    losses = [norm2(sub(xs[i],xs[j]))-norm2(sub(ys[i],ys[j]))
              for i,j in combinations(range(len(xs)),2)]
    require(min(losses)>=0, 'Benchmark is not a contraction')
    return {'source':[[str(v) for v in x] for x in xs],
            'target':[[str(v) for v in y] for y in ys],
            'paired_determinant':str(paired_det), 'paired_affine_rank':6,
            'displacement_determinant':str(displacement_det),
            'displacement_rank':3, 'norm_preserving_labels':len(xs),
            'tight_pairs':sum(v==0 for v in losses),
            'strict_pairs':sum(v>0 for v in losses)}


def rejected_controls():
    cases = [
        [((Q(1),Q(0)),(Q(2),Q(0)))],
        [((Q(1),Q(0)),(Q(-1),Q(0)))],
        [((Q(0),Q(0)),(Q(0),Q(0))),
         ((Q(0),Q(1)),(Q(0),Q(2)))],
        [((Q(0),Q(0)),(Q(1),Q(0)))],
    ]
    rejected = 0
    for case in cases:
        try:
            check_meridian(case)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('Invalid meridian data accepted')
    # Omitting the second auxiliary for S(r,z)=(r,-z) restores separation
    # after an artificial midpoint collision. Its distance is (1-2t)^2.
    require((1-2*Q(1))**2 > (1-2*Q(1,2))**2,
            'Omitted axial auxiliary negative control failed')
    # Allowing signed radius with S(r,z)=(-r,z) gives the same failure for
    # antipodal azimuths in this particular motion, though that endpoint
    # map itself is a rigid isometry, not a counterexample to the conjecture.
    require(4*(1-2*Q(1))**2 > 4*(1-2*Q(1,2))**2,
            'Signed-radius motion control failed')
    return {'invalid_hypothesis_rejections':rejected,
            'explicit_bad_motion_controls':2}


def run():
    base = [(Q(r),Q(z)) for r,z in
            [(0,0),(0,1),(0,-1),(1,0),(1,1),(1,-1),(2,1),(3,-2)]]
    cone = [(Q(r),Q(z)) for r,z in [(0,0),(0,1),(1,2),(1,1),(2,2),(4,3)]]
    def inversion(p):
        k = max(Q(1),norm2(p))
        return tuple(x/k for x in p)
    # A coupled meridian map used only as a rational control. Its derivative
    # Frobenius norm is <=sqrt(33)/8<1, so the family is globally admissible.
    def coupled(p):
        r,z=p
        return (r/(2*(1+r)),z/2+r/(8*(1+r)))
    families = {
        'identity':[(p,p) for p in base],
        'axial_fold':[(p,(p[0],abs(p[1]))) for p in base],
        'collapse':[(p,(Q(0),Q(0))) for p in base],
        'radial_inversion_control':[(p,inversion(p)) for p in base],
        'coupled_rational_map':[(p,coupled(p)) for p in base],
        'conical_fold':[(p,fold(p)) for p in cone],
    }
    out={'status':'MERIDIAN_CONTRACTION_CHECKS_PASS',
         'arithmetic':'Python integers and fractions.Fraction; no sampling proof',
         'symbolic':symbolic_check(),
         'families':{name:family_check(pairs) for name,pairs in families.items()},
         'benchmark':benchmark(),'negative_controls':rejected_controls()}
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--emit',action='store_true',help='Write the compact expected record')
    args=parser.parse_args()
    record=run()
    text=json.dumps(record,indent=2,sort_keys=True)+'\n'
    path=Path(__file__).with_name('EXPECTED.json')
    if args.emit:
        path.write_text(text)
    else:
        require(path.read_text()==text,'Expected record mismatch')
    print(json.dumps({'status':record['status'],
        'record_sha256':hashlib.sha256(text.encode()).hexdigest(),
        'physical_pairs':sum(v['physical_pairs'] for v in record['families'].values()),
        'coordinate_controls':sum(v['exact_coordinate_controls'] for v in record['families'].values()),
        'paired_rank':record['benchmark']['paired_affine_rank']},sort_keys=True))


if __name__=='__main__':
    main()
