#!/usr/bin/env python3
"""Independent augmentation, target-side Hall closure, and exact bounded arrays.

Imports no primary-checker code. pynauty is used only by this second audit.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path
import subprocess
import tempfile
import numpy as np
import pynauty

HERE = Path(__file__).resolve().parent
PERMS = tuple(itertools.permutations(range(6)))


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def nauty(g: list[set[int]]):
    return pynauty.Graph(len(g), directed=True, adjacency_dict={i: sorted(r) for i, r in enumerate(g)})


def signature(g: list[set[int]]) -> bytes:
    return pynauty.certificate(nauty(g))


def enumerate_graphs() -> tuple[dict, list[int]]:
    graphs = [[set()]]
    counts = [1]
    for n in range(2, 7):
        unique = {}
        for old in graphs:
            for states in itertools.product(range(3), repeat=n-1):
                g = [r.copy() for r in old] + [set()]
                for i, state in enumerate(states):
                    if state == 1:
                        g[i].add(n-1)
                    elif state == 2:
                        g[n-1].add(i)
                unique.setdefault(signature(g), g)
        graphs = list(unique.values())
        counts.append(len(graphs))
    need(counts == [1,2,7,42,582,21480], 'augmentation counts')
    return unique, counts


def target_closures(g: list[set[int]], p: int) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    outside = set(range(6)) - g[p] - {p}
    neighborhoods = {u: g[u] & outside for u in g[p]}
    right = sorted(set().union(*neighborhoods.values()))
    choices = set()
    for k in range(len(right)+1):
        for values in itertools.combinations(right, k):
            target = set(values)
            source = {u for u, neighbors in neighborhoods.items() if neighbors <= target}
            if source:
                actual = set().union(*(neighborhoods[u] for u in source))
                choices.add((tuple(sorted(source)), tuple(sorted(actual))))
    return sorted(choices)


def parity(p: tuple[int, ...]) -> int:
    return (-1)**sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))


def known_cones(cert: dict) -> dict:
    known = {}
    for family in cert['types']:
        g = [{j for j in range(6) if row >> j & 1} for row in family['out']]
        records = []
        for cone in family['cones']:
            choices = []
            for p, mask in enumerate(cone['source']):
                source = {j for j in range(6) if mask >> j & 1}
                target = set().union(*(g[u] for u in source)) - g[p] - {p}
                need((tuple(sorted(source)), tuple(sorted(target))) in target_closures(g, p), 'uncertified source')
                need(sum(1 << j for j in target) == cone['target'][p], 'target disagreement')
                choices.append((source, target))
            a = [[int(j in src)-int(j in dst) for j in range(6)] for src, dst in choices]
            det = sum(parity(p) * math.prod(a[i][p[i]] for i in range(6)) for p in PERMS)
            need(det == -1, 'permutation determinant')
            inv = [[0]*6 for _ in range(6)]
            for i in range(6):
                for j in range(6):
                    minor = [[a[u][v] for v in range(6) if v != j] for u in range(6) if u != i]
                    cofactor = (-1)**(i+j) * sum(parity(p) * math.prod(minor[u][p[u]] for u in range(5))
                                               for p in itertools.permutations(range(5)))
                    inv[j][i] = -cofactor
            need(all(x >= 0 for row in inv for x in row), 'independent inverse positivity')
            need(all(sum(a[i][k]*inv[k][j] for k in range(6)) == int(i == j)
                     for i in range(6) for j in range(6)), 'cofactor inverse identity')
            w, dual = cone['weights'], cone['dual']
            need(all(type(x) is int and x > 0 for x in w+dual), 'positive data')
            need(all(sum(a[i][j]*w[j] for j in range(6)) == 1 for i in range(6)), 'independent primal check')
            need(all(sum(a[i][j]*dual[i] for i in range(6)) == 1 for j in range(6)), 'independent total dual check')
            records.append(tuple(tuple(sorted(src)) for src, _ in choices))
        known[signature(g)] = (g, records)
    return known


def transport_cones(g: list[set[int]], old: list[set[int]], records: list) -> set:
    mappings = [p for p in PERMS if all((j in old[i]) == (p[j] in g[p[i]])
                                      for i in range(6) for j in range(6))]
    need(bool(mappings), 'missing explicit isomorphism')
    results = set()
    for p in mappings:
        for row in records:
            target = [()] * 6
            for i, source in enumerate(row):
                target[p[i]] = tuple(sorted(p[j] for j in source))
            results.add(tuple(target))
    return results


def audit_orbits(graphs: dict) -> str:
    with tempfile.TemporaryDirectory(prefix='independent-six-oriented-') as tmp:
        binary = str(Path(tmp) / 'audit')
        subprocess.run(['g++','-std=c++20','-O3',str(HERE/'orbit_audit.cpp'),'-o',binary],check=True)
        text = subprocess.run([binary],check=True,text=True,capture_output=True).stdout
    found, covered = set(), 0
    pairs = list(itertools.combinations(range(6), 2))
    for line in text.splitlines():
        if not line.startswith('ORBIT '):
            continue
        _, code, orbit, chambers = line.split()
        value = int(code)
        g = [set() for _ in range(6)]
        for i, j in pairs:
            value, digit = divmod(value, 3)
            if digit == 1:
                g[i].add(j)
            elif digit == 2:
                g[j].add(i)
        need(value == 0, 'bad ternary code')
        key = signature(g)
        need(key in graphs and key not in found, 'orbit-set mismatch')
        found.add(key)
        _, mantissa, exponent, _, _ = pynauty.autgrp(nauty(g))
        order = int(mantissa * 10**exponent)
        need(order > 0 and 720 // order == int(orbit) and 720 % order == 0, 'orbit size disagreement')
        need(math.prod(len(target_closures(g, p)) for p in range(6)) == int(chambers), 'per-orbit Hall coverage disagreement')
        covered += int(orbit)
    need(found == set(graphs) and covered == 14348907, 'whole orbit partition mismatch')
    return hashlib.sha256(text.encode()).hexdigest()


def match(g: list[set[int]], v: int) -> int:
    left = sorted(g[v])
    right = set().union(*(g[u] for u in left)) - g[v] - {v}
    mates = {}
    def augment(u: int, seen: set[int]) -> bool:
        for t in sorted(g[u] & right):
            if t not in seen:
                seen.add(t)
                if t not in mates or augment(mates[t], seen):
                    mates[t] = u
                    return True
        return False
    return sum(augment(u, set()) for u in left)


def expanded_checks(cert: dict) -> list[dict]:
    results = []
    for family in cert['types']:
        cone = min(family['cones'], key=lambda r: sum(r['weights']))
        w, q = cone['weights'], family['out']
        labels = [i for i, size in enumerate(w) for _ in range(size)]
        for transitive in (False, True):
            g = [{j for j, b in enumerate(labels) if (i < j and transitive if a == b else q[a] >> b & 1)}
                 for i, a in enumerate(labels)]
            if family['name'] == 'missing_arc' and transitive:
                literal = (HERE/'oriented51.txt').read_text().splitlines()
                need(len(literal) == 51 and all(len(row) == 51 and set(row) <= {'0','1'} for row in literal),
                     'invalid literal 51-vertex graph')
                need(g == [{j for j, bit in enumerate(row) if bit == '1'} for row in literal],
                     'literal graph disagrees with independent expansion')
            profile = [[len(g[v]), match(g,v)] for v in range(len(g))]
            need(all(a > b for a,b in profile), 'expanded strong vertex')
            results.append({'family':family['name'],'transitive':transitive,'order':len(g),
                            'minimum_out_degree':min(len(row) for row in g),
                            'profile_sha256':hashlib.sha256(json.dumps(profile,separators=(',',':')).encode()).hexdigest()})
    return results


def main() -> None:
    cert = json.loads((HERE/'certificate.json').read_text())
    known = known_cones(cert)
    graphs, counts = enumerate_graphs()
    # Every integer array product has absolute value <= 6*4 = 24: int16 cannot overflow.
    binary = np.array([p for p in itertools.product(range(2),repeat=6) if any(p)], dtype=np.int16)
    rest = [p for p in itertools.product(range(4),repeat=6) if max(p)>1]
    rest += sorted(set(itertools.permutations((1,1,1,1,4,4))))
    rest = np.array(rest, dtype=np.int16)
    totals = Counter()
    for key, g in graphs.items():
        opts = [target_closures(g,p) for p in range(6)]
        if any(not row for row in opts):
            totals['zero_root'] += 1
            continue
        feasible = transport_cones(g,*known[key]) if key in known else set()
        witnessed = set()
        for selections in itertools.product(*opts):
            totals['systems'] += 1
            sources = tuple(r[0] for r in selections)
            if sources in feasible:
                witnessed.add(sources)
                totals['feasible'] += 1
                continue
            a = np.array([[int(j in src)-int(j in dst) for j in range(6)] for src,dst in selections],dtype=np.int16)
            if np.any(np.all(binary @ a <= 0,axis=1)) or np.any(np.all(rest @ a <= 0,axis=1)):
                totals['blocked'] += 1
            else:
                raise ValueError('Hall system lacks positive witness or exact multicover')
        need(witnessed == feasible, 'feasible cone completeness')
    need(dict(totals) == {'zero_root':13348,'systems':235526,'blocked':235506,'feasible':20}, 'independent classification totals')
    output = {'status':'INDEPENDENT ORIENTED-QUOTIENT CLASSIFICATION VERIFIED',
              'augmentation_counts':counts,'totals':dict(totals),
              'native_audit_sha256':audit_orbits(graphs), 'expanded_checks':expanded_checks(cert)}
    print(json.dumps(output,sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
