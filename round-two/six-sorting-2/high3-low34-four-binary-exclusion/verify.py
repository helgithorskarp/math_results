"""Portable four-binary scalar replay of every actual-original binding.
No selector, private path, old negative corpus or generated cube is imported.
The separate reconstructed cover supplies every exact function binding.
"""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
SCALAR_SHA = '83c79d716581cdc8f947a21d9120a001624d8179fab8935817e28326f10bb041'
if hashlib.sha256((ROOT / 'numeric.py').read_bytes()).hexdigest() != SCALAR_SHA:
    raise ValueError('credited scalar source changed')
spec = importlib.util.spec_from_file_location('credited_scalar_numerical_primitives', ROOT / 'numeric.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)
FLOORS = {9: 25, 10: 29, 11: 35, 12: 39}
DEAD = (4, 5, 6, 7, 9, 10)

class Replay:
    def __init__(self, prefix):
        self.prefix, self.base = prefix, {}

    def record(self, expected, extension):
        lo, hi = expected[:2]
        if (lo, hi) not in self.base:
            self.base[lo, hi] = n.follow(n.fresh_domain(lo, hi), self.prefix, 0)
        actual, rows = n.follow(self.base[lo, hi], extension, 28)
        n.need(actual == expected, 'actual original D/R/tags/identity positions differ')
        return actual, rows

    def check(self, w, extension):
        kind = w['kind']
        if kind == 'SEMANTIC_WEIGHTED_MASS':
            counts = w['original_counts']
            k = 13 - sum(counts)
            n.need(k in FLOORS and w['imported_size'] == FLOORS[k], 'semantic imported floor mismatch')
            classes, records = set(), []
            for expected in w['distinct_tag_witness_records']:
                actual, rows = self.record(expected, extension)
                n.need([actual[0].bit_count(), actual[1].bit_count()] == counts, 'semantic original family mismatch')
                tag = tuple(actual[2:4])
                n.need(tag not in classes, 'duplicate actual current semantic class')
                classes.add(tag)
                records.append([actual, n.digest(rows)])
            mass, ceiling = sum(1 << (r[0][4] + r[0][5]) for r in records), 1 << (44 - FLOORS[k])
            n.need(mass == w['mass'] and ceiling == w['ceiling'] and mass > ceiling, 'semantic mass not strict')
            return {'kind': kind, 'actual_original_records': records, 'strict_mass': mass, 'ceiling': ceiling}
        actual, rows = self.record(w['record'], extension)
        k = 13 - (actual[0] | actual[1]).bit_count()
        n.need(k in FLOORS and w['imported_size'] == FLOORS[k], 'imported original floor mismatch')
        cost = actual[4] + actual[5]
        if kind == 'DIRECT_COST':
            n.need(cost + FLOORS[k] > 44, 'direct original cost insufficient')
            return {'kind': kind, 'actual_original_record': actual, 'entire_original_rows_sha256': n.digest(rows)}
        n.need(kind in ('TIGHT_FREE_CUT', 'TIGHT_MARKED_PORT_LOCK') and cost + FLOORS[k] == 44,
               'cut/lock original is not tight')
        q, x = w['physical_port'], w['full_Boolean_witness']
        n.need(type(q) is int and 0 <= q < 13 and type(x) is int and 0 <= x < 8192, 'rank witness malformed')
        if kind == 'TIGHT_MARKED_PORT_LOCK':
            n.need(all(v[q] < 0 or v[q] > 1 for v in rows), 'locked physical port is not always marked')
        else:
            n.need(all(v[q] in (0, 1) and all(v[t] <= v[q] if t < q else v[q] <= v[t]
                     for t in range(13) if t != q and v[t] in (0, 1)) for v in rows), 'whole-original free cut fails')
        bit = n.bool_word(x, self.prefix + extension) >> q & 1
        want = int(x.bit_count() >= 13 - q)
        n.need(bit == w['actual_bit'] and want == w['sorted_bit'] and bit != want, 'actual unclamped rank witness fails')
        return {'kind': kind, 'actual_original_record': actual, 'entire_original_rows_sha256': n.digest(rows),
                'physical_port': q, 'full_Boolean_witness': x, 'actual_bit': bit, 'sorted_bit': want}

def tail_structure():
    words, evidence = {}, []
    for q in DEAD:
        support = sorted((1, 2, 3, min(8, q)))
        a, b, c, d = support
        pairs = (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))
        canonical = [[list(x), list(y), sorted((min(x), min(y)))] for x, y in pairs]
        orders = list(n.all_equal_tails({p: 7 for p in support}))
        n.need(len(orders) == 6 and all(len(w) == 3 for w in orders), 'complete equal-tail recursion differs')
        groups = {}
        for w in orders:
            local = [[support.index(x), support.index(y)] for x, y in w]
            table = tuple(n.bool_word(x, local) for x in range(16))
            n.need(all(table[x] & 1 == int(x == 15) for x in range(16)), 'tail whole minimum differs')
            groups.setdefault(table, []).append(w)
        tables = [tuple(n.bool_word(x, [[support.index(u), support.index(v)] for u, v in w])
                        for x in range(16)) for w in canonical]
        n.need(len(groups) == 3 and set(tables) == set(groups) and all(len(ws) == 2 for ws in groups.values()),
               'complete three whole tail functions differ')
        words[q] = canonical
        evidence.append([q, orders, [list(t) for t in tables], [2, 2, 2]])
    return words, evidence


