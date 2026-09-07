#!/usr/bin/env python3
"""Check a compact colouring DAG and all resulting full-host deletion words."""
import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import exact as ex

HERE = Path(__file__).resolve().parent

def need(test, message):
    if not test:
        raise ValueError(message)

def integer(x, lo, hi, message):
    need(type(x) is int and lo <= x < hi, message)
    return x

def geometry(path):
    points, left, right = ex.construct(path)
    edges, survivors = ex.edges(points)
    L, R = set(left), set(right); local = {v:i for i,v in enumerate(left)}
    need(len(points)==1441 and len(left)==len(right)==721, 'orders')
    need(points[left[0]]==(-96,)+(0,)*15 and points[left[1]]==(96,)+(0,)*15, 'terminals')
    need(L&R=={left[0]} and left[0]==right[0], 'shared anchor')
    need(L|R==set(range(len(points))), 'union')
    he=sorted(tuple(sorted((local[u],local[v]))) for u,v in edges if u in L and v in L)
    le={tuple(sorted((left[u],left[v]))) for u,v in he}
    re={tuple(sorted((right[u],right[v]))) for u,v in he}
    need(re=={e for e in edges if e[0]in R and e[1]in R}, 'half isometry')
    bridge=tuple(sorted((left[1],right[1])))
    need(set(edges)-le-re=={bridge} and le.isdisjoint(re), 'unique bridge')
    hp=[points[v] for v in left]; ids={p:i for i,p in enumerate(hp)}
    current=hp; rotations=[]
    for k in range(6):
        perm=[ids[p] for p in current]
        need({tuple(sorted((perm[u],perm[v]))) for u,v in he}==set(he), 'rotation automorphism')
        rotations.append(perm); following=[]
        for p in current:
            x,y=ex.unpack(p); c={1:F(1,2)}; s={3:F(1,2)}
            following.append(ex.key((ex.add(ex.mul(c,x),ex.neg(ex.mul(s,y))),ex.add(ex.mul(s,x),ex.mul(c,y)))))
        current=following
    need(current==hp, 'rotation order')
    return dict(points=points,edges=edges,half_edges=he,left=left,right=right,
                inverse=rotations[3],rotations=rotations,terminals=[0,1],bridge=bridge,modular_survivors=survivors)

def check_word(word, n, edges, deleted=None, terminals=None):
    need(type(word) is str and len(word) == n, 'word length')
    need(all(c in ('-' if v == deleted else '0123') for v, c in enumerate(word)), 'word support or colour')
    if terminals is not None:
        a, b = terminals
        need(deleted not in terminals and word[a] != word[b], 'terminal separation')
    count = 0
    for u, v in edges:
        if u != deleted and v != deleted:
            need(word[u] != word[v], 'monochromatic edge')
            count += 1
    return count

def decode(cert, g):
    n = len(g['left']); terms = g['terminals']; inv = g['inverse']
    need(cert.get('version') == 'heule-t721-spindle-cover-v1', 'version')
    need(type(cert.get('target')) is int and cert['target'] == 508, 'target')
    need(cert.get('terminals') == terms and all(type(v) is int for v in cert['terminals']), 'terminals')
    baseline = cert.get('baseline')
    checks = check_word(baseline, n, g['half_edges'])
    steps = cert.get('steps'); need(type(steps) is list, 'steps list')
    words = {}; kinds = Counter()
    for row in steps:
        need(type(row) is dict, 'step object')
        v = integer(row.get('deleted'), 0, n, 'deleted label')
        need(v not in words and v not in terms, 'duplicate or terminal deletion')
        kind = row.get('kind')
        if kind == 'seed':
            need(set(row) == {'kind', 'deleted', 'word'}, 'seed fields')
            word = row['word']
        else:
            p = integer(row.get('parent'), 0, n, 'parent label')
            need(p in words, 'parent precedes child')
            if kind == 'rotation':
                need(set(row)=={'kind','deleted','parent','power'}, 'rotation fields')
                k=integer(row.get('power'),1,6,'rotation power'); perm=g['rotations'][k]
                need(v==perm[p], 'rotation deletion')
                word=''.join(words[p][perm.index(u)] for u in range(n))
            elif kind == 'patch':
                need(set(row) == {'kind', 'deleted', 'parent', 'changes'}, 'patch fields')
                changes = row['changes']; need(type(changes) is list and changes, 'patch list')
                word = list(words[p]); changed = set()
                for item in changes:
                    need(type(item) is list and len(item) == 2, 'patch item')
                    u = integer(item[0], 0, n, 'patch label'); c = item[1]
                    need(u not in changed and type(c) is str and len(c) == 1 and c in '-0123', 'patch colour or duplicate')
                    need(word[u] != c, 'redundant patch')
                    changed.add(u); word[u] = c
                word = ''.join(word)
            else:
                raise ValueError('step kind')
        checks += check_word(word, n, g['half_edges'], v, terms)
        words[v] = word; kinds[kind] += 1
    return baseline, words, checks, dict(sorted(kinds.items()))

