#!/usr/bin/env python3
"""Private simplex attachment compiler and direct exact audit; Python >=3.10."""
from collections import Counter, defaultdict, deque
from hashlib import sha256
from heapq import heappop, heappush
from itertools import combinations
from pathlib import Path
import argparse
import json


def require(test, message):
    if not test:
        raise ValueError(message)


def subsets(s):
    s = sorted(s)
    return {frozenset(t) for k in range(len(s)+1) for t in combinations(s, k)}


def complex_faces(facets):
    require(bool(facets), "nonvoid complex")
    return set().union(*(subsets(f) for f in facets))


def ordered(faces):
    return sorted(faces, key=lambda f: (len(f), tuple(sorted(f))))


def mobius(faces):
    """Defining upper recurrence, independent of the attachment formula."""
    mu = {}
    for f in reversed(ordered(faces)):
        mu[f] = -1-sum(v for g, v in mu.items() if f < g)
    return mu


def replay(faces, word, optimal=True):
    mu = mobius(faces)
    state, counts, net = set(), Counter(), Counter()
    for k, f in enumerate(word):
        require(f in faces and mu[f] != 0, ("forbidden move", k, sorted(f)))
        ideal = {g for g in faces if g <= f}
        on = state & ideal
        require(not on or on == ideal, ("nonmonochromatic move", k))
        counts[f] += 1
        net[f] += -1 if on else 1
        state.symmetric_difference_update(ideal)
    require(state == faces, "not winning")
    require(all(net[f] == -mu[f] for f in faces), "wrong net counts")
    if optimal:
        require(all(counts[f] == abs(mu[f]) for f in faces), "not facewise optimal")
    return mu


def attach(faces, word, ears):
    """ears is [(old face F, private new nonempty vertex set W), ...]."""
    mu = replay(faces, word)
    vertices = set().union(*faces)
    used_new = set()
    groups = defaultdict(list)
    outfaces = set(faces)
    simplices = []
    for f, w in ears:
        require(f in faces, "attachment base is not an old face")
        require(bool(w), "empty private vertex set")
        require(not (w & vertices), "private vertices are old")
        require(not (w & used_new), "private vertices are shared")
        used_new.update(w)
        s = f | w
        groups[f].append(s)
        simplices.append(s)
        outfaces.update(subsets(s))
    # The first min(a_F,(-mu(F))_+) occurrences may be replaced.
    assigned = {f: deque(ss[:max(-mu[f], 0)]) for f, ss in groups.items()}
    replaced = set()
    outword = []
    for f in word:
        if mu[f] < 0 and assigned.get(f):
            s = assigned[f].popleft()
            outword.append(s)
            replaced.add(s)
        else:
            outword.append(f)
    for (f, _), s in zip(ears, simplices):
        if s not in replaced:
            outword.extend((f, s))
    return outfaces, outword


def clear(ideals):
    if not ideals:
        return []
    last = ideals[-1]
    return clear(ideals[:-1])+list(reversed(clear([s & last for s in ideals[:-1]])))+[last]


def pure_shelling_word(facets):
    """Prior shelling compiler, with supplied order validated directly."""
    require(len({len(f) for f in facets}) == 1, "base shelling not pure")
    old, word = set(), []
    for f in facets:
        new = subsets(f)-old
        require(bool(new), "redundant facet")
        r = frozenset.intersection(*new)
        require(new == {g for g in subsets(f) if r <= g}, "not an interval shelling")
        word += clear([f-{v} for v in sorted(r)])+[f]
        old.update(subsets(f))
    replay(old, word)
    return old, word


