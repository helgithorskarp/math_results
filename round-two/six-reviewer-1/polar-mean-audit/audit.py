#!/usr/bin/env python3
"""Independent polar audit: closed-integral interpolation and exact certificates.

No author code or fixture is needed. The written variational and analytic
proof is in REVIEW.md; finite controls are not a proof by sampling.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def trim(v):
    v = list(map(F, v))
    while len(v) > 1 and not v[-1]:
        v.pop()
    return v


def plus(a, b):
    return trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def times(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def scale(a, c):
    return trim([c * x for x in a])


def evaluate(a, x):
    out = F(0)
    for v in reversed(a):
        out = out * x + v
    return out


def interpolate(nodes, values):
    """Newton divided differences, followed by exact power reconstruction."""
    differences = list(values)
    newton = [differences[0]]
    for order in range(1, len(nodes)):
        differences = [(differences[j + 1] - differences[j]) /
                       (nodes[j + order] - nodes[j])
                       for j in range(len(differences) - 1)]
        newton.append(differences[0])
    out, basis = [F(0)], [F(1)]
    for i, v in enumerate(newton):
        out = plus(out, scale(basis, v))
        basis = times(basis, [-nodes[i], F(1)])
    require(all(evaluate(out, x) == y for x, y in zip(nodes, values)), 'interpolation residual')
    return out


def integral_values(a):
    b = 1 - a * a
    if not b:
        return a ** 8, a ** 6 / 2
    endpoint = a + b
    H = (endpoint ** 9 - a ** 9) / (9 * b)
    T = ((endpoint ** 8 - a ** 8) / 8 - a * (endpoint ** 7 - a ** 7) / 7) / (b * b)
    return H, T


def compose(a, left, right):
    out = [F(0)]
    for v in reversed(a):
        out = plus(times(out, [left, right - left]), [v])
    return out


def bernstein(a, n):
    """Triangular elimination against the actual Bernstein basis coefficients."""
    require(len(a) <= n + 1, 'Bernstein degree bound')
    residual = list(a) + [F(0)] * (n + 1 - len(a))
    out, reconstructed = [], [F(0)] * (n + 1)
    for i in range(n + 1):
        value = residual[i] / comb(n, i)
        out.append(value)
        for k in range(i, n + 1):
            contribution = value * comb(n, i) * comb(n - i, k - i) * (-1) ** (k - i)
            residual[k] -= contribution
            reconstructed[k] += contribution
    require(not any(residual) and trim(reconstructed) == trim(a), 'complete Bernstein inverse')
    return out


def midpoint_split(v):
    """A separate de Casteljau check of interval restriction."""
    layers = [v]
    while len(layers[-1]) > 1:
        layers.append([(a + b) / 2 for a, b in zip(layers[-1], layers[-1][1:])])
    return [row[0] for row in layers], [row[-1] for row in reversed(layers)]


def digest(v):
    return sha256(json.dumps([str(x) for x in v], separators=(',', ':')).encode()).hexdigest()


def scalar_certificate():
    nodes = [F(i, 16) for i in range(17)]
    values = [integral_values(a) for a in nodes]
    H = interpolate(nodes, [x[0] for x in values])
    T = interpolate(nodes, [x[1] for x in values])
    require((len(H), len(T)) == (17, 13), 'written integral degree bounds')
    delta, D, a, b = [F(1), F(-1)], [F(4), F(-3)], [F(0), F(1)], [F(1), F(0), F(-1)]
    J = times(b, T)
    numerator = plus(times(D, plus([F(1)], scale(H, -1))), scale(times(times(a, delta), J), 8))
    # A different division: interpolate the quotient on 16 points excluding a=1,
    # then verify the entire degree17 polynomial identity, including the endpoint.
    quotient_nodes = nodes[:-1]
    P = interpolate(quotient_nodes, [evaluate(numerator, x) / (1 - x) ** 2 for x in quotient_nodes])
    require(len(P) == 16 and times(times(delta, delta), P) == numerator, 'full double-zero division identity')
    R = plus(P, scale(D, -F(8, 9)))
    W = plus(P, scale(T, -F(16, 5)))
    original = {'R': bernstein(R, 15), 'W': bernstein(W, 15)}
    require(all(x >= 0 for x in original['R']) and [i for i,x in enumerate(original['R']) if x == 0] == [0],
            'original low-mean certificate and exact zero support')
    require(min(original['W']) == F(7346, 20475) > 0, 'original strict mean certificate')
    coefficient = F(47, 100)
    improved = plus(P, scale(T, -8 * coefficient))
    full = bernstein(improved, 15)
    cells = [bernstein(compose(improved, F(0), F(1,2)), 15),
             bernstein(compose(improved, F(1,2), F(1)), 15)]
    require(tuple(cells) == midpoint_split(full), 'independent interval restriction algorithms agree')
    require(all(x > 0 for cell in cells for x in cell), 'strict47/100 uniform refinement')
    require(min(x for cell in cells for x in cell) == F(7799537, 1729728000), 'refinement minimum')
    polys = {'H':H, 'T':T, 'P':P, 'R':R, 'W':W}
    return polys, {'closed_integral_interpolation_points':17, 'quotient_interpolation_points':16,
                   'full_defect_identity':True, 'power_sha256':{name:digest(v) for name,v in polys.items()},
                   'original_bernstein':{name:list(map(str,v)) for name,v in original.items()},
                   'original_sign_coefficients':32, 'original_W_minimum':str(min(original['W'])),
                   'refined_coefficient':str(coefficient), 'refined_intervals':['[0,1/2]','[1/2,1]'],
                   'refined_sign_coefficients':32, 'refined_bernstein':[list(map(str,v)) for v in cells],
                   'refined_minimum':str(min(x for cell in cells for x in cell)),
                   'interval_composition_matches_de_Casteljau':True}


def gauss_add(x, y):
    return x[0] + y[0], x[1] + y[1]


def gauss_mul(x, y):
    return x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0]


def gauss_div(x, y):
    denominator = y[0] ** 2 + y[1] ** 2
    require(denominator > 0, 'nonzero Gaussian divisor')
    return ((x[0]*y[0]+x[1]*y[1])/denominator, (x[1]*y[0]-x[0]*y[1])/denominator)


def gauss_scale(x, t):
    return x[0] * t, x[1] * t


def norm2(x):
    return x[0] ** 2 + x[1] ** 2


def gauss_polynomial_product(factors):
    out = [(F(1),F(0))]
    for factor in factors:
        nxt = [(F(0),F(0))] * (len(out) + len(factor) - 1)
        for i,x in enumerate(out):
            for j,y in enumerate(factor):
                nxt[i+j] = gauss_add(nxt[i+j],gauss_mul(x,y))
        out = nxt
    return out


def variational_controls():
    y=[F(0),F(1)]; ell=[F(8,7),F(-1,7)]
    u=scale(times(y,[-1,1]),F(8,7))
    d=plus(times(y,y),scale(u,-1))
    require(d == times(y,ell) == plus(y,scale(u,-F(1,8))), 'stationary norm identities')
    require(plus(plus([1],scale(u,F(3,4))),scale(d,-1)) == [F(1),F(-2),F(1)], 'derivative denominator bound')
    uprime=[i*u[i] for i in range(1,len(u))]
    require(plus(plus(ell,scale(y,-F(15,7))),uprime)==[F(0)], 'full logarithmic derivative identity')
    for zi,zj,qi,qj in [(F(1),F(1),F(1,2),F(1,2)),(F(3,2),F(1,2),F(2),F(1,8))]:
        epsilon=F(1,1000)
        gain=2*epsilon*(zi-zj)+2*epsilon**2
        ni,nj=qi+gain/2,qj+gain/2
        require(0<ni<(zi+epsilon)**2 and 0<nj<(zj-epsilon)**2, 'strict feasible two-loss variation')
        require((zi+epsilon)**2-ni+(zj-epsilon)**2-nj==zi**2-qi+zj**2-qj and ni*nj>qi*qj,
                'loss preservation and positive product improvement')
    return {'complete_extremum_polynomial_identities':4,'two_loss_controls':2}


def physical_controls(polys):
    phases=[(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1)),
            (F(3,5),F(4,5)),(F(3,5),F(-4,5)),(F(5,13),F(12,13)),(F(5,13),F(-12,13))]
    require(all(norm2(z)==1 for z in phases), 'unit Gaussian phases')
    pointwise=integrals=mean_controls=0
    for index in range(16):
        mu=(F(0),F(1,3),F(3,4),F(1))[index%4]
        weights=[F((index+3*j)%9) for j in range(8)]
        if index in (0,7): weights=[F(1)]*8
        radii=[8*mu*r/sum(weights) for r in weights]
        q=[gauss_scale(phases[(index+j)%8] if index!=7 else phases[0],r) for j,r in enumerate(radii)]
        x=sum(z[0] for z in q)/8
        for A in (F(1,10),F(2,5),F(3,4),F(99,100)):
            B=1-A*A; enlarged=[r+1-mu for r in radii]; s=max(A,x)
            projections=[z[0] for z in q]
            if x<=A:
                lam=(A-x)/(1-x)
                projections=[p+lam*(r-p) for p,r in zip(projections,enlarged)]
            require(sum(enlarged)==8 and sum(projections)==8*s,'all saturation means')
            for t in (F(0),F(1,5),F(1,2),F(1)):
                h=B*t; M=A+h; c=16*A*h*(1-s)
                z=[A+h*r for r in enlarged]
                Q=[A*A+2*A*h*p+h*h*r*r for p,r in zip(projections,enlarged)]
                original=[norm2(gauss_add((A,F(0)),gauss_scale(v,h))) for v in q]
                require(all(0<=old<=new<=Z*Z for old,new,Z in zip(original,Q,z)),'complete physical envelopes')
                require(sum(z)==8*M and sum(Z*Z-new for Z,new in zip(z,Q))==c,'complete loss constraint')
                require(0<=c/M**2<=4*(1-s)<=4,'normalized loss range')
                bound=M**8-8*A*h*(1-s)*M**6/(4-3*s)
                product=F(1)
                for value in original:product*=value
                require(bound>=0 and product<=bound**2,'pointwise rational bound control')
                pointwise+=1
            coefficients=gauss_polynomial_product([[(A,F(0)),gauss_scale(v,B)] for v in q])
            C=(F(0),F(0))
            for k,v in enumerate(coefficients):C=gauss_add(C,gauss_scale(v,F(1,k+1)))
            H=evaluate(polys['H'],A);T=evaluate(polys['T'],A)
            envelope=H-8*A*(1-s)*B*T/(4-3*s)
            require(envelope>=0 and norm2(C)<=envelope**2,'integrated Gaussian control')
            if x<=A:require(norm2(C)<=(1-F(8,9)*(1-A)**2)**2,'low mean defect control')
            if norm2(C)>=1:
                K=F(47,100)*(1-A)/(A*(1+A))
                require(x>A+K and x>(A+4*K)/(1+3*K),'both improved mean controls')
                mean_controls+=1
            integrals+=1
    return {'pointwise_saturation_controls':pointwise,'exact_Gaussian_integral_controls':integrals,
            'nonvacuous_refined_mean_controls':mean_controls,'zero_abstract_inputs_included':True}


def communication_controls():
    roots=[(F(0),F(0)),(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1)),
           (F(3,5),F(4,5)),(F(3,5),F(-4,5)),(F(-5,13),F(12,13))]
    count=0
    for A in (F(1,5),F(1,2),F(4,5)):
        factors=[[(F(-A),F(0)),(F(1),F(0))]]+[[gauss_scale(z,-1),(F(1),F(0))] for z in roots]
        p=gauss_polynomial_product(factors)
        derivative=[gauss_scale(p[k],k) for k in range(1,len(p))]
        shifted=[(F(0),F(0))]*9
        for k,v in enumerate(derivative):
            for j in range(k+1):shifted[j]=gauss_add(shifted[j],gauss_scale(v,comb(k,j)*A**(k-j)))
        reciprocal_elementary=[gauss_div(v,shifted[0]) for v in shifted]
        B=1-A*A; C=(F(0),F(0)); rhs=(F(1),F(0))
        for k,v in enumerate(reciprocal_elementary):C=gauss_add(C,gauss_scale(v,A**(8-k)*B**k/F(k+1)))
        for z in roots:
            numerator=gauss_add((F(1),F(0)),gauss_scale(z,-A))
            denominator=gauss_add((A,F(0)),gauss_scale(z,-1))
            require(norm2(numerator)-norm2(denominator)==B*(1-norm2(z))>=0,'every root disk inequality')
            rhs=gauss_mul(rhs,gauss_div(numerator,denominator))
        require(C==rhs and norm2(C)>=1,'full polar communication identity control')
        count+=1
    return {'exact_disk_polynomial_communication_controls':count,'critical_roots_not_numerically_solved':True}


def sharp_defect_family():
    # Exact eighth roots in Q[w]/(w^4+1), with w=exp(pi*i/4).
    one=(1,0,0,0);zero=(0,0,0,0)
    roots=[]
    for j in range(8):
        v=[0]*4;v[j%4]=1 if j<4 else -1;roots.append(tuple(v))
    def add(x,y):return tuple(a+b for a,b in zip(x,y))
    def mul(x,y):
        out=[0]*4
        for i,a in enumerate(x):
            for j,b in enumerate(y):out[(i+j)%4]+=a*b*(1 if i+j<4 else -1)
        return tuple(out)
    require(tuple(sum(r[k] for r in roots) for k in range(4))==zero,'exact zero mean roots of unity')
    out=[one]
    for root in roots:
        nxt=[zero]*(len(out)+1)
        for i,value in enumerate(out):
            nxt[i]=add(nxt[i],mul(value,root));nxt[i+1]=add(nxt[i+1],value)
        out=nxt
    require(out==[(-1,0,0,0)]+[zero]*7+[one],'full eighth-root product polynomial')
    limit=F(-1,9)
    require(1-abs(limit)==F(8,9),'exact limiting sharp defect')
    return {'abstract_family':'q_j=exp(pi*i*j/4), j=0,...,7',
            'exact_product_identity':'product(a+h*q_j)=a^8-h^8',
            'exact_integral':'C(a)=a^8-(1-a^2)^8/9',
            'limit_as_a_decreases_to_zero':str(limit),
            'sharp_uniform_low_mean_defect':'8/9',
            'actual_disk_polynomial_realization_claimed':False}


def audit():
    polys,scalar=scalar_certificate()
    return {'reviewer':'six-reviewer-1','role':'independent mathematical reviewer',
            'target_ref':'bafkreidm3pbjbv5tzj34fehpdi2njyutz7xgczubba2yn4twlg54xb7mhq',
            'scalar_certificate':scalar,'variational_controls':variational_controls(),
            'physical_controls':physical_controls(polys),'communication_controls':communication_controls(),
            'sharp_low_mean_defect_family':sharp_defect_family(),
            'first_power_endpoint_proved':False,
            'trust_boundary':'Written uniform extremum/calculus/communication proof plus exact finite polynomial identities; controls do not prove a general inequality by sampling.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',type=Path)
    parser.add_argument('--author-expected',type=Path)
    args=parser.parse_args();result=audit()
    if args.author_expected:
        original=json.loads(args.author_expected.read_text());scalar=result['scalar_certificate']
        require(scalar['power_sha256']==original['power_sha256'],'all five original power polynomial hashes')
        for name in ('R','W'):require(scalar['original_bernstein'][name]==original[name+'_bernstein'],'all original32 sign coefficients')
    raw=json.dumps(result,indent=2)+'\n'
    if args.check:require(raw==args.check.read_text(),'complete independent expected output')
    print(raw,end='')


if __name__=='__main__':
    main()
