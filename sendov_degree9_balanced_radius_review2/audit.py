"""Independent exact audit: real/imaginary powers and a delta-domain certificate.

six-reviewer-2, independent mathematical reviewer. Standard library only.
No author module, norm recurrence or polynomial certificate is imported.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from math import comb, factorial
import json
from pathlib import Path
import argparse


def check(condition, message):
    if not condition:
        raise ArithmeticError(message)


def clean(p):
    return {k: v for k, v in p.items() if v}


def plus(*polys):
    out = {}
    for p in polys:
        for k, v in p.items():
            out[k] = out.get(k, Q(0)) + v
    return clean(out)


def times(p, q):
    out = {}
    for m, a in p.items():
        for n, b in q.items():
            key = tuple(i+j for i, j in zip(m, n))
            out[key] = out.get(key, Q(0)) + a*b
    return clean(out)


def scaled(p, a):
    return clean({k: v*a for k, v in p.items()})


def real_imaginary_origin():
    # w=x+i sqrt(1-x^2). Expand its ordinary binomial powers, without
    # Chebyshev recurrence, Laurent correlations or quotient-ring reduction.
    real, imag = {}, {}
    for linear in range(5):
        for quadratic in range(5-linear):
            constant = 4-linear-quadratic
            k = linear+2*quadratic
            h = Q(9*factorial(4)*(-2)**linear,
                  (k+1)*factorial(linear)*factorial(quadratic)*factorial(constant))
            for parity, out in [(0, real), (1, imag)]:
                for j in range(parity, k+1, 2):
                    half = j//2
                    # Imaginary coefficients have sqrt(1-x^2) factored out.
                    for r in range(half+1):
                        key = (k, linear, k-j+2*r)
                        v = h*comb(k, j)*comb(half, r)*(-1)**(half+r)
                        out[key] = out.get(key, Q(0))+v
    real, imag = clean(real), clean(imag)
    norm = plus(times(real, real),
                times({(0,0,0): Q(1), (0,0,2): Q(-1)}, times(imag, imag)))
    check(tuple(max(m[i] for m in norm) for i in range(3)) == (16,8,8),
          'complete norm degrees')
    return norm


def delta_transform(norm):
    # tau=1-d, c=1-d*e, x=1-d*f, with e=1-y, f=1-z.
    # Direct simultaneous binomial expansion; then division by d is a shift.
    source = plus(norm, {(0,0,0): Q(-3), (1,0,0): Q(2)})
    out = {}
    for (i,j,k), v in source.items():
        for p in range(i+1):
            for q in range(j+1):
                for r in range(k+1):
                    key = (p+q+r, q, r)
                    val = v*comb(i,p)*comb(j,q)*comb(k,r)*(-1)**(p+q+r)
                    out[key] = out.get(key, Q(0))+val
    out = clean(out)
    check(all(m[0] > 0 for m in out), 'zero delta constant term')
    quotient = {(i-1,j,k): v for (i,j,k),v in out.items()}
    check(tuple(max(m[i] for m in quotient) for i in range(3)) == (19,8,8),
          'complete quotient degrees')
    return quotient


def linear_map_axis(p, axis, n, matrix):
    out = {}
    for m, v in p.items():
        for j in range(n+1):
            factor = matrix[j][m[axis]]
            if factor:
                key = list(m)
                key[axis] = j
                key = tuple(key)
                out[key] = out.get(key, Q(0))+v*factor
    return clean(out)


def local_power(p, low, high, degree):
    matrix = [[Q(comb(k,j))*low**(k-j)*(high-low)**j if j<=k else Q(0)
               for k in range(degree+1)] for j in range(degree+1)]
    return linear_map_axis(p, 0, degree, matrix)


def tensor_bernstein(p, degrees, inverse=False):
    out = p
    for axis, n in enumerate(degrees):
        if inverse:
            matrix = [[Q((-1)**(i-j)*comb(i,j)*comb(n,i)) if j<=i else Q(0)
                       for j in range(n+1)] for i in range(n+1)]
        else:
            matrix = [[Q(comb(i,j),comb(n,j)) if j<=i else Q(0)
                       for j in range(n+1)] for i in range(n+1)]
        out = linear_map_axis(out, axis, n, matrix)
    return out


def coefficient_digest(values):
    return sha256(('\n'.join(str(z) for z in values)+'\n').encode()).hexdigest()


def origin_cells(quotient, exported=None):
    ds = (19,8,8)
    cuts = [Q(0), Q(1,2), Q(3,4), Q(7,8), Q(1)]
    rows = []
    for lo, hi in zip(cuts, cuts[1:]):
        # Original tau-cell corresponds to reversed delta-cell.
        local = local_power(quotient, 1-hi, 1-lo, ds[0])
        beta = tensor_bernstein(local, ds)
        check(tensor_bernstein(beta, ds, inverse=True) == local,
              'full inverse tensor identity')
        check(all(z>=0 for z in beta.values()), 'all certificate signs')
        indices = list(product(*(range(n+1) for n in ds)))
        values = [beta.get(tuple(n-i for n,i in zip(ds,m)), Q(0)) for m in indices]
        if exported is not None:
            exported.append(list(map(str, values)))
        zeros = [list(m) for m,z in zip(indices,values) if not z]
        check(zeros == ([] if hi<1 else [[19,8,k] for k in range(9)]),
              'complete zeros including closed boundaries')
        rows.append({'interval':[str(lo),str(hi)], 'degree':list(ds),
                     'count':len(values), 'minimum':str(min(values)),
                     'zero_indices':zeros, 'sha256':coefficient_digest(values)})
    return rows


def polar_coefficients():
    # Expand directly in D=1-a^2: bracket=1+(2t-1)D+(t^2-2t)D^2.
    # All arrays here are ordinary dense univariate power coefficients.
    def convolve(a,b):
        out = [Q(0)]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b): out[i+j] += x*y
        return out
    cs = [[Q(1)]]
    bracket = [[Q(1)], [Q(-1),Q(2)], [Q(0),Q(-2),Q(1)]]
    for _ in range(4):
        out = [[Q(0)] for _ in range(len(cs)+2)]
        for i, row in enumerate(cs):
            for j, factor in enumerate(bracket):
                term=convolve(row,factor)
                out[i+j] += [Q(0)]*(len(term)-len(out[i+j]))
                for k,z in enumerate(term): out[i+j][k] += z
        cs=out
    integral=[sum(z/Q(k+1) for k,z in enumerate(row)) for row in cs]
    defect=[-z for z in integral];defect[0]+=1
    check(defect[0]==defect[1]==0, 'double polar zero in D')
    q=defect[2:]
    beta=[sum(q[j]*Q(comb(i,j),comb(6,j)) for j in range(i+1)) for i in range(7)]
    beta.reverse()  # convert D basis to A=1-D basis
    check(min(beta)==Q(2,3), 'polar uniform margin')
    original=list(reversed(beta))
    recovered=[sum(original[j]*(-1)**(i-j)*comb(i,j)*comb(6,i)
                   for j in range(i+1)) for i in range(7)]
    check(recovered==q, 'full independent polar inverse')
    return {'coefficients':list(map(str,beta)), 'sha256':coefficient_digest(beta)}


def gaussian_multiply(z,w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])


def gaussian_power(z,n):
    result=(Q(1),Q(0))
    for _ in range(n): result=gaussian_multiply(result,z)
    return result


def gaussian_integral(q,a,polar=False):
    # Direct closed binomial sum for eight identical factors.
    constant=a if polar else Q(1)
    linear=(1-a*a) if polar else -a
    scale=1 if polar else 9
    real=imag=Q(0)
    for k in range(9):
        z=gaussian_power(q,k)
        coef=Q(scale*comb(8,k),k+1)*constant**(8-k)*linear**k
        real+=coef*z[0];imag+=coef*z[1]
    return real*real+imag*imag


def radial_obstruction():
    a=Q(3,4);phase=(Q(5,13),Q(12,13));r=Q(199,200)
    check(sum(z*z for z in phase)==1, 'unit phase')
    origin=[];polar=[];slack=[]
    for radius in [Q(1),r]:
        q=tuple(z*radius for z in phase)
        origin.append(gaussian_integral(q,a)/radius**16)
        polar.append(gaussian_integral(q,a,polar=True))
        slack.append(2*a*q[0]+(1-a*a)*sum(z*z for z in q)-1)
    check(min(slack)>0 and max(polar)<1 and origin[1]<origin[0],
          'strict radial obstruction, outside joint premise')
    return {'slacks':list(map(str,slack)), 'origin_values':list(map(str,origin)),
            'difference':str(origin[1]-origin[0]), 'polar_values':list(map(str,polar))}


def widened_constants():
    half=Q(1,40000)
    lower=Q(8,13)
    check(lower*lower+lower<Q(1), 'mean radius lower implication')
    square_bound=1/lower**2+Q(1,3)
    check(square_bound==Q(571,192)<3<Q(7,4)**2,
          'balanced normalized factors below sqrt(3) and 7/4')
    bound=Q(7,4)+4*half
    origin=288*bound**7
    check(Q(5,4)+half<Q(63,50) and 8*Q(63,50)**7<50,
          'polar perturbation for enlarged window')
    check(50*half==Q(1,800)<Q(2,3), 'polar forcing survives')
    check(origin<15000 and Q(1,2)-origin*half>Q(1,8),
          'strict normalized origin gap survives')
    return {'radius_difference':'1/20000', 'half_difference':str(half),
            'balanced_factor_square_upper':str(square_bound),
            'perturbed_factor_upper':str(bound),
            'origin_telescoping':str(origin),
            'strict_origin_gap_coefficient':str(Q(1,2)-origin*half),
            'stated_origin_gap_coefficient':'1/8', 'width_improvement':50}


def sharpness(norm):
    diagonal={}
    for (i,j,k),z in norm.items(): diagonal[i]=diagonal.get(i,Q(0))+z
    shifted=[sum(v*comb(i,k)*(-1)**k for i,v in diagonal.items() if i>=k)
             for k in range(17)]
    expected=[Q(k+1 if k<=8 else 17-k) for k in range(17)]
    check(shifted==expected, 'full squared geometric-sum identity')
    return list(map(str,shifted))


def definition_checks(norm):
    # Direct four-plus-four Gaussian integration on rational unit directions.
    unit=[(Q(1),Q(0)),(Q(0),Q(1)),(Q(3,5),Q(4,5)),
          (Q(-3,5),Q(4,5)),(Q(5,13),Q(-12,13))]
    count=0
    for tau in [Q(0),Q(1,3),Q(7,8),Q(1)]:
        for c,d in [(Q(1),Q(0)),(Q(0),Q(1)),(Q(3,5),Q(4,5))]:
            for w in unit:
                u=gaussian_multiply(w,(c,d));v=gaussian_multiply(w,(c,-d))
                real=imag=Q(0)
                for j in range(5):
                    for k in range(5):
                        z=gaussian_multiply(gaussian_power(u,j),gaussian_power(v,k))
                        a=Q(9*comb(4,j)*comb(4,k),j+k+1)*(-tau)**(j+k)
                        real+=a*z[0];imag+=a*z[1]
                symbolic=sum(a*tau**i*c**j*w[0]**k for (i,j,k),a in norm.items())
                check(real*real+imag*imag==symbolic, 'direct definition-level norm identity')
                count+=1
    return count


def controls():
    rejected=0
    for p in [{(0,0,0):Q(1)}, {(1,0,0):Q(-1)}]:
        try:
            check(all(m[0]>0 for m in p) and all(v>=0 for v in p.values()),
                  'deliberate invalid certificate')
        except ArithmeticError: rejected+=1
    fixture={(0,0,0):Q(1),(2,1,1):Q(3)}
    beta=tensor_bernstein(fixture,(2,1,1));beta[0,0,0]+=1
    check(tensor_bernstein(beta,(2,1,1),True)!=fixture,'altered coefficient rejected')
    rejected+=1
    for half in [Q(1,1000), Q(1,100)]:
        try:
            check(Q(1,2)-288*(Q(7,4)+4*half)**7*half>Q(1,8),
                  'unsupported wider transport window')
        except ArithmeticError:rejected+=1
    check(rejected==5,'control count')
    return rejected


def build(exported=None):
    norm=real_imaginary_origin()
    quotient=delta_transform(norm)
    values=[]
    cells=origin_cells(quotient,values if exported is not None else None)
    if exported is not None:
        exported.update({'norm':[[list(m),str(v)] for m,v in sorted(norm.items())],
                         'quotient_delta':[[list(m),str(v)] for m,v in sorted(quotient.items())],
                         'origin_bernstein':values})
    return {'reviewer':'six-reviewer-2', 'origin_cells':cells,
            'polar':polar_coefficients(), 'radial_obstruction':radial_obstruction(),
            'sharpness':sharpness(norm), 'strengthening':widened_constants(),
            'definition_checks':definition_checks(norm),
            'rejected_controls':controls(), 'certificate_entries':6487}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--export',type=Path,help='optional private coefficient comparison output')
    args=parser.parse_args()
    exported={} if args.export else None
    result=build(exported)
    expected=Path(__file__).with_name('expected.json')
    check(expected.exists(),'compact expected manifest required')
    check(result==json.loads(expected.read_text()),'complete manifest match')
    if args.export:args.export.write_text(json.dumps(exported,separators=(',',':'))+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':main()