def interface(c, cover):
    n.need(c['schema'] == 'HIGH3_LOW34_ZERO_SINGLETON_FOUR_BINARY_EXCLUSION_V1' and
           c['size_budget'] == 44 and c['dead_ports'] == list(DEAD) and
           c['imported_live_head_lemma'] == '10034/0', 'literal schema/premises differ')
    n.need(c['literal_prefix'] == cover['literal_prefix'] and
           n.digest(c['literal_prefix']) == '89c4715b824b7cf4cee8a5698a612f336abdf20497ed48c5132dca514486afd4' and
           n.digest(cover) == c['cover_math_sha256'] ==
           'f9b99ef13250aef100e07aa37ce5d9aa6495bb5e59d2099b800216bd669ba523',
           'complete literal function cover differs')
    classes, rows = cover['whole_Q_function_classes'], c['function_bindings']
    n.need(len(classes) == len(rows) == 6400 and len(c['witnesses']) > 0 and
           n.digest([x['shortest_word'] for x in classes]) == c['function_words_sha256'],
           'all6400 canonical literal words/rows missing or changed')
    used = set()

    def reference(ref):
        n.need(type(ref) is int and 0 <= ref < len(c['witnesses']), 'actual witness reference malformed')
        used.add(ref)

    for state, (entry, row) in enumerate(zip(classes, rows)):
        n.need(entry['state_id'] == state, 'canonical state order differs')
        word = entry['shortest_word']
        live = set(DEAD)
        for a, b in word[:4]:
            n.need(a < b and a in live and b in live, 'non-live four-binary representative')
            live.remove(a)
        free = set(DEAD) - live
        n.need(len(live) == 2 and len(free) == 4 and
               all(a < b and a in free and b in free for a, b in word[4:]),
               'actual G leaves the final freed support')
        if type(row) is int:
            reference(row)
        else:
            n.need(isinstance(row, list) and len(row) == 6, 'head case lacks six physical partners')
            for q, refs in zip(DEAD, row):
                if q in live:
                    n.need(refs == 'L', 'actual live head is not the explicit10034 case')
                else:
                    n.need(type(refs) is int or isinstance(refs, list) and len(refs) == 3,
                           'freed head lacks one whole-head or three balanced-tail negatives')
                    for ref in [refs] if type(refs) is int else refs:
                        reference(ref)
    n.need(used == set(range(len(c['witnesses']))), 'unused or missing compact witness records')
    for w in c['witnesses']:
        n.need(w['kind'] in ('DIRECT_COST', 'TIGHT_FREE_CUT', 'TIGHT_MARKED_PORT_LOCK'),
               'unsupported sufficient witness kind')
        r = w['record']
        n.need(len(r) == 7 and all(type(x) is int and x >= 0 for x in r) and
               r[0] < 8192 and r[1] < 8192 and not r[0] & r[1],
               'literal immutable original record malformed')


def check_slice(c, cover, start, stop):
    interface(c, cover)
    n.need(type(start) is int and type(stop) is int and 0 <= start < stop <= 6400,
           'invalid complete-cover slice')
    tails, tail_evidence = tail_structure()
    replay = Replay(c['literal_prefix'])
    prep, heads, counts, samples = [], [], Counter(), []
    for state in range(start, stop):
        word = cover['whole_Q_function_classes'][state]['shortest_word']
        row = c['function_bindings'][state]
        if type(row) is int:
            w = c['witnesses'][row]
            checked = replay.check(w, word)
            prep.append([state, word, checked]); samples.append((w, word))
            counts['preparation_only_classes'] += 1
            counts[checked['kind']] += 1
            counts['covered_free_tail_alternatives'] += 12
            continue
        counts['head_tail_classes'] += 1
        for q, refs in zip(DEAD, row):
            if refs == 'L':
                counts['live_heads_by_actual10034'] += 1
                continue
            counts['actual_freed_heads'] += 1
            parts = [(None, refs)] if type(refs) is int else list(enumerate(refs))
            for tail, ref in parts:
                extension = word + [sorted((8, q))]
                if tail is not None:
                    extension += tails[q][tail]
                w = c['witnesses'][ref]
                checked = replay.check(w, extension)
                heads.append({'state_id': state, 'head_partner': q, 'tail_id': tail,
                              'extension': extension, 'checked': checked})
                samples.append((w, extension)); counts[checked['kind']] += 1
                counts['covered_free_tail_alternatives'] += 3 if tail is None else 1
    n.need(counts['preparation_only_classes'] + counts['head_tail_classes'] == stop - start and
           counts['actual_freed_heads'] == 4 * counts['head_tail_classes'] and
           counts['live_heads_by_actual10034'] == 2 * counts['head_tail_classes'] and
           counts['covered_free_tail_alternatives'] == 12 * (stop - start), 'actual slice coverage incomplete')
    return {'literal_prefix': c['literal_prefix'], 'selected_state_ids': list(range(start, stop)),
            'actual_preparation_only_bindings': prep, 'actual_head_tail_bindings': heads,
            'summary': dict(counts), 'all_tail_orders_and_full_functions': tail_evidence,
            'actual_original_domains': sorted([list(x) for x in replay.base]),
            'complete_selected_case_exclusion': True, 'unrestricted44_exclusion': False,
            'imported_live_head_lemma': 'actual10034/0; explicit ordinary dependency, not independently audited here'}, samples, replay


