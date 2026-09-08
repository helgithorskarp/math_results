"""Exact geometry for the unavoidable core and a deduplicated EI assembly."""
import hashlib
import importlib.util
import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
EI = REPOSITORY / 'hadwiger_nelson_ei_interface_minima'
T375 = REPOSITORY / 'hadwiger_nelson_small_triangle_forcer375'


def check_dependencies():
    expected = json.loads((ROOT / 'dependency_hashes.json').read_text())
    for name, digest in expected.items():
        actual = hashlib.sha256((REPOSITORY / name).read_bytes()).hexdigest()
        if actual != digest:
            raise ValueError(f'changed dependency: {name}')


check_dependencies()
spec = importlib.util.spec_from_file_location('ei_physical_order_assembly', EI / 'assembly.py')
assembly = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assembly)


def inputs():
    g40 = list(map(assembly.point, json.loads((EI / 'g40.json').read_text())))
    g49 = list(map(assembly.point, json.loads((EI / 'g49.json').read_text())))
    certificate = json.loads((EI / 'certificate.json').read_text())
    pairs = [(i, j) for i, j in combinations(range(40), 2)
             if assembly.distance(g40[i], g40[j]) == assembly.scalar(4752)]
    triangles = [t for t in combinations(range(49), 3)
                 if all(assembly.distance(g49[i], g49[j]) == assembly.scalar(432)
                        for i, j in combinations(t, 2))]
    if len(pairs) != 59 or len(triangles) != 18:
        raise ValueError('source incidence mismatch')
    return g40, g49, pairs, triangles, certificate


def put_g40(g40, target_outer, swap, reflect):
    origin = assembly.ZERO, assembly.ZERO
    source_a, source_b = (g40[1], g40[0]) if swap else (g40[0], g40[1])
    frame = assembly.frame(source_a, source_b, origin, target_outer, 9216, reflect)
    placed = [assembly.apply(frame, p) for p in g40]
    shared_label = 1 if swap else 0
    if placed[shared_label] != origin:
        raise ValueError('G40 shared-terminal mismatch')
    return placed


def g49_attachment_sets(g49, u, v):
    copies = []
    for swap, reflect in product((False, True), repeat=2):
        target_a, target_b = (v, u) if swap else (u, v)
        frame = assembly.frame(g49[0], g49[1], target_a, target_b, 4752, reflect)
        copies.append(frozenset(assembly.apply(frame, p) for p in g49))
    return copies


def normalized_g49_kernel(g49):
    copies = g49_attachment_sets(g49, g49[0], g49[1])
    if copies[0] != copies[1] or copies[2] != copies[3]:
        raise ValueError('G49 lacks terminal-axis reflection invariance')
    if copies[0] == copies[2]:
        raise ValueError('G49 endpoint choices unexpectedly coincide')
    kernel = set.intersection(*(set(copy) for copy in copies))
    if len(kernel) != 16:
        raise ValueError('wrong normalized G49 kernel')
    return frozenset(kernel), copies


def place_kernel(kernel, g49, u, v):
    frame = assembly.frame(g49[0], g49[1], u, v, 4752)
    return {assembly.apply(frame, p) for p in kernel}


def spindle_targets(x):
    """The two radius-|x| points at unit distance from x."""
    rotations = assembly.ROT_SPINDLE, assembly.radicals.conjugate(assembly.ROT_SPINDLE)
    targets = tuple(assembly.cmul(rotation, x) for rotation in rotations)
    if any(assembly.norm(y) != assembly.scalar(9216) or
           assembly.distance(x, y) != assembly.scalar(1296) for y in targets):
        raise ValueError('wrong spindle targets')
    if targets[0] == targets[1]:
        raise ValueError('coincident spindle targets')
    return targets


