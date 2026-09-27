#!/usr/bin/env python3
"""Certify a full prior simplex and coordinate cell, at Gaussian variance one.

Standard-library CPython >=3.11. See PROOF.md for the measure reduction,
convexity argument and endpoint signs. This is an author certificate producer,
not an independent review or a proof-assistant formalization.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from math import comb, factorial
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
CENTERS = [(0,0,0),(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
ALPHA, BETA = F(21,156), F(30,156)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def pinned_inputs():
    pins = json.loads((HERE/'INPUTS.json').read_text())
    need(pins.get('schema') == 1 and pins.get('files'), 'dependency manifest')
    for name, digest in pins['files'].items():
        need(sha256((HERE/name).read_bytes()).hexdigest() == digest,
             'changed dependency: '+name)
    return pins['files']


PINS = pinned_inputs()
sys.path.insert(0, str(HERE.parent/'gaussian_prior_localization'))
from direct_hinge import density_histograms, exp_neg, gaussian_constant, quadrature_error


def decompose(weights):
    """Exact barycentric coordinates in the seven-vertex prior simplex."""
    need(len(weights) == 7 and all(type(w) in (int, F) for w in weights),
         'seven exact weights required')
    need(sum(weights) == 1 and weights[0] >= 0
         and all(w >= ALPHA for w in weights[1:]), 'weight outside prior simplex')
    return [weights[0]/BETA]+[(w-ALPHA)/BETA for w in weights[1:]]


def window_max(source, target, left, right):
    """Exact upper-polygon maximum, including rational boundary thresholds.

    This uses the knot-sweep mechanism of R2's coordinate-cell certificate.
    Equal-mass densities are not inferred from histogram values; only the
    spatial multiplicities of the two histograms must match.
    """
    need(0 <= left < right, 'invalid threshold window')
    need(sum(source.values()) == sum(target.values()), 'unequal grid counts')
    need(all(type(q) is int and q >= 0 and type(n) is int and n > 0
             for hist in (source,target) for q,n in hist.items()), 'invalid histogram')
    value = sum(n*max(q-left,0) for q,n in source.items())
    value -= sum(n*max(q-left,0) for q,n in target.items())
    slope = sum(n for q,n in target.items() if q > left)
    slope -= sum(n for q,n in source.items() if q > left)
    best, arg, previous = value, left, left
    knots = sorted({q for q in source.keys() | target.keys() if left < q <= right}
                   | {right})
    for q in knots:
        value += slope*(q-previous)
        if value > best:
            best, arg = value, q
        slope += source.get(q,0)-target.get(q,0)
        previous = q
    return best, arg, len(knots)


def vertex_histograms(h, M, bits):
    """Upper densities for both vertex orbits and the point-target lower.

    The outer-heavy vertex is asymmetric. Each signed-permutation spatial
    orbit is therefore split by the value of its distinguished coordinate.
    Treating that density as invariant under the whole group would be wrong.
    """
    need(isinstance(h,F) and h > 0 and type(M) is int and M >= 0
         and type(bits) is int and bits >= 16, 'invalid lattice parameters')
    Q, denominator = 1 << bits, 156*(1 << (2*bits))
    A = [exp_neg((h*j)**2/2,bits) for j in range(M+1)]
    P = [exp_neg((h*j-1)**2/2,bits)[1] for j in range(M+1)]
    N = [exp_neg((h*j+1)**2/2,bits)[1] for j in range(M+1)]
    central, outer, target = Counter(), Counter(), Counter()
    stream, orbits, split_entries = sha256(), 0, 0
    for xyz in combinations_with_replacement(range(M+1),3):
        divisor = 1
        for n in Counter(xyz).values():
            divisor *= factorial(n)
        numerator = (1 << sum(v > 0 for v in xyz))*6
        need(numerator % divisor == 0, 'nonintegral orbit multiplicity')
        mult = numerator//divisor
        i,j,k = xyz
        ai,aj,ak = [A[v][1] for v in xyz]
        product_upper = ai*aj*ak
        other_factors = [aj*ak,ai*ak,ai*aj]
        core = 21*sum((P[v]+N[v])*other_factors[pos] for pos,v in enumerate(xyz))
        source_upper = min(Q,(core+30*product_upper+denominator-1)//denominator)
        target_lower = A[i][0]*A[j][0]*A[k][0]//(Q*Q)
        central[source_upper] += mult
        target[target_lower] += mult
        choices, split = Counter([i,-i,j,-j,k,-k]), []
        for value, occurrences in sorted(choices.items()):
            need(mult*occurrences % 6 == 0, 'nonintegral distinguished-axis count')
            count = mult*occurrences//6
            pos = xyz.index(abs(value))
            shifted = (P if value >= 0 else N)[abs(value)]*other_factors[pos]
            upper = min(Q,(core+30*shifted+denominator-1)//denominator)
            outer[upper] += count
            split.append((value,count,upper))
        need(sum(row[1] for row in split) == mult, 'incomplete orbit split')
        split_entries += len(split)
        stream.update(f'{xyz},{mult},{source_upper},{target_lower},{split}\n'.encode())
        orbits += 1
    need(sum(central.values()) == sum(outer.values()) == sum(target.values())
         == (2*M+1)**3, 'incomplete full-grid coverage')
    return central,outer,target,orbits,split_entries,stream.hexdigest()


def determinant(rows):
    a = [list(map(F,row)) for row in rows]
    need(all(len(row) == len(a) for row in a), 'square determinant required')
    answer = F(1)
    for i in range(len(a)):
        pivot_row = next((j for j in range(i,len(a)) if a[j][i]),None)
        if pivot_row is None:
            return F(0)
        if pivot_row != i:
            a[i],a[pivot_row] = a[pivot_row],a[i]
            answer = -answer
        pivot = a[i][i]
        answer *= pivot
        for j in range(i+1,len(a)):
            factor = a[j][i]/pivot
            for k in range(i,len(a)):
                a[j][k] -= factor*a[i][k]
    return answer


def controls():
    sites = 0
    for h,M in [(F(1,2),2),(F(1,3),3),(F(1,4),4)]:
        a,b,g,*_ = vertex_histograms(h,M,32)
        for masses,hist in [([30]+[21]*6,a),([0,51]+[21]*5,b)]:
            groups = Counter({tuple(map(F,x)):w for x,w in zip(CENTERS,masses) if w})
            need(hist == density_histograms(groups,156,h,M,32)[1],
                 'vertex histogram differs from complete unquotiented grid')
        zero = Counter({(F(0),)*3:1})
        need(g == density_histograms(zero,1,h,M,32)[0], 'target histogram differs')
        sites += (2*M+1)**3
    sweeps = 0
    for xs,ys in product(list(product(range(4),repeat=2)),repeat=2):
        for left,right in [(0,3),(1,2),(1,3),(F(1,2),F(5,2))]:
            best,arg,_ = window_max(Counter(xs),Counter(ys),left,right)
            knots = {left,right} | {q for q in xs+ys if left <= q <= right}
            values = {q:sum(max(v-q,0) for v in xs)-sum(max(v-q,0) for v in ys)
                      for q in knots}
            need(best == max(values.values()) and values[arg] == best, 'window maximum')
            sweeps += 1
    mixtures = 0
    for i in range(7):
        for j in range(i,7):
            for n in range(31):
                residual = [0]*7
                residual[i] += n
                residual[j] += 30-n
                w = [F(residual[0],156)]+[F(21+v,156) for v in residual[1:]]
                lam = decompose(w)
                need(sum(lam) == 1 and all(v >= 0 for v in lam), 'barycentric probability')
                need(w == [BETA*lam[0]]+[ALPHA+BETA*v for v in lam[1:]],
                     'barycentric reconstruction')
                kernels = [F((3*k+2*n)%17,17) for k in range(7)]
                vertex_values = [ALPHA*sum(kernels[1:])+BETA*v for v in kernels]
                value = sum(p*v for p,v in zip(w,kernels))
                for threshold in (F(1,5),F(1,2),F(4,5)):
                    need(max(value-threshold,0) <=
                         sum(p*max(v-threshold,0) for p,v in zip(lam,vertex_values)),
                         'hinge convexity control')
                    mixtures += 1
    counts = [1]*31
    for _ in range(6):
        counts = [sum(counts[:n+1]) for n in range(31)]
    need(all(counts[n] == comb(n+6,6) for n in range(31)), 'prior count formula')
    rejected = 0
    bad = [lambda:decompose([F(1,7)]*6), lambda:decompose([1]+[0]*6),
           lambda:decompose([F(-1,156)]+[F(157,936)]*6),
           lambda:decompose([1.0]+[0]*6),
           lambda:window_max(Counter({1:1}),Counter({1:2}),0,2),
           lambda:window_max(Counter({1:1}),Counter({1:1}),2,1),
           lambda:vertex_histograms(F(1),True,32)]
    for fn in bad:
        try:
            fn()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('invalid control accepted')
    return {'unquotiented_grid_sites_per_vertex':sites,'vertex_histograms_compared':6,
            'definition_level_window_sweeps':sweeps,'prior_hinge_convexity_checks':mixtures,
            'small_prior_count_checks':31,'invalid_controls_rejected':rejected}


def calculate():
    raw = (HERE/'CELL.json').read_bytes()
    cell = json.loads(raw)
    need(cell['source_centers'] == [list(v) for v in CENTERS], 'source centers')
    required = {'variance':'1','source_coordinate_radius':'1/256',
                'target_coordinate_radius':'1/16','outer_source_mass_floor':'21/156',
                'origin_source_mass_floor':'0','weight_denominator':156,
                'coordinate_denominator':256,'frontier_level':1,
                'middle_window':['1/256','7/10'],'claimed_adverse_middle_upper':'-1/256',
                'quadrature_step':'1/16','quadrature_half_grid':112,'precision_bits':48,
                'frontier_anchoring':'subtract each endpoint label 0 separately'}
    need(all(cell.get(k) == v for k,v in required.items()), 'changed certificate cell')
    checked = controls()
    eps,ry,rho = F(1,128),F(7,64),F(25,8)
    left,right = map(F,cell['middle_window'])
    need(3*F(1,256)**2 < eps**2 and 3*F(1,16)**2 < ry**2, 'Euclidean radii')
    need(6*ALPHA+BETA == 1, 'prior simplex mass')
    h,M,bits = F(cell['quadrature_step']),cell['quadrature_half_grid'],cell['precision_bits']
    Q = 1 << bits
    a,b,g,orbits,split_entries,digest = vertex_histograms(h,M,bits)
    cl,cu = gaussian_constant(bits)
    quad,tail = quadrature_error(h,M*h-1,bits+10)
    perturbation = eps/2+F(3,1024)
    rows = []
    for name,hist,multiplicity in [('central_residual',a,1),('outer_residual',b,6)]:
        value,arg,knots = window_max(hist,g,left*Q,right*Q)
        discrete = (cl if value < 0 else cu)*h**3*value/Q
        reference = discrete+quad+tail
        uniform = reference+perturbation
        need(uniform < -F(1,256), 'a simplex vertex lacks the claimed middle margin')
        rows.append({'vertex_orbit':name,'number_of_vertices':multiplicity,
                     'discrete_adverse_upper':str(discrete),
                     'reference_adverse_upper':str(reference),
                     'cell_adverse_upper':str(uniform),
                     'argmax_over_C':str(F(arg,Q)),'window_knots':knots})
    slope = F(4,7)-eps-ry
    q = slope*rho-F(1,2)-eps-eps**2/2+ry**2/2
    outer_exp_upper = F(exp_neg(q,bits)[1],Q)
    need(slope > 0 and q > 0 and outer_exp_upper < 3*ALPHA, 'outer density comparison')
    constant = F(1,2)+eps+eps**2/2
    source_inside = 3*ALPHA*min(F(exp_neg(constant,bits)[0],Q),
        F(exp_neg(rho*rho/2-(F(4,7)-eps)*rho+constant,bits)[0],Q))
    target_inside = F(exp_neg((rho+ry)**2/2,bits)[0],Q)
    need(min(source_inside,target_inside) > left, 'low endpoint has a gap')
    need(F(exp_neg(F(1,2),bits)[1],Q) < F(61,100), 'peak scalar')
    peak = 6*ALPHA*F(61,100)+BETA+eps
    need(peak < right, 'upper endpoint has a gap')
    loss = (1-2*eps)**2-F(3,64)
    need(loss > F(1,256) and 1+2*eps < 3 and 2*ry < 3, 'rational frontier geometry')
    inherited = json.loads((HERE/'../gaussian_frontier_middle_cell/CELL.json').read_text())
    weights = list(map(F,inherited['weights']))
    decompose(weights)
    ys = [tuple(F(v,256) for v in row) for row in inherited['rank_six_target_integer_numerators']]
    det = determinant([list(CENTERS[i])+list(ys[i]) for i in range(1,7)])
    need(det != 0 and all(abs(v) <= F(1,16) for row in ys for v in row), 'inherited rank-six member')
    return {'status':'GAP_FREE_PRIOR_SIMPLEX_CELL_PASS',
            'cell_sha256':sha256(raw).hexdigest(),'dependency_sha256':PINS,
            'variance':1,'middle_window':[str(left),str(right)],'claimed_middle_upper':'-1/256',
            'step':str(h),'half_grid':M,'precision_bits':bits,
            'full_lattice_sites_per_vertex':(2*M+1)**3,'spatial_orbit_representatives':orbits,
            'distinguished_coordinate_records':split_entries,'vertex_orbits':rows,
            'quadrature_error':str(quad),'tail_error':str(tail),
            'uniform_perturbation_loss':str(perturbation),
            'uniform_middle_upper':str(max(F(row['cell_adverse_upper']) for row in rows)),
            'outer_slope_lower':str(slope),'outer_exponent':str(q),
            'outer_exp_upper':str(outer_exp_upper),'outer_coefficient':str(3*ALPHA),
            'source_inside_lower':str(source_inside),'target_inside_lower':str(target_inside),
            'source_peak_upper':str(peak),'seven_label_pair_loss_lower':str(loss),
            'prior_simplex_dimension':6,'denominator156_weight_vectors':comb(36,6),
            'anchored_coordinate_dimension':36,'anchored_coordinate_and_weight_dimension':42,
            'inherited_rank_six_determinant':str(det),'orbit_stream_sha256':digest,
            'controls':checked,
            'scope':'Every threshold, all laws in the stated source/target measure cells, and the full prior simplex at variance one. Author proof; independent review pending; unrestricted majorisation remains open.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--write-expected',action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    record = calculate()
    encoded = (json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if args.write_expected:
        args.expected.write_bytes(encoded)
    else:
        need(json.loads(args.expected.read_text()) == record, 'expected certificate mismatch')
    print(record['status'])
    print('record_sha256',sha256(encoded).hexdigest())
    print('uniform_middle_upper',record['uniform_middle_upper'])
    print('denominator156_weight_vectors',record['denominator156_weight_vectors'])
    print('seconds',round(time.monotonic()-start,3))


if __name__ == '__main__':
    main()
