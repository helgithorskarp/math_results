#!/usr/bin/env python3
"""Deterministic complete-family fixtures and independent physical checks."""
import copy
import hashlib
import itertools
import json
from extract import extract, load_graph, clique
from verify import verify
from bounds import report, need


def fixture(m, t, seed, triangle=False, reverse=False):
    # Exact fixed 32-bit LCG, no claim of representative sampling.
    state = seed
    def bit():
        nonlocal state
        state = (1664525*state + 1013904223) % 2**32
        return state >> 31
    module = list(range(m))
    deleted = list(range(43-t, 43))
    uniform = {v: bit() for v in range(m, 43-t)}
    edges = []
    for u, v in itertools.combinations(range(43), 2):
        c = bit()
        if u < m <= v < 43-t:
            c = uniform[v]
        elif v < m and triangle:
            c = 1
        if bool(c) != reverse:
            edges.append([u, v])
    # A permutation makes labels irrelevant, while preserving explicit parts.
    perm = [(17*v + 5) % 43 for v in range(43)]
    return {'n': 43,
            'red_edges': sorted(sorted((perm[u],perm[v])) for u,v in edges),
            'module': sorted(perm[v] for v in module),
            'deleted': sorted(perm[v] for v in deleted)}


def rejected(call):
    try:
        call()
    except (ValueError, TypeError, KeyError):
        return
    raise ValueError('malformed object was accepted')


def triangle_fixture(reverse=False):
    # Five all-red contacts to a red triangle: all three degrees are >=18,
    # all relevant edge common counts <=13, but the triangle cap fails.
    signatures = [7]*5 + [0]*18 + [3]*5 + [5]*6 + [6]*6
    need(len(signatures) == 40)
    es = []
    for u,v in itertools.combinations(range(43),2):
        c = 1 if v < 3 else ((signatures[v-3] >> u & 1) if u < 3 else (u*v+u+v)%2)
        if bool(c) != reverse:
            es.append([u,v])
    return {'n':43,'red_edges':es,'module':[0,1,2],'deleted':list(range(26,43))}


def run():
    report()
    reasons = {}
    digest = hashlib.sha256()
    cases = [(2,7,False), (3,16,False), (3,17,True), (5,15,False),
             (13,15,False), (24,15,False), (25,7,False), (34,7,False)]
    for m,t,mono in cases:
        for seed in range(8):
            for reverse in (False, True):
                graph = fixture(m,t,seed,mono,reverse)
                certificate = extract(graph)
                verify(graph, certificate)
                reasons[certificate['reason']] = reasons.get(certificate['reason'],0)+1
                digest.update(json.dumps([graph,certificate],sort_keys=True).encode()+b'\n')
    for reverse in (False,True):
        g = triangle_fixture(reverse)
        c = extract(g)
        verify(g,c)
        need(c['reason'] == 'triangle_common')
        reasons[c['reason']] = reasons.get(c['reason'],0)+1
        digest.update(json.dumps([g,c],sort_keys=True).encode()+b'\n')

    # Check the recursive clique search against literal combinations on every
    # graph of order five, all clique sizes, and both physical colors.
    pairs = list(itertools.combinations(range(5),2))
    checks = 0
    for mask in range(1 << len(pairs)):
        for color in (0,1):
            rows = [0]*5
            for i,(u,v) in enumerate(pairs):
                if (mask >> i & 1) == color:
                    rows[u] |= 1 << v
                    rows[v] |= 1 << u
            for k in range(1,6):
                literal = [q for q in itertools.combinations(range(5),k)
                           if all(rows[u] >> v & 1 for u,v in itertools.combinations(q,2))]
                got = clique(rows,range(5),k)
                need((got is None) == (not literal))
                if got is not None:
                    need(tuple(got) in literal)
                checks += 1

    graph = fixture(2,7,3)
    certificate = extract(graph)
    mutations = []
    for field,value in [('n',42),('n',True),('module',[0,0]),
                        ('deleted',list(range(43))),('module',[True,2])]:
        g = copy.deepcopy(graph); g[field] = value; mutations.append(g)
    g = copy.deepcopy(graph); g['red_edges'] += [g['red_edges'][-1]]; mutations.append(g)
    g = copy.deepcopy(graph); g['red_edges'][0] = [0,43]; mutations.append(g)
    g = copy.deepcopy(graph); g['red_edges'][0] = [0,True]; mutations.append(g)
    # Wrong-family cases: excessive exception budget, and one broken cross pair.
    mutations.append(fixture(2,8,0))
    g = copy.deepcopy(graph)
    u = g['module'][0]
    v = next(v for v in range(43) if v not in g['module']+g['deleted'])
    pair = sorted((u,v))
    if pair in g['red_edges']: g['red_edges'].remove(pair)
    else: g['red_edges'].append(pair); g['red_edges'].sort()
    mutations.append(g)
    for g in mutations:
        rejected(lambda: load_graph(g))
    badcerts = []
    for field,value in [('color',True),('color',2),('vertices',[0]*5),
                        ('vertices',[0,1,2,3,43]),('vertices',[0,1,2,3,True])]:
        c = copy.deepcopy(certificate); c[field] = value; badcerts.append(c)
    c = copy.deepcopy(certificate); c['color'] ^= 1; badcerts.append(c)
    for c in badcerts:
        rejected(lambda: verify(graph,c))
    return {'status':'VERIFIED_MODULE_RESILIENCE_CONTROLS',
            'physical_family_graphs':130, 'physical_stream_sha256':digest.hexdigest(),
            'extractor_branches':reasons,'small_literal_clique_checks':checks,
            'rejected_inputs':len(mutations),'rejected_certificates':len(badcerts)}


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
