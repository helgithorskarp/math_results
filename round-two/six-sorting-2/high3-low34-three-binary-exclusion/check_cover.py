"""Portable separate scalar checker for every three-binary cover binding.

The producer's packed columns are not used to reconstruct truth functions.
No producer module is imported. The public numerical primitives are used
only for fresh original-domain/initial-floor checks; the finite forest and
function cover is independently reconstructed from scalar rows.
"""
import argparse
from collections import Counter, deque
from itertools import combinations
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT
DEAD = (4, 5, 6, 7, 9, 10)
PREFIX_SHA = '89c4715b824b7cf4cee8a5698a612f336abdf20497ed48c5132dca514486afd4'
NUMERIC_SHA = '83c79d716581cdc8f947a21d9120a001624d8179fab8935817e28326f10bb041'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def scalar(x, word):
    bits = [(x >> q) & 1 for q in range(13)]
    for a, b in word:
        bits[a], bits[b] = min(bits[a], bits[b]), max(bits[a], bits[b])
    return sum(bit << q for q, bit in enumerate(bits))


def table(word, n):
    return tuple(scalar(x, word) for x in range(1 << n))


def columns(rows, n):
    return [sum(((y >> q) & 1) << x for x, y in enumerate(rows)) for q in range(n)]


def semigroup():
    gates = [list(g) for g in combinations(range(3), 2)]
    identity = tuple(range(8))
    queue = deque([identity])
    paths, ids, states, edges = {identity: []}, {identity: 0}, [], []
    while queue:
        f = queue.popleft()
        i = ids[f]
        states.append({'id': i, 'columns': columns(f, 3), 'word': paths[f]})
        for g in gates:
            after = tuple(scalar(y, [g]) for y in f)
            if after not in paths:
                ids[after] = len(paths)
                paths[after] = paths[f] + [g]
                queue.append(after)
            edges.append([i, g, ids[after]])
    need(len(states) == len(paths) and len(edges) == 3 * len(states), 'unfinished semigroup queue')
    return {'states': states, 'all_edges': edges, 'complete_closure': True}


def all_words(length, live, path=()):
    if length == 0:
        yield [list(g) for g in path]
    else:
        for a, b in combinations(live, 2):
            yield from all_words(length - 1, [q for q in live if q != a], path + ((a, b),))


def initial_ground(prefix, early_entries):
    path = PUBLIC / 'numeric.py'
    need(hashlib.sha256(path.read_bytes()).hexdigest() == NUMERIC_SHA, 'credited numerical source changed')
    spec = importlib.util.spec_from_file_location('credited_numeric_initial_only', path)
    numeric = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(numeric)
    records, envelopes, assignments = {}, {}, 0
    for count, low in ((2, True), (2, False), (3, False)):
        original, groups = [], {}
        for ports in combinations(range(13), count):
            mask = sum(1 << q for q in ports)
            lo, hi = (mask, 0) if low else (0, mask)
            record, cube = numeric.follow(numeric.fresh_domain(lo, hi), prefix, 0)
            assignments += len(cube)
            original.append(record)
            tag = (record[2], record[3])
            groups[tag] = max(groups.get(tag, -1), record[4])
        name = f'{count}{"L" if low else "H"}'
        records[name], envelopes[name] = original, groups
    high = {q: envelopes['3H'].get((0, 6144 | (1 << q))) for q in DEAD}
    need(envelopes['2L'] == {(1 | (1 << q), 0): d for q, d in ((1, 7), (2, 7), (3, 7), (8, 6))},
         'fresh ordinary LOW ground changed')
    need(envelopes['2H'] == {(0, 6144): 9}, 'fresh held HIGH saturation changed')
    need(len(envelopes['3H']) == 6 and high == {4: 11, 5: 11, 6: 11, 7: 13, 9: 11, 10: 12},
         'fresh ordinary third-HIGH classes changed')
    checked = []
    for entry in early_entries:
        gate, w = entry['gate'], entry['witness']
        word = prefix + [gate]
        r = w['record']
        got, rows = numeric.follow(numeric.fresh_domain(*r[:2]), word, 0)
        need(got == r, 'actual early original record mismatch')
        k = 13 - (r[0] | r[1]).bit_count()
        need(k in (11, 12) and w['imported_size'] == {11: 35, 12: 39}[k], 'early bound changed')
        if w['kind'] == 'DIRECT_COST':
            need(r[4] + r[5] + w['imported_size'] > 44, 'early direct cost insufficient')
        else:
            need(w['kind'] == 'TIGHT_FREE_CUT' and r[4] + r[5] + w['imported_size'] == 44,
                 'early cut is not tight')
            q, x = w['physical_port'], w['full_Boolean_witness']
            need(all(v[q] in (0, 1) and all(v[t] <= v[q] if t < q else v[q] <= v[t]
                     for t in range(13) if t != q and v[t] in (0, 1)) for v in rows), 'early cut fails')
            actual, sorted_bit = scalar(x, word) >> q & 1, int(x.bit_count() >= 13 - q)
            need(actual == w['actual_bit'] and sorted_bit == w['sorted_bit'] and actual != sorted_bit,
                 'early scalar global rank witness fails')
        checked.append([gate, r, digest(rows)])
    return records, high, assignments, checked


