"""Independent literal AP census and critical-window gain audit.

No search implementation is imported. A cached gain is verified using only
monochromatic windows (negative contribution at every point) and windows
with one minority bit (positive contribution at that minority point).
"""
import argparse
import hashlib
import json
from pathlib import Path

N = 3704


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_checkpoint(path):
    lines = path.read_text().splitlines()
    head = lines[0].split()
    require(len(head) == 4 and head[0] in ("VDW3704PAWS1", "VDW3704PAWS2", "VDW3704PAWS3"), "wrong format")
    require(len(lines[1]) == N and set(lines[1]) <= {"0", "1"}, "wrong current word")
    require(len(lines[2]) == N and set(lines[2]) <= {"0", "1"}, "wrong best word")
    weight_count = int(lines[4])
    require(0 <= weight_count <= 1141450, "wrong weight count")
    weights = {}
    previous = -1
    for row in lines[5:5 + weight_count]:
        eid, weight = map(int, row.split())
        require(previous < eid < 1141450 and 1 < weight <= 1000000, "wrong weight record")
        previous = eid
        weights[eid] = weight
    return list(map(int, lines[1])), list(map(int, lines[2])), weights, int(head[3])


def edit_profile(word):
    # Euler's criterion rather than the search's square enumeration.
    edits = [0, 0]
    for x in range(3703):
        if x % 617:
            original = int(pow(x % 617, 308, 617) != 1)
            edits[original] += word[x] != original
    return edits


