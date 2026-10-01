"""Three NO-THREE pair patterns, with complete 60-degree supplier censuses.

The pinned preceding public source regenerates every NO-TWO premise and the
two positive corona packings. No private certificate, solver or trace input.
The written corner-locking lemma, not the grid alone, licenses real motions.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

BASE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependency(data):
    need(data['dependency_directory'] == 'heesch_t211_two_surround_obstructions', 'unexpected dependency')
    folder = BASE.parent/data['dependency_directory']
    pins = {'check.py': 'e42023e52b2b20780e12292ebff835973c8325f1d61ac247b717411311dd67ca',
            'geometry.py': '6fdd49f7029c8a4d6b4bc4013024dda0130b9ea544559e0117b9e068fa88f4d7',
            'input.json': '3bbc8da67ff71d31fd156d542938ebe5ea327515032ec7fcd94554d83a0168cf'}
    need(data['dependency_sha256'] == pins and all(sha(folder/name) == value for name, value in pins.items()),
         'changed public NO-TWO dependency')
    sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location('t211_two_surround_public', folder/'check.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    need(Path(module.c.__file__).resolve() == (folder/'geometry.py').resolve(), 'wrong geometry module')
    return module, json.loads((folder/'input.json').read_text())


class Checker:
    def __init__(self, data, previous, legacy, deadline):
        need(data['schema'] == 'T211-three-pair-NO-THREE-v1'
             and data['all_real_motions_including_reflections'] is True
             and data['global_finite_upper_proved'] is False, 'incorrect local theorem scope')
        self.data, self.previous = data, previous
        self.reader = previous.Checker(legacy, deadline)
        self.legacy = legacy
        self.two_sources = {m['id']: m for m in legacy['motifs'][:3]}

    def motif(self, motif):
        r, old = self.reader, self.previous.c
        k = motif['r']
        need(type(k) is int and k in (0, 1, 2)
             and motif['id'] == f'NO-THREE-r{k}', 'unexpected parameter')
        need(motif['future_surrounds_ruled_out'] == 3 and motif['supplier_stage'] == 1
             and motif['supplier_later_strict_surround_stages'] == [2, 3],
             'forced supplier needs TWO later surrounds S2,S3')
        fixed = r.fixed(motif['fixed_poses'])
        expected_fixed = {(0,-1,-1,0,21,21), (1,0,0,1,9+3*k,3*k)}
        need(len(fixed) == 2 and set(fixed) == expected_fixed, 'different claimed pair')
        v = r.point(motif['forcing_vertex'])
        need(v == (18+3*k,12+3*k), 'wrong forcing point')
        occupied, gap = r.gap(fixed, v)
        need(len(gap) == 1, 'not a 60-degree gap')
        raw = r.suppliers(v, gap)
        allowed = [q for q in raw if not r.g.footprint(q) & occupied]
        q = r.pose(motif['forced_supplier'])
        need(len(raw) == 2 and allowed == [q]
             and q == (0,-1,-1,0,30+3*k,21+3*k)
             and gap <= r.g.footprint(q), 'incorrect complete unique supplier census')
        # The gap is only 60 degrees and P has no smaller positive angle.
        # Thus no second incident supplier or split edge contact can occur.
        source_id = motif['NO_TWO_source_id']
        need(source_id == f'pair-r{2-k}' and source_id in self.two_sources, 'wrong NO-TWO family')
        t = r.pose(motif['NO_TWO_transfer'])
        source = self.two_sources[source_id]
        scope = {old.compose(t, r.pose(p)) for p in source['fixed_poses']}
        need(scope == {(0,-1,-1,0,21,21), q}, 'NO-TWO transfer protects different copies')
        blocked = []
        for p in raw:
            if p == q:
                continue
            blocker = min(a for a in fixed if r.g.footprint(a) & r.g.footprint(p))
            blocked.append({'supplier': list(p), 'old_blocker': list(blocker),
                            'shared_face': list(min(r.g.footprint(blocker) & r.g.footprint(p)))})
        r.guard()
        return {'id': motif['id'], 'fixed_copies': 2, 'forcing_vertex': list(v),
                'raw_suppliers': [list(p) for p in raw], 'blocked_suppliers': blocked,
                'forced_supplier': list(q), 'NO_TWO_source_id': source_id,
                'NO_TWO_transfer': list(t), 'supplier_later_strict_surround_stages': [2,3],
                'future_surrounds_ruled_out': 3}

    def positive(self, fixture):
        r, c = self.reader, self.previous.c
        last = len(fixture['counts'])-1
        latest_protected = last-3
        prefix = {r.pose(row[1:]) for row in fixture['placements'] if row[0] <= latest_protected}
        counts = []
        for motif in self.data['motifs']:
            fixed = r.fixed(motif['fixed_poses'])
            trials = {c.compose(a, c.inverse(p)) for a in prefix for p in fixed}
            occurrences = [t for t in trials if {c.compose(t, p) for p in fixed} <= prefix]
            need(not occurrences, 'NO-THREE pattern contradicts a genuine three-future prefix')
            counts.append({'id': motif['id'], 'occurrences': len(occurrences)})
            r.guard()
        return {'fixture': fixture['id'], 'root_coronas': last,
                'protected_prefix_last_level': latest_protected,
                'protected_prefix_copies': len(prefix), 'NO_THREE_occurrences': counts}

    def run(self):
        r = self.reader
        # Recompute every one-gap premise and all THREE relevant NO-TWO
        # proofs; the prior graph's acceptance is not a proof input.
        primitive = [r.primitive(cap) for cap in self.legacy['primitive_no_one_lemmas']]
        two = [r.motif(m) for m in self.legacy['motifs'][:3]]
        need(len(two) == 3 and all(m['providers'] == 0 for m in two), 'unexpected NO-TWO source proofs')
        need([m['r'] for m in self.data['motifs']] == [0,1,2], 'incomplete or duplicate three-pair family')
        three = [self.motif(m) for m in self.data['motifs']]
        positives = [r.positive(p, self.legacy['motifs'][:3]) for p in self.legacy['positive_calibrations']]
        calibration = [self.positive(p) for p in self.legacy['positive_calibrations']]
        return {'schema': self.data['schema'], 'prototype_mesh': r.mesh,
                'replayed_primitive_NO_ONE_lemmas': len(primitive),
                'replayed_NO_TWO_sources': two, 'three_NO_THREE_pairs': three,
                'positive_corona_packings': positives, 'three_future_calibrations': calibration,
                'all_three_NO_THREE_pairs_verified': True,
                'global_finite_upper_proved': False, 'peer_or_formal_audit_claimed': False}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, default=BASE/'input.json')
    ap.add_argument('--expected', type=Path)
    ap.add_argument('--controls', action='store_true')
    args = ap.parse_args()
    start = time.monotonic()
    data = json.loads(args.input.read_text())
    previous, legacy = load_dependency(data)
    checker = Checker(data, previous, legacy, start+42)
    report = checker.run()
    report['input_sha256'] = sha(args.input)
    if args.controls:
        controls = []
        for label in ('shortened_future_license', 'wrong_NO_TWO_transfer', 'wrong_forced_supplier',
                      'wrong_forcing_vertex', 'duplicate_pair_copy', 'missing_pair_case'):
            bad = copy.deepcopy(data)
            m = bad['motifs'][0]
            if label == 'shortened_future_license':
                m['supplier_later_strict_surround_stages'] = [2]
            elif label == 'wrong_NO_TWO_transfer':
                m['NO_TWO_transfer'][4] += 1
            elif label == 'wrong_forced_supplier':
                m['forced_supplier'][4] += 1
            elif label == 'wrong_forcing_vertex':
                m['forcing_vertex'][0] += 1
            elif label == 'duplicate_pair_copy':
                m['fixed_poses'][1] = m['fixed_poses'][0]
            else:
                bad['motifs'].pop()
            try:
                mutant = Checker(bad, previous, legacy, start+42)
                if label == 'missing_pair_case':
                    need([m['r'] for m in bad['motifs']] == [0,1,2], 'incomplete or duplicate three-pair family')
                else:
                    mutant.motif(bad['motifs'][0])
            except (ValueError, KeyError) as error:
                controls.append({'malformation': label, 'rejected': True, 'reason': str(error)})
            else:
                raise ValueError(('malformed proof input accepted', label))
        report['malformed_controls'] = controls
    if args.expected:
        need(report == json.loads(args.expected.read_text()), 'deterministic result differs from expected')
    checker.reader.guard()
    print(json.dumps({'result': report, 'seconds': round(time.monotonic()-start, 3),
                      'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, indent=2))


if __name__ == '__main__':
    main()
