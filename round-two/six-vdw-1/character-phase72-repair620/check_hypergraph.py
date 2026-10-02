"""Independent actual-residue/square-set checker; imports no producer."""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def hash_list(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def check(record, mask):
    need(type(mask) is int and 0 <= mask < 1024, 'explicit absolute phase input')
    need(record['schema'] == 'F31_CHARACTER_PHASE20_BAD_SUPPORTS_V1'
         and record['q'] == 31 and record['period'] == 620
         and record['phase_period'] == 20 and record['mask'] == mask, 'exact physical family')
    squares = {(x * x) % 31 for x in range(1, 31)}
    need(len(squares) == 15 and 0 not in squares, 'literal nonzero square set')
    chi = [None] + [0 if r in squares else 1 for r in range(1, 31)]
    lower = [int(bool(mask & (2 ** i))) for i in range(10)]
    phase = lower + [1 - bit for bit in lower]
    need(record['character_word'] == chi and record['phase_word'] == phase,
         'entire square-set character and absolute phase decoding')
    phase_bad = 0
    for origin in range(20):
        for diff in range(1, 20):
            bits = [phase[(origin + j * diff) % 20] for j in range(7)]
            phase_bad += int(all(bit == bits[0] for bit in bits))
    need(phase_bad == 0, 'all380 original phase APs legal')
    colors = [None if n % 31 == 0 else chi[n % 31] ^ phase[n % 20]
              for n in range(620)]
    regular = poles = bad = constant_regular = constant_bad = 0
    edges = set()
    primitive = []
    # Every original physical progression, before any normalization or projection.
    for origin in range(620):
        for diff in range(1, 620):
            actual = [(origin + j * diff) % 620 for j in range(7)]
            if any(colors[n] is None for n in actual):
                poles += 1
                continue
            regular += 1
            is_constant_field = diff % 31 == 0
            constant_regular += int(is_constant_field)
            monochromatic = all(colors[n] == colors[actual[0]] for n in actual)
            if not monochromatic:
                continue
            bad += 1
            constant_bad += int(is_constant_field)
            support = tuple(sorted({n % 31 for n in actual}))
            need(len(support) == 7 and 0 not in support, 'seven distinct reference-regular columns')
            edges.add(support)
            if diff % 31 == 1:
                primitive.append([origin % 31, origin % 20, diff % 20, colors[origin]])
    need(regular == 299400 and poles == 84380 and regular + poles == 383780,
         'complete original cyclic domain including nonunit/repeated modular APs')
    need(constant_regular == 11400 and constant_bad == 0, 'all constant-field original APs mixed')
    edge_list = [list(e) for e in sorted(edges)]
    primitive.sort()
    need(record['edges'] == edge_list, 'ENTIRE independent original-AP projected hypergraph')
    need(record['monochromatic_primitive_patterns'] == primitive,
         'ENTIRE literal field-step-one subset, independently found among original APs')
    need(record['normalized_field_starts'] == sorted({row[0] for row in primitive}),
         'whole field-start list')
    need(record['tested_normalized_patterns'] == 9600
         and record['tested_constant_field_patterns'] == 380
         and record['constant_field_bad_patterns'] == 0, 'complete claimed pattern domains')
    need(bad == 30 * len(primitive), 'whole normalized-to-original multiplicity')
    degrees = [sum(r in e for e in edges) for r in range(1, 31)]
    need(record['edge_degrees'] == degrees and len(set(degrees)) == 1 and degrees[0] > 0,
         'all actual vertex degrees, positive and constant')
    need(record['edge_sha256'] == hash_list(edge_list)
         and record['primitive_sha256'] == hash_list(primitive), 'full canonical hashes')
    point_actions = edge_actions = multiplicativity = antipodal = h3 = 0
    for n in range(620):
        if colors[n] is not None:
            need(colors[(n + 310) % 620] == 1 - colors[n], 'actual antipodal point identity')
            antipodal += 1
            for h in [1, 5, 25]:
                images = [t for t in range(620) if t % 31 == h * (n % 31) % 31
                          and t % 20 == n % 20]
                need(len(images) == 1 and colors[images[0]] == colors[n], 'actual H3 background point identity')
                h3 += 1
    for mu in range(1, 31):
        units = [u for u in range(1, 620) if u % 31 == mu and u % 20 == 1]
        need(len(units) == 1 and math.gcd(units[0], 620) == 1, 'actual unique CRT field-scalar unit')
        unit = units[0]
        for r in range(1, 31):
            need(chi[mu * r % 31] == chi[r] ^ chi[mu], 'literal square-set multiplicativity')
            multiplicativity += 1
        for n in range(620):
            if colors[n] is not None:
                need(colors[unit * n % 620] == colors[n] ^ chi[mu], 'actual600-point scalar flip')
                point_actions += 1
        for edge in edges:
            need(tuple(sorted(mu * r % 31 for r in edge)) in edges, 'actual entire scalar-edge permutation')
            edge_actions += 1
    field_regular = field_bad = 0
    for a in range(31):
        for d in range(1, 31):
            points = [(a + j * d) % 31 for j in range(7)]
            if 0 in points:
                continue
            field_regular += 1
            field_bad += int(all(chi[r] == chi[points[0]] for r in points))
    need(field_regular == 720 and field_bad == 0, 'complete pure-character fieldAP7 check')
    need(all(set(e) & squares and set(e) - squares for e in edges), 'both15-column character classes cover every edge')
    degree = degrees[0]
    need(Fraction(len(edges), degree) == Fraction(30, 7), 'exact rational uniform fractional dual total')
    phase_orbit = set()
    for unit in range(20):
        if math.gcd(unit, 20) != 1:
            continue
        for shift in range(20):
            image = [phase[(unit * s + shift) % 20] for s in range(20)]
            need(all(image[s + 10] == 1 - image[s] for s in range(10)), 'actual phase-affine antipodal images')
            phase_orbit.add(sum(image[i] * (2 ** i) for i in range(10)))
    return {'author': 'six-vdw-1', 'role': 'researcher',
            'status': 'COMPLETE_INDEPENDENT_ACTUAL_AP_HYPERGRAPH_AUDIT', 'mask': mask,
            'all_original_cyclic_pairs': regular + poles, 'regular_pairs': regular,
            'pole_pairs': poles, 'actual_monochromatic_pairs': bad,
            'actual_constant_field_regular_pairs': constant_regular,
            'normalized_bad_patterns': len(primitive),
            'normalized_field_starts': sorted({row[0] for row in primitive}),
            'distinct_edges': len(edges), 'degree': degree,
            'edge_sha256': hash_list(edge_list), 'primitive_sha256': hash_list(primitive),
            'all_scalar_point_identities': point_actions, 'all_scalar_edge_identities': edge_actions,
            'all_character_multiplicativity_inputs': multiplicativity,
            'all_antipodal_point_identities': antipodal, 'all_H3_background_point_identities': h3,
            'all_pure_character_regular_field_pairs': field_regular,
            'pure_character_monochromatic_field_pairs': field_bad,
            'phase_affine_orbit_masks': sorted(phase_orbit),
            'fractional_cover_optimum': {'numerator': 30, 'denominator': 7},
            'explicit_cover_upper_bound': 15,
            'scope': 'One complete legal profile and its phase orbit; no integer cover optimum, repair sufficiency or coloring.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--mask', type=int, default=72)
    args = parser.parse_args()
    print(json.dumps(check(json.loads(args.certificate.read_text()), args.mask), sort_keys=True))
