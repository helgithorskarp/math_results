"""Exhaustive tiny-core inverse maps; generated binary tables stay in scratch."""
from array import array
from itertools import combinations, permutations
from pathlib import Path
import argparse
import collections
import hashlib
import json
import time
from support import HERE, need, parents

SPECS = json.loads((HERE.parent / 'ramsey_r55_global_maximal_packing' / 'INPUTS.json').read_text())

def catalog(cache, n):
    parents()
    row = next(x for x in SPECS if x['n'] == n)
    raw = (Path(cache) / row['name']).read_bytes()
    need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
         'catalog identity')
    # Own graph6 parser, lexicographic physical pairs as output.
    result = []
    for line in raw.splitlines():
        need(len(line) == row['line_bytes'] - 1 and line[0] == n + 63, 'catalog row')
        bits = ''.join(format(c - 63, '06b') for c in line[1:])
        need(set(bits[n*(n-1)//2:]) <= {'0'}, 'graph6 padding')
        edges = {p for k, p in enumerate(( (i,j) for j in range(1,n) for i in range(j)))
                 if bits[k] == '1'}
        result.append(sum(int(p in edges) << k for k, p in enumerate(combinations(range(n), 2))))
    need(len(result) == row['count'], 'catalog cardinality')
    return result

def build(cache, n, out):
    words = catalog(cache, n)
    pairs = list(combinations(range(n), 2))
    index = {p: k for k, p in enumerate(pairs)}
    perms = list(permutations(range(n)))
    # p maps catalogue positions to input positions, precisely the receiver direction.
    moves = [[1 << index[tuple(sorted((p[i], p[j])))] for i, j in pairs] for p in perms]
    owners = array('h', [-1]) * (1 << len(pairs))
    codes = array('H', [0]) * len(owners)
    need(owners.itemsize == codes.itemsize == 2, '16-bit array ABI')
    start = time.monotonic()
    for c, word in enumerate(words):
        occupied = [k for k in range(len(pairs)) if word >> k & 1]
        for pi, move in enumerate(moves):
            w = sum(move[k] for k in occupied)
            need(owners[w] in (-1, c), 'catalogue isomorphism collision')
            if owners[w] < 0:
                owners[w] = c
                codes[w] = pi
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    # Explicit little endian output, independent of host byte order.
    import sys
    if sys.byteorder != 'little':
        owners.byteswap(); codes.byteswap()
    (out / f'owners{n}.bin').write_bytes(owners.tobytes())
    (out / f'perms{n}.bin').write_bytes(codes.tobytes())
    if sys.byteorder != 'little':
        owners.byteswap(); codes.byteswap()
    hist = collections.Counter(owners)
    return {'n': n, 'catalog_records': len(words), 'labelled_inputs': len(owners),
            'accepted': len(owners) - hist[-1], 'rejected': hist[-1],
            'orbit_sizes': [hist[i] for i in range(len(words))],
            'owners_sha256': hashlib.sha256((out / f'owners{n}.bin').read_bytes()).hexdigest(),
            'perms_sha256': hashlib.sha256((out / f'perms{n}.bin').read_bytes()).hexdigest(),
            'seconds': time.monotonic() - start}

class Lookup:
    def __init__(self, cache, tables):
        import sys
        self.words = {}; self.owners = {}; self.codes = {}; self.perms = {}
        for n in (3, 7):
            self.words[n] = catalog(cache, n)
            self.perms[n] = list(permutations(range(n)))
            owners = array('h'); codes = array('H')
            owners.frombytes((Path(tables) / f'owners{n}.bin').read_bytes())
            codes.frombytes((Path(tables) / f'perms{n}.bin').read_bytes())
            if sys.byteorder != 'little': owners.byteswap(); codes.byteswap()
            need(len(owners) == len(codes) == 1 << (n*(n-1)//2), 'lookup dimensions')
            self.owners[n] = owners; self.codes[n] = codes

    def find(self, a, core):
        n = len(core)
        need(n in (3, 7), 'destination core order')
        word = sum(a[core[i]][core[j]] << k for k, (i,j) in enumerate(combinations(range(n), 2)))
        c = self.owners[n][word]
        need(0 <= c < len(self.words[n]), 'core absent from catalogue')
        pi = self.codes[n][word]
        need(pi < len(self.perms[n]), 'permutation code')
        order = [core[i] for i in self.perms[n][pi]]
        # Never trust a loaded table as an unchecked certificate.
        target = sum(a[order[i]][order[j]] << k for k, (i,j) in enumerate(combinations(range(n), 2)))
        need(target == self.words[n][c], 'core isomorphism certificate')
        return c, order

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('cache'); p.add_argument('out'); args = p.parse_args()
    result = [build(args.cache, n, args.out) for n in (3, 7)]
    Path(args.out, 'LOOKUP.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps([{k:v for k,v in x.items() if k != 'orbit_sizes'} for x in result]))
