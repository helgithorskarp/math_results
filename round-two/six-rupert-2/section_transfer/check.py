#!/usr/bin/env python3
"""Central-section witnesses and enlarged J74 passage transfer.

Python 3.11+, exact Fraction arithmetic in Q(sqrt(5)). The generator uses
projected hulls and opposite-height preimages. The certificate checker
instead checks original-vertex membership, planar convexity and all-pair
separable support bounds; it never trusts a generated silhouette.
"""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import sys
from fractions import Fraction

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_dependency():
    record = json.loads((HERE/'DEPENDENCIES.json').read_text())
    directory = (HERE/record['directory']).resolve()
    required = {'q5.py', 'model.py', 'shadow.py', 'verify.py', 'caps_verify.py',
                'caps_expected.json', 'PROOF.md', 'RECEIVING_CAPS.md'}
    require(set(record['sha256']) == required, 'incomplete pinned source inputs')
    for name, wanted in record['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest() == wanted,
                'changed pinned input: '+name)
    sys.path.insert(0, str(directory))
    import caps_verify
    import model
    import q5
    import shadow
    replay = caps_verify.verify_caps()
    require(replay == json.loads((directory/'caps_expected.json').read_text()),
            'entire prior compact geometric record must regenerate')
    return model, q5, shadow, caps_verify, record


def generate_witnesses(model, q5, shadow, caps):
    """Find direct half-differences or equal opposite-height midpoints.

    This algorithm is a construction finder, not the production verifier.
    """
    V, Q, dot, sub, scale = model.VERTICES, q5.Q, q5.dot, q5.sub, q5.scale
    records = []
    for index, m in enumerate(caps.minimum_units()):
        groups = {}
        for i, v in enumerate(V):
            groups.setdefault(shadow.projection(v, m), []).append(i)
        corners = [shadow.projection(V[i], m) for i in shadow.hull_indices(V, m)]
        differences = tuple(sorted({scale(Q(1)/2, sub(p, q))
                                    for p in corners for q in corners}, key=repr))
        hull = [differences[i] for i in shadow.hull_indices(differences, m)]
        heights = {p: [] for p in hull}
        for p in corners:
            for q in corners:
                d = scale(Q(1)/2, sub(p, q))
                if d not in heights:
                    continue
                for i in groups[p]:
                    for j in groups[q]:
                        heights[d].append((dot(m, sub(V[i], V[j]))/2, i, j))
        lifts = []
        for p in hull:
            zero = [(i, j) for h, i, j in heights[p] if h == 0]
            if zero:
                lifts.append([list(min(zero))])
            else:
                lo, hi = min(heights[p]), max(heights[p])
                require(lo[0] < 0 < hi[0] and lo[0] == -hi[0],
                        'finder needs exact equal opposite-height lifts')
                lifts.append([list(lo[1:]), list(hi[1:])])
        records.append({'axis': index, 'corner_lifts': lifts})
    return records


