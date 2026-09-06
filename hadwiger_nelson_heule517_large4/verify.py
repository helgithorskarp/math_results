#!/usr/bin/env python3
"""Solver-free exact checker of all four-large/five-small deletions.

The target-order corollary also invokes the published large3 closure;
that closed computation is not rerun by this checker.
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


def mask(vertices): return sum(1 << v for v in vertices)


def raw(n, clauses):
    return (f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()


def verify(work=None):
    start = time.monotonic()
    for name,digest in json.loads((HERE/'manifest.json').read_text()).items():
        require(sha256((REPO/name).read_bytes()).hexdigest() == digest, ('input hash',name))
    spec = importlib.util.spec_from_file_location('independent_geometry', REPO/'hadwiger_nelson_heule517_joint_interface/verify.py')
    G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
    points, edges = G.graph()
    L = {v for v,p in enumerate(points) if all(p[a][k] == 0 for a in (0,1) for k in (2,3,6,7))}
    S = set(range(517))-L; ls = sorted(L); ss = sorted(S)
    require(len(L) == 375 and len(S) == 142 and len(edges) == 2555, 'graph counts')
    old = json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
    labels = [v for v in range(553) if '510' in old['provenance'][v]]
    prior = json.loads((REPO/'hadwiger_nelson_heule517_family_pilot/certificate.json').read_text())['rows']
    c133 = json.loads((REPO/'hadwiger_nelson_heule517_small_pilot/certificate.json').read_text())['rows']
    c134 = json.loads((REPO/'hadwiger_nelson_heule517_small134/certificate.json').read_text())
    small_rows = [(c133 if k == 'initial' else c134['new_rows'])[i] for k,i in c134['final_rows']]
    large2 = json.loads((REPO/'hadwiger_nelson_heule517_large2_pilot/certificate.json').read_text())['rows']
    large3 = json.loads((REPO/'hadwiger_nelson_heule517_large3/certificate.json').read_text())['rows']
    profiles = json.loads((REPO/'hadwiger_nelson_heule517_joint_interface/certificate.json').read_text())['rows']

    def decode_prior(row):
        if row['source'] == 'native': return row['colouring']
        if row['source'] == 'forced':
            D = [row['index']]; text = old['forced_witness'][str(row['index'])]
        else:
            require(row['source'] == 'family', 'prior kind')
            source = old['family'][row['index']]; D = source['D']; text = source['witness']
        retained = sorted(set(range(553))-set(D)); require(len(retained) == len(text), 'prior witness length')
        c = dict(zip(retained,text)); return ''.join(c.get(v,'.') for v in labels)+row['extra']

    def decode_small(row):
        if row['kind'] == 'seed':
            source = prior[row['row']]; require(row['D'] == source['D'], 'small seed omission set')
            return decode_prior(source)
        require(row['kind'] == 'case' and type(row['case']) is int and 0 <= row['case'] < 20, 'small case')
        lc = profiles[row['case']]['colouring']; sc = row['colouring']
        require(len(lc) == 375 and len(sc) == 142, 'block witness lengths')
        c = ['.']*517
        for v,x in zip(ls,lc): c[v] = x
        for v,x in zip(ss,sc): c[v] = x
        return ''.join(c)

    def check(c,D):
        require(len(c) == 517 and set(c) <= set('.0123'), 'colouring domain')
        require(D == [i for i,x in enumerate(c) if x == '.'] and D, 'exact nonempty omissions')
        require(all(c[u] == '.' or c[v] == '.' or c[u] != c[v] for u,v in edges), 'proper full graph colouring')
        return sum(c[u] != '.' and c[v] != '.' for u,v in edges)

    require(len(prior) == 526 and len(small_rows) == 202 and len(large2) == 86 and len(large3) == 108, 'initial counts')
    initial_checks = sum(check(decode_prior(r),r['D']) for r in prior)
    initial_checks += sum(check(decode_small(r),r['D']) for r in small_rows)
    initial_checks += sum(check(r['colouring'],r['D']) for r in large2)
    initial_checks += sum(check(r['colouring'],r['D']) for r in large3)
    all_initial = [set(r['D']) for r in prior+small_rows+large2+large3]
    require(all(len(d & L) <= 3 for d in all_initial), 'initial large-cut structure')
    forced = {next(iter(d)) for d in all_initial if len(d) == 1}; free = sorted(S-forced)
    require(len(forced) == 467 and len(forced & L) == 340 and len(forced & S) == 127 and len(free) == 15, 'forcing')
    small_masks = [mask(d) for d in all_initial if d <= S]
    small_cases = []; five_count = 0
    for O in combinations(free,5):
        five_count += 1; om = mask(O)
        if not any(om & d == d for d in small_masks): small_cases.append(list(O))
    require(five_count == 3003 and len(small_cases) == 94, 'complete five-omission enumeration')
    new = json.loads((HERE/'certificate.json').read_text())['rows']
    require(len({r['native_index'] for r in new}) == len(new), 'distinct witness provenance')
    new_checks = sum(check(r['colouring'],r['D']) for r in new)
    global_forced = forced | {r['D'][0] for r in new if len(r['D']) == 1}
    require(len(global_forced) == 490 and len(global_forced & L) == 362 and len(global_forced & S) == 128, 'new global forcing')
    require(all(len(set(r['D']) & L) <= 4 and len(set(r['D']) & S) <= 5 for r in new), 'new witness family')
    require(all(not set(a['D']) <= set(b['D']) for i,a in enumerate(new) for j,b in enumerate(new) if i != j), 'new antichain')
    new_masks = [mask(r['D']) for r in new]; checked_quadruples = 0; initial_quadruple_sets = []; t = time.monotonic()
    for O in small_cases:
        os = set(O); om = mask(O)
        relevant = [d & L for d in all_initial if d & S <= os]
        require(all(relevant), 'surviving small omissions')
        forced_large = set().union(*(d for d in relevant if len(d) == 1))
        excluded_sets = [d for d in relevant if 2 <= len(d) <= 3]
        quadruples = set()
        for quadruple in combinations(sorted(L-forced_large),4):
            if any(d <= set(quadruple) for d in excluded_sets): continue
            full_omission = om | mask(quadruple)
            require(any(full_omission & d == d for d in new_masks), ('uncovered quadruple',O,quadruple))
            checked_quadruples += 1
            if work: quadruples.add(quadruple)
        if work: initial_quadruple_sets.append(quadruples)
    require(checked_quadruples == 31695, 'complete large-quadruple cover')
    cover_seconds = time.monotonic()-t; native_checks = 0; native_count = 0
    if work:
        native = json.loads((work/'native_witnesses.json').read_text()); native_count = len(native)
        native_checks = sum(check(r['colouring'],r['D']) for r in native)
        for r in new:
            original = native[r['native_index']]
            require(r['D'] == original['D'] and r['colouring'] == original['colouring'], 'retained witness')
        require(all(any(set(q['D']) <= set(r['D']) for q in new) for r in native), 'all native rows subsumed')
        result = json.loads((work/'result.json').read_text()); history = result['history']
        require(result['status'] == 'FOUR_LARGE_FAMILY_CLOSED' and result['proof'] is None and result['target'] is None, 'native result')
        require(len(history) == len(native) <= 256 and result['remaining_quadruples'] == 0, 'native count')
        initial_counts = json.loads((work/'initial_counts.json').read_text())
        require(initial_counts == [dict(small_omitted=o,quadruples=len(ts)) for o,ts in zip(small_cases,initial_quadruple_sets)], 'actual initial family')
        cursor = 0; remaining = checked_quadruples
        for turn,(rec,row) in enumerate(zip(history,native)):
            while not initial_quadruple_sets[cursor]: cursor = (cursor+1) % len(small_cases)
            i = cursor; quadruple = min(initial_quadruple_sets[i]); cursor = (cursor+1) % len(small_cases)
            O = sorted(small_cases[i]+list(quadruple))
            require(rec['turn'] == turn and rec['state'] == i and rec['omitted'] == O and rec['answer'] is True, 'round-robin candidate')
            require(set(row['D']) <= set(O) and row['D'] == rec['D'], 'witness covers 508-vertex query')
            ds = set(row['D']) & S; dl = set(row['D']) & L
            for j,os in enumerate(small_cases):
                if ds <= set(os): initial_quadruple_sets[j] = {tr for tr in initial_quadruple_sets[j] if not dl <= set(tr)}
            current = sum(map(len,initial_quadruple_sets))
            require(rec['remaining'] == current and rec['removed'] == remaining-current, 'actual removal counts')
            remaining = current
        require(remaining == 0, 'native exhaustion')
        clauses = [[-2069-v]+[4*v+c+1 for c in range(4)] for v in range(517)]
        for u,v in edges:
            for c in range(4): clauses.append([-4*u-c-1,-4*v-c-1])
        clauses.append([-2069,1])
        require((work/'activation.cnf').read_bytes() == raw(2585,clauses), 'actual activated graph formula')
    return dict(status='ALL FOUR-LARGE/FIVE-SMALL DELETIONS OF H517 ARE FOUR-COLOURABLE',
                record_improvement=False, unrestricted_at_most508_family_closed=False,
                target_corollary_uses_prior_large3_theorem=True,
                prior_theorem='bafkreicbbe6mjmfjyqqtlqmot2ku5g7jhgds2ehwf6anihjhzlasjclifu',
                corollary_small_vertices_at_least=138, corollary_large_vertices_at_most=370,
                vertices=517, unit_edges=len(edges), exact_pair_checks=133386,
                initial_positive_rows=922, initial_witness_edge_checks=initial_checks,
                new_certificate_rows=len(new), new_witness_edge_checks=new_checks,
                forced_large=340, forced_small=127, five_sets_checked=five_count,
                final_global_forced=490, final_forced_large=362, final_forced_small=128,
                global_free_vertices=sorted(set(range(517))-global_forced),
                surviving_small_cases=94, large_quadruples_checked=checked_quadruples,
                remaining_quadruples=0, native_witnesses_checked=native_count,
                native_witness_edge_checks=native_checks, actual_activation_cnf_compared=bool(work),
                negative_solver_proof_required=False, native_solver_used_by_checker=False,
                cover_seconds=cover_seconds, seconds=time.monotonic()-start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work',type=Path); parser.add_argument('--report',type=Path)
    args = parser.parse_args(); result = verify(args.work)
    if args.report: args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
