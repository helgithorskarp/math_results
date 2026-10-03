"""Portable scalar replay of the compact actual-original certificate.
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
    n.need(c['schema'] == 'HIGH3_LOW34_ZERO_SINGLETON_THREE_BINARY_EXCLUSION_V1' and
           c['size_budget'] == 44 and c['dead_ports'] == list(DEAD) and c['imported_live_head_lemma'] == '10034/0',
           'exact candidate schema or premise differs')
    n.need(c['literal_prefix'] == cover['literal_prefix'] and
           n.digest(c['literal_prefix']) == '89c4715b824b7cf4cee8a5698a612f336abdf20497ed48c5132dca514486afd4',
           'literal Q differs')
    fs = c['function_bindings']
    n.need(len(fs) == len(cover['whole_Q_function_classes']) == 1042 and len(c['witnesses']) > 0,
           'complete1042 function coverage or actual witnesses missing')
    for state, (word, heads) in enumerate(fs):
        n.need(word == cover['whole_Q_function_classes'][state]['shortest_word'] and len(heads) == 6,
               'actual minimum-length representative or complete six heads differ')
        live = set(DEAD)
        for a, b in word[:3]:
            n.need(a in live and b in live and a < b, 'non-live labelled binary')
            live.remove(a)
        freed = set(DEAD) - live
        n.need(all(a in freed and b in freed and a < b for a, b in word[3:]),
               'preparation is outside the final freed support')
        for q, refs in zip(DEAD, heads):
            if q in live:
                n.need(refs == 'L', 'live head not bound to actual10034')
            else:
                n.need(type(refs) is int or isinstance(refs, list) and len(refs) == 3,
                       'freed head requires one negative or all three tail negatives')
                for ref in [refs] if type(refs) is int else refs:
                    n.need(type(ref) is int and 0 <= ref < len(c['witnesses']), 'negative reference malformed')


def check_slice(c, cover, start, stop):
    interface(c, cover)
    n.need(type(start) is int and type(stop) is int and 0 <= start < stop <= 1042,
           'invalid exact finite slice')
    tails, tail_evidence = tail_structure()
    replay = Replay(c['literal_prefix'])
    bindings, counts, samples = [], Counter(), []
    for state in range(start, stop):
        word, heads = c['function_bindings'][state]
        for q, refs in zip(DEAD, heads):
            if refs == 'L':
                counts['live_heads_by_actual10034'] += 1
                continue
            counts['freed_heads'] += 1
            parts = [(None, refs)] if type(refs) is int else list(enumerate(refs))
            for tail, ref in parts:
                extension = word + [sorted((8, q))]
                if tail is not None:
                    extension += tails[q][tail]
                w = c['witnesses'][ref]
                checked = replay.check(w, extension)
                bindings.append({'state_id': state, 'head_partner': q, 'tail_id': tail,
                                 'extension': extension, 'checked': checked})
                samples.append((w, extension))
                counts[checked['kind']] += 1
                counts['covered_free_tail_alternatives'] += 3 if tail is None else 1
    n.need(counts['freed_heads'] == counts['live_heads_by_actual10034'] == 3 * (stop - start) and
           counts['covered_free_tail_alternatives'] == 9 * (stop - start), 'complete selected head/tail coverage differs')
    return {'literal_prefix': c['literal_prefix'], 'selected_state_ids': list(range(start, stop)),
            'all_actual_negative_bindings': bindings, 'summary': dict(counts),
            'all_tail_orders_and_full_functions': tail_evidence,
            'actual_original_domains': sorted([list(x) for x in replay.base]),
            'complete_selected_freed_head_exclusion': True, 'unrestricted44_exclusion': False,
            'imported_live_head_lemma': 'actual10034/0; author-checked, independent-person review pending'}, samples, replay


def damages(c, cover, start, stop, samples, replay):
    damaged = []
    sample, extension = next((w, e) for w, e in samples if w['kind'] != 'SEMANTIC_WEIGHTED_MASS')
    for name, key, value in (('false_original_D', 4, sample['record'][4] - 1),
                             ('false_current_HIGH_tag', 3, sample['record'][3] ^ 1),
                             ('false_absolute_identity_positions', 6, sample['record'][6] ^ 1)):
        w = copy.deepcopy(sample)
        w['record'][key] = value
        damaged.append((name, w, extension))
    w = copy.deepcopy(sample); w['imported_size'] -= 1
    damaged.append(('weakened_imported_floor', w, extension))
    ranked = [(w, e) for w, e in samples if w['kind'] in ('TIGHT_MARKED_PORT_LOCK', 'TIGHT_FREE_CUT')]
    if ranked:
        sample, extension = ranked[0]
        w = copy.deepcopy(sample); w['full_Boolean_witness'] = 0
        damaged.append(('no_incorrect_global_rank', w, extension))
        w = copy.deepcopy(sample); w['physical_port'] = 0
        damaged.append(('different_physical_rank_port', w, extension))
    semantic = [(w, e) for w, e in samples if w['kind'] == 'SEMANTIC_WEIGHTED_MASS']
    if semantic:
        sample, extension = semantic[0]
        w = copy.deepcopy(sample); w['distinct_tag_witness_records'].append(copy.deepcopy(w['distinct_tag_witness_records'][0]))
        damaged.append(('duplicated_actual_mass_tag', w, extension))
        w = copy.deepcopy(sample); w['mass'] += 1
        damaged.append(('altered_strict_semantic_mass', w, extension))
    rejected = []
    for name, w, extension in damaged:
        try:
            replay.check(w, extension)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('damaged mathematical witness accepted: ' + name)
    # These damage the exact cover binding, without checking a file hash.
    changes = []
    p = copy.deepcopy(c); p['function_bindings'].pop()
    changes.append(('omitted_prefix_function', p))
    p = copy.deepcopy(c); p['function_bindings'][start][1].pop()
    changes.append(('omitted_physical_head', p))
    p = copy.deepcopy(c); p['function_bindings'][start][0].append([4, 5])
    changes.append(('changed_actual_prefix_word', p))
    p = copy.deepcopy(c)
    head = next((state, j) for state in range(start, stop)
                for j, ref in enumerate(p['function_bindings'][state][1]) if ref != 'L')
    p['function_bindings'][head[0]][1][head[1]] = 'L'
    changes.append(('freed_head_falsely_assigned_to_live_lemma', p))
    tails = [(state, j) for state in range(start, stop) for j, ref in enumerate(c['function_bindings'][state][1])
             if isinstance(ref, list)]
    if tails:
        p = copy.deepcopy(c); state, j = tails[0]
        p['function_bindings'][state][1][j].pop()
        changes.append(('missing_balanced_tail_function', p))
    for name, p in changes:
        try:
            interface(p, cover)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('damaged coverage interface accepted: ' + name)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--offset', type=int, required=True)
    parser.add_argument('--cases', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    cover = json.loads((ROOT / 'generated/cover-produced.json').read_text())['mathematical']
    n.need(n.digest(cover) == 'f81df63d10258d3560c7915e617d04f9f8caf76cfd961dc517b607e2bf6066ab', 'entire fresh packed cover differs')
    checked = json.loads((ROOT / 'generated/cover-checked-normal.json').read_text())
    n.need(checked['status'] == 'COMPLETE_SEPARATE_SCALAR_THREE_BINARY_COVER' and
           n.digest(checked['mathematical']) == checked['entire_mathematical_record_sha256'] ==
           '5da3911448df2171ae2823136b750a57ac6fd87d24d546a342cfade4b44484c4', 'entire independent scalar cover missing')
    c = json.loads((ROOT / 'certificate.json').read_text())
    math, samples, replay = check_slice(c, cover, args.offset, args.offset + args.cases)
    math['damages_rejected'] = damages(c, cover, args.offset, args.offset + args.cases, samples, replay)
    output = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'COMPLETE_SELECTED_PORTABLE_SCALAR_EXCLUSION',
              'mathematical': math, 'entire_mathematical_record_sha256': n.digest(math),
              'seconds': time.monotonic() - started, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, separators=(',', ':')) + '\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'mathematical'}))
    print(json.dumps({'summary': math['summary'], 'original_domains': len(replay.base), 'damages': len(math['damages_rejected'])}))


if __name__ == '__main__':
    main()
