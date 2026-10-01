"""Regenerate six local NO-TWO proofs with exact FACE-centroid joins.

Input: prototype, 26 primitive NO-ONE pairs, six small fixed patterns and
two positive packings.  No solver, discovery catalogue, CNF or trace input.
Written narrow-corner locking licenses arbitrary real supplier enumeration.
"""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

import geometry as c

BASE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


class Checker:
    def __init__(self, data, deadline):
        self.deadline = deadline
        need(data['schema'] == 'T211-six-local-two-surround-obstructions-v1'
             and data['all_real_motions_including_reflections'] is True
             and data['global_finite_upper_proved'] is False, 'incorrect theorem scope')
        self.data = data
        self.fs = frozenset(self.point(f) for f in data['prototype_triangles'])
        need(len(self.fs) == len(data['prototype_triangles']) == 211, 'incorrect prototype')
        self.g = c.Geometry(self.fs)
        self.mesh, _ = c.mesh(self.fs)
        self.provider_cache = {}
        self.forbidden = set()

    def guard(self):
        need(time.monotonic() < self.deadline, 'incomplete time guard; no exclusion')

    def point(self, p):
        need(len(p) == 2 and all(type(x) is int for x in p), 'invalid point')
        return tuple(p)

    def pose(self, p):
        need(len(p) == 6 and all(type(x) is int for x in p)
             and tuple(p[:4]) in self.g.ms, 'invalid D6 pose')
        return tuple(p)

    def fixed(self, rows):
        out = tuple(self.pose(p) for p in rows)
        need(out and len(set(out)) == len(out), 'empty or duplicate fixed copy')
        return out

    def gap(self, fixed, v):
        occupied = self.g.union(fixed)
        star = c.star(v)
        present = [f in occupied for f in star]
        need(sum(present) in (4, 5) and
             sum(present[j] != present[(j+1) % 6] for j in range(6)) == 2,
             'not a contiguous narrow gap')
        return occupied, frozenset(star)-occupied

    def suppliers(self, v, gap):
        key = v, tuple(sorted(gap))
        if key not in self.provider_cache:
            trials = set()
            for m in self.g.ms:
                for f in self.fs:
                    x, y = c.face(m+(0, 0), f)
                    for a, b in gap:
                        if (a-x) % 3 == (b-y) % 3 == 0:
                            trials.add(m+((a-x)//3, (b-y)//3))
            star = set(c.star(v))
            self.provider_cache[key] = tuple(sorted(q for q in trials
                if len(star & self.g.footprint(q)) in (1, 2)
                and star & self.g.footprint(q) <= gap))
            self.guard()
        return self.provider_cache[key]

    def primitive(self, cap):
        need(cap['kind'] == 'primitive_no_one', 'unexpected deeper premise')
        fixed = self.fixed(cap['fixed_poses'])
        need(len(fixed) == 2, 'primitive premise is not a pair')
        v = self.point(cap['vertex'])
        occupied, gap = self.gap(fixed, v)
        raw = self.suppliers(v, gap)
        allowed = [q for q in raw if not self.g.footprint(q) & occupied]
        need(not any(gap <= self.g.footprint(q) for q in allowed), 'one-copy completion of NO-ONE')
        need(not any(gap <= self.g.footprint(q) | self.g.footprint(p)
                     and not self.g.footprint(q) & self.g.footprint(p)
                     for p, q in combinations(allowed, 2)), 'two-copy completion of NO-ONE')
        for anchor in fixed:
            inv = c.inverse(anchor)
            for p in fixed:
                relative = c.compose(inv, p)
                if relative != c.IDENTITY:
                    self.forbidden.add(relative)
        return {'sha256': digest(cap), 'raw_suppliers': len(raw), 'allowed_suppliers': len(allowed)}

    def bad(self, p, q):
        return c.compose(c.inverse(p), q) in self.forbidden

    def formula(self, fixed, vertices):
        occupied = self.g.union(fixed)
        rows, retained = [], set()
        vertices = [self.point(v) for v in vertices]
        need(vertices and len(set(vertices)) == len(vertices), 'empty or duplicate cover target')
        for v in vertices:
            old, gap = self.gap(fixed, v)
            need(old == occupied, 'changed OLD union')
            raw = self.suppliers(v, gap)
            keep = [q for q in raw if not self.g.footprint(q) & occupied
                    and not any(self.bad(p, q) for p in fixed)]
            retained.update(keep)
            rows.append((v, gap, raw, keep))
        poses = sorted(retained)
        need(len(poses) <= 10000, 'incomplete pose guard; no exclusion')
        lookup = {q: j for j, q in enumerate(poses, 1)}
        clauses, covers = [], []
        for v, gap, raw, keep in rows:
            for f in sorted(gap):
                clauses.append([lookup[q] for q in keep if f in self.g.footprint(q)])
            covers.append({'vertex': list(v), 'raw_suppliers': len(raw),
                           'retained_suppliers': len(keep), 'gap_faces': len(gap)})
        clashes, pair_cuts = 0, 0
        for p, q in combinations(poses, 2):
            if self.g.footprint(p) & self.g.footprint(q):
                clauses.append([-lookup[p], -lookup[q]])
                clashes += 1
            elif self.bad(p, q):
                clauses.append([-lookup[p], -lookup[q]])
                pair_cuts += 1
        need(len(clauses) <= 1000000, 'incomplete clause guard; no exclusion')
        self.guard()
        return poses, clauses, {'providers': len(poses), 'clauses': len(clauses),
                               'covers': covers, 'whole_overlap_clauses': clashes,
                               'NO_ONE_pair_clauses': pair_cuts}

    def contradiction(self, clauses):
        assigned, steps = {}, []
        while True:
            chosen = None
            for j, row in enumerate(clauses):
                if any(assigned.get(abs(lit)) == (lit > 0) for lit in row):
                    continue
                open_row = [lit for lit in row if abs(lit) not in assigned]
                if not open_row:
                    return {'unit_steps': len(steps), 'conflict_clause': j,
                            'unit_proof_sha256': digest({'steps': steps, 'conflict': j})}
                if len(open_row) == 1 and chosen is None:
                    chosen = open_row[0], j
            need(chosen is not None, 'necessary formula has no unit contradiction')
            lit, reason = chosen
            assigned[abs(lit)] = lit > 0
            steps.append({'literal': lit, 'reason': reason})
            self.guard()

    def motif(self, motif):
        need(motif['future_surrounds_ruled_out'] == 2, 'incorrect future license')
        fixed = self.fixed(motif['fixed_poses'])
        poses, clauses, report = self.formula(fixed, motif['cover_vertices'])
        return {'id': motif['id'], 'fixed_copies': len(fixed), **report,
                **self.contradiction(clauses), 'future_surrounds_ruled_out': 2}

    def positive(self, fixture, motifs):
        counts = fixture['counts']
        need(len(counts) in (5, 6) and counts[0] == 1, 'invalid calibration levels')
        layers = [[] for _ in counts]
        for row in fixture['placements']:
            need(len(row) == 7 and type(row[0]) is int and 0 <= row[0] < len(layers),
                 'invalid calibration placement')
            layers[row[0]].append(self.pose(row[1:]))
        need([len(layer) for layer in layers] == counts and layers[0] == [c.IDENTITY],
             'invalid calibration counts or root')
        all_poses = tuple(p for layer in layers for p in layer)
        need(len(set(all_poses)) == len(all_poses), 'duplicate positive copy')
        self.g.union(all_poses)
        occupied, prefix, meshes, previous_vs = set(), [], [], None
        for j, layer in enumerate(layers):
            if j:
                need(all(previous_vs & {v for f in self.g.footprint(p) for v in c.vertices(f)}
                         for p in layer), 'missing previous-corona contact')
            previous_vs = {v for p in layer for f in self.g.footprint(p) for v in c.vertices(f)}
            prefix.extend(layer)
            occupied.update(self.g.union(layer))
            mesh, vs = c.mesh(occupied)
            meshes.append(mesh['faces'])
            if j+1 < len(layers):
                nxt = occupied | self.g.union(layers[j+1])
                need(all(set(c.star(v)) <= nxt for v in vs), 'positive prefix not strictly surrounded')
            if j == len(layers)-2:
                need(not any(self.bad(p, q) for p, q in combinations(prefix, 2)),
                     'NO-ONE premise contradicts known positive')
            if j == len(layers)-3:
                full = set(prefix)
                for motif in motifs:
                    fixed = self.fixed(motif['fixed_poses'])
                    transfers = {c.compose(a, c.inverse(p)) for a in full for p in fixed}
                    need(not any({c.compose(t, p) for p in fixed} <= full for t in transfers),
                         'NO-TWO motif contradicts known positive')
            self.guard()
        return {'id': fixture['id'], 'coronas': len(layers)-1, 'counts': counts,
                'prefix_face_counts': meshes, 'strict_containment_and_disc_meshes': True,
                'primitive_and_two_future_calibrations_passed': True}

    def run(self):
        caps = self.data['primitive_no_one_lemmas']
        need(len(caps) == len({digest(cap) for cap in caps}) == 26, 'wrong primitive library')
        primitive = [self.primitive(cap) for cap in caps]
        motifs = self.data['motifs']
        need([m['id'] for m in motifs] == ['pair-r0', 'pair-r1', 'pair-r2',
                                         'triple-r0', 'triple-r1', 'triple-r2'], 'wrong motif family')
        return {'input_schema': self.data['schema'], 'prototype': self.mesh,
                'prototype_boundary_angle_counts_degrees': dict(sorted(Counter(
                    60*sum(f in self.fs for f in c.star(v)) for v in self.g.vs
                    if sum(f in self.fs for f in c.star(v)) < 6).items())),
                'primitive_lemmas': primitive, 'motifs': [self.motif(m) for m in motifs],
                'positive_calibrations': [self.positive(p, motifs)
                                          for p in self.data['positive_calibrations']],
                'all_six_local_obstructions_verified': True,
                'global_finite_upper_proved': False, 'peer_or_formal_audit_claimed': False}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, default=BASE/'input.json')
    ap.add_argument('--expected', type=Path)
    ap.add_argument('--controls', action='store_true')
    args = ap.parse_args()
    start = time.monotonic()
    data = json.loads(args.input.read_text())
    checker = Checker(data, start+42)
    report = checker.run()
    report['input_sha256'] = hashlib.sha256(args.input.read_bytes()).hexdigest()
    if args.controls:
        controls = []
        for label in ('non_D6_pose', 'duplicate_fixed_copy', 'missing_positive_copy', 'shortened_future_license'):
            bad = copy.deepcopy(data)
            if label == 'non_D6_pose':
                bad['primitive_no_one_lemmas'][0]['fixed_poses'][0][0] = 2
            elif label == 'duplicate_fixed_copy':
                bad['primitive_no_one_lemmas'][0]['fixed_poses'][1] = bad['primitive_no_one_lemmas'][0]['fixed_poses'][0]
            elif label == 'missing_positive_copy':
                bad['positive_calibrations'][0]['placements'].pop(1)
            else:
                bad['motifs'][0]['future_surrounds_ruled_out'] = 1
            try:
                Checker(bad, start+42).run()
            except ValueError as error:
                controls.append({'kind': label, 'rejected': True, 'reason': str(error)})
            else:
                raise ValueError('malformed input accepted: '+label)
        report['negative_controls'] = controls
    # Compare JSON-normalized semantics (integer dictionary keys become strings).
    report = json.loads(json.dumps(report))
    if args.expected:
        need(report == json.loads(args.expected.read_text()), 'deterministic expected output differs')
    print(json.dumps({'result': report, 'seconds': round(time.monotonic()-start, 3),
                      'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, indent=2))


if __name__ == '__main__':
    main()