def check_section(record, index, model, q5, m):
    """Independent finite certificate check of P_m S = S intersect m-perp.

    All points are averages of one or two actual original half-differences.
    Thus convexity puts them in S. An all-original support audit proves the
    resulting planar polygon contains the ENTIRE projection of S.
    """
    Q, add, cross, dot, scale, sub = q5.Q, q5.add, q5.cross, q5.dot, q5.scale, q5.sub
    V = model.VERTICES
    require(set(record) == {'axis', 'corner_lifts'} and record['axis'] == index,
            'unexpected section record or axis')
    require(dot(m, m) == 1, 'physical unit section normal')
    polygon, direct, midpoint = [], 0, 0
    for pairs in record['corner_lifts']:
        require(isinstance(pairs, list) and len(pairs) in (1, 2), 'invalid lift length')
        points = []
        for pair in pairs:
            require(isinstance(pair, list) and len(pair) == 2 and
                    all(type(i) is int and 0 <= i < len(V) for i in pair),
                    'invalid original vertex index')
            i, j = pair
            points.append(scale(Q(1)/2, sub(V[i], V[j])))
        if len(points) == 1:
            p = points[0]
            direct += 1
        else:
            require(dot(m, points[0]) == -dot(m, points[1]) != 0,
                    'midpoint has exact nonzero opposite axial heights')
            p = scale(Q(1)/2, add(points[0], points[1]))
            midpoint += 1
        require(dot(m, p) == 0, 'every lifted corner lies in central section')
        polygon.append(p)
    require(len(polygon) >= 3 and len(set(polygon)) == len(polygon),
            'distinct nondegenerate section polygon corners')
    area_vector, support_audits, corner_gates = (Q(), Q(), Q()), 0, 0
    for p, q in zip(polygon, polygon[1:]+polygon[:1]):
        edge = sub(q, p)
        inward = cross(m, edge)
        require(dot(inward, inward) > 0, 'nonzero section boundary edge')
        for w in polygon:
            if w != p and w != q:
                require(dot(inward, sub(w, p)) > 0,
                        'all other section corners strictly inside every oriented edge')
                corner_gates += 1
        values = [dot(inward, v) for v in V]
        require((min(values)-max(values))/2-dot(inward, p) == 0,
                'boundary supports all 3600 original ordered half-differences')
        support_audits += len(V)
        area_vector = add(area_vector, scale(Q(1)/2, cross(p, q)))
    area = dot(area_vector, m)
    require(area > 0 and area_vector == scale(area, m), 'positive physical planar area')
    require(all(scale(-1, p) in polygon for p in polygon), 'centered symmetric section')
    a0 = (13+7*model.s)/2
    wanted = a0 if index == 1 else (Q(127)/20+Q(0, 18)/5 if index == 0
                                    else Q(51)/8+Q(0, 143)/40)
    require(area == wanted, 'exact full section area')
    return {'axis': index, 'corners': len(polygon), 'direct_lifts': direct,
            'opposite_height_midpoints': midpoint, 'area': str(area),
            'support_evaluations': support_audits, 'strict_boundary_gates': corner_gates}


def negative_controls(witnesses, model, q5, caps):
    records = []
    # A genuine lifted midpoint becomes nonplanar if either half is discarded.
    bad = copy.deepcopy(witnesses[0])
    i = next(i for i, pairs in enumerate(bad['corner_lifts']) if len(pairs) == 2)
    bad['corner_lifts'][i] = [bad['corner_lifts'][i][0]]
    records.append(bad)
    # Reversing one physical half-difference destroys opposite-height matching.
    bad = copy.deepcopy(witnesses[0])
    bad['corner_lifts'][i][1] = bad['corner_lifts'][i][1][::-1]
    records.append(bad)
    # Geometrically valid points in an incorrect cyclic order fail full gates.
    bad = copy.deepcopy(witnesses[0])
    bad['corner_lifts'][0], bad['corner_lifts'][1] = bad['corner_lifts'][1], bad['corner_lifts'][0]
    records.append(bad)
    # Cropping a valid corner fails the all-original completeness support audit.
    bad = copy.deepcopy(witnesses[0])
    bad['corner_lifts'].pop(0)
    records.append(bad)
    for bad in records:
        try:
            check_section(bad, 0, model, q5, caps.minimum_units()[0])
        except ValueError:
            continue
        raise ValueError('malformed central-section certificate was accepted')
    return len(records)


