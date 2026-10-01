"""Producer: exact single/pair pools and every compatible four/six-clique."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time
import model as m


def compatible_cliques(adj, size, prefix=(), remaining=None):
    if remaining is None:
        remaining = (1 << len(adj))-1
    if len(prefix) == size:
        yield prefix
        return
    needed = size-len(prefix)
    while remaining.bit_count() >= needed:
        bit = remaining & -remaining
        remaining -= bit
        i = bit.bit_length()-1
        yield from compatible_cliques(adj, size, prefix+(i,), remaining & adj[i])


def case(g, p, J, P, weight):
    rows = m.graph(g, J, P)
    bad = m.blue_bad(rows)
    pool = []
    if bad is None:
        for d in range(35):
            m.toggle(rows, g[2][d])
            good = m.blue_bad(rows) is None
            m.toggle(rows, g[2][d])
            if good:
                pool.append(d)
    adj = [0]*len(pool)
    for i, j in combinations(range(len(pool)), 2):
        m.toggle(rows, g[2][pool[i]])
        m.toggle(rows, g[2][pool[j]])
        good = m.blue_bad(rows) is None
        m.toggle(rows, g[2][pool[j]])
        m.toggle(rows, g[2][pool[i]])
        if good:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    critical = []
    for indices in compatible_cliques(adj, 2*p+2):
        D = tuple(pool[i] for i in indices)
        violation = m.blue_bad(m.graph(g, J, P, D))
        m.need(violation is not None, 'counterexample to the proposed blue budget')
        critical.append(dict(deletions=list(D), violation=violation))
    return dict(promotions=p, joins=list(J), additions=list(P), multiplicity=weight,
                base_blue_valid=bad is None, pool=pool, compatibility=adj, critical=critical)


def run(first, seconds):
    started = time.monotonic()
    g = m.geometry()
    tasks = [(p, J, P, w) for p in (1, 2) for J, P, w in m.choices(g, p)]
    m.need(type(first) is int and 0 <= first <= len(tasks) and 0 < seconds <= 30, 'phase domain')
    records, index = [], first
    while index < len(tasks):
        if records and time.monotonic()-started >= seconds:
            break
        records.append(case(g, *tasks[index]))
        index += 1
    return dict(first=first, next=index, total=len(tasks), complete=index == len(tasks),
                records=records, seconds=time.monotonic()-started)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--first', type=int, default=0)
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = run(args.first, args.seconds)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, sort_keys=True)+'\n')
    print(json.dumps({k: out[k] for k in ('first', 'next', 'total', 'complete', 'seconds')}))
