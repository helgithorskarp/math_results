"""Exact finite interface encoding around a pinned origin colour."""
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

GRAPH_HASH = '54a68876eb8c55d885905482b8373c5542651f7683bf66d4406ce44825563458'
TARGETS = [[24, 218], [24, 395], [25, 202]]


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < v < n
        adj[u].add(v); adj[v].add(u)
    return adj


def wheel_decomposition(n, edges, origin):
    adj = adjacency(n, edges)
    neighbors = adj[origin]
    rest = sorted(set(range(n)) - neighbors - {origin})
    left = set(neighbors)
    cycles = []
    while left:
        start = min(left)
        assert len(adj[start] & neighbors) == 2
        cycle = [start, min(adj[start] & neighbors)]
        while len(cycle) < 6:
            following = (adj[cycle[-1]] & neighbors) - {cycle[-2]}
            assert len(following) == 1
            cycle.append(next(iter(following)))
        assert len(set(cycle)) == 6 and set(cycle) <= left
        assert cycle[0] in adj[cycle[-1]]
        assert all(len(adj[v] & neighbors) == 2 for v in cycle)
        left -= set(cycle)
        cycles.append(cycle)
    return adj, rest, cycles


def encode(n, edges, origin, target=None):
    adj, rest, cycles = wheel_decomposition(n, edges, origin)
    states = [list(row) for row in product([1, 2, 3], repeat=6)
              if all(row[i] != row[(i+1) % 6] for i in range(6))]
    assert len(states) == 66
    index = {v: i for i, v in enumerate(rest)}
    bv = lambda v, c: 4*index[v]+c+1
    clauses = [[bv(v, c) for c in range(4)] for v in rest]
    clauses += [[-bv(u, c), -bv(v, c)] for u, v in edges
                if u in index and v in index for c in range(4)]
    variables = 4*len(rest)
    wheel_options = []
    if target is not None:
        assert len(target) == 2 and target[0] != target[1]
        assert sum(set(target) <= set(cycle) for cycle in cycles) == 1
    for cycle in cycles:
        rows = states
        if target is not None and set(target) <= set(cycle):
            a, b = map(cycle.index, target)
            rows = [row for row in states if row[a] == row[b]]
        options = []
        for row in rows:
            variables += 1
            options.append((variables, row))
            for v, color in zip(cycle, row):
                for u in sorted(adj[v] & set(rest)):
                    clauses.append([-variables, -bv(u, color)])
        clauses.append([v for v, row in options])
        wheel_options.append(options)
    return {'variables': variables, 'clauses': clauses, 'rest': rest,
            'cycles': cycles, 'options': wheel_options, 'origin': origin,
            'target': target}


def dimacs(instance):
    clauses = instance['clauses']
    return (f"p cnf {instance['variables']} {len(clauses)}\n" +
            ''.join(' '.join(map(str, row))+' 0\n' for row in clauses)).encode()


def lift_colouring(instance, colours):
    """Return a one-hot model if this graph colouring obeys the target."""
    assert colours[instance['origin']] == 0
    true = {4*i+colours[v]+1 for i, v in enumerate(instance['rest'])}
    for cycle, options in zip(instance['cycles'], instance['options']):
        matches = [var for var, row in options if row == [colours[v] for v in cycle]]
        if len(matches) != 1:
            return None
        true.add(matches[0])
    return true


def satisfies(clauses, true):
    return all(any((literal in true) if literal > 0 else (-literal not in true)
                   for literal in row) for row in clauses)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph-work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    raw = (args.graph_work / 'graph.json').read_bytes()
    assert sha256(raw).hexdigest() == GRAPH_HASH
    g = json.loads(raw)
    summaries = []
    for i, target in enumerate([None]+TARGETS):
        instance = encode(421, g['edges'], 210, target)
        cnf = dimacs(instance)
        filename = 'base.cnf' if target is None else f'q{i-1}.cnf'
        (args.out / filename).write_bytes(cnf)
        summaries.append({'target': target, 'variables': instance['variables'],
                          'clauses': len(instance['clauses']),
                          'states_per_cycle': [len(options) for options in instance['options']],
                          'filename': filename, 'bytes': len(cnf),
                          'sha256': sha256(cnf).hexdigest()})
    result = {'graph_sha256': GRAPH_HASH, 'vertices': 421, 'unit_edges': 1848,
              'origin': 210, 'rest_vertices': len(instance['rest']),
              'cycles': instance['cycles'], 'queries': summaries}
    (args.out / 'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
