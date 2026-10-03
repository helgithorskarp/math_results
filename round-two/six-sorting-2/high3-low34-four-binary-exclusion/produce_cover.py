"""Complete four-binary candidate cover, packed functions, before exclusions.

Whole-function quotient adapted from public10084 generate_cover.py; all
2700 labelled histories and all261 four-port G functions are represented.
No actual original numeric negative or D/R history is transferred.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

DEAD = (4, 5, 6, 7, 9, 10)
INITIAL = {4: 11, 5: 11, 6: 11, 7: 13, 9: 11, 10: 12}
PUBLIC = Path(__file__).resolve().parent
EARLY = {(4, 7), (4, 10), (5, 7), (6, 7), (6, 10), (7, 10), (9, 10)}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def identity(n):
    return tuple(sum(1 << x for x in range(1 << n) if x >> q & 1) for q in range(n))


def follow(columns, word):
    v = list(columns)
    for a, b in word:
        v[a], v[b] = v[a] & v[b], v[a] | v[b]
    return tuple(v)


def forests():
    output = []

    def visit(word, live):
        if len(word) == 4:
            costs, parts, stages = dict(INITIAL), {q: {q} for q in DEAD}, []
            for a, b in word:
                costs[b] = 1 + max(costs.pop(a), costs[b])
                parts[b] |= parts.pop(a)
                stages.append([sorted(costs.items()), sum(1 << d for d in costs.values())])
            status = ('MASS_REJECTED' if any(s[1] > 32768 for s in stages) else
                      'EARLY_PUBLIC_NEGATIVE' if tuple(word[0]) in EARLY else 'RETAINED')
            output.append({'id': len(output), 'word': word, 'stages': stages,
                           'components': [[q, sorted(p)] for q, p in sorted(parts.items())],
                           'status': status})
            return
        for a, b in combinations(live, 2):
            visit(word + [[a, b]], tuple(q for q in live if q != a))
    visit([], DEAD)
    return output


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--library', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    started = time.monotonic()
    library_packet = json.loads(args.library.read_text())
    lib = library_packet['mathematical']
    need(digest(lib) == 'b902f66e290883233e77992729df6f28deefbdf0abbc75a2405855f5991fee22'
         and library_packet['whole_math_sha256'] == digest(lib), 'complete four-port library changed')
    original = PUBLIC / 'fixture.json'
    need(hashlib.sha256(original.read_bytes()).hexdigest() ==
         'cd8efb3b155157cfcb6d9275ce521bc22373fa3da78a2df08ca502db57150a1a', 'public10084 certificate changed')
    parent = json.loads(original.read_text())
    prefix = parent['literal_prefix']
    need(digest(prefix) == '89c4715b824b7cf4cee8a5698a612f336abdf20497ed48c5132dca514486afd4',
         'literal Q changed')
    full = follow(identity(13), prefix)
    reachable = sorted({sum(((full[q] >> x) & 1) << j for j, q in enumerate(DEAD))
                        for x in range(8192)})
    need(len(reachable) == 36, 'Q projection changed')
    projected = {}

    def key(cols):
        result = []
        for col in cols:
            if col not in projected:
                projected[col] = sum(((col >> x) & 1) << j for j, x in enumerate(reachable))
            result.append(projected[col])
        return tuple(result)

    local_id = identity(6)
    all_forests = forests()
    need(len(all_forests) == 2700, 'four-binary forest coverage changed')
    groups, raw, class_counts = {}, [], Counter()
    for forest in all_forests:
        if forest['status'] != 'RETAINED':
            continue
        live = {q for q, leaves in forest['components']}
        free = sorted(set(DEAD) - live)
        need(len(free) == 4 and len(live) == 2, 'four-binary support changed')
        for entry in lib['states']:
            if time.monotonic() - started > 30:
                raise RuntimeError('operational cap: incomplete cover, not an exclusion')
            word = forest['word'] + [[free[a], free[b]] for a, b in entry['word']]
            cols = follow(local_id, [[DEAD.index(a), DEAD.index(b)] for a, b in word])
            k = key(cols)
            if k not in groups:
                groups[k] = {'temporary_id': len(groups), 'minimum_word': word,
                             'representative_forest_id': forest['id'],
                             'representative_library_id': entry['id'],
                             'full64_columns': list(cols), 'represented_raw_count': 0}
            group = groups[k]
            if (len(word), word) < (len(group['minimum_word']), group['minimum_word']):
                group.update(minimum_word=word, representative_forest_id=forest['id'],
                             representative_library_id=entry['id'], full64_columns=list(cols))
            group['represented_raw_count'] += 1
            raw.append([forest['id'], entry['id'], group['temporary_id']])
    ordered = sorted(groups, key=lambda k: (len(groups[k]['minimum_word']), groups[k]['minimum_word']))
    relabel, classes = {}, []
    for state, k in enumerate(ordered):
        group = groups[k]
        relabel[group['temporary_id']] = state
        entry = {'state_id': state, 'shortest_word': group['minimum_word'],
                 'representative_forest_id': group['representative_forest_id'],
                 'representative_library_id': group['representative_library_id'],
                 'full64_columns': group['full64_columns'], 'actual_Q_key': list(k),
                 'represented_raw_count': group['represented_raw_count'],
                 'public10084_equal_prefix': None}
        # Rank2 unit images cannot equal a three-binary rank3 function.
        class_counts['NEW_WHOLE_Q_FUNCTION'] += 1
        classes.append(entry)
    for binding in raw:
        binding[2] = relabel[binding[2]]
    math = {'literal_prefix': prefix, 'dead_ports': list(DEAD),
            'actual_reachable_Q_inputs': reachable, 'four_input_library': lib,
            'all2700_binary_forests': all_forests, 'all_retained_raw_bindings': raw,
            'whole_Q_function_classes': classes, 'class_status_counts': dict(class_counts),
            'complete_preparation_word_cover': True,
            'four_binary_exclusion': False, 'unrestricted44_exclusion': False}
    output = {'agent': 'six-sorting-2', 'role': 'researcher',
              'status': 'COMPLETE_FOUR_BINARY_CANDIDATE_COVER_PRODUCED_NOT_SEPARATELY_CHECKED',
              'mathematical': math, 'whole_math_sha256': digest(math),
              'seconds': time.monotonic() - started,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(output, separators=(',', ':')) + '\n')
    print(json.dumps({'status': output['status'], 'forest_status_counts': dict(Counter(f['status'] for f in all_forests)),
                      'retained_BG_words': len(raw), 'whole_Q_function_classes': len(classes),
                      'class_status_counts': dict(class_counts),
                      'representative_lengths': dict(Counter(len(c['shortest_word']) for c in classes)),
                      'whole_math_sha256': output['whole_math_sha256'],
                      'seconds': output['seconds'], 'rss_kib': output['maximum_rss_kib']}))


if __name__ == '__main__':
    main()
