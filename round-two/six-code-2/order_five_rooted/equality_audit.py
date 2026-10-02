"""Check exact equality counts from physical candidates and a counting DAG.

No producer/search/solver import. The only shared helper is the independently
written physical checker. Every positive path is compared with the literal
inventory; counts are verified by induction through exact include/exclude
partitions, with no assumed zero from a solver status.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

from physical import encoded, full_model, mask, need, packing, points


def physical_graph(g, root, graph):
    packing(root, 20)
    long, short, physical = full_model(g)
    prefix = sorted(root + [ws[0] for ws in short])
    occupied = packing(prefix, 23)
    direct = {mask(ps) for ps in physical
              if all(len(ps & points(w)) <= 2 for w in prefix)}
    by_triples = {mask(ps) for ps in physical
                  if not any(t in occupied for t in combinations(sorted(ps), 3))}
    need(direct == by_triples, 'physical direct/triple candidate coverage differs')
    rows = [ws for ws in long if set(ws) <= direct]
    need(graph['root_words'] == root and
         graph['invariant_cycle_words'] == [ws[0] for ws in short] and
         graph['residual_orbits'] == list(map(list, rows)), 'missing or invented physical equality orbit')
    triples = [packing(ws, 5) for ws in rows]
    adjacency = tuple(sum(2 ** j for j, ts in enumerate(triples)
                          if i != j and not covered & ts) for i, covered in enumerate(triples))
    need(graph['adjacency'] == list(adjacency), 'wrong physical equality edge')
    return prefix, rows, adjacency, len(direct)


def count_dag(proof, adjacency):
    nodes = proof['nodes']
    full = 2 ** len(adjacency) - 1
    need(nodes and isinstance(proof['root_node'], int) and 0 <= proof['root_node'] < len(nodes), 'missing counting root')
    states = set()
    for index, n in enumerate(nodes):
        domain, target, count = n['domain'], n['required'], n['count']
        need(type(domain) is int and 0 <= domain <= full and type(target) is int and 0 <= target <= 9 and
             type(count) is int and count >= 0, 'invalid counting state/count')
        need((domain, target) not in states, 'duplicated counting state')
        states.add((domain, target))
        if n['kind'] == 'positive':
            need(target == 0 and count == 1, 'false empty-clique count')
        elif n['kind'] == 'cardinality':
            need(target > domain.bit_count() and count == 0, 'false cardinality exclusion count')
        elif n['kind'] == 'proper_colors':
            need(len(n['classes']) < target and count == 0, 'false proper-color exclusion count')
            covered = 0
            for color in n['classes']:
                need(type(color) is int and color > 0 and not color & ~domain and not color & covered,
                     'out-of-domain/overlapping/empty color class')
                covered |= color
                for v in range(len(adjacency)):
                    if color >> v & 1:
                        need(not adjacency[v] & color, 'color contains a physical compatibility edge')
            need(covered == domain, 'color leaf does not cover domain')
        elif n['kind'] == 'split':
            v, a, b = n['vertex'], n['without'], n['with']
            need(target > 0 and type(v) is int and 0 <= v < len(adjacency) and domain >> v & 1,
                 'invalid counting split vertex')
            need(type(a) is int and type(b) is int and 0 <= a < index and 0 <= b < index,
                 'nonpreceding counting children')
            need(nodes[a]['domain'] == domain ^ 2 ** v and nodes[a]['required'] == target,
                 'exclude child misses part of domain')
            need(nodes[b]['domain'] == (domain ^ 2 ** v) & adjacency[v] and nodes[b]['required'] == target - 1,
                 'include child misses physical neighborhood')
            need(count == nodes[a]['count'] + nodes[b]['count'], 'false branch count sum')
        else:
            raise ValueError('unknown counting node kind')
    root = nodes[proof['root_node']]
    need(root['domain'] == full and root['required'] == 9, 'count root misses full nine-clique target')
    reached = set()
    stack = [proof['root_node']]
    while stack:
        index = stack.pop()
        if index in reached:
            continue
        reached.add(index)
        if nodes[index]['kind'] == 'split':
            stack.extend((nodes[index]['without'], nodes[index]['with']))
    need(reached == set(range(len(nodes))), 'unreachable counting node')
    # This walk is separate from the producer's recursive positive extractor.
    positives = []
    stack = [(proof['root_node'], frozenset())]
    while stack:
        index, selected = stack.pop()
        n = nodes[index]
        if n['kind'] == 'positive':
            need(len(selected) == 9, 'positive path has wrong clique size')
            positives.append(tuple(sorted(selected)))
        elif n['kind'] == 'split':
            stack.append((n['without'], selected))
            stack.append((n['with'], selected | {n['vertex']}))
    need(len(positives) == len(set(positives)) == root['count'], 'positive coverage/count mismatch')
    for clique in positives:
        need(all(adjacency[a] >> b & 1 for a, b in combinations(clique, 2)), 'positive path is not a literal clique')
    return sorted(positives)


def inventory(records, cliques, prefix, rows):
    actual = []
    for clique in cliques:
        words = sorted(prefix + [w for i in clique for w in rows[i]])
        packing(words, 68)
        degrees = [sum(p in points(w) for w in words) for p in range(18)]
        actual.append({'selected_orbits': list(clique), 'words': words,
                       'support': [p for p in range(18) if degrees[p]], 'degrees': degrees})
    need(records == actual, 'omitted, duplicate or altered literal equality completion')
    return actual


def reject(test, value):
    try:
        test(value)
    except (ValueError, KeyError, IndexError):
        return
    raise ValueError('semantic equality damage accepted')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', type=Path, default=Path(__file__).parent / 'INSTANCE.json')
    parser.add_argument('--equality', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    need(not (args.work / 'AUDIT.json').exists(), 'refuse completed equality audit overwrite')
    begin = time.monotonic()
    fixture = json.loads(args.instance.read_text())
    g = fixture['permutation']
    need(sorted(g) == list(range(18)), 'wrong permutation')
    root = sorted(w for w in fixture['classical68_words'] if w & 1)
    raws = {name: (args.equality / name).read_bytes()
            for name in ('GRAPH.json', 'COUNT_CERTIFICATE.json', 'COMPLETIONS68.json')}
    graph, proof, records = (json.loads(raws[name]) for name in raws)
    prefix, rows, adjacency, allowed = physical_graph(g, root, graph)
    cliques = count_dag(proof, adjacency)
    actual = inventory(records, cliques, prefix, rows)
    damages = []
    broken = deepcopy(graph); broken['residual_orbits'].pop()
    reject(lambda value: physical_graph(g, root, value), broken); damages.append('omitted_physical_orbit')
    broken = deepcopy(graph); broken['adjacency'][0] ^= 2
    reject(lambda value: physical_graph(g, root, value), broken); damages.append('wrong_physical_edge')
    pi = next(i for i, n in enumerate(proof['nodes']) if n['kind'] == 'positive')
    broken = deepcopy(proof); broken['nodes'][pi]['count'] = 0
    reject(lambda value: count_dag(value, adjacency), broken); damages.append('wrong_empty_clique_count')
    si = next(i for i, n in enumerate(proof['nodes']) if n['kind'] == 'split')
    broken = deepcopy(proof); broken['nodes'][si]['count'] += 1
    reject(lambda value: count_dag(value, adjacency), broken); damages.append('wrong_branch_count')
    broken = deepcopy(proof); broken['nodes'][si]['with'] = broken['nodes'][si]['without']
    reject(lambda value: count_dag(value, adjacency), broken); damages.append('omitted_include_partition')
    ci = next(i for i, n in enumerate(proof['nodes']) if n['kind'] == 'proper_colors')
    broken = deepcopy(proof); broken['nodes'][ci]['classes'].pop()
    reject(lambda value: count_dag(value, adjacency), broken); damages.append('uncovered_color_leaf')
    broken = deepcopy(proof); broken['nodes'][proof['root_node']]['required'] = 8
    reject(lambda value: count_dag(value, adjacency), broken); damages.append('wrong_equality_target')
    broken = deepcopy(records); broken.pop()
    reject(lambda value: inventory(value, cliques, prefix, rows), broken); damages.append('omitted_positive')
    broken = deepcopy(records); broken[1] = deepcopy(broken[0])
    reject(lambda value: inventory(value, cliques, prefix, rows), broken); damages.append('duplicate_positive')
    broken = deepcopy(records); broken[0]['degrees'][0] -= 1
    reject(lambda value: inventory(value, cliques, prefix, rows), broken); damages.append('wrong_literal_degree')
    result = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'COMPLETE_INDEPENDENT_PHYSICAL_EQUALITY_COUNT_DAG_AND_POSITIVE_INVENTORY_AUDIT',
              'physical_candidate_universe': 8568, 'prefix_words': len(prefix), 'allowed_physical_words': allowed,
              'graph_vertices': len(rows), 'graph_edges': sum(a.bit_count() for a in adjacency) // 2,
              'verified_counting_nodes': len(proof['nodes']), 'verified_exact68_completions': len(actual),
              'node_kind_counts': dict(Counter(n['kind'] for n in proof['nodes'])),
              'support_size_histogram': sorted(Counter(len(r['support']) for r in actual).items()),
              'degree_profile_histogram': sorted(Counter(tuple(sorted(r['degrees'])) for r in actual).items()),
              'semantic_damage_rejections': damages, 'solver_used_or_trusted': False,
              'evidence': {name: {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
                           for name, raw in raws.items()},
              'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'All exact68 completions of the actual seed rooted20 star. Whole-root transfer is checked separately; no unsaturated-fixed-point or unrestricted-code classification.'}
    (args.work / 'AUDIT.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
