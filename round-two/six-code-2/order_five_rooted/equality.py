"""Classify every size68 completion with a saturated C5-fixed point.

All three invariant cycle words must be included at size68. A complete
counting DAG partitions every exact nine-clique; positive leaves are fully
expanded and independently literal-checked, not just counted.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

from generate import encoded, need


def colors(domain, adjacency):
    classes = []
    while domain:
        available = domain
        color = 0
        while available:
            bit = available & -available
            v = bit.bit_length() - 1
            color |= bit
            domain ^= bit
            available ^= bit
            available &= ~adjacency[v]
        classes.append(color)
    return tuple(classes)


def literal(words):
    need(len(words) == len(set(words)) and all(0 <= w < 2 ** 18 and w.bit_count() == 5 for w in words), 'bad physical code')
    need(all((a & b).bit_count() <= 2 for a, b in combinations(words, 2)), 'physical code repeats triple')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--roots', type=Path, required=True)
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    need(not (args.work / 'RESULT.json').exists(), 'refuse completed equality evidence overwrite')
    begin = time.monotonic()
    data = json.loads(args.model.read_text())
    root = json.loads(args.roots.read_text())[args.seed]['words']
    fixed_words = sorted(r['words'][0] for r in data['invariant_one_word_orbits'])
    need(len(fixed_words) == 3, 'wrong invariant cycle-word inventory')
    prefix = sorted(root + fixed_words)
    literal(prefix)
    need(len(prefix) == 23, 'complete star overlaps invariant words')
    rows = [r for r in data['admissible_five_word_orbits']
            if all((a & b).bit_count() <= 2 for a in r['words'] for b in prefix)]
    occupied = [sum(1 << i for i in r['resources']) for r in rows]
    adjacency = tuple(sum(1 << j for j in range(len(rows)) if i != j and not used & occupied[j])
                      for i, used in enumerate(occupied))
    nodes, cache = [], {}
    explored = 0

    def count(domain, required):
        nonlocal explored
        explored += 1
        if time.monotonic() - begin > 60 or explored > 250000:
            (args.work / 'partial.json').write_bytes(encoded({'status': 'INCOMPLETE_NO_EQUALITY_COVERAGE',
                                                             'closed_nodes': len(nodes), 'explored_calls': explored}))
            raise TimeoutError('INCOMPLETE initial60s/250000-state exact equality guard')
        key = domain, required
        if key in cache:
            return cache[key]
        if required == 0:
            node = {'domain': domain, 'required': required, 'kind': 'positive', 'count': 1}
        elif domain.bit_count() < required:
            node = {'domain': domain, 'required': required, 'kind': 'cardinality', 'count': 0}
        else:
            partition = colors(domain, adjacency)
            if len(partition) < required:
                node = {'domain': domain, 'required': required, 'kind': 'proper_colors', 'classes': partition, 'count': 0}
            else:
                vertices = [i for i in range(len(rows)) if domain >> i & 1]
                v = max(vertices, key=lambda i: (adjacency[i] & domain).bit_count())
                bit = 1 << v
                a = count(domain ^ bit, required)
                b = count((domain ^ bit) & adjacency[v], required - 1)
                node = {'domain': domain, 'required': required, 'kind': 'split', 'vertex': v,
                        'without': a, 'with': b, 'count': nodes[a]['count'] + nodes[b]['count']}
        index = len(nodes)
        cache[key] = index
        nodes.append(node)
        return index

    root_node = count((1 << len(rows)) - 1, 9)
    positives = []

    def extract(index, selected):
        node = nodes[index]
        if not node['count']:
            return
        if node['kind'] == 'positive':
            need(len(selected) == 9, 'wrong terminal orbit count')
            words = sorted(prefix + [w for i in selected for w in rows[i]['words']])
            literal(words)
            need(len(words) == 68, 'wrong equality word count')
            support = sorted({p for p in range(18) for w in words if w >> p & 1})
            positives.append({'selected_orbits': sorted(selected), 'words': words, 'support': support,
                              'degrees': [sum(w >> p & 1 for w in words) for p in range(18)]})
        else:
            need(node['kind'] == 'split', 'positive count on a nonbranch exclusion leaf')
            extract(node['without'], selected)
            extract(node['with'], selected + (node['vertex'],))

    extract(root_node, ())
    positives.sort(key=lambda r: r['selected_orbits'])
    need(len(positives) == nodes[root_node]['count'] and
         len(positives) == len({tuple(r['words']) for r in positives}), 'count/positive equality inventory differs')
    graph_raw = encoded({'root_words': root, 'invariant_cycle_words': fixed_words,
                         'residual_orbits': [r['words'] for r in rows], 'adjacency': adjacency})
    proof_raw = encoded({'root_node': root_node, 'nodes': nodes})
    positive_raw = encoded(positives)
    (args.work / 'GRAPH.json').write_bytes(graph_raw)
    (args.work / 'COUNT_CERTIFICATE.json').write_bytes(proof_raw)
    (args.work / 'COMPLETIONS68.json').write_bytes(positive_raw)
    result = {'agent': 'six-code-2', 'role': 'researcher', 'status': 'COMPLETE_GENERATED_SATURATED_FIXED_POINT_68_EQUALITY_CENSUS',
              'seed_root_index': args.seed, 'prefix_words': len(prefix), 'vertices': len(rows),
              'edges': sum(a.bit_count() for a in adjacency) // 2, 'exact68_completions': len(positives),
              'support_size_histogram': sorted(Counter(len(r['support']) for r in positives).items()),
              'degree_profile_histogram': sorted(Counter(tuple(sorted(r['degrees'])) for r in positives).items()),
              'all_completions_omit_a_point': all(len(r['support']) == 17 for r in positives),
              'certificate_nodes': len(nodes), 'explored_calls': explored,
              'graph_sha256': hashlib.sha256(graph_raw).hexdigest(), 'certificate_sha256': hashlib.sha256(proof_raw).hexdigest(),
              'completions_sha256': hashlib.sha256(positive_raw).hexdigest(),
              'initial_whole_guard_seconds': 60, 'initial_node_guard': 250000,
              'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Every68 completion of the seedC5 saturated fixed-point star; transfer to all raw rooted stars requires actual cover. No no-saturated-fixed-point classification.'}
    (args.work / 'RESULT.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
