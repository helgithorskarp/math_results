"""Independent scalar four-binary cover and original-domain mass replay.

No packed producer is imported. For every raw B;G binding, compose actual
row functions, rebuild every minimum representative and classify by
ordered rows on the same reachable Q inputs. Parent initial_ground is
credited numeric replay only (not its forest or function producer).
"""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

from check_g4 import reconstruct

DEAD = (4, 5, 6, 7, 9, 10)
PUBLIC = Path(__file__).resolve().parent
PUBLIC_CERT_SHA = 'cd8efb3b155157cfcb6d9275ce521bc22373fa3da78a2df08ca502db57150a1a'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def scalar(value, word):
    for a, b in word:
        if (value >> a & 1) > (value >> b & 1):
            value ^= (1 << a) | (1 << b)
    return value


def columns(rows, n):
    return [sum(((y >> q) & 1) << x for x, y in enumerate(rows)) for q in range(n)]


def all_words(count, live, word=()):
    if not count:
        yield [list(g) for g in word]
    else:
        for a, b in combinations(live, 2):
            yield from all_words(count-1, tuple(q for q in live if q != a), word+((a, b),))


def inspect(packet, parent):
    supplied = packet['mathematical']
    need(digest(supplied) == packet['whole_math_sha256'], 'whole packed packet digest differs')
    prefix = parent['literal_prefix']
    need(prefix == supplied['literal_prefix'] and supplied['dead_ports'] == list(DEAD), 'literal Q/support changed')
    phase = time.monotonic()
    import initial_ground as numeric_parent
    originals, initial, ground_assignments, early_checks = numeric_parent.initial_ground(
        prefix, parent['early_negative_first_gates'])
    print('FRESH_ORIGINAL_GROUND', ground_assignments, time.monotonic()-phase, flush=True)
    phase = time.monotonic()
    semigroup = reconstruct()
    need(semigroup == supplied['four_input_library'], 'whole separately reconstructed G catalogue differs')
    parents = [scalar(x, prefix) for x in range(8192)]
    reachable = sorted({sum(((y >> q) & 1) << j for j, q in enumerate(DEAD)) for y in parents})
    need(reachable == supplied['actual_reachable_Q_inputs'] and len(reachable) == 36, 'actual Q projection differs')
    unit_preimages = []
    for j, port in enumerate(DEAD):
        matches = [x for x, y in enumerate(parents)
                   if sum(((y >> q) & 1) << t for t, q in enumerate(DEAD)) == 1 << j]
        need(matches, 'actual Q projection lacks a labelled unit input')
        unit_preimages.append([port, min(matches), parents[min(matches)]])
    early = {tuple(w['gate']) for w in parent['early_negative_first_gates']}
    forests = []
    for i, word in enumerate(all_words(4, DEAD)):
        routed = [[r[3], r[4]] for r in originals['3H']]
        parts = {q: {q} for q in DEAD}
        stages = []
        for a, b in word:
            need(a in parts and b in parts and a < b, 'illegal live forest gate')
            for record in routed:
                tags, d = record
                hit = bool(tags & ((1 << a) | (1 << b)))
                if tags >> a & 1 and not tags >> b & 1:
                    tags ^= (1 << a) | (1 << b)
                record[:] = [tags, d + int(hit)]
            parts[b].update(parts.pop(a))
            envelope = {}
            for tags, d in routed:
                secondary = tags & ~6144
                need(tags & 6144 == 6144 and secondary.bit_count() == 1, 'wrong actual original HIGH tags')
                q = secondary.bit_length()-1
                envelope[q] = max(envelope.get(q, -1), d)
            need(set(envelope) == set(parts), 'actual original live-root partition differs')
            stages.append([[[q, d] for q, d in sorted(envelope.items())], sum(1 << d for d in envelope.values())])
        status = 'MASS_REJECTED' if any(s[1] > 32768 for s in stages) else (
                 'EARLY_PUBLIC_NEGATIVE' if tuple(word[0]) in early else 'RETAINED')
        forests.append({'id': i, 'word': word, 'stages': stages,
                        'components': [[q, sorted(p)] for q, p in sorted(parts.items())], 'status': status})
    need(forests == supplied['all2700_binary_forests'] and len(forests) == 2700,
         'every original-routed labelled forest or negative status differs')
    print('ALL2700_ACTUAL_ORIGINAL_FORESTS', time.monotonic()-phase, flush=True)
    phase = time.monotonic()
    libraries = [(g, [scalar(x, g['word']) for x in range(16)]) for g in semigroup['states']]
    groups, raw = {}, []
    for forest in forests:
        if forest['status'] != 'RETAINED':
            continue
        free = sorted(set(DEAD) - {q for q, p in forest['components']})
        free_local = [DEAD.index(q) for q in free]
        free_mask = sum(1 << j for j in free_local)
        local_word = [[DEAD.index(a), DEAD.index(b)] for a, b in forest['word']]
        base = [scalar(x, local_word) for x in range(64)]
        # Literal labelled substitution into four freed physical ports.
        # This is a row lookup, not a packed bit-column computation.
        projected = [(y & (63 ^ free_mask), sum(((y >> q) & 1) << j
                                                for j, q in enumerate(free_local)))
                     for y in (base[x] for x in reachable)]
        embedding = [sum(((x >> j) & 1) << q for j, q in enumerate(free_local)) for x in range(16)]
        for g, row_function in libraries:
            key = tuple(held | embedding[row_function[x]] for held, x in projected)
            word = forest['word'] + [[free[a], free[b]] for a, b in g['word']]
            if key not in groups:
                groups[key] = {'temporary_id': len(groups), 'word': word,
                               'forest_id': forest['id'], 'library_id': g['id'], 'raw_count': 0}
            group = groups[key]
            if (len(word), word) < (len(group['word']), group['word']):
                group.update(word=word, forest_id=forest['id'], library_id=g['id'])
            group['raw_count'] += 1
            raw.append([forest['id'], g['id'], group['temporary_id']])
    ordered = sorted(groups, key=lambda key: (len(groups[key]['word']), groups[key]['word']))
    classes, relabel, counts, unit_maps = [], {}, Counter(), []
    for state, key in enumerate(ordered):
        group = groups[key]
        relabel[group['temporary_id']] = state
        rows = [scalar(x, [[DEAD.index(a), DEAD.index(b)] for a, b in group['word']]) for x in range(64)]
        need(tuple(rows[x] for x in reachable) == key, 'entire scalar representative differs')
        forest = forests[group['forest_id']]
        leaf_roots = {leaf: q for q, leaves in forest['components'] for leaf in leaves}
        actual_unit_map = [rows[1 << j] for j in range(6)]
        expected_unit_map = [1 << DEAD.index(leaf_roots[q]) for q in DEAD]
        need(actual_unit_map == expected_unit_map and len(set(actual_unit_map)) == 2,
             'whole function does not recover the exact rooted two-component forest')
        unit_maps.append([state, actual_unit_map, forest['components']])
        entry = {'state_id': state, 'shortest_word': group['word'],
                 'representative_forest_id': group['forest_id'], 'representative_library_id': group['library_id'],
                 'full64_columns': columns(rows, 6), 'actual_Q_key': columns(key, 6),
                 'represented_raw_count': group['raw_count'], 'public10084_equal_prefix': None}
        counts['NEW_WHOLE_Q_FUNCTION'] += 1
        classes.append(entry)
    for entry in raw:
        entry[2] = relabel[entry[2]]
    need(raw == supplied['all_retained_raw_bindings'], 'every raw forest/G/class binding differs')
    need(classes == supplied['whole_Q_function_classes'], 'every whole function/class/minimum-length binding differs')
    need(dict(counts) == supplied['class_status_counts'], 'parent comparison status differs')
    expected_packet_math = {'literal_prefix': prefix, 'dead_ports': list(DEAD),
            'actual_reachable_Q_inputs': reachable, 'four_input_library': semigroup,
            'all2700_binary_forests': forests, 'all_retained_raw_bindings': raw,
            'whole_Q_function_classes': classes, 'class_status_counts': dict(counts),
            'complete_preparation_word_cover': True,
            'four_binary_exclusion': False, 'unrestricted44_exclusion': False}

    def compare(packet):
        need(digest(packet['mathematical']) == packet['whole_math_sha256'], 'damaged storage hash')
        need(packet['mathematical'] == expected_packet_math, 'entire independently derived mathematical packet differs')

    compare(packet)
    rejected = []
    damage_names = ['omit_forest', 'wrong_original_HIGH_cost', 'wrong_forest_pruning',
                    'omit_raw_binding', 'wrong_raw_class', 'omit_function_class',
                    'wrong_minimum_word', 'wrong_reachable_projection', 'wrong_ordered_Q_function',
                    'invented_parent_reduction', 'unfinished_semigroup', 'wrong_generator_edge']
    for name in damage_names:
        damaged = copy.deepcopy(packet)
        m = damaged['mathematical']
        if name == 'omit_forest': m['all2700_binary_forests'].pop()
        elif name == 'wrong_original_HIGH_cost': m['all2700_binary_forests'][0]['stages'][0][0][0][1] += 1
        elif name == 'wrong_forest_pruning': m['all2700_binary_forests'][0]['status'] = 'RETAINED'
        elif name == 'omit_raw_binding': m['all_retained_raw_bindings'].pop()
        elif name == 'wrong_raw_class': m['all_retained_raw_bindings'][0][2] += 1
        elif name == 'omit_function_class': m['whole_Q_function_classes'].pop()
        elif name == 'wrong_minimum_word': m['whole_Q_function_classes'][0]['shortest_word'].append([4, 5])
        elif name == 'wrong_reachable_projection': m['actual_reachable_Q_inputs'].pop()
        elif name == 'wrong_ordered_Q_function': m['whole_Q_function_classes'][0]['actual_Q_key'][0] ^= 1
        elif name == 'invented_parent_reduction': m['whole_Q_function_classes'][0]['public10084_equal_prefix'] = {'state_id': 0}
        elif name == 'unfinished_semigroup': m['four_input_library']['queue_exhausted'] = False
        else: m['four_input_library']['all_edges'][0][2] = 0
        damaged['whole_math_sha256'] = digest(m)
        try:
            compare(damaged)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted actual semantic catalogue damage '+name)
    print('ALL111969_ROW_FUNCTION_BINDINGS', time.monotonic()-phase, flush=True)
    phase = time.monotonic()
    mask = sum(1 << q for q in DEAD)
    original_bindings = [(y & (8191 ^ mask), sum(((y >> q) & 1) << j for j, q in enumerate(DEAD))) for y in parents]
    physical = [sum(((x >> j) & 1) << q for j, q in enumerate(DEAD)) for x in range(64)]
    embeddings = []
    for entry in classes:
        word = [[DEAD.index(a), DEAD.index(b)] for a, b in entry['shortest_word']]
        rows = [scalar(x, word) for x in range(64)]
        entire = [held | physical[rows[x]] for held, x in original_bindings]
        embeddings.append([entry['state_id'], digest(entire)])
    print('ALL6400_WHOLE8192_INPUT_EMBEDDINGS', time.monotonic()-phase, flush=True)
    return {'fresh_original_ground_records': originals,
            'fresh_ground_assignments': ground_assignments, 'early_negative_original_checks': early_checks,
            'whole_four_input_semigroup_sha256': digest(semigroup),
            'all2700_actual_original_forest_sha256': digest(forests),
            'all111969_raw_scalar_binding_sha256': digest(raw),
            'all6400_scalar_class_binding_sha256': digest(classes),
            'whole13_embedding_hashes': embeddings, 'class_status_counts': dict(counts),
            'actual_unit_projection_preimages': unit_preimages,
            'all6400_exact_rooted_component_unit_maps': unit_maps,
            'independently_reconstructed_entire_producer_math_sha256': digest(expected_packet_math),
            'rejected_semantic_damages': rejected,
            'complete_four_binary_candidate_cover': True,
            'four_binary_exclusion': False, 'unrestricted44_exclusion': False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    started = time.monotonic()
    raw_parent = (PUBLIC / 'fixture.json').read_bytes()
    need(hashlib.sha256(raw_parent).hexdigest() == PUBLIC_CERT_SHA, 'credited parent certificate changed')
    math = inspect(json.loads(args.input.read_text()), json.loads(raw_parent))
    output = {'agent': 'six-sorting-2', 'role': 'researcher',
              'status': 'COMPLETE_SEPARATE_SCALAR_FOUR_BINARY_CANDIDATE_COVER_NOT_AN_EXCLUSION',
              'mathematical': math, 'whole_math_sha256': digest(math),
              'seconds': time.monotonic()-started,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(output, separators=(',', ':'))+'\n')
    print(json.dumps({'status': output['status'], 'whole_math_sha256': output['whole_math_sha256'],
                      'class_status_counts': math['class_status_counts'],
                      'whole_embeddings': len(math['whole13_embedding_hashes']),
                      'seconds': output['seconds'], 'rss_kib': output['maximum_rss_kib']}))


if __name__ == '__main__':
    main()
