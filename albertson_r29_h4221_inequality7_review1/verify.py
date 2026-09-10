#!/usr/bin/env python3
"""Definition-level witness that the c_A upper bound need not be attained.

This does not attempt to realize every ambient Albertson-lane constraint.  It
checks the local component facts used at h4221 and shows that they do not imply
the equality silently required by the implementation of inequality (7).
"""

from collections import deque


A = {"a0", "a1"}
W = {"w0", "w1", "w2"}
S_R = set()

# H[A] is independent.  H[W] has components {w0,w1} and {w2}.  Both A
# vertices meet both W-components, so H[A union W] is connected.
EDGES = {
    frozenset(("w0", "w1")),
    *(frozenset((a, w)) for a in A for w in W),
}


def adjacent(x, y):
    return frozenset((x, y)) in EDGES


def components(vertices):
    vertices = set(vertices)
    answer = []
    while vertices:
        root = min(vertices)
        vertices.remove(root)
        queue = deque([root])
        component = {root}
        while queue:
            x = queue.popleft()
            found = {y for y in vertices if adjacent(x, y)}
            vertices.difference_update(found)
            component.update(found)
            queue.extend(sorted(found))
        answer.append(frozenset(component))
    return sorted(answer, key=lambda c: tuple(sorted(c)))


def main():
    assert not any(adjacent(x, y) for x in A for y in A if x != y)
    w_components = components(W)
    full_components = components(A | W)
    p = len(w_components)
    c_a = len(full_components)
    iso = sum(
        all(w in S_R for w in W if adjacent(a, w))
        for a in A
    )
    rho_a = min(sum(adjacent(a, w) for w in W) for a in A)
    s_r = len(S_R)
    c_a_upper = min(iso + p, len(A))
    exact_lhs = (c_a - iso) * max(0, rho_a - s_r)
    substituted_lhs = (c_a_upper - iso) * max(0, rho_a - s_r)

    assert w_components == [frozenset({"w0", "w1"}), frozenset({"w2"})]
    assert full_components == [frozenset(A | W)]
    assert (len(A), p, iso, c_a, c_a_upper) == (2, 2, 0, 1, 2)
    assert (rho_a, len(W), exact_lhs, substituted_lhs) == (3, 3, 3, 6)
    assert exact_lhs <= len(W) < substituted_lhs

    print("H[A] independent: yes")
    print("components of H[W]:", p)
    print("actual c_A:", c_a)
    print("min(iso+p,a):", c_a_upper)
    print("inequality (7), exact quantities: %d <= %d" % (exact_lhs, len(W)))
    print("implementation substitution: %d > %d" % (substituted_lhs, len(W)))
    print("VERDICT: c_A <= min(iso+p,a) cannot be substituted as equality in (7)")


if __name__ == "__main__":
    main()
