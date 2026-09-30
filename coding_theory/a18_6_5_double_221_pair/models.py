#!/usr/bin/env python3
"""Production integer models for the double(2,2,1) multiplicity-three case."""
from itertools import combinations, permutations, product
from pathlib import Path
import json
import hashlib
import subprocess
import time

ROOT=None
PAIRS=list(combinations(range(17),2))

def leave(shape):
    if shape == 0:
        edges = [(0, 1), (0, 2)]
        groups = [range(3, 8), range(8, 14), range(14, 17)]
    elif shape == 1:
        edges = [(0, 1), (1, 2)]
        groups = [range(3, 9), range(9, 14), range(14, 17)]
    elif shape == 2:
        edges = [(0, 2), (1, 2)]
        groups = [range(3, 9), range(9, 15), range(15, 17)]
    elif shape == 3:
        edges = [(0, 1), (0, 2), (1, 2), (15, 16)]
        groups = [range(3, 8), range(8, 13), range(13, 15)]
    else:
        raise ValueError('unknown marked shape')
    return frozenset(edges + [(v, z) for v, group in enumerate(groups) for z in group])


def matrix(shape):
    missing = leave(shape)
    target = [p for p in PAIRS if p not in missing]
    index = {p: i for i, p in enumerate(target)}
    rows = []
    for q in combinations(range(17), 4):
        six = list(combinations(q, 2))
        if not any(p in missing for p in six):
            rows.append((sum(1 << z for z in q), [index[p] for p in six]))
    rows.sort()
    if len(target) != 120 or len(rows) not in (1299, 1316, 1334):
        raise RuntimeError('unexpected mathematical input dimensions')
    return target, rows


def check_star(shape, words):
    sets = [frozenset(z for z in range(17) if w >> z & 1) for w in words]
    if len(sets) != 20 or len(set(sets)) != 20 or any(len(s) != 4 for s in sets):
        raise RuntimeError('wrong star size or word')
    if any(len(a & b) > 1 for a, b in combinations(sets, 2)):
        raise RuntimeError('repeated covered pair')
    covered = set().union(*(set(combinations(sorted(s), 2)) for s in sets))
    if frozenset(set(PAIRS) - covered) != leave(shape):
        raise RuntimeError('wrong reconstructed leave')
    reps = [sum(z in s for s in sets) for z in range(17)]
    if reps != [3, 3, 4] + [5] * 14:
        raise RuntimeError('wrong shortened replications')


def run_case(name, shape, fixed=()):
    target, rows = matrix(shape)
    row_map = dict(rows)
    columns = [k for w in fixed for k in row_map[w]]
    if len(set(columns)) != len(columns):
        raise RuntimeError('fixed rows overlap')
    inp = ROOT / (name + '.input')
    out = ROOT / (name + '.jsonl')
    inp.write_text('\n'.join([
        f'120 {len(rows)} 6',
        *(str(w) + ' ' + ' '.join(map(str, p)) for w, p in rows),
        '1', '0 ' + str(len(columns)) + ' ' + ' '.join(map(str, columns))
    ]) + '\n')
    started = time.monotonic()
    result = subprocess.run([str(ROOT / 'bitset'), str(inp), str(out)],
                            text=True, capture_output=True, timeout=20)
    report = dict(name=name, shape=shape, fixed=list(fixed), rows=len(rows),
                  seconds=round(time.monotonic() - started, 6), exit=result.returncode,
                  stdout=result.stdout.strip(), stderr=result.stderr.strip())
    if result.returncode == 0:
        data = json.loads(out.read_text())
        for cover in data['covers']:
            check_star(shape, list(fixed) + cover)
        report.update(status='COMPLETE', nodes=data['nodes'], covers=len(data['covers']),
                      output_sha256=hashlib.sha256(out.read_bytes()).hexdigest())
    elif 'INCOMPLETE' in result.stderr:
        report['status'] = 'INCOMPLETE; no exclusion or census'
    else:
        raise RuntimeError(report)
    return report




def vertices_permutations(parts):
    result = []
    for choice in product(*(list(permutations(p)) for p in parts)):
        mapping = dict(zip(sum(parts, ()), sum(choice, ())))
        result.append(tuple(mapping[v] for v in range(sum(map(len, parts)))))
    return result


def image(edges, mapping):
    return tuple(sorted(tuple(sorted((mapping[a], mapping[b]))) for a, b in edges))


