"""Compare the new ordered kernel with every labelled six-vertex graph.

six-code-2, researcher. A separate literal subset-edge-mask algorithm
supplies the full truth/count/witness oracle. No producer clique DFS.
Original60s/2M state budget, serial/native1/existing1CPU2GiB.
This validates an algorithm; the ordinary graph lemma remains unformalized.
"""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time
from physical_helpers import operations_guard

from audit_ordered import ordered_neighborhood_certificate, validate_simple_graph


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rejection(label, thunk, message):
    try:
        thunk()
    except ValueError as exc:
        need(str(exc) == message, 'wrong semantic rejection: ' + label)
        return {'control': label, 'rejected_for': str(exc)}
    raise ValueError('damaged input accepted: ' + label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    need(not args.work.exists(), 'fresh finite-check directory required')
    args.work.mkdir(parents=True)
    begin, states = time.monotonic(), 0

    def guard(stage):
        operations_guard()
        need(time.monotonic() - begin < 60, 'INCOMPLETE original60s finite ordered audit: ' + stage)
        need(states <= 2_000_000, 'INCOMPLETE original two-million finite ordered proof states')

    vertices, edges = tuple(range(6)), tuple(combinations(range(6), 2))
    edge_index = {pair: k for k, pair in enumerate(edges)}
    subsets = {k: [(vs, sum(1 << edge_index[pair] for pair in combinations(vs, 2)))
                   for vs in combinations(vertices, k)] for k in (3,4,5,6)}
    oracle_digest, ordered_digest = hashlib.sha256(), hashlib.sha256()
    totals = {k: 0 for k in (3,4,5,6)}
    positive_graphs, checked, positive_witnesses = 0, 0, 0
    literal_checks, ordered_rows, outer_edges, inner_edges = 0, 0, 0, 0

    def witness_ok(mask, witness):
        need(witness is not None and len(witness) == len(set(witness)) == 5 and
             all(type(v) is int and 0 <= v < 6 for v in witness) and
             all(mask & (1 << edge_index[tuple(sorted(pair))]) for pair in combinations(witness, 2)),
             'literal positive five-clique differs')

    def compare_counts(actual, expected):
        need(tuple(actual[k] for k in ('triangles','four_cliques','five_cliques')) == expected,
             'literal all-count record differs')

    for mask in range(1 << 15):
        graph = [set() for _ in vertices]
        for bit, (a,b) in enumerate(edges):
            if mask & (1 << bit):
                graph[a].add(b)
                graph[b].add(a)
        counts = {}
        for k in (3,4,5,6):
            counts[k] = sum(mask & required == required for _, required in subsets[k])
            literal_checks += len(subsets[k])
            totals[k] += counts[k]
        result = ordered_neighborhood_certificate(graph, guard, require_no_k5=False, trace=False)
        expected = (counts[3], counts[4], counts[5])
        compare_counts(result, expected)
        if counts[5]:
            witness_ok(mask, result['first_five'])
            positive_graphs += 1
            positive_witnesses += 1
        else:
            need(result['first_five'] is None, 'false positive five-clique witness')
            need(counts[6] == 0, 'literal noK5 implies noK6')
        checked += 1
        ordered_rows += result['vertices']
        outer_edges += result['outer_edge_tests']
        inner_edges += result['actual_inner_edge_tests']
        states = checked + literal_checks + ordered_rows + outer_edges + inner_edges
        line = json.dumps([mask, *expected], separators=(',',':')).encode() + b'\n'
        oracle_digest.update(line)
        line2 = json.dumps([mask, result['triangles'],result['four_cliques'],result['five_cliques']],
                           separators=(',',':')).encode() + b'\n'
        ordered_digest.update(line2)
        if mask % 256 == 0:
            guard('whole labelled six-vertex domain')

    need(checked == 32768 and literal_checks == 42 * 32768 and
         totals == {3:81920,4:7680,5:192,6:1} and positive_graphs == 172 and
         oracle_digest.hexdigest() == ordered_digest.hexdigest(), 'whole finite coverage/count totals')
    k5 = [set(range(5)) - {i} if i < 5 else set() for i in vertices]
    k6 = [set(vertices) - {i} for i in vertices]
    controls = []
    for label, graph in [('actual-isolated-K5-refutes-absence',k5),('actual-K6-refutes-absence',k6)]:
        controls.append(rejection(label,
            lambda graph=graph: ordered_neighborhood_certificate(graph,guard),
            'physical K5 refutes claimed upper4 caps'))
    bad = [set(row) for row in k5]; bad[1].remove(0)
    controls.append(rejection('one-direction-edge-damage',lambda:validate_simple_graph(bad),
                              'physical ordered graph symmetry'))
    self_bad = [set(row) for row in k5]; self_bad[0].add(0)
    controls.append(rejection('self-edge-damage',lambda:validate_simple_graph(self_bad),
                              'physical ordered graph self edge'))
    domain_bad = [set(row) for row in k5]; domain_bad[0].add(6)
    controls.append(rejection('out-of-domain-vertex',lambda:validate_simple_graph(domain_bad),
                              'physical ordered graph vertex domain'))
    positive = ordered_neighborhood_certificate(k5,guard,require_no_k5=False)
    altered = dict(positive); altered['five_cliques'] = 0
    controls.append(rejection('suppressed-positive-five-clique',lambda:compare_counts(altered,(10,5,1)),
                              'literal all-count record differs'))
    k5_mask = sum(1 << edge_index[pair] for pair in combinations(range(5),2))
    controls.append(rejection('distinct-positive-witness-nonedge',lambda:witness_ok(k5_mask,[0,1,2,3,5]),
                              'literal positive five-clique differs'))
    def check_coverage(value):
        need(value == 32768, 'whole finite labelled graph domain differs')
    controls.append(rejection('omitted-labelled-graph',lambda:check_coverage(checked-1),
                              'whole finite labelled graph domain differs'))
    states += len(controls) + positive['proof_states'] + 2 * 51
    guard('complete finite controls')
    result = {'agent':'six-code-2','role':'researcher',
        'status':'ALL_32768_LABELLED_SIX_VERTEX_GRAPHS_MATCH_LITERAL_CLIQUE_ORACLE',
        'vertices':6,'graphs':checked,'literal_subset_checks':literal_checks,
        'ordered_rows':ordered_rows,'actual_outer_edges':outer_edges,'actual_ordered_inner_edges':inner_edges,
        'clique_incidence_totals':{str(k):v for k,v in totals.items()},
        'graphs_with_K5':positive_graphs,'literal_positive_five_witnesses_checked':positive_witnesses,
        'literal_count_stream_sha256':oracle_digest.hexdigest(),
        'ordered_count_stream_sha256':ordered_digest.hexdigest(),
        'positive_controls':[{'name':'K5-plus-isolated-vertex','triangles':10,'four_cliques':5,'five_cliques':1},
                             {'name':'complete-K6','triangles':20,'four_cliques':15,'five_cliques':6}],
        'semantic_controls':controls,'proof_states':states,
        'original_seconds':60,'original_states':2000000,'formalized':False,
        'all_algorithms_same_author':True,'independent_person_review':'pending',
        'scope':'Algorithm validation only; physical case76 and the ordinary all-graph correctness bridge are separate.'}
    raw=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode()
    (args.work/'EXACT_RESULT.json').write_bytes(raw)
    execution={'seconds':time.monotonic()-begin,'peak_RSS_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'exact_result_sha256':hashlib.sha256(raw).hexdigest(),'exact_result_bytes':len(raw),
               'initial_seconds':60,'initial_states':2000000}
    (args.work/'EXECUTION.json').write_text(json.dumps(execution,sort_keys=True,indent=2)+'\n')
    print(json.dumps(execution,sort_keys=True))


if __name__ == '__main__':
    main()
