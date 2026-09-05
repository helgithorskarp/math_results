"""Small exhaustive clique controls and malformed-certificate rejection."""
import argparse
import base64
import copy
import itertools
import json
from pathlib import Path
import generate
import verify


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    fixture_count = 0
    for n in range(6):
        pairs = list(itertools.combinations(range(n), 2))
        for code in range(1 << len(pairs)):
            edges = {edge for j, edge in enumerate(pairs) if (code >> j) & 1}
            rows = [sum(1 << v for v in range(n) if tuple(sorted((u, v))) in edges)
                    for u in range(n)]
            for color in (False, True):
                for k in range(6):
                    literal = [list(q) for q in itertools.combinations(range(n), k)
                               if all((edge in edges) == color for edge in itertools.combinations(q, 2))]
                    actual = verify.clique_list(rows if color else verify.complement(rows), k)
                    verify.need(actual == literal, 'small clique list control')
                    verify.need(generate.count(edges, n, k, color) == len(literal), 'producer small clique control')
                    fixture_count += 1
    doc = json.loads((generate.HERE / 'INPUT.json').read_text())
    result, graph, handoff = [json.loads((a.work / name).read_text()) for name in
                             ('result.json', 'GRAPH.json', 'HANDOFF.json')]
    verify.check(doc, result, graph, handoff)
    baseline = [doc, result, graph, handoff]
    rejected = []
    def bad(name, mutate, input_only=False):
        items = copy.deepcopy(baseline)
        mutate(items)
        calls = [('checker', lambda: verify.check(*items))]
        if input_only:
            calls.append(('producer', lambda: generate.decode(items[0])))
        for implementation, call in calls:
            try:
                call()
            except (ValueError, TypeError, KeyError):
                rejected.append(name + ':' + implementation)
            else:
                raise ValueError('accepted corruption: ' + name + ':' + implementation)
    bad('boolean_order', lambda x: x[0].update(n=True), True)
    bad('invalid_base64', lambda x: x[0].update(red_parent_graph6_base64='!'), True)
    raw = base64.b64decode(doc['red_parent_graph6_base64'])
    bad('truncated_graph6', lambda x: x[0].update(red_parent_graph6_base64=base64.b64encode(raw[:-1]).decode()), True)
    bad('graph6_padding', lambda x: x[0].update(red_parent_graph6_base64=base64.b64encode(raw[:-1] + bytes([raw[-1] + 1])).decode()), True)
    bad('duplicate_source_deletion', lambda x: x[0]['red_deletions'].__setitem__(5, x[0]['red_deletions'][0]), True)
    bad('reversed_source_deletion', lambda x: x[0]['red_deletions'].__setitem__(0, [12, 5]), True)
    bad('boolean_source_deletion', lambda x: x[0]['red_deletions'].__setitem__(0, [False, 5]), True)
    bad('source_deletion_out_of_range', lambda x: x[0]['red_deletions'].__setitem__(0, [0, 22]), True)
    bad('omitted_case', lambda x: x[1]['cases'].pop())
    bad('changed_case_count', lambda x: x[1]['cases'][0].update(blue_K5=99))
    bad('boolean_case_count', lambda x: x[1]['cases'][0].update(red_K4=False))
    obstruction_index = next(j for j, c in enumerate(result['cases']) if c['blue_K5'])
    bad('changed_obstruction', lambda x: x[1]['cases'][obstruction_index].update(first_blue_K5=[0]*5))
    bad('omitted_survivor', lambda x: x[1]['surviving_deletions'].pop())
    bad('changed_chosen_edge', lambda x: x[1].update(chosen_deletion=[0, 1]))
    bad('changed_scalar', lambda x: x[1].update(opposite_blue_edges=108))
    bad('missing_graph_edge', lambda x: x[2]['red_edges'].pop())
    bad('duplicate_graph_edge', lambda x: x[2]['red_edges'].append(x[2]['red_edges'][0]))
    bad('graph_loop', lambda x: x[2]['red_edges'].append([0, 0]))
    bad('boolean_graph_vertex', lambda x: x[2]['red_edges'].__setitem__(0, [False, 1]))
    bad('graph_vertex_out_of_range', lambda x: x[2]['red_edges'].append([0, 22]))
    bad('cross_debt', lambda x: x[3]['H20_required_cross_red_degrees'].__setitem__(0, 13))
    report = {'status': 'PASS', 'small_graph_orders': [0, 1, 2, 3, 4, 5],
              'small_graphs': 1100, 'complete_clique_list_comparisons': fixture_count,
              'malformed_records': 21, 'rejections': rejected}
    verify.need(fixture_count == 13200 and len(rejected) == 29, 'control coverage')
    a.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
