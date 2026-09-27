#!/usr/bin/env python3
"""Exact controls for paired cubature with error proportional to distance loss.

See LOSS_CUBATURE.md. This checks finite constants, moment preservation,
replica normalization and interval remainder controls, not a new hinge sign.
Standard-library CPython >=3.11; no floating-point mathematical arithmetic.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from math import comb, factorial
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def inputs():
    pins = json.loads((HERE/'LOSS_CUBATURE_INPUTS.json').read_text())
    need(pins.get('schema') == 1 and pins.get('files'), 'dependency manifest')
    for name, digest in pins['files'].items():
        need(sha256((HERE/name).read_bytes()).hexdigest() == digest,
             'changed dependency: '+name)
    return pins['files']


PINS = inputs()
from paired_cubature import null_vector, verify_moments, pair_loss
from direct_hinge import exp_neg, sqrt_bounds


def beta_width(N, q, epsilon):
    need(type(N) is int and N >= 0 and type(q) is int and q >= 2,
         'integer row and coordinate half-degree')
    need(type(epsilon) in (int,F) and epsilon >= 0, 'nonnegative exact radius ratio')
    powers = [(j+2)**(q-2) for j in range(N+1)]
    width = max(comb(N,k)*sum(comb(N-k,j)*powers[k+j] for j in range(N-k+1))
                for k in range(N+1))
    return F(N+1,4*factorial(q))*(F(epsilon)/2)**q*width


def safe_degree(N, epsilon, bits):
    beta_width(N,2,epsilon)
    need(type(bits) is int and bits >= 0, 'nonnegative tolerance bits')
    return max(2,(3*(N+2)*F(epsilon)).__ceil__(),bits+2*N+N.bit_length())


def select_degree(N, epsilon, bits):
    upper = safe_degree(N,epsilon,bits)
    start = max(2,(F(N+2)*epsilon/2).__ceil__())
    lower, target = start, F(1,1 << bits)
    need(beta_width(N,upper,epsilon) <= target, 'explicit schedule failed')
    while lower < upper:
        middle = (lower+upper)//2
        if beta_width(N,middle,epsilon) <= target:
            upper = middle
        else:
            lower = middle+1
    need(beta_width(N,lower,epsilon) <= target, 'selected degree failed')
    need(lower == start or beta_width(N,lower-1,epsilon) > target,
         'not first valid degree on the decreasing range')
    return lower


def scale_interval(interval, factor):
    lo,hi = interval
    return (lo*factor,hi*factor) if factor >= 0 else (hi*factor,lo*factor)


def multiply_intervals(a,b):
    values = [x*y for x in a for y in b]
    return min(values),max(values)


def reported_interval(interval,bits=64):
    """Compact outward dyadic record; all internal comparisons precede rounding."""
    scale=1 << bits
    lo,hi=interval
    return [str(F((lo*scale).__floor__(),scale)),
            str(F((hi*scale).__ceil__(),scale))]


def exp_linear(terms, constant=F(0), bits=160):
    """Outward enclosure after exact collection of equal exponential terms."""
    lo=hi=constant
    for z,coefficient in terms.items():
        if not coefficient:
            continue
        a,b = exp_neg(z,bits)
        a,b = scale_interval((F(a,1 << bits),F(b,1 << bits)),coefficient)
        lo += a
        hi += b
    return lo,hi


def taylor(z,q):
    return sum(((-z)**r/F(factorial(r)) for r in range(q+1)),F(0))


def reduced_weights(columns, weights):
    """Small exact control using the accepted affine-elimination primitive."""
    weights = list(weights)
    active = [i for i,w in enumerate(weights) if w]
    cap = len(columns[0])
    while len(active) > cap:
        ids = active[:cap+1]
        direction = null_vector([columns[i] for i in ids])
        step = min(weights[i]/v for i,v in zip(ids,direction) if v > 0)
        for i,v in zip(ids,direction):
            weights[i] -= step*v
            need(weights[i] >= 0, 'negative elimination mass')
        newer = [i for i in active if weights[i]]
        need(len(newer) < len(active), 'nonprogressing elimination')
        active = newer
    return active,[weights[i] for i in active]


def one_dimensional_scatter(xs,weights,m):
    """Exact distribution of z=one half the iid replica scatter."""
    answer = Counter()
    for ids in combinations_with_replacement(range(len(xs)),m):
        multiplicities = Counter(ids)
        multiplicity = factorial(m)
        weight = F(1)
        for i,n in multiplicities.items():
            multiplicity //= factorial(n)
            weight *= weights[i]**n
        total = sum(xs[i] for i in ids)
        z = (sum(xs[i]**2 for i in ids)-total*total/m)/2
        answer[z] += multiplicity*weight
    need(sum(answer.values()) == 1 and min(answer) >= 0, 'replica histogram')
    return answer


def projected_moments(xs,weights,m,q):
    """Compute E(S_1^a S_2^b) recursively, then expand the scatter power."""
    indices = [(a,b) for b in range(q+1) for a in range(2*q-2*b+1)]
    moments = [sum(w*x**j for x,w in zip(xs,weights)) for j in range(2*q+1)]
    state = {(a,b):F(a == 0 and b == 0) for a,b in indices}
    for _ in range(m):
        state = {(a,b):sum(comb(a,i)*comb(b,j)*state[a-i,b-j]*moments[i+2*j]
                          for i in range(a+1) for j in range(b+1))
                 for a,b in indices}
    return [sum(comb(r,j)*(-F(1,m))**j*state[2*j,r-j] for j in range(r+1))/2**r
            for r in range(q+1)]


def controls():
    scalar = 0
    grid = [F(0),F(1,16),F(1,4),F(1),F(2),F(4)]
    for q in range(2,9):
        for w in grid:
            for v in grid:
                if v > w:
                    continue
                terms = Counter()
                terms[v] += 1
                terms[w] -= 1
                interval = exp_linear(terms,taylor(w,q)-taylor(v,q))
                lo,hi = scale_interval(interval,(-1)**q)
                need(0 <= lo <= hi <= (w-v)*w**q/factorial(q),
                     'paired Taylor remainder sign or magnitude')
                scalar += 1
    budgets = 0
    for N,q,epsilon in product(range(9),range(2,18),[F(0),F(1,16),F(1,2),F(2)]):
        value = beta_width(N,q,epsilon)
        A = F(N+2)*epsilon/2
        coarse = F((N+1)*3**N,4*(N+2)**2)*A**q/factorial(q)
        need(value <= coarse, 'coarse beta width')
        need(beta_width(N,q+1,epsilon) <= A*value/(q+1), 'tail monotonicity')
        budgets += 1
    schedules = 0
    for N,epsilon,b in product(range(9),[F(0),F(1,16),F(1,2),F(2)],range(0,17,4)):
        need(beta_width(N,safe_degree(N,epsilon,b),epsilon) <= F(1,1 << b),
             'loss-independent degree schedule')
        schedules += 1
    xs = [(F(-1,4),F(0),F(0)),(F(0),F(1,4),F(0)),
          (F(1,4),F(0),F(0)),(F(0),F(0),F(-1,4))]
    ys = [(abs(x[0])/2,x[1]/2,x[2]/3) for x in xs]
    weights = list(map(F,[F(1,10),F(2,10),F(3,10),F(4,10)]))
    d = pair_loss(xs,ys,weights)
    def variance(sites):
        mean = [sum(w*x[j] for w,x in zip(weights,sites)) for j in range(3)]
        return sum(w*sum(v*v for v in x) for w,x in zip(weights,sites))-sum(v*v for v in mean)
    need(d == 2*(variance(xs)-variance(ys)), 'covariance normalization')
    replica_tuples = 0
    for m in range(2,5):
        expected = F(0)
        for ids in product(range(4),repeat=m):
            probability = F(1)
            for i in ids:
                probability *= weights[i]
            zs = []
            for sites in (xs,ys):
                sums = [sum(sites[i][j] for i in ids) for j in range(3)]
                zs.append((sum(sum(v*v for v in sites[i]) for i in ids)
                           -sum(v*v for v in sums)/m)/2)
            need(0 <= zs[1] <= zs[0] <= F(m,32), 'replica radius/order')
            expected += probability*(zs[0]-zs[1])
            replica_tuples += 1
        need(expected == F(m-1,4)*d, 'replica mean-loss factor')
    rejected = 0
    for call in [lambda:beta_width(-1,2,F(1)),lambda:beta_width(2,1,F(1)),
                 lambda:beta_width(2,2,-F(1)),lambda:beta_width(2,2,0.5),
                 lambda:safe_degree(2,F(1),True),lambda:safe_degree(2,F(1),-1)]:
        try:
            call()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('malformed parameter accepted')
    return {'paired_scalar_intervals':scalar,'beta_bound_and_ratio_checks':budgets,
            'explicit_schedule_checks':schedules,'three_dimensional_replica_tuples':replica_tuples,
            'three_dimensional_loss':str(d),'malformed_parameters_rejected':rejected}


def compression_controls():
    xs = [F(i,32) for i in range(-8,9)]
    original = [F(1,len(xs))]*len(xs)
    reference_y = [x if x >= 0 else x/2 for x in xs]
    columns = [(F(1),)+tuple(x**j for j in range(1,5))
               +tuple(y**j for j in range(1,5)) for x,y in zip(xs,reference_y)]
    ids,ws = reduced_weights(columns,original)
    for j in range(1,5):
        need(sum(w*x**j for x,w in zip(xs,original) if x < 0)
             == sum(w*xs[i]**j for i,w in zip(ids,ws) if xs[i] < 0),
             'negative-half moment not preserved')
    rows=[]
    for t in [F(0),F(1,4),F(1,2),F(1),F(1,1024),F(1,1 << 40)]:
        yy = [x if x >= 0 else (1-2*t)*x for x in xs]
        xx3,yy3 = [[(x,F(0),F(0)) for x in sites] for sites in (xs,yy)]
        result={'indices':ids,'weights':ws,'degree':4}
        checked=verify_moments(xx3,yy3,original,result)
        before=pair_loss(xx3,yy3,original)
        after=pair_loss([xx3[i] for i in ids],[yy3[i] for i in ids],ws)
        need(before == after and (before > 0 if t else before == 0), 'loss retention')
        rows.append({'t':str(t),'loss':str(before),'marginal_monomials_checked':checked})
    return {'nonlinear_input_atoms':len(xs),'retained_atoms':len(ids),'indices':ids,
            'weights':list(map(str,ws)),'common_cubature_parameter_controls':rows}


def near_isometry_controls():
    xs=[F(i,12) for i in range(-3,4)]
    original=[F(1,7)]*7
    ids,ws=reduced_weights([tuple(x**j for j in range(5)) for x in xs],original)
    ys=[xs[i] for i in ids]
    histograms={}
    moments_checked=0
    for name,sites,weights in [('mu',xs,original),('nu',ys,ws)]:
        for m in range(2,5):
            hist=one_dimensional_scatter(sites,weights,m)
            moments=projected_moments(sites,weights,m,2)
            for r in range(3):
                need(moments[r] == sum(p*z**r for z,p in hist.items()),
                     'dynamic and definition-level replica moments disagree')
                moments_checked += 1
            histograms[name,m]=hist
    for m in range(2,5):
        for r in range(3):
            need(sum(p*z**r for z,p in histograms['mu',m].items())
                 == sum(p*z**r for z,p in histograms['nu',m].items()),
                 'matched polynomial replica moment')
    variance=sum(w*x*x for x,w in zip(xs,original))-sum(w*x for x,w in zip(xs,original))**2
    output=[]
    for t in [F(1,4),F(1,1024),F(1,1 << 40)]:
        lam=1-t
        d=2*(1-lam*lam)*variance
        moment_intervals=[]
        actual_moments=[]
        polynomial_moments=[]
        for m in range(2,5):
            terms=Counter()
            for name,sgn in [('mu',1),('nu',-1)]:
                for z,p in histograms[name,m].items():
                    terms[lam*lam*z] += sgn*p
                    terms[z] -= sgn*p
            root_lo,root_hi=sqrt_bounds(F(m),128)
            factor=(1/(m*m*(m-1)*root_hi*d),1/(m*m*(m-1)*root_lo*d))
            interval=multiply_intervals(exp_linear(terms),factor)
            width=F(1,4*m*m)*(F(m,32)**2)/factorial(2)
            need(max(abs(v) for v in interval) <= width,
                 'observed normalized moment difference exceeds bound')
            moment_intervals.append(interval)
            actual_terms=Counter()
            polynomial=F(0)
            for z,p in histograms['mu',m].items():
                actual_terms[lam*lam*z] += p
                actual_terms[z] -= p
                polynomial += p*(taylor(lam*lam*z,2)-taylor(z,2))
            actual_moments.append(multiply_intervals(exp_linear(actual_terms),factor))
            polynomial_moments.append(multiply_intervals((polynomial,polynomial),factor))
        beta=[]
        certificate_intervals=[]
        rejected_zero_remainder=False
        for k in range(3):
            lo=hi=F(0)
            actual_lo=actual_hi=polynomial_lo=polynomial_hi=F(0)
            negative_width=positive_width=F(0)
            for j in range(3-k):
                coefficient=3*comb(2,k)*(-1)**j*comb(2-k,j)
                term=scale_interval(moment_intervals[k+j],coefficient)
                lo+=term[0];hi+=term[1]
                actual=scale_interval(actual_moments[k+j],coefficient)
                polynomial=scale_interval(polynomial_moments[k+j],coefficient)
                actual_lo+=actual[0];actual_hi+=actual[1]
                polynomial_lo+=polynomial[0];polynomial_hi+=polynomial[1]
                m=k+j+2
                width=abs(coefficient)*F(1,4*m*m)*F(m,32)**2/factorial(2)
                if j % 2:
                    negative_width+=width
                else:
                    positive_width+=width
            need(max(abs(lo),abs(hi)) <= beta_width(2,2,F(1,16)),
                 'observed normalized row difference exceeds bound')
            beta.append(reported_interval((lo,hi)))
            need(polynomial_lo-negative_width <= actual_lo <= actual_hi
                 <= polynomial_hi+positive_width,'moment-based beta interval')
            if actual_lo > polynomial_hi or actual_hi < polynomial_lo:
                rejected_zero_remainder=True
            certificate_intervals.append(reported_interval(
                (polynomial_lo-negative_width,polynomial_hi+positive_width)))
        need(rejected_zero_remainder,'omitting the remainder was not detected')
        output.append({'t':str(t),'loss':str(d),'normalized_beta_difference_intervals':beta,
                       'moment_based_beta_enclosures':certificate_intervals,
                       'zero_remainder_interval_rejected':rejected_zero_remainder})
    return {'input_atoms':7,'retained_atoms':len(ids),'indices':ids,'weights':list(map(str,ws)),
            'definition_level_replica_moments_checked':moments_checked,
            'exponential_bits':160,'radical_bits':128,'reported_interval_bits':64,
            'row':2,'half_degree':2,'radius_ratio':'1/16',
            'theorem_relative_width':str(beta_width(2,2,F(1,16))),'controls':output}


def calculate():
    table=[]
    for N,e,b in [(8,F(1,2),10),(32,F(1,2),10),(64,F(1,2),20),
                  (8,F(4),10),(32,F(9),10)]:
        q=select_degree(N,e,b)
        width=beta_width(N,q,e)
        table.append({'row':N,'radius_ratio':str(e),'error_bits':b,
                      'safe_half_degree':safe_degree(N,e,b),'selected_half_degree':q,
                      'coordinate_degree':2*q,'atoms':2*comb(2*q+3,3)-1,
                      'relative_beta_upper':reported_interval((F(0),width))[1],
                      'exact_width_sha256':sha256(str(width).encode()).hexdigest()})
    return {'status':'LOSS_PROPORTIONAL_CUBATURE_PASS','dependency_sha256':PINS,
            'degree_budgets':table,'controls':controls(),
            'nonlinear_common_cubature':compression_controls(),
            'near_isometry_remainder_enclosures':near_isometry_controls(),
            'scope':'Exact finite controls for the written loss-proportional approximation theorem. No new beta or hinge sign; full-curve transfer additionally requires epsilon<=1/2 and the accepted loss modulus.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path,default=HERE/'LOSS_CUBATURE_EXPECTED.json')
    parser.add_argument('--write-expected',action='store_true')
    args=parser.parse_args()
    started=time.monotonic()
    record=calculate()
    encoded=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if args.write_expected:
        args.expected.write_bytes(encoded)
    else:
        need(json.loads(args.expected.read_text()) == record,'expected result mismatch')
    print(record['status'])
    print('record_sha256',sha256(encoded).hexdigest())
    print('seconds',round(time.monotonic()-started,3))


if __name__ == '__main__':
    main()
