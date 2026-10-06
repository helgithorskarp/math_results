#!/usr/bin/env python3
"""Pinned finite controls for fixed-node transport; same-author validation only."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import platform
import resource
import sys
from time import monotonic, perf_counter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kernel import blockers, insert_maximum, legal_maximum_gaps
from verify_kernel import direct_occurrences


def canonical(x):
    return (json.dumps(json.loads(json.dumps(x)), sort_keys=True, separators=(',', ':')) + '\n').encode()


def fingerprint(p):
    d = p.read_bytes()
    return {'bytes': len(d), 'sha256': sha256(d).hexdigest()}


class Failure(Exception):
    def __init__(self, context):
        self.context = context


def need(ok, context):
    if not ok:
        raise Failure(context)


def original_gaps(tags):
    return [i for i, t in enumerate(tags) if t is not None] + [len(tags)]


def snapshot(p, tags):
    weights = [int(t is not None) for t in tags] + [1]
    result = {}
    for j, value in enumerate(p):
        ell = next((i for i in range(j - 1, -1, -1) if p[i] > value), -1)
        r = next((i for i in range(j + 1, len(p)) if p[i] > value), len(p))
        result[value] = {'position': j, 'left': ell, 'right': r,
                         'left_id': None if ell < 0 else p[ell],
                         'right_id': None if r == len(p) else p[r],
                         'K': sum(weights[j + 1:r + 1]),
                         'eligible': ell >= 0 and r < len(p) and p[ell] < p[r],
                         'original': tags[j] is not None}
    return result, weights


def path_minima(p, gap):
    lo, hi, word, visited = 0, len(p), '', []
    while lo < hi:
        pivot = max(range(lo, hi), key=p.__getitem__)
        visited.append(p[pivot])
        if gap <= pivot:
            word += 'L'
            hi = pivot
        else:
            word += 'R'
            lo = pivot + 1
    minima = [visited[i + 1] for i in range(len(word) - 1)
              if word[i:i + 2] == 'RR' and 'L' in word[:i]]
    return word, minima


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-directory', required=True, type=Path)
    args = parser.parse_args()
    out = args.output_directory
    need(not out.exists(), 'fresh output directory required')
    out.mkdir(parents=True)
    began, deadline = perf_counter(), monotonic() + 60
    counts = Counter()
    streams = {k: sha256() for k in ('insertions', 'episodes', 'conditional', 'family', 'birth_groups')}
    cert_path = out / 'all_records_v1.ndjson'
    cert = cert_path.open('wb')

    def emit(kind, record):
        need(monotonic() < deadline, {'failure': '60-second cap', 'kind': kind})
        streams[kind].update(canonical(record))
        cert.write(canonical({'kind': kind, 'record': record}))
        counts[kind] += 1

    def single(p, tags, gap, new_tag, context):
        old, weights = snapshot(p, tags)
        z = int(new_tag is not None)
        need(not z or weights[gap] == 1, {'failure': 'original selected zero boundary', 'context': context})
        child = insert_maximum(p, gap)
        child_tags = tags[:gap] + (new_tag,) + tags[gap:]
        need(len(child) < 80, {'failure': '80-point cap', 'context': context})
        boxes = direct_occurrences(child)
        need(not boxes, {'failure': 'actual child literal box', 'context': context, 'child': child, 'boxes': boxes})
        new, _ = snapshot(child, child_tags)
        rules = []
        for value, s in old.items():
            j, ell, r = s['position'], s['left'], s['right']
            if j < gap <= r:
                mass = sum(weights[j + 1:gap]) + z
                eligible = ell >= 0
                kind = 'right fence'
            elif ell < gap <= j:
                mass, eligible, kind = s['K'], False, 'left fence'
            else:
                mass, eligible, kind = s['K'], s['eligible'], 'unchanged fences'
            need((new[value]['K'], new[value]['eligible']) == (mass, eligible),
                 {'failure': 'single exact mass/eligibility rule', 'context': context, 'identity': value,
                  'old': s, 'new': new[value], 'expected': [mass, eligible], 'cut': gap, 'z': z})
            need(mass <= s['K'], {'failure': 'fixed mass increases', 'context': context, 'identity': value})
            counts['existing_point_insertions'] += 1
            rules.append([value, kind, mass, eligible])
        birth = len(child)
        need(new[birth]['K'] == sum(weights[gap:]) and not new[birth]['eligible'],
             {'failure': 'birth mass/eligibility', 'context': context, 'birth': birth})
        emit('insertions', {'context': context, 'parent': p, 'tags': tags, 'cut': gap, 'new_tag': new_tag,
                           'old_points': old, 'rules': rules, 'child': child, 'child_tags': child_tags,
                           'new_points': new, 'full_literal_child_boxes': boxes})
        return child, child_tags

    def validate_groups(p, tags, groups, context):
        need(set(groups) == {v for v, t in zip(p, tags) if t is None}, {'failure': 'group tag closure', 'context': context})
        state, _ = snapshot(p, tags)
        members = {}
        for v in p:
            if v in groups:
                members.setdefault(groups[v], []).append(v)
        for group, values in members.items():
            need(all(a < b and state[a]['right'] <= state[b]['position'] for a, b in zip(values, values[1:])), {'failure': 'persistent disjoint group intervals', 'context': context, 'group': group, 'members': values})
        counts['group_state_controls'] += 1

    def episode(p, tags, gap, rank, context, prior_groups):
        initial, weights = snapshot(p, tags)
        initial_path, initial_minima = path_minima(p, gap)
        predicted = {p[b.minimum] for b in blockers(p) if b.blocks(gap)}
        need(set(initial_minima) == predicted, {'failure': 'path versus blocker labels', 'context': context})
        original_gap, parent, parent_tags = gap, p, tags
        charged, births, trace = [], [], []
        groups = dict(prior_groups)
        need(set(groups) == {v for v, t in zip(p, tags) if t is None}, {'failure': 'complete auxiliary group tags', 'context': context})
        while gap not in legal_maximum_gaps(p):
            path, minima = path_minima(p, gap)
            need(bool(minima), {'failure': 'illegal gap has no path minimum', 'context': context})
            label = minima[0]
            need(label in predicted and label not in charged,
                 {'failure': 'new or duplicate episode charge', 'context': context, 'label': label})
            cut = max(k for k in legal_maximum_gaps(p) if k < gap)
            charged.append(label)
            p, tags = single(p, tags, cut, None, [context, 'auxiliary', len(charged)])
            births.append(len(p))
            groups[len(p)] = rank
            validate_groups(p, tags, groups, [context, 'after auxiliary'])
            gap += 1
            trace.append({'charged_identity': label, 'cut': cut, 'desired_gap_after': gap,
                          'child': p, 'tags': tags})
        p, tags = single(p, tags, gap, rank, [context, 'original'])
        validate_groups(p, tags, groups, [context, 'after original'])
        need(charged == initial_minima, {'failure': 'complete ordered charge labels', 'context': context,
                                      'initial': initial_minima, 'actual': charged})
        need(not set(charged).intersection(births), {'failure': 'auxiliary charged at birth', 'context': context})
        final, _ = snapshot(p, tags)
        birth_mass = sum(final[v]['K'] for v in births)
        original_birth_mass = final[len(p)]['K']
        if births:
            need(all(trace[i + 1]['cut'] >= trace[i]['cut'] + 2 for i in range(len(trace) - 1)), {'failure': 'increasing auxiliary cuts', 'context': context})
            need(all(final[v]['left_id'] is None and not final[v]['eligible'] for v in births), {'failure': 'new auxiliary left endpoint/eligibility', 'context': context})
            need(birth_mass == sum(weights[trace[0]['cut']:original_gap]) + 1, {'failure': 'new auxiliary mass partition', 'context': context})
            need(birth_mass + original_birth_mass == sum(weights[trace[0]['cut']:]) + 1, {'failure': 'all-birth mass sum', 'context': context})
        else:
            need(birth_mass == 0, {'failure': 'mass with no auxiliary birth', 'context': context})
        need(original_birth_mass == sum(weights[original_gap:]), {'failure': 'original birth suffix mass', 'context': context})
        need(birth_mass + original_birth_mass <= rank + 1, {'failure': 'all-birth mass bound n+2', 'context': context})
        charged_groups = [prior_groups[v] for v in charged if not initial[v]['original']]
        need(len(set(charged_groups)) == len(charged_groups), {'failure': 'multiple charges to same birth group', 'context': context})
        n, G = rank - 1, len(set(prior_groups.values()))
        need(G <= n and len(charged) <= n + G <= 2 * n, {'failure': 'uniform quadratic step bound', 'context': context})
        emit('birth_groups', {'context': context, 'old_groups': prior_groups, 'new_groups': groups, 'new_auxiliaries': births, 'auxiliary_birth_mass': birth_mass, 'original_birth_mass': original_birth_mass, 'newborn_mass_sum': birth_mass + original_birth_mass, 'charged_auxiliary_groups': charged_groups, 'actual_cost': len(charged), 'n': n, 'old_group_count': G})
        caps = []
        for value, s in initial.items():
            inside = s['position'] < original_gap <= s['right']
            ordinal = sum(weights[s['position'] + 1:original_gap + 1]) if inside else None
            cap = ordinal if inside else s['K']
            need(final[value]['K'] <= cap, {'failure': 'whole-episode original ordinal cap',
                 'context': context, 'identity': value, 'initial': s, 'final': final[value], 'cap': cap})
            caps.append([value, ordinal, cap, final[value]['K']])
        emit('episodes', {'context': context, 'parent': parent, 'tags': parent_tags, 'original_gap': original_gap,
                          'source_rank': rank, 'initial_path': initial_path, 'initial_charge_labels': initial_minima,
                          'actual_charge_labels': charged, 'auxiliary_births': births, 'trace': trace,
                          'final_original_gap': gap, 'child': p, 'child_tags': tags, 'point_caps': caps})
        return p, tags, charged, groups

    def complete(source, context):
        positions = {v: i for i, v in enumerate(source)}
        p, tags, groups = (), (), {}
        for rank in range(1, len(source) + 1):
            gap = next((i for i, t in enumerate(tags)
                        if t is not None and positions[t] > positions[rank]), len(p))
            p, tags, _, groups = episode(p, tags, gap, rank, [context, 'history', rank], groups)
        need(tuple(t for t in tags if t is not None) == source, {'failure': 'original tag decoding', 'source': source})
        need(len(p) <= max(1, len(source) ** 2), {'failure': 'quadratic completed-source bound', 'context': context})
        return p, tags, groups

    def all_children(source, p, tags, groups, context):
        state, _ = snapshot(p, tags)
        sums = {v: 0 for v in p}
        child_list = []
        total_aux = 0
        for h, gap in enumerate(original_gaps(tags)):
            child, child_tags, labels, child_groups = episode(p, tags, gap, len(source) + 1, [context, 'next', h], groups)
            after, _ = snapshot(child, child_tags)
            for v in p:
                sums[v] += after[v]['K']
            total_aux += len(labels)
            child_list.append((child, child_tags, labels))
        inequalities = []
        for v, s in state.items():
            bound = (len(source) + 1) * s['K'] - s['K'] * (s['K'] - 1) // 2
            need(sums[v] <= bound, {'failure': 'complete conditional mass inequality',
                 'context': context, 'identity': v, 'sum': sums[v], 'bound': bound})
            inequalities.append([v, s['K'], sums[v], bound])
        emit('conditional', {'context': context, 'source': source, 'parent': p, 'tags': tags,
                             'inequalities': inequalities, 'next_originals': len(child_list),
                             'next_auxiliaries': total_aux})
        return child_list, total_aux

    rows, family_rows, failure = [], [], None
    try:
        for n in range(6):
            parents = children = auxiliaries = 0
            for source in permutations(range(1, n + 1)):
                p, tags, groups = complete(source, ['complete-source', source])
                child_list, aux = all_children(source, p, tags, groups, ['complete-source', source])
                parents += 1
                children += len(child_list)
                auxiliaries += aux
            rows.append({'n': n, 'complete_sources': parents, 'next_original_children': children,
                         'next_auxiliary_children': auxiliaries})
        for n in range(6, 13):
            source = (5, 2) + tuple(range(n, 5, -1)) + (1, 4, 3)
            p, tags, groups = complete(source, ['directed-family', n])
            expected = (6, 2) + tuple(range(8, 2 * n - 5, 2)) + (4,) + tuple(range(2 * n - 5, 6, -2)) + (1, 5, 3)
            expected_tags = (5, 2) + (None,) * (n - 6) + (None,) + tuple(range(n, 5, -1)) + (1, 4, 3)
            need((p, tags) == (expected, expected_tags), {'failure': 'uniform repeated family word/tags', 'n': n})
            state, _ = snapshot(p, tags)
            need(state[4]['K'] == 1 and state[4]['eligible'] and not state[4]['original'],
                 {'failure': 'persistent auxiliary K1 eligible', 'n': n, 'state': state[4]})
            children, aux = all_children(source, p, tags, groups, ['directed-family', n])
            distinguished, distinguished_tags, labels = children[2]
            need(labels == [4], {'failure': 'same old auxiliary repeat charge', 'n': n, 'labels': labels})
            final, _ = snapshot(distinguished, distinguished_tags)
            need(final[4]['K'] == 1 and final[4]['eligible'], {'failure': 'repeat auxiliary remains K1', 'n': n})
            next_n = n + 1
            expected_next = (6, 2) + tuple(range(8, 2 * next_n - 5, 2)) + (4,) + tuple(range(2 * next_n - 5, 6, -2)) + (1, 5, 3)
            need(distinguished == expected_next, {'failure': 'distinguished family continuation', 'n': n})
            row = {'n': n, 'source': source, 'word': p, 'tags': tags, 'auxiliaries': len(p) - n,
                   'old_auxiliary': state[4], 'distinguished_next_word': distinguished,
                   'distinguished_next_tags': distinguished_tags, 'charge_labels': labels,
                   'final_old_auxiliary': final[4], 'next_original_children': len(children),
                   'next_auxiliary_children': aux}
            family_rows.append(row)
            emit('family', row)
    except Failure as error:
        failure = error.context
    finally:
        cert.close()
    report = {'actor': 'literature-researcher-3', 'full_target_solved': False,
              'status': 'PASS pinned same-author finite controls; new whole uniform scope pending' if failure is None else 'STOP first failure; no completed-scope claim',
              'first_failure': failure, 'complete_source_rows': rows, 'directed_family_rows': family_rows,
              'record_counts': dict(counts), 'streams_sha256': {k: v.hexdigest() for k, v in streams.items()},
              'certificate': fingerprint(cert_path),
              'source_sha256': {str(p.relative_to(ROOT)): fingerprint(p)['sha256'] for p in
                               (Path(__file__), Path(__file__).parent / 'FIXED_INTERVAL_TRANSPORT_AND_REPEAT_CHARGES_V3.md',
                                ROOT / 'kernel.py', ROOT / 'verify_kernel.py')},
              'python': platform.python_version(), 'processes': 1, 'native_threads': 1,
              'time_cap_seconds': 60, 'point_cap': 80,
              'seconds_including_certificate_before_report': perf_counter() - began,
              'peak_rss_kib_linux_before_final_serialization': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'excluded': 'useful little-o(m log m) population estimate, new independent check, complete S6 parent-with-every-next-gap census, novelty, full410'}
    (out / 'report_v1.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'directed_family_rows'}, sort_keys=True))
    if failure is not None:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