def quotient(graphs, maps):
    domain = set(graphs)
    seen = set()
    reps = []
    for g in sorted(domain):
        if g in seen:
            continue
        orbit = {image(g, p) for p in maps}
        if not orbit <= domain or g != min(orbit):
            raise RuntimeError('invalid actual graph action or canonical representative')
        if orbit & seen:
            raise RuntimeError('orbit overlap')
        seen.update(orbit)
        reps.append((g, len(orbit)))
    if seen != domain:
        raise RuntimeError('missing graph orbit')
    return reps


def degree(edges, n):
    return [sum(v in e for e in edges) for v in range(n)]


def cubic_graphs():
    # Y=(0,1,2), A=(3,4), B=(5,6,7), degrees3 throughout.
    ya = list(product(range(3), range(3, 5)))
    yb = list(product(range(3), range(5, 8)))
    ab = list(product(range(3, 5), range(5, 8)))
    graphs = []
    for u in combinations(ya, 3):
        for v in combinations(yb, 6):
            d = degree(u + v, 8)
            if d[:3] != [3] * 3:
                continue
            for w in combinations(ab, 3):
                edges = tuple(sorted(u + v + w))
                if degree(edges, 8) == [3] * 8:
                    graphs.append(edges)
    return graphs, vertices_permutations(((0, 1, 2), (3, 4), (5, 6, 7)))


def triangle_graphs():
    # Low15 lies in high-blocksY0,A0,B0; low16 inY1,A1,B1.
    # Y0,Y1,Y2=0,1,2; A0,A1,A2=3,4,5; B0..B3=6..9.
    ya = [(y, a) for y in range(3) for a in range(3, 6)
          if (y, a) not in ((0, 3), (1, 4))]
    yb_neighbors = [(7, 8, 9), (6, 8, 9), (6, 7, 8, 9)]
    ab_neighbors = [(7, 8, 9), (6, 8, 9), (6, 7, 8, 9)]
    targets = [2, 2, 3, 2, 2, 3, 2, 2, 3, 3]
    graphs = []
    for first in combinations(ya, 2):
        first_d = degree(first, 10)
        yc = [list(combinations(yb_neighbors[y], targets[y] - first_d[y])) for y in range(3)]
        ac = [list(combinations(ab_neighbors[a], targets[a + 3] - first_d[a + 3])) for a in range(3)]
        for yn in product(*yc):
            yedges = tuple((y, b) for y, bs in enumerate(yn) for b in bs)
            current = degree(first + yedges, 10)
            if any(current[b] > targets[b] for b in range(6, 10)):
                continue
            for an in product(*ac):
                edges = tuple(sorted(first + yedges + tuple((a + 3, b) for a, bs in enumerate(an) for b in bs)))
                if degree(edges, 10) == targets:
                    graphs.append(edges)
    maps = []
    for swap_isolated, swap_free_b in product(range(2), repeat=2):
        p = list(range(10))
        if swap_isolated:
            for a, b in ((0, 1), (3, 4), (6, 7)):
                p[a], p[b] = p[b], p[a]
        if swap_free_b:
            p[8], p[9] = p[9], p[8]
        maps.append(tuple(p))
    return graphs, maps


def cubic_words(graph):
    rows = [{0} for _ in range(3)] + [{1} for _ in range(2)] + [{2} for _ in range(3)]
    buckets = [([e for e in graph if 3 <= e[0] < 5 and e[1] >= 5], range(5, 8)),
               ([e for e in graph if e[0] < 3 and e[1] >= 5], range(8, 14)),
               ([e for e in graph if e[0] < 3 and 3 <= e[1] < 5], range(14, 17))]
    for edges, labels in buckets:
        if len(edges) != len(labels):
            raise RuntimeError('wrong cubic edge class size')
        for edge, z in zip(edges, labels):
            for v in edge:
                rows[v].add(z)
    rows.append({1, 2, 3, 4})
    return sorted(sum(1 << z for z in row) for row in rows)


def triangle_words(graph):
    rows = [{0} for _ in range(3)] + [{1} for _ in range(3)] + [{2} for _ in range(4)]
    for z, endpoints in [(15, (0, 3, 6)), (16, (1, 4, 7))]:
        for v in endpoints:
            rows[v].add(z)
    buckets = [([e for e in graph if 3 <= e[0] < 6 and e[1] >= 6], range(3, 8)),
               ([e for e in graph if e[0] < 3 and e[1] >= 6], range(8, 13)),
               ([e for e in graph if e[0] < 3 and 3 <= e[1] < 6], range(13, 15))]
    for edges, labels in buckets:
        if len(edges) != len(labels):
            raise RuntimeError('wrong triangle edge class size')
        for edge, z in zip(edges, labels):
            for v in edge:
                rows[v].add(z)
    return sorted(sum(1 << z for z in row) for row in rows)


