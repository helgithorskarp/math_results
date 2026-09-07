#!/usr/bin/env python3
"""Regenerate the hinge geometry and verify every target-order colouring."""
from itertools import combinations
from pathlib import Path
import argparse
import base64
import hashlib
import json

import geometry

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / "hadwiger_nelson_cyclic_batch_probe"


def unpack(data, omitted, length):
    expected = (length-len(omitted)+3)//4
    geometry.require(len(data) == expected, "wrong packed row length")
    values = [(byte >> shift) & 3 for byte in data for shift in (0, 2, 4, 6)]
    geometry.require(all(colour == 0 for colour in values[length-len(omitted):]),
                     "nonzero packed padding")
    iterator = iter(values)
    return [-1 if vertex in omitted else next(iterator) for vertex in range(length)]


def extends(word, candidate, omitted=()):
    used = {word[vertex] for vertex in candidate["point_neighbours"]
            if vertex not in omitted and word[vertex] >= 0}
    return len(used) <= 3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    certificate = json.loads((HERE / "certificate.json").read_text())
    labels, rows, swaps, edges, external, internal, summary = geometry.enumerate_outputs(
        certificate["seed_certificate_sha256"])
    geometry.require(summary == certificate["geometry_summary"], "geometry summary")

    # Recheck and decode the 509 base rows and 300 compact rows from the
    # preceding public triangle gate. They are only colourings of S-u here;
    # no triangle-enumeration theorem is imported.
    prior_path = PRIOR / "gate_certificate.json"
    geometry.require(geometry.digest(prior_path.read_bytes()) ==
                     certificate["prior_gate_certificate_sha256"], "prior certificate hash")
    seed_certificate = json.loads((geometry.SEED / "certificate.json").read_text())
    inputs = geometry.seed.load_inputs(seed_certificate)
    base, _, _ = geometry.seed.check_colourings(
        seed_certificate, inputs, labels, swaps, edges)
    prior = json.loads(prior_path.read_text())
    prior_extra = base64.b64decode(prior["additional_rows_base64"], validate=True)
    geometry.require(len(prior["additional_family_sizes"]) == 509 and
                     sum(prior["additional_family_sizes"]) == prior["additional_rows"] and
                     len(prior_extra) == 127*prior["additional_rows"] and
                     hashlib.sha256(prior_extra).hexdigest() == prior["additional_rows_sha256"],
                     "prior extra-row metadata")
    families = []
    offset = 0
    for deleted, count in enumerate(prior["additional_family_sizes"]):
        family = [geometry.seed.unpack(base[127*deleted:127*(deleted+1)], deleted)]
        for _ in range(count):
            word = geometry.seed.unpack(prior_extra[offset:offset+127], deleted)
            offset += 127
            geometry.require(all(word[a] != word[b] for a, b in edges
                                 if deleted not in (a, b)), "invalid prior extra row")
            family.append(word)
        families.append(family)
    geometry.require(offset == len(prior_extra), "unused prior rows")

    extra = base64.b64decode(certificate["additional_rows_base64"], validate=True)
    geometry.require(len(certificate["additional_family_sizes"]) == 509 and
                     sum(certificate["additional_family_sizes"]) == certificate["additional_rows"] and
                     len(extra) == 127*certificate["additional_rows"] and
                     hashlib.sha256(extra).hexdigest() == certificate["additional_rows_sha256"],
                     "additional-row metadata")
    offset = 0
    for deleted, count in enumerate(certificate["additional_family_sizes"]):
        for _ in range(count):
            word = unpack(extra[offset:offset+127], {deleted}, 509)
            offset += 127
            geometry.require(all(word[a] != word[b] for a, b in edges
                                 if deleted not in (a, b)), "invalid additional row")
            families[deleted].append(word)
    geometry.require(offset == len(extra), "unused additional rows")

    # A destination already in S contracts directly to S-v, certified by the
    # corresponding base deletion row. Low-degree external parents extend
    # immediately. The stored family rows cover all but seven other parents.
    geometry.require(len(internal) == certificate["geometry_summary"][
                     "internal_collision_outputs"], "internal output count")
    candidates = [row for row in external if len(row["point_neighbours"]) >= 4]
    exceptional = [index for index, candidate in enumerate(candidates)
                   if not any(extends(word, candidate) for word in families[candidate["moved"]])]
    geometry.require(exceptional == certificate["exceptional_candidate_indices"],
                     "exceptional parent list")

    direct_data = base64.b64decode(certificate["direct_rows_base64"], validate=True)
    direct_instances = [tuple(row) for row in certificate["direct_instances"]]
    geometry.require(len(direct_instances) == certificate["direct_rows"] and
                     len(direct_data) == 127*len(direct_instances) and
                     hashlib.sha256(direct_data).hexdigest() == certificate["direct_rows_sha256"],
                     "direct-row metadata")
    direct_words = {}
    for row_id, (candidate_index, deleted) in enumerate(direct_instances):
        candidate = candidates[candidate_index]
        moved = candidate["moved"]
        geometry.require(candidate_index in exceptional and deleted not in (moved, 509),
                         "invalid direct instance")
        word = unpack(direct_data[127*row_id:127*(row_id+1)], {moved, deleted}, 510)
        active = set(range(510))-{moved, deleted}
        graph_edges = [(a, b) for a, b in edges if a in active and b in active]
        graph_edges += [(vertex, 509) for vertex in candidate["point_neighbours"]
                        if vertex in active]
        geometry.require(all(word[a] != word[b] for a, b in graph_edges),
                         "invalid direct target-order row")
        direct_words[candidate_index, deleted] = word

    inherited_targets = 0
    direct_targets = 0
    residual = []
    for candidate_index in exceptional:
        candidate = candidates[candidate_index]
        moved = candidate["moved"]
        for deleted in range(510):
            if deleted == moved:
                continue
            if deleted == 509:
                inherited_targets += 1
                continue
            if any(extends(word, candidate, (moved, deleted)) for word in families[deleted]):
                inherited_targets += 1
            elif (candidate_index, deleted) in direct_words:
                direct_targets += 1
            else:
                residual.append([candidate_index, deleted])
    geometry.require(not residual and set(direct_words) == set(direct_instances),
                     "uncovered or unused direct target rows")

    result = {
        "all_checks": True,
        "geometry": summary,
        "internal_508_point_contractions": len(internal),
        "external_hinge_outputs": len(external),
        "external_target_instances": len(external)*509,
        "low_degree_parent_colourings": summary["external_low_degree_outputs"],
        "nontrivial_parent_outputs": len(candidates),
        "parent_outputs_covered": len(candidates)-len(exceptional),
        "exceptional_parent_outputs": len(exceptional),
        "exceptional_target_instances": len(exceptional)*509,
        "exceptional_targets_covered_by_seed_words": inherited_targets,
        "direct_target_rows_checked": direct_targets,
        "additional_seed_words_checked": certificate["additional_rows"],
        "target_order": 508,
        "all_target_graphs_four_colourable": True,
    }
    geometry.require(result == certificate["expected_result"], "verification result")
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