def census(word, weights=None, gains=False):
    require(len(word) == N and all(type(b) is int and b in (0, 1) for b in word),
            "invalid word")
    weights = {} if weights is None else weights
    raw = [0] * N
    weighted = [0] * N
    count = cost = covered = 0
    examples = []
    for start in range(N - 6):
        for step in range(1, (N - 1 - start) // 6 + 1):
            positions = [start + j * step for j in range(7)]
            colors = [word[x] for x in positions]
            ones = sum(colors)
            eid = (step - 1) * N - 3 * step * (step - 1) + start
            weight = weights.get(eid, 1)
            covered += 1
            if ones in (0, 7):
                count += 1
                cost += weight
                if len(examples) < 20:
                    examples.append([start, step, colors[0]])
                if gains:
                    for x in positions:
                        raw[x] -= 1
                        weighted[x] -= weight
            elif gains and ones in (1, 6):
                minority = int(ones == 1)
                x = positions[colors.index(minority)]
                raw[x] += 1
                weighted[x] += weight
    require(covered == 1141450, "incomplete AP coverage")
    return {"monochromatic_windows": count, "weighted_cost": cost,
            "coverage": covered, "examples": examples, "edits": edit_profile(word)}, raw, weighted


def literal_block(word, weights, r, s):
    """Condition each literal AP on its fixed outside colors.

    A surviving window contributes exactly when its selected bits equal a
    particular pattern. No quadratic coefficient or shared-pair formula is
    used here. The support test covers every actual window, including those
    whose outside colors already make them safe for all block assignments.
    """
    require(type(r) is int and type(s) is int and 2 <= r < 617 and
            2 <= s < 617 and r != s, "invalid ordinary-column block")
    points = [r + 617 * k for k in range(6)] + [s + 617 * k for k in range(6)]
    selected = {x: i for i, x in enumerate(points)}
    terms = {}
    covered = affected = max_support = 0
    for start in range(N - 6):
        for step in range(1, (N - 1 - start) // 6 + 1):
            inside = []
            fixed = set()
            for j in range(7):
                x = start + j * step
                if x in selected:
                    inside.append(selected[x])
                else:
                    fixed.add(word[x])
            covered += 1
            affected += bool(inside)
            max_support = max(max_support, len(inside))
            require(len(inside) <= 2 and len({i // 6 for i in inside}) == len(inside),
                    "ordinary-column geometric property failed")
            if len(fixed) != 1:
                continue
            color = next(iter(fixed))
            support = sum(1 << i for i in inside)
            pattern = sum((word[points[i]] ^ color) << i for i in inside)
            eid = (step - 1) * N - 3 * step * (step - 1) + start
            counts = terms.setdefault((support, pattern), [0, 0])
            counts[0] += 1
            counts[1] += weights.get(eid, 1)
    require(covered == 1141450 and max_support == 2, "block coverage failed")
    values = [[0, 0] for _ in range(4096)]
    for mask, costs in enumerate(values):
        for (support, pattern), counts in terms.items():
            if mask & support == pattern:
                costs[0] += counts[0]
                costs[1] += counts[1]
    return values, {"r": r, "s": s, "coverage": covered,
                    "affected_windows": affected, "maximum_selected_support": max_support,
                    "conditional_patterns": len(terms), "assignments_checked": 4096}


def audit(path):
    current, best, weights, claimed_best = read_checkpoint(path)
    result, raw, weighted = census(current, weights, gains=True)
    gain_lines = Path(str(path) + ".gains").read_text().splitlines()
    first = list(map(int, gain_lines[0].split()))
    require(first == [result["monochromatic_windows"], result["weighted_cost"], *result["edits"]],
            "current totals mismatch")
    require(list(map(int, gain_lines[1].split())) == raw, "unweighted flip gains mismatch")
    require(list(map(int, gain_lines[2].split())) == weighted, "weighted flip gains mismatch")
    pair_file = Path(str(path) + ".pairs")
    pairs_checked = 0
    if pair_file.exists():
        for row in pair_file.read_text().splitlines():
            x, y, claimed_raw, claimed_weighted = map(int, row.split())
            require(0 <= x < N and 0 <= y < N and x != y, "invalid test pair")
            # Enumerate all windows affected by either point by putting that
            # point in each of the seven slots. This does not use a gap divisor.
            affected = set()
            for point in (x, y):
                for step in range(1, 618):
                    for slot in range(7):
                        start = point - slot * step
                        if 0 <= start and start + 6 * step < N:
                            affected.add((start, step))
            direct_raw = direct_weighted = 0
            for start, step in affected:
                positions = [start + j * step for j in range(7)]
                before = [current[z] for z in positions]
                after = [current[z] ^ int(z in (x, y)) for z in positions]
                delta = int(len(set(after)) == 1) - int(len(set(before)) == 1)
                eid = (step - 1) * N - 3 * step * (step - 1) + start
                direct_raw += delta
                direct_weighted += delta * weights.get(eid, 1)
            require((direct_raw, direct_weighted) == (claimed_raw, claimed_weighted),
                    "joint flip gain mismatch")
            pairs_checked += 1
    best_result, _, _ = census(best)
    require(best_result["monochromatic_windows"] == claimed_best, "best cost mismatch")
    for profile in (result["edits"], best_result["edits"]):
        require(min(profile) >= 30 and sum(profile) >= 65, "heuristic floor mismatch")
    bits = Path(str(path) + ".best.bits").read_bytes()
    require(bits == ("".join(map(str, best)) + "\n").encode(), "best word byte mismatch")
    output = {"status": "EXACT_INTERVAL_COST_AND_ALL_GAINS_CHECKED", "current": result,
            "best": best_result, "best_word_sha256": hashlib.sha256(bits).hexdigest(),
            "weighted_edges": len(weights), "gain_entries_checked": 2 * N,
            "paired_move_entries_checked": 2 * pairs_checked}
    block_file = Path(str(path) + ".block.json")
    if block_file.exists():
        block = json.loads(block_file.read_text())
        require(set(block) in ({"r", "s", "raw", "weighted"},
                              {"r", "s", "raw", "weighted", "minimum"}), "wrong block fields")
        for field in ("raw", "weighted"):
            require(len(block[field]) == 4096 and
                    all(type(x) is int and x >= 0 for x in block[field]), "invalid block costs")
        values, coverage = literal_block(current, weights, block["r"], block["s"])
        require(block["raw"] == [x[0] for x in values] and
                block["weighted"] == [x[1] for x in values], "literal block cost mismatch")
        if "minimum" in block:
            points = [block["r"] + 617 * k for k in range(6)] + [block["s"] + 617 * k for k in range(6)]
            reference = [int(pow(x % 617, 308, 617) != 1) for x in points]
            optimum = None
            claimed_cost = None
            for mask, (count, cost) in enumerate(values):
                profile = result["edits"].copy()
                for i, x in enumerate(points):
                    if mask >> i & 1:
                        profile[reference[i]] += 1 if current[x] == reference[i] else -1
                if min(profile) < 30 or sum(profile) < 65:
                    continue
                score = (cost, count)
                if optimum is None or score < optimum:
                    optimum = score
                if mask == block["minimum"]["mask"]:
                    claimed_cost = score
            minimum = block["minimum"]
            require(minimum["feasible"] and optimum == claimed_cost ==
                    (minimum["weighted"], minimum["raw"]), "64-conditioning optimum mismatch")
            coverage["floor_constrained_minimum_checked"] = True
        output["block_audit"] = coverage
        output["block_audit"]["cost_entries_checked"] = 8192
        output["block_audit"]["canonical_cost_sha256"] = hashlib.sha256(
            json.dumps(values, separators=(",", ":")).encode()).hexdigest()
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("checkpoint", type=Path, nargs="?")
    parser.add_argument("--word", type=Path, help="count a literal 3704-bit word, without search metadata")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    require((args.checkpoint is None) != (args.word is None), "give exactly one checkpoint or --word")
    if args.word is not None:
        data = args.word.read_bytes()
        require(len(data) == N + 1 and data[-1:] == b"\n" and set(data[:-1]) <= {48, 49},
                "word must contain exactly 3704 binary digits and one newline")
        count, _, _ = census([b - 48 for b in data[:-1]])
        result = {"status": "EXACT_LITERAL_INTERVAL_WORD_COUNTED", "word": count,
                  "word_sha256": hashlib.sha256(data).hexdigest(),
                  "example_coordinates": "zero-based start, positive step, color"}
    else:
        result = audit(args.checkpoint)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")
