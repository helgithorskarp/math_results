"""Finite hypotheses for RECEIVING_CAPS.md; Python 3.11+, standard library.

This regenerates the original-body minimum spectrum, tangent disks, and
translation-free half-difference shadows. The continuum proof and the
published RID all-source cap theorem are explicit written dependencies.
"""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

from model import FACES, VERTICES, cupola_construction, s
from q5 import Q, add, cross, dot, scale, sub
from shadow import hull_indices, projection
from verify import absolute, area_candidates, brightness, canonical
from verify import common_shadow_cone, require, sign_enclosure, validate_model


def minimum_units():
    phi = (1+s)/2
    return [(Q(1), Q(), Q()), (Q(), Q(1), Q())] + [
        scale(Q(1)/(2*phi), (Q(1), a*phi, b*phi*phi))
        for a, b in itertools.product((-1, 1), repeat=2)]


def half_difference_area(vertices, unit):
    """Exact half-difference hull, plus separable all-original support audit.

    Each hull point is an original corner half-difference. For each edge,
    minimizing its linear functional over all original half-differences is
    half the minimum minus the maximum over the original vertices. Thus the
    support audit covers all ordered original pairs, without storing them.
    """
    require(dot(unit, unit) == 1, 'physical unit normal')
    original_hull = hull_indices(vertices, unit)
    corners = [projection(vertices[i], unit) for i in original_hull]
    differences = tuple(sorted({scale(Q(1)/2, sub(p, q))
                                for p in corners for q in corners}, key=repr))
    hull = hull_indices(differences, unit)
    polygon = [differences[i] for i in hull]
    area_vector = (Q(), Q(), Q())
    for p, q in zip(polygon, polygon[1:]+polygon[:1]):
        area_vector = add(area_vector, scale(Q(1)/2, cross(p, q)))
        inward = cross(unit, sub(q, p))
        values = [dot(inward, v) for v in vertices]
        slack = (min(values)-max(values))/2-dot(inward, p)
        require(slack == 0, 'edge supports all original half-differences')
        for w in polygon:
            if w != p and w != q:
                require(dot(inward, sub(w, p)) > 0,
                        'complete strict half-difference corner order')
    area = dot(area_vector, unit)
    require(area > 0, 'positive physical half-difference area')
    require(all(tuple(-x for x in p) in polygon for p in polygon),
            'centered half-difference polygon')
    return area, len(hull), len(hull)*len(vertices)


def controls():
    z = (Q(), Q(), Q(1))
    triangle = ((Q(), Q(), Q()), (Q(2), Q(), Q()),
                (Q(), Q(2), Q()))
    square = tuple((Q(a), Q(b), Q())
                   for a, b in itertools.product((-1, 1), repeat=2))
    require(half_difference_area(triangle, z)[:2] == (Q(3), 6),
            'area-two triangle has area-three half-difference hexagon')
    translated = tuple(add(p, (Q(100), Q(-79), Q(23))) for p in triangle)
    require(half_difference_area(translated, z)[:2] == (Q(3), 6),
            'physical translation cancels exactly')
    require(half_difference_area(square, z)[:2] == (Q(4), 4),
            'central square is unchanged by half-difference')
    require(half_difference_area(triangle, scale(-1, z))[:2] == (Q(3), 6),
            'directed normal reversal preserves physical area')
    return 4


