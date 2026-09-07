#!/usr/bin/env python3
"""Reproduce the compact proof from its explicit SAT seed words, without SAT."""
import argparse
import json
from collections import deque
from pathlib import Path
import native

HERE = Path(__file__).resolve().parent

def build():
    points, left = native.construction()
    hp = [points[v] for v in left]; label = {p: i for i, p in enumerate(hp)}
    edges, _ = native.exact_edges(hp)
    inverse = [label[tuple(-x for x in p)] for p in hp]
    terms = [label[(s*2*native.SCALE,)+(0,)*31] for s in (-1, 1)]
    return hp, edges, inverse, terms

def generate(source):
    hp, edges, inv, terms = build(); n = len(hp); a, b = terms
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    native.require(type(source.get('baseline')) is str and len(source['baseline']) == n and all(c in '0123' for c in source['baseline']), 'baseline format')
    native.require(all(source['baseline'][u] != source['baseline'][v] for u, v in edges), 'baseline colouring')
    seeds = [r for r in source['steps'] if r['kind'] == 'seed']
    seen = {}; queue = deque(); steps = []
    def insert(v, w, parent=None):
        if v in seen:
            return
        native.require(type(w) is str and len(w) == n and all(c in ('-' if u == v else '0123') for u, c in enumerate(w)) and w[a] != w[b], 'seed or derived support')
        native.require(all(w[u] != w[z] for u, z in edges if v not in (u, z)), 'invalid colouring')
        if parent is None:
            row = dict(kind='seed', deleted=v, word=w)
        else:
            row = dict(kind='patch', deleted=v, parent=parent,
                       changes=[[i, c] for i, c in enumerate(w) if c != seen[parent][i]])
        seen[v] = w; queue.append(v); steps.append(row)
        if inv[v] not in seen:
            vv = inv[v]; ww = ''.join(w[inv[x]] for x in range(n))
            seen[vv] = ww; queue.append(vv)
            steps.append(dict(kind='inversion', deleted=vv, parent=v))
    for row in seeds:
        insert(row['deleted'], row['word'])
    def variants(v, w):
        yield w
        for c in range(4):
            for d in range(c):
                palette = {str(c), str(d)}
                remaining = {u for u in range(n) if w[u] in palette}
                while remaining:
                    root = min(remaining); component = {root}; stack = [root]
                    remaining.remove(root)
                    while stack:
                        u = stack.pop()
                        for z in adj[u]:
                            if z in remaining:
                                remaining.remove(z); component.add(z); stack.append(z)
                    if not component.intersection(adj[v]):
                        continue
                    ww = list(w)
                    for u in component:
                        ww[u] = str(d) if w[u] == str(c) else str(c)
                    if ww[a] != ww[b]:
                        yield ''.join(ww)
    while queue:
        v = queue.popleft(); w = seen[v]
        for variant in variants(v, w):
            for c in '0123':
                vs = [u for u in adj[v] if variant[u] == c]
                if len(vs) == 1 and vs[0] not in terms:
                    u = vs[0]; ww = list(variant); ww[v] = c; ww[u] = '-'
                    insert(u, ''.join(ww), v)
            if len(seen)+2 >= 255:
                break
        if len(seen)+2 >= 255:
            break
    native.require(len(seen)+2 >= 255, 'seed set does not close target')
    return dict(version='degrey-terminal-cover-v1', target=508, terminals=terms,
                baseline=source['baseline'], steps=steps)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed-certificate', type=Path, default=HERE/'certificate.json')
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    output = generate(json.loads(args.seed_certificate.read_text()))
    args.out.write_text(json.dumps(output, separators=(',', ':'))+'\n')
    print(json.dumps(dict(steps=len(output['steps']), bytes=args.out.stat().st_size)))
