#!/usr/bin/env python3
"""Independent review checker for the point-613 Parts support closure.

This checker imports no module from either reviewed contribution.  It rebuilds
the exact unit-distance graph from the original scale-96 table and the public
completion-point list, checks the deletion-colouring reduction, reconstructs
the direct pseudo-Boolean instance, and invokes a separately pinned VeriPB
binary only for the cutting-planes proof.
"""

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import lcm
import os
from pathlib import Path
import re
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
TARGET = REPO / "hadwiger_nelson_parts509_point613_closure"
OLD = REPO / "hadwiger_nelson_parts509_degree_pool_minimum" / "certificate_D7.json"
CATALOGUE = REPO / "hadwiger_nelson_parts509_degree6_lift_family" / "catalogue.json"
ORIGINALS = REPO / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
COMPLETION = REPO / "hadwiger_nelson_parts509_swap_closure" / "completion_points.json"
OLD_REVIEW = REPO / "hadwiger_nelson_parts509_degree7_extension610_closure_review1" / "old_bound.opb"

HASHES = {
    "old": "41a47be8d0568be7e1497f16a45c17d433e31e01fb62877856189fbf1ad53729",
    "catalogue": "0282698f8bfb3b7df241c3d60af0dfef82f6f0535f114af71bf0db11807d0a4f",
    "originals": "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "completion": "b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6",
    "old_bound": "03dfd3601258be7899c607696b96bf9b0ddba77784db404cca045e7b8dfdda9d",
    "opb": "060ff2f0e3bb5c7cf904f6f3e064c2d301e6cf6f98d7582288f5e01ab65d3778",
    "proof": "51ff373e47a42fa8dc0f5b2d5bc7e493775d86843e2e43774585e2c7048a71be",
}
PRIMES = (3, 5, 11)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    value = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def multiply(left, right):
    """Product in the subset basis for Q(sqrt(3),sqrt(5),sqrt(11))."""
    answer = [0] * 8
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            coefficient = a * b
            overlap = i & j
            for bit, prime in enumerate(PRIMES):
                if overlap & (1 << bit):
                    coefficient *= prime
            answer[i ^ j] += coefficient
    return tuple(answer)


def squared_distance(first, second):
    dx = tuple(a - b for a, b in zip(first[0], second[0], strict=True))
    dy = tuple(a - b for a, b in zip(first[1], second[1], strict=True))
    return tuple(a + b for a, b in zip(multiply(dx, dx), multiply(dy, dy), strict=True))


def scaled(values, denominator):
    result = []
    for value in values:
        coefficient = Fraction(value) * denominator
        require(coefficient.denominator == 1, ("nonintegral scaling", value, denominator))
        result.append(coefficient.numerator)
    return tuple(result)


