#!/usr/bin/env python3
"""Fast definition-level checks for the h4231 implementation defects."""

from collections import deque


def components(vertices, edges):
    remaining = set(vertices)
    answer = []
    while remaining:
        root = min(remaining)
        remaining.remove(root)
        queue = deque([root])
        component = {root}
        while queue:
            x = queue.popleft()
            found = {y for y in remaining if frozenset((x, y)) in edges}
            remaining.difference_update(found)
            component.update(found)
            queue.extend(sorted(found))
        answer.append(frozenset(component))
    return sorted(answer, key=lambda c: tuple(sorted(c)))


def check_ca_substitution():
    a_vertices = {"a0", "a1"}
    w_vertices = {"w0", "w1", "w2"}
    edges = {
        frozenset(("w0", "w1")),
        *(frozenset((a, w)) for a in a_vertices for w in w_vertices),
    }
    p = len(components(w_vertices, edges))
    c_a = len(components(a_vertices | w_vertices, edges))
    iso = 0
    rho_a = 3
    c_a_upper = min(iso + p, len(a_vertices))
    exact_lhs = (c_a - iso) * rho_a
    substituted_lhs = (c_a_upper - iso) * rho_a
    assert (p, c_a, c_a_upper) == (2, 1, 2)
    assert exact_lhs == len(w_vertices) < substituted_lhs
    print("c_A witness: actual lhs 3 <= |W| 3; substituted lhs 6 > |W| 3")


def check_repeated_block_cap():
    # A genuine configuration shape appearing in the target enumeration:
    # |R|=25 and partitioning block multiset (17,8,8).  Select A inside one
    # 8-block with a=1 and take u=4.  The other 8-block must remain in the cap.
    r_size, mult, selected_q, a, u = 25, (17, 8, 8), 8, 1, 4
    rho = lambda q: max(0, q + r_size - 29)
    selected_rho = rho(selected_q)
    target = ((selected_q - a) * min(selected_rho, u)
              + sum(q * min(rho(q), u) for q in mult if q != selected_q))
    exact = (sum(q * min(rho(q), u) for q in mult)
             - a * min(selected_rho, u))
    omitted_equal_block = selected_q * min(selected_rho, u)
    assert (target, exact, omitted_equal_block) == (96, 128, 32)
    print("repeated-block cap: target 96; exact 128; omitted equal block 32")


def main():
    check_ca_substitution()
    check_repeated_block_cap()
    print("VERDICT: both source substitutions can make a necessary-condition scan too strong")


if __name__ == "__main__":
    main()
