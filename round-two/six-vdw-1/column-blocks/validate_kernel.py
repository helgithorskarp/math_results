"""Independent complete truth-table checks of the 64-conditioning optimizer."""
import argparse
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(path):
    data = json.loads(path.read_text())
    require(len(data) == 120, "wrong fixture count")
    feasible_cases = states = 0
    results = []
    for fixture in data:
        best = None
        actual = None
        for mask in range(4096):
            states += 1
            if mask & ~fixture["allowed"]:
                continue
            edits = fixture["outside"].copy()
            toggles = [(mask >> i) & 1 for i in range(12)]
            for i, (edited, toggle) in enumerate(zip(fixture["edited"], toggles)):
                edits[fixture["classes"][i // 6]] += edited ^ toggle
            if min(edits) < 30 or sum(edits) < 65:
                continue
            cost = [0, 0]
            for i, toggle in enumerate(toggles):
                if toggle:
                    for metric in range(2):
                        cost[metric] += fixture["linear"][i][metric]
            for i in range(6):
                for j in range(6):
                    if toggles[i] and toggles[j + 6]:
                        for metric in range(2):
                            cost[metric] += fixture["cross"][i][j][metric]
            objective = (cost[1], cost[0])
            if best is None or objective < best:
                best = objective
            if mask == fixture["mask"]:
                actual = objective
        require(fixture["feasible"] == (best is not None), "feasibility mismatch")
        if best is not None:
            require(actual == best == tuple(reversed(fixture["minimum"])), "exact optimum mismatch")
            feasible_cases += 1
        results.append(best)
    require(feasible_cases > 0 and feasible_cases < 120, "vacuous fixture coverage")
    return {"status": "EXACT_ALL_4096_STATE_OPTIMA_CHECKED", "fixtures": len(data),
            "states": states, "feasible_fixtures": feasible_cases,
            "canonical_result_sha256": hashlib.sha256(
                json.dumps(results, separators=(",", ":")).encode()).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fixtures", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check(args.fixtures)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")
