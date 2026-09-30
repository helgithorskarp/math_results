"""Exact replay of precisely the four new minimum-phase exclusions."""
import argparse
import hashlib
import json
from pathlib import Path
import verify

HERE = Path(__file__).parent
PHASES = (184, 201, 205, 269)


def check_all(directory):
    paths = sorted(directory.glob("phase-*.json"))
    if {p.name for p in paths} != {f"phase-{s}.json" for s in PHASES}:
        raise ValueError("Exactly all four new phases required")
    results = []
    for phase in PHASES:
        path = directory / f"phase-{phase}.json"
        raw = path.read_bytes()
        data = json.loads(raw)
        if data.get("phase") != phase:
            raise ValueError("Phase filename mismatch")
        out = verify.check(data, HERE / f"base/certificates/phase-{phase}.json", HERE / "base/verify.py")
        out["certificate_sha256"] = hashlib.sha256(raw).hexdigest()
        results.append(out)
    return {"agent": "six-vdw-3", "role": "researcher",
            "status": "EXACT_COMPLETE_FOUR_PHASE_CLASS196_EXCLUSION",
            "phases": list(PHASES), "required_edits_per_reference_color_each_phase": 197,
            "nodes": sum(x["nodes"] for x in results),
            "splits": sum(len(x["splits"]) for x in results),
            "leaves": sum(len(x["leaves"]) for x in results),
            "checked_AP_instances": sum(x["checked_AP_instances"] for x in results),
            "checked_original_incidences": sum(x["checked_original_incidences"] for x in results),
            "cases": results,
            "other_613_phase_bounds_not_rechecked_here": True,
            "no_new_W_bound_or_coloring": True}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--certificates", type=Path, default=HERE / "certificates")
    p.add_argument("--expected", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    out = check_all(args.certificates)
    if args.expected and out != json.loads(args.expected.read_text()):
        raise ValueError("Checked result differs from expected result")
    if args.output:
        args.output.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k: v for k, v in out.items() if k != "cases"}))


if __name__ == "__main__":
    main()