def verify_caps():
    controls_count = controls()
    vectors, original = validate_model()
    candidates, parallel = area_candidates(vectors)
    values = [(brightness(vectors, d)*brightness(vectors, d)/dot(d, d), d)
              for d in candidates]
    a0 = (13+7*s)/2
    levels = sorted(set(x for x, _ in values))
    units = minimum_units()
    require(all(dot(m, m) == 1 for m in units), 'six physical unit normals')
    require(levels[0] == a0*a0, 'global minimum from all candidate facets')
    require({d for x, d in values if x == levels[0]} ==
            {canonical(m) for m in units}, 'exactly the six stated minimum axes')
    require(levels[1] == Q(16727, 7293)/160, 'complete second area level')
    require(levels[1] > (a0+Q(1)/80)*(a0+Q(1)/80),
            'nonminimum polar vertices excluded throughout the area budget')
    require(all((x-levels[0]).sign() == sign_enclosure(x-levels[0])
                for x, _ in values), 'independent complete spectrum signs')
    require(len(candidates) == 613 and parallel == 14, 'complete candidate counts')
    require(Q(14) < a0 < Q(29)/2, 'area bounds for tangent coercivity')
    require(Q(11, 4)/4 < 5, 'original circumradius squared below five')
    facet_square_areas = {3: Q(3)/16, 4: Q(1), 5: Q(25, 10)/16}
    require(all(dot(b, b) == facet_square_areas[len(face)]
                for face, b in zip(FACES, vectors)), 'physical regular face areas')
    # Positive-root upper bounds prove half the surface area is below 30.
    require(Q(3) < Q(Fraction(7, 4)**2), 'triangle root upper bound')
    require(Q(25, 10) < Q(Fraction(69, 10)**2), 'pentagon root upper bound')
    require(Fraction(5, 2)*Fraction(7, 4)+15+
            Fraction(3, 2)*Fraction(69, 10) < 30, 'brightness Lipschitz bound')
    require(Fraction(2, 80*14) < Fraction(1, 400), 'polar enters chord one-twentieth')
    require(Fraction(7, 2)*Fraction(999, 1000)-
            Fraction(29, 2)/40 > 3, 'linear area growth above three times chord')

    tangent_records, difference_records, support_audits = [], [], 0
    for i, m in enumerate(units):
        zeros = [b for b in vectors if dot(b, m) == 0]
        fixed = tuple(sum((b[j]*dot(b, m).sign()/2
                          for b in vectors if dot(b, m) != 0), Q())
                      for j in range(3))
        require(fixed == scale(a0, m), 'centered minimum exposed area facet')
        require(len(zeros) == 12, 'twelve zero-dot physical area vectors')
        require(any(dot(cross(b, c), cross(b, c)) > 0
                    for b, c in itertools.combinations(zeros, 2)), 'tangent generators span plane')
        tangent_axes = {canonical(cross(m, b)) for b in zeros}
        tangent_squared = []
        for t in tangent_axes:
            h = sum((absolute(dot(b, t))/2 for b in zeros), Q())
            require(h > 0, 'positive tangent facet height')
            tangent_squared.append(h*h/dot(t, t))
        rho2 = min(tangent_squared)
        required_rho2 = Q(277)/40+Q(0, 619)/200 if i == 0 else Q(13)/2+Q(0, 29)/10
        require(rho2 == required_rho2, 'sharp tangent disk radius')
        require(rho2 > Q(Fraction(7, 2)**2), 'tangent radius exceeds seven-halves')
        require(all(x.sign() == sign_enclosure(x) for x in tangent_squared),
                'independent tangent support signs')
        tangent_records.append({'axis': i, 'zero_generators': len(zeros),
                                'projective_tangent_facets': len(tangent_axes),
                                'inradius_squared': str(rho2)})
        difference_area, count, audits = half_difference_area(VERTICES, m)
        wanted = a0 if i == 1 else (Q(127)/20+Q(0, 18)/5 if i == 0
                                    else Q(51)/8+Q(0, 143)/40)
        require(difference_area == wanted, 'exact original half-difference area')
        gap = difference_area-a0
        require(gap == 0 if i == 1 else gap > Q(1)/25,
                'positive gap separates every competing source branch')
        difference_records.append({'axis': i, 'corners': count, 'area': str(difference_area),
                                   'extra_area': str(gap)})
        support_audits += audits

    # The global area-continuity bound is 40 times chord on chord <=1/20.
    require(Fraction(22, 7)*(10+Fraction(5, 20)) < 40,
            'Steiner and circumdisk constants below forty')
    require(Fraction(1, 25)-40*Fraction(1, 1200) > Fraction(1, 400),
            'all non-y source branches excluded at transfer budget')
    zeros_y = [b for b in vectors if b[1] == 0]
    representatives_y = [b for b in zeros_y if next(x for x in b if x != 0) > 0]
    require(len(representatives_y) == 6 and
            set(zeros_y) == set(representatives_y) |
            {scale(-1, b) for b in representatives_y},
            'paired y-tangent generators')
    cosine2 = min(b[1]*b[1]/dot(b, b) for b in vectors if b[1] != 0)
    require(cosine2 == Q(3, -1)/8 and cosine2 > Q(Fraction(1, 20)**2),
            'nonzero y signs persist on chord one-twentieth')
    endpoint_squared = []
    for signs in itertools.product((-1, 1), repeat=6):
        g = tuple(sum((t*b[i] for t, b in zip(signs, representatives_y)), Q())
                  for i in range(3))
        endpoint_squared.append(dot(g, g))
    require(max(endpoint_squared) == Q(10, 4) < Q(Fraction(35, 8)**2),
            'local receiving brightness grows by less than thirty-five-eighths times chord')
    require(Fraction(35, 8*1750) <= Fraction(1, 400),
            'closed-fit transfer cap uses only the proved area budget')
    rho = (s-1)/8
    require(rho > Q(3)/20, 'explicit common-cone margin')
    require(Q(1)/20 < rho*(1-Q(1)/800), 'chord one-twentieth lies in common cone')
    require(Fraction(30, 30000) <= Fraction(1, 400), 'full RID cap lies in transfer budget')
    original_rid = cupola_construction()[0]
    phi = (1+s)/2
    rid_edge_two = set()
    for base in ((Q(1), Q(1), phi*phi*phi),
                 (phi*phi, phi, 2*phi), (2+phi, Q(), phi*phi)):
        for signs in itertools.product((-1, 1), repeat=3):
            p = tuple(x*y for x, y in zip(signs, base))
            rid_edge_two.update((p, (p[1], p[2], p[0]), (p[2], p[0], p[1])))
    require(rid_edge_two == {scale(2, p) for p in original_rid},
            'cited edge-two RID is twice the common-cone RID')
    cone = common_shadow_cone()
    return {'original_vertices': original['vertices'], 'original_facets': original['facets'],
            'original_support_sign_audits': original['support_sign_audits'],
            'projective_area_candidates': len(candidates), 'distinct_area_levels': len(levels),
            'candidate_spectrum_sha256': hashlib.sha256(
                ''.join(repr(d)+':'+str(x)+'\n' for x, d in values).encode()).hexdigest(),
            'minimum_area': str(a0), 'second_area_squared': str(levels[1]),
            'global_area_budget': '1/80', 'source_chord_per_area_excess': '1/3',
            'tangent_facets': tangent_records, 'half_difference_shadows': difference_records,
            'half_difference_original_support_audits': support_audits,
            'half_difference_area_lipschitz': '40 on chord <=1/20',
            'common_cone_closed_fit_transfer_area_budget': '1/400',
            'y_nonzero_generator_minimum_cosine_squared': str(cosine2),
            'y_tangent_endpoint_count': len(endpoint_squared),
            'y_tangent_maximum_radius_squared': str(max(endpoint_squared)),
            'closed_fit_transfer_cap_chord_radius': '1/1750',
            'receiving_cap_chord_radius': '1/30000',
            'common_cone_strict_receiving_area_gap': '1/10000',
            'rid_original_vertices_scale': 'edge-two input is 2 times unit-edge RID',
            'hand_controls': controls_count, **cone}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true', help='regenerate compact evidence')
    args = parser.parse_args()
    result = verify_caps()
    if args.emit:
        print(json.dumps(result, indent=2))
    else:
        expected = json.loads(Path(__file__).with_name('caps_expected.json').read_text())
        require(result == expected, 'complete receiving-cap evidence matches')
        print(json.dumps({'status': 'exact receiving-cap hypotheses verified',
                          'projective_area_candidates': result['projective_area_candidates'],
                          'half_difference_original_support_audits':
                          result['half_difference_original_support_audits'],
                          'receiving_cap_chord_radius': result['receiving_cap_chord_radius']}, indent=2))
