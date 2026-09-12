"""Pinned catalogue access and exhaustive, literal isomorphism destinations."""
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import gzip
import hashlib
import json
import urllib.request
from exchange import need
HERE = Path(__file__).resolve().parent


def adjacency(raw):
    raw = raw.strip(); n = raw[0]-63
    need(1 <= n <= 15 and len(raw) == 1+(n*(n-1)//2+5)//6, 'graph6 length')
    need(all(63 <= x <= 126 for x in raw), 'graph6 character')
    a = [[0]*n for _ in range(n)]; k = 0
    for v in range(1, n):
        for u in range(v):
            a[u][v] = a[v][u] = ((raw[1+k//6]-63) >> (5-k%6)) & 1
            k += 1
    return a


def pins():
    return json.loads((HERE.parent/'ramsey_r55_maximal_residual_domains/INPUTS.json').read_text())


def obtain(directory):
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    result = {}
    for pin in pins():
        path = directory/pin['file']
        if not path.exists():
            wire = urllib.request.urlopen(pin['url'], timeout=90).read()
            need(hashlib.sha256(wire).hexdigest() == pin['download_sha256'], 'download hash')
            path.write_bytes(gzip.decompress(wire) if pin['url'].endswith('.gz') else wire)
        raw = path.read_bytes()
        need(hashlib.sha256(raw).hexdigest() == pin['sha256'], 'catalogue hash')
        lines = raw.splitlines(); need(len(lines) == pin['count'], 'catalogue size')
        result[pin['order']] = lines
    return result


def isomorphism(source, destination):
    """Return destination-to-source bijection, or None, by complete backtracking."""
    n = len(source)
    ds, dt = list(map(sum, source)), list(map(sum, destination))
    if sorted(ds) != sorted(dt):
        return None
    # Exact local invariant, only pruning. Every branch with this invariant is kept.
    ks = [(ds[u], tuple(sorted(ds[v] for v in range(n) if source[u][v]))) for u in range(n)]
    kt = [(dt[u], tuple(sorted(dt[v] for v in range(n) if destination[u][v]))) for u in range(n)]
    if sorted(ks) != sorted(kt):
        return None
    mapping = {}; used = set()
    def visit():
        if len(mapping) == n:
            return [mapping[v] for v in range(n)]
        possibilities = []
        for v in range(n):
            if v in mapping:
                continue
            choices = [u for u in range(n) if u not in used and ks[u] == kt[v]
                       and all(source[u][mapping[w]] == destination[v][w] for w in mapping)]
            if not choices:
                return None
            possibilities.append((len(choices), v, choices))
        _, v, choices = min(possibilities)
        for u in choices:
            mapping[v] = u; used.add(u)
            answer = visit()
            if answer is not None:
                return answer
            used.remove(u); del mapping[v]
        return None
    answer = visit()
    if answer is not None:
        need(sorted(answer) == list(range(n)), 'isomorphism bijection')
        need(all(source[answer[u]][answer[v]] == destination[u][v] for u, v in combinations(range(n), 2)), 'literal isomorphism')
    return answer


class Lookup:
    def __init__(self, data):
        self.lines = obtain(data); self.index = {}
    def find(self, a, vertices):
        n = len(vertices)
        need(n in self.lines, 'catalogue order')
        core = [[a[u][v] for v in vertices] for u in vertices]
        key = tuple(sorted(map(sum, core)))
        if n not in self.index:
            index = defaultdict(list)
            for i, raw in enumerate(self.lines[n]):
                index[tuple(sorted(map(sum, adjacency(raw))))].append(i)
            self.index[n] = index
        for i in self.index[n].get(key, []):
            mapping = isomorphism(core, adjacency(self.lines[n][i]))
            if mapping is not None:
                return i, [vertices[v] for v in mapping]
        raise ValueError('no catalogue destination; completeness is an imported premise')
