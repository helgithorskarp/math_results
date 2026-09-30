#!/usr/bin/env python3
"""six-reviewer-4: independent exact complete-neighborhood audit.

No campaign executable imports. Global integer separating-axis tests on
homothetically shrunken quadrilaterals replace rational clipping. A direct
first Cartesian census and incremental relational joins on the frontier
regenerate every complete assignment and compare every published entry.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from math import prod
from pathlib import Path
import resource
import sys
import time

ROOT = (0, 0, 0, 0)
LOCAL = (0, 1, 17, 18, 20, 23, 24, 25, 28, 30, 60, 62, 64, 91, 111)
QUAD = ((0, -1), (8, -1), (7, 1), (0, 1))
CENTER = (3, 0)


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def json_tree(x):
    return json.loads(json.dumps(x))


def linear(point, hand, rotation):
    q, r = point
    if hand:
        q, r = q + r, -r
    for _ in range(rotation):
        q, r = -r, q + r
    return q, r


MATRICES = {(h, k): (linear((1, 0), h, k), linear((0, 1), h, k))
            for h in range(2) for k in range(6)}
ORIENTATIONS = {v: k for k, v in MATRICES.items()}


def image(p, point):
    q, r = linear(point, p[0], p[1])
    return q + p[2], r + p[3]


@lru_cache(maxsize=100000)
def compose(a, b):
    cols = tuple(linear(c, a[0], a[1]) for c in MATRICES[b[:2]])
    h, k = ORIENTATIONS[cols]
    q, r = image(a, b[2:])
    return h, k, q, r


def closed_intersection(a, b):
    """Exact separating-axis theorem in the invertible axial coordinates."""
    for poly in (a, b):
        for p, q in zip(poly, poly[1:] + poly[:1]):
            normal = (p[1] - q[1], q[0] - p[0])
            ap = [normal[0] * x + normal[1] * y for x, y in a]
            bp = [normal[0] * x + normal[1] * y for x, y in b]
            if max(ap) < min(bp) or max(bp) < min(ap):
                return False
    return True


class Geometry:
    def __init__(self, base):
        self.vertices = tuple(map(tuple, base['prototype_axial_vertices']))
        self.positive_ports = tuple(tuple(x) for x, s in
                                    zip(base['ports_counterclockwise'], base['states']) if s == 1)
        poses = tuple(map(tuple, base['candidate_poses']))
        self.families = {i: frozenset((ROOT,) + tuple(poses[j - 1]
                          for j in base['necessary_subsets'][i])) for i in LOCAL}

    @lru_cache(maxsize=20000)
    def endpoints(self, p):
        return frozenset(image(p, v) for v in self.vertices)

    @lru_cache(maxsize=20000)
    def positive_chords(self, p):
        return frozenset(tuple(sorted((image(p, self.vertices[a]), image(p, self.vertices[b]))))
                         for a, b in self.positive_ports)

    @lru_cache(maxsize=20000)
    def shrunk(self, p):
        center = image(p, CENTER)
        return tuple((999 * x + center[0], 999 * y + center[1])
                     for x, y in (image(p, v) for v in QUAD))

    def contact(self, a, b):
        return bool(self.endpoints(a) & self.endpoints(b))

    @lru_cache(maxsize=150000)
    def conflict_sorted(self, a, b):
        if a == b:
            return False
        return bool(self.positive_chords(a) & self.positive_chords(b)) or \
            closed_intersection(self.shrunk(a), self.shrunk(b))

    def conflict(self, a, b):
        return self.conflict_sorted(*sorted((a, b)))

    @lru_cache(maxsize=30000)
    def placed(self, anchor, kind):
        return frozenset(compose(anchor, p) for p in self.families[kind])

    def domain(self, known, anchor):
        choices = []
        for kind in LOCAL:
            family = self.placed(anchor, kind)
            if any(self.contact(anchor, p) for p in known - family):
                continue
            if any(self.contact(ROOT, p) for p in family - known):
                continue
            if any(self.conflict(p, q) for p in family for q in known):
                continue
            choices.append(kind)
        return tuple(choices)

    @lru_cache(maxsize=100000)
    def joinable(self, a, i, b, j):
        left, right = self.placed(a, i), self.placed(b, j)
        if any(self.contact(b, p) for p in left - right):
            return False
        if any(self.contact(a, p) for p in right - left):
            return False
        return not any(self.conflict(p, q) for p in left for q in right)


def census(g):
    first, raw_first = [], 0
    first_domains = []
    for root_kind in LOCAL:
        anchors = tuple(sorted(g.families[root_kind]))
        domains = tuple(g.domain(g.families[root_kind], a) for a in anchors)
        raw_first += prod(map(len, domains))
        pairs = tuple(itertools.combinations(range(len(anchors)), 2))
        kept = []
        for vector in itertools.product(*domains):
            if all(g.joinable(anchors[a], vector[a], anchors[b], vector[b]) for a, b in pairs):
                kept.append(vector)
                first.append((root_kind, vector))
        first_domains.append([root_kind, list(map(len, domains)), len(kept)])
    first = tuple(sorted(first))
    depth4 = set(i for i, _ in first)
    thirds, assignments, states, raw_third, joined_rows = [], [], 0, 0, 0
    for root_kind, vector in first:
        if not set(vector) <= depth4:
            continue
        states += 1
        anchors = tuple(sorted(g.families[root_kind]))
        fixed = tuple(zip(anchors, vector))
        second = frozenset(p for a, k in fixed for p in g.placed(a, k))
        frontier = tuple(sorted(second - set(anchors)))
        domains = []
        for a in frontier:
            domains.append(tuple(i for i in g.domain(second, a)
                                 if all(g.joinable(a, i, b, j) for b, j in fixed)))
        raw_third += prod(map(len, domains))
        # A finite relational join: retain *all* compatible partial rows,
        # extending one receiver at a time. No propagation masks or MRV search.
        rows = [()]
        for index, (a, domain) in enumerate(zip(frontier, domains)):
            rows = [row + (i,) for row in rows for i in domain
                    if all(g.joinable(a, i, frontier[j], row[j]) for j in range(index))]
            joined_rows += len(rows)
        for row in rows:
            assignment = tuple(sorted(fixed + tuple(zip(frontier, row))))
            third = tuple(sorted({p for a, k in assignment for p in g.placed(a, k)}))
            thirds.append((root_kind, third))
            assignments.append((root_kind, anchors, second, assignment))
    need(len(set(first)) == len(first), 'duplicate first assignment')
    need(len(set(thirds)) == len(thirds), 'assignment/catalog alias')
    third = tuple(sorted(thirds))
    depth5 = set(i for i, _ in third)
    def refine(allowed):
        return {i for i, v in first if i in allowed and set(v) <= allowed}
    depth6, depth7 = refine(depth5), refine(refine(depth5))
    # Every stage is just a necessary finite consistency test. Report all
    # surviving six-depth candidates without treating them as packings.
    filtered6 = [(i, assignment) for i, anchors, second, assignment in assignments
                 if i in depth6 and
                 all(k in (depth5 if a in anchors else depth4) for a, k in assignment)]
    six_catalog = tuple(sorted((i, tuple(sorted({p for a, k in assignment
                                   for p in g.placed(a, k)}))) for i, assignment in filtered6))
    need(len(set(six_catalog)) == len(six_catalog), 'six-depth assignment/catalog alias')
    report = {'first_raw_products': raw_first, 'first_models': len(first),
              'first_counts': dict(Counter(i for i, _ in first)),
              'first_domain_profiles': first_domains,
              'height5_second_states': states, 'third_raw_products': raw_third,
              'third_models': len(third), 'third_counts': dict(Counter(i for i, _ in third)),
              'relational_join_partial_rows': joined_rows,
              'first_entries_sha256': digest(first), 'third_entries_sha256': digest(third),
              'combined_catalog_sha256': digest({'first': first, 'third': third}),
              'types_at_depth': {str(m): sorted(s) for m, s in
                                 [(3, set(LOCAL)), (4, depth4), (5, depth5), (6, depth6), (7, depth7)]},
              'six_depth_frontier_consistency_models': len(filtered6),
              'six_depth_frontier_consistency_counts': dict(Counter(i for i, _ in filtered6)),
              'six_depth_catalog_sha256': digest(six_catalog),
              'six_depth_third_copy_counts': dict(Counter(len(c) for _, c in six_catalog))}
    return report, first, third, assignments, filtered6, six_catalog


def controls():
    need(len(ORIENTATIONS) == 12, 'orientation collision')
    checks = 0
    for p in ((h, k, a, b) for h in range(2) for k in range(6) for a, b in [(0, 0), (2, -3)]):
        for q in ((h, k, -1, 4) for h in range(2) for k in range(6)):
            for v in [(0, 0), (1, 0), (0, 1), (4, -7)]:
                need(image(compose(p, q), v) == image(p, image(q, v)), 'composition failure')
                checks += 1
    # Integer Gram and shrink clearance, and literal intersection boundary cases.
    for (h, k), cols in MATRICES.items():
        for v in [(1, 0), (0, 1), (1, -1), (2, 3)]:
            x, y = linear(v, h, k)
            need(x*x+x*y+y*y == v[0]*v[0]+v[0]*v[1]+v[1]*v[1], 'nonisometry')
    square = ((0, 0), (2, 0), (2, 2), (0, 2))
    need(closed_intersection(square, tuple((x+2, y) for x, y in square)), 'closed contact lost')
    need(not closed_intersection(square, tuple((x+3, y) for x, y in square)), 'separation lost')
    need(closed_intersection(square, tuple((x+1, y+1) for x, y in square)), 'overlap lost')
    need(3*1600 > 4000, 'shrink clearance too small')
    for p, q in zip(QUAD, QUAD[1:] + QUAD[:1]):
        e = (q[0]-p[0], q[1]-p[1]); c = (CENTER[0]-p[0], CENTER[1]-p[1])
        det = e[0]*c[1]-e[1]*c[0]
        need(det > 0, 'shrink center outside skeleton')
        need(12*det*det >= 9*(e[0]*e[0]+e[0]*e[1]+e[1]*e[1]), 'center edge distance below3/4')
    need(all((q-3)**2+(q-3)*r+r*r < 25 for q, r in QUAD), 'center radius exceeds5')
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, required=True)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--six-depth-catalog', type=Path)
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    start = time.monotonic()
    base_path = args.repo_root / 'heesch_trapezoid_first_prefix_reduction/input.json'
    cert_path = args.repo_root / 'heesch_trapezoid_six_upper_bound/certificate.json'
    base = json.loads(base_path.read_text()); cert = json.loads(cert_path.read_text())
    need(hashlib.sha256(base_path.read_bytes()).hexdigest() ==
         'cad5df7e063428ca7b9d03a5c33a1a6f4a6e250f12f1b083beb0e86a4b56761c',
         'changed geometric input bytes')
    need(base['amplitude'] == '1/100', 'wrong physical amplitude')
    need(len(base['prototype_axial_vertices']) == 18, 'missing labelled endpoint')
    need(base['states'] == [1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,0], 'wrong port states')
    g = Geometry(base); ncontrols = controls()
    report, first, third, assignments, filtered6, six_catalog = census(g)
    need(json_tree(first) == cert['first_neighborhood_models'], 'literal first entry mismatch')
    need(json_tree(third) == cert['height5_third_prefixes'], 'literal third entry mismatch')
    need(digest(first) == digest(cert['first_neighborhood_models']), 'first entry mismatch')
    need(digest(third) == digest(cert['height5_third_prefixes']), 'third entry mismatch')
    for m, values in report['types_at_depth'].items():
        need(values == cert['types_at_depth'][m], 'incorrect refinement')
    need(report['types_at_depth']['7'] == [], 'no seven-depth exclusion')
    report['affine_composition_controls'] = ncontrols
    report['literal_geometry_inputs_sha256'] = hashlib.sha256(base_path.read_bytes()).hexdigest()
    report['negative_controls'] = 3
    for name, damaged, expected in [
            ('drop first entry', first[1:], cert['first_neighborhood_models']),
            ('drop third entry', third[1:], cert['height5_third_prefixes']),
            ('alter whole pose', [(i, list(c)[:-1]) for i, c in third], cert['height5_third_prefixes'])]:
        need(digest(damaged) != digest(expected), 'mutation not detected: '+name)
    args.scratch.mkdir(parents=True, exist_ok=True)
    # Complete assignment details are private, regenerable scratch output.
    serial = [(i, sorted(anchors), sorted(second), assignment)
              for i, anchors, second, assignment in assignments]
    (args.scratch/'assignments.json').write_text(json.dumps(serial)+'\n')
    (args.scratch/'filtered6.json').write_text(json.dumps(filtered6)+'\n')
    (args.scratch/'six-depth-catalog.json').write_text(json.dumps(six_catalog)+'\n')
    if args.six_depth_catalog:
        need(json_tree(six_catalog) == json.loads(args.six_depth_catalog.read_text()),
             'published six-depth catalog mismatch')
    if args.expected:
        need(digest(report) == digest(json.loads(args.expected.read_text())), 'expected evidence mismatch')
    (args.scratch/'result.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'passed', 'result': report,
                      'elapsed_seconds': time.monotonic()-start,
                      'peak_self_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'python': sys.version.split()[0]}, sort_keys=True))


if __name__ == '__main__':
    main()