def shape1_words(words):
    labels = {0: 1, 1: 0, 2: 2}
    labels.update(zip(range(3, 8), range(9, 14)))
    labels.update(zip(range(8, 14), range(3, 9)))
    labels.update(zip(range(14, 17), range(14, 17)))
    return sorted(sum(1 << labels[z] for z in range(17) if w >> z & 1) for w in words)


def validate_fixed(shape, words):
    sets = [frozenset(z for z in range(17) if w >> z & 1) for w in words]
    if len(set(sets)) != len(sets) or any(len(q) != 4 or not q & {0, 1, 2} for q in sets):
        raise RuntimeError('invalid fixed high-block')
    if any(len(a & b) > 1 for a, b in combinations(sets, 2)):
        raise RuntimeError('fixed high-block pair conflict')
    covered = set().union(*(set(combinations(sorted(s), 2)) for s in sets))
    required = {p for p in PAIRS if p not in leave(shape) and p[0] < 3}
    if covered & leave(shape) or not required <= covered:
        raise RuntimeError('fixed high-blocks do not cover exactly the allowed high pairs')
    if [sum(v in s for s in sets) for v in range(3)] != [3, 3, 4]:
        raise RuntimeError('wrong high replication')




def transport(words,p):
    return tuple(sorted(sum(1<<p[z] for z in range(18) if w>>z&1) for w in words))


def automorphisms(star):
    common=[w for w in star if (w&7).bit_count()==2]
    if len(common)!=1:raise RuntimeError('expected exactly one high-pair block')
    low_common=[z for z in range(3,17) if common[0]>>z&1]
    groups=[[w for w in star if w>>h&1 and w!=common[0]] for h in range(3)]
    rows=sum(groups,[]);ranges=[];offset=0
    for g in groups:ranges.append(tuple(range(offset,offset+len(g))));offset+=len(g)
    if len(rows)!=8 or len(low_common)!=2:raise RuntimeError('wrong high-block incidence dimensions')
    edges={}
    for z in range(3,17):
        if z in low_common:continue
        edge=tuple(i for i,w in enumerate(rows) if w>>z&1)
        if len(edge)!=2 or edge in edges:raise RuntimeError('high-block incidence is not simple')
        edges[edge]=z
    results=[]
    for parts in product(*(list(permutations(r)) for r in ranges)):
        block_map=dict(zip(sum(ranges,()),sum(parts,())))
        if any(tuple(sorted(block_map[v] for v in e)) not in edges for e in edges):continue
        for swap in range(2):
            p=list(range(18))
            for e,z in edges.items():p[z]=edges[tuple(sorted(block_map[v] for v in e))]
            if swap:p[low_common[0]],p[low_common[1]]=p[low_common[1]],p[low_common[0]]
            if transport(star,p)==tuple(star):results.append(tuple(p))
    results=sorted(set(results))
    if not results or tuple(range(18)) not in results:raise RuntimeError('missing identity')
    maps=set(results)
    for p,q in product(results,repeat=2):
        if tuple(p[q[z]] for z in range(18)) not in maps:raise RuntimeError('not a permutation group')
    return results




def proper_color(active,adj):
    order=[];bounds=[];color=0
    remaining=active
    while remaining:
        color+=1;available=remaining
        while available:
            bit=available&-available;v=bit.bit_length()-1
            order.append(v);bounds.append(color)
            remaining^=bit
            available&=~bit;available&=~adj[v]
    return order,bounds


def maximum(adj):
    best=[];nodes=0;start=time.monotonic()
    def visit(active,chosen):
        nonlocal best,nodes
        nodes+=1
        if nodes>200000 or time.monotonic()-start>10:
            raise RuntimeError('INCOMPLETE residual maximum guard; no exclusion')
        if not active:
            if len(chosen)>len(best):best=chosen[:]
            return
        order,bounds=proper_color(active,adj)
        for i in range(len(order)-1,-1,-1):
            if len(chosen)+bounds[i]<=len(best):return
            v=order[i];bit=1<<v
            if not active&bit:raise RuntimeError('invalid coloring order')
            visit(active&adj[v],chosen+[v]);active^=bit
    visit((1<<len(adj))-1,[])
    if any(not(adj[a]>>b&1) for a,b in combinations(best,2)):
        raise RuntimeError('invalid clique witness')
    return best,nodes
