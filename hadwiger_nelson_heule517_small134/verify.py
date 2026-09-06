#!/usr/bin/env python3
"""Solver-free proof: reconstruct exact geometry, check colours, cover omissions.

Does not import run.py, engine.py or a SAT solver.  The independent monomial
geometry implementation from the joint-interface artifact is hash-pinned.
"""
import argparse
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def require(ok, detail):
    if not ok: raise ValueError(detail)


def uncovered(free, cuts, k):
    """Complete finite cover, with explicit uncovered tuples for small frontiers."""
    pos = {v:i for i,v in enumerate(free)}
    masks = [sum(1 << pos[v] for v in d) for d in cuts]
    count = 0; residual = []
    for indices in combinations(range(len(free)), k):
        mask = sum(1 << i for i in indices); count += 1
        if not any(mask & d == d for d in masks):
            residual.append([free[i] for i in indices])
    return count, residual


def raw(n, clauses):
    return (f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()


def verify(work=None):
    start = time.monotonic()
    for name, digest in json.loads((HERE/'manifest.json').read_text()).items():
        require(sha256((REPO/name).read_bytes()).hexdigest() == digest, ('input hash', name))
    spec = importlib.util.spec_from_file_location('independent_geometry', REPO/'hadwiger_nelson_heule517_joint_interface/verify.py')
    geometry = importlib.util.module_from_spec(spec); spec.loader.exec_module(geometry)
    points, edges = geometry.graph()
    L = sorted(v for v,p in enumerate(points) if all(p[a][k] == 0 for a in (0,1) for k in (2,3,6,7)))
    S = sorted(set(range(517))-set(L)); ss = set(S)
    require(len(L) == 375 and len(S) == 142 and len(edges) == 2555, 'exact graph counts')
    initial = json.loads((REPO/'hadwiger_nelson_heule517_small_pilot/certificate.json').read_text())['rows']
    prior = json.loads((REPO/'hadwiger_nelson_heule517_family_pilot/certificate.json').read_text())['rows']
    profiles = json.loads((REPO/'hadwiger_nelson_heule517_joint_interface/certificate.json').read_text())['rows']
    union = json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
    labels = [v for v in range(553) if '510' in union['provenance'][v]]

    def decode(row):
        if row['kind'] == 'seed':
            r = prior[row['row']]; require(row['D'] == r['D'], 'old omitted set')
            if r['source'] == 'native': return r['colouring']
            if r['source'] == 'forced':
                D = [r['index']]; text = union['forced_witness'][str(r['index'])]
            else:
                require(r['source'] == 'family', 'old witness kind')
                old = union['family'][r['index']]; D = old['D']; text = old['witness']
            surviving = sorted(set(range(553))-set(D))
            require(len(text) == len(surviving), 'old witness length')
            colours = dict(zip(surviving, text))
            return ''.join(colours.get(v, '.') for v in labels)+r['extra']
        require(row['kind'] == 'case' and type(row['case']) is int and 0 <= row['case'] < 20, 'case identity')
        p = profiles[row['case']]
        require(len(p['colouring']) == 375 and len(row['colouring']) == 142, 'block witness lengths')
        out = ['.']*517
        for v,c in zip(L, p['colouring']): out[v] = c
        for v,c in zip(S, row['colouring']): out[v] = c
        return ''.join(out)

    def check(row):
        c = decode(row)
        require(len(c) == 517 and set(c) <= set('.0123'), 'colouring domain')
        D = [i for i,x in enumerate(c) if x == '.']
        require(D == row['D'] and D and set(D) <= ss, 'small omission set')
        require(all(c[u] == '.' or c[v] == '.' or c[u] != c[v] for u,v in edges), 'proper full graph colouring')
        return sum(c[u] != '.' and c[v] != '.' for u,v in edges)

    cert = json.loads((HERE/'certificate.json').read_text()); new = cert['new_rows']
    require(len(initial) == 206 and len(new) == 16, 'input witness counts')
    initial_checks = sum(check(r) for r in initial); new_checks = sum(check(r) for r in new)
    rows = []
    for kind, index in cert['final_rows']:
        require(kind in ['initial', 'new'] and type(index) is int and index >= 0, 'final recipe')
        rows.append((initial if kind == 'initial' else new)[index])
    require(len(rows) == 202, 'final row count')
    cuts = [set(r['D']) for r in rows]
    require(all(not a <= b for i,a in enumerate(cuts) for j,b in enumerate(cuts) if i != j), 'antichain')
    forced = {next(iter(d)) for d in cuts if len(d) == 1}; free = sorted(ss-forced)
    require(len(forced) == 120 and len(free) == 22, 'forced and free counts')
    t = time.monotonic()
    count, remaining = uncovered(free, [d for d in cuts if not d & forced], 8)
    require(count == 319770 and not remaining, ('eight-omission cover', remaining[:1]))
    cover_seconds = time.monotonic()-t

    # Independently reconstruct and account for the entire frozen discovery set.
    old_forced = {r['D'][0] for r in initial if len(r['D']) == 1}
    old_free = sorted(ss-old_forced)
    count0, candidates = uncovered(old_free, [set(r['D']) for r in initial if not set(r['D']) & old_forced], 8)
    require(len(old_forced) == 119 and len(old_free) == 23 and count0 == 490314 and len(candidates) == 195, 'complete preflight')
    require(all(any(set(r['D']) <= set(o) for r in new) for o in candidates), 'all survivors covered by new positives')

    if work:
        require(json.loads((work/'survivors.json').read_text()) == candidates, 'actual survivor enumeration')
        require(json.loads((work/'native_witnesses.json').read_text()) == new, 'actual native positives')
        require(json.loads((work/'certificate.json').read_text()) == {'rows':rows}, 'actual final antichain')
        result = json.loads((work/'result.json').read_text()); history = result['history']
        require(result['status'] == 'FIXED_L_SMALL134_FAMILY_CLOSED' and not result['proofs'] and result['target'] is None, 'native closure status')
        require(len(history) == 16 and len(result['skipped_indices']) == 179, 'native branch counts')
        seen = []; h = 0; skipped = []
        for i,o in enumerate(candidates):
            if any(set(r['D']) <= set(o) for r in seen): skipped.append(i); continue
            rec = history[h]; row = new[h]
            require(rec['index'] == i and rec['omitted'] == o and rec['new_D'] == row['D'] and set(row['D']) <= set(o), 'tested selection')
            answers = rec['cases']; require([x['case'] for x in answers] == list(range(row['case']+1)), 'ordered case calls')
            require(answers[-1]['answer'] is True and all(x['answer'] is False for x in answers[:-1]), 'native answer bookkeeping')
            seen.append(row); h += 1
        require(h == 16 and skipped == result['skipped_indices'], 'all survivors accounted for')
        require(sum(len(r['cases']) for r in history) == 74, 'case call count')
        cross = [e for e in edges if (e[0] in ss) != (e[1] in ss)]
        boundary = sorted({v for e in cross for v in e if v not in ss})
        se = [e for e in edges if set(e) <= ss]; spos = {v:i for i,v in enumerate(S)}
        for k,p in enumerate(profiles):
            fixed = dict(zip(boundary, map(int,p['pattern'])))
            require(p['pattern'] == ''.join(p['colouring'][L.index(v)] for v in boundary), 'profile restriction')
            clauses = [[-569-i]+[4*i+c+1 for c in range(4)] for i in range(142)]
            for u,v in se:
                for c in range(4): clauses.append([-4*spos[u]-c-1, -4*spos[v]-c-1])
            for u,v in cross:
                if u in fixed: clauses.append([-4*spos[v]-fixed[u]-1])
                else: clauses.append([-4*spos[u]-fixed[v]-1])
            require((work/f'activation_{k:02d}.cnf').read_bytes() == raw(710, clauses), 'actual activated formula')
    # Small control catches a missing cover witness without another production run.
    require(uncovered([0,1,2], [{0},{1}], 2) == (3, []), 'complete toy cover')
    require(uncovered([0,1,2], [{0}], 2) == (3, [[1,2]]), 'incomplete toy cover detected')
    return dict(status='ALL SUBGRAPHS WITH AT MOST 134 SMALL VERTICES ARE FOUR-COLOURABLE',
                record_improvement=False, unrestricted_at_most508_family_closed=False,
                small_vertices_needed_by_any_nonfour_subgraph_at_least=135,
                large_vertices_in_any_at_most508_nonfour_subgraph_at_most=373,
                vertices=517, unit_edges=len(edges), exact_pair_checks=133386,
                initial_rows=206, new_rows=16, final_rows=len(rows),
                initial_witness_edge_checks=initial_checks, new_witness_edge_checks=new_checks,
                final_witness_edge_checks=sum(check(r) for r in rows),
                forced_small=sorted(forced), free_small=free, eight_sets_checked=count,
                preflight_eight_sets_checked=count0, preflight_survivors=len(candidates),
                native_case_calls_audited=74 if work else 0,
                native_activation_formulas_compared=20 if work else 0,
                negative_solver_proof_required=False, native_solver_used_by_checker=False,
                cover_seconds=cover_seconds, seconds=time.monotonic()-start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path); parser.add_argument('--report', type=Path)
    args = parser.parse_args(); result = verify(args.work)
    if args.report: args.report.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True))