def verify(witnesses, dependency):
    model, q5, shadow, caps, manifest = dependency
    Q, dot = q5.Q, q5.dot
    require(isinstance(witnesses, list) and len(witnesses) == 6, 'all six sections required')
    records = [check_section(record, i, model, q5, m)
               for i, (record, m) in enumerate(zip(witnesses, caps.minimum_units()))]
    require([r['corners'] for r in records] == [18, 12, 16, 16, 16, 16],
            'complete six-section corner inventory')
    require([r['direct_lifts'] for r in records] == [6, 12, 8, 8, 8, 8],
            'direct and midpoint witness inventory')
    a0 = (13+7*model.s)/2
    a1 = Q(51)/8+Q(0, 143)/40
    require(a1*a1 == Q(16727, 7293)/160, 'second polar level equals mixed section area squared')
    require(a1 > a0+Q(1)/25, 'extended polar budget below next level')
    require(Fraction(2, 25*14) < Fraction(2, 25)**2, 'polar enters chord two-twenty-fifths')
    require(Fraction(999, 1000)**2 < 1-Fraction(1, 625), 'positive-root coercivity factor')
    require(Q(13)/2+Q(0, 29)/10 > Q(Fraction(18, 5)**2), 'every tangent radius exceeds eighteen-fifths')
    require(Q(277)/40+Q(0, 619)/200 > Q(13)/2+Q(0, 29)/10,
            'x tangent disk is larger than the other five')
    require(Fraction(18, 5)*Fraction(999, 1000)-Fraction(29, 2)*Fraction(1, 25) > 3,
            'linear localization still exceeds three times chord')
    require(Q(127)/20+Q(0, 18)/5 > a1, 'all non-y sections have area at least a1')
    require(a1*(1-Q(1)/11250) > a0+Q(1)/25,
            'quadratic section loss separates every competing source branch')
    require(Fraction(1, 75) < Fraction(1, 20), 'localized y source lies inside common cone')
    require(Fraction(8, 875) < Fraction(1, 20), 'transfer cap has stable original y signs')
    require(Fraction(35, 8)*Fraction(8, 875) == Fraction(1, 25), 'exact transfer cap budget')
    require(Fraction(1, 270) < Fraction(8, 875), 'entire committed RID cap lies inside transfer band')
    require(Fraction(35, 8*270) == Fraction(7, 432) < Fraction(1, 60),
            'reverse RID source localization holds throughout requested exclusion cap')
    # The reverse existence transfer needs only the published complete RID
    # polar spectrum: its coarse near-axis bound enters the common cone.
    rid_second_area_squared = Q(425, 190)/4
    require(rid_second_area_squared > (a0+Q(1)/25)*(a0+Q(1)/25),
            'published RID nonminimum polar level excludes coarse source competitors')
    cone_ratio = (model.s-1)/8
    require(Q(2)/25 < cone_ratio*(1-Q(2)/625),
            'coarse folded RID source chord two-twenty-fifths lies inside common cone')
    negative = negative_controls(witnesses, model, q5, caps)
    return {'agent': 'six-rupert-2', 'role': 'researcher',
            'section_witnesses': witnesses, 'verified_sections': records,
            'central_section_corner_count': sum(r['corners'] for r in records),
            'direct_lift_count': sum(r['direct_lifts'] for r in records),
            'opposite_height_midpoint_count': sum(r['opposite_height_midpoints'] for r in records),
            'all_original_support_evaluations': sum(r['support_evaluations'] for r in records),
            'strict_boundary_gates': sum(r['strict_boundary_gates'] for r in records),
            'minimum_original_area': str(a0), 'mixed_section_area': str(a1),
            'global_original_area_budget': '1/25', 'source_chord_per_excess': '1/3',
            'minimum_half_difference_area': str(a0),
            'half_difference_minimum_directed_axes': ['+e_y', '-e_y'],
            'global_half_difference_area_budget': '1/25',
            'half_difference_y_chord_per_excess': '1/3',
            'global_half_difference_strict_receiving_area_gap': '1/90',
            'closed_common_cone_source_transfer_area_budget': '1/25',
            'y_closed_source_transfer_cap_chord': '8/875',
            'all_source_J74_exclusion_cap_chord': '1/270',
            'common_cone_strict_receiving_area_gap': '1/90',
            'negative_certificate_controls': negative,
            'pinned_prior_source_commit': manifest['source_commit']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true', help='find and check exact section witnesses')
    args = parser.parse_args()
    dependency = load_dependency()
    if args.emit:
        model, q5, shadow, caps, _ = dependency
        result = verify(generate_witnesses(model, q5, shadow, caps), dependency)
        print(json.dumps(result, indent=2))
    else:
        expected = json.loads((HERE/'expected.json').read_text())
        result = verify(expected['section_witnesses'], dependency)
        require(result == expected, 'every finite-hypothesis result field matches')
        print(json.dumps({key: value for key, value in result.items()
                          if key not in {'section_witnesses', 'verified_sections'}}, indent=2))
