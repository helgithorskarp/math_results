"""Portable complete three-binary/three-input-G packed candidate producer.

Whole functions and labelled forest histories are retained. No failed
selector is used here. Structural negatives depend on public9982 and
the credited ordinary mass theorem, not transferred original histories.
"""
import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT
DEAD = (4, 5, 6, 7, 9, 10)
INITIAL = {4: 11, 5: 11, 6: 11, 7: 13, 9: 11, 10: 12}
EARLY = {(4, 7), (4, 10), (5, 7), (6, 7), (6, 10), (7, 10), (9, 10)}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def truth_columns(n):
    return tuple(sum(1 << x for x in range(1 << n) if x >> q & 1) for q in range(n))


def follow(columns, word):
    result = list(columns)
    for a, b in word:
        result[a], result[b] = result[a] & result[b], result[a] | result[b]
    return tuple(result)


def library():
    gates = [list(g) for g in combinations(range(3), 2)]
    states, words, edges = [truth_columns(3)], [[]], []
    seen = {states[0]: 0}
    cursor = 0
    while cursor < len(states):
        for gate in gates:
            after = follow(states[cursor], [gate])
            if after not in seen:
                seen[after] = len(states)
                states.append(after)
                words.append(words[cursor] + [gate])
            edges.append([cursor, gate, seen[after]])
        cursor += 1
    return {'states': [{'id': i, 'columns': list(f), 'word': w}
                       for i, (f, w) in enumerate(zip(states, words))],
            'all_edges': edges, 'complete_closure': True}


def binary_record(word):
    costs = dict(INITIAL)
    components = {q: {q} for q in DEAD}
    stages = []
    for a, b in word:
        need(a in costs and b in costs and a < b, 'non-live binary')
        costs[b] = 1 + max(costs.pop(a), costs[b])
        components[b] |= components.pop(a)
        stages.append([sorted(costs.items()), sum(1 << e for e in costs.values())])
    return stages, components