def outer_cases():
    """All normalized outer G40 isometries, modulo one global isometry."""
    g40, g49, pairs, _, certificate = inputs()
    essential = certificate['g40']['essential']
    if len(essential) != 48:
        raise ValueError('wrong compulsory interface size')
    kernel, _ = normalized_g49_kernel(g49)
    x = g40[1]
    ys = spindle_targets(x)
    for first_swap, first_reflect, side, second_swap, second_reflect in product((False, True), repeat=5):
        hosts = (put_g40(g40, x, first_swap, first_reflect),
                 put_g40(g40, ys[side], second_swap, second_reflect))
        outer = set(hosts[0] + hosts[1])
        if len(outer) != 79:
            raise ValueError('wrong outer G40 union')
        core = set(outer)
        for host in hosts:
            for index in essential:
                i, j = pairs[index]
                core.update(place_kernel(kernel, g49, host[i], host[j]))
        yield (first_swap, first_reflect, side, second_swap, second_reflect), outer, core


def selected_pair_indices(certificate, mask):
    return sorted(set(certificate['g40']['essential']) |
                  {index for bit, index in enumerate(certificate['g40']['optional'])
                   if mask >> bit & 1})


def canonical_union(mask=1682):
    """One explicit union: endpoint order by label, terminal order by coordinate."""
    g40, g49, pairs, triangles, certificate = inputs()
    selected = selected_pair_indices(certificate, mask)
    if mask not in certificate['g40']['minimal_covers'] or len(selected) != 53:
        raise ValueError('mask is not a minimum valid support')
    required_triangles = [triangles[i] for i in certificate['g49']['essential']]
    rotated = [assembly.cmul(assembly.ROT_SPINDLE, p) for p in g40]
    union = set(g40 + rotated)
    target_triangles = set()
    pair_supports = []
    for host in (g40, rotated):
        for index in selected:
            i, j = pairs[index]
            outer = assembly.frame(g49[0], g49[1], host[i], host[j], 4752)
            support = frozenset(assembly.apply(outer, p) for p in g49)
            pair_supports.append(support)
            union.update(support)
            for triangle in required_triangles:
                target_triangles.add(frozenset(assembly.apply(outer, g49[v]) for v in triangle))
    pair_union_points = len(union)
    geometry = assembly.load_dependency('geometry')
    t375_certificate = json.loads((T375 / 'certificate.json').read_text())
    reference = geometry.reference()
    forcer = [assembly.point(reference[i]) for i in t375_certificate['retained_reference_indices']]
    if len(forcer) != 375:
        raise ValueError('wrong T375 support')
    terminals = forcer[:3]
    triangle_frames = []
    for target in sorted(target_triangles, key=lambda s: sorted(s)):
        ordered = sorted(target)
        frame = assembly.frame(terminals[0], terminals[1], ordered[0], ordered[1], 432)
        if assembly.apply(frame, terminals[2]) != ordered[2]:
            frame = assembly.frame(terminals[0], terminals[1], ordered[0], ordered[1], 432, True)
        if any(assembly.apply(frame, p) != q for p, q in zip(terminals, ordered)):
            raise ValueError('T375 target mismatch')
        triangle_frames.append(frame)
        union.update(assembly.apply(frame, p) for p in forcer)
    return {
        'minimum_support_mask': mask,
        'outer_points': 79,
        'formal_pair_attachments': 2 * len(selected),
        'unique_pair_supports': len(set(pair_supports)),
        'pair_layer_points': pair_union_points,
        'formal_triangle_obligations': 2 * len(selected) * len(required_triangles),
        'distinct_target_triangles': len(target_triangles),
        'triangle_frames': len(triangle_frames),
        'physical_union_points': len(union),
    }, union


def encode_point(p):
    return [[[value.numerator, value.denominator] for value in axis] for axis in p]


def point_digest(points):
    digest = hashlib.sha256()
    for p in sorted(points):
        digest.update(json.dumps(encode_point(p), separators=(',', ':')).encode() + b'\n')
    return digest.hexdigest()