def shortest(faces, costs=None):
    """Definition-level BFS or Dijkstra; no compiler or formula used."""
    require(len(faces) <= 18, "state graph exceeds fixture bound")
    fs, mu = ordered(faces), mobius(faces)
    moves = [(sum(1 << j for j, g in enumerate(fs) if g <= f), f)
             for f in fs if mu[f]]
    goal = (1 << len(fs))-1
    if costs is None:
        queue, dist = deque([0]), {0: 0}
        while queue:
            s = queue.popleft()
            if s == goal:
                return dist[s], len(dist)
            for mask, f in moves:
                if s & mask in (0, mask):
                    ns = s ^ mask
                    if ns not in dist:
                        dist[ns] = dist[s]+1
                        queue.append(ns)
    else:
        require(all(costs[f] >= 0 for _, f in moves), "negative cost")
        heap, dist = [(0, 0)], {0: 0}
        while heap:
            d, s = heappop(heap)
            if d != dist[s]:
                continue
            if s == goal:
                return d, len(dist)
            for mask, f in moves:
                if s & mask in (0, mask):
                    ns, nd = s ^ mask, d+costs[f]
                    if ns not in dist or nd < dist[ns]:
                        dist[ns] = nd
                        heappush(heap, (nd, ns))
    raise ValueError("unreachable goal")


def cone_boundary(q):
    b = frozenset(range(1, q+1))
    return pure_shelling_word([frozenset({0}) | (b-{v}) for v in sorted(b)])


def encoded(word):
    return [sorted(f) for f in word]


def audit(name, faces, word, ears, search=False):
    oldmu = replay(faces, word)
    out, newword = attach(faces, word, ears)
    newmu = replay(out, newword)
    a = Counter(f for f, _ in ears)
    ss = {f | w for f, w in ears}
    require(all(newmu[f] == oldmu[f]+a[f] for f in faces), "old coefficient update")
    require(all(newmu[f] == (-1 if f in ss else 0) for f in out-faces),
            "new-face coefficient formula")
    predicted = len(ears)+sum(abs(oldmu[f]+a[f]) for f in faces)
    update = len(word)+2*sum(max(oldmu[f]+a[f], 0)-max(oldmu[f], 0) for f in faces)
    require(len(newword) == predicted == update, "length formula")
    record = {"name": name, "old_faces": len(faces), "new_faces": len(out),
              "attachments": [[sorted(f), sorted(w)] for f, w in ears],
              "old_length": len(word), "new_length": len(newword),
              "changed_coefficients": [[sorted(f), oldmu[f], newmu[f]]
                                       for f in ordered(a)],
              "word_sha256": sha256(json.dumps(encoded(newword),
                                     separators=(",", ":")).encode()).hexdigest()}
    if search:
        optimum, explored = shortest(out)
        require(optimum == predicted, "BFS disagrees")
        record["BFS"] = {"optimum": optimum, "states_discovered": explored}
        # Zero and unequal positive costs; exact integer objective.
        costs = {f: (len(f)+sum(f)) % 4 for f in out}
        optimum, explored = shortest(out, costs)
        actual = sum(costs[f] for f in newword)
        bound = sum(costs[f]*abs(newmu[f]) for f in out)
        require(optimum == actual == bound, "weighted Dijkstra disagrees")
        record["Dijkstra"] = {"optimum": optimum, "states_discovered": explored}
        record["word"] = encoded(newword)
    return record, out, newword


