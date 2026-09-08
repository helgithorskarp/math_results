"""Strict physical graph and full SAT-model checking; no solver success is assumed."""
from itertools import combinations
from pathlib import Path
import argparse
import json
import re
import sys
import compile as compiler


def graph_check(graph):
    if not isinstance(graph, dict) or set(graph) != {'n', 'red_hex'} or type(graph['n']) is not int or graph['n'] != 43:
        raise ValueError('exact good43 graph schema required')
    h = graph['red_hex']
    if not isinstance(h, str) or re.fullmatch('[0-9a-f]{226}', h) is None or int(h, 16) >= 2**903:
        raise ValueError('physical graph bits')
    bits = int(h, 16); red = [0]*43
    for k, (u, v) in enumerate(combinations(range(43), 2)):
        if bits >> k & 1:
            red[u] |= 1 << v; red[v] |= 1 << u
    counts = [0, 0]; first = None
    for q in combinations(range(43), 5):
        colors = {(red[u] >> v) & 1 for u, v in combinations(q, 2)}
        if len(colors) == 1:
            color = colors.pop(); counts[color] += 1
            if first is None:
                first = {'color': color, 'vertices': list(q)}
    return {'status': 'VERIFIED_GOOD43' if sum(counts) == 0 else 'REJECTED_MONOCHROMATIC_FIVE',
            'red_fives': counts[1], 'blue_fives': counts[0],
            'five_subsets_checked': 962598, 'first_violation': first}


def decode(values):
    model = compiler.Model()
    if set(values) != set(range(1, model.variables+1)) or any(type(x) is not bool for x in values.values()):
        raise ValueError('complete Boolean assignment required')
    selected = [i for i, z in enumerate(model.selectors) if values[z]]
    if len(selected) != 1 or not values[1] or (values[795] and not values[794]):
        raise ValueError('invalid selector or color assignment')
    graph = [[0]*43 for _ in range(43)]
    for u, v in combinations(range(43), 2):
        edge = model.edge(u, v, selected[0])
        color = edge if u >= 31 else int(values[edge])
        graph[u][v] = graph[v][u] = color
    for name, clauses in model.sections():
        for index, clause in enumerate(clauses):
            if not any(values[abs(x)] == (x > 0) for x in clause):
                raise ValueError(f'failed {name} clause {index}')
    bits = sum(graph[u][v] << k for k, (u, v) in enumerate(combinations(range(43), 2)))
    result = {'n': 43, 'red_hex': format(bits, '0226x')}
    verified = graph_check(result)
    if verified['status'] != 'VERIFIED_GOOD43':
        raise ValueError('physical target failure')
    return result, verified


def parse_model(path):
    values = {}; status = []
    for line in Path(path).read_text().splitlines():
        if line.startswith('s '):
            status.append(line)
        if line.startswith('v '):
            for token in line.split()[1:]:
                literal = int(token)
                if literal == 0:
                    continue
                if abs(literal) in values and values[abs(literal)] != (literal > 0):
                    raise ValueError('conflicting assignment')
                values[abs(literal)] = literal > 0
    if status != ['s SATISFIABLE']:
        raise ValueError('exact SATISFIABLE status required')
    return values


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--graph', type=Path); p.add_argument('--model', type=Path)
    a = p.parse_args()
    if a.graph:
        result = graph_check(json.loads(a.graph.read_text()))
    elif a.model:
        graph, checked = decode(parse_model(a.model)); result = {'graph': graph, 'verification': checked}
    else:
        p.error('supply --graph or --model')
    print(json.dumps(result, sort_keys=True))
    if a.graph and result['status'] != 'VERIFIED_GOOD43':
        sys.exit(1)