def forest_record(i, word, original_records, early):
    # Route every actual immutable original triple, accumulating marked
    # contacts. This does not apply the producer's max-cost recurrence.
    routed = [[r[3], r[4]] for r in original_records]
    roots = {q: {q} for q in DEAD}
    stages = []
    for a, b in word:
        need(a in roots and b in roots and a < b, 'non-live labelled binary')
        for r in routed:
            tags, cost = r
            hit = bool(tags & ((1 << a) | (1 << b)))
            if tags >> a & 1 and not tags >> b & 1:
                tags ^= (1 << a) | (1 << b)
            r[:] = [tags, cost + int(hit)]
        roots[b].update(roots.pop(a))
        envelope = {}
        for tags, cost in routed:
            secondary = tags & ~6144
            need(tags & 6144 == 6144 and secondary.bit_count() == 1, 'third-HIGH actual tags malformed')
            q = secondary.bit_length() - 1
            envelope[q] = max(envelope.get(q, -1), cost)
        need(set(envelope) == set(roots), 'live-root partition differs from actual original tags')
        stages.append([[[q, d] for q, d in sorted(envelope.items())],
                       sum(1 << d for d in envelope.values())])
    status = 'MASS_REJECTED' if any(stage[1] > 32768 for stage in stages) else (
             'EARLY_PUBLIC_NEGATIVE' if tuple(word[0]) in early else 'RETAINED')
    rules = []
    for q, component in sorted(roots.items()):
        other = [j for j, gate in enumerate(word) if any(p not in component for p in gate)]
        if other:
            j = max(other)
            moved = [list(g) for g in word]
            # Replay literal adjacent disjoint swaps, rather than only
            # assuming the desired permuted forest has equal endpoints.
            for p in range(j, len(word) - 1):
                need(set(moved[p]).isdisjoint(moved[p + 1]), 'component commutation is not disjoint')
                moved[p], moved[p + 1] = moved[p + 1], moved[p]
            need(table(word, 6) == table(moved, 6), 'disjoint forest functions differ')
            # Above gates are physical ports; test all local DEAD inputs
            # as well (the thirteen-column helper includes fixed upper bits).
            local = [[DEAD.index(a), DEAD.index(b)] for a, b in word]
            reordered = [[DEAD.index(a), DEAD.index(b)] for a, b in moved]
            need(table(local, 6) == table(reordered, 6), 'entire64-row reordering differs')
            freed = set(DEAD) - set(roots)
            head_support = {8, q}
            tail_support = {1, 2, 3, min(8, q)}
            need(head_support.isdisjoint(moved[-1]) and tail_support.isdisjoint(moved[-1]) and
                 head_support.isdisjoint(freed) and tail_support.isdisjoint(freed),
                 'head/tail cannot cross displaced binary or arbitrary freed preparation')
            # The reordered first two binaries must still be legal live
            # events. Both the original minimum-length BG representative
            # and this exact sorter word have the same total length.
            active = set(DEAD)
            for a, b in moved:
                need(a in active and b in active, 'reordered forest not legal')
                active.remove(a)
            rules.append({'partner': q, 'kind': 'COMMUTATION_TO_PUBLIC_TWO_BINARY',
                          'outside_binary_index': j, 'reordered_forest': moved,
                          'two_binary_prefix': moved[:2]})
        else:
            e = dict(stages[-1][0])[q]
            head_mass = stages[-1][1] + (1 << e)
            if head_mass > 32768:
                rules.append({'partner': q, 'kind': 'ORDINARY_THIRD_HIGH_HEAD_MASS',
                              'ordinary_mass': stages[-1][1], 'exponent': e, 'head_mass': head_mass})
            else:
                need(component == {4, 5, 6, 9} and q == 9 and e == 13 and stages[-1][1] == 20480,
                     'unclassified live-component exception')
                need(set(word[0]).isdisjoint(word[1]) and set(word[0] + word[1]) == component and
                     word[2] == sorted([max(word[0]), max(word[1])]), 'exception is not a balanced tree')
                rules.append({'partner': q, 'kind': 'BALANCED_FOUR_ELEVEN_EXCEPTION',
                              'leaves': sorted(component), 'ordinary_mass': 20480,
                              'exponent': 13, 'head_mass': 28672})
    return {'id': i, 'word': word, 'stages': stages,
            'components': [[q, sorted(leaves)] for q, leaves in sorted(roots.items())],
            'status': status, 'head_rules': rules}