def run():
    records = []
    tri = frozenset({0, 1, 2})
    simple = complex_faces([tri])
    # Test negative, zero and positive old coefficients; repeat and nest bases.
    cases = [
        ("negative_to_zero", [(tri, frozenset({3}))]),
        ("negative_through_zero", [(tri, frozenset({3})), (tri, frozenset({4}))]),
        ("zero_vertex", [(frozenset({0}), frozenset({3}))]),
        ("empty_base", [(frozenset(), frozenset({3}))]),
        ("nonshellable_pure_pair", [(frozenset({0}), frozenset({3, 4}))]),
        ("nested_bases", [(frozenset({0}), frozenset({3})),
                          (frozenset({0, 1}), frozenset({4}))]),
    ]
    for name, ears in cases:
        size = len(simple | set().union(*(subsets(f | w) for f, w in ears)))
        rec, _, _ = audit(name, simple, [tri], ears, search=size <= 18)
        records.append(rec)
    cycle, cw = pure_shelling_word([frozenset({0, 1}), frozenset({1, 2}),
                                    frozenset({0, 2})])
    records.append(audit("positive_vertex_and_negative_empty", cycle, cw,
        [(frozenset({0}), frozenset({3})), (frozenset(), frozenset({4}))],
        search=True)[0])
    k4, kw = pure_shelling_word([frozenset(e) for e in combinations(range(4), 2)])
    require(mobius(k4)[frozenset()] == -3, "multiplicity-three base control")
    for m in (2, 3, 4):
        records.append(audit("coefficient_minus_three_%d_attachments" % m, k4, kw,
            [(frozenset(), frozenset({4+i})) for i in range(m)], search=True)[0])
    records.append(audit("reversed_optimal_input", k4, list(reversed(kw)),
        [(frozenset(), frozenset({4})), (frozenset(), frozenset({5}))], search=True)[0])
    # Simultaneous attachments at every old face exercise all signs and nesting.
    f, w = cone_boundary(3)
    ears = [(h, frozenset({10+i})) for i, h in enumerate(ordered(f))]
    records.append(audit("all_base_faces_simultaneously", f, w, ears)[0])
    # Infinite-family formula: these are controls, not a parameter census.
    for q, m in [(3, 1), (3, 2), (3, 4), (5, 1), (5, 3), (7, 2)]:
        f, w = cone_boundary(q)
        ears = [(frozenset({0}), frozenset({q+i+1})) for i in range(m)]
        rec, out, nw = audit("cone_boundary_q%d_m%d" % (q, m), f, w, ears,
                              search=q == 3 and m <= 2)
        require(rec["new_length"] == 2**q+2*m-3, "cancellation family formula")
        records.append(rec)
    # Sequential attachment can use a newly created face from an earlier step.
    rec, f1, w1 = audit("sequential_first", simple, [tri],
                       [(frozenset({0}), frozenset({3}))], search=True)
    records.append(rec)
    records.append(audit("sequential_second", f1, w1,
        [(frozenset({0, 3}), frozenset({4}))], search=True)[0])

    rejected = []
    def reject(name, fn):
        try:
            fn()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("negative control accepted: "+name)
    reject("not_an_old_face", lambda: attach(simple, [tri],
        [(frozenset({9}), frozenset({3}))]))
    reject("no_new_vertex", lambda: attach(simple, [tri],
        [(frozenset({0}), frozenset())]))
    reject("old_private_vertex", lambda: attach(simple, [tri],
        [(frozenset({0}), frozenset({1}))]))
    reject("shared_private_vertex", lambda: attach(simple, [tri],
        [(frozenset({0}), frozenset({3})), (frozenset({1}), frozenset({3}))]))
    reject("winning_but_not_optimal_input", lambda: attach(simple, [tri, tri, tri], []))
    f, w = cone_boundary(3)
    out, nw = attach(f, w, [(frozenset({0}), frozenset({4}))])
    reject("naive_append_uses_cancelled_face",
           lambda: replay(out, w+[frozenset({0}), frozenset({0, 4})]))
    # Direct obstruction to the coefficient claim when privacy is dropped.
    shared = complex_faces([frozenset({0, 2}), frozenset({1, 2})])
    require(mobius(shared)[frozenset({2})] == 1, "shared-vertex control")
    # Missing base optimality is rejected even though the input word wins.
    replay(simple, [tri, tri, tri], optimal=False)
    return {"schema": 1, "fixtures": records, "fixture_count": len(records),
            "BFS_fixtures": sum("BFS" in x for x in records),
            "Dijkstra_fixtures": sum("Dijkstra" in x for x in records),
            "moves_replayed_in_outputs": sum(x["new_length"] for x in records),
            "negative_controls_rejected": rejected,
            "shared_new_vertex_coefficient": 1,
            "trust_boundary": "Finite checks corroborate the universal written proof."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.emit:
        print(json.dumps(result, indent=2))
        return
    raw = Path(__file__).with_name("expected.json").read_bytes()
    require(result == json.loads(raw), "frozen evidence mismatch")
    print(json.dumps({"status": "PASS", "fixtures": result["fixture_count"],
        "BFS": result["BFS_fixtures"], "Dijkstra": result["Dijkstra_fixtures"],
        "output_moves": result["moves_replayed_in_outputs"],
        "negative_controls": len(result["negative_controls_rejected"]),
        "expected_sha256": sha256(raw).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
