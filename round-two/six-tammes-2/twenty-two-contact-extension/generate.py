"""Bounded deterministic generation with unchanged G22 witness selectors.

This module selects records; acceptance belongs to the frozen reader.
Budget stops are intentional partial transitions, not exclusion claims.
"""
from collections import Counter
from pathlib import Path
import argparse
import json
import signal
import time
from binding import load, write_json

MAX_DEPTH = 22
MAX_NODES = 20000
GUARD_SECONDS = 160
CAMPAIGN_STATE = Path('/scratch/research-team-sol61-six-20260929/state')


class TransitionBudget(Exception):
    pass


def advance(initial, reader, budget=2500):
    if type(budget) is not int or not 1 <= budget <= 2500:
        raise ValueError('logical transition budget must be 1..2500')
    reader.shape(initial)
    c = reader.c
    # Callers provide a fresh decoded state. Install every node/tree update
    # by replacing one tuple; an alarm cannot expose a half-created split.
    tree = (initial['nodes'], initial['stack'])
    added = 0
    started = time.monotonic()
    status, reason = 'RUNNING', None

    def replace(index, **changes):
        nonlocal tree
        nodes, stack = tree
        node = dict(nodes[index]); node.update(changes)
        next_nodes = list(nodes); next_nodes[index] = node
        tree = (next_nodes, stack)

    def record(index, triple, witness):
        nonlocal added
        node = tree[0][index]
        reader.require(triple in node['remaining'], 'unresolved triple')
        replace(index, proofs=node['proofs'] + [[triple, *witness]],
                remaining=[j for j in node['remaining'] if j != triple])
        added += 1
        if added >= budget:
            raise TransitionBudget()

    def close(index, **changes):
        nonlocal tree
        nodes, stack = tree
        node = dict(nodes[index]); node.update(changes)
        next_nodes = list(nodes); next_nodes[index] = node
        tree = (next_nodes, stack[:-1])

    def split(index, axis, cells):
        nonlocal tree
        nodes, stack = tree
        node = dict(nodes[index])
        inherited = node['bounded_inherited'] or node['bounded']
        children = [len(nodes), len(nodes) + 1]
        next_children = [dict(cell=list(cell), remaining=list(node['remaining']),
                              proofs=[], bounded_inherited=inherited, bounded=False)
                         for cell in cells]
        node.update(split=axis, children=children)
        next_nodes = list(nodes); next_nodes[index] = node
        next_nodes.extend(next_children)
        tree = (next_nodes, stack[:-1] + list(reversed(children)))

    try:
        while tree[1]:
            if any((CAMPAIGN_STATE / name).exists()
                   for name in ('PAUSED.json', 'HANDOVER.json')):
                raise RuntimeError('operational pause barrier')
            index = tree[1][-1]
            node = tree[0][index]
            td, ti, zd, zi = node['cell']
            try:
                P, t, _ = c.m.enclosed(*c.box(td, ti, zd, zi))
                prune = c.packing_prune(P, t)
                if prune:
                    close(index, prune=list(prune)); continue
                base = dict(P=P, t=t)
                for triple in node['remaining']:
                    witness = c.gram3_classify(triple, base)
                    if witness is not None:
                        record(index, triple, witness)
                geometry = c.geometry(P, t)
                geometry['products'] = base.setdefault('products', {})
                node = tree[0][index]
                if not (node['bounded_inherited'] or node['bounded']):
                    c.bounded(geometry); replace(index, bounded=True)
                node = tree[0][index]
                for triple in node['remaining']:
                    witness = c.classify(triple, geometry, False)
                    if witness is not None:
                        record(index, triple, witness)
                node = tree[0][index]
                if not node['remaining']:
                    close(index, complete=True); continue
            except ArithmeticError as error:
                replace(index, last_arithmetic_obstacle=str(error))
            if td + zd >= MAX_DEPTH:
                status = 'INCOMPLETE_DEPTH'; reason = 'depth22 unresolved'; break
            if len(tree[0]) + 2 > MAX_NODES:
                status = 'INCOMPLETE_NODE_GUARD'; reason = 'node guard'; break
            axis = 't' if td <= zd else 'z'
            cells = ([td+1, 2*ti, zd, zi], [td+1, 2*ti+1, zd, zi]) if axis == 't' else (
                [td, ti, zd+1, 2*zi], [td, ti, zd+1, 2*zi+1])
            split(index, axis, cells)
        else:
            status = 'COMPLETE_SEARCH_REQUIRES_LITERAL_REPLAY'
    except TransitionBudget:
        status = 'TRANSITION_BUDGET_REACHED_REQUIRES_LITERAL_REPLAY'
    except TimeoutError as error:
        status = 'INCOMPLETE_TIMEOUT'; reason = str(error)
    except RuntimeError as error:
        status = 'STOPPED_OPERATIONAL_BARRIER'; reason = str(error)
    nodes, stack = tree
    counts = Counter(row[1] for node in nodes for row in node['proofs'])
    state = dict(agent='six-tammes-2', role='researcher', status=status, reason=reason,
                 seconds=round(time.monotonic()-started, 3), nodes=nodes, stack=stack,
                 max_depth=MAX_DEPTH, guard_seconds=GUARD_SECONDS,
                 stats=dict(counts))
    reader.shape(state)
    return state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--budget', type=int, default=2500)
    args = parser.parse_args()
    if Path(args.input).resolve() == Path(args.output).resolve():
        raise ValueError('preserve checked input')
    delta, _, _ = load(args.work)
    initial = json.loads(Path(args.input).read_text())
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(
        TimeoutError('160-second generation guard; incomplete')))
    signal.alarm(GUARD_SECONDS)
    try:
        state = advance(initial, delta.r, args.budget)
    finally:
        signal.alarm(0)
    write_json(args.output, state, compact=True)
    print(json.dumps(dict(status=state['status'], node_count=len(state['nodes']),
                          witnesses=sum(state['stats'].values()), pending=len(state['stack']),
                          seconds=state['seconds'])))
    if state['status'] not in ('COMPLETE_SEARCH_REQUIRES_LITERAL_REPLAY',
                              'TRANSITION_BUDGET_REACHED_REQUIRES_LITERAL_REPLAY'):
        raise SystemExit(2)


if __name__ == '__main__':
    main()
