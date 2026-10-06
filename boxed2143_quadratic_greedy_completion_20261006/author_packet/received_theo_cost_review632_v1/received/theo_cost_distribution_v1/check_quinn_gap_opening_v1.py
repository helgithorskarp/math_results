#!/usr/bin/env python3
"""Independent whole requested gap-opening check, without author imports."""

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import resource
import time


def occurrences(p):
    answer = []
    for i, j, k, ell in itertools.combinations(range(len(p)), 4):
        if p[j] < p[i] < p[ell] < p[k]:
            if all(x in (i, j, k, ell) or not p[j] < p[x] < p[k]
                   for x in range(i + 1, ell)):
                answer.append((i, j, k, ell))
    return answer


def literal_new_maximum_gaps(p):
    """Complete literal new-box test, with the new max as selected third point."""
    result = []
    for gap in range(len(p) + 1):
        q = p[:gap] + (len(p) + 1,) + p[gap:]
        bad = False
        for i, j in itertools.combinations(range(gap), 2):
            if q[j] >= q[i]:
                continue
            for ell in range(gap + 1, len(q)):
                if q[i] >= q[ell]:
                    continue
                if all(x in (i, j, gap, ell) or q[x] <= q[j]
                       for x in range(i + 1, ell)):
                    bad = True
                    break
            if bad:
                break
        if not bad:
            result.append(gap)
    return tuple(result)


def blocking_triples(p):
    result = []
    for j in range(len(p)):
        left = next((i for i in range(j - 1, -1, -1) if p[i] > p[j]), None)
        right = next((i for i in range(j + 1, len(p)) if p[i] > p[j]), None)
        if left is not None and right is not None and p[left] < p[right]:
            result.append((left, j, right))
    return result


def geometric_gaps(p):
    excluded = {gap for _, j, right in blocking_triples(p)
                for gap in range(j + 1, right + 1)}
    return tuple(g for g in range(len(p) + 1) if g not in excluded)


def normalized(obj):
    return json.loads(json.dumps(obj))