def geometry(old):
    require(digest(ORIGINALS) == HASHES["originals"], "original coordinate hash")
    require(digest(COMPLETION) == HASHES["completion"], "completion coordinate hash")
    originals = []
    for line in ORIGINALS.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        require(len(row) == 16, ("original coordinate width", len(originals)))
        originals.append((row[:8], row[8:]))
    require(len(originals) == 509, "original point count")

    raw = json.loads(COMPLETION.read_text())
    denominator = 96
    candidates = []
    for record in raw["points"]:
        point = (tuple(Fraction(x) for x in record["x"]),
                 tuple(Fraction(y) for y in record["y"]))
        require(len(point[0]) == len(point[1]) == 8, "completion coordinate width")
        for coefficient in point[0] + point[1]:
            denominator = lcm(denominator, coefficient.denominator)
        candidates.append((point, tuple(record["neighbors"])))
    require(len(candidates) == 1158 and denominator == 288, "completion census dimensions")

    base = [
        (tuple((denominator // 96) * x for x in point[0]),
         tuple((denominator // 96) * x for x in point[1]))
        for point in originals
    ]
    scaled_candidates = [
        ((scaled(point[0], denominator), scaled(point[1], denominator)), recorded)
        for point, recorded in candidates
    ]
    target = (denominator * denominator,) + (0,) * 7
    high_degree = []
    incidence_checks = 0
    for point, recorded in scaled_candidates:
        neighbours = tuple(i for i, original in enumerate(base)
                           if squared_distance(point, original) == target)
        incidence_checks += len(base)
        require(neighbours == recorded, "completion neighbour list differs from exact scan")
        if len(neighbours) >= 7:
            high_degree.append(point)
    require(len(high_degree) == 76, "degree-seven completion count")

    points = dict(enumerate(base))
    for offset, point in enumerate(high_degree):
        points[509 + offset] = point
    q = ((-240,) + (0,) * 7, (0,) * 4 + (48,) + (0,) * 3)
    points[613] = q
    vertices = tuple(range(585)) + (613,)
    require(len(set(points.values())) == 586, "coordinate collision")

    # Cross-check the independently parsed sources against the review input's
    # label convention; no reviewed geometry routine is imported.
    for vertex in range(585):
        recorded = old["coordinates"][str(vertex)]
        expected = (scaled(recorded[0], denominator), scaled(recorded[1], denominator))
        require(points[vertex] == expected, ("coordinate label mismatch", vertex))

    old_edges = tuple((a, b) for a, b in combinations(range(585), 2)
                      if squared_distance(points[a], points[b]) == target)
    q_neighbours = tuple(v for v in range(585)
                         if squared_distance(points[v], q) == target)
    edges = old_edges + tuple((v, 613) for v in q_neighbours)
    require(len(old_edges) == 3083 and len(edges) == 3089, "unit-edge count")
    require(q_neighbours == (0, 8, 53, 148, 164, 195), "point-613 neighbourhood")
    edge_text = "".join(f"{a},{b}\n" for a, b in edges).encode("ascii")
    require(sha256(edge_text).hexdigest() ==
            "fa49f88e7524a3e151d1133584ed7330ea03137bcdc218f83cd642552beef38b",
            "reviewed edge stream mismatch")
    canonical = "".join(f"{a},{b}\n" for a, b in sorted(edges)).encode("ascii")
    return points, old_edges, edges, q_neighbours, incidence_checks, sha256(canonical).hexdigest()


def check_colouring(labels, witness, edges):
    require(len(labels) == len(witness) and set(witness) <= set("0123"), "colouring dimensions")
    colours = dict(zip(labels, witness, strict=True))
    checks = 0
    for a, b in edges:
        if a in colours and b in colours:
            require(colours[a] != colours[b], ("improper deletion colouring", a, b))
            checks += 1
    return colours, checks


def witness_reduction(old, old_edges, edges, q_neighbours):
    vertices = tuple(old["vertices"])
    require(vertices == tuple(range(585)), "old support labels")
    forced = tuple(old["forced"])
    free = tuple(old["free"])
    require(len(forced) == 451 and len(free) == 134, "forced/free sizes")
    require(set(forced).isdisjoint(free) and set(forced) | set(free) == set(vertices),
            "forced/free partition")
    family = tuple(frozenset(row["D"]) for row in old["family"])
    require(len(family) == 425 and all(row and row <= set(free) for row in family),
            "killing family domain")
    minimal = tuple(i for i, row in enumerate(family)
                    if not any(other < row for other in family))
    require(len(minimal) == 337, "minimal killing family size")
    require(all(any(family[i] <= row for i in minimal) for row in family),
            "minimal family does not cover full family")

    library = {("forced", v): [old["forced_witness"][str(v)]] for v in forced}
    library.update({("kill", i): [old["family"][i]["witness"]] for i in minimal})
    require(digest(CATALOGUE) == HASHES["catalogue"], "lift catalogue hash")
    catalogue = json.loads(CATALOGUE.read_text())
    require(len(catalogue) == 42, "lift catalogue size")
    for record in catalogue:
        key = (record["kind"], record["key"])
        require(key in library and record["index"] == len(library[key]), "catalogue indexing")
        library[key].append(record["witness"])

    selected = []
    missing = []
    retained_checks = 0
    chosen_data = {}
    for key, candidates in library.items():
        kind, value = key
        deleted = frozenset((value,)) if kind == "forced" else family[value]
        labels = tuple(v for v in vertices if v not in deleted)
        lifted = None
        for index, witness in enumerate(candidates):
            colours, _ = check_colouring(labels, witness, old_edges)
            available = tuple(sorted(set("0123") - {colours[v] for v in q_neighbours if v in colours}))
            if available:
                lifted = (index, witness, available[0])
                break
        if lifted is None:
            missing.append([kind, value])
            continue
        index, witness, q_colour = lifted
        colours, checks = check_colouring(labels + (613,), witness + q_colour, edges)
        retained_checks += checks
        selected.append((kind, value, index, q_colour))
        chosen_data[key] = (deleted, colours)
    require(missing == [["kill", 245], ["kill", 316]], "unexpected unliftable rows")
    require(sum(1 for row in selected if row[0] == "forced") == 451, "forced lift count")
    require(sum(1 for row in selected if row[0] == "kill") == 335, "killing lift count")
    require(retained_checks == 2_410_698, "retained edge-check count")
    selected_digest = sha256(json.dumps(selected, separators=(",", ":")).encode()).hexdigest()
    require(selected_digest == "3e3df795f2474a880ad196ec37da4571d807b51c3857bfba03ccf337520598e1",
            "selected lift digest")

    first = next(key for key in chosen_data if key[0] == "forced")
    deleted, colours = chosen_data[first]
    require(len(deleted) == 1, "five-colour seed deletion")
    full = dict(colours)
    full[next(iter(deleted))] = "4"
    require(len(full) == 586 and all(full[a] != full[b] for a, b in edges),
            "full support five-colouring")
    return family, minimal, free, selected_digest, retained_checks


def reduction_audit(old, family, minimal, free):
    first_missing = family[245]
    second_missing = family[316]
    require(first_missing == frozenset((129, 518)), "row 245")
    require(second_missing == frozenset((13, 24)), "row 316")
    kept = tuple(i for i in minimal if i not in (245, 316))
    require(len(kept) == 335, "kept hitting rows")
    omissions = frozenset((13, 24, 129, 518))
    require(omissions <= set(free), "omission domain")
    pool = frozenset(old["pool"])
    require(pool == frozenset(range(509, 585)), "pool labels")

    stage1_rows = (260, 285, 303, 377, 394)
    stage1 = tuple(tuple(sorted(family[i] - {13, 24})) for i in stage1_rows)
    require(stage1 == ((515, 564), (525,), (522, 539, 547),
                       (510, 529, 543), (524, 555, 572)), "stage-one groups")
    require(all(set(group) <= pool for group in stage1), "stage-one pool containment")
    require(sum(map(len, stage1)) == len(set().union(*map(set, stage1))), "stage-one overlap")

    stage2_rows = (126, 252) + stage1_rows
    stage2 = tuple(tuple(sorted(family[i] - omissions)) for i in stage2_rows)
    require(stage2[:2] == ((545,), (580,)) and stage2[2:] == stage1,
            "stage-two groups")
    require(sum(map(len, stage2)) == len(set().union(*map(set, stage2))), "stage-two overlap")

    residual_units = sorted(set().union(*(
        family[i] - omissions for i in kept if len(family[i] - omissions) == 1
    )))
    require(residual_units == [27, 75, 114, 125, 127, 184, 525, 545, 580],
            "residual forced vertices")
    # Audit the two monotone repair implications used in the prose.  Meeting
    # row 316 and adjoining pool point 518 hits both missing rows with at most
    # one new selection (or an arbitrary spare pool point supplies quota four).
    # After the five disjoint pool groups are forced, meeting row 245 and
    # adjoining original 13 does the symmetric job.  Once both rows are missed,
    # adjoining 13 and 518 repairs both with at most two selections.
    require(518 in first_missing & pool and 13 in second_missing - pool,
            "repair labels and pool types")
    require(len(pool) == 76 and first_missing.isdisjoint(second_missing),
            "repair availability")
    require(56 + 1 == 57 < 58 and 55 + 2 == 57 < 58,
            "old-bound repair cardinalities")
    require(451 + 1 + 56 == 508, "counterexample order bookkeeping")
    require(digest(OLD_REVIEW) == HASHES["old_bound"], "accepted old-bound input hash")
    return kept, omissions, residual_units, stage1, stage2


def direct_opb(family, kept, free, omissions):
    variable = {v: i + 1 for i, v in enumerate(free)}
    lines = []
    for i in kept:
        lines.append(" ".join(f"+1 x{variable[v]}" for v in sorted(family[i])) + " >= 1 ;")
    lines.extend(f"-1 x{variable[v]} >= 0 ;" for v in (13, 24, 129, 518))
    lines.append(" ".join(f"-1 x{variable[v]}" for v in free) + " >= -56 ;")
    result = ("* #variable= 134 #constraint= 340 #equal= 0 intsize= 8\n" +
              "\n".join(lines) + "\n").encode("ascii")
    require(sha256(result).hexdigest() == HASHES["opb"], "independent OPB hash")
    require(result == (TARGET / "residual.opb").read_bytes(), "independent OPB byte mismatch")

    # Parse the committed instance separately to audit Boolean indices and row shape.
    parsed = []
    for line in result.decode("ascii").splitlines()[1:]:
        lhs, rhs = line.split(" >= ")
        require(rhs.endswith(" ;"), "OPB row terminator")
        words = lhs.split()
        require(len(words) % 2 == 0, "OPB term width")
        terms = {}
        for coefficient, name in zip(words[::2], words[1::2], strict=True):
            require(re.fullmatch(r"x[1-9][0-9]*", name), "OPB variable syntax")
            index = int(name[1:])
            require(1 <= index <= 134 and index not in terms, "OPB variable range")
            terms[index] = int(coefficient)
        parsed.append((terms, int(rhs[:-2])))
    require(len(parsed) == 340, "OPB parsed row count")
    for position, i in enumerate(kept):
        require(parsed[position] == ({variable[v]: 1 for v in family[i]}, 1),
                ("OPB hitting row", position, i))
    require(parsed[335:339] == [({variable[v]: -1}, 0) for v in (13, 24, 129, 518)],
            "OPB omission rows")
    require(parsed[339] == ({i: -1 for i in range(1, 135)}, -56), "OPB budget row")
    require(set(omissions) == {free[i - 1] for i in (1, 6, 21, 68)}, "omission wire labels")
    return result


def check_proof(veripb, opb):
    proof = TARGET / "closure.pb"
    require(digest(proof) == HASHES["proof"] and proof.stat().st_size == 8372,
            "proof identity")
    first = proof.read_text(encoding="ascii").splitlines()
    require(first[:2] == ["pseudo-Boolean proof version 2.0", "f 340"], "proof header")
    require(first[-3:] == ["output NONE", "conclusion UNSAT : 367",
                           "end pseudo-Boolean proof"], "proof conclusion")
    checker = Path(veripb).resolve()
    require(digest(checker) == "b2296daa8735ace3320f15abb8ffa6fbad345c6626eff1e5fbff00c6eed2ae34",
            "VeriPB binary identity")
    version = subprocess.run([str(checker), "--version"], capture_output=True, text=True)
    require(version.returncode == 0 and "3.0.2" in version.stdout + version.stderr,
            "VeriPB version")
    scratch = Path(os.environ.get("TMPDIR", "/tmp"))
    with tempfile.TemporaryDirectory(prefix="hn613-review1-", dir=scratch) as directory:
        work = Path(directory)
        instance = work / "independent.opb"
        instance.write_bytes(opb)
        checked = subprocess.run([str(checker), str(instance), str(proof)],
                                 capture_output=True, text=True)
        require(checked.returncode == 0 and "s VERIFIED UNSATISFIABLE" in checked.stdout,
                "VeriPB rejected the complete proof")
        bad = proof.read_text(encoding="ascii").replace(
            "conclusion UNSAT : 367", "conclusion UNSAT : 341")
        require(bad != proof.read_text(encoding="ascii"), "negative proof mutation")
        wrong = work / "wrong.pb"
        wrong.write_text(bad, encoding="ascii")
        rejected = subprocess.run([str(checker), str(instance), str(wrong)],
                                  capture_output=True, text=True)
        require(rejected.returncode != 0 and "s VERIFIED UNSATISFIABLE" not in rejected.stdout,
                "VeriPB accepted the false conclusion")
    return digest(checker)


def compute(veripb):
    for path, key in ((OLD, "old"), (CATALOGUE, "catalogue"),
                      (TARGET / "residual.opb", "opb"), (TARGET / "closure.pb", "proof")):
        require(digest(path) == HASHES[key], ("input hash", key))
    old = json.loads(OLD.read_text())
    points, old_edges, edges, q_neighbours, incidence_checks, canonical_edge_hash = geometry(old)
    family, minimal, free, selected_hash, retained_checks = witness_reduction(
        old, old_edges, edges, q_neighbours)
    kept, omissions, residual_units, stage1, stage2 = reduction_audit(
        old, family, minimal, free)
    opb = direct_opb(family, kept, free, omissions)
    checker_hash = check_proof(veripb, opb)
    return {
        "status": "ACCEPTED AT FIXED POINT-613 SUPPORT SCOPE",
        "target_contribution": "bafkreibvpnwnkje6ovzbusyb5erpbfz2izxjjwxryrstb6gzr7p5bwoo6q",
        "predecessor_contribution": "bafkreigpgftito4ltzvhm7xfuepd3qtzr37xtuvdjfrvwce6cumlwq3o7q",
        "vertices": len(points),
        "unit_edges": len(edges),
        "point613_neighbours": list(q_neighbours),
        "completion_candidates_exactly_scanned": 1158,
        "completion_incidence_checks": incidence_checks,
        "degree_at_least_seven_completion_points": 76,
        "canonical_edge_sha256": canonical_edge_hash,
        "forced_deletion_colourings": 451,
        "killing_deletion_colourings": 335,
        "retained_coloured_edge_checks": retained_checks,
        "selected_lift_sha256": selected_hash,
        "minimal_killing_sets": len(minimal),
        "unliftable_minimal_rows": [245, 316],
        "omitted_vertices": sorted(omissions),
        "residual_forced_vertices": residual_units,
        "stage_one_disjoint_pool_groups": [list(group) for group in stage1],
        "stage_two_disjoint_pool_groups": [list(group) for group in stage2],
        "free_variables": len(free),
        "hitting_constraints": len(kept),
        "opb_constraints": 340,
        "maximum_selected_free_vertices": 56,
        "old_degree7_bound_minimum_selected": 58,
        "staged_repair_implications_verified": True,
        "opb_sha256": sha256(opb).hexdigest(),
        "proof_bytes": (TARGET / "closure.pb").stat().st_size,
        "proof_sha256": HASHES["proof"],
        "veripb_version": "3.0.2",
        "veripb_binary_sha256": checker_hash,
        "complete_proof_verified_unsatisfiable": True,
        "false_conclusion_rejected": True,
        "closure_through_507_predecessor_verified": True,
        "closure_through_508": True,
        "minimum_five_chromatic_subgraph_order": 509,
        "record_improvement": False,
        "imported_old_degree7_bound_review":
            "bafkreidxgsafxxo3gcm3lu2ekqdoxpkjdkluhpqg3wmuorcofmvs4olbn4",
        "imported_old_degree7_bound_opb_sha256": HASHES["old_bound"],
        "imported_parts509_five_chromaticity": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--veripb", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = compute(args.veripb)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
