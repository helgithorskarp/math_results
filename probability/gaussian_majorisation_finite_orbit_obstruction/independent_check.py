#!/usr/bin/env python3
"""Separate six-axis/Laurent-polynomial audit, importing no other verifier."""
from fractions import Fraction as R
import json
from pathlib import Path


def check(ok, message):
    if not ok:
        raise ValueError(message)


def determinant(rows):
    a,b,c = rows
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            -a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))


def main():
    cert = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    a,b = cert['A'],cert['B']
    # The paired coordinate sum/difference separates these two spans.
    check(determinant(a[:3]) != 0 and determinant(b[:3]) != 0, 'Rank-six block proof')
    normals = b[:2]
    squared_norms = [sum(v*v for v in n) for n in normals]
    inner = sum(x*y for x,y in zip(*normals))
    trace_formula = -1+4*R(inner*inner,squared_norms[0]*squared_norms[1])
    check(trace_formula == R(-5,9) == R(cert['product_trace']), 'Reflection trace formula')
    check((trace_formula-1).denominator != 1, 'Finite-order exclusion input')
    for normal, fixed_indices in zip(normals,[(2,3),(0,3)]):
        check(all(sum(x*y for x,y in zip(normal,a[i])) == 0 for i in fixed_indices),
              'Perpendicular fixed directions')
        check(determinant([a[i] for i in fixed_indices]+[normal]) != 0,
              'Isometric subfamily basis')

    for row, eta, scale, gap in zip(cert['fixtures'],[R(0),R(1,16)],
                                    [R(16),R(18)],[R(-1,64),R(-1,384)]):
        # Component norm factors are 1/4 for A, 1/8 for B.
        aw,bw = [1,1,eta,eta],[eta,eta,1,eta]
        weights = list(map(R,row['packet_weights']))
        check(weights == [4*R(v)/scale for v in aw]+[8*R(v)/scale for v in bw],
              'Packet normalization/norm factors')
        # Direct Laurent forms at the six axes, before division by scale.
        source = [5+R(9,2)*eta,2+R(15,2)*eta,
                  5+R(9,2)*eta,2+R(15,2)*eta,
                  R(9,2)+R(11,2)*eta,3+7*eta]
        target = [R(7,2)+6*eta]*4+[6+10*eta,R(3,2)+R(5,2)*eta]
        check(sum(source) == sum(target), 'Equal orbit sums')
        observed = sum(max(t-R(7,2),0)-max(s-R(7,2),0)
                       for s,t in zip(source,target))/(6*scale)
        check(observed == gap == R(row['average_gap_over_c_without_origin']),
              'Six-axis exact hinge sign')
        check(R(row['threshold_over_c_without_origin']) == R(7,2)/scale,
              'Threshold normalization')
    # Definition-level isometry for the congruent control, with normal B_2.
    normal = b[2]
    for v, target_v in [(a[0],a[0]),(a[1],a[1]),([-x for x in normal],normal)]:
        inner = sum(x*y for x,y in zip(v,normal))
        image = [R(x)-R(2*inner,3)*n for x,n in zip(v,normal)]
        check(image == target_v, 'Congruent control isometry')
    print('SEPARATE_AXIS_AND_TRACE_CHECK_PASS gaps=-1/64,-1/384 trace=-5/9')


if __name__ == '__main__':
    main()
