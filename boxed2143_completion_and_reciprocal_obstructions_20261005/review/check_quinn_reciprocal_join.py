#!/usr/bin/env python3
"""Independent string-state DP, without the author's interned tree IDs.

Legal gaps use the independently checked external-leaf automaton. New-root
splitting uses an iterative zipper of sibling substrings. No author code is
imported and no historical shape or transition cache is retained.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import sys
import time

sys.dont_write_bytecode = True
from check_quinn_boundary_automaton import descending_preorder_representative
from check_quinn_tree_state import naive_shape, legal_from_values, word
from check_quinn_reverse_join import seed, literal_join
from rectangle_checker import boxed_occurrences


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def record(path):
    data = path.read_bytes()
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def barrier():
    root = Path('/scratch/research-team-colloquium-sol61-20261005')
    for base in (root, root / 'state', root / 'state/monitor',
                 root / 'state/monitor/literature-first-20261005'):
        require(not (base / 'PAUSED.json').exists(), 'PAUSED barrier')
        if (base / 'HANDOVER.json').exists():
            require(json.loads((base / 'HANDOVER.json').read_text()).get('phase') == 'completed',
                    'Incomplete HANDOVER barrier')


def legal_mask(text):
    # A=0, B=1, C=2, rejected=3. Contexts are consumed in preorder.
    stack = [0]
    gap = mask = 0
    for character in text:
        if character == '(':
            context = stack.pop()
            stack.extend(((0, 2, 3, 3)[context], 1 if context != 3 else 3))
        elif character == '.':
            if stack.pop() != 3:
                mask |= 1 << gap
            gap += 1
    require(not stack, 'Malformed shape word')
    return mask


def zipper_children(text, gaps):
    ends, dots, opens = {}, [], []
    for position, character in enumerate(text):
        if character == '(':
            opens.append(position)
        elif character == '.':
            dots.append(position)
            ends[position] = position + 1
        else:
            ends[opens.pop()] = position + 1
    require(not opens, 'Unbalanced tree word')
    answer = {}
    for gap in gaps:
        target = dots[gap]
        start = 0
        path = []
        while text[start] != '.':
            left = start + 1
            right = ends[left]
            if target < right:
                path.append((False, text[right:ends[right]]))
                start = left
            else:
                path.append((True, text[left:right]))
                start = right
        require(start == target, 'Zipper reached wrong external leaf')
        prefix = suffix = '.'
        for came_right, sibling in reversed(path):
            if came_right:
                prefix = '(' + sibling + prefix + ')'
            else:
                suffix = '(' + suffix + sibling + ')'
        answer[gap] = '(' + prefix + suffix + ')'
    return answer


def stream(current):
    digest = hashlib.sha256()
    for (i, text), weight in sorted(current.items()):
        digest.update((str(i) + ':' + text + ':' + str(weight) + '\n').encode())
    return digest.hexdigest()


def count(alpha, beta, expected, label, state_cap=200000, seconds_cap=600):
    m = len(alpha)
    require(len(beta) == m, 'Unequal input lengths')
    gaps_a = tuple(sum(value < rank for value in alpha[:alpha.index(rank)])
                   for rank in range(1, m + 1))
    gaps_b = tuple(sum(value < rank for value in beta[:beta.index(rank)])
                   for rank in range(1, m + 1))
    current = {(0, '.'): 1}
    rows = []
    maximum = 1
    transitions = 0
    began = time.perf_counter()
    for total in range(2 * m):
        if total % 16 == 0:
            barrier()
        new, masks, edges = {}, {}, {}
        for (i, text), weight in current.items():
            j = total - i
            mask = masks.get(text)
            if mask is None:
                mask = legal_mask(text)
                masks[text] = mask
            options = []
            if i < m and (mask >> gaps_a[i]) & 1:
                options.append((i + 1, gaps_a[i]))
            if j < m and (mask >> (i + gaps_b[j])) & 1:
                options.append((i, i + gaps_b[j]))
            missing = {gap for _, gap in options if (text, gap) not in edges}
            if missing:
                for gap, child in zipper_children(text, missing).items():
                    edges[(text, gap)] = child
            for next_i, gap in options:
                key = (next_i, edges[(text, gap)])
                new[key] = new.get(key, 0) + weight
                transitions += 1
        del masks, edges
        require(len(new) <= state_cap, 'State cap: incomplete, no count')
        current = new
        maximum = max(maximum, len(current))
        row = {'ranks_inserted': total + 1, 'states': len(current),
               'state_weight_stream_sha256': stream(current)}
        require(row == expected['states_per_level'][total],
                label + ': canonical level mismatch at ' + str(total + 1))
        rows.append(row)
        require(time.perf_counter() - began <= seconds_cap, 'Time cap: incomplete, no count')
        require(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss <= 1400000,
                'Conservative memory cap: incomplete, no count')
        if m == 63 and (total + 1) % 16 == 0:
            print(json.dumps({'label': label, 'ranks_inserted': total + 1,
                              'states': len(current), 'seconds': time.perf_counter() - began}), flush=True)
    answer = sum(weight for (i, text), weight in current.items()
                 if i == m and (legal_mask(text) >> m) & 1)
    require(answer == expected['valid_rank_partitions'], label + ': final count mismatch')
    require(maximum == expected['peak_level_states'], label + ': peak state mismatch')
    require(transitions == expected['legal_transitions'], label + ': transition count mismatch')
    return {'m': m, 'alpha': alpha, 'beta': beta, 'valid_rank_partitions': answer,
            'states_per_level': rows, 'peak_level_states': maximum,
            'legal_transitions': transitions, 'state_cap': state_cap,
            'seconds_cap': seconds_cap, 'seconds': time.perf_counter() - began}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path,
                        default=Path(__file__).resolve().parent.parent / 'author/reciprocal')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    barrier()
    require(not args.output.exists(), 'Preserve an existing output; choose a new version')
    source = args.author_dir
    manifest = json.loads((source / 'MANIFEST.json').read_text())
    before = {name: record(source / name) for name in manifest['files']}
    require(before == manifest['files'], 'Frozen author bytes changed')
    began = time.perf_counter()
    shape_controls = child_controls = 0
    for n in range(8):
        for tree in {naive_shape(p) for p in itertools.permutations(range(1, n + 1))}:
            p = descending_preorder_representative(tree, n)
            text = word(tree)
            mask = legal_mask(text)
            require(tuple(g for g in range(n + 1) if (mask >> g) & 1) == legal_from_values(p),
                    'New string legality implementation fails geometry control')
            children = zipper_children(text, range(n + 1))
            for g, child in children.items():
                require(child == word(naive_shape(p[:g] + (n + 1,) + p[g:])),
                        'New string zipper fails geometry control')
                child_controls += 1
            shape_controls += 1
    controls = []
    forwards = json.loads((source / 'fixed_pair_join_counts_v3.json').read_text())['family']
    transposes = json.loads((source / 'reciprocal_join_probe_v1.json').read_text())['family']
    for orientation, rows in (('forward', forwards), ('transpose', transposes)):
        for row in rows:
            expected = row if orientation == 'forward' else row['transpose_count_certificate']
            a, b = tuple(expected['alpha']), tuple(expected['beta'])
            result = count(a, b, expected, orientation + str(len(a)))
            controls.append({'orientation': orientation, 'm': len(a),
                             'valid_rank_partitions': result['valid_rank_partitions'],
                             'all_complete_streams_and_transitions_match': True})
    literal_controls = 0
    literal = json.loads((source / 'balanced_join_reference.json').read_text())
    for row in literal['rows']:
        for pair in row['pair_counts']:
            require(literal_join(tuple(pair['alpha']), tuple(pair['beta'])) == pair['valid_rank_partitions'],
                    'Literal definition baseline mismatch')
            literal_controls += 1
    expected = json.loads((source / 'compact_join_dp_v2.json').read_text())
    a = seed(6)
    small = seed(5)
    d = len(small)
    b = tuple(1 if value == 1 else d + value for value in small) + (2 * d + 1,) + tuple(value + 1 for value in small)
    perfect = ()
    for _ in range(6):
        perfect = perfect, perfect
    require(len(a) == len(b) == 63 and not boxed_occurrences(a) and not boxed_occurrences(b),
            'Actual inputs outside avoiding domain')
    require(naive_shape(a) == naive_shape(b) == perfect, 'Actual inputs outside perfect domain')
    report = {'author': 'literature-researcher-3', 'checker': 'literature-researcher-4',
              'decision_message_id': 410, 'full_target_solved': False,
              'status': 'domain and controls checked; incomplete until both orientations finish',
              'no_author_implementation_imported': True,
              'representation': 'canonical shape strings, contextual leaf automaton, iterative sibling zipper',
              'manifest_sha256': record(source / 'MANIFEST.json')['sha256'], 'source_files': before,
              'shape_geometry_controls': shape_controls, 'child_geometry_controls': child_controls,
              'all10_prior_full_stream_controls': controls, 'literal_definition_baselines': literal_controls,
              'certificates': {}, 'R_bound': 1 << 62, 'domain_checked': True,
              'processes': 1, 'native_threads': 1}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    for label, x, y in (('N_P_Q', a, b), ('N_Q_P', b, a)):
        certificate = expected['certificates'][label]
        require(list(x) == certificate['alpha'] and list(y) == certificate['beta'], 'Input arrays mismatch')
        result = count(x, y, certificate, label)
        report['certificates'][label] = result
        report[label] = result['valid_rank_partitions']
        args.output.write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({'completed': label, 'count': result['valid_rank_partitions'],
                          'seconds': result['seconds']}), flush=True)
    report['product'] = report['N_P_Q'] * report['N_Q_P']
    require(report['product'] == expected['product'] < report['R_bound'], 'Reciprocal obstruction mismatch')
    require(before == {name: record(source / name) for name in before}, 'Frozen sources changed during replay')
    report['status'] = 'Both exact orientations and every full level stream independently reproduced; R refuted'
    report['python'] = platform.python_version()
    report['seconds'] = time.perf_counter() - began
    report['peak_rss_kib_linux'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('source_files', 'certificates', 'all10_prior_full_stream_controls')}, indent=2))


if __name__ == '__main__':
    main()
