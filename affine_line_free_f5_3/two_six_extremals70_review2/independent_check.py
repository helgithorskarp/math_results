#!/usr/bin/env python3
"""Independent reconstruction for the two-six-plane 70-point classification.

Standard library only.  This implementation imports none of the reviewed
Python or C++ code.  It regenerates the quotient catalogue and orbit partition,
checks every published positive lift, reconstructs all 262 deterministic CNFs,
and compares their hashes with two complete DRAT replay summaries.
"""

import argparse
import hashlib
import json
from collections import defaultdict
from itertools import combinations, permutations, product
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


POINTS = tuple(product(range(5), repeat=3))
PLANAR = tuple(product(range(5), repeat=2))
NORMALS2 = tuple([(1, a) for a in range(5)] + [(0, 1)])
VALUES2 = tuple(tuple((a * x + b * y) % 5 for x, y in PLANAR)
                for a, b in NORMALS2)
NORMALS3 = tuple(p for p in POINTS if any(p) and next(x for x in p if x) == 1)


def enumerate_quotients():
    """Enumerate weak deficit compositions, then check all quotient lines."""
    accepted = set()
    interior = [0] * 16
    row_sums = [0] * 4
    column_sums = [0] * 4

    def visit(position, remaining):
        if position == 16:
            if remaining:
                return
            total = sum(interior)
            deficit = [0] * 25
            for position2, value in enumerate(interior):
                x, y = divmod(position2, 4)
                deficit[5 * (x + 1) + y + 1] = value
            for x in range(1, 5):
                deficit[5 * x] = 4 - row_sums[x - 1]
            for y in range(1, 5):
                deficit[y] = 4 - column_sums[y - 1]
            deficit[0] = total - 2
            require(sum(deficit) == 30, "deficit total")
            require(all(0 <= d <= 4 for d in deficit), "deficit range")
            # Check all 30 affine quotient lines, including both axis families.
            for values in VALUES2:
                for level in range(5):
                    if sum(deficit[i] for i, value in enumerate(values)
                           if value == level) < 4:
                        return
            accepted.add("".join(str(4 - d) for d in deficit))
            return
        slots = 16 - position
        if remaining < 0 or remaining > 4 * slots:
            return
        x, y = divmod(position, 4)
        maximum = min(4, remaining, 3 - row_sums[x], 3 - column_sums[y])
        for value in range(maximum + 1):
            interior[position] = value
            row_sums[x] += value
            column_sums[y] += value
            visit(position + 1, remaining - value)
            row_sums[x] -= value
            column_sums[y] -= value

    visit(0, 5)
    visit(0, 6)
    return sorted(accepted)


def validate_word(word):
    require(len(word) == 25 and set(word) <= set("01234"), "quotient word")
    weights = list(map(int, word))
    require(sum(weights) == 70, "quotient cardinality")
    profiles = [[sum(weights[i] for i, value in enumerate(values) if value == level)
                 for level in range(5)] for values in VALUES2]
    require(profiles[0] == profiles[-1] == [6, 16, 16, 16, 16],
            "normalized axis profiles")
    require(all(6 <= count <= 16 for profile in profiles for count in profile),
            "quotient profile range")
    return profiles


def normalized_orbit(word):
    profiles = validate_word(word)
    low = [(direction, level) for direction in range(6) for level in range(5)
           if profiles[direction][level] == 6]
    images = set()
    for (d, t), (e, u) in permutations(low, 2):
        if d == e:
            continue
        for first_scale, second_scale in product(range(1, 5), repeat=2):
            image = [None] * 25
            for old in range(25):
                x = first_scale * (VALUES2[d][old] - t) % 5
                y = second_scale * (VALUES2[e][old] - u) % 5
                new = 5 * x + y
                require(image[new] is None, "singular normalization")
                image[new] = word[old]
            candidate = "".join(image)
            validate_word(candidate)
            images.add(candidate)
    return images


