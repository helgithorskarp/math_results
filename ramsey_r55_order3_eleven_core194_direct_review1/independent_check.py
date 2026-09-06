#!/usr/bin/env python3
"""Definition-level review of the direct 320-primary Core194 formulas.

No module from the reviewed package is imported.  Variables are recovered by
physical C3 edge orbits.  Every physical five-set is simplified directly,
the two formulas are emitted independently, and all fixed-pair relabelings
used by the coverage argument are checked.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import gc
import hashlib
import json


WORD = "100110110110110100"
EXPECTED = {
    "blue": {
        "bytes": 14_883_777,
        "sha256": "f3314485280b2080f3459774b944e010beeb175788673d53703d60cba091e84c",
        "clauses": 366_069,
        "ramsey_clauses": 366_034,
        "possible_red": 454_199,
        "possible_blue": 655_371,
    },
    "red": {
        "bytes": 14_841_387,
        "sha256": "2aa575e6b988d788f57f98abaa3728518517adc02c795ef5f75458c459e85a72",
        "clauses": 364_095,
        "ramsey_clauses": 364_068,
        "possible_red": 457_300,
        "possible_blue": 646_149,
    },
}
SOURCE_FILES = {
    "SHA256SUMS": "8957c50722503ecb09e350161a4061bf8a45872f715a71dbbd18c1f80c1c2011",
    "generate.py": "fc8b15a087b02e31a254df7b7c0314e391b27c11cfe3a54bdc4a870a1aa382e9",
    "check.py": "93298ebc771c1c4f7bb6e019eb3387986745d8394feb20ecb4f93321f3a235ef",
    "PROOF.md": "5178dd3e8e404fa02e17014a0e2e56c8b8a048b415cd958ea6a7ebd470e09888",
    "README.md": "e2bf2c0844814abe6b6b5529172381c256c713461d0ee5e1876bf1ddb6918f61",
    "result.json": "9500da9e2358316eeaece258bbce553e6df4070bc67feca3da573854094273f1",
    "verification.json": "3c7ca7dfe39bb492f27f0a6d42d897f400d08f9f9f1b6af1625b4ec3ce3f04fd",
    "boundary.json": "cb474a08b91c7d343f289c41c0c48dc0dd35b18688f1a8ca394ea9db2564159f",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def info(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def source_identity(target):
    observed = {}
    for name, wanted in SOURCE_FILES.items():
        got = info(target / name)["sha256"]
        require(got == wanted, f"reviewed source drift: {name}")
        observed[name] = got
    saved = json.loads((target / "result.json").read_text())
    require(saved["complete"] and saved["open"] == ["blue", "red"]
            and saved["excluded"] == [] and not saved["target_graph"],
            "submitted decision boundary differs")
    require(all(row["status"] == "open" and row["solver_code"] == 0
                for row in saved["cases"]), "submitted outcomes are not both open")
    return observed


def rotate(vertex):
    return vertex if vertex >= 33 else 3 * (vertex // 3) + (vertex + 1) % 3


def physical_orbits():
    remaining = set(combinations(range(43), 2))
    classes = {"moving": [], "fixed": [], "incidence": []}
    internal = {}
    while remaining:
        first = min(remaining)
        orbit = {first}
        image = tuple(sorted(map(rotate, first)))
        while image != first:
            orbit.add(image)
            image = tuple(sorted(map(rotate, image)))
        remaining -= orbit
        a, b = first
        if b < 33 and a // 3 == b // 3:
            for edge in orbit:
                internal[edge] = a < 12
        elif b < 33:
            classes["moving"].append((first, orbit))
        elif a >= 33:
            classes["fixed"].append((first, orbit))
        else:
            classes["incidence"].append((first, orbit))
    classes["moving"].sort(
        key=lambda row: (row[0][0] // 3, row[0][1] // 3,
                         (row[0][1] - row[0][0]) % 3))
    classes["fixed"].sort()
    classes["incidence"].sort(key=lambda row: (row[0][1], row[0][0] // 3))
    rows = classes["moving"] + classes["fixed"] + classes["incidence"]
    mapping = {edge: index for index, (_, orbit) in enumerate(rows, 1)
               for edge in orbit}
    require([len(classes[k]) for k in ("moving", "fixed", "incidence")] ==
            [165, 45, 110], "wrong primary orbit census")
    require(len(internal) == 33 and len(mapping) == 870
            and set(mapping.values()) == set(range(1, 321)),
            "physical pairs are not completely represented")
    return mapping, internal


def displayed_index(a, b):
    """The closed formula stated in the reviewed proof, checked but not used."""
    if b < 33:
        i, s = divmod(a, 3)
        j, t = divmod(b, 3)
        require(i != j, "internal edges are constants")
        rank = i * (21 - i) // 2 + j - i - 1
        return 1 + 3 * rank + (t - s) % 3
    if a >= 33:
        i, j = a - 33, b - 33
        return 166 + i * (19 - i) // 2 + j - i - 1
    return 211 + 11 * (b - 33) + a // 3


def check_displayed_index(mapping):
    for edge, index in mapping.items():
        require(displayed_index(*edge) == index,
                f"closed index disagrees on physical edge {edge}")
    return {"noninternal_edges_checked": len(mapping), "primary_variables": 320}


def fixed_values(color, mapping):
    require(color in ("blue", "red"), "unknown pair color")
    fixed = {}
    for position, (i, j) in enumerate(combinations(range(4), 2)):
        for offset in range(3):
            variable = mapping[(3 * i, 3 * j + offset)]
            value = WORD[3 * position + offset] == "1"
            require(variable not in fixed or fixed[variable] == value,
                    "Core194 is not orbit-invariant")
            fixed[variable] = value
    for vertex in (33, 34):
        for cycle in range(4):
            fixed[mapping[(3 * cycle, vertex)]] = False
    fixed[mapping[(33, 34)]] = color == "red"
    require(len(fixed) == 27, "wrong fixed-primary count")
    return fixed


def local_pair_lemma(mapping, internal):
    fixed = fixed_values("blue", mapping)
    core_red = {
        edge for edge in combinations(range(12), 2)
        if internal.get(edge, fixed.get(mapping.get(edge)))
    }
    classes = Counter()
    k4 = {}
    pair_checks = 0
    for mask in range(16):
        red = set(core_red)
        red.update((a, 14) for a in range(12) if mask & (1 << (a // 3)))
        witnesses = []
        for subset in combinations(range(15), 5):
            colors = {edge in red for edge in combinations(subset, 2)}
            pair_checks += 10
            if len(colors) == 1:
                witnesses.append((next(iter(colors)), subset))
        wanted_red = mask.bit_count() >= 3
        witness = next((subset for red_color, subset in witnesses
                        if red_color == wanted_red), None)
        require(witness is not None, f"unobstructed third-fixed signature {mask}")
        classes["red" if wanted_red else "blue"] += 1
        if mask.bit_count() == 3:
            omitted = next(i for i in range(4) if not mask & (1 << i))
            require(14 in witness, "red witness omits the common fixed vertex")
            k4[str(omitted)] = list(witness[:-1])
    require(classes == Counter({"blue": 11, "red": 5}),
            "wrong local obstruction split")
    return {"signatures": 16, "five_sets": 16 * 3003,
            "literal_pair_colors_checked": pair_checks,
            "obstructions": dict(classes), "red_k4_by_omitted_triangle": k4}


def formula(color, mapping, internal, output):
    fixed = fixed_values(color, mapping)
    known = dict(internal)
    known.update((edge, fixed[index]) for edge, index in mapping.items()
                 if index in fixed)
    constraints = set()
    counts = Counter(all_five_sets=0, possible_red=0, possible_blue=0)
    for vertices in combinations(range(43), 5):
        counts["all_five_sets"] += 1
        free = {mapping[edge] for edge in combinations(vertices, 2)
                if edge not in known}
        constants = {known[edge] for edge in combinations(vertices, 2)
                     if edge in known}
        if False not in constants:
            constraints.add(tuple(sorted(-variable for variable in free)))
            counts["possible_red"] += 1
        if True not in constants:
            constraints.add(tuple(sorted(free)))
            counts["possible_blue"] += 1
    counts["distinct_ramsey_clauses"] = len(constraints)
    constraints.update((index if value else -index,) for index, value in fixed.items())
    if color == "blue":
        constraints.update(tuple(sorted((mapping[(33, f)], mapping[(34, f)])))
                           for f in range(35, 43))
    rows = sorted(constraints)
    counts.update(variables=320, fixed_units=27,
                  pair_consequences=8 if color == "blue" else 0,
                  clauses=len(rows))
    require(counts["all_five_sets"] == 962_598, "incomplete five-set domain")
    wanted = EXPECTED[color]
    require(counts["possible_red"] == wanted["possible_red"]
            and counts["possible_blue"] == wanted["possible_blue"]
            and counts["distinct_ramsey_clauses"] == wanted["ramsey_clauses"]
            and counts["clauses"] == wanted["clauses"],
            f"{color} formula census differs")
    with output.open("w") as stream:
        stream.write(f"p cnf 320 {len(rows)}\n")
        for row in rows:
            stream.write(" ".join(map(str, row)) + (" " if row else "") + "0\n")
    observed = info(output)
    require(observed == {k: wanted[k] for k in ("bytes", "sha256")},
            f"{color} full formula identity differs")
    # Re-open and check serialization independently of the in-memory rows.
    with output.open() as stream:
        require(stream.readline() == f"p cnf 320 {len(rows)}\n", "wrong DIMACS header")
        parsed = []
        for line in stream:
            values = tuple(map(int, line.split()))
            require(values and values[-1] == 0, "unterminated DIMACS row")
            row = values[:-1]
            require(row == tuple(sorted(set(row)))
                    and all(1 <= abs(x) <= 320 for x in row)
                    and not any(-x in row for x in row), "noncanonical clause")
            parsed.append(row)
    require(parsed == rows, "serialized formula differs from definition")
    result = {"formula": observed, "census": dict(counts),
              "clause_lengths": dict(sorted(Counter(map(len, rows)).items()))}
    del parsed, rows, constraints
    gc.collect()
    return result


def fixed_pair_relabelings(mapping):
    fixed_vertices = list(range(33, 43))
    checked = 0
    for a, b in combinations(fixed_vertices, 2):
        others = [v for v in fixed_vertices if v not in (a, b)]
        permutation = {v: v for v in range(33)}
        permutation.update({a: 33, b: 34})
        permutation.update(dict(zip(others, range(35, 43))))
        require(set(permutation) == set(range(43))
                and set(permutation.values()) == set(range(43)), "not a vertex permutation")
        require(all(permutation[rotate(v)] == rotate(permutation[v]) for v in range(43)),
                "fixed-pair relabeling does not commute with C3")
        image_by_primary = {}
        for edge, source in mapping.items():
            image = tuple(sorted((permutation[edge[0]], permutation[edge[1]])))
            target = mapping[image]
            require(source not in image_by_primary or image_by_primary[source] == target,
                    "one orbit splits under relabeling")
            image_by_primary[source] = target
        require(set(image_by_primary) == set(range(1, 321))
                and set(image_by_primary.values()) == set(range(1, 321)),
                "relabeling is not a primary-orbit bijection")
        checked += 1
    return {"unordered_empty_pairs_checked": checked,
            "moving_vertices_fixed_pointwise": 33,
            "primary_orbit_bijections": checked}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    mapping, internal = physical_orbits()
    answer = {
        "reviewed_source": source_identity(args.target),
        "orbit_census": {"moving": 165, "fixed": 45, "incidence": 110,
                          "internal_constant_edges": 33, "physical_pairs": 903},
        "displayed_index": check_displayed_index(mapping),
        "local_blue_pair_lemma": local_pair_lemma(mapping, internal),
        "fixed_pair_coverage": fixed_pair_relabelings(mapping),
        "cases": {},
    }
    for color in ("blue", "red"):
        answer["cases"][color] = formula(
            color, mapping, internal, args.work / f"{color}.cnf")
    answer.update({
        "solver_claims_reproduced": False,
        "decision_boundary": "Both submitted solves are UNKNOWN; neither case is excluded.",
        "equivalence_scope": "Distinguished-pair formulas are exact; whole-Core194 coverage imports z>=2.",
    })
    args.report.write_text(json.dumps(answer, indent=2, sort_keys=True) + "\n")
    print("PASS independent direct Core194 formula equivalence and coverage")


if __name__ == "__main__":
    main()
