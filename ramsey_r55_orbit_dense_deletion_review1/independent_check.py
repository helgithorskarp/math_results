#!/usr/bin/env python3
"""Independent audit of the h3975 orbit-dense deletion result.

No module from the reviewed package is imported.  The checker uses direct
translation orbits for pairs (rather than the source union-find), reconstructs
the Paley cover from quadratic residues, and probes the receiver on fresh
cyclic inputs generated here.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import argparse
import json
from pathlib import Path
import subprocess
import sys


SOURCE_MANIFEST_SHA256 = "9ae8498be5a6b0787b4d20dae9a77b61288caa56bdcc4d7001c09581c6966048"
CERTIFICATE_SHA256 = "9a20f46245d7f17b76ac78621e5ad6bf646391436e35efa406e66dc63dbaf5fd"
REDUCTION_SHA256 = "0b8d16b40305f59660941fc22a501ca022b6418c4f01ff6d30513997853a48cc"


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def choose(n, k):
    k = min(k, n - k)
    answer = 1
    for step in range(1, k + 1):
        answer = answer * (n - k + step) // step
    return answer


def verify_source_manifest(source):
    manifest = source / "SHA256SUMS"
    need(digest(manifest) == SOURCE_MANIFEST_SHA256,
         "source manifest SHA-256")
    names = []
    for row in manifest.read_text().splitlines():
        expected, name = row.split("  ", 1)
        need(Path(name).name == name and name not in names,
             "source manifest path")
        need(digest(source / name) == expected, "source file digest " + name)
        names.append(name)
    present = {path.name for path in source.iterdir() if path.is_file()}
    need(set(names) == present - {"SHA256SUMS"},
         "source manifest file coverage")
    need(len(names) == 19, "source manifest entry count")
    return len(names)


def check_paley(certificate):
    prime = 53
    need(all(prime % divisor for divisor in range(2, 8)), "53 is prime")
    squares = {value * value % prime for value in range(1, prime)}
    need(len(squares) == 26 and 52 in squares, "quadratic residue set")

    def red(u, v):
        return (v - u) % prime in squares

    record = certificate["paley53"]
    seed = tuple(record["seed"])
    need(len(seed) == 5 and len(set(seed)) == 5,
         "Paley seed cardinality")
    need(all(red(u, v) for u, v in combinations(seed, 2)),
         "Paley seed is a literal clique")
    translates = sorted({tuple(sorted((vertex + shift) % prime
                                      for vertex in seed))
                         for shift in range(prime)})
    need(len(translates) == prime, "Paley translate orbit size")
    need(record["translates"] == [list(row) for row in translates],
         "Paley committed translate list")
    incidences = [0] * prime
    literal_pairs = 0
    for row in translates:
        for vertex in row:
            incidences[vertex] += 1
        for u, v in combinations(row, 2):
            need(red(u, v), "Paley translated literal edge")
            literal_pairs += 1
    need(incidences == [5] * prime == record["vertex_incidence"],
         "Paley uniform incidence")
    maximum_hit = 10 * max(incidences)
    surviving = len(translates) - maximum_hit
    need((maximum_hit, surviving) == (50, 3), "Paley cover gap")
    need(5 * 43 == 215 and 4 * 53 == 212 and 215 > 212,
         "Paley summed inequality")
    need(record["maximum_rows_hit_by_deletions"] == maximum_hit
         and record["minimum_surviving_rows"] == surviving
         and record["farkas_gap"] == 3,
         "Paley certificate arithmetic")
    return {
        "seed": list(seed),
        "translate_cliques": len(translates),
        "literal_pairs_checked": literal_pairs,
        "incidence_per_vertex": 5,
        "maximum_rows_hit_by_ten_deletions": maximum_hit,
        "minimum_surviving_cliques": surviving,
        "physical_subset_jobs_excluded": choose(53, 10),
        "uses_imported_ramsey_bound": False,
    }


def shift53(vertex):
    if vertex < 26:
        return (vertex + 1) % 26
    if vertex < 52:
        return 26 + (vertex - 26 + 1) % 26
    return 52


def shifted_pair(pair):
    return tuple(sorted(map(shift53, pair)))


def direct_pair_orbits():
    remaining = set(combinations(range(53), 2))
    cells = []
    while remaining:
        seed = min(remaining)
        cell = set()
        current = seed
        for _ in range(26):
            cell.add(current)
            current = shifted_pair(current)
        need(current == seed, "pair returns after 26 shifts")
        need(cell <= remaining, "pair orbits are disjoint")
        remaining.difference_update(cell)
        cells.append(frozenset(cell))
    return tuple(cells)


def check_template(certificate):
    record = certificate["two_orbit53"]
    expected_generator = [shift53(vertex) for vertex in range(53)]
    need(record["generator"] == expected_generator,
         "two-cycle generator")
    cells = direct_pair_orbits()
    need(len(cells) == 54 and sum(map(len, cells)) == choose(53, 2),
         "complete 54-cell pair partition")
    histogram = {}
    for cell in cells:
        histogram[len(cell)] = histogram.get(len(cell), 0) + 1
    need(histogram == {13: 2, 26: 52}, "pair-orbit size histogram")

    used = set()
    records = record["edge_classes"]
    need([row["index"] for row in records] == list(range(54)),
         "edge-class indices")
    for row in records:
        representative = tuple(row["representative"])
        matches = [index for index, cell in enumerate(cells)
                   if representative in cell]
        need(len(matches) == 1 and matches[0] not in used,
             "one representative per pair orbit")
        used.add(matches[0])
        need(row["size"] == len(cells[matches[0]]),
             "edge-class size")
    need(len(used) == len(cells), "all pair orbits represented")

    need(record["vertex_orbits"]
         == [list(range(26)), list(range(26, 52)), [52]],
         "vertex orbit partition")
    retained = record["selected_per_orbit"]
    need(retained == [21, 21, 1], "template retained profile")
    need(all(5 * kept > 4 * size
             for kept, size in zip(retained, (26, 26, 1))),
         "strict template orbit density")
    maximum_seed_deletions = max(
        Fraction(5 * (left + right), 26)
        for left in range(6) for right in range(6 - left))
    need(maximum_seed_deletions == Fraction(25, 26),
         "template worst exact expectation")
    deletion_pairs = choose(26, 5) ** 2
    jobs = (1 << 54) * deletion_pairs
    return {
        "edge_orbits": len(cells),
        "pairs_partitioned": sum(map(len, cells)),
        "edge_orbit_size_histogram": {str(k): v
                                      for k, v in sorted(histogram.items())},
        "ambient_graph_words": 1 << 54,
        "deletion_pairs": deletion_pairs,
        "physical_parameter_jobs_excluded": jobs,
        "maximum_deleted_incidence_mean": [25, 26],
        "candidate_symmetry_required": False,
    }


def clique_of_five(adjacency, color):
    n = len(adjacency)
    universe = (1 << n) - 1

    def search(chosen, candidates):
        if len(chosen) == 5:
            return tuple(chosen)
        if candidates.bit_count() < 5 - len(chosen):
            return None
        while candidates:
            # Highest-first search deliberately differs from the receiver's
            # lowest-first seed traversal.
            bit = 1 << (candidates.bit_length() - 1)
            candidates ^= bit
            vertex = bit.bit_length() - 1
            neighbors = adjacency[vertex] if color else universe ^ adjacency[vertex]
            answer = search(chosen + [vertex], candidates & neighbors)
            if answer is not None:
                return answer
        return None

    return search([], universe)


def adjacency_from_edges(n, edges):
    adjacency = [0] * n
    seen = set()
    for edge in edges:
        u, v = edge
        need(0 <= u < v < n and (u, v) not in seen, "fresh input edge")
        seen.add((u, v))
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return adjacency


def run_interface(source, input_path):
    completed = subprocess.run(
        [sys.executable, "-B", str(source / "interface.py"), str(input_path)],
        text=True, capture_output=True, check=False)
    need(completed.returncode == 0 and not completed.stderr,
         "source interface execution")
    return json.loads(completed.stdout)


def validate_receiver_certificate(data, certificate):
    n = data["n"]
    adjacency = adjacency_from_edges(n, data["red_edges"])
    permutation = data["generators"][0]
    need(sorted(permutation) == list(range(n)), "fresh generator permutation")
    need(all(bool(adjacency[u] >> v & 1)
             == bool(adjacency[permutation[u]] >> permutation[v] & 1)
             for u, v in combinations(range(n), 2)),
         "fresh generator automorphism")
    need(certificate["status"]
         == "CERTIFIED_MONOCHROMATIC_FIVE_IN_PHYSICAL43",
         "fresh receiver status")
    seed = certificate["seed"]
    red = certificate["color"] == "red"
    need(certificate["color"] in ("red", "blue")
         and all(bool(adjacency[u] >> v & 1) == red
                 for u, v in combinations(seed, 2)),
         "fresh seed monochromatic")
    mapped = list(seed)
    for step in certificate["generator_word"]:
        need(step == 0, "fresh generator word index")
        mapped = [permutation[vertex] for vertex in mapped]
    witness = sorted(mapped)
    need(witness == certificate["ambient_witness"]
         and set(witness) <= set(data["selected"]),
         "fresh surviving translated witness")
    physical = certificate["physical_witness"]
    need([data["selected"][index] for index in physical] == witness,
         "fresh physical relabeling")
    need(certificate["expected_deleted_intersection"] == [20, 47],
         "fresh exact average")
    need(certificate["target43_found"] is False, "fresh scope marker")
    return certificate["color"], witness


def check_fresh_receiver(source, work):
    n = 47
    distances = {1, 2, 4, 7, 9, 13, 18, 21}
    edges = [[u, v] for u, v in combinations(range(n), 2)
             if min((v - u) % n, (u - v) % n) in distances]
    deleted = {0, 5, 17, 31}
    data = {
        "n": n,
        "red_edges": edges,
        "generators": [[(vertex + 1) % n for vertex in range(n)]],
        "selected": [vertex for vertex in range(n) if vertex not in deleted],
    }
    input_path = work / "fresh-c47.json"
    input_path.write_text(json.dumps(data, sort_keys=True))
    certificate = run_interface(source, input_path)
    source_color, source_witness = validate_receiver_certificate(data,
                                                                  certificate)
    adjacency = adjacency_from_edges(n, edges)
    independent_seed = clique_of_five(adjacency, True)
    independent_color = True
    if independent_seed is None:
        independent_seed = clique_of_five(adjacency, False)
        independent_color = False
    need(independent_seed is not None, "fresh independent ambient five")
    independent_witness = None
    for shift in range(n):
        candidate = tuple(sorted((vertex + shift) % n
                                 for vertex in independent_seed))
        if set(candidate).isdisjoint(deleted):
            independent_witness = candidate
            break
    need(independent_witness is not None,
         "fresh independent avoiding translate")
    need(Fraction(5 * len(deleted), n) == Fraction(20, 47) < 1,
         "fresh orbit average")

    outside = {
        "n": 53,
        "red_edges": [],
        "generators": [[shift53(vertex) for vertex in range(53)]],
        "selected": [vertex for vertex in range(53)
                     if vertex not in set(range(6)) | set(range(26, 30))],
    }
    outside_path = work / "outside.json"
    outside_path.write_text(json.dumps(outside, sort_keys=True))
    outside_certificate = run_interface(source, outside_path)
    need(outside_certificate["status"] == "OUTSIDE_DECLARED_ORBIT_DENSE_FAMILY"
         and outside_certificate["ramsey_verdict"] is None,
         "outside-family no-verdict behavior")
    return {
        "ambient_order": n,
        "red_edges": len(edges),
        "deleted_vertices": len(deleted),
        "exact_deleted_intersection_mean": [20, 47],
        "source_witness_color": source_color,
        "source_witness": source_witness,
        "independent_witness_color": "red" if independent_color else "blue",
        "independent_witness": list(independent_witness),
        "outside_family_has_no_ramsey_verdict": True,
    }


def theorem_controls():
    # Exhaust every five-set for C7 with one deletion: retained density 6/7.
    avoided = 0
    for seed in combinations(range(7), 5):
        need(any(0 not in {(vertex + shift) % 7 for vertex in seed}
                 for shift in range(7)), "C7 averaging control")
        avoided += 1
    need(avoided == choose(7, 5), "C7 control count")
    # Equality at 4/5 is insufficient: the sole five-set of C5 always meets
    # a one-point deletion under translation.
    seed = set(range(5))
    need(all(0 in {(vertex + shift) % 5 for vertex in seed}
             for shift in range(5)), "strict 4/5 boundary")
    admitted_orders = [n for n in range(43, 60) if 5 * 43 > 4 * n]
    need(admitted_orders == list(range(43, 54)), "density endpoint")
    return {
        "small_cyclic_five_sets_checked": avoided,
        "strict_four_fifths_boundary_checked": True,
        "density_forces_ambient_order_at_most": 53,
        "imported_ramsey_premise_applies_from_order": 46,
        "declared_orders": list(range(46, 54)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    work = args.work.resolve()
    need(source.is_dir(), "source directory")
    need(not work.exists(), "work path must not exist")
    work.mkdir(parents=True)

    manifest_entries = verify_source_manifest(source)
    need(digest(source / "CERTIFICATE.json") == CERTIFICATE_SHA256,
         "certificate SHA-256")
    need(digest(source / "REDUCTION.json") == REDUCTION_SHA256,
         "reduction SHA-256")
    certificate = json.loads((source / "CERTIFICATE.json").read_text())
    need(certificate["schema"] == "r55-orbit-dense-deletion-v1",
         "certificate schema")
    reduction = json.loads((source / "REDUCTION.json").read_text())
    paley = check_paley(certificate)
    template = check_template(certificate)
    need(reduction["paley53"]["physical_subset_jobs"]
         == paley["physical_subset_jobs_excluded"], "Paley inventory")
    need(reduction["two_orbit53"]["physical_parameter_jobs"]
         == template["physical_parameter_jobs_excluded"],
         "template inventory")
    need(reduction["target43_found"] is False
         and reduction["whole_q10_task_decided"] is False,
         "scope inventory")
    report = {
        "status": "INDEPENDENTLY_VERIFIED_ORBIT_DENSE_DELETION_EXCLUSION",
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "source_manifest_entries": manifest_entries,
        "certificate_sha256": CERTIFICATE_SHA256,
        "reduction_sha256": REDUCTION_SHA256,
        "theorem_controls": theorem_controls(),
        "paley53": paley,
        "two_cycle_template53": template,
        "fresh_receiver": check_fresh_receiver(source, work),
        "imported_boundary": (
            "The universal order-46-through-53 theorem imports "
            "Angeltveit--McKay R(5,5)<=46 (arXiv:2409.15709v2); "
            "that computer-assisted theorem is not reproduced."
        ),
        "target43_found": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