def complete(source, compact_certificate=False):
    assert sorted(source) == list(range(1, len(source) + 1))
    positions = {v: i for i, v in enumerate(source)}
    p = ()
    tags = []
    costs, trace, steps = [], [], []
    stream = hashlib.sha256()
    legal_gap_counts = []
    for rank in range(1, len(source) + 1):
        targets = [i for i, tag in enumerate(tags)
                   if tag is not None and positions[tag] > positions[rank]]
        desired = min(targets) if targets else len(p)
        repair_count = 0
        initial_distance = None
        while True:
            legal = literal_new_maximum_gaps(p)
            assert legal == geometric_gaps(p)
            legal_gap_counts.append(len(legal))
            if desired in legal:
                p = p[:desired] + (len(p) + 1,) + p[desired:]
                tags.insert(desired, rank)
                child_boxes = occurrences(p)
                assert not child_boxes
                steps.append({'kind': 'source', 'source_rank': rank,
                              'insertion_gap': desired, 'after': p,
                              'after_source_identities': list(tags),
                              'literal_child_occurrences': child_boxes})
                costs.append(repair_count)
                stream.update((json.dumps([p, tags], separators=(',', ':')) + '\n').encode())
                break
            earlier = [g for g in legal if g < desired]
            assert earlier
            k = max(earlier)
            before_distance = desired - k
            if initial_distance is None:
                initial_distance = before_distance
            witness = [{'left': a, 'minimum': b, 'right': c}
                       for a, b, c in blocking_triples(p)
                       if b == k and b < k + 1 <= c]
            assert witness and k + 1 not in legal
            row = {'kind': 'auxiliary', 'source_rank': rank, 'before': p,
                   'before_source_identities': list(tags),
                   'desired_gap_before': desired, 'rightmost_legal_before': k,
                   'followed_source_identity': tags[k],
                   'first_forbidden_gap_witness': witness}
            p = p[:k] + (len(p) + 1,) + p[k:]
            tags.insert(k, None)
            desired += 1
            repair_count += 1
            child_legal = literal_new_maximum_gaps(p)
            assert child_legal == geometric_gaps(p)
            assert k + 1 in child_legal and k + 2 in child_legal
            after_distance = desired - max(g for g in child_legal if g <= desired)
            assert after_distance <= before_distance - 1
            assert repair_count <= initial_distance
            child_boxes = occurrences(p)
            assert not child_boxes
            row.update({'after': p, 'after_source_identities': list(tags),
                        'desired_gap_after': desired, 'distance_after': after_distance,
                        'literal_child_occurrences': child_boxes})
            steps.append(row)
            if len(source) <= 8:
                trace.append({'source_rank': rank, 'auxiliary_gap': k,
                              'tracked_gap': desired, 'distance_before': before_distance,
                              'distance_after': after_distance})
            stream.update((json.dumps([p, tags], separators=(',', ':')) + '\n').encode())
        assert len(p) <= (1 << rank) - 1
    assert tuple(tag for tag in tags if tag is not None) == source
    kept = [v for v, tag in zip(p, tags) if tag is not None]
    ranks = {v: i + 1 for i, v in enumerate(sorted(kept))}
    assert tuple(ranks[v] for v in kept) == source
    result = {'input': source, 'output_length': len(p),
              'auxiliaries': len(p) - len(source), 'stage_costs': costs,
              'trace_sha256': stream.hexdigest()}
    if len(source) <= 8:
        result.update({'output': p, 'source_identities': tags, 'auxiliary_trace': trace})
    if compact_certificate:
        result.update({'output': p, 'source_identities': tags,
                       'source_positions': [i for i, tag in enumerate(tags) if tag is not None],
                       'complete_steps': steps,
                       'old_auxiliary_guarded_again': [i for i, step in enumerate(steps)
                           if step['kind'] == 'auxiliary' and step['followed_source_identity'] is None],
                       'literal_legal_gap_counts_every_step': legal_gap_counts})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve().parent
    parser.add_argument('--packet', type=Path, default=here / 'received/quinn_gap_opening_v1')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), 'Preserve prior output'
    began = time.perf_counter()
    raw = (args.packet / 'MANIFEST.json').read_bytes()
    manifest = json.loads(raw)
    for name, rec in manifest['files'].items():
        data = (args.packet / name).read_bytes()
        assert len(data) == rec['bytes']
        assert hashlib.sha256(data).hexdigest() == rec['sha256']
    for name, digest in manifest['dependencies'].items():
        assert hashlib.sha256((args.packet / 'dependencies' / name).read_bytes()).hexdigest() == digest
    diagnostics = json.loads((args.packet / 'gap_opening_probe_v1.json').read_text())
    certificate = json.loads((args.packet / 'gap_opening_review_certificate_v1.json').read_text())
    two_gap_stream = hashlib.sha256()
    parent_count = child_count = literal_test_count = 0
    for n in range(7):
        for p in itertools.permutations(range(1, n + 1)):
            if occurrences(p):
                continue
            parent_count += 1
            legal = literal_new_maximum_gaps(p)
            assert legal == geometric_gaps(p)
            for g in legal:
                q = p[:g] + (n + 1,) + p[g:]
                assert not occurrences(q)
                lg = literal_new_maximum_gaps(q)
                assert lg == geometric_gaps(q)
                assert g + 1 in lg and (g == n or g + 2 in lg)
                for k in range(len(q) + 1):
                    child = q[:k] + (len(q) + 1,) + q[k:]
                    assert (k in lg) == (not occurrences(child))
                    literal_test_count += 1
                child_count += 1
                two_gap_stream.update((json.dumps([p, g, q, lg], separators=(',', ':')) + '\n').encode())
    two_gap = {'max_parent': 6, 'parents': parent_count, 'legal_children': child_count,
               'stream_sha256': two_gap_stream.hexdigest()}
    assert two_gap == diagnostics['two_gap_literal_control'] == certificate['two_gap_literal_control']

    controls = []
    for m in range(1, 7):
        histogram, worst, total = {}, None, 0
        digest = hashlib.sha256()
        for p in itertools.permutations(range(1, m + 1)):
            result = complete(p)
            n = result['output_length']
            histogram[str(n)] = histogram.get(str(n), 0) + 1
            total += n
            if worst is None or n > worst['output_length']:
                worst = result
            digest.update((json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n').encode())
        row = {'m': m, 'input_count': math.factorial(m),
               'output_length_histogram': histogram, 'output_length_sum': total,
               'worst_input': worst, 'input_stream_sha256': digest.hexdigest()}
        controls.append(row)
    assert normalized(controls) == diagnostics['complete_small_inputs'] == certificate['complete_small_inputs']
    source = tuple(json.loads((args.packet / 'gap_opening_counterexample27_input_v1.json').read_text())['input'])
    fixture = complete(source, compact_certificate=True)
    fixture_fields = ('input', 'output', 'output_length', 'source_identities', 'source_positions',
                      'stage_costs', 'auxiliaries', 'complete_steps', 'old_auxiliary_guarded_again')
    for field in fixture_fields:
        assert normalized(fixture[field]) == certificate[field], field
    assert fixture['output_length'] == 52 and fixture['auxiliaries'] == 25
    assert certificate['coefficient2_bound'] == 2 * len(source) - 3 == 51
    assert certificate['bound_refuted'] and not certificate['global_minimality_claim']
    guarded_ranks = [fixture['complete_steps'][i]['source_rank']
                     for i in fixture['old_auxiliary_guarded_again']]
    assert guarded_ranks == [16, 23]
    report = {'author': 'literature-researcher-3', 'checker': 'literature-researcher-4',
              'decision_message_id': 410, 'full_target_solved': False,
              'packet_manifest_sha256': hashlib.sha256(raw).hexdigest(),
              'independent_algorithm': 'literal insertion third-point triples and full quadruples; direct nearest-greater scans; own source order and greedy simulation',
              'two_gap_literal_control': two_gap,
              'additional_literal_child_gap_tests': literal_test_count,
              'complete_small_inputs': controls, 'fixture': fixture,
              'guarded_again_source_ranks': guarded_ranks,
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'python': platform.python_version(), 'seconds': time.perf_counter() - began,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ('complete_small_inputs', 'fixture')}, indent=2))


if __name__ == '__main__':
    main()
