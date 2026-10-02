"""Finite literal controls; the universal result is an ordinary proof.

Run python3 -B check.py, or python3 -O -B check.py. Standard library only.
The optional --emit mode prints the compact expected record without loading it.
No assertion is used, so optimization cannot disable a check.
"""
from itertools import combinations
import json
from pathlib import Path
import sys

from branches import branch_masks, memberships, three_tail_phases


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def triple(H, mixed=False):
    """Literal pair-and-third witness, independent of the matching partition."""
    by = {d: [0] * d for d in (3, 5, 7, 9)}
    for i, y in enumerate(H):
        for d in by:
            by[d][y % d] |= 1 << i
    conflicts = [by[5][y % 5] | by[7][y % 7] | by[9][y % 9] for y in H]
    full = (1 << len(H)) - 1
    for i, mask in enumerate(conflicts):
        remaining = full & ~mask & ~((1 << (i + 1)) - 1)
        while remaining:
            bit = remaining & -remaining
            j = bit.bit_length() - 1
            third = full & ~(mask | conflicts[j])
            if mixed and H[i] % 3 == H[j] % 3:
                third &= ~by[3][H[i] % 3]
            if third:
                k = (third & -third).bit_length() - 1
                return (H[i], H[j], H[k])
            remaining ^= bit
    return None


def direct_memberships(H):
    """Definition-level predicate, without importing the mask construction."""
    answer = ["small87"] if len(H) <= 87 else []
    for a, b in combinations(range(5), 2):
        if all(y % 5 == a or y % 5 == b for y in H):
            answer.append(f"rows{a}{b}")
    for c in (1, 2):
        if all(y % 3 == c for y in H):
            answer.append(f"color{c}")
    return tuple(answer)


