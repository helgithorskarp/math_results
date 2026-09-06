#!/usr/bin/env python3
"""Independent exact geometry, positive-witness and coupled family checker."""
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
    profiles = json.loads((REPO/'hadwiger_nelson_heule517_joint_interface/certificate.json').read_text())['rows']

    def decode_prior(row):
        if row['source'] == 'native': return row['colouring']
        if row['source'] == 'forced':
            D = [row['index']]; text = old['forced_witness'][str(row['index'])]
        else:
            require(row['source'] == 'family', 'prior kind')
            source = old['family'][row['index']]; D = source['D']; text = source['witness']
        retained = sorted(set(range(553))-set(D)); require(len(retained) == len(text), 'prior witness length')
        c = dict(zip(retained,text))
        return ''.join(c.get(v,'.') for v in labels)+row['extra']

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
        require(D == [i for i,x in enumerate(c) if x == '.'] and D, 'exact nonempty omission set')
        require(all(c[u] == '.' or c[v] == '.' or c[u] != c[v] for u,v in edges), 'proper full graph colouring')
        return sum(c[u] != '.' and c[v] != '.' for u,v in edges)

    require(len(prior) == 526 and len(small_rows) == 202, 'initial counts')
    prior_checks = sum(check(decode_prior(r),r['D']) for r in prior)
    small_checks = sum(check(decode_small(r),r['D']) for r in small_rows)
    new = json.loads((HERE/'certificate.json').read_text())['rows']
    require(len(new) == 86 and len({r['native_index'] for r in new}) == 86, 'new certificate count')
    new_checks = sum(check(r['colouring'],r['D']) for r in new)
    require(all(len(set(r['D']) & L) <= 2 and len(set(r['D']) & S) <= 7 for r in new), 'new witness family')
    require(all(not set(a['D']) <= set(b['D']) for i,a in enumerate(new) for j,b in enumerate(new) if i != j), 'new antichain')
    small_cuts = [set(r['D']) for r in small_rows]
    require(all(d <= S for d in small_cuts), 'pure small input cuts')
    forced = {next(iter(d)) for d in small_cuts if len(d) == 1}; free = sorted(S-forced)
    require(len(forced) == 120 and len(free) == 22, 'small forcing')
    residual_small = [mask(d) for d in small_cuts if not d & forced]

    # Recheck the inherited positive proof used for the <=508 corollary.
    eight_count = 0
    for O in combinations(free,8):
        om = mask(O); require(any(om & d == d for d in residual_small), 'inherited eight-omission cover')
        eight_count += 1
    require(eight_count == 319770, 'complete inherited cover')

    small_cases = []; seven_count = 0
    for O in combinations(free,7):
        seven_count += 1; om = mask(O)
        if not any(om & d == d for d in residual_small): small_cases.append(list(O))
    require(seven_count == 170544 and len(small_cases) == 167, 'complete seven-omission enumeration')
    all_initial = [set(r['D']) for r in prior+small_rows]
    require(all(len(d & L) <= 1 for d in all_initial), 'initial large-cut structure')
    new_masks = [mask(r['D']) for r in new]; checked_pairs = 0; initial_pair_sets = []
    t = time.monotonic()
    for O in small_cases:
        os = set(O); om = mask(O)
        require(not any(d <= os for d in all_initial), 'surviving small omission case')
        forced_large = set()
        for d in all_initial:
            if d & S <= os: forced_large.update(d & L)
        eligible = sorted(L-forced_large); pairs = set()
        for a,b in combinations(eligible,2):
            full_omission = om | (1 << a) | (1 << b)
            require(any(full_omission & d == d for d in new_masks), ('uncovered two-large case',a,b,O))
            checked_pairs += 1
            if work: pairs.add((a,b))
        if work: initial_pair_sets.append(pairs)
    require(checked_pairs == 870215, 'complete initial pair cover')
    cover_seconds = time.monotonic()-t
    native_checks = 0
    if work:
        native = json.loads((work/'native_witnesses.json').read_text())
        require(len(native) == 143, 'native positives count')
        native_checks = sum(check(r['colouring'],r['D']) for r in native)
        for r in new:
            original = native[r['native_index']]
            require(r['D'] == original['D'] and r['colouring'] == original['colouring'], 'retained native witness')
        require(all(any(set(q['D']) <= set(r['D']) for q in new) for r in native), 'omitted native rows subsumed')
        result = json.loads((work/'result.json').read_text()); history = result['history']
        require(result['status'] == 'TWO_LARGE_FAMILY_CLOSED' and result['proof'] is None and result['target'] is None, 'native result')
        require(len(history) == 143 and result['remaining_pairs'] == 0, 'native query count')
        cursor = 0; remaining = checked_pairs
        initial_counts = json.loads((work/'initial_counts.json').read_text())
        require(initial_counts == [dict(small_omitted=o,pairs=len(p)) for o,p in zip(small_cases,initial_pair_sets)], 'actual initial family')
        for rec,row in zip(history,native):
            while not initial_pair_sets[cursor]: cursor = (cursor+1) % len(small_cases)
            i = cursor; pair = min(initial_pair_sets[i]); cursor = (cursor+1) % len(small_cases)
            O = sorted(small_cases[i]+list(pair))
            require(rec['state'] == i and rec['omitted'] == O and rec['answer'] is True, 'round-robin candidate')
            require(set(row['D']) <= set(O) and row['D'] == rec['D'], 'witness covers selected 508 graph')
            ds = set(row['D']) & S; dl = set(row['D']) & L
            for j,os in enumerate(small_cases):
                if ds <= set(os):
                    initial_pair_sets[j] = {p for p in initial_pair_sets[j] if not dl <= set(p)}
            current = sum(map(len,initial_pair_sets))
            require(rec['remaining'] == current and rec['removed'] == remaining-current, 'exact native coverage counts')
            remaining = current
        require(remaining == 0, 'native coverage exhaustion')
        clauses = [[-2069-v]+[4*v+c+1 for c in range(4)] for v in range(517)]
        for u,v in edges:
            for c in range(4): clauses.append([-4*u-c-1,-4*v-c-1])
        clauses.append([-2069,1])
        require((work/'activation.cnf').read_bytes() == raw(2585,clauses), 'actual activated graph CNF')
    return dict(status='ALL TWO-LARGE/SEVEN-SMALL DELETIONS OF H517 ARE FOUR-COLOURABLE',
                record_improvement=False, unrestricted_at_most508_family_closed=False,
                small_vertices_needed_by_any_at_most508_nonfour_subgraph_at_least=136,
                large_vertices_in_any_at_most508_nonfour_subgraph_at_most=372,
                vertices=517, unit_edges=len(edges), exact_pair_checks=133386,
                initial_full_rows=526, initial_small_rows=202, new_certificate_rows=86,
                full_witness_edge_checks=prior_checks, small_witness_edge_checks=small_checks,
                new_witness_edge_checks=new_checks, inherited_eight_sets_checked=eight_count,
                seven_sets_checked=seven_count, surviving_small_choices=167,
                large_pairs_checked=checked_pairs, remaining_pairs=0,
                native_witnesses_checked=143 if work else 0, native_witness_edge_checks=native_checks,
                actual_activation_cnf_compared=bool(work), negative_solver_proof_required=False,
                native_solver_used_by_checker=False, cover_seconds=cover_seconds,
                seconds=time.monotonic()-start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work',type=Path); parser.add_argument('--report',type=Path)
    args = parser.parse_args(); result = verify(args.work)
    if args.report: args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
