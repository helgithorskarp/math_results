"""Regenerate the compact finite capacity proof; Python>=3.11, standard library.
Actual author six-covering-1, researcher. Incompleteness produces no certificate.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time

def physical(rows, period):
    if (not rows or len({m for a, m in rows}) != len(rows)
            or any(type(a) is not int or type(m) is not int
                   or m < 2 or period % m or not 0 <= a < m for a, m in rows)):
        raise ValueError('Invalid distinct congruence system')
    covered = bytearray(period)
    for a, m in rows:
        for x in range(a, period, m):
            covered[x] = 1
    return [x for x, c in enumerate(covered) if not c]

def run(rows, period, free, bound, seconds, max_nodes, trace=None):
    physical(rows, period)
    if (not free or len(set(free)) != len(free) or not set(free) <= {m for a, m in rows}
            or not 0 <= bound < period or not 0 < seconds <= 10
            or not 1 <= max_nodes <= 5000):
        raise ValueError('Invalid bounded residual problem')
    started = time.monotonic()
    fixed = [(a, m) for a, m in rows if m not in free]
    points = physical(fixed, period) if fixed else list(range(period))
    old = {m: a for a, m in rows}
    buckets = {}
    for m in free:
        h = {}
        for i, x in enumerate(points):
            a = x % m
            h[a] = h.get(a, 0) | (1 << i)
        buckets[m] = h
    nodes = pruned = branches = 0
    chosen = {}
    solution = None

    def record(value):
        if trace is not None:
            trace.write(json.dumps(value, separators=(',', ':')) + '\n')

    def dfs(mask, remaining, parent, incoming):
        nonlocal nodes, pruned, branches, solution
        if nodes >= max_nodes or time.monotonic() - started >= seconds:
            return 'INCOMPLETE'
        node = nodes
        nodes += 1
        count = mask.bit_count()
        head = dict(node=node, parent=parent, incoming=incoming, residual=count)
        if count <= bound:
            record(dict(head, status='FOUND'))
            solution = [(chosen.get(m, a), m) for a, m in rows]
            if len(physical(solution, period)) > bound:
                raise ValueError('Residual tree witness fails physical coverage')
            return 'FOUND'
        histograms = {}
        capacities = {}
        for m in remaining:
            histogram = [(a, (mask & footprint).bit_count()) for a, footprint in buckets[m].items()]
            histogram = [(a, mass) for a, mass in histogram if mass]
            histograms[m] = histogram
            capacities[m] = max((mass for a, mass in histogram), default=0)
        capacity = sum(capacities.values())
        slack = capacity - count + bound
        if slack < 0:
            pruned += 1
            record(dict(head, status='STRICT_CAPACITY_LEAF', capacities=capacities,
                        capacity_sum=capacity, lower_bound=count - capacity))
            return 'CLOSED'
        options = {m: [(a, mass) for a, mass in histogram
                        if mass >= max(1, capacities[m] - slack)]
                   for m, histogram in histograms.items()}
        if not remaining or any(not opts for opts in options.values()):
            raise ValueError('Nonnegative-slack node lacks a positive admissible phase')
        m = min(remaining, key=lambda label: (len(options[label]), -capacities[label], label))
        phases = [a for a, mass in sorted(options[m],
                         key=lambda value: (value[0] != old[m], -value[1], value[0]))]
        branches += 1
        record(dict(head, status='BRANCH', capacities=capacities, capacity_sum=capacity,
                    slack=slack, modulus=m, phases=phases))
        rest = tuple(label for label in remaining if label != m)
        for a in phases:
            chosen[m] = a
            status = dfs(mask & ~buckets[m][a], rest, node, [m, a])
            if status != 'CLOSED':
                return status
        del chosen[m]
        return 'CLOSED'

    result = dfs((1 << len(points)) - 1, tuple(sorted(free)), None, None)
    metadata = dict(status=result, initial_residual=len(points), hole_target=bound,
                    free_labels=len(free), free_moduli=sorted(free), nodes=nodes,
                    strict_capacity_leaves=pruned, branch_nodes=branches,
                    seconds=time.monotonic() - started, native_seconds_limit=seconds,
                    node_limit=max_nodes)
    return solution, metadata

class Decisions:
    def __init__(self):
        self.rows = []
    def write(self, text):
        row = json.loads(text)
        if row['status'] == 'STRICT_CAPACITY_LEAF':
            self.rows.append(['L'])
        elif row['status'] == 'BRANCH':
            self.rows.append(['B', row['modulus'], row['phases']])
        else:
            raise ValueError('Unclosed proof node')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    seed = Path(__file__).with_name('seed.tsv')
    rows = [tuple(map(int, line.split())) for line in seed.read_text().splitlines()]
    low = [m for a, m in rows if m < 360]
    high = [m for a, m in rows if m >= 360]
    old = {m: a for a, m in rows}
    forced, nonforced = [], []
    for m0 in low:
        free = set(high + [m0])
        fixed = [(a, m) for a, m in rows if m not in free]
        points = physical(fixed, 15120)
        hist = {m: Counter(x % m for x in points) for m in free}
        caps = {m: max(h.values(), default=0) for m, h in hist.items()}
        slack = sum(caps.values()) - len(points) + 83
        alternatives = [a for a in range(m0) if a != old[m0] and caps[m0] - hist[m0][a] <= slack]
        (nonforced if alternatives else forced).append(m0)
    out = dict(period=15120, cutoff=360, hole_bound=83,
               seed_sha256=hashlib.sha256(seed.read_bytes()).hexdigest(),
               forced_old_cases=forced, trees=[])
    for extra in [None] + nonforced:
        collector = Decisions()
        free = high if extra is None else high + [extra]
        solution, metadata = run(rows, 15120, free, 83, 10, 5000, collector)
        if metadata['status'] != 'CLOSED' or solution is not None:
            raise ValueError('Incomplete tree or improved witness: no completed negative certificate')
        out['trees'].append(dict(extra=extra, decisions=collector.rows))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, separators=(',', ':')) + '\n')
    print(json.dumps(dict(status='ALL_TREES_COMPLETE', tree_nodes=sum(len(t['decisions']) for t in out['trees']),
                         fixture_sha256=hashlib.sha256(args.output.read_bytes()).hexdigest())))

if __name__ == '__main__':
    main()
