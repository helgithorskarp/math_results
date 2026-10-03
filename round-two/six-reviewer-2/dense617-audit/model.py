"""Independent literal field graph and increasing-tuple coverage. Python 3.11."""
import hashlib
import json
from collections import Counter

P = 617

def require(condition, message):
    if not condition:
        raise ValueError(message)

def canon(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n"

def digest(x):
    return hashlib.sha256(canon(x).encode()).hexdigest()

def inverse(a):
    old_r, r, old_s, s = P, a, 0, 1
    while r:
        q = old_r // r
        old_r, r, old_s, s = r, old_r-q*r, s, old_s-q*s
    require(old_r == 1, "nonunit")
    return old_s % P

def graph():
    require(all(P % d for d in range(2, 25)), "prime")
    square = set(x*x % P for x in range(1, P))
    S = tuple(sorted(square))
    T = tuple(x for x in range(1, P) if x not in square)
    supports = []
    for step in range(1, P):
        row = tuple(sorted((1+j*step) % P for j in range(1, 7)))
        if all(t in T for t in row):
            supports.append((step, row))
    V = set().union(*(set(row) for step, row in supports))
    invV = set(inverse(v) for v in V)
    require(len(V) == 33 and not V & invV, "directed ratios")
    D = V | invV
    rows = tuple(sum(1 << j for j, t in enumerate(T)
                     if t*inverse(s) % P in D) for s in S)
    columns = tuple(sum(1 << i for i, s in enumerate(S)
                        if (rows[i] >> j) & 1) for j in range(len(T)))
    require(len(S) == len(T) == 308, "classes")
    require(all(x.bit_count() == 66 for x in rows+columns), "degrees")
    return S, T, rows, columns, supports

def increasing(rows, threshold=6):
    """All anchored increasing row tuples, with no closure-family input."""
    levels = [[] for _ in range(8)]
    trials = [0]*8
    def visit(a, b):
        require(len(a) < len(levels), "unexpected large biclique")
        levels[len(a)].append((a, b))
        for i in range(a[-1]+1, len(rows)):
            trials[len(a)+1] += 1
            c = b & rows[i]
            if c.bit_count() >= threshold:
                visit(a+(i,), c)
    visit((0,), rows[0])
    return levels, trials

def bits(mask):
    return tuple(i for i in range(308) if mask >> i & 1)

def model_record():
    S, T, rows, columns, supports = graph()
    levels, trials = increasing(rows)
    states = sorted({b for level in levels for a, b in level})
    state_set = set(states)
    closures = []
    retained = 0
    for b in states:
        a = tuple(i for i, row in enumerate(rows) if b & row == b)
        require(a and 0 in a, "unanchored closure")
        require(sum(1 << j for j in range(308)
                    if all(rows[i] >> j & 1 for i in a)) == b,
                "literal closure intersection")
        closures.append((b, a))
        for row in rows:
            c = b & row
            if c.bit_count() >= 6:
                require(c in state_set, "missing transition")
                retained += 1
    return dict(supports=supports, rows_sha256=digest(rows),
                columns_sha256=digest(columns), classes=[len(S), len(T)],
                degree=66, tuple_counts=[len(x) for x in levels],
                tuple_trials=trials, all_tuples_sha256=digest(levels),
                states=len(states), states_sha256=digest(closures),
                transitions=len(states)*308, retained_transitions=retained,
                closure_histogram=sorted(Counter((len(a), b.bit_count())
                                                for b, a in closures).items()),
                cores5=len(levels[5]), max_rows=max(len(a) for b, a in closures),
                max_five_common=max(b.bit_count() for a, b in levels[5]),
                max_six_common=max(b.bit_count() for a, b in levels[6]))

# State membership is deliberately a whole-set check, never a successful-case list.
def complete_model_record():
    return model_record()
