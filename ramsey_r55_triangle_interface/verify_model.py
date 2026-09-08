"""Strict full-model decoder and physical good43 verifier for factored tasks."""
from itertools import combinations
from pathlib import Path
import argparse
import json
import factor


def parse(path):
    status = []; values = {}
    for line in Path(path).read_text().splitlines():
        if line.startswith('s '):
            status.append(line)
        elif line.startswith('v '):
            for word in line[2:].split():
                literal = int(word)
                if not literal:
                    continue
                variable = abs(literal); value = literal > 0
                if variable in values and values[variable] != value:
                    raise ValueError('conflicting assignment')
                values[variable] = value
    if status != ['s SATISFIABLE']:
        raise ValueError('exact SATISFIABLE status required')
    return values


def decode(task, values):
    plan = factor.plan(task); last = max(plan['variables'].values())
    if set(values) != set(range(1, last+1)) or any(type(x) is not bool for x in values.values()):
        raise ValueError('complete Boolean assignment required')
    for section, clause in factor.clauses(task, plan):
        if not any(values[abs(literal)] == (literal > 0) for literal in clause):
            raise ValueError('failed encoded clause in '+section)
    matrix = [[0]*43 for _ in range(43)]
    for u, v in task.edges:
        color = task.fixed[u, v] if (u, v) in task.fixed else int(values[task.variables[u, v]])
        matrix[u][v] = matrix[v][u] = color
    # Use the pinned parent's literal physical checker through the same verified loader.
    physical = factor.parent().graph(matrix)
    task.rank(physical)
    if not task.closure(physical):
        raise ValueError('red maximality failure')
    certificate = factor.parent().parent()['verify_target'].count(physical)
    if certificate['status'] != 'VERIFIED_GOOD43':
        raise ValueError('physical target rejected')
    return {'graph': physical, 'certificate': certificate, 'task': task.name}


def edge_list(graph):
    bits = int(graph['red_hex'], 16)
    return '43\n'+''.join(f'{u} {v}\n' for k, (u, v) in enumerate(combinations(range(43), 2))
                           if bits >> k & 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('cache', type=Path)
    parser.add_argument('--task', required=True); parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--graph-output', type=Path); parser.add_argument('--edge-output', type=Path)
    args = parser.parse_args(); family = factor.parent(); task = family.Task(args.task, args.cache)
    result = decode(task, parse(args.model))
    if args.graph_output:
        args.graph_output.write_text(json.dumps(result['graph'], sort_keys=True)+'\n')
    if args.edge_output:
        args.edge_output.write_text(edge_list(result['graph']))
    print(json.dumps(result, sort_keys=True))