def damages(c, cover, start, stop, samples, replay):
    rejected = []
    numerical = []
    sample, extension = samples[0]
    for name, field in [('false_original_D', 4), ('false_current_HIGH_tag', 3),
                        ('false_absolute_identity_positions', 6)]:
        w = copy.deepcopy(sample); w['record'][field] ^= 1
        numerical.append((name, w, extension))
    w = copy.deepcopy(sample); w['imported_size'] -= 1
    numerical.append(('weakened_imported_floor', w, extension))
    for kind in ('TIGHT_FREE_CUT', 'TIGHT_MARKED_PORT_LOCK'):
        selected = [(w, e) for w, e in samples if w['kind'] == kind]
        if selected:
            original, extension = selected[0]
            w = copy.deepcopy(original); w['full_Boolean_witness'] = 0
            numerical.append((kind + ':no_incorrect_unclamped_rank', w, extension))
            w = copy.deepcopy(original); w['physical_port'] = 0
            numerical.append((kind + ':different_physical_port', w, extension))
    for name, w, extension in numerical:
        try:
            replay.check(w, extension)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted actual numerical corruption: ' + name)
    # Complete interface damages are tested without using certificate byte seals.
    changes = []
    d = copy.deepcopy(c); d['function_bindings'].pop()
    changes.append(('omitted_actual_prefix_class', d))
    d = copy.deepcopy(c); d['function_bindings'][start] = len(d['witnesses'])
    changes.append(('invalid_actual_original_reference', d))
    head_state = next(i for i, row in enumerate(c['function_bindings']) if isinstance(row, list))
    d = copy.deepcopy(c); d['function_bindings'][head_state].pop()
    changes.append(('omitted_physical_head', d))
    freed = next(j for j, ref in enumerate(c['function_bindings'][head_state]) if ref != 'L')
    d = copy.deepcopy(c); d['function_bindings'][head_state][freed] = 'L'
    changes.append(('freed_head_falsely_assigned_to_live_lemma', d))
    i, j = next((i, j) for i, row in enumerate(c['function_bindings']) if isinstance(row, list)
                for j, ref in enumerate(row) if isinstance(ref, list))
    d = copy.deepcopy(c); d['function_bindings'][i][j].pop()
    changes.append(('omitted_balanced_tail_function', d))
    for name, d in changes:
        try:
            interface(d, cover)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted damaged actual coverage: ' + name)
    return rejected


def main():
    p = argparse.ArgumentParser(); p.add_argument('--offset', type=int, required=True)
    p.add_argument('--cases', type=int, required=True); p.add_argument('--output', type=Path, required=True)
    args = p.parse_args(); started = time.monotonic()
    cover = json.loads((ROOT / 'generated/cover-produced.json').read_text())['mathematical']
    checked = json.loads((ROOT / 'generated/cover-checked-normal.json').read_text())
    fixture = json.loads((ROOT / 'fixture.json').read_text())
    n.need(n.digest(cover) == fixture['expected_cover_math_sha256'] and
           n.digest(checked['mathematical']) == checked['whole_math_sha256'] ==
           fixture['expected_scalar_cover_math_sha256'] and
           checked['mathematical']['independently_reconstructed_entire_producer_math_sha256'] == n.digest(cover) and
           checked['mathematical']['fresh_ground_assignments'] == 612352 and
           checked['mathematical']['complete_four_binary_candidate_cover'],
           'fresh complete independently reconstructed cover is absent or changed')
    c = json.loads((ROOT / 'certificate.json').read_text())
    math, samples, replay = check_slice(c, cover, args.offset, args.offset + args.cases)
    math['damages_rejected'] = damages(c, cover, args.offset, args.offset + args.cases, samples, replay)
    out = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'COMPLETE_SELECTED_PORTABLE_FOUR_BINARY_EXCLUSION',
           'mathematical': math, 'whole_math_sha256': n.digest(math), 'seconds': time.monotonic() - started,
           'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, separators=(',', ':')) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'mathematical'}))
    print(json.dumps({'summary': math['summary'], 'original_domains': len(replay.base), 'damages': len(math['damages_rejected'])}))


if __name__ == '__main__':
    main()
