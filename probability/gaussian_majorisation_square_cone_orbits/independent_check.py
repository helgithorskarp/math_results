#!/usr/bin/env python3
"""Separate exact algorithm: polynomial multiplication, BFS, and all upper-set pairs.

Imports no constructor code. Reads the compact order certificate, but checks
every needed coefficient inequality and every finite correlation inequality.
This is algorithmic cross-checking, not independent mathematical peer review.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json

N = 48
A = ((1,0,1),(0,1,1),(-1,0,1),(0,-1,1))
B = ((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1))
WA, WB = (12,7,15,44), (21,11,23,43)


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def encoded(value):
    return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()


def matrices():
    out = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if len({i,j,k}) != 3:
                    continue
                for bits in range(8):
                    m = [[0]*3 for _ in range(3)]
                    for row,col in enumerate((i,j,k)):
                        m[row][col] = 1 if bits >> (2-row) & 1 else -1
                    out.append(tuple(tuple(row) for row in m))
    return out


def shifted_monomial(powers):
    """Repeated polynomial multiplication, without binomial coefficients."""
    polynomial = {(0,0,0):1}
    for axis,power in enumerate(powers):
        need(power >= 0,'Uncleared negative exponent')
        for _ in range(power):
            result = dict(polynomial)
            for key,value in polynomial.items():
                other = list(key)
                other[axis] += 1
                other = tuple(other)
                result[other] = result.get(other,0)+value
            polynomial = result
    return polynomial


def coefficient_data(points, group):
    data = []
    for matrix in group:
        row = []
        for point in points:
            e = [sum(point[i]*matrix[i][j] for i in range(3)) for j in range(3)]
            row.append(shifted_monomial((1+e[0],2+e[0]+e[1],3+sum(e))))
        data.append(row)
    return data


def check_coefficients(up, data, base):
    keys = sorted(set().union(*(p.keys() for row in data for p in row)))
    least = None
    tested = 0
    for i in range(N):
        need(up[i] >> i & 1,'Missing reflexivity')
        need(up[i] >> N == 0,'An order vertex exceeds the group')
        for j in range(N):
            if not up[i] >> j & 1:
                continue
            need(i == j or not up[j] >> i & 1,'Order cycle')
            need(up[j] & ~up[i] == 0,'Missing transitive edge')
            for key in keys:
                form = [data[j][l].get(key,0)-data[i][l].get(key,0) for l in range(4)]
                value = sum(c*w for c,w in zip(form,base))
                need(value >= 0,'Negative coefficient in a claimed order')
                if any(form):
                    need(value > 0,'Weight-dependent zero coefficient is not robust')
                    ratio = Fraction(value,184*max(map(abs,form)))
                    least = ratio if least is None else min(least,ratio)
                    tested += 1
    need(least is not None,'No nonzero forms')
    return least,tested


def breadth_first_upper_sets(up):
    seen,queue = {0},[0]
    for s in queue:
        for vertex in range(N):
            bit = 1 << vertex
            # Add a vertex only after all its strict successors.
            if s & bit == 0 and up[vertex] & ~(s|bit) == 0:
                new = s|bit
                if new not in seen:
                    seen.add(new)
                    queue.append(new)
    return sorted(seen)


def audit():
    here = Path(__file__).resolve().parent
    certificate_bytes = (here/'CERTIFICATE.json').read_bytes()
    cert = json.loads(certificate_bytes)
    need(cert['schema'] == 'square-cone-orbit-orders-v1','Unknown certificate schema')
    need(cert['group_size'] == 48 and cert['base_denominator'] == 184,'Wrong normalization')
    need(cert['base_probability_numerators'] == [8,*WA,*WB],'Wrong weight vector')
    need(cert['points_A'] == [list(x) for x in A] and cert['points_B'] == [list(x) for x in B],
         'Wrong theorem configuration')
    group = matrices()
    index = {m:i for i,m in enumerate(group)}
    need(len(index) == 48,'Wrong signed-permutation enumeration')
    negative = [index[tuple(tuple(-x for x in row) for row in m)] for m in group]
    need(all(negative[negative[i]] == i and negative[i] != i for i in range(N)),
         'Antipodal map is not a fixed-point-free involution')
    orders = {name:cert['orders'][name]['up'] for name in ('A','B')}
    counts = {}; margins = {}; forms = {}
    for name,points,weights in [('A',A,WA),('B',B,WB)]:
        need(len(orders[name]) == N,'Wrong number of order rows')
        margin,number = check_coefficients(orders[name],coefficient_data(points,group),weights)
        margins[name] = str(margin)
        forms[name] = number
        counts[name] = sum(row.bit_count() for row in orders[name])
        need(margin >= Fraction(1,552),'Insufficient weight neighborhood')

    aa = breadth_first_upper_sets(orders['A'])
    bb = breadth_first_upper_sets(orders['B'])
    opposite_b = [sum(1 << negative[i] for i in range(N) if s >> i & 1) for s in bb]
    hist = {}; minimum = N; digest = hashlib.sha256()
    for s in aa:
        for t,opposite in zip(bb,opposite_b):
            gap = (s&t).bit_count()-(s&opposite).bit_count()
            need(gap >= 0,'A universal upper-set correlation is false')
            minimum = min(minimum,gap)
            hist[gap] = hist.get(gap,0)+1
            digest.update(bytes([gap+N]))

    # Meaningful invalid certificate control: reverse a strict A comparison.
    a_data = coefficient_data(A,group)
    invalid = [row for row in orders['A']]
    i,j = next((i,j) for i in range(N) for j in range(N)
               if i != j and invalid[i] >> j & 1)
    invalid[j] |= 1 << i
    rejected = False
    try:
        check_coefficients(invalid,a_data,WA)
    except RuntimeError:
        rejected = True
    need(rejected,'Corrupted comparison was accepted')
    return {
        'status':'SQUARE_CONE_ALL_UPPER_SETS_CROSSCHECK_PASS',
        'certificate_sha256':hashlib.sha256(certificate_bytes).hexdigest(),
        'ordered_pairs':counts, 'nonzero_coefficient_forms_checked':forms,
        'weight_L1_margins':margins,
        'A_upper_sets':len(aa), 'B_upper_sets':len(bb),
        'upper_set_pairs':len(aa)*len(bb), 'minimum_correlation_gap':minimum,
        'correlation_gap_histogram':hist, 'all_pair_digest':digest.hexdigest(),
        'invalid_comparison_rejected':True,
        'trust_boundary':'Separate exact polynomial expansion and enumeration algorithm. The universal Gaussian transfer is the written proof; this is not peer review or formalization.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    result = encoded(audit())
    if args.check:
        need(result == Path(__file__).with_name('INDEPENDENT_EXPECTED.json').read_bytes(),
             'Independent audit record differs')
        print('SQUARE_CONE_ALL_UPPER_SETS_CROSSCHECK_PASS',hashlib.sha256(result).hexdigest())
    else:
        print(result.decode(),end='')


if __name__=='__main__':
    main()
