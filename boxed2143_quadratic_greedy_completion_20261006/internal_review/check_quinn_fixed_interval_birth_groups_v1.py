#!/usr/bin/env python3
"""Independent ENTIRE718 replay, using ONLY Theo's already checked648 helper.

Nearest-greater snapshots use two monotone stacks and boundary prefix sums.
Charge identities use an explicit pointer-stack Cartesian tree walk. Records
are generated before comparison with either author certificate. One execution
checks both original encodings on exactly their common preregistered domain.
"""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import permutations
import json
from pathlib import Path
import platform
import resource
from time import monotonic, perf_counter

HERE = Path(__file__).resolve().parent
HELPER = HERE / 'check_quinn_repair_path_cost_v3.py'
HELPER_SHA = '15eec89d395d135b97841f355df947cc000692df59c3863e92c215a854eb3adc'


class Mismatch(Exception):
    pass


def check(ok, context):
    if not ok:
        raise Mismatch(context)


def fp(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def canon(record, version):
    if version == 2:
        record = json.loads(json.dumps(record))
    return (json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n').encode()


def snapshot(p, tags):
    """Two independent nearest-greater sweeps; no author snapshot imports."""
    n = len(p)
    left, right = [-1] * n, [n] * n
    for indices, endpoints in ((range(n), left), (range(n - 1, -1, -1), right)):
        stack = []
        for j in indices:
            while stack and p[stack[-1]] < p[j]:
                stack.pop()
            if stack:
                endpoints[j] = stack[-1]
            stack.append(j)
    weights = [int(t is not None) for t in tags] + [1]
    prefix = [0]
    for w in weights:
        prefix.append(prefix[-1] + w)
    points = {}
    for j, identity in enumerate(p):
        ell, r = left[j], right[j]
        points[identity] = {
            'position': j, 'left': ell, 'right': r,
            'left_id': p[ell] if ell >= 0 else None,
            'right_id': p[r] if r < n else None,
            'K': prefix[r + 1] - prefix[j + 1],
            'eligible': ell >= 0 and r < n and p[ell] < p[r],
            'original': tags[j] is not None,
        }
    return points, weights


def path_labels(p, gap):
    """Linear Cartesian construction, then external-leaf pointer walk."""
    left, right, stack = [None] * len(p), [None] * len(p), []
    for j, value in enumerate(p):
        detached = None
        while stack and p[stack[-1]] < value:
            detached = stack.pop()
        if stack:
            right[stack[-1]] = j
        left[j] = detached
        stack.append(j)
    node = stack[0] if stack else None
    directions, nodes = [], []
    while node is not None:
        nodes.append(p[node])
        move_left = gap <= node
        directions.append('L' if move_left else 'R')
        node = left[node] if move_left else right[node]
    word = ''.join(directions)
    labels, seen_left = [], False
    for i, letter in enumerate(directions[:-1]):
        if letter == 'L':
            seen_left = True
        if seen_left and letter == 'R' and directions[i + 1] == 'R':
            labels.append(nodes[i + 1])
    return word, labels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--output-directory', type=Path, required=True)
    args = parser.parse_args()
    check(fp(HELPER)['sha256'] == HELPER_SHA, 'accepted helper pin')
    spec = importlib.util.spec_from_file_location('theo_checked648', HELPER)
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    packet = args.packet.resolve()
    source = packet / 'workday7_fixed_interval_v1'
    check(not args.output_directory.exists(), 'fresh output required')
    out = args.output_directory
    out.mkdir(parents=True)
    began, deadline = perf_counter(), monotonic() + 60
    input_reports = {v: json.loads((source / f'controls_v{v}/report_v1.json').read_text()) for v in (1, 2)}
    kinds = ('insertions', 'episodes', 'conditional', 'family', 'birth_groups')
    streams = {v: {k: sha256() for k in kinds if v == 2 or k != 'birth_groups'} for v in (1, 2)}
    counts = {1: Counter(), 2: Counter()}
    output_paths = {v: out / f'author_encoding_v{v}_records.ndjson' for v in (1, 2)}
    outputs = {v: output_paths[v].open('wb') for v in (1, 2)}
    inputs = {v: (source / f'controls_v{v}/all_records_v1.ndjson').open('rb') for v in (1, 2)}
    lines = Counter()
    diagnostic = {'group_states': 0, 'zero_mass_old_points': 0, 'maximum_points': 0,
                  'original_steps': 0, 'auxiliary_steps': 0}

    def emit(kind, record):
        check(monotonic() < deadline, {'failure': '60s cap', 'kind': kind})
        for version in (1, 2):
            if kind == 'birth_groups' and version == 1:
                continue
            streams[version][kind].update(canon(record, version))
            encoded = canon({'kind': kind, 'record': record}, version)
            outputs[version].write(encoded)
            actual = inputs[version].readline()
            lines[version] += 1
            check(encoded == actual, {'failure': 'independent certificate record mismatch',
                  'version': version, 'line': lines[version], 'kind': kind,
                  'context': record.get('context'), 'generated_sha256': sha256(encoded).hexdigest(),
                  'expected_sha256': sha256(actual).hexdigest()})
            counts[version][kind] += 1

    def single(p, tags, gap, tag, context):
        old, weights = snapshot(p, tags)
        z = int(tag is not None)
        check(not z or weights[gap] == 1, ('unit source boundary', context))
        child = h.inserted(p, gap)
        new_tags = tags[:gap] + (tag,) + tags[gap:]
        check(len(child) < 80, ('80point cap', context))
        diagnostic['maximum_points'] = max(diagnostic['maximum_points'], len(child))
        diagnostic['original_steps' if z else 'auxiliary_steps'] += 1
        full_boxes = h.boxes(child)
        check(not full_boxes, ('actual literal child', context, full_boxes))
        after, _ = snapshot(child, new_tags)
        rules = []
        for identity in p:
            s, t = old[identity], after[identity]
            j, ell, r = s['position'], s['left'], s['right']
            if j < gap <= r:
                mass, eligible, kind = sum(weights[j + 1:gap]) + z, ell >= 0, 'right fence'
                check(t['right_id'] == len(child) and t['left_id'] == s['left_id'],
                      ('new right endpoint identity', context, identity))
            elif ell < gap <= j:
                mass, eligible, kind = s['K'], False, 'left fence'
                check(t['left_id'] == len(child) and t['right_id'] == s['right_id'],
                      ('new left endpoint identity', context, identity))
            else:
                mass, eligible, kind = s['K'], s['eligible'], 'unchanged fences'
                check((t['left_id'], t['right_id']) == (s['left_id'], s['right_id']),
                      ('retained endpoint identity', context, identity))
            check((t['K'], t['eligible']) == (mass, eligible), ('exact insertion rule', context, identity))
            check(mass <= s['K'], ('actual insertion monotonicity', context, identity))
            if s['K'] == 0:
                diagnostic['zero_mass_old_points'] += 1
                check(t['K'] == 0 and t['right_id'] is not None and not after[t['right_id']]['original'],
                      ('permanent zero mass/auxiliary fence', context, identity))
            for v in (1, 2):
                counts[v]['existing_point_insertions'] += 1
            rules.append([identity, kind, mass, eligible])
        birth = after[len(child)]
        check(birth['K'] == sum(weights[gap:]) and birth['left_id'] is None
              and birth['right_id'] is None and not birth['eligible'], ('birth mass', context))
        emit('insertions', {'context': context, 'parent': p, 'tags': tags, 'cut': gap, 'new_tag': tag,
                           'old_points': old, 'rules': rules, 'child': child, 'child_tags': new_tags,
                           'new_points': after, 'full_literal_child_boxes': full_boxes})
        return child, new_tags

    def group_check(p, tags, groups, context):
        check(set(groups) == {v for v, tag in zip(p, tags) if tag is None}, ('all auxiliary groups', context))
        state, _ = snapshot(p, tags)
        members = {}
        for value in p:
            if value in groups:
                members.setdefault(groups[value], []).append(value)
        for group, values in members.items():
            for i, a in enumerate(values):
                for b in values[i + 1:]:
                    check(a < b and state[a]['right'] <= state[b]['position'],
                          ('persistent interval separation', context, group, a, b))
        counts[2]['group_state_controls'] += 1
        diagnostic['group_states'] += 1

    def episode(parent, old_tags, selected, rank, context, old_groups):
        initial, weights = snapshot(parent, old_tags)
        initial_path, initial_labels = path_labels(parent, selected)
        covered = {identity for identity, s in initial.items()
                   if s['eligible'] and s['position'] < selected <= s['right']}
        check(set(initial_labels) == covered and len(initial_labels) == len(covered),
              ('initial pair-to-minimum identities', context))
        p, tags, gap, groups = parent, old_tags, selected, dict(old_groups)
        charged, births, trace = [], [], []
        check(set(old_groups) == {v for v, t in zip(p, tags) if t is None}, ('complete initial groups', context))
        while gap not in h.legal_gaps(p):
            path, labels = path_labels(p, gap)
            check(labels == initial_labels[len(charged):], ('untouched suffix minimum identities', context, path))
            label = labels[0]
            check(label in covered and label not in charged, ('pre-episode distinct label', context, label))
            cut = max(x for x in h.legal_gaps(p) if x < gap)
            charged.append(label)
            p, tags = single(p, tags, cut, None, [context, 'auxiliary', len(charged)])
            births.append(len(p))
            groups[len(p)] = rank
            group_check(p, tags, groups, [context, 'after auxiliary'])
            gap += 1
            trace.append({'charged_identity': label, 'cut': cut, 'desired_gap_after': gap, 'child': p, 'tags': tags})
        p, tags = single(p, tags, gap, rank, [context, 'original'])
        group_check(p, tags, groups, [context, 'after original'])
        check(charged == initial_labels and not set(charged).intersection(births), ('complete original labels', context))
        final, _ = snapshot(p, tags)
        aux_mass = sum(final[value]['K'] for value in births)
        original_mass = final[len(p)]['K']
        if births:
            check(all(b['cut'] >= a['cut'] + 2 for a, b in zip(trace, trace[1:])), ('ordered cuts', context))
            check(all(final[value]['left_id'] is None and not final[value]['eligible'] for value in births),
                  ('new auxiliary left endpoint', context))
            check(aux_mass == sum(weights[trace[0]['cut']:selected]) + 1, ('auxiliary mass partition', context))
            check(aux_mass + original_mass == sum(weights[trace[0]['cut']:]) + 1, ('all birth mass partition', context))
        else:
            check(aux_mass == 0, ('no auxiliary mass', context))
        check(original_mass == sum(weights[selected:]) and not final[len(p)]['eligible'], ('original birth mass', context))
        check(aux_mass + original_mass <= rank + 1, ('all birth mass cap', context))
        charged_groups = [old_groups[value] for value in charged if not initial[value]['original']]
        n, G = rank - 1, len(set(old_groups.values()))
        check(len(set(charged_groups)) == len(charged_groups), ('distinct charged groups', context))
        check(G <= n and len(charged) <= n + G <= 2 * n, ('quadratic episode cap', context))
        emit('birth_groups', {'context': context, 'old_groups': old_groups, 'new_groups': groups,
                             'new_auxiliaries': births, 'auxiliary_birth_mass': aux_mass,
                             'original_birth_mass': original_mass, 'newborn_mass_sum': aux_mass + original_mass,
                             'charged_auxiliary_groups': charged_groups, 'actual_cost': len(charged),
                             'n': n, 'old_group_count': G})
        caps = []
        for value in parent:
            s = initial[value]
            inside = s['position'] < selected <= s['right']
            ordinal = sum(weights[s['position'] + 1:selected + 1]) if inside else None
            cap = ordinal if inside else s['K']
            check(final[value]['K'] <= cap, ('episode ordinal cap', context, value))
            caps.append([value, ordinal, cap, final[value]['K']])
        emit('episodes', {'context': context, 'parent': parent, 'tags': old_tags, 'original_gap': selected,
                          'source_rank': rank, 'initial_path': initial_path, 'initial_charge_labels': initial_labels,
                          'actual_charge_labels': charged, 'auxiliary_births': births, 'trace': trace,
                          'final_original_gap': gap, 'child': p, 'child_tags': tags, 'point_caps': caps})
        return p, tags, charged, groups

    def complete(source_word, context):
        positions = {value: i for i, value in enumerate(source_word)}
        p, tags, groups = (), (), {}
        for rank in range(1, len(source_word) + 1):
            successors = [tag for tag in tags if tag is not None and positions[tag] > positions[rank]]
            gap = tags.index(successors[0]) if successors else len(p)
            p, tags, _, groups = episode(p, tags, gap, rank, [context, 'history', rank], groups)
        check(tuple(tag for tag in tags if tag is not None) == source_word, ('original source decoding', source_word))
        check(len(p) <= len(source_word) ** 2, ('quadratic completion length', source_word))
        return p, tags, groups

    def next_children(source_word, p, tags, groups, context):
        old, _ = snapshot(p, tags)
        sums, children, aux = dict.fromkeys(p, 0), [], 0
        for hgap, gap in enumerate(h.original_gaps(tags)):
            child, child_tags, labels, _ = episode(p, tags, gap, len(source_word) + 1, [context, 'next', hgap], groups)
            state, _ = snapshot(child, child_tags)
            for identity in p:
                sums[identity] += state[identity]['K']
            children.append((child, child_tags, labels))
            aux += len(labels)
        inequalities = []
        for identity in p:
            mass = old[identity]['K']
            bound = (len(source_word) + 1) * mass - mass * (mass - 1) // 2
            check(sums[identity] <= bound, ('complete conditional drift', context, identity))
            inequalities.append([identity, mass, sums[identity], bound])
        emit('conditional', {'context': context, 'source': source_word, 'parent': p, 'tags': tags,
                             'inequalities': inequalities, 'next_originals': len(children), 'next_auxiliaries': aux})
        return children, aux

    rows, family_rows, failure = [], [], None
    try:
        for n in range(6):
            population = children_count = auxiliaries = 0
            for source_word in permutations(range(1, n + 1)):
                context = ['complete-source', source_word]
                p, tags, groups = complete(source_word, context)
                children, aux = next_children(source_word, p, tags, groups, context)
                population += 1
                children_count += len(children)
                auxiliaries += aux
            rows.append({'n': n, 'complete_sources': population, 'next_original_children': children_count,
                         'next_auxiliary_children': auxiliaries})
        for n in range(6, 13):
            source_word = (5, 2) + tuple(range(n, 5, -1)) + (1, 4, 3)
            context = ['directed-family', n]
            p, tags, groups = complete(source_word, context)
            expected = (6, 2) + tuple(range(8, 2 * n - 5, 2)) + (4,) + tuple(range(2 * n - 5, 6, -2)) + (1, 5, 3)
            expected_tags = (5, 2) + (None,) * (n - 5) + tuple(range(n, 5, -1)) + (1, 4, 3)
            check((p, tags) == (expected, expected_tags), ('recurrent output', n))
            old, _ = snapshot(p, tags)
            check(old[4]['K'] == 1 and old[4]['eligible'] and not old[4]['original'], ('eligible auxiliary4', n))
            children, aux = next_children(source_word, p, tags, groups, context)
            distinguished, next_tags, labels = children[2]
            after, _ = snapshot(distinguished, next_tags)
            nn = n + 1
            expected_next = (6, 2) + tuple(range(8, 2 * nn - 5, 2)) + (4,) + tuple(range(2 * nn - 5, 6, -2)) + (1, 5, 3)
            check(distinguished == expected_next and labels == [4] and after[4]['K'] == 1 and after[4]['eligible'],
                  ('distinguished recurrent charge', n))
            row = {'n': n, 'source': source_word, 'word': p, 'tags': tags, 'auxiliaries': len(p) - n,
                   'old_auxiliary': old[4], 'distinguished_next_word': distinguished, 'distinguished_next_tags': next_tags,
                   'charge_labels': labels, 'final_old_auxiliary': after[4], 'next_original_children': len(children),
                   'next_auxiliary_children': aux}
            family_rows.append(row)
            emit('family', row)
        for v in (1, 2):
            check(inputs[v].read() == b'', ('unconsumed author records', v))
    except (Mismatch, RuntimeError) as error:
        failure = repr(error)
    finally:
        for f in (*outputs.values(), *inputs.values()):
            f.close()

    alignment = {}
    if failure is None:
        try:
            for v in (1, 2):
                original = input_reports[v]
                proof_name = f'FIXED_INTERVAL_TRANSPORT_AND_REPEAT_CHARGES_V{1 if v == 1 else 3}.md'
                source_shas = {rel: fp(packet / rel)['sha256'] for rel in
                               (f'workday7_fixed_interval_v1/fixed_interval_controls_v{v}.py',
                                f'workday7_fixed_interval_v1/{proof_name}', 'kernel.py', 'verify_kernel.py')}
                excluded = ('all-birth population estimate, new independent check, larger permutation census, novelty, full410'
                            if v == 1 else 'useful little-o(m log m) population estimate, new independent check, complete S6 parent-with-every-next-gap census, novelty, full410')
                expected = {'actor': 'literature-researcher-3', 'full_target_solved': False,
                            'status': 'PASS pinned same-author finite controls; new whole uniform scope pending',
                            'first_failure': None, 'complete_source_rows': rows, 'directed_family_rows': family_rows,
                            'record_counts': dict(counts[v]), 'streams_sha256': {k: s.hexdigest() for k, s in streams[v].items()},
                            'certificate': fp(output_paths[v]), 'source_sha256': source_shas,
                            'python': platform.python_version(), 'processes': 1, 'native_threads': 1,
                            'time_cap_seconds': 60, 'point_cap': 80, 'excluded': excluded}
                documentary = ('seconds_including_certificate_before_report', 'peak_rss_kib_linux_before_final_serialization')
                check(set(original) == set(expected) | set(documentary), ('every report field accounted', v))
                check(json.loads(json.dumps(expected)) == {k: x for k, x in original.items() if k not in documentary},
                      ('all deterministic report fields', v))
                check(0 < original[documentary[0]] < 60 and original[documentary[1]] > 0, ('author runtime/RSS documentary', v))
                stdout = json.loads((source / f'controls_v{v}.stdout').read_text())
                check(stdout == {k: x for k, x in original.items() if k != 'directed_family_rows'}, ('all author stdout fields', v))
                check((source / f'controls_v{v}.stderr').read_bytes() == b'', ('author stderr', v))
                plan = json.loads((source / f'PRERUN_MANIFEST_V{v}.json').read_text())
                command = json.loads((source / f'command_v{v}.json').read_text())
                check(plan['command'] == command and command[:2] == ['python3', '-B']
                      and command[2] == f'boxed2143_quinn_20261005/workday7_fixed_interval_v1/fixed_interval_controls_v{v}.py'
                      and command[3] == '--output-directory'
                      and command[4].endswith(f'/boxed2143_quinn_20261005/workday7_fixed_interval_v1/controls_v{v}'), ('exact author command', v))
                for rel, pinned in plan['files'].items():
                    check(fp(packet / rel) == pinned, ('every author prerun file pin', v, rel))
                receipt = json.loads((source / f'execution_receipt_v{v}.json').read_text())
                check(receipt['exit_code'] == 0 and receipt['attempts'] == 1 and receipt['full_target_solved'] is False,
                      ('author attempt receipt', v))
                check(receipt.get('completed_attempts', receipt.get('completed_executions')) == 1, ('author execution count', v))
                check(receipt.get('source_bytes_unchanged', receipt.get('all_pinned_bytes_unchanged')) is True, ('author pin receipt', v))
                alignment[v] = {'every_deterministic_report_field': True, 'every_stdout_field': True,
                                'empty_stderr': True, 'every_prerun_source_pin': True, 'command': command,
                                'report_sha256': fp(source / f'controls_v{v}/report_v1.json')['sha256'],
                                'certificate': fp(output_paths[v]), 'streams_sha256': expected['streams_sha256'],
                                'record_counts': expected['record_counts'],
                                'runtime_RSS_documentary_only': {k: original[k] for k in documentary}}
        except Mismatch as error:
            failure = repr(error)
    report = {'actor': 'literature-researcher-4', 'status': 'PASS entire prescribed finite scope' if failure is None else 'STOP first failure',
              'first_failure': failure, 'author_request_message_id': 718, 'one_independent_mathematical_execution': True,
              'author_executions': 2, 'encodings_compared': [1, 2], 'all_author_record_bytes_compared': lines,
              'author_report_alignment': alignment, 'complete_source_rows': rows, 'directed_family_rows': family_rows,
              'extra_independent_controls': diagnostic, 'helper': fp(HELPER), 'checker': fp(Path(__file__)),
              'native_threads': 1, 'processes': 1, 'time_cap_seconds': 60, 'point_cap_exclusive': 80,
              'seconds_before_final_report_serialization': perf_counter() - began,
              'peak_rss_kib_linux_before_final_report_serialization': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'full_target_solved': False, 'uniform_proof_review_separate': True,
              'excluded': 'useful population bound, independent external peer review, novelty, publication, graph commitment, full410'}
    (out / 'report_v1.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: report[k] for k in ('actor', 'status', 'first_failure', 'all_author_record_bytes_compared',
                                           'extra_independent_controls', 'seconds_before_final_report_serialization',
                                           'peak_rss_kib_linux_before_final_report_serialization', 'full_target_solved')}, sort_keys=True))
    if failure is not None:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
