#!/usr/bin/env python3
"""Finite arithmetic, boundary and malformed-evidence controls."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import tempfile
from verify import (adjacency, bipartite_or_cycle, certificate_rows, check_cycle,
                    digest, dump, geometry, mobius, ramanujan, require, verify)

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--proposal', type=Path, required=True)
    args = ap.parse_args()
    cert = json.loads((HERE / 'certificate.json').read_text())
    failures = []

    def reject(name, action):
        try:
            action()
        except (ValueError, KeyError) as e:
            failures.append({'case': name, 'reason': str(e)})
        else:
            raise ValueError('accepted corruption: ' + name)

    count = 0
    for n in range(1, 257):
        require(sum(mobius(d) for d in range(1, n + 1) if n % d == 0) == (n == 1),
                'Mobius divisor identity')
    for n in range(1, 37):
        r = ramanujan(n)
        for k in range(n):
            require(sum(r[j] * r[(k-j) % n] for j in range(n)) == n * r[k],
                    'Ramanujan convolution projector')
            count += 1
        points = {tuple(r[(i-k) % n] - r[(j-k) % n] for k in range(n))
                  for i in range(n) for j in range(n)}
        require(len(points) == (n * (n-1) if n % 2 else n*n//2) + 1,
                'boundary collision cardinality')
    require(geometry(1) == ([[0, 0]], []), 'singleton order')
    for length in (3, 4, 5, 6, 7, 8):
        edges = sorted([sorted([i, (i+1) % length]) for i in range(length)])
        adj = adjacency(length, edges)
        colour, cycle = bipartite_or_cycle(adj)
        require((cycle is None) == (length % 2 == 0), 'cycle parity fixture')
        if cycle is not None:
            check_cycle(adj, cycle)
    triangle = adjacency(3, [[0, 1], [0, 2], [1, 2]])
    reject('even alleged odd cycle', lambda: check_cycle(triangle, [0, 1]))
    reject('repeated odd cycle vertex', lambda: check_cycle(triangle, [0, 1, 0]))
    reject('nonedge in odd cycle', lambda: check_cycle(adjacency(3, [[0, 1], [1, 2]]), [0, 1, 2]))

    for name, mutate in [
        ('boolean version', lambda c: c.update(version=True)),
        ('wrong family', lambda c: c.update(family='other')),
        ('duplicate core key', lambda c: c['cores'].append(deepcopy(c['cores'][0]))),
        ('boolean key', lambda c: c['cores'][0].update(n=True)),
        ('nonternary word', lambda c: c['cores'][0].update(word='4')),
    ]:
        corrupted = deepcopy(cert)
        mutate(corrupted)
        reject(name, lambda c=corrupted: certificate_rows(c))
    first3 = next(i for i, c in enumerate(cert['cores']) if c['n'] == 3)
    for name, mutate in [
        ('missing core word', lambda c: c['cores'].pop(first3)),
        ('short core word', lambda c: c['cores'][first3].update(word='0')),
        ('monochromatic core', lambda c: c['cores'][first3].update(word='0' * 7)),
        ('wrong shell key', lambda c: c['cores'][first3].update(pair=[0, 999])),
    ]:
        corrupted = deepcopy(cert)
        mutate(corrupted)
        reject(name, lambda c=corrupted: verify(c, only_orders=[3]))

    original = json.loads((args.proposal / '3.json').read_text())
    for name, mutate in [
        ('missing point', lambda p: p['addresses'].pop()),
        ('wrong point coordinate', lambda p: p['coordinates'][0].__setitem__(0, 7)),
        ('missing scale', lambda p: p['cases'].pop()),
        ('missing shell edge', lambda p: p['cases'][0]['edges'].pop()),
        ('wrong squared distance', lambda p: p['cases'][0]['delta'].__setitem__(0, 999)),
        ('wrong chromatic number', lambda p: p['cases'][0].update(chi=4)),
        ('wrong positive proposal', lambda p: p['cases'][0].update(colour='0' * 7)),
    ]:
        corrupted = deepcopy(original)
        mutate(corrupted)
        with tempfile.TemporaryDirectory(prefix='hn-polygon-control-') as directory:
            path = Path(directory)
            (path / '3.json').write_text(dump(corrupted))
            reject(name, lambda: verify(cert, path, only_orders=[3]))
    report = {'verified': True, 'Mobius_controls': 256,
              'Ramanujan_projector_entries': count,
              'chord_cardinality_orders': 36, 'cycle_parity_fixtures': 6,
              'rejected_faults': failures, 'rejection_count': len(failures),
              'certificate_sha256': digest(cert)}
    print(dump(report), end='')


if __name__ == '__main__':
    main()
