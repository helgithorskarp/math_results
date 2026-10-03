"""Source-only scalar reconstruction of the complete conditional cover.

No producer, private data, prior catalogue or negative corpus is imported.
Every original ground domain and every candidate binding is reconstructed.
Ordinary arbitrary-word normalization is the separate argument in PROOF.md.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
DEAD = (4, 5, 6, 7, 9, 10)
PREFIX_SHA = '89c4715b824b7cf4cee8a5698a612f336abdf20497ed48c5132dca514486afd4'
NUMERIC_SHA = '83c79d716581cdc8f947a21d9120a001624d8179fab8935817e28326f10bb041'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def get_numeric():
    path = ROOT / 'numeric.py'
    need(hashlib.sha256(path.read_bytes()).hexdigest() == NUMERIC_SHA,
         'numeric primitive source changed before import')
    spec = importlib.util.spec_from_file_location('credited_numeric_primitives', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def inspect_early(m, prefix, entries):
    need([e['gate'] for e in entries] == [[4, 7], [4, 10], [5, 7], [6, 7], [6, 10], [7, 10], [9, 10]],
         'complete seven early negatives differ')
    records = []
    for entry in entries:
        word, w = prefix + [entry['gate']], entry['witness']
        expected = w['record']
        lo, hi = expected[:2]
        k = 13 - (lo | hi).bit_count()
        need(k in (11, 12) and w['imported_size'] == {11: 35, 12: 39}[k], 'early floor differs')
        actual, rows = m.follow(m.fresh_domain(lo, hi), word, 0)
        need(actual == expected, 'actual early whole-original history differs')
        if w['kind'] == 'DIRECT_COST':
            need(actual[4] + actual[5] + w['imported_size'] > 44, 'early direct cost insufficient')
        else:
            need(w['kind'] == 'TIGHT_FREE_CUT' and actual[4] + actual[5] + w['imported_size'] == 44,
                 'early free cut is not tight')
            q, x = w['physical_port'], w['full_Boolean_witness']
            need(type(q) is int and 0 <= q < 13 and type(x) is int and 0 <= x < 8192, 'early rank witness invalid')
            need(all(v[q] in (0, 1) and all(v[t] <= v[q] if t < q else v[q] <= v[t]
                 for t in range(13) if t != q and v[t] in (0, 1)) for v in rows), 'early whole-cube cut fails')
            bit = m.bool_word(x, word) >> q & 1
            want = int(x.bit_count() >= 13 - q)
            need(bit == w['actual_bit'] and want == w['sorted_bit'] and bit != want, 'early global rank witness fails')
        records.append([entry['gate'], actual, digest(rows)])
    return records


def reconstruct(c):
    need(c['schema'] == 'HIGH3_LOW34_ZERO_SINGLETON_TWO_BINARY_EXCLUSION_V1' and
         c['size_budget'] == 44 and c['dead_ports'] == list(DEAD), 'literal conditional certificate interface differs')
    prefix = c['literal_prefix']
    need(len(prefix) == 28 and digest(prefix) == PREFIX_SHA, 'literal Q differs')
    m = get_numeric()
    early = inspect_early(m, prefix, c['early_negative_first_gates'])
    ground, classes, assignments = {}, {}, 0
    for low_count, high_count in ((2, 0), (0, 2), (0, 3)):
        records, family_classes = [], {}
        for ports in combinations(range(13), low_count + high_count):
            mask = sum(1 << q for q in ports)
            lo, hi = (mask, 0) if low_count else (0, mask)
            record, cube = m.follow(m.fresh_domain(lo, hi), prefix, 0)
            assignments += len(cube)
            records.append(record)
            tag = (record[2], record[3])
            family_classes[tag] = max(family_classes.get(tag, 0), record[4])
        ground[str((low_count, high_count))] = sorted(records)
        classes[low_count, high_count] = family_classes
    low = {q: classes[2, 0].get((1 | (1 << q), 0)) for q in (1, 2, 3, 8)}
    need(len(classes[2, 0]) == 4 and low == {1: 7, 2: 7, 3: 7, 8: 6}, 'ordinary LOW ground differs')
    need(classes[0, 2] == {(0, 6144): 9}, 'ordinary HIGH saturation differs')
    high3 = {q: classes[0, 3].get((0, 6144 | (1 << q))) for q in DEAD}
    need(len(classes[0, 3]) == 6 and high3 == {4: 11, 5: 11, 6: 11, 7: 13, 9: 11, 10: 12},
         'entire original third-HIGH ground differs')
    parent = [m.bool_word(x, prefix) for x in range(8192)]
    need(all(all((y >> q & 1) == int(x.bit_count() >= 13 - q) for q in (0, 11, 12)) and
             min(y >> q & 1 for q in (1, 2, 3, 8)) == int(x.bit_count() >= 12) and
             max(y >> q & 1 for q in DEAD) == int(x.bit_count() >= 3)
             for x, y in enumerate(parent)), 'entire original held order statistics differ')
    reachable = sorted({sum(((y >> q) & 1) << j for j, q in enumerate(DEAD)) for y in parent})
    need(len(reachable) == 36, 'true Q projection differs')
    bad = {tuple(e['gate']) for e in c['early_negative_first_gates']}
    rejected, early_words, allowed, groups = [], [], [], {}
    for a, b in combinations(DEAD, 2):
        one = dict(high3)
        one[b] = 1 + max(one.pop(a), one[b])
        need(sum(1 << e for e in one.values()) <= 32768, 'first binary ground ceiling differs')
        for u, v in combinations(sorted(one), 2):
            after = dict(one)
            after[v] = 1 + max(after.pop(u), after[v])
            word = [[a, b], [u, v]]
            mass = sum(1 << e for e in after.values())
            if mass > 32768:
                rejected.append([word, sorted(after.items()), mass])
                continue
            allowed.append(word)
            if (a, b) in bad:
                early_words.append(word)
                continue
            freed = [q for q in DEAD if q not in after]
            need(len(freed) == 2, 'exactly-two binary support differs')
            for extra in ([], [freed]):
                f = word + extra
                local = [[DEAD.index(s), DEAD.index(t)] for s, t in f]
                key = tuple(m.bool_word(x, local) for x in reachable)
                groups.setdefault(key, []).append(f)
    need(len(allowed) == 130 and len(rejected) == 20 and len(early_words) == 54 and len(groups) == 113,
         'complete150/130/20/54/113 candidate accounting differs')
    keys = sorted(groups, key=lambda key: min((len(f), f) for f in groups[key]))
    need([f['state_id'] for f in c['functions']] == list(range(113)), 'entire113 function-ID cover differs')
    functions = []
    for i, key in enumerate(keys):
        expected = min(groups[key], key=lambda f: (len(f), f))
        supplied = c['functions'][i]
        need(supplied['shortest_word'] == expected, 'chosen actual prefix-function representative differs')
        local = [[DEAD.index(a), DEAD.index(b)] for a, b in expected]
        table = [m.bool_word(x, local) for x in range(64)]
        columns = [sum(((y >> j) & 1) << x for x, y in enumerate(table)) for j in range(6)]
        need(columns == supplied['full64_function'] and [table[x] for x in reachable] == list(key),
             'whole local function/ordered reachable binding differs')
        full = [m.bool_word(x, expected) for x in parent]
        # Independent full13 scalar embedding checks every original row;
        # other seven outputs are unchanged, never an unordered image test.
        for x, y in zip(parent, full):
            local_input = sum(((x >> q) & 1) << j for j, q in enumerate(DEAD))
            expected_local = table[local_input]
            need(sum(((y >> q) & 1) << j for j, q in enumerate(DEAD)) == expected_local and
                 all((y >> q & 1) == (x >> q & 1) for q in range(13) if q not in DEAD),
                 'entire thirteen-output candidate embedding differs')
        functions.append({'state_id': i, 'representative_word': expected,
                          'actual_reachable_ordered_outputs': list(key),
                          'entire_8192_FULL13_function_sha256': digest(full),
                          'represented_raw_words': groups[key]})
    # Pointwise idempotence proves every arbitrary word on the two freed
    # physical ports is represented; this is not a selected depth search.
    idempotence = [[x, m.bool_word(x, [[0, 1]]), m.bool_word(x, [[0, 1], [0, 1]])] for x in range(4)]
    need(all(a == b for _, a, b in idempotence), 'two-port complete semigroup differs')
    return {'literal_prefix': prefix, 'all_original_ground_records': ground,
            'numeric_ground_assignments': assignments, 'ordinary_LOW_classes': sorted(low.items()),
            'ordinary_third_HIGH_classes': sorted(high3.items()), 'initial_third_HIGH_mass': 20480,
            'third_HIGH_mass_ceiling': 32768, 'whole13_ground_Boolean_inputs': 8192,
            'early_negative_original_checks': early, 'all20_mass_rejected_binary_words': rejected,
            'all130_allowed_binary_words': allowed, 'all54_early_negative_binary_words': early_words,
            'entire_reachable_input_patterns': reachable, 'whole_prefix_function_classes': functions,
            'complete_two_port_function_semigroup': idempotence,
            'complete_conditional_two_binary_cover': True, 'full_LOW34_branch_exclusion': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'generated/cover.json')
    args = parser.parse_args()
    started = time.monotonic()
    c = json.loads((ROOT / 'certificate.json').read_text())
    math = reconstruct(c)
    result = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'COMPLETE_SOURCE_ONLY_SCALAR_CONDITIONAL_COVER',
              'mathematical': math, 'entire_mathematical_record_sha256': digest(math),
              'seconds': time.monotonic() - started, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'mathematical'}))


if __name__ == '__main__':
    main()
