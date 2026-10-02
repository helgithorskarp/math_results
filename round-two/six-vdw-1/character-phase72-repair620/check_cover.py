"""Independent vertex-constraint inclusion/exclusion cover classifier.

Producer ORs edge-incidence columns over flat combinations; this checker
partitions binary vertex assignments and certifies whole pruned subdomains.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def classify(n, edges, size):
    need(1 <= size <= n, 'cardinality in physical domain')
    constraints = [sum(1 << (r - 1) for r in edge) for edge in edges if 1 not in edge]
    stats = {'nodes': 0, 'negative_volume': 0, 'positive_volume': 0,
             'empty_projection_prunes': 0, 'disjoint_projection_prunes': 0}

    def visit(position, left, unmet):
        remaining = n - position + 1
        if not 0 <= left <= remaining:
            return
        stats['nodes'] += 1
        need(stats['nodes'] <= 2000000, 'fixed two-million-node guard; incomplete evidence')
        volume = math.comb(remaining, left)
        if not unmet:
            stats['positive_volume'] += volume
            return
        if left == 0:
            stats['negative_volume'] += volume
            return
        future = ((1 << n) - 1) ^ ((1 << (position - 1)) - 1)
        projections = {edge & future for edge in unmet}
        if 0 in projections:
            stats['empty_projection_prunes'] += 1
            stats['negative_volume'] += volume
            return
        # Pairwise disjoint remaining supports each require a different vertex.
        packed = occupied = 0
        for support in sorted(projections, key=lambda x: (x.bit_count(), x)):
            if not (occupied & support):
                occupied |= support
                packed += 1
                if packed > left:
                    stats['disjoint_projection_prunes'] += 1
                    stats['negative_volume'] += volume
                    return
        vertex = 1 << (position - 1)
        visit(position + 1, left - 1, [edge for edge in unmet if not (edge & vertex)])
        visit(position + 1, left, unmet)

    visit(2, size - 1, constraints)
    expected = math.comb(n - 1, size - 1)
    need(stats['negative_volume'] + stats['positive_volume'] == expected,
         'entire weighted binary-assignment partition, no omitted or duplicate candidate')
    stats['candidate_domain_size'] = expected
    return stats


def check(hypergraph, record):
    need(hypergraph['mask'] == 72 and hypergraph['edge_sha256'] ==
         'b44cf8af4cbb78425f5bfc3c4b82c9e050fe57bb82e691200c6756b5241d4846', 'frozen audited hypergraph')
    need(record['schema'] == 'F31_PHASE72_NORMALIZED_COVER_PROPOSAL_V1'
         and record['mask'] == 72 and record['fixed_vertex'] == 1
         and record['edge_sha256'] == hypergraph['edge_sha256'], 'exact normalized cover problem')
    size = record['size']
    need(type(size) is int and 1 <= size <= 15, 'exact integral cover size')
    expected = math.comb(29, size - 1)
    need(record['candidate_domain_size'] == expected and 1 <= record['tested_count'] <= expected,
         'whole candidate domain and actual producer count')
    edges = hypergraph['edges']
    need(hashlib.sha256(json.dumps(edges, separators=(',', ':'), sort_keys=True).encode()).hexdigest()
         == hypergraph['edge_sha256'], 'whole audited edge input, not a self-reported hash')
    edge_set = {tuple(e) for e in edges}
    need(len(edge_set) == 240 and all(len(set(e)) == 7 and e == sorted(e)
                                    and all(1 <= r <= 30 for r in e) for e in edges), 'whole actual seven-uniform field domain')
    for scalar in range(1, 31):
        need({tuple(sorted(scalar * r % 31 for r in e)) for e in edges} == edge_set,
             'ENTIRE transitive scalar support action for normalized-cover bridge')
    witness = record['first_cover']
    if witness is not None:
        need(record['status'] == 'DIRECT_POSITIVE_COVER' and record['covers_found'] == 1,
             'positive evidence status')
        need(witness == sorted(set(witness)) and len(witness) == size and 1 in witness
             and all(type(r) is int and 1 <= r <= 30 for r in witness), 'literal30-vertex cover decoding')
        need(all(set(edge) & set(witness) for edge in edges), 'every actual bad support hit')
        return {'status': 'DIRECT_LITERAL_POSITIVE_COVER_CHECKED', 'size': size,
                'witness': witness, 'all_edges_checked': len(edges),
                'scope': 'Cover existence only; minimum needs complete smaller negatives and justified scalar reduction.'}
    need(record['status'] == 'COMPLETE_NO_NORMALIZED_COVER' and record['covers_found'] == 0
         and record['complete'] is True and record['tested_count'] == expected,
         'complete negative proposition, no partial producer coverage')
    stats = classify(30, edges, size)
    need(stats['positive_volume'] == 0 and stats['negative_volume'] == expected,
         'independent full binary-assignment no-cover classification')
    return {'status': 'COMPLETE_INDEPENDENT_NO_NORMALIZED_COVER', 'size': size,
            'all_domain_statistics': stats,
            'scope': 'All size-k covers containing1 excluded; actual transitive scalar automorphisms supply the whole-cover bridge.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hypergraph', type=Path)
    parser.add_argument('proposal', type=Path)
    args = parser.parse_args()
    result = check(json.loads(args.hypergraph.read_text()), json.loads(args.proposal.read_text()))
    result.update({'author': 'six-vdw-1', 'role': 'researcher'})
    print(json.dumps(result, sort_keys=True))
