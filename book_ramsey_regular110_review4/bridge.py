#!/usr/bin/env python3
"""Independent literal signed controls for the regular Book incidence bridge.

Round-robin matching unions, two disjoint cliques, and a crown graph are
implementation controls, not valid Ramsey witnesses or a host census.
"""
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path


def require(value, text):
    if not value:
        raise ValueError(text)


def encode(x):
    return (json.dumps(x, sort_keys=True, separators=(',', ':'))+'\n').encode()


def from_edges(edges):
    red = [set() for _ in range(22)]
    for i, j in edges:
        require(i != j and j not in red[i], 'simple distinct control edges')
        red[i].add(j)
        red[j].add(i)
    require(list(map(len, red)) == [10]*22, 'literal ten-regular control')
    return red


def controls():
    out = []
    for seed, step in enumerate((1, 2, 4, 5, 8, 10)):
        edges = []
        for k in range(10):
            round_ = (2*seed+step*k) % 21
            edges.append((21, round_))
            edges.extend(((round_+q) % 21, (round_-q) % 21) for q in range(1, 11))
        out.append(from_edges(edges))
    out.append(from_edges([(i, j) for i, j in combinations(range(22), 2)
                           if (i < 11) == (j < 11)]))
    out.append(from_edges([(i, 11+j) for i in range(11) for j in range(11) if i != j]))
    return out


def run():
    stream = hashlib.sha256()
    paired = 0
    for index, red in enumerate(controls()):
        blue = [set(range(22))-{i}-red[i] for i in range(22)]
        F = [[0]*22 for _ in range(22)]
        for i, j in combinations(range(22), 2):
            f = 3-len(red[i] & red[j]) if j in red[i] else 6-len(blue[i] & blue[j])
            F[i][j] = F[j][i] = f
        require(list(map(sum, F)) == [6]*22, 'signed full defect row six')
        K = [[2*int(j in red[i])+3*int(i == j) for j in range(22)] for i in range(22)]
        require([[sum(a*b for a, b in zip(x, y)) for y in K] for x in K] ==
                [[25*int(i == j)+24-4*F[i][j] for j in range(22)] for i in range(22)],
                'full regular integer-square bridge')
        for v in range(22):
            A, B = sorted(red[v]), sorted(blue[v])
            h = [len(red[a] & red[v]) for a in A]
            J = [red[a] & red[v] for a in A]
            Z = [red[v]-red[b] for b in B]
            z = list(map(len, Z))
            t = [sum(a in row for row in Z) for a in A]
            require(t == [x+2 for x in h], 'column misses h+2')
            require(z == [len(red[b] & blue[v]) for b in B], 'outside degrees equal row sizes')
            require(sum(z) == sum(h)+20, 'total misses')
            eA = sum(h)//2
            eB = sum(len(red[b] & blue[v]) for b in B)//2
            require(eB == eA+10, 'outside edge budget')
            actual = [[sum(a in row and b in row for row in Z) for b in A] for a in A]
            E = [[0]*10 for _ in range(10)]
            for i, j in combinations(range(10), 2):
                a, b = A[i], A[j]
                slack = 3-len(red[a] & red[b]) if b in red[a] else 6-len(blue[a] & blue[b])
                E[i][j] = E[j][i] = slack
            base = [[h[i]+2 if i == j else h[i]+h[j]-(5 if A[j] in red[A[i]] else 2)
                     -len(J[i] & J[j]) for j in range(10)] for i in range(10)]
            require([[base[i][j]-E[i][j] for j in range(10)] for i in range(10)] == actual,
                    'every literal miss Gram entry')
            u = [sum(len(row)-4 for row in Z if a in row) for a in A]
            incident = [3*h[i]+sum(h)-24-sum(h[j] for j in range(10) if A[j] in J[i])-u[i]
                        for i in range(10)]
            require(incident == list(map(sum, E)), 'every signed incident slack equation')
            for i, x in enumerate(A):
                if h[i] != 0:
                    continue
                exceptional = [B[j] for j, row in enumerate(Z) if x in row]
                require(len(exceptional) == 2, 'isolated local point has two miss rows')
                p, q = exceptional
                C = set(B)-{p, q}
                eC = sum(len(red[c] & C) for c in C)//2
                k = z[B.index(p)]+z[B.index(q)]-2
                require(eC == eA+8-k+int(q in red[p]), 'literal paired-root edge identity')
                paired += 1
            stream.update(encode([index, v, h, t, z, E, actual]))
    return {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'signed_ten_regular_graphs': 8, 'root_controls': 176,
            'local_Gram_entries': 17600, 'local_spines': 7920,
            'incident_slack_identities': 1760, 'column_identities': 1760,
            'outside_degree_identities': 1936, 'paired_root_identities': paired,
            'global_square_entries': 3872, 'control_stream_sha256': stream.hexdigest(),
            'Ramsey_witnesses_claimed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = run()
    if args.check:
        require(encode(result) == encode(json.loads(args.check.read_text())), 'bridge expected mismatch')
    print(json.dumps(result, sort_keys=True, indent=2))
