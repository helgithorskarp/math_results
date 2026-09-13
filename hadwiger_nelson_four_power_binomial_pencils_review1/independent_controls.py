#!/usr/bin/env python3
"""Negative controls for the independent A5 binomial-pencil audit."""
from argparse import ArgumentParser
import copy
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("independent_binomial_audit", HERE / "independent_audit.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def reject(name, function, expected):
    try:
        function()
    except ValueError as error:
        audit.require(expected in str(error), f"wrong rejection for {name}: {error}")
        return name
    raise ValueError(f"corruption accepted: {name}")


def run(certificate_path):
    certificate = json.loads(Path(certificate_path).read_text())
    rows, events, factors, buckets = audit.make_inventory()
    raw_by_row = {row: raw for row, (raw, event) in zip(rows, events)}
    edgegroups = audit.row_edgegroups()
    source = next(component for component in certificate["components"]
                  if component.get("point_count") == 129)
    rejected = []

    bad = copy.deepcopy(source)
    bad["real_embeddings"] += 1
    rejected.append(reject("alter_real_root_count",
                           lambda: audit.component_audit(bad, factors, raw_by_row, edgegroups),
                           "real-root count"))

    bad = copy.deepcopy(source)
    bad["active_curves"] = bad["active_curves"][:-1]
    rejected.append(reject("omit_active_curve",
                           lambda: audit.component_audit(bad, factors, raw_by_row, edgegroups),
                           "active-curve list"))

    bad = copy.deepcopy(source)
    bad["edge_sha256"] = "0" * 64
    rejected.append(reject("alter_strict_edge_hash",
                           lambda: audit.component_audit(bad, factors, raw_by_row, edgegroups),
                           "strict unit-edge hash"))

    bad = copy.deepcopy(source)
    bad["colour_weights"] = [1, 1, 1, 1, 1]
    rejected.append(reject("break_collision_colour",
                           lambda: audit.component_audit(bad, factors, raw_by_row, edgegroups),
                           "colour descends through collision"))

    row = next(record for record in certificate["pairs"]
               if source["key"] in record["components"])
    components = {component["key"]: component for component in certificate["components"]}
    a, b = row["pair"]
    claimed = [components[key] for key in row["components"]]
    missing = [component for component in claimed if component["key"] != source["key"]]
    rejected.append(reject("omit_algebraic_component",
                           lambda: audit.fiber_task(((a, b), factors[a], factors[b], missing)),
                           "complete independent square-free fibre coverage"))
    rejected.append(reject("duplicate_algebraic_component",
                           lambda: audit.fiber_task(((a, b), factors[a], factors[b], claimed + [source])),
                           "unique x projection factor"))

    return {"status": "PASS", "corruptions_rejected": rejected,
            "control_graph": [source["point_count"], source["edge_count"], 3]}


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(args.certificate)
    if args.check_expected:
        audit.require(result == json.loads(HERE.joinpath("EXPECTED_CONTROLS.json").read_text()),
                      "expected independent controls")
    print(json.dumps(result, sort_keys=True, indent=2))