def paste(g, left_word, right_word, deleted):
    """Enumerate the 24 palette maps and check the whole induced host directly."""
    n = len(g['points']); a, b = g['terminals']
    for perm in permutations('0123'):
        if g['left'][a] != deleted and left_word[a] != perm[int(right_word[a])]:
            continue
        if deleted not in g['bridge'] and left_word[b] == perm[int(right_word[b])]:
            continue
        word = ['-']*n
        for side, mapping in ((left_word, g['left']), (right_word, g['right'])):
            for v, global_v in enumerate(mapping):
                if global_v == deleted:
                    continue
                c = side[v] if mapping is g['left'] else perm[int(side[v])]
                need(word[global_v] in ('-', c), 'shared colour conflict')
                word[global_v] = c
        word = ''.join(word)
        check_word(word, n, g['edges'], deleted)
        return word
    raise ValueError('no palette gluing')

def full_cover(cert, g, require_target=True):
    baseline, half_words, local_checks, kinds = decode(cert, g)
    a, b = g['terminals']; mandatory_half = sorted({a, b} | set(half_words))
    M = sorted({side[v] for side in (g['left'], g['right']) for v in mandatory_half})
    need(len(M) == 2*len(mandatory_half)-1, 'mandatory overlap count')
    degree = Counter(v for e in g['edges'] for v in e)
    colour_hash = hashlib.sha256(); global_checks = 0
    for deleted in M:
        lw = rw = baseline
        if deleted not in {g['left'][a], g['left'][b], g['right'][b]}:
            if deleted in g['left']:
                lw = half_words[g['left'].index(deleted)]
            else:
                rw = half_words[g['right'].index(deleted)]
        word = paste(g, lw, rw, deleted)
        global_checks += len(g['edges']) - degree[deleted]
        colour_hash.update(f'{deleted} {word}\n'.encode())
    if require_target:
        need(len(M) > 508, 'target coverage not reached')
    return dict(verified=True, record_improvement=False, target=508,
                arbitrary_target_subsets_classified=len(M)>508,
                vertices=len(g['points']), edges=len(g['edges']),
                half_vertices=len(g['left']), half_edges=len(g['half_edges']),
                half_terminals=g['terminals'], shared_vertex=g['left'][a], bridge=list(g['bridge']),
                pair_checks=len(g['points'])*(len(g['points'])-1)//2,
                modular_survivors=g['modular_survivors'],
                half_omission_words=len(half_words), required_half_vertices=len(mandatory_half),
                step_kinds=kinds, required_global_vertices=len(M),
                four_colourable_through=len(M)-1, half_edge_checks=local_checks,
                global_deletion_edge_checks=global_checks,
                global_word_sha256=colour_hash.hexdigest(), mandatory_global_vertices=M,
                coordinate_sha256=hashlib.sha256(''.join(' '.join(map(str,p))+'\n' for p in g['points']).encode()).hexdigest(),
                edge_sha256=hashlib.sha256(''.join(f'{u} {v}\n' for u,v in g['edges']).encode()).hexdigest())