def enumerate_forests():
    raw = []

    def visit(word, live):
        if len(word) == 3:
            stages, parts = binary_record(word)
            status = ('MASS_REJECTED' if any(s[1] > 32768 for s in stages)
                      else 'EARLY_PUBLIC_NEGATIVE' if tuple(word[0]) in EARLY else 'RETAINED')
            record = {'id': len(raw), 'word': word, 'stages': stages,
                      'components': [[q, sorted(leaves)] for q, leaves in sorted(parts.items())],
                      'status': status, 'head_rules': []}
            for q, leaves in sorted(parts.items()):
                outside = [i for i, gate in enumerate(word) if not set(gate) <= leaves]
                if outside:
                    i = outside[-1]
                    reordered = word[:i] + word[i + 1:] + [word[i]]
                    need(all(not set(word[i]) & set(gate) for gate in word[i + 1:]),
                         'forest-component swap is not disjoint')
                    rule = {'partner': q, 'kind': 'COMMUTATION_TO_PUBLIC_TWO_BINARY',
                            'outside_binary_index': i, 'reordered_forest': reordered,
                            'two_binary_prefix': reordered[:2]}
                elif stages[-1][1] + (1 << dict(stages[-1][0])[q]) > 32768:
                    rule = {'partner': q, 'kind': 'ORDINARY_THIRD_HIGH_HEAD_MASS',
                            'ordinary_mass': stages[-1][1], 'exponent': dict(stages[-1][0])[q],
                            'head_mass': stages[-1][1] + (1 << dict(stages[-1][0])[q])}
                else:
                    need(leaves == {4, 5, 6, 9} and q == 9 and
                         dict(stages[-1][0])[q] == 13 and stages[-1][1] == 20480,
                         'unexpected surviving live-head structure')
                    rule = {'partner': q, 'kind': 'BALANCED_FOUR_ELEVEN_EXCEPTION',
                            'leaves': sorted(leaves), 'ordinary_mass': 20480,
                            'exponent': 13, 'head_mass': 28672}
                record['head_rules'].append(rule)
            raw.append(record)
            return
        for a, b in combinations(sorted(live), 2):
            visit(word + [[a, b]], live - {a})

    visit([], set(DEAD))
    return raw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'generated/cover-produced.json')
    args = parser.parse_args()
    start = time.monotonic()
    fixture = json.loads((PUBLIC / 'fixture.json').read_text())
    prefix = fixture['literal_prefix']
    need(digest(prefix) == '89c4715b824b7cf4cee8a5698a612f336abdf20497ed48c5132dca514486afd4',
         'literal Q differs')
    full = follow(truth_columns(13), prefix)
    reachable = sorted({sum(((full[q] >> x) & 1) << j for j, q in enumerate(DEAD))
                        for x in range(8192)})
    need(len(reachable) == 36, 'actual Q projection differs')
    lib, forests, raws, groups = library(), enumerate_forests(), [], {}
    need(len(forests) == 900, 'raw three-binary coverage differs')
    local_identity = truth_columns(6)
    for forest in forests:
        if forest['status'] != 'RETAINED':
            continue
        live = {q for q, leaves in forest['components']}
        freed = sorted(set(DEAD) - live)
        need(len(freed) == 3, 'freed support differs')
        for g in lib['states']:
            word = forest['word'] + [[freed[a], freed[b]] for a, b in g['word']]
            cols = follow(local_identity, [[DEAD.index(a), DEAD.index(b)] for a, b in word])
            key = tuple(sum(((col >> x) & 1) << j for j, x in enumerate(reachable)) for col in cols)
            raw = {'id': len(raws), 'forest_id': forest['id'], 'library_id': g['id'],
                   'freed_ports': freed, 'word': word, 'full64_function': list(cols),
                   'actual_Q_key': list(key)}
            raws.append(raw)
            groups.setdefault(key, []).append(raw['id'])
    keys = sorted(groups, key=lambda key: min((len(raws[i]['word']), raws[i]['word']) for i in groups[key]))
    classes, counts = [], Counter()
    for state, key in enumerate(keys):
        ids = groups[key]
        rep = min((raws[i] for i in ids), key=lambda raw: (len(raw['word']), raw['word']))
        minimum = len(rep['word'])
        eligible = sorted((raws[i] for i in ids if len(raws[i]['word']) == minimum), key=lambda raw: raw['word'])
        heads = []
        for q in DEAD:
            candidates = [(raw, rule) for raw in eligible
                          for rule in forests[raw['forest_id']]['head_rules'] if rule['partner'] == q
                          and rule['kind'] != 'BALANCED_FOUR_ELEVEN_EXCEPTION']
            if candidates:
                raw, rule = min(candidates, key=lambda item: (item[1]['kind'], item[0]['word']))
                heads.append({'partner': q, 'structural_negative': {**rule, 'raw_word_id': raw['id']}})
                counts[rule['kind']] += 1
            else:
                heads.append({'partner': q, 'structural_negative': None})
                counts['UNCHECKED_HEAD'] += 1
        classes.append({'state_id': state, 'shortest_word': rep['word'],
                        'full64_function': rep['full64_function'], 'actual_Q_key': list(key),
                        'representative_raw_id': rep['id'], 'represented_raw_ids': ids,
                        'minimum_length_raw_ids': [raw['id'] for raw in eligible], 'heads': heads})
    math = {'literal_prefix': prefix, 'prefix_sha256': digest(prefix), 'dead_ports': list(DEAD),
            'actual_reachable_Q_inputs': reachable, 'three_input_library': lib,
            'all900_raw_binary_forests': forests, 'all_retained_raw_BG_words': raws,
            'whole_Q_function_classes': classes, 'structural_head_counts': dict(counts),
            'remaining_head_tail_alternatives': 3 * counts['UNCHECKED_HEAD'],
            'scope': 'Complete candidate cover and structural deductions; remaining fronts not excluded; fullLOW34/global44gap open.'}
    out = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'COMPLETE_THREE_BINARY_CANDIDATE_COVER_PRODUCED_NOT_SEPARATELY_CHECKED',
           'mathematical': math, 'entire_mathematical_record_sha256': digest(math),
           'seconds': time.monotonic() - start, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, separators=(',', ':')) + '\n')
    print(json.dumps({'functions': len(classes), 'raw_forests_by_status': dict(Counter(f['status'] for f in forests)),
                      'G_functions': len(lib['states']), 'retained_raw_BG_words': len(raws),
                      'head_counts': dict(counts), 'remaining_alternatives': math['remaining_head_tail_alternatives'],
                      'whole_math_sha256': out['entire_mathematical_record_sha256'],
                      'seconds': out['seconds'], 'rss_kib': out['maximum_rss_kib']}))


if __name__ == '__main__':
    main()
