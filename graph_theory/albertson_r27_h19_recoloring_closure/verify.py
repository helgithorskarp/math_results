#!/usr/bin/env python3
"""Exact audit of the Albertson r=27 h=19 recolouring closure."""

from hashlib import sha256


B = 19
ORDER = 19
EDGES = 56


def recolouring_transitions():
    """Return weights whose moves preserve the required class profiles."""
    all_active = tuple([B] * 8)
    one_zero = tuple([0] + [B] * 8)

    active_to_active = []
    active_to_zero = []
    for weight in range(1, B + 1):
        moved_all = list(all_active)
        moved_all[0] -= weight
        moved_all[1] += weight
        if sorted(moved_all) == sorted(all_active):
            active_to_active.append(weight)

        moved_active = list(one_zero)
        moved_active[1] -= weight
        moved_active[2] += weight
        if sorted(moved_active) == sorted(one_zero):
            active_to_active.append(weight)

        moved_zero = list(one_zero)
        moved_zero[1] -= weight
        moved_zero[0] += weight
        if sorted(moved_zero) == sorted(one_zero):
            active_to_zero.append(weight)

    assert active_to_active == []
    assert active_to_zero == [B]
    return tuple(active_to_active), tuple(active_to_zero)


def degree_audit():
    """Check every possible count of zero-incidence high vertices."""
    rows = []
    for zero_count in range(ORDER + 1):
        positive_count = ORDER - zero_count
        floor = 7 * positive_count + 12 * zero_count
        rows.append((zero_count, positive_count, floor))
        assert floor == 133 + 5 * zero_count
        assert floor > 2 * EDGES
    return tuple(rows)


def main():
    transitions = recolouring_transitions()
    rows = degree_audit()
    payload = repr((transitions, rows, 2 * EDGES)).encode()
    digest = sha256(payload).hexdigest()
    print("PASS Albertson r=27 h=19 recolouring closure")
    print(f"transitions={transitions}; handshake_ceiling={2 * EDGES}")
    print(f"minimum_degree_sum={rows[0][2]}; certificate_sha256={digest}")


if __name__ == "__main__":
    main()