def rejected(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return
    raise ValueError("Missing-hypothesis/domain control was accepted")


def run():
    U = [y for y in range(315) if y % 9]
    P = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
    X = [x for x in range(2520) if x % 8 == 4
         and all(x % n != a for n, a in P)]
    require(len(X) == 280 and sorted(x % 315 for x in X) == U,
            "Literal prescribed-prefix parent universe")
    base = [n for n in range(8, 2521) if 2520 % n == 0
            and n not in {n for n, a in P}]
    all_unused = [n for n in range(8, 10081) if 10080 % n == 0
                  and n not in {n for n, a in P}]
    tail = sorted(n * d for n in (16, 32) for d in range(1, 316) if 315 % d == 0)
    require(len(base) == 36 and len(tail) == 24 and len(all_unused) == 60
            and sorted(base + tail) == all_unused,
            "Original BASE/TAIL ownership")
    mask_rows = branch_masks()
    require(len(mask_rows) == 13 and len({name for name, m, cap in mask_rows}) == 13,
            "Thirteen distinct named cases")
    require([len(m) for name, m, cap in mask_rows] == [280] + [112] * 10 + [105] * 2
            and [cap for name, m, cap in mask_rows] == [87] + [None] * 12,
            "Literal branch domains and cap")
    calls = 0

    def match(H, a):
        nonlocal calls
        actual = memberships(H, a)
        require(actual == direct_memberships(H), "Branch mask disagrees with definition")
        calls += 1
        return actual

    templates = stars_points = mandatory15 = 0
    summaries = []
    for a in range(21):
        V = [y for y in U if y % 21 != a]
        cells = {(y % 7, y % 9) for y in V}
        sizes = []
        for k in range(8):
            E = [(b, c) for b, c in cells if (b + c - 1) % 8 == k]
            require(len(E) in (6, 7) and len({b for b, c in E}) == len(E)
                    and len({c for b, c in E}) == len(E), "Cell matching")
            sizes.append(len(E))
        require(sum(sizes) == len(cells) and sizes.count(7) >= 5, "Color partition")
        bound = len(cells) + 32
        require(bound == (86 if a % 3 == 0 else 85), "Abstract bound")
        for alpha in range(5):
            for b in range(7):
                if b == a % 7:
                    continue
                H = [y for y in V if y % 5 == alpha or y % 7 == b]
                require(len(H) == bound and len({y % 5 for y in H}) == 5
                        and triple(H) is None, "Literal equality-template failure")
                require(match(H, a) == ("small87",), "Equality template branch")
                for phase15 in range(15):
                    hit = sum(y % 15 == phase15 for y in H)
                    require(hit >= 2, "Original15 unexpectedly avoids equality shape")
                    mandatory15 += 1
                templates += 1
                stars_points += len(H)
        for pair in combinations(range(5), 2):
            H = [y for y in V if y % 5 in pair]
            require(triple(H) is None and match(H, a) == (f"rows{pair[0]}{pair[1]}",),
                    "Two-row branch")
        for color in (0, 1, 2):
            H = [y for y in V if y % 3 == color]
            require(triple(H, mixed=True) is None, "Monochromatic mixed triple")
            require(match(H, a) == (("small87",) if color == 0 else (f"color{color}",)),
                    "Color branch")
        small = V[:87]
        require("small87" in match(small, a), "Small case missing")
        require(triple(small, mixed=True) is not None,
                "Membership alone unexpectedly certifies A4")
        two = [y for y in V if y % 5 in (3, 4)]
        damage = two + [next(y for y in V if y % 5 not in (3, 4))]
        require(match(damage, a) == () and triple(damage, mixed=True) is not None,
                "Invalid high nonrow control")
        summaries.append({"phase21": a, "abstract_bound": bound,
                          "strict_complete36_BASE_bound": bound - 1,
                          "color_matching_sizes": sizes})

    # Exhaust all3x4 bipartite graphs, comparing literal triple matchings
    # against direct enumeration of every cover of at most two vertices.
    bipartite = 0
    for bits in range(1 << 12):
        edges = [(i // 4, i % 4) for i in range(12) if bits >> i & 1]
        matched3 = any(len({a for a, b in T}) == 3 and len({b for a, b in T}) == 3
                       for T in combinations(edges, 3))
        hascover2 = any(all(left >> a & 1 or right >> b & 1 for a, b in edges)
                       for left in range(1 << 3) for right in range(1 << 4)
                       if left.bit_count() + right.bit_count() <= 2)
        require(hascover2 == (not matched3), "Bipartite two-cover control failed")
        bipartite += 1

    physical = 0
    tail_records = []
    for color in (0, 1, 2):
        phases = three_tail_phases(color)
        require({n for n, a in phases} == {16, 32, 96}
                and all(n in tail and n not in base for n, a in phases),
                "Three distinct free original TAIL resources")
        a96 = dict(phases)[96]
        require(a96 % 32 == 28 and a96 % 3 == color, "Original96 CRT phase")
        X = [x for x in range(10080) if x % 8 == 4 and x % 3 == color]
        require(len(X) == 420 and all(any(x % n == a for n, a in phases) for x in X),
                "Literal three-tail bridge")
        require(any(all(x % n != a for n, a in phases[:2]) for x in X),
                "Omitting96 does not expose remaining leaf")
        physical += len(X)
        tail_records.append({"color": color, "phases": phases, "targets": len(X)})

    unpruned = [y for y in U if y % 5 == 0 or y % 7 == 0]
    require(len(unpruned) == 88 and triple(unpruned) is None
            and direct_memberships(unpruned) == (), "Missing21 premise countercontrol")
    for a in range(21):
        rejected(memberships, unpruned, a)
    bad_domain = [([1, 1], 0), ([0], 1), ([315], 0), ([9], 0), ([-1], 0),
                  ([True], 0), ([1], -1), ([1], 21), ([1], True), ([1], 1)]
    for H, a in bad_domain:
        rejected(memberships, H, a)
    for color in (-1, 3, True):
        rejected(three_tail_phases, color)
    require(match([], 0) == tuple(name for name, m, cap in mask_rows), "Empty case overlap")
    return {"agent": "six-covering-3", "role": "researcher",
            "equality_templates": templates, "equality_point_checks": stars_points,
            "original15_phase_intersections": mandatory15,
            "all_bipartite3x4_graphs": bipartite, "three_tail_physical_points": physical,
            "branch_mask_definition_comparisons": calls,
            "missing21_phase_rejections": 21, "malformed_domain_rejections": len(bad_domain),
            "bad_tail_color_rejections": 3,
            "phase21_summaries": summaries, "three_tail_phases": tail_records,
            "ordinary_universal_and_equality_proof_unformalized": True,
            "all280_point_subsets_enumerated": False,
            "actual_BASE_stage_equality_or_full_cover_claimed": False,
            "branch_membership_certifies_A4": False,
            "global_Lmin8_bound_changed": False}


if __name__ == "__main__":
    record = run()
    if sys.argv[1:] == ["--emit"]:
        print(json.dumps(record, sort_keys=True))
    elif not sys.argv[1:]:
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        # Convert tuples through canonical JSON before comparing literal outputs.
        require(json.loads(json.dumps(record)) == expected, "Expected record mismatch")
        print(json.dumps(record, sort_keys=True))
    else:
        raise ValueError("Use no options or --emit")
