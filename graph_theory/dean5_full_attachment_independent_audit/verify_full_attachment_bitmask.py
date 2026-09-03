#!/usr/bin/env python3
"""Independent verifier for the Dean-5 full-attachment census.

This implementation does not read the distributed certificate or import its
verifier.  Simple core paths are represented only by (visited-set, endpoint)
states, two-link existence is decided by disjoint bitmasks, and the global
search is an exact maximum-coverage clique search.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from itertools import combinations, product


CORE = tuple(range(8))
X = (0, 2, 4, 6)
Y = (1, 3, 5, 7)
CLASSES = (X, Y)
BOUNDARY = {tuple(sorted((v, (v + 1) % 8))) for v in CORE}
CORES = {
    "T_A": BOUNDARY | {(0, 3), (3, 6)},
    "T_B": BOUNDARY | {(0, 3), (4, 7)},
}
D2_ROOTS = tuple(combinations(X, 2)) + tuple(combinations(Y, 2))
CORE_MASK = sum(1 << v for v in CORE)


@dataclass(frozen=True, order=True)
class Atom:
    kind: int
    roots: tuple[int, ...]
    port: int
    phase: int


@dataclass(frozen=True)
class Configuration:
    kind: int
    roots: tuple[int, ...]
    atoms: tuple[Atom, ...]
    covered: int


class MaskGraph:
    """A tiny simple graph with subset-state path and linkage queries."""

    def __init__(self, edges: set[tuple[int, int]]):
        normalized = {tuple(sorted(edge)) for edge in edges}
        assert all(a != b for a, b in normalized)
        self.edges = frozenset(normalized)
        self.order = 1 + max(v for edge in normalized for v in edge)
        adjacency = [0] * self.order
        for a, b in normalized:
            adjacency[a] |= 1 << b
            adjacency[b] |= 1 << a
        self.adjacency = tuple(adjacency)

    @cache
    def path_masks(self, start: int, finish: int) -> frozenset[int]:
        """Visited-vertex masks of all simple start--finish paths.

        The dynamic-programming state is (visited mask, last vertex).  Two
        paths with the same state are interchangeable for every later query,
        so no path ordering or certificate witness is retained.
        """
        initial = (1 << start, start)
        seen = {initial}
        frontier = [initial]
        answer: set[int] = set()
        while frontier:
            mask, last = frontier.pop()
            if last == finish:
                answer.add(mask)
                continue
            available = self.adjacency[last] & ~mask
            while available:
                bit = available & -available
                available ^= bit
                state = (mask | bit, bit.bit_length() - 1)
                if state not in seen:
                    seen.add(state)
                    frontier.append(state)
        return frozenset(answer)

    @cache
    def path_residues(self, start: int, finish: int) -> frozenset[int]:
        return frozenset((mask.bit_count() - 1) % 5 for mask in self.path_masks(start, finish))

    @cache
    def linkage_residues(
        self, left: tuple[int, int], right: tuple[int, int]
    ) -> frozenset[int]:
        """Total lengths mod 5 of vertex-disjoint two-path linkages."""
        answer: set[int] = set()
        for targets in (right, right[::-1]):
            first = self.path_masks(left[0], targets[0])
            second = self.path_masks(left[1], targets[1])
            for p_mask in first:
                for q_mask in second:
                    if p_mask & q_mask == 0:
                        answer.add((p_mask.bit_count() + q_mask.bit_count() - 2) % 5)
        return frozenset(answer)


def increments(kind: int) -> tuple[int, ...]:
    assert kind in (1, 2)
    return (0, 2, 4) if kind == 1 else (0, 2)


def terminal_pairs(atom: Atom) -> tuple[tuple[int, int], ...]:
    return tuple((root, atom.port) for root in atom.roots if root != atom.port)


def locally_allowed(graph: MaskGraph, atom: Atom) -> bool:
    # A d=2 secondary foot may coincide with one selected root, but the other
    # root still supplies a genuine terminal pair.  The coincident root's
    # trivial core path is also a legitimate local closing path.
    if not terminal_pairs(atom):
        return False
    for root in atom.roots:
        for core_length in graph.path_residues(root, atom.port):
            for extra in increments(atom.kind):
                if (atom.phase + extra + 2 + core_length) % 5 == 0:
                    return False
    return True


def atoms_for(graph: MaskGraph, kind: int, roots: tuple[int, ...]) -> tuple[Atom, ...]:
    return tuple(
        atom
        for port in CORE
        for phase in range(5)
        if locally_allowed(graph, (atom := Atom(kind, roots, port, phase)))
    )


@cache
def atom_pair_allowed(graph: MaskGraph, left: Atom, right: Atom) -> bool:
    """Whether the relaxed data fail to force a two-component zero-cycle."""
    if right < left:
        return atom_pair_allowed(graph, right, left)
    for left_pair in terminal_pairs(left):
        for right_pair in terminal_pairs(right):
            for linkage in graph.linkage_residues(left_pair, right_pair):
                for left_extra, right_extra in product(
                    increments(left.kind), increments(right.kind)
                ):
                    if (
                        left.phase
                        + left_extra
                        + right.phase
                        + right_extra
                        + 4
                        + linkage
                    ) % 5 == 0:
                        return False
    return True


def configurations(
    graph: MaskGraph, kind: int, require_three: bool = False
) -> tuple[Configuration, ...]:
    root_sets = tuple((v,) for v in CORE) if kind == 1 else D2_ROOTS
    answer: list[Configuration] = []
    for roots in root_sets:
        options: dict[int, list[Atom]] = {}
        for atom in atoms_for(graph, kind, roots):
            options.setdefault(atom.port, []).append(atom)
        ports = tuple(sorted(options))
        choices = tuple((None, *options[port]) for port in ports)
        for selected in product(*choices):
            atoms = tuple(atom for atom in selected if atom is not None)
            if not atoms:
                continue
            covered = sum(1 << v for v in roots)
            for atom in atoms:
                covered |= 1 << atom.port
            if require_three and covered.bit_count() < 3:
                continue
            answer.append(Configuration(kind, roots, atoms, covered))
    return tuple(answer)


def configurations_compatible(
    graph: MaskGraph, left: Configuration, right: Configuration
) -> bool:
    return all(atom_pair_allowed(graph, a, b) for a in left.atoms for b in right.atoms)


def maximum_coverage(
    graph: MaskGraph,
    nodes: tuple[Configuration, ...],
    *,
    fixed: Configuration | None = None,
    base_covered: int = 0,
    forbidden: int = 0,
) -> int:
    """Maximum core coverage by an admissible family of >=2 components.

    Nodes are component configurations and edges mean pairwise compatibility.
    A repeated all-d=2 configuration is needed only when it is the sole chosen
    node; otherwise repetition changes neither compatibility nor coverage.
    """
    nodes = tuple(node for node in nodes if node.covered & forbidden == 0)
    if fixed is not None and fixed.covered & forbidden:
        return -1
    nodes = tuple(
        node
        for node in nodes
        if fixed is None or configurations_compatible(graph, fixed, node)
    )
    count = len(nodes)
    adjacency = [0] * count
    self_allowed = [False] * count
    for i, left in enumerate(nodes):
        self_allowed[i] = configurations_compatible(graph, left, left)
        for j in range(i + 1, count):
            if configurations_compatible(graph, left, nodes[j]):
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i

    covered = base_covered | (0 if fixed is None else fixed.covered)
    best = -1
    ceiling = (CORE_MASK & ~forbidden).bit_count()

    def family_size_ok(chosen_count: int, only: int | None) -> bool:
        if fixed is not None:
            return chosen_count >= 1
        if chosen_count >= 2:
            return True
        return chosen_count == 1 and only is not None and self_allowed[only]

    def visit(candidates: int, union: int, chosen_count: int, only: int | None) -> bool:
        nonlocal best
        if family_size_ok(chosen_count, only):
            best = max(best, (union & CORE_MASK).bit_count())
            if best == ceiling:
                return True

        possible = union
        bits = candidates
        while bits:
            bit = bits & -bits
            bits ^= bit
            possible |= nodes[bit.bit_length() - 1].covered
        if (possible & CORE_MASK).bit_count() <= best:
            return False

        remaining = candidates
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            index = bit.bit_length() - 1
            next_only = index if chosen_count == 0 else None
            if visit(
                remaining & adjacency[index],
                union | nodes[index].covered,
                chosen_count + 1,
                next_only,
            ):
                return True
        return False

    visit((1 << count) - 1, covered, 0, None)
    return best


def mode_maximum(
    graph: MaskGraph,
    mode: str,
    *,
    require_three: bool = False,
    base_covered: int = 0,
    forbidden: int = 0,
) -> int:
    d2 = configurations(graph, 2, require_three)
    if mode == "all-d2":
        return maximum_coverage(
            graph, d2, base_covered=base_covered, forbidden=forbidden
        )
    assert mode == "mixed"
    answer = -1
    for d1 in configurations(graph, 1, require_three):
        answer = max(
            answer,
            maximum_coverage(
                graph,
                d2,
                fixed=d1,
                base_covered=base_covered,
                forbidden=forbidden,
            ),
        )
    return answer


def with_edges(base: set[tuple[int, int]], extra: set[tuple[int, int]]) -> MaskGraph:
    return MaskGraph(base | {tuple(sorted(edge)) for edge in extra})


def range_text(values: list[int]) -> str:
    return str(values[0]) if min(values) == max(values) else f"{min(values)}..{max(values)}"


def audit_core(name: str, displayed: set[tuple[int, int]]) -> list[str]:
    graph = MaskGraph(displayed)
    d1_count = sum(len(atoms_for(graph, 1, (v,))) for v in CORE)
    d2_count = sum(len(atoms_for(graph, 2, roots)) for roots in D2_ROOTS)
    expected_atoms = {"T_A": (8, 34), "T_B": (8, 32)}
    if (d1_count, d2_count) != expected_atoms[name]:
        raise RuntimeError(
            f"{name}: atom counts {(d1_count, d2_count)} != {expected_atoms[name]}"
        )
    lines = [name, f"  locally allowed atoms: d1={d1_count}, d2={d2_count}"]

    displayed_results: dict[tuple[str, bool], int] = {}
    for require_three in (False, True):
        for mode in ("all-d2", "mixed"):
            displayed_results[mode, require_three] = mode_maximum(
                graph, mode, require_three=require_three
            )
    expected_displayed = {
        "T_A": {
            ("all-d2", False): 6,
            ("mixed", False): 6,
            ("all-d2", True): 6,
            ("mixed", True): -1,
        },
        "T_B": {
            ("all-d2", False): 6,
            ("mixed", False): 4,
            ("all-d2", True): 6,
            ("mixed", True): -1,
        },
    }
    if displayed_results != expected_displayed[name]:
        raise RuntimeError(
            f"{name}: displayed maxima {displayed_results} != {expected_displayed[name]}"
        )
    lines.append(
        "  displayed maxima: "
        + ", ".join(
            f"{mode}{'+A>=3' if requirement else ''}="
            f"{displayed_results[mode, requirement]}"
            for requirement in (False, True)
            for mode in ("all-d2", "mixed")
        )
    )

    scenario_values: dict[tuple[str, str], list[int]] = {}

    def record(case: str, mode: str, value: int, required: int) -> None:
        assert value < required, (name, case, mode, value, required)
        scenario_values.setdefault((case, mode), []).append(value)

    # Type I, R empty: every exterior component has at least three core feet.
    for mode in ("all-d2", "mixed"):
        record("Type I, R empty", mode, displayed_results[mode, True], 7)

    # Type II, R empty: U is the uncovered same-class smoothing pair.  Insert
    # its forced complete opposite-class adjacency and the genuine theta path.
    for uncovered in D2_ROOTS:
        extra: set[tuple[int, int]] = set()
        for u in uncovered:
            opposite = Y if u in X else X
            extra.update((u, z) for z in opposite)
            extra.add((8, u))
        augmented = with_edges(displayed, extra)
        forbidden = sum(1 << u for u in uncovered)
        for mode in ("all-d2", "mixed"):
            value = mode_maximum(augmented, mode, forbidden=forbidden)
            record("Type II, R empty", mode, value, 6)

    # Type I, one low R vertex: its genuine neighborhood has size three or four.
    for color_class in CLASSES:
        for size in (3, 4):
            for neighborhood in combinations(color_class, size):
                augmented = with_edges(displayed, {(8, z) for z in neighborhood})
                base = sum(1 << z for z in neighborhood)
                for mode in ("all-d2", "mixed"):
                    value = mode_maximum(
                        augmented, mode, require_three=True, base_covered=base
                    )
                    record("Type I, |R|=1", mode, value, 8)

    # Type II, one R vertex complete to a core color class.
    for color_class in CLASSES:
        augmented = with_edges(displayed, {(8, z) for z in color_class})
        base = sum(1 << z for z in color_class)
        for mode in ("all-d2", "mixed"):
            value = mode_maximum(augmented, mode, base_covered=base)
            record("Type II, |R|=1", mode, value, 7)

    # Type II, both theta-neighbors in R; 10 is the genuine theta vertex.
    for color_class in CLASSES:
        extra = {(p, z) for p in (8, 9) for z in color_class} | {(10, 8), (10, 9)}
        augmented = with_edges(displayed, extra)
        base = sum(1 << z for z in color_class)
        for mode in ("all-d2", "mixed"):
            value = mode_maximum(augmented, mode, base_covered=base)
            record("Type II, |R|=2", mode, value, 8)

    expected_scenarios = {
        ("Type I, R empty", "all-d2"): (6, 6),
        ("Type I, R empty", "mixed"): (-1, -1),
        ("Type II, R empty", "all-d2"): (-1, -1),
        ("Type II, R empty", "mixed"): (-1, -1),
        ("Type I, |R|=1", "all-d2"): (6, 6),
        ("Type I, |R|=1", "mixed"): (-1, -1),
        ("Type II, |R|=1", "all-d2"): (6, 6),
        ("Type II, |R|=1", "mixed"): (-1, -1),
        ("Type II, |R|=2", "all-d2"): (-1, -1),
        ("Type II, |R|=2", "mixed"): (-1, -1),
    }
    observed_scenarios = {
        key: (min(values), max(values)) for key, values in scenario_values.items()
    }
    if observed_scenarios != expected_scenarios:
        raise RuntimeError(
            f"{name}: scenario ranges {observed_scenarios} != {expected_scenarios}"
        )

    for (case, mode), values in scenario_values.items():
        lines.append(f"  {case} / {mode}: {range_text(values)}")
    lines.append(f"  structural rows checked: {sum(map(len, scenario_values.values()))}")
    return lines


def self_test() -> None:
    square = MaskGraph({(0, 1), (1, 2), (2, 3), (0, 3)})
    assert square.path_masks(0, 2) == frozenset({0b0111, 0b1101})
    assert square.path_residues(0, 0) == frozenset({0})
    assert square.linkage_residues((0, 2), (1, 3)) == frozenset({2})
    assert square.path_masks(0, 2) == square.path_masks(2, 0)


def main() -> None:
    self_test()
    lines: list[str] = []
    for name, edges in CORES.items():
        lines.extend(audit_core(name, set(edges)))
    lines.append("FINAL SURVIVORS: []")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
