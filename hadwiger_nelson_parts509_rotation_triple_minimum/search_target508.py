#!/usr/bin/env python3
"""Target-cardinality CEGAR for a 508-vertex core in a placement union."""

from __future__ import annotations

import argparse
import json
import os
import random
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

from verify import build_union, edge_digest


K = 4
TARGET_ORDER = 508


def inclusion_minimal(rows):
    kept = []
    kept_sets = []
    for row in sorted(rows, key=lambda r: (len(r['D']), r['D'])):
        deleted = frozenset(row['D'])
        if any(old <= deleted for old in kept_sets):
            continue
        kept.append(row)
        kept_sets.append(deleted)
    return kept


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('forced_checkpoint', type=Path)
    parser.add_argument('seed_family', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--seed', type=int, default=5)
    parser.add_argument('--chains', type=int, default=100)
    parser.add_argument('--improve', type=int, default=0)
    parser.add_argument('--max-rounds', type=int, default=10000)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    points_path = here.parent / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
    points, edges, _, _ = build_union(points_path)
    n = len(points)
    graph_digest = edge_digest(edges)
    forced_data = json.loads(args.forced_checkpoint.read_text())
    seed = json.loads(args.seed_family.read_text())
    if forced_data['union_edge_sha256'] != graph_digest:
        raise ValueError('forced checkpoint graph mismatch')
    if seed['union_edge_sha256'] != graph_digest:
        raise ValueError('seed family graph mismatch')
    forced = set(forced_data['forced'])
    if seed['forced'] != sorted(forced):
        raise ValueError('seed family forced-set mismatch')
    if not forced <= set(range(n)):
        raise ValueError('seed forced set contains an invalid vertex')
    target_optional = TARGET_ORDER - len(forced)
    if not 0 <= target_optional <= n - len(forced):
        raise ValueError('target order is incompatible with the forced set')
    optional = sorted(set(range(n)) - forced)
    optional_index = {v: i + 1 for i, v in enumerate(optional)}
    rng = random.Random(args.seed)

    if args.output.exists():
        state = json.loads(args.output.read_text())
        if state['union_edge_sha256'] != graph_digest:
            raise ValueError('output checkpoint graph mismatch')
    else:
        state = {
            'format': 'parts509-exceptional-rotation-triple-target508-v1',
            'union_edge_sha256': graph_digest,
            'events': [108, 109, 789],
            'forced': sorted(forced),
            'target_optional': target_optional,
            'family': seed['family'],
            'history': [],
            'status': 'running',
            'record': None,
        }
    if state['forced'] != sorted(forced):
        raise ValueError('output checkpoint forced-set mismatch')
    if state['target_optional'] != target_optional:
        raise ValueError('output checkpoint target-cardinality mismatch')
    if state.get('events') not in (None, [108, 109, 789]):
        raise ValueError('output checkpoint event mismatch')
    state['events'] = [108, 109, 789]
    seen = {tuple(row['D']) for row in state['family']}

    def cv(v, c):
        return K * v + c + 1

    def av(v):
        return K * n + v + 1

    graph_clauses = [[-av(v), *[cv(v, c) for c in range(K)]] for v in range(n)]
    for u, v in edges:
        for c in range(K):
            graph_clauses.append([-av(u), -av(v), -cv(u, c), -cv(v, c)])
    for c, v in enumerate((0, 149, 152)):
        graph_clauses.append([cv(v, c)])

    def save():
        temporary = args.output.with_suffix(args.output.suffix + '.tmp')
        temporary.write_text(json.dumps(state, sort_keys=True))
        temporary.replace(args.output)

    def master_candidate():
        rows = inclusion_minimal(state['family'])
        clauses = [[optional_index[v] for v in row['D']] for row in rows]
        clauses.extend(CardEnc.equals(
            lits=list(optional_index.values()), bound=target_optional,
            top_id=len(optional), encoding=EncType.totalizer,
        ).clauses)
        started = time.monotonic()
        with Solver(name='cadical195', bootstrap_with=clauses) as solver:
            ok = solver.solve()
            model = {lit for lit in solver.get_model() if lit > 0} if ok else set()
        candidate = {v for v in optional if optional_index[v] in model}
        return ok, candidate, len(rows), time.monotonic() - started

    def oracle_coloring(active, solver):
        started = time.monotonic()
        ok = solver.solve(assumptions=[av(v) if v in active else -av(v) for v in range(n)])
        elapsed = time.monotonic() - started
        if not ok:
            return None, elapsed
        model = {lit for lit in solver.get_model() if lit > 0}
        colors = {v: next(c for c in range(K) if cv(v, c) in model) for v in active}
        if any(colors[u] == colors[v] for u, v in edges if u in active and v in active):
            raise AssertionError('invalid oracle colouring')
        return colors, elapsed

    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    def greedy_extend(active, colors):
        active = set(active)
        colors = dict(colors)
        remaining = [v for v in optional if v not in active]
        rng.shuffle(remaining)
        changed = True
        while changed:
            changed = False
            for v in list(remaining):
                used = {colors[w] for w in adjacency[v] if w in active}
                if len(used) < K:
                    choices = [c for c in range(K) if c not in used]
                    colors[v] = choices[rng.randrange(len(choices))]
                    active.add(v)
                    remaining.remove(v)
                    changed = True
        return active, colors

    save()
    if state['status'] in {'theorem', 'record'}:
        print(json.dumps({'checkpoint_status': state['status'], 'family': len(state['family'])}), flush=True)
        return
    print(json.dumps({'pid': os.getpid(), 'pgid': os.getpgrp(), 'cpu_affinity': sorted(os.sched_getaffinity(0)), 'initial_family': len(state['family'])}), flush=True)
    with Solver(name='cadical195', bootstrap_with=graph_clauses) as oracle:
        for round_number in range(len(state['history']) + 1, args.max_rounds + 1):
            master_ok, X, minimal_count, master_seconds = master_candidate()
            if not master_ok:
                state['status'] = 'theorem'
                state['history'].append({'round': round_number, 'master': 'UNSAT', 'minimal_family': minimal_count, 'master_seconds': master_seconds})
                save()
                print(f'THEOREM no_target_hitting_set family={len(state["family"])} minimal_family={minimal_count} master_seconds={master_seconds:.2f}', flush=True)
                return
            if len(X) != target_optional:
                raise AssertionError(len(X))
            active = forced | X
            colors, oracle_seconds = oracle_coloring(active, oracle)
            if colors is None:
                state['status'] = 'record'
                state['record'] = sorted(active)
                state['history'].append({'round': round_number, 'master': 'SAT', 'oracle': 'UNSAT', 'minimal_family': minimal_count, 'master_seconds': master_seconds, 'oracle_seconds': oracle_seconds})
                save()
                print(f'RECORD vertices={len(active)} round={round_number} master_seconds={master_seconds:.2f} oracle_seconds={oracle_seconds:.2f}', flush=True)
                return
            added = 0
            sizes = []
            improve_calls = 0
            improve_seconds = 0.0
            for chain_index in range(args.chains):
                extended, full_colors = greedy_extend(active, colors)
                budget = args.improve if chain_index == 0 else 0
                while budget:
                    remaining = list(set(optional) - extended)
                    if not remaining:
                        break
                    rng.shuffle(remaining)
                    advanced = False
                    for vertex in remaining:
                        if not budget:
                            break
                        budget -= 1
                        candidate_colors, elapsed = oracle_coloring(extended | {vertex}, oracle)
                        improve_calls += 1
                        improve_seconds += elapsed
                        if candidate_colors is not None:
                            extended, full_colors = greedy_extend(extended | {vertex}, candidate_colors)
                            advanced = True
                            break
                    if not advanced:
                        break
                deleted = tuple(sorted(set(range(n)) - extended))
                sizes.append(len(deleted))
                if deleted in seen:
                    continue
                seen.add(deleted)
                state['family'].append({'D': list(deleted), 'witness': ''.join(str(full_colors[v]) for v in range(n) if v not in deleted)})
                added += 1
            state['history'].append({
                'round': round_number, 'master': 'SAT', 'oracle': 'SAT',
                'minimal_family': minimal_count, 'master_seconds': master_seconds,
                'oracle_seconds': oracle_seconds, 'new_killing_sets': added,
                'deletion_sizes': sizes, 'improve_calls': improve_calls,
                'improve_seconds': improve_seconds,
            })
            save()
            print(
                f'round={round_number} family={len(state["family"])} minimal={minimal_count} '
                f'master_seconds={master_seconds:.2f} oracle_seconds={oracle_seconds:.2f} '
                f'new={added} improve_calls={improve_calls} improve_seconds={improve_seconds:.2f} '
                f'sizes={sizes}', flush=True,
            )
            if not added:
                state['status'] = 'stalled'
                save()
                print('STALLED no new killing sets', flush=True)
                return


if __name__ == '__main__':
    main()
