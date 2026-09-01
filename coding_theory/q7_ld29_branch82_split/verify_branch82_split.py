#!/usr/bin/env python3
"""Verify the family split and build exact Q7 LD29 branch-82 CNFs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import pathlib
import sys
import time


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_branch79_split"))

import verify_branch79_split as core  # noqa: E402


BRANCH = 82
EXPECTED_MASK = 7100
EXPECTED_VARIABLES = 10432
EXPECTED_BASE_CLAUSES = 183619
EXPECTED_D24_SURVIVORS = (
    (4, (1, 1, 5, 5), 0, 2),
    (5, (1, 1, 1, 1, 1, 1, 1, 5), 0, 0),
    (5, (1, 1, 1, 4, 5), 0, 0),
    (5, (1, 1, 5, 5), 2, 0),
    (5, (2, 5, 5), 1, 0),
)
EXPECTED_SINGLE_REPRESENTATIVES = (63, 126, 127)
EXPECTED_PAIR_REPRESENTATIVES = (
    (15, 23),
    (15, 50),
    (15, 63),
    (15, 76),
    (15, 95),
    (15, 113),
    (15, 127),
    (27, 63),
    (27, 95),
    (27, 123),
    (27, 127),
    (50, 63),
    (50, 76),
    (50, 95),
    (50, 126),
    (63, 95),
    (63, 119),
    (63, 125),
    (63, 126),
)

EXPECTED_DIGESTS = {
    "branch82-d25": "0cdb0542b0c0c50166829a4e6b8fa45f0889de3a3c91626306f4937a8be96c07",
    "branch82-full-f63": "dc704304a64e26c6b1380adcb84cf1217830ac0383799d03884b1e917663d67f",
    "branch82-full-f126": "95ecd3aa1e95278211c21456e037e39b425b13aa9aef03d6c7f655b4bd17360c",
    "branch82-full-f127": "ef539060b77ec875eedec175a2f6384122707024515c659db97b08aa91e57c52",
    "branch82-pair-f15-g23": "0dd927cddb194f15e2a896ea7cb8380872240bff80b55ee4ddb7a1cd4d1b0f67",
    "branch82-pair-f15-g50": "b9ed9fcef0b771a1733b77c7d64dce7c1182dca661d9e829d068d4669a1e7eae",
    "branch82-pair-f15-g63": "a43aef06645c4870978ea73bb58c93c20daaa32b8882e648e80b01577439682c",
    "branch82-pair-f15-g76": "ed4576d823b034811d6ca5f78e4035801efda881f32826feaea7e77591b09fea",
    "branch82-pair-f15-g95": "15646f1375d76683cad12531c9bca63b1173b0c8f5739c821d3b6b7f0f10eb26",
    "branch82-pair-f15-g113": "527473511755411e585bb2d8d62a59a21cf2545cab9d2d93fd73c678a232bb80",
    "branch82-pair-f15-g127": "fb64cf5ee588c3d90e37a4243ba6d3b59e8c53f9baa56e2859d960f8ec6c7564",
    "branch82-pair-f27-g63": "2b397b8d16f38e3034ec1bdca0c440dddf31742a80d6bba4d909a0dc1308002f",
    "branch82-pair-f27-g95": "e0122491c9750a95d3e352daaf40ebdbf20751a995055aad67520488c8813c1a",
    "branch82-pair-f27-g123": "99b47655eec2b6f66c7981ed8cad880e1c243373cf40650a841db226cea4673d",
    "branch82-pair-f27-g127": "08c150465ed48c352f5eff9e2b5ee496b442b34cf36ee4d86c67c2d7a2c0d9fd",
    "branch82-pair-f50-g63": "f9437bd1e28f89919d1351db88792a1f65343c6ffff92feea68b7eeb847bff48",
    "branch82-pair-f50-g76": "c167d197a09c5f2204b8c15dc32ab768f433b7e53198e0b4fed990de065ec39a",
    "branch82-pair-f50-g95": "1a7b3b8263ffc518cd433f2760856cf45a4ba300fb000d1ea58364376b8c4e34",
    "branch82-pair-f50-g126": "178ea87a1f3f0c47e6a99daf54f7a6efc1221a101f7e8323425d4692f064e864",
    "branch82-pair-f63-g95": "1e7315ee271f913ebbfb9aa1215eb82d7e899fea967ee66c35e7d8de3d37363d",
    "branch82-pair-f63-g119": "ca9a1a06f1cd609d7658e38666b4b2c9788ea770343e402bf5feb254bbcf9752",
    "branch82-pair-f63-g125": "fd476e38154ad736ca3b135c4e3cfc001446f8a822ee4a7ac067f01b516647b1",
    "branch82-pair-f63-g126": "08042430ccea8fa95f6d3de3c168ec830783efdc797feaf00112d2312374cd57",
}


def configure_core() -> None:
    core.BRANCH = BRANCH
    core.EXPECTED_MASK = EXPECTED_MASK


def permute_word(word: int, permutation: tuple[int, ...]) -> int:
    """Apply a permutation of coordinates 1,...,6, fixing orphan coordinate 0."""
    image = word & 1
    for coordinate, target in enumerate(permutation):
        if word & (1 << (coordinate + 1)):
            image |= 1 << (target + 1)
    return image


def local_automorphisms(mask: int) -> tuple[tuple[int, ...], ...]:
    edges = core.selected_edges(mask)
    return tuple(
        permutation
        for permutation in itertools.permutations(range(6))
        if {
            tuple(sorted((permutation[first], permutation[second])))
            for first, second in edges
        }
        == set(edges)
    )


def orbit_representatives(
    objects: set[int] | set[tuple[int, int]],
    automorphisms: tuple[tuple[int, ...], ...],
) -> tuple[int, ...] | tuple[tuple[int, int], ...]:
    remaining = set(objects)
    representatives = []
    while remaining:
        representative = min(remaining)
        if isinstance(representative, int):
            orbit = {
                permute_word(representative, permutation)
                for permutation in automorphisms
            }
        else:
            first, second = representative
            orbit = {
                tuple(
                    sorted(
                        (
                            permute_word(first, permutation),
                            permute_word(second, permutation),
                        )
                    )
                )
                for permutation in automorphisms
            }
        assert orbit <= objects
        remaining -= orbit
        representatives.append(representative)
    return tuple(representatives)


def separation_cost(first: int, second: int) -> int | None:
    """Missing slots forced jointly by two defect-five family centers."""
    distance = core.hamming_distance(first, second)
    if distance <= 1:
        return None
    if distance in (2, 3):
        return 2
    if distance == 4:
        return 3
    return 0


def all_two_slack_pairs(mask: int) -> set[tuple[int, int]]:
    pairs = set()
    for first, second in itertools.combinations(range(128), 2):
        first_cost = core.center_cost(first, mask)
        second_cost = core.center_cost(second, mask)
        joint_cost = separation_cost(first, second)
        if first_cost is None or second_cost is None or joint_cost is None:
            continue
        # The individual local-cost slots and the between-center slots need
        # not be proved disjoint: imposing the two necessary inequalities
        # separately deliberately leaves a superset of the genuine cases.
        if first_cost + second_cost <= 2 and joint_cost <= 2:
            pairs.add((first, second))
    return pairs


def verify_split(mask: int) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...]]:
    data = core.local_data(mask)
    assert data == ((3, 3, 3, 3, 3, 3), 2, 12, 42, 22, 2)
    assert core.raw_states(mask, 23) == ((5, (5, 6), 0, 1),)
    assert not tuple(
        filter(core.survives_defect_six_occupancy, core.raw_states(mask, 23))
    )
    survivors = tuple(
        filter(core.survives_defect_six_occupancy, core.raw_states(mask, 24))
    )
    assert survivors == EXPECTED_D24_SURVIVORS

    automorphisms = local_automorphisms(mask)
    assert len(automorphisms) == 12

    full_centers = {center for center in range(128) if core.center_cost(center, mask) == 0}
    assert full_centers == {63, 95, 111, 119, 123, 125, 126, 127}
    single_representatives = orbit_representatives(full_centers, automorphisms)
    assert single_representatives == EXPECTED_SINGLE_REPRESENTATIVES

    # The q=4 state has two full defect-five families.  A selected father
    # would put at least seven codewords in its full family, above the global
    # budget two, so both fathers are noncodewords.  Zero free slack makes
    # both centers have local cost zero, hence weight at least six.  Full
    # centers must be separated by at least five, whereas two words of weight
    # at least six in Q_7 have distance at most two.
    assert all(center.bit_count() >= 6 for center in full_centers)
    assert all(
        core.hamming_distance(first, second) <= 2
        for first, second in itertools.combinations(full_centers, 2)
    )

    pair_cases = all_two_slack_pairs(mask)
    assert len(pair_cases) == 129
    pair_representatives = orbit_representatives(pair_cases, automorphisms)
    assert pair_representatives == EXPECTED_PAIR_REPRESENTATIVES

    print(
        f"PASS branch={BRANCH} mask={mask} local_data={data} "
        f"automorphisms={len(automorphisms)} d24_states={len(survivors)} "
        f"single_orbits={len(single_representatives)} "
        f"pair_cases={len(pair_cases)} pair_orbits={len(pair_representatives)}"
    )
    return single_representatives, pair_representatives


def add_full_center(cnf, center: int) -> None:
    """Impose a full noncodeword defect-five family centered at ``center``."""
    units = {center: False}
    units.update({neighbor: True for neighbor in core.NEIGHBORS[center]})
    units.update(
        {
            word: False
            for word in range(128)
            if core.hamming_distance(center, word) in (2, 3)
        }
    )
    cnf.extend(
        [[word + 1 if selected else -(word + 1)] for word, selected in units.items()]
    )


def formula_digest(cnf) -> str:
    return hashlib.sha256(core.dimacs_bytes(cnf)).hexdigest()


def check_formula(cnf, name: str, output: pathlib.Path | None) -> None:
    digest = formula_digest(cnf)
    assert cnf.nv == EXPECTED_VARIABLES
    if EXPECTED_DIGESTS:
        assert digest == EXPECTED_DIGESTS[name]
    if output is not None:
        (output / f"{name}.cnf").write_bytes(core.dimacs_bytes(cnf))
    print(
        f"PASS formula={name} variables={cnf.nv} clauses={len(cnf.clauses)} "
        f"sha256={digest}"
    )


def solve_kissat(cnf, name: str) -> None:
    from pysat.solvers import Solver

    started = time.monotonic()
    with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
        assert not solver.solve()
    print(f"PASS formula={name} Kissat-4.0.4=UNSAT seconds={time.monotonic()-started:.3f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = core.scratch_directory(args.write_directory) if args.write_directory else None

    configure_core()
    strong, mask = core.build_with_defect_bound(25)
    assert len(strong.clauses) == EXPECTED_BASE_CLAUSES
    single_cases, pair_cases = verify_split(mask)
    formulas = [("branch82-d25", strong)]

    base, second_mask = core.build_with_defect_bound(24)
    assert second_mask == mask
    assert len(base.clauses) == EXPECTED_BASE_CLAUSES
    for center in single_cases:
        cnf = base.copy()
        add_full_center(cnf, center)
        formulas.append((f"branch82-full-f{center}", cnf))
    for first, second in pair_cases:
        cnf = base.copy()
        core.add_center_case(cnf, first, second)
        formulas.append((f"branch82-pair-f{first}-g{second}", cnf))

    for name, cnf in formulas:
        check_formula(cnf, name, output)
        if args.solve_kissat:
            solve_kissat(cnf, name)


if __name__ == "__main__":
    main()