def quotient_partition(words):
    remaining = set(words)
    records = []
    for word in words:
        if word not in remaining:
            continue
        orbit = normalized_orbit(word)
        require(orbit <= remaining and min(orbit) == word, "orbit partition")
        records.append((word, len(orbit)))
        remaining -= orbit
    require(not remaining, "uncovered quotient")
    return records


def affine_lines():
    index = {point: i for i, point in enumerate(POINTS)}
    lines = set()
    for point in POINTS:
        for direction in NORMALS3:
            line = tuple(sorted(index[tuple((point[j] + t * direction[j]) % 5
                                            for j in range(3))]
                                for t in range(5)))
            lines.add(line)
    require(len(lines) == 775, "affine line count")
    return tuple(sorted(lines))


def affine_planes():
    planes = []
    for normal in NORMALS3:
        for level in range(5):
            planes.append(tuple(i for i, point in enumerate(POINTS)
                                if sum(a * b for a, b in zip(normal, point)) % 5 == level))
    require(len(planes) == 155 and all(len(p) == 25 for p in planes),
            "affine plane count")
    return tuple(planes)


def determinant(matrix):
    a, b, c = matrix
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0])) % 5


def inspect_positive_objects(source, representatives):
    lines = affine_lines()
    planes = affine_planes()
    seeds = {item["name"]: item for item in
             json.loads((source / "seeds.json").read_text())}
    models = json.loads((source / "models.json").read_text())
    representative_set = {word for word, _ in representatives}

    def check_set(point_list):
        selected = set(point_list)
        require(len(point_list) == len(selected) == 70, "70-point set")
        require(not any(set(line) <= selected for line in lines), "affine line")
        require([sum(POINTS[p][j] for p in selected) % 5 for j in range(3)] ==
                [0, 0, 0], "coordinate sum")
        for q in range(125):
            if q not in selected:
                require(any(q in line and set(line) - {q} <= selected for line in lines),
                        "nonmaximal positive object")
        return selected

    seed_sets = {name: check_set(seed["points"]) for name, seed in seeds.items()}
    seed_six_counts = {
        name: sum(len(selected.intersection(plane)) == 6 for plane in planes)
        for name, selected in seed_sets.items()
    }
    require(sorted(seed_six_counts.values()) == [4, 5, 7], "seed distinction")

    groups = defaultdict(list)
    seen = set()
    for model in models:
        word = model["word"]
        selected = check_set(model["points"])
        require(word in representative_set, "model quotient class")
        require(tuple(model["points"]) not in seen, "duplicate model")
        seen.add(tuple(model["points"]))
        actual_word = "".join(str(sum(25 * x + 5 * y + z in selected
                                          for z in range(5)))
                              for x, y in PLANAR)
        require(actual_word == word, "model quotient")
        full = [i for i, value in enumerate(map(int, word)) if value == 4]
        gauge = next(triple for triple in combinations(full, 3)
                     if ((triple[1] // 5 - triple[0] // 5) *
                         (triple[2] % 5 - triple[0] % 5)
                         - (triple[2] // 5 - triple[0] // 5) *
                         (triple[1] % 5 - triple[0] % 5)) % 5)
        require(all(5 * i not in selected for i in gauge), "height gauge")

        certificate = model["affine_map"]
        matrix = certificate["matrix"]
        translation = certificate["translation"]
        require(certificate["seed"] in seed_sets and determinant(matrix),
                "affine certificate")
        image = set()
        for p in seed_sets[certificate["seed"]]:
            point = POINTS[p]
            mapped = tuple((sum(matrix[j][k] * point[k] for k in range(3))
                            + translation[j]) % 5 for j in range(3))
            image.add(25 * mapped[0] + 5 * mapped[1] + mapped[2])
        require(image == selected, "affine image")
        groups[word].append(model["points"])
    require(len(models) == 48 and len(groups) == 7, "positive census")
    return groups, seed_six_counts, lines


def exactly_clauses(fiber, count):
    return ([tuple(-v for v in subset) for subset in combinations(fiber, count + 1)]
            + [tuple(subset) for subset in combinations(fiber, 6 - count)])


def cnf_bytes(word, model_lists, lines):
    clauses = [tuple(-p - 1 for p in line) for line in lines]
    weights = list(map(int, word))
    for i, count in enumerate(weights):
        clauses.extend(exactly_clauses(tuple(range(5 * i + 1, 5 * i + 6)), count))
    full = [i for i, count in enumerate(weights) if count == 4]
    gauge = next(triple for triple in combinations(full, 3)
                 if ((triple[1] // 5 - triple[0] // 5) *
                     (triple[2] % 5 - triple[0] % 5)
                     - (triple[2] // 5 - triple[0] // 5) *
                     (triple[1] % 5 - triple[0] % 5)) % 5)
    clauses.extend((-(5 * i + 1),) for i in gauge)
    clauses.extend(tuple(-p - 1 for p in model) for model in model_lists)
    text = f"p cnf 125 {len(clauses)}\n"
    text += "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return text.encode()


def inspect_replays(paths, representatives, groups, lines):
    runs = [json.loads(path.read_text()) for path in paths]
    require(len(runs) == 2, "release and sanitizer summaries required")
    require(runs[0]["result"] == runs[1]["result"], "stable summaries differ")
    require(runs[0]["proof_bytes"] == runs[1]["proof_bytes"], "proof sizes differ")
    require(runs[0]["checker_sha256"] == runs[1]["checker_sha256"],
            "checker binaries differ")
    for run in runs:
        require(len(run["records"]) == len(representatives) == 262,
                "incomplete replay records")

    cnf_hashes = []
    proof_hashes = []
    for index, (word, _) in enumerate(representatives):
        expected_hash = sha(cnf_bytes(word, groups.get(word, []), lines))
        left, right = runs[0]["records"][index], runs[1]["records"][index]
        require(left["index"] == right["index"] == index, "record index")
        require(left["word"] == right["word"] == word, "record word")
        require(left["models"] == right["models"] == len(groups.get(word, [])),
                "record model count")
        require(left["cnf_sha256"] == right["cnf_sha256"] == expected_hash,
                "independent CNF mismatch")
        require(left["proof_sha256"] == right["proof_sha256"], "proof mismatch")
        require(left["proof_bytes"] == right["proof_bytes"] > 0, "proof size")
        cnf_hashes.append(expected_hash)
        proof_hashes.append(left["proof_sha256"])
    return {
        "proof_bytes": runs[0]["proof_bytes"],
        "checker_sha256": runs[0]["checker_sha256"],
        "cnf_hash_list_sha256": sha("\n".join(cnf_hashes).encode()),
        "proof_hash_list_sha256": sha("\n".join(proof_hashes).encode()),
    }


def audit(source, replay_paths):
    words = enumerate_quotients()
    raw = ("\n".join(words) + "\n").encode()
    require(len(words) == 7464, "quotient count")
    representatives = quotient_partition(words)
    rep_bytes = ("\n".join(word for word, _ in representatives) + "\n").encode()
    require(len(representatives) == 262, "orbit count")
    groups, six_counts, lines = inspect_positive_objects(source, representatives)
    replay = inspect_replays(replay_paths, representatives, groups, lines)
    return {
        "status": "INDEPENDENT_TWO_SIX_CLASSIFICATION_AUDIT_PASSED",
        "scope": "third quotient/orbit/CNF reconstruction plus two full DRAT replays",
        "quotients": len(words),
        "quotient_sha256": sha(raw),
        "classes": len(representatives),
        "representative_sha256": sha(rep_bytes),
        "positive_classes": len(groups),
        "positive_models": sum(map(len, groups.values())),
        "seed_six_plane_counts": six_counts,
        "affine_lines": len(lines),
        "replayed_unsat_formulas": len(representatives),
        **replay,
        "corollary_scope": "f+3epsilon<=4; no 71-point existence decision",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--release", type=Path, required=True)
    parser.add_argument("--sanitize", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = audit(args.source.resolve(),
                   [args.release.resolve(), args.sanitize.resolve()])
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        require(encoded == expected, "EXPECTED.json mismatch")
        print("PASS " + sha(encoded.encode()))
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
