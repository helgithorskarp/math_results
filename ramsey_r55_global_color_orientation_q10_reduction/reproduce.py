#!/usr/bin/env python3
"""Fresh-output normal/-O replay, controls, and corruption rejection."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def invoke(flags, script, *arguments, check=True):
    return subprocess.run(
        [sys.executable, *flags, "-B", str(HERE / script),
         *map(str, arguments)],
        check=check, capture_output=True,
    )


def check_manifest():
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    need(set(manifest) == {path.name for path in HERE.iterdir()
                           if path.is_file() and path.name != "MANIFEST.json"},
         "manifest file inventory")
    for name, expected in manifest.items():
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        need(actual == expected, "package identity: " + name)


def synthetic_degree22(path):
    edges = set()
    for vertex in range(43):
        for step in range(1, 12):
            edges.add(tuple(sorted((vertex, (vertex + step) % 43))))
    need(len(edges) == 473, "synthetic degree-22 edge count")
    path.write_text(json.dumps({
        "order": 43,
        "red_edges": [list(edge) for edge in sorted(edges)],
    }) + "\n")


def reproduce(destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    check_manifest()
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    receipts = {}

    for label, flags in (("normal", []), ("optimized", ["-O"])):
        produced = invoke(flags, "analyze.py")
        result = json.loads(produced.stdout)
        need(result == expected, "frozen expected result: " + label)
        result_path = destination / (label + "-result.json")
        result_path.write_bytes(produced.stdout)
        independent = json.loads(invoke(
            flags, "independent_check.py", result_path).stdout)
        controls = json.loads(invoke(flags, "controls.py").stdout)
        need(independent["status"] == "INDEPENDENT_CHECK_ACCEPT",
             "independent result")
        need(controls["status"] == "CONTROLS_PASS", "controls result")

        corruptions = 0
        for field in ("active", "literal", "coverage"):
            bad = json.loads(json.dumps(result))
            if field == "active":
                bad["oriented_q10_unknown_queue"]["target_active_orientation"] = 68
            elif field == "literal":
                bad["literal_h3987_state"]["unknown"] = 160
            else:
                bad["coverage"]["redirect_destination"] = "same child"
            bad_path = destination / f"{label}-bad-{field}.json"
            bad_path.write_text(json.dumps(bad) + "\n")
            rejection = invoke(flags, "independent_check.py", bad_path,
                               check=False)
            need(rejection.returncode != 0,
                 "corrupt result accepted: " + label + "/" + field)
            corruptions += 1

        receipts[label] = {
            "controls": controls,
            "deliberate_result_corruptions_rejected": corruptions,
            "independent": independent,
        }

    graph_path = destination / "synthetic-degree22.json"
    synthetic_degree22(graph_path)
    oriented = json.loads(invoke([], "orient_graph.py", graph_path).stdout)
    need(oriented["complemented"] is True, "edge-list complement control")
    need(oriented["original_red_edge_count"] == 473, "input edge count")
    need(oriented["red_edge_count"] == 430, "oriented edge count")
    need(oriented["good43"] is False, "synthetic graph is not a candidate")

    answer = {
        "edge_list_orientation_control": {
            "complemented": True,
            "input_edges": 473,
            "output_edges": 430,
        },
        "normal_and_optimized": True,
        "python": sys.version,
        "receipts": receipts,
        "solver_calls": 0,
        "status": "REPRODUCED_GLOBAL_COLOR_ORIENTATION_Q10_EFFECT",
    }
    (destination / "RECEIPT.json").write_text(
        json.dumps(answer, indent=2, sort_keys=True) + "\n")
    return answer


if __name__ == "__main__":
    need(len(sys.argv) == 2, "usage: reproduce.py FRESH_OUTPUT_DIRECTORY")
    print(json.dumps(reproduce(sys.argv[1]), indent=2, sort_keys=True))
