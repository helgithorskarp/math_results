#!/usr/bin/env python3
"""Malformed-certificate controls and explicit tests of the obstruction hypotheses."""
import argparse
import copy
from itertools import combinations
import json
from pathlib import Path
from verify import attachment_graph, attachments, certificate, classify, fixed_matrix, k5_free, need


def run(cover_path, source, report):
    cover = json.loads(cover_path.read_text())
    partition = json.loads((source/'classification.json').read_text())
    data = json.loads((source/'attachments.json').read_text())
    raw = (source/'packing.opb').read_text()
    cert = json.loads((source/'packing_certificate.json').read_text())
    rejected = []

    def reject(name, function):
        try:
            function()
        except (ValueError, TypeError, KeyError, IndexError):
            rejected.append(name)
        else:
            raise ValueError('accepted malformed input: '+name)

    missing = copy.deepcopy(partition)
    missing['excluded'].pop()
    reject('missing_excluded_core', lambda: classify(cover, missing))
    wrong = copy.deepcopy(partition)
    wrong['excluded'][0]['blue_k4'] = [0, 1, 2, 3]
    reject('wrong_blue_k4_witness', lambda: classify(cover, wrong))
    bad_patterns = copy.deepcopy(data)
    bad_patterns['blue_fixed_masks'].append(528)
    reject('extra_two_pair_attachment', lambda: attachments(bad_patterns))
    reject('wrong_packing_coefficient', lambda: certificate(raw.replace('-1 x1 ', '+1 x1 ', 1), cert))
    reject('missing_packing_row', lambda: certificate('\n'.join(raw.splitlines()[:-1])+'\n', cert))
    zero_weight = copy.deepcopy(cert)
    zero_weight['multipliers'][0] = 0
    reject('uncancelled_sum', lambda: certificate(raw, zero_weight))
    negative = copy.deepcopy(cert)
    negative['multipliers'][0] = -1
    reject('negative_multiplier', lambda: certificate(raw, negative))
    wrong_rhs = copy.deepcopy(cert)
    wrong_rhs['expected_rhs'] = 6
    reject('wrong_certificate_rhs', lambda: certificate(raw, wrong_rhs))

    fixed = fixed_matrix(0)
    def monochromatic(adj, vs, color):
        return all(adj[a][b] == color for a, b in combinations(vs, 2))
    # Two complementary pair neighbors force the four singleton vertices red to D.
    two_pairs = attachment_graph(fixed, 528)
    need(monochromatic(two_pairs, [0, 1, 2, 3, 10], True), 'two-pair red K5 witness')
    # A singleton intersecting a pair cannot share a blue-triangle neighborhood.
    intersection = attachment_graph(fixed, 17)
    need(monochromatic(intersection, [0, 4, 10, 11, 12], False), 'intersecting-signature blue K5 witness')
    need(k5_free(attachment_graph(fixed, 20)), 'valid disjoint singleton/pair attachment')
    # Removing the red singleton clique makes the row bound false locally.
    relaxed_fixed = copy.deepcopy(fixed)
    for a, b in combinations(range(4), 2):
        relaxed_fixed[a][b] = relaxed_fixed[b][a] = False
    need(k5_free(attachment_graph(relaxed_fixed, 528)), 'singleton-clique hypothesis control')

    # These are countermodels only to weakened incidence systems, not full graph models.
    one_demand = [[int(j == k) for k in range(6)] for j in range(7)]
    need(all(sum(row) <= 1 for row in one_demand) and
         all(sum(row[k] for row in one_demand) >= 1 for k in range(6)), 'weakened column witness')
    two_capacity = [[int(j in (k, k+1)) for k in range(6)] for j in range(7)]
    need(all(sum(row) <= 2 for row in two_capacity) and
         all(sum(row[k] for row in two_capacity) >= 2 for k in range(6)), 'weakened row witness')
    out = dict(rejected=rejected, literal_hypothesis_controls=4,
               weakened_column_witness=one_demand, weakened_row_witness=two_capacity)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(rejected=len(rejected), literal_hypothesis_controls=4)))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--cover', type=Path, default=Path(__file__).resolve().parent.parent/'ramsey_r55_order3_eleven_four_core/cover.json')
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    run(a.cover, a.source, a.report)
