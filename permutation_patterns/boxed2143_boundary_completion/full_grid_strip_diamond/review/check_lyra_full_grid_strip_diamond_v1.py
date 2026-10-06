"""Independent ENTIRE finite replay of Lyra673; no author code imported/run.

Grid encoding uses the reviewer's prior arithmetic bands. Strip sets are
obtained by geometric band extraction from the full grid, and every diamond
is checked at its four actual points. The r3 population is also counted by
explicit whole-chain pairs through a four-bit intersection, independently
of the displayed 256-state weight partition. Exact standard-library code.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from check_lyra_boundary import occurrences, require
from check_lyra_adaptive_full_guard import full_encode, full_decode, selected_box

PIN = 'fddc6d0ad8775a7b25977b308fccf9fc7d218b600b0ca9044e3a839d0cbb5898'


def fingerprint(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def pin_check(packet):
    manifest = json.loads((packet / 'MANIFEST.json').read_text())
    for name, pin in manifest['files'].items():
        require(fingerprint(packet / name) == pin, 'Public source differs: ' + name)


def inverse(p):
    out = [0] * len(p)
    for i, value in enumerate(p, 1):
        out[value - 1] = i
    return tuple(out)


def comparison(p):
    positions = inverse(p)
    return tuple(int(a < b) for a, b in zip(positions, positions[1:]))


@lru_cache(None)
def literal_component(p):
    return occurrences(p)


@lru_cache(None)
def strip_data(old, guard, old_first):
    old_values = tuple(2 * x - 1 for x in old)
    guard_values = tuple(2 * x for x in guard)
    word = old_values + guard_values if old_first else guard_values + old_values
    kinds = ('old',) * len(old) + ('guard',) * len(guard) if old_first else (
        ('guard',) * len(guard) + ('old',) * len(old))
    return word, kinds, occurrences(word)


def strip_tables(avoiders):
    tables = []
    for r in range(2, 6):
        digest = hashlib.sha256()
        counts, types, first = Counter(), Counter(), {}
        for old in avoiders[r]:
            for guard in avoiders[r - 1]:
                for old_first in (False, True):
                    word, kinds, boxes = strip_data(old, guard, old_first)
                    counts[old_first] += not boxes
                    for q in boxes:
                        n = sum(kinds[k] == 'guard' for k in q)
                        require(1 <= n <= 3, 'Strip has an unexpected monochrome box')
                        types[str(old_first) + ':' + str(n)] += 1
                        key = old_first, n
                        if key not in first:
                            first[key] = {'old': old, 'guard': guard, 'old_first': old_first,
                                          'word': word, 'complete_occurrences': boxes,
                                          'first_selected_guard_count': n}
                    digest.update((json.dumps([old, guard, old_first, word, boxes],
                                              separators=(',', ':')) + '\n').encode())
        tables.append({'r': r, 'complete_component_pair_domain': len(avoiders[r]) * len(avoiders[r - 1]),
                       'old_then_guard_safe_pairs': counts[True],
                       'guard_then_old_safe_pairs': counts[False],
                       'all_mixed_occurrence_type_counts': dict(sorted(types.items())),
                       'all_first_type_representatives': [first[k] for k in sorted(first)],
                       'entire_pair_stream_sha256': digest.hexdigest()})
    return tables


def extracted_strip_sets(word, tags):
    """Extract two adjacent actual bands; no author local-tag mapper used."""
    r = sum(t[0] == 'old' and t[1] == 0 for t in tags)
    outputs = []
    for coordinate in (1, 2):
        found = set()
        for h in range(r - 1):
            for old_band in (h, h + 1):
                positions = [i for i, t in enumerate(tags)
                             if (t[0] == 'old' and t[coordinate] == old_band) or
                                (t[0] == 'guard' and t[coordinate] == h)]
                subword = tuple(word[i] for i in positions)
                for q in occurrences(subword):
                    found.add(tuple(positions[k] for k in q))
        outputs.append(found)
    return outputs


def diamonds_at_actual_points(rows, columns, guards, gcolumns, word, tags):
    r = len(rows)
    where = {t: i for i, t in enumerate(tags)}
    found = {}
    for i in range(1, r - 1):
        for j in range(r - 1):
            q = tuple(sorted(where[t] for t in
                      (('guard', i - 1, j), ('old', i, j),
                       ('old', i, j + 1), ('guard', i, j))))
            bit = comparison(rows[i])[j] and comparison(inverse(gcolumns[j]))[i - 1]
            require(selected_box(word, q) == bool(bit), 'Old-row diamond bit/actual rectangle differs')
            if bit:
                found[q] = ('old_row_guard_column', i, j)
    for i in range(r - 1):
        for j in range(1, r - 1):
            q = tuple(sorted(where[t] for t in
                      (('old', i, j), ('guard', i, j - 1),
                       ('guard', i, j), ('old', i + 1, j))))
            bit = comparison(guards[i])[j - 1] and comparison(inverse(columns[j]))[i]
            require(selected_box(word, q) == bool(bit), 'Old-column diamond bit/actual rectangle differs')
            if bit:
                require(q not in found, 'Different diamonds have the same four tags')
                found[q] = ('old_column_guard_row', i, j)
    return found


def full_record(rows, columns, guards, gcolumns, metadata):
    for p in rows + columns + guards + gcolumns:
        require(not literal_component(p), 'A full-grid component is not an avoider')
    word, tags = full_encode(rows, columns, guards, gcolumns)
    require(full_decode(word, len(rows)) == (rows, columns, guards, gcolumns), 'Arithmetic full decoder differs')
    boxes = occurrences(word)
    horizontal, vertical = extracted_strip_sets(word, tags)
    diamond = diamonds_at_actual_points(rows, columns, guards, gcolumns, word, tags)
    require(set(boxes) == horizontal | vertical | set(diamond), 'COMPLETE strip/diamond union differs')
    return {'r': len(rows), 'old_rows': rows, 'old_columns': columns, 'guard_rows': guards,
            'guard_columns': gcolumns, 'metadata': metadata, 'word': word,
            'complete_occurrences': boxes, 'horizontal_strip_occurrences': sorted(horizontal),
            'vertical_strip_occurrences': sorted(vertical),
            'orthogonal_diamond_occurrences': sorted(diamond.items())}, tags


def r3_records(avoiders):
    domain = avoiders[3]
    identity, reverse = domain[0], domain[-1]
    cores = []
    # Membership filtering of the entire 6^6 old tuple domain differs from
    # the author's additive set construction of the same prescribed family.
    for core in itertools.product(domain, repeat=6):
        one_change = min(sum(p != identity for p in core), sum(p != reverse for p in core)) <= 1
        constant_sides = len(set(core[:3])) == len(set(core[3:])) == 1
        if one_change or constant_sides:
            cores.append(core)
    records, tags_by_record = [], []
    for core in cores:
        for extra in itertools.product(avoiders[2], repeat=4):
            record, tags = full_record(core[:3], core[3:], extra[:2], extra[2:],
                                      {'control': 'all16guards/fixed_old_core'})
            records.append(record)
            tags_by_record.append(tags)
    return {'complete_specified_old_core_domain': len(cores), 'all16_guard_profiles_per_core': True,
            'full_grid_cases': len(records), 'records': records}, tags_by_record


def swap_identity(n, k):
    return tuple(k + 2 if x == k + 1 else k + 1 if x == k + 2 else x
                 for x in range(1, n + 1))


def r4_records():
    identity, guard_id = (1, 2, 3, 4), (1, 2, 3)
    records, all_tags = [], []
    for transpose in (False, True):
        axis = 'old_column_guard_row' if transpose else 'old_row_guard_column'
        for internal in range(1, 3):
            for gap in range(3):
                for first, second in itertools.product((0, 1), repeat=2):
                    rows, columns = [identity] * 4, [identity] * 4
                    guards, gcolumns = [guard_id] * 3, [guard_id] * 3
                    if transpose:
                        columns[internal] = identity if first else swap_identity(4, gap)
                        guards[gap] = guard_id if second else swap_identity(3, internal - 1)
                        target = ('old_column_guard_row', gap, internal)
                    else:
                        rows[internal] = identity if first else swap_identity(4, gap)
                        gcolumns[gap] = guard_id if second else swap_identity(3, internal - 1)
                        target = ('old_row_guard_column', internal, gap)
                    record, tags = full_record(tuple(rows), tuple(columns), tuple(guards), tuple(gcolumns),
                              {'control': 'complete_diamond_2bit_states', 'axis': axis,
                               'internal': internal, 'gap': gap, 'two_bits': (first, second)})
                    require(any(label == target for q, label in record['orthogonal_diamond_occurrences']) ==
                            bool(first and second), 'Directed diamond truth control differs')
                    records.append(record)
                    all_tags.append(tags)
    return {'all4_states_both_axes_every_interior_and_gap': True,
            'full_grid_cases': len(records), 'records': records}, all_tags


def r5_records():
    olds = ((1, 2, 3, 4, 5), (5, 4, 3, 2, 1), (2, 1, 3, 4, 5), (1, 3, 2, 4, 5))
    guards = ((1, 2, 3, 4), (4, 3, 2, 1), (2, 1, 3, 4), (1, 3, 2, 4))
    profiles = set()
    for base in (0, 1):
        plain = (olds[base],) * 10 + (guards[base],) * 8
        for coordinate in range(18):
            for replacement in olds if coordinate < 10 else guards:
                profiles.add(plain[:coordinate] + (replacement,) + plain[coordinate + 1:])
    records, all_tags = [], []
    for p in sorted(profiles):
        record, tags = full_record(p[:5], p[5:10], p[10:14], p[14:],
                  {'control': 'one_component_variation_identity_or_reverse_base/fixed4choices'})
        records.append(record)
        all_tags.append(tags)
    return {'specified_profiles': len(profiles), 'full_grid_cases': len(records),
            'records': records}, all_tags


def chain_masks(words):
    old, guard = words
    left = old[1] + (guard[0][0], guard[1][0])
    right = (guard[0][0], guard[1][0]) + old[1]
    return tuple(sum(bit << k for k, bit in enumerate(bits)) for bits in (left, right))


def chain_partition(avoiders):
    candidates = itertools.product(avoiders[3], avoiders[2], avoiders[3], avoiders[2], avoiders[3])
    raw, safe = 0, []
    for p in candidates:
        raw += 1
        old, guard = p[::2], p[1::2]
        if all(not strip_data(old[h], guard[h], True)[2] and
               not strip_data(old[h + 1], guard[h], False)[2] for h in (0, 1)):
            safe.append((old, guard))
    safe.sort()
    chains, weights = [], Counter()
    digest = hashlib.sha256()
    chain_word_pairs = []
    for old, guard in safe:
        words = tuple(map(comparison, old)), tuple(map(comparison, guard))
        weights[words] += 1
        chain_word_pairs.append(words)
        row = {'old_rows': old, 'guard_rows': guard,
               'old_comparison_words': words[0], 'guard_comparison_words': words[1]}
        chains.append(row)
        digest.update((json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n').encode())
    states = sorted(weights)
    partition_digest = hashlib.sha256()
    K, pairs = 0, 0
    for a in states:
        left = chain_masks(a)[0]
        for b in states:
            right = chain_masks(b)[1]
            compatible = not bool(left & right)
            weight = weights[a] * weights[b]
            K += weight * compatible
            pairs += 1
            partition_digest.update((json.dumps([a, b, weight, compatible],
                                        separators=(',', ':')) + '\n').encode())
    # A separate count uses EVERY actual pair of retained whole chains.
    actual_pair_count = sum(not bool(chain_masks(a)[0] & chain_masks(b)[1])
                            for a in chain_word_pairs for b in chain_word_pairs)
    require(actual_pair_count == K, 'Actual whole-chain mass differs from weighted word partition')
    result = {'r': 3, 'complete_raw_row_chain_domain': raw,
              'compatible_row_chain_count': len(chains), 'all_compatible_row_chains': chains,
              'complete_comparison_word_states': len(states), 'complete_word_pair_domain': pairs,
              'all_full_chain_word_multiplicities': [{'old_words': a[0], 'guard_words': a[1],
                                                     'chain_count': weights[a]} for a in states],
              'claimed_K3_from_exact_kernel': K, 'all_full_tuple_domain': 6 ** 6 * 2 ** 4,
              'chain_filtered_tuple_domain': len(chains) ** 2, 'a3_power6': 6 ** 6,
              'chain_stream_sha256': digest.hexdigest(), 'partition_stream_sha256': partition_digest.hexdigest(),
              'no_fitted_all_size_delta_or_complete_grid_literal_census': True}
    return result, actual_pair_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path, required=True)
    parser.add_argument('--author-report', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    packet = args.author_dir.resolve()
    out = args.output
    require(not out.exists(), 'Preserve prior evidence')
    started = time.perf_counter()
    pin_check(packet)
    avoiders = {r: tuple(p for p in itertools.permutations(range(1, r + 1)) if not literal_component(p))
                for r in range(1, 6)}
    tables = strip_tables(avoiders)
    first, tags1 = r3_records(avoiders)
    print('Independent complete prescribed r3 grid domain:', len(first['records']), flush=True)
    diamond, tags2 = r4_records()
    later, tags3 = r5_records()
    print('Independent complete r4/r5 prescribed domains:', len(diamond['records']), len(later['records']), flush=True)
    all_records = first['records'] + diamond['records'] + later['records']
    all_tags = tags1 + tags2 + tags3
    types = Counter()
    digest = hashlib.sha256()
    for row, tags in zip(all_records, all_tags):
        for q in row['complete_occurrences']:
            types[sum(tags[k][0] == 'guard' for k in q)] += 1
        digest.update((json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n').encode())
    small, actual_chain_pairs = chain_partition(avoiders)
    fields = {'strip_tables': tables, 'directed_r3': first, 'diamond_controls_r4': diamond,
              'directed_r5': later, 'total_full_literal_grid_cases': len(all_records),
              'mixed_guard_count_totals': dict(sorted(types.items())),
              'entire_full_boxset_stream_sha256': digest.hexdigest(),
              'small_chain_partition': small,
              'source_sha256': fingerprint(packet / 'full_grid_strip_diamond_probe_v1.py')['sha256'],
              'dependency_sha256': {name: fingerprint(packet / name)['sha256'] for name in
                     ('definition_checker.py', 'adaptive_full_guard_probe_v1.py', 'FULL_GRID_STRIP_DIAMOND_PLAN_V1.md')}}
    author = json.loads(args.author_report.read_text())
    normalized = json.loads(json.dumps(fields))
    for key in fields:
        require(normalized[key] == author[key], 'Some deterministic mathematical field differs: ' + key)
    require(author['author'] == 'literature-researcher-2' and author['decision_message_id'] == 410 and
            not author['full_target_solved'] and
            author['status'] == 'all_pinned_literal_characterization_controls_pass',
            'Author status/identity fields differ')
    # r2 has four whole chains and all sixteen cross-pairs compatible;
    # its strips have length3, no diamonds exist, and every literal grid
    # is checked rather than inheriting this boundary from r3.
    r2 = []
    for old in itertools.product(avoiders[2], repeat=4):
        record, tags = full_record(old[:2], old[2:], ((1,),), ((1,),), {'control': 'independent_r2_boundary'})
        require(not record['complete_occurrences'], 'r2 boundary has a box')
        r2.append(record)
    identity3 = full_record(((1, 2, 3),) * 3, ((1, 2, 3),) * 3,
                           ((1, 2),) * 2, ((1, 2),) * 2,
                           {'control': 'independent_identity_self_pair'})[0]
    require(identity3['orthogonal_diamond_occurrences'], 'Identity self-pair has no diamond')
    pin_check(packet)
    report = {'checker': 'literature-researcher-1', 'author_message_id': 673,
              'full_target_solved': False, 'uniform_K_growth_estimate_proved': False,
              'no_author_executable_imported_or_run': True, 'author_manifest_sha256': PIN,
              'public_source_manifest_sha256': fingerprint(packet / 'MANIFEST.json')['sha256'],
              'all_specified_deterministic_mathematical_fields_match': True,
              'author_schema_reproduction': normalized,
              'own_additional_r2_all16_literal_records': r2,
              'own_identity_chain_self_pair_complete_record': identity3,
              'actual_616_squared_whole_chain_pairs_evaluated': 616 ** 2,
              'actual_whole_chain_compatible_count': actual_chain_pairs,
              'complete_full_grid_literal_census_claimed_at_r3': False,
              'code': fingerprint(Path(__file__)),
              'own_imported_source_pins': {name: fingerprint(base / name) for name in
                        ('check_lyra_boundary.py', 'check_lyra_adaptive_full_guard.py')},
              'python': platform.python_version(), 'processes': 1, 'native_threads': 1,
              'seconds_before_report_serialization': time.perf_counter() - started,
              'rss_kib_before_report_serialization': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in
                     ('author_schema_reproduction', 'own_additional_r2_all16_literal_records',
                      'own_identity_chain_self_pair_complete_record')}, separators=(',', ':')), flush=True)


if __name__ == '__main__':
    main()
