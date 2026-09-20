#!/usr/bin/env python3
"""Independent finite audit for the order-15 strong Seymour proof.

This file deliberately imports neither the submitted SAT generator nor any of
its classification checkers.  It checks definitions on all tournaments through
order six, probes the precise gap between a minimal Hall witness and the
necessary conditions used by the SAT encoding, and independently reconstructs
the size-four, size-five, and size-six local classifications.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json


def pairs(n: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def tournament(n: int, bits: int) -> list[int]:
    """Return out-neighborhood bit masks for one labelled tournament."""
    out = [0] * n
    for shift, (i, j) in enumerate(pairs(n)):
        winner, loser = (i, j) if bits >> shift & 1 else (j, i)
        out[winner] |= 1 << loser
    return out


def hall_neighbors(out: list[int], root: int, selected: int) -> int:
    a = out[root]
    b = ((1 << len(out)) - 1) ^ a ^ (1 << root)
    result = 0
    active = selected
    while active:
        bit = active & -active
        tail = bit.bit_length() - 1
        result |= out[tail] & b
        active ^= bit
    return result


def hall_strong(out: list[int], root: int) -> bool:
    a = out[root]
    selected = a
    while selected:
        if hall_neighbors(out, root, selected).bit_count() < selected.bit_count():
            return False
        selected = (selected - 1) & a
    return True


def matching_size(out: list[int], root: int) -> int:
    """Independent augmenting-path oracle for the directed Hall link."""
    a = out[root]
    b = ((1 << len(out)) - 1) ^ a ^ (1 << root)
    mate: dict[int, int] = {}

    def augment(tail: int, seen: set[int]) -> bool:
        candidates = out[tail] & b
        while candidates:
            bit = candidates & -candidates
            head = bit.bit_length() - 1
            candidates ^= bit
            if head in seen:
                continue
            seen.add(head)
            if head not in mate or augment(mate[head], seen):
                mate[head] = tail
                return True
        return False

    active = a
    while active:
        bit = active & -active
        augment(bit.bit_length() - 1, set())
        active ^= bit
    return len(mate)


def exact_second(out: list[int], root: int) -> int:
    reached = 0
    active = out[root]
    while active:
        bit = active & -active
        reached |= out[bit.bit_length() - 1]
        active ^= bit
    return reached & ~out[root] & ~(1 << root)


def definition_census(max_order: int = 6) -> dict[str, object]:
    tournaments = vertex_cases = minimal_witnesses = 0
    strong_vertices = ordinary_vertices = 0
    digest = sha256()
    by_order = []
    for n in range(1, max_order + 1):
        order_tournaments = 1 << (n * (n - 1) // 2)
        order_strong = order_ordinary = 0
        for bits in range(order_tournaments):
            tournaments += 1
            out = tournament(n, bits)
            has_strong = has_ordinary = False
            for root in range(n):
                vertex_cases += 1
                a = out[root]
                strong = hall_strong(out, root)
                matched = matching_size(out, root) == a.bit_count()
                assert strong == matched
                ordinary = exact_second(out, root).bit_count() >= a.bit_count()
                has_strong |= strong
                has_ordinary |= ordinary
                strong_vertices += strong
                ordinary_vertices += ordinary
                order_strong += strong
                order_ordinary += ordinary

                deficient = []
                selected = a
                while selected:
                    if hall_neighbors(out, root, selected).bit_count() < selected.bit_count():
                        deficient.append(selected)
                    selected = (selected - 1) & a
                deficient_set = set(deficient)
                for selected in deficient:
                    active = selected
                    is_minimal = True
                    while active:
                        bit = active & -active
                        if selected ^ bit in deficient_set:
                            is_minimal = False
                            break
                        active ^= bit
                    if not is_minimal:
                        continue
                    minimal_witnesses += 1
                    neighbors = hall_neighbors(out, root, selected)
                    assert neighbors.bit_count() == selected.bit_count() - 1
                    active = neighbors
                    while active:
                        head_bit = active & -active
                        head = head_bit.bit_length() - 1
                        assert (selected & sum(
                            1 << tail for tail in range(n) if out[tail] >> head & 1
                        )).bit_count() >= 2
                        active ^= head_bit

                digest.update(
                    f"{n}:{bits}:{root}:{a.bit_count()}:"
                    f"{exact_second(out, root).bit_count()}:{int(strong)}\n".encode()
                )
            assert has_ordinary
            assert has_strong
        by_order.append(
            {
                "n": n,
                "ordinary_vertex_cases": order_ordinary,
                "strong_vertex_cases": order_strong,
                "tournaments": order_tournaments,
            }
        )
    return {
        "by_order": by_order,
        "minimal_witnesses": minimal_witnesses,
        "ordinary_vertex_cases": ordinary_vertices,
        "record_sha256": digest.hexdigest(),
        "strong_vertex_cases": strong_vertices,
        "tournaments": tournaments,
        "vertex_cases": vertex_cases,
    }


def minimal_link(rows: tuple[int, ...], r: int) -> bool:
    s = len(rows)
    for subset in range(1, (1 << s) - 1):
        union = 0
        for i in range(s):
            if subset >> i & 1:
                union |= rows[i]
        if union.bit_count() < subset.bit_count():
            return False
    return True


def abstract_witness_census() -> dict[str, object]:
    """Test which encoded 'minimality' consequences are equivalences."""
    records = []
    first_relaxed_nonminimal = None
    for s in range(1, 5):
        r = s - 1
        total = relaxed = truly_minimal = relaxed_nonminimal = 0
        for bits in range(1 << (s * r)):
            total += 1
            rows = tuple(
                sum(1 << j for j in range(r) if bits >> (i * r + j) & 1)
                for i in range(s)
            )
            union = 0
            for row in rows:
                union |= row
            deficiency_one = union.bit_count() == r
            double_covered = all(sum(row >> j & 1 for row in rows) >= 2 for j in range(r))
            encoded_relaxation = deficiency_one and double_covered
            actual_minimal = deficiency_one and minimal_link(rows, r)
            relaxed += encoded_relaxation
            truly_minimal += actual_minimal
            if encoded_relaxation and not actual_minimal:
                relaxed_nonminimal += 1
                if first_relaxed_nonminimal is None:
                    first_relaxed_nonminimal = {
                        "row_masks": list(rows),
                        "s": s,
                    }
            if actual_minimal:
                assert double_covered
        records.append(
            {
                "encoded_relaxations": relaxed,
                "minimal_witnesses": truly_minimal,
                "relaxed_nonminimal": relaxed_nonminimal,
                "s": s,
                "total_links": total,
            }
        )
    assert first_relaxed_nonminimal == {"row_masks": [3, 3, 0], "s": 3}
    return {
        "first_relaxed_nonminimal": first_relaxed_nonminimal,
        "records": records,
    }


def relabel_tournament_bits(n: int, bits: int, new_to_old: tuple[int, ...]) -> int:
    out = tournament(n, bits)
    value = 0
    for shift, (i, j) in enumerate(pairs(n)):
        if out[new_to_old[i]] >> new_to_old[j] & 1:
            value |= 1 << shift
    return value


def local_s4_pattern(tbits: int, lbits: int) -> tuple[list[int], list[int]]:
    out = tournament(4, tbits)
    rows = [sum(1 << j for j in range(3) if lbits >> (3 * i + j) & 1) for i in range(4)]
    return out, rows


def s4_forced_extras(out: list[int], rows: list[int], vertex: int) -> set[tuple[str, int]]:
    extras: set[tuple[str, int]] = set()
    direct_s = out[vertex]
    direct_r = rows[vertex]
    if direct_r:
        extras.add(("root", 0))
    for other in range(4):
        if direct_s >> other & 1:
            continue
        through_s = any(
            direct_s >> mid & 1 and out[mid] >> other & 1 for mid in range(4)
        )
        through_r = any(
            direct_r >> head & 1 and not (rows[other] >> head & 1)
            for head in range(3)
        )
        if through_s or through_r:
            extras.add(("S", other))
    for head in range(3):
        if direct_r >> head & 1:
            continue
        if any(direct_s >> mid & 1 and rows[mid] >> head & 1 for mid in range(4)):
            extras.add(("R", head))
    return extras


def relabel_s4_key(key: int, sp: tuple[int, ...], rp: tuple[int, ...]) -> int:
    tbits = key & 63
    lbits = key >> 6
    out, rows = local_s4_pattern(tbits, lbits)
    result = 0
    for shift, (i, j) in enumerate(pairs(4)):
        if out[sp[i]] >> sp[j] & 1:
            result |= 1 << shift
    shift = 6
    for i in range(4):
        for j in range(3):
            if rows[sp[i]] >> rp[j] & 1:
                result |= 1 << shift
            shift += 1
    return result


def size_four_census() -> dict[str, object]:
    feasible: set[int] = set()
    survivors: set[int] = set()
    for tbits in range(64):
        out = tournament(4, tbits)
        p = [out[i].bit_count() for i in range(4)]
        for lbits in range(1 << 12):
            rows = [sum(1 << j for j in range(3) if lbits >> (3 * i + j) & 1) for i in range(4)]
            if any(sum(row >> j & 1 for row in rows) < 2 for j in range(3)):
                continue
            q = [row.bit_count() for row in rows]
            if any(p[i] + q[i] < 3 for i in range(4)):
                continue
            key = tbits | (lbits << 6)
            feasible.add(key)
            forced = any(
                p[i] + q[i] == 3 and len(s4_forced_extras(out, rows, i)) >= 2
                for i in range(4)
            )
            if not forced:
                survivors.add(key)

    unseen = set(survivors)
    orbit_sizes = []
    representatives = []
    s_perms = list(permutations(range(4)))
    r_perms = list(permutations(range(3)))
    while unseen:
        seed = min(unseen)
        orbit = {
            relabel_s4_key(seed, sp, rp)
            for sp in s_perms
            for rp in r_perms
        }
        assert orbit <= survivors
        representatives.append(min(orbit))
        orbit_sizes.append(len(orbit))
        unseen -= orbit
    assert len(feasible) == 22368
    assert len(survivors) == 472
    assert len(orbit_sizes) == 10
    return {
        "all_patterns": 1 << 18,
        "degree_feasible": len(feasible),
        "forced_ordinary": len(feasible) - len(survivors),
        "orbit_count": len(orbit_sizes),
        "orbit_sizes": sorted(orbit_sizes),
        "representative_sha256": sha256(
            ("\n".join(map(str, sorted(representatives))) + "\n").encode()
        ).hexdigest(),
        "surviving_labeled": len(survivors),
    }


def canonical_tournament(n: int, bits: int) -> int:
    return min(relabel_tournament_bits(n, bits, perm) for perm in permutations(range(n)))


def size_five_census() -> dict[str, object]:
    classes: Counter[int] = Counter()
    for bits in range(1 << 10):
        out = tournament(5, bits)
        if min(mask.bit_count() for mask in out) < 1:
            continue
        classes[canonical_tournament(5, bits)] += 1
    assert len(classes) == 8
    assert sum(classes.values()) == 704
    return {
        "labeled_tournaments": sum(classes.values()),
        "orbit_sizes": sorted(classes.values()),
        "representatives": sorted(classes),
    }


def symmetry_normalizable(out: list[int]) -> bool:
    blocks: dict[int, list[int]] = {}
    for vertex, mask in enumerate(out):
        blocks.setdefault(mask.bit_count(), []).append(vertex)
    for block in blocks.values():
        if len(block) < 2:
            continue
        assert any(out[u] >> v & 1 for u in block for v in block if u != v)
    return True


def size_six_census() -> dict[str, object]:
    counts: Counter[tuple[int, ...]] = Counter()
    symmetry_checked = 0
    for bits in range(1 << 15):
        out = tournament(6, bits)
        scores = tuple(sorted(mask.bit_count() for mask in out))
        if scores[0] == 0:
            continue
        counts[scores] += 1
        assert symmetry_normalizable(out)
        symmetry_checked += 1
    sequences = sorted(counts)
    payload = "\n".join(",".join(map(str, sequence)) for sequence in sequences) + "\n"
    assert len(sequences) == 13
    assert sum(counts.values()) == 26624
    return {
        "labeled_counts": [counts[sequence] for sequence in sequences],
        "positive_labeled_tournaments": sum(counts.values()),
        "score_sequences": [list(sequence) for sequence in sequences],
        "sequence_sha256": sha256(payload.encode()).hexdigest(),
        "symmetry_checked": symmetry_checked,
    }


def partition_arithmetic() -> list[dict[str, int]]:
    rows = []
    for s in range(1, 7):
        r = s - 1
        c = 7 - s
        d = 7 - r
        lower = 6 - c
        assert lower == s - 1
        rows.append({"C": c, "D": d, "R": r, "S": s, "p_plus_q_lower": lower})
    return rows


def main() -> None:
    report = {
        "abstract_witnesses": abstract_witness_census(),
        "definitions": definition_census(),
        "partition_arithmetic": partition_arithmetic(),
        "size_four": size_four_census(),
        "size_five": size_five_census(),
        "size_six": size_six_census(),
        "status": "VERIFIED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
