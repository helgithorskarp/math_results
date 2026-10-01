"""Generate two clique exclusions; no campaign source or certificate is imported."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def build(lengths):
    zeros = set()
    offset = 0
    for length in lengths:
        for i in range(length):
            zeros.update([(offset + i, offset + i),
                          (offset + i, offset + (i + 1) % length)])
        offset += length
    cells = [(i, j) for i in range(5) for j in range(5) if (i, j) not in zeros]
    # Producer chooses four rows and injects them into columns.
    vertex = {cell: i for i, cell in enumerate(cells)}
    columns = []
    for rows in itertools.combinations(range(5), 4):
        for image in itertools.permutations(range(5), 4):
            if all((r, c) in vertex for r, c in zip(rows, image)):
                columns.append(tuple(sorted(vertex[r, c] for r, c in zip(rows, image))))
    columns = sorted(set(columns))
    pair_id = {pair: i for i, pair in enumerate(itertools.combinations(range(15), 2))}
    masks = [sum(1 << pair_id[p] for p in itertools.combinations(c, 2)) for c in columns]
    adjacency = [sum(1 << j for j, n in enumerate(masks) if i != j and not m & n)
                 for i, m in enumerate(masks)]
    return cells, columns, adjacency


def prove(adjacency, target, node_cap=200000):
    nodes = 0

    def color(vertices):
        groups, order, bounds = [], [], []
        left = vertices
        while left:
            allowed, group = left, []
            while allowed:
                bit = allowed & -allowed
                v = bit.bit_length() - 1
                group.append(v)
                order.append(v)
                bounds.append(len(groups) + 1)
                left -= bit
                allowed -= bit
                allowed &= ~adjacency[v]
            groups.append(group)
        return groups, order, bounds

    def visit(vertices, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise RuntimeError('node guard reached; no exclusion')
        if len(chosen) == target:
            return None, chosen
        groups, order, bounds = color(vertices)
        branches = []
        for i in range(len(order) - 1, -1, -1):
            if len(chosen) + bounds[i] < target:
                # Proper colors are reconstructed by the independent verifier.
                return branches, None
            v = order[i]
            proof, witness = visit(vertices & adjacency[v], chosen + [v])
            if witness is not None:
                return None, witness
            branches.append([v, proof])
            vertices &= ~(1 << v)
        return branches, None

    proof, witness = visit((1 << len(adjacency)) - 1, [])
    return proof, witness, nodes


def produce():
    models = []
    for lengths in [(5,), (2, 3)]:
        cells, columns, adjacency = build(lengths)
        proof, witness, nodes = prove(adjacency, 10)
        if witness is not None:
            raise RuntimeError('ten-clique found; claimed theorem fails')
        _, nine, _ = prove(adjacency, 9)
        if nine is None:
            raise RuntimeError('missing sharp nine-clique control')
        models.append({'cycle_half_lengths': lengths,
                       'column_count': len(columns),
                       'column_sha256': hashlib.sha256(canonical(columns)).hexdigest(),
                       'proof': proof, 'proof_nodes': nodes, 'nine_clique': nine})
    return {'format': 'rebuild-color-branch-v1', 'target': 10, 'models': models}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    output = canonical(produce())
    if args.write:
        args.certificate.write_bytes(output)
    elif output != args.certificate.read_bytes():
        raise RuntimeError('certificate regeneration differs')
    print(json.dumps({'certificate_bytes': len(output), 'sha256': hashlib.sha256(output).hexdigest()}, sort_keys=True))
