#!/usr/bin/env python3
"""Independent blocker audit for the hubbed three-clique NF recurrence.

A type is (x, X', y, Y', z, Z'), where the hub coordinates are bits and
the primed coordinates count ordinary vertices.  This checker computes the
NF operator as complements of minimal transversals.  It does not use the
reviewed source's middle-coordinate threshold/delta implementation.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from math import comb, prod

Type = tuple[int, int, int, int, int, int]
State = frozenset[Type]


def capacities(n: int, m: int, ell: int) -> Type:
    if min(n, m, ell) < 3:
        raise ValueError("the reviewed theorem assumes n,m,ell >= 3")
    return (1, n - 1, 1, m - 1, 1, ell - 1)


def all_types(caps: Type):
    return product(*(range(c + 1) for c in caps))


def predecessors(t: Type):
    for q, value in enumerate(t):
        if value:
            yield t[:q] + (value - 1,) + t[q + 1 :]


def disjoint_representatives_exist(t: Type, u: Type, caps: Type) -> bool:
    """Whether a fixed representative of type t misses some one of type u."""
    if t[0] and u[0] or t[2] and u[2] or t[4] and u[4]:
        return False
    return all(t[q] + u[q] <= caps[q] for q in (1, 3, 5))


def hits_every_orbit_member(t: Type, facets: State, caps: Type) -> bool:
    return all(not disjoint_representatives_exist(t, u, caps) for u in facets)


def nf_types(facets: State, caps: Type) -> State:
    """NF via complements of minimal transversals of the invariant clutter."""
    minimal_transversals: list[Type] = []
    for t in all_types(caps):
        if not hits_every_orbit_member(t, facets, caps):
            continue
        if all(not hits_every_orbit_member(p, facets, caps) for p in predecessors(t)):
            minimal_transversals.append(t)
    return frozenset(tuple(c - a for c, a in zip(caps, t)) for t in minimal_transversals)


P0: State = frozenset(
    {
        (1, 1, 0, 0, 0, 0),
        (0, 2, 0, 0, 0, 0),
        (0, 0, 1, 1, 0, 0),
        (0, 0, 0, 2, 0, 0),
        (0, 0, 0, 0, 1, 1),
        (0, 0, 0, 0, 0, 2),
        (1, 0, 1, 0, 0, 0),
        (0, 0, 1, 0, 1, 0),
    }
)

P1: State = frozenset(
    {
        (0, 1, 0, 1, 0, 1),
        (0, 1, 0, 1, 1, 0),
        (0, 1, 1, 0, 0, 1),
        (1, 0, 0, 1, 0, 1),
        (1, 0, 0, 1, 1, 0),
    }
)

D3: State = frozenset(
    {
        (1, 0, 1, 0, 0, 0),
        (1, 0, 0, 1, 0, 0),
        (1, 0, 0, 0, 1, 0),
        (1, 0, 0, 0, 0, 1),
        (0, 1, 1, 0, 0, 0),
        (0, 1, 0, 0, 1, 0),
        (0, 1, 0, 0, 0, 1),
        (0, 0, 1, 0, 1, 0),
        (0, 0, 1, 0, 0, 1),
        (0, 0, 0, 1, 1, 0),
    }
)

D4: State = frozenset(
    {
        (1, 1, 0, 0, 0, 0),
        (1, 0, 1, 0, 1, 0),
        (1, 0, 1, 0, 0, 1),
        (1, 0, 0, 1, 1, 0),
        (0, 2, 0, 0, 0, 0),
        (0, 1, 1, 0, 1, 0),
        (0, 1, 1, 0, 0, 1),
        (0, 1, 0, 1, 0, 0),
        (0, 0, 1, 1, 0, 0),
        (0, 0, 0, 2, 0, 0),
        (0, 0, 0, 1, 0, 1),
        (0, 0, 0, 0, 1, 1),
        (0, 0, 0, 0, 0, 2),
    }
)


def complement_types(types: State, caps: Type) -> State:
    return frozenset(tuple(c - a for c, a in zip(caps, t)) for t in types)


def startup_states(n: int, m: int, ell: int) -> list[State]:
    caps = capacities(n, m, ell)
    p2 = frozenset(
        {
            (0, 0, 1, m - 1, 1, ell - 1),
            (1, 0, 1, 0, 1, ell - 1),
            (1, n - 1, 0, 0, 1, ell - 1),
            (1, n - 1, 1, m - 1, 0, 0),
            (1, n - 1, 1, 0, 1, 0),
        }
    )
    return [P0, P1, p2, complement_types(D3, caps), complement_types(D4, caps)]


def epsilon(t: Type, caps: Type) -> int:
    full_block = any(
        t[h] == 1 and t[o] == caps[o]
        for h, o in ((0, 1), (2, 3), (4, 5))
    )
    contains_bridge = bool(t[0] and t[2] or t[2] and t[4])
    if full_block or contains_bridge:
        return 1
    blocks_met = sum(bool(t[h] or t[o]) for h, o in ((0, 1), (2, 3), (4, 5)))
    return -1 if blocks_met <= 1 else 0


def kappa(t: Type, caps: Type) -> int:
    return sum(t) + epsilon(t, caps)


def full_blocks(caps: Type) -> tuple[Type, Type, Type]:
    return (
        (1, caps[1], 0, 0, 0, 0),
        (0, 0, 1, caps[3], 0, 0),
        (0, 0, 0, 0, 1, caps[5]),
    )


def B(s: int, caps: Type) -> State:
    layer = {t for t in all_types(caps) if kappa(t, caps) == s}
    layer.update(q for q in full_blocks(caps) if sum(q) == s + 1)
    return frozenset(layer)


def predicted_orbit(n: int, m: int, ell: int) -> list[State]:
    caps = capacities(n, m, ell)
    N = n + m + ell
    return startup_states(n, m, ell) + [B(s, caps) for s in range(N - 2, 1, -1)]


def assert_startup(n: int, m: int, ell: int) -> dict[str, object]:
    caps = capacities(n, m, ell)
    states = startup_states(n, m, ell)
    expected = states[1:] + [B(n + m + ell - 2, caps)]
    for index, (before, after) in enumerate(zip(states, expected)):
        got = nf_types(before, caps)
        assert got == after, (n, m, ell, index, sorted(got ^ after))
    return {
        "case": [n, m, ell],
        "type_box": 8 * n * m * ell,
        "startup_state_sizes": [len(s) for s in states],
        "top_layer_size": len(expected[-1]),
    }


def assert_full_orbit(n: int, m: int, ell: int) -> dict[str, object]:
    caps = capacities(n, m, ell)
    orbit = predicted_orbit(n, m, ell)
    for index, before in enumerate(orbit):
        after = orbit[(index + 1) % len(orbit)]
        got = nf_types(before, caps)
        assert got == after, (n, m, ell, index, sorted(got ^ after))
    assert len(orbit) == n + m + ell + 2
    assert all(max(map(sum, state)) >= 3 for state in orbit[1:])
    return {
        "case": [n, m, ell],
        "period": len(orbit),
        "state_sizes": [len(s) for s in orbit],
        "facet_orbits_checked": sum(len(s) for s in orbit),
    }


def vertex_groups(n: int, m: int, ell: int):
    return (
        (0,),
        tuple(range(1, n)),
        (n,),
        tuple(range(n + 1, n + m)),
        (n + m,),
        tuple(range(n + m + 1, n + m + ell)),
    )


def expand_type(t: Type, n: int, m: int, ell: int) -> set[int]:
    choices = []
    for count, group in zip(t, vertex_groups(n, m, ell)):
        choices.append(tuple(combinations(group, count)))
    masks: set[int] = set()
    for selected in product(*choices):
        mask = 0
        for group_choice in selected:
            for vertex in group_choice:
                mask |= 1 << vertex
        masks.add(mask)
    expected = prod(comb(len(g), q) for g, q in zip(vertex_groups(n, m, ell), t))
    assert len(masks) == expected
    return masks


def expand_state(state: State, n: int, m: int, ell: int) -> set[int]:
    result: set[int] = set()
    for t in state:
        result.update(expand_type(t, n, m, ell))
    return result


def nf_labeled(facets: set[int], N: int) -> set[int]:
    """Direct Boolean-lattice definition, used only as a reduction cross-check."""
    allowed = []
    for mask in range(1 << N):
        if all(mask & facet != facet for facet in facets):
            allowed.append(mask)
    allowed_set = set(allowed)
    return {
        mask
        for mask in allowed
        if all(mask | (1 << v) not in allowed_set for v in range(N) if not mask >> v & 1)
    }


def assert_labeled_333() -> dict[str, object]:
    n = m = ell = 3
    N = 9
    orbit = predicted_orbit(n, m, ell)
    labelled_counts = []
    for index, state in enumerate(orbit):
        before = expand_state(state, n, m, ell)
        expected = expand_state(orbit[(index + 1) % len(orbit)], n, m, ell)
        got = nf_labeled(before, N)
        assert got == expected, (index, sorted(got ^ expected))
        labelled_counts.append(len(before))
    return {"case": [3, 3, 3], "states": len(orbit), "labelled_facet_counts": labelled_counts}


def canonical_hash(payload: object) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(data).hexdigest()


def run_audit() -> dict[str, object]:
    startup_cases = [(3, 3, 3), (3, 4, 5), (4, 7, 11), (8, 13, 21), (3, 25, 40)]
    full_cases = [(3, 3, 3), (3, 3, 4), (3, 4, 5), (4, 4, 4), (3, 5, 7)]
    result = {
        "method": "orbit-type minimal transversals",
        "startup": [assert_startup(*case) for case in startup_cases],
        "full_orbits": [assert_full_orbit(*case) for case in full_cases],
        "direct_boolean_lattice": assert_labeled_333(),
    }
    result["audit_sha256"] = canonical_hash(result)
    return result


def main() -> None:
    result = run_audit()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("VERIFIED independent blocker audit")


if __name__ == "__main__":
    main()