def inspect(data, ground=True, embed=True):
    supplied = data['mathematical']
    need(digest(supplied) == data['entire_mathematical_record_sha256'], 'whole producer mathematical digest mismatch')
    prefix = supplied['literal_prefix']
    need(len(prefix) == 28 and digest(prefix) == PREFIX_SHA and supplied['dead_ports'] == list(DEAD),
         'literal Q or physical support changed')
    public = json.loads((PUBLIC / 'certificate.json').read_text())
    early = {tuple(x['gate']) for x in public['early_negative_first_gates']}
    need(early == {(4, 7), (4, 10), (5, 7), (6, 7), (6, 10), (7, 10), (9, 10)}, 'early negatives differ')
    if ground:
        originals, high, assignments, early_checks = initial_ground(prefix, public['early_negative_first_gates'])
    else:
        # Corruption controls need not repeat the expensive original cubes.
        # The full positive invocation supplies this cache, not the producer.
        originals, high, assignments, early_checks = GROUND_CACHE
    need(supplied['three_input_library'] == semigroup(), 'complete whole-row semigroup/shortest paths/edges differ')
    words = list(all_words(3, list(DEAD)))
    need(len(words) == 900 and len(supplied['all900_raw_binary_forests']) == 900, 'labelled forest coverage differs')
    forests = [forest_record(i, w, originals['3H'], early) for i, w in enumerate(words)]
    need(supplied['all900_raw_binary_forests'] == forests, 'whole labelled forests/stages/components/head rules differ')
    parents = [scalar(x, prefix) for x in range(8192)]
    reachable = sorted({sum(((v >> q) & 1) << j for j, q in enumerate(DEAD)) for v in parents})
    need(len(reachable) == 36 and supplied['actual_reachable_Q_inputs'] == reachable, 'true ordered-input projection differs')
    need(all(all((y >> q & 1) == int(x.bit_count() >= 13 - q) for q in (0, 11, 12)) and
                 min(y >> q & 1 for q in (1, 2, 3, 8)) == int(x.bit_count() >= 12)
             for x, y in enumerate(parents)), 'scalar held ranks/LOW collection changed')
    raws, groups = [], {}
    for forest in forests:
        if forest['status'] != 'RETAINED':
            continue
        free = sorted(set(DEAD) - {q for q, leaves in forest['components']})
        for f in supplied['three_input_library']['states']:
            word = forest['word'] + [[free[a], free[b]] for a, b in f['word']]
            local = [[DEAD.index(a), DEAD.index(b)] for a, b in word]
            whole = table(local, 6)
            key = tuple(whole[x] for x in reachable)
            raw = {'id': len(raws), 'forest_id': forest['id'], 'library_id': f['id'], 'freed_ports': free,
                   'word': word, 'full64_function': columns(whole, 6),
                   'actual_Q_key': columns(key, 6)}
            raws.append(raw)
            groups.setdefault(key, []).append(raw['id'])
    need(raws == supplied['all_retained_raw_BG_words'], 'every raw BG function/binding differs')
    keys = sorted(groups, key=lambda k: min((len(raws[i]['word']), raws[i]['word']) for i in groups[k]))
    classes, counts, embeddings = [], Counter(), []
    for state, key in enumerate(keys):
        ids = groups[key]
        rep = min((raws[i] for i in ids), key=lambda r: (len(r['word']), r['word']))
        shortest = len(rep['word'])
        eligible = sorted((raws[i] for i in ids if len(raws[i]['word']) == shortest), key=lambda r: r['word'])
        heads = []
        for q in DEAD:
            options = [(r, rule) for r in eligible for rule in forests[r['forest_id']]['head_rules']
                       if rule['partner'] == q and rule['kind'] != 'BALANCED_FOUR_ELEVEN_EXCEPTION']
            if options:
                raw, rule = min(options, key=lambda x: (x[1]['kind'], x[0]['word']))
                heads.append({'partner': q, 'structural_negative': {**rule, 'raw_word_id': raw['id']}})
                counts[rule['kind']] += 1
            else:
                heads.append({'partner': q, 'structural_negative': None})
                counts['UNCHECKED_HEAD'] += 1
        classes.append({'state_id': state, 'shortest_word': rep['word'], 'full64_function': rep['full64_function'],
                        'actual_Q_key': rep['actual_Q_key'], 'representative_raw_id': rep['id'],
                        'represented_raw_ids': ids, 'minimum_length_raw_ids': [r['id'] for r in eligible], 'heads': heads})
        # Validate every original thirteen-output function by direct local
        # scalar substitution. All 8192 entries, including unchanged outputs,
        # are retained in the digest; no unordered image is compared.
        if not embed:
            continue
        t = table([[DEAD.index(a), DEAD.index(b)] for a, b in rep['word']], 6)
        complement = 8191 ^ sum(1 << q for q in DEAD)
        entire = []
        for y in parents:
            original = sum(((y >> q) & 1) << j for j, q in enumerate(DEAD))
            z = t[original]
            entire.append((y & complement) | sum(((z >> j) & 1) << q for j, q in enumerate(DEAD)))
        embeddings.append([state, digest(entire)])
    need(classes == supplied['whole_Q_function_classes'], 'entire quotient/minimum-length structural head binding differs')
    need(dict(counts) == supplied['structural_head_counts'] and
         3 * counts['UNCHECKED_HEAD'] == supplied['remaining_head_tail_alternatives'], 'head accounting differs')
    surviving_live = []
    for c in classes:
        forest = forests[raws[c['representative_raw_id']]['forest_id']]
        live = {q for q, leaves in forest['components']}
        for h in c['heads']:
            if h['structural_negative'] is None and h['partner'] in live:
                need(h['partner'] == 9, 'unexpected surviving live head')
                surviving_live.append({'state_id': c['state_id'], 'partner': 9, 'word': c['shortest_word'],
                                       'minimum_length_raw_ids': c['minimum_length_raw_ids']})
    checked = {'entire_producer_math_sha256': digest(supplied), 'all900_forests_from_actual_original_routes': forests,
               'fresh_original_ground_records': originals, 'fresh_ground_assignments': assignments,
               'early_negative_original_checks': early_checks, 'whole13_embedding_hashes': embeddings,
               'entire_three_input_semigroup': supplied['three_input_library'],
               'all3597_raw_scalar_bindings_sha256': digest(raws), 'all1042_class_bindings_sha256': digest(classes),
               'structural_head_counts': dict(counts), 'surviving_live_head_cases': surviving_live,
               'remaining_head_tail_alternatives': 3 * counts['UNCHECKED_HEAD'],
               'complete_cover': True, 'three_binary_exclusion': False, 'global44_exclusion': False}
    return checked, (originals, high, assignments, early_checks)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, default=ROOT / 'generated/cover-produced.json')
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    started = time.monotonic()
    data = json.loads(args.input.read_text())
    checked, ground = inspect(data)
    output = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'COMPLETE_SEPARATE_SCALAR_THREE_BINARY_COVER',
              'mathematical': checked, 'entire_mathematical_record_sha256': digest(checked),
              'seconds': time.monotonic() - started, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(output, separators=(',', ':')) + '\n')
    print(json.dumps({'status': output['status'], 'whole_math_sha256': output['entire_mathematical_record_sha256'],
                      'surviving_live_heads': checked['surviving_live_head_cases'],
                      'head_counts': checked['structural_head_counts'], 'seconds': output['seconds'],
                      'rss_kib': output['maximum_rss_kib']}))


if __name__ == '__main__':
    main()
