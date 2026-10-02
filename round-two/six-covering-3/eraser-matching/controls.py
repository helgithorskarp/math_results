"""Small complete algorithm controls and concrete certificate damage checks."""

from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from model import (divisors, eraser_graph, matching_certificate,
                   weighted_cover)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def right_cover_cost(rows, resource_count, left_weight, right_weight):
    best = None
    for right in range(1 << resource_count):
        left_count = sum(bool(row & ~right) for row in rows)
        cost = left_weight * left_count + right_weight * right.bit_count()
        if best is None or cost < best:
            best = cost
    return best


def small_graphs():
    graph_count = allocation_count = strict_two_layer = 0
    for target_count in range(4):
        for resource_count in range(4):
            labels = list(range(1, resource_count + 1))
            allocations = list(product(range(-1, target_count), repeat=resource_count))
            for code in range(1 << (target_count * resource_count)):
                graph = [[j + 1 for j in range(resource_count)
                          if code & (1 << (i * resource_count + j))]
                         for i in range(target_count)]
                graph_count += 1
                best_matching = best_erased = 0
                for allocation in allocations:
                    allocation_count += 1
                    used = [(i, j + 1) for j, i in enumerate(allocation) if i != -1]
                    if len({i for i, j in used}) == len(used) and all(j in graph[i] for i, j in used):
                        best_matching = max(best_matching, len(used))
                    erased = 0
                    for i in range(target_count):
                        assigned = [j + 1 for j, dest in enumerate(allocation) if dest == i]
                        if len(assigned) >= 2 or (len(assigned) == 1 and assigned[0] in graph[i]):
                            erased += 1
                    best_erased = max(best_erased, erased)
                cert = matching_certificate(graph, labels)
                require(cert["value"] == best_matching, "augmenting path differs from full assignments")
                require(len(cert["cover_left"]) + len(cert["cover_right"]) == best_matching,
                        "cover cardinality")
                require(all(i in cert["cover_left"] or d in cert["cover_right"]
                            for i, row in enumerate(graph) for d in row), "cover edge")
                require(best_erased == min(target_count, (resource_count + best_matching) // 2),
                        "one-layer erasure bound/control sharpness")
                masks = [sum(1 << (d - 1) for d in row) for row in graph]
                if right_cover_cost(masks, resource_count, 4, 3) < 4 * target_count - 3 * resource_count:
                    strict_two_layer += 1
                    require(not abstract_two_layer_completion(graph, resource_count),
                            "two-layer inequality rejects permissible abstract completion")
    require(not abstract_two_layer_completion([[1]] * 4, 4), "triangle abstract control")
    require(abstract_two_layer_completion([[1, 2, 3, 4]] * 4, 4), "positive abstract control")
    return {"graphs": graph_count, "resource_assignments": allocation_count,
            "strict_two_layer_graphs": strict_two_layer, "special_two_layer_controls": 2}


def abstract_two_layer_completion(graph, resource_count):
    # Permissive relaxation: two assigned resources may erase any target;
    # one may erase only along a graph edge. Any changed survivor may gain
    # every eraser edge. Literal congruence actions are a subset of this model.
    for allocation in product(range(-1, len(graph)), repeat=resource_count):
        assigned = [[j + 1 for j, dest in enumerate(allocation) if dest == i]
                    for i in range(len(graph))]
        erasable = [i for i, row in enumerate(assigned)
                    if len(row) >= 2 or (len(row) == 1 and row[0] in graph[i])]
        for code in range(1 << len(erasable)):
            erased = {i for j, i in enumerate(erasable) if code & (1 << j)}
            survivors = [i for i in range(len(graph)) if i not in erased]
            if not survivors:
                return True
            if 2 * len(survivors) > resource_count:
                continue  # Every nonempty final target needs an original resource.
            rows = [list(range(1, resource_count + 1)) if assigned[i] else graph[i]
                    for i in survivors for _ in range(2)]
            for final in product(range(-1, len(rows)), repeat=resource_count):
                all_erased = True
                for i, neighbors in enumerate(rows):
                    resources = [j + 1 for j, dest in enumerate(final) if dest == i]
                    if not (len(resources) >= 2 or (len(resources) == 1 and resources[0] in neighbors)):
                        all_erased = False
                        break
                if all_erased:
                    return True
    return False


def weighted_covers():
    count = 0
    for cofactor, max_parents, primes in [(15, 3, [2, 3]), (315, 3, [2])]:
        resources = divisors(cofactor)
        for m in range(max_parents + 1):
            for signatures in product(resources, repeat=m):
                fibers = [[0, g] if g < cofactor else [0] for g in signatures]
                parent_masks = [sum(1 << j for j, d in enumerate(resources) if g % d == 0)
                                for g in signatures]
                for p in primes:
                    produced = weighted_cover(cofactor, fibers, resources, p)
                    # Independent optimization over RIGHT subsets, as opposed
                    # to the producer's parent subsets.
                    alternate = right_cover_cost(parent_masks, len(resources), 2 * p * p, p + 1)
                    require(produced["value"] == alternate, "weighted cover optima differ")
                    graph = eraser_graph(cofactor, fibers, resources, p)
                    require(all(i in produced["cover_left"] or d in produced["cover_right"]
                                for i, row in enumerate(graph) for d in row), "weighted cover missing edge")
                    count += 1
    return {"weighted_parent_states": count, "right_subsets_per_315_state": 4096}


def damage_checks():
    directory = Path(__file__).resolve().parent
    original = json.loads((directory / "certificate.json").read_text())
    damaged = []

    def damage(name, edit):
        packet = deepcopy(original)
        edit(packet)
        damaged.append((name, packet))

    damage("false_toy_edge", lambda x: x["toy"]["graph"][0].append(3))
    damage("nonedge_matching", lambda x: x["toy"]["matching_certificate"]["matching"].__setitem__(0, [0, 3]))
    damage("missing_cover", lambda x: x["toy"]["weighted_cover"].__setitem__("cover_right", []))
    damage("wrong_cost", lambda x: x["toy"]["weighted_cover"].__setitem__("value", 4))
    damage("wrong_fraction", lambda x: x["toy"]["fractional_phases"][0]["phases"][0].__setitem__(2, 8))
    damage("wrong_phase", lambda x: x["toy"]["fractional_phases"][1]["phases"][0].__setitem__(0, 0))
    damage("duplicate_modulus", lambda x: x["toy"]["fractional_phases"][1].__setitem__("modulus", 8))
    damage("wrong_point_coverage", lambda x: x["toy"].__setitem__("point_coverage", [1, 1]))
    damage("terminal_duplicate_resource", lambda x: x["saturated_terminal_control"]["completion_phases"][1].__setitem__(0, 32))
    damage("terminal_wrong_phase", lambda x: x["saturated_terminal_control"]["completion_phases"][0].__setitem__(1, 0))
    damage("closed_10_phase", lambda x: x["period10080"]["prefix"][2].__setitem__(1, 0))
    damage("base_resource_count", lambda x: x["period10080"].__setitem__("unused_base_count", 35))
    damage("wrong_copy_count", lambda x: x["period10080"].__setitem__("physical_holes", 2796))
    damage("wrong_subset_cut", lambda x: x["period10080"]["subset_minimum_eraser_labels"].__setitem__("7", 6))
    with tempfile.TemporaryDirectory(prefix="eraser-damage-") as temp:
        for name, packet in damaged:
            target = Path(temp) / (name + ".json")
            target.write_text(json.dumps(packet))
            result = subprocess.run([sys.executable, "-B", str(directory / "check.py"),
                                     "--certificate", str(target)], capture_output=True, text=True, timeout=8)
            require(result.returncode != 0 and "ValueError" in result.stderr,
                    "damaged certificate accepted or unrelated failure: " + name)
    return {"rejected_concrete_damages": len(damaged)}


def stage_checks():
    from check import check_matching
    from stage import BASE_RESOURCES, PREFIX, evaluate
    for pattern in ["zero", "last", "middle"]:
        phases = [[n, 0 if pattern == "zero" else n - 1 if pattern == "last" else n // 2]
                  for n in BASE_RESOURCES]
        state = evaluate(phases)
        literal = [x for x in range(10080) if not any(x % n == a for n, a in PREFIX + phases)]
        independent = {r: sorted({x % 315 for x in literal if x % 8 == r}) for r in range(8)}
        prefixes = [r for r in range(8) if independent[r]]
        require(state["prefixes"] == prefixes and state["holes"] == [independent[r] for r in prefixes],
                "stage holes differ from literal10080-point predicates")
        graph = []
        for r in prefixes:
            for child in [r, r + 8]:
                target = [x for x in literal if x % 16 == child]
                graph.append([d for d in divisors(315)
                              if len({x % (16 * d) for x in target}) == 1])
        check_matching(graph, divisors(315), state["matching_certificate"])
        cover = state["weighted_cover"]
        require(all(i in cover["cover_left"] or d in cover["cover_right"]
                    for i, row in enumerate(graph) for d in row), "stage cover contains nonedge gap")
        require(cover["value"] == 4 * len(cover["cover_left"]) + 3 * len(cover["cover_right"]),
                "stage cover cost")
        require(state["two_layer_threshold"] == 4 * len(graph) - 36, "stage threshold")
    bad = [[], [[n, 0] for n in BASE_RESOURCES[:-1]],
           [[n, n] for n in BASE_RESOURCES], [[16, 0]] + [[n, 0] for n in BASE_RESOURCES[1:]]]
    for phases in bad:
        try:
            evaluate(phases)
        except ValueError:
            pass
        else:
            raise ValueError("malformed36-phase stage input accepted")
    return {"literal_stage_assignments": 3, "rejected_stage_inputs": len(bad)}


if __name__ == "__main__":
    result = {"graphs": small_graphs(), "weighted": weighted_covers(), "damages": damage_checks(),
              "stages": stage_checks()}
    print(json.dumps(result, sort_keys=True))
