"""Produce selected original-clamping and complete two-marked-touch data.

Packed Boolean columns and dyadic anchor aggregation are imported from the
credited, hash-pinned semantic/anchor sources. No heuristic search is used.
"""
import hashlib
import importlib.util
from itertools import combinations
import json
import os
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
SOURCE = Path(os.environ.get("SORTING_SOURCE_ROOT", ROOT.parents[2]))
BASE = "round-two/six-sorting-2/native24-kernel-cover/"
PINS = {
    BASE + "fixture.json": "93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6",
    BASE + "certificate.json": "21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06",
    BASE + "touch-certificate.json": "04bcf3e1617c3ae2ce026149d1c76f620c8acf6e38bdc448719e26fa3ecd2455",
    BASE + "normalize-certificate.json": "99bcad813962ff1495a7f9f217b5ec4a8b94b83e71020754ff5eacf6f7abe490",
}
CODE_PINS = {
    "profile.py": "dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719",
    "anchors.py": "0b95573e7e3c446d0b7ca5352f6b5f4b8d92b91d6f3c72e7b4f783cd99d89902",
}
IDS = [2, 8, 15, 20, 24, 31, 32, 33, 34, 36, 38, 39, 41, 42]


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def load_sources():
    sources = {}
    for path, pin in PINS.items():
        raw = (SOURCE / path).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == pin, "published input changed: " + path)
        sources[path] = json.loads(raw)
    directory = SOURCE / "round-two/six-sorting-2/semantic-pruning"
    for name, pin in CODE_PINS.items():
        need(hashlib.sha256((directory / name).read_bytes()).hexdigest() == pin,
             "published column/anchor code changed: " + name)
    spec = importlib.util.spec_from_file_location("three_touch_anchors", directory / "anchors.py")
    anchor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(anchor)
    return sources, anchor


def pruning(gates, low, high, semantic):
    free = [i for i in range(13) if not (low | high) >> i & 1]
    columns = iter(semantic.truth_columns(len(free)))
    values = ["L" if low >> i & 1 else "H" if high >> i & 1 else next(columns) for i in range(13)]
    carrier = [free.index(i) if i in free else None for i in range(13)]
    word, d, r, redundant = [], 0, 0, 0
    for t, (a, b) in enumerate(gates):
        x, y = values[a], values[b]
        if isinstance(x, str) or isinstance(y, str):
            rank = lambda z: -1 if z == "L" else 1 if z == "H" else 0
            d += 1
            if rank(x) > rank(y):
                values[a], values[b] = y, x
                carrier[a], carrier[b] = carrier[b], carrier[a]
        else:
            if not x & ~y:
                r += 1
                redundant |= 1 << t
            else:
                word.append([carrier[a], carrier[b]])
            values[a], values[b] = x & y, x | y
    current = semantic.marked_ports(values)
    output = [i for i in range(13) if isinstance(values[i], int)]
    rename = {carrier[i]: j for j, i in enumerate(output)}
    return {"outer_record": [low, high, *current, d, r, redundant],
            "input_free_wires": free, "output_free_wires": output,
            "input_to_output_wire": [rename[i] for i in range(len(free))],
            "retained_prefix": [[rename[a], rename[b]] for a, b in word]}


def full_boolean(gates):
    image, wrong = set(), {}
    for x in range(8192):
        y = x
        for a, b in gates:
            if y >> a & 1 and not y >> b & 1:
                y ^= (1 << a) | (1 << b)
        correct = 8192 - (1 << (13 - x.bit_count()))
        need(all((y >> p & 1) == (correct >> p & 1) for p in (0, 1, 11, 12)),
             "outer frozen output ranks differ")
        image.add((y >> 2) & 511)
        for p in range(13):
            if p not in wrong and (y >> p & 1) != (correct >> p & 1):
                wrong[p] = [p, x, y, y >> p & 1, correct >> p & 1]
    return sorted(image), [wrong[p] for p in sorted(wrong)]


def two_touch_cover(low, high, wrong_ports):
    """Enumerate marked subsequences, with all free preparations omitted.

    The written proof establishes that every <=2-marked-touch sorting suffix
    is covered, using the imported unique (2,3) restriction.
    """
    initial = ["L" if low >> p & 1 else "H" if high >> p & 1 else "F" for p in range(13)]
    required = [p for p in wrong_ports if (low | high) >> p & 1]
    gates = [(2, 3), *combinations(range(3, 11), 2)]
    rank = {"L": -1, "F": 0, "H": 1}
    counts, terminal = [0, 0, 0], []

    def visit(row, word, touched):
        counts[len(word)] += 1
        lo = sum(1 << p for p, x in enumerate(row) if x == "L")
        hi = sum(1 << p for p, x in enumerate(row) if x == "H")
        if word.count([2, 3]) == 1 and (lo, hi) == (7, 7168):
            terminal.append({"word": word, "untouched_required_ports": [p for p in required if p not in touched]})
        if len(word) == 2:
            return
        for a, b in gates:
            if row[a] == row[b] == "F" or (a, b) == (2, 3) and [2, 3] in word:
                continue
            child = list(row)
            if rank[child[a]] > rank[child[b]]:
                child[a], child[b] = child[b], child[a]
            visit(child, word + [[a, b]], touched | {a, b})

    visit(initial, [], set())
    terminal.sort(key=lambda x: x["word"])
    return {"allowed_standard_pairs": [list(g) for g in gates],
            "required_initial_marked_wrong_ports": required,
            "complete_counts_by_marked_word_length": counts,
            "root_terminal_words": terminal,
            "compatible_words": [x["word"] for x in terminal if not x["untouched_required_ports"]]}


def generate(fixture, sources, anchor):
    native, kernels, touch, normalized = (sources[BASE + name] for name in
                                          ("fixture.json", "certificate.json", "touch-certificate.json", "normalize-certificate.json"))
    need(fixture["previous_nine_wire_ids"] == normalized["remaining_nine_wire_ids"] == IDS,
         "parent frontier differs")
    need(fixture["native_prefix24"] == native["gates"][:24] and fixture["known46"] == native["gates"],
         "literal native source differs")
    need(fixture["forced_gates"] == native["forced_gates"] == [[11, 12], [1, 2]], "forced pair differs")
    need([r["kernel_id"] for r in fixture["cases"]] == IDS, "case cover differs")
    cases = []
    for item in fixture["cases"]:
        i = item["kernel_id"]
        need(item["kernel"] == kernels["kernels"][i]["kernel"], "literal kernel ID differs")
        need(i in touch["single_wire2_touch_kernel_ids"], "unique wire2 touch not covered")
        gates = fixture["native_prefix24"] + fixture["forced_gates"] + item["kernel"]
        image, wrong = full_boolean(gates)
        need(image == kernels["kernels"][i]["target"]["image"], "parent nine-wire image differs")
        pruned = pruning(gates, item["original_low_mask"], item["original_high_mask"], anchor.semantic)
        row = pruned["outer_record"]
        need(row[2] == 19 and row[3] in (6656, 7168), "wrong three-low/three-high class")
        profiles = anchor.semantic.analyze(7, pruned["retained_prefix"])
        compact = {name: {"low_count": x["low_count"], "high_count": x["high_count"],
                          "envelope": x["envelope"], "records_sha256": digest(x["records"]),
                          "summary": x["summary"]} for name, x in profiles.items()}
        anchors = anchor.both(7, profiles)
        bound = max(16, *(x["lower_bound"] for x in anchors.values()))
        cover = two_touch_cover(row[2], row[3], [x[0] for x in wrong])
        need(not cover["compatible_words"], "a two-touch word remains compatible")
        need(row[4] + row[5] + bound == 42, "selected nested cost differs")
        cases.append({"kernel_id": i, "prefix32_sha256": digest(gates),
                      "target9_image": image, "target9_sha256": digest(image),
                      "full_boolean_wrong_port_witnesses": wrong, "pruning": pruned,
                      "inner_profiles": compact, "inner_anchors": anchors, "inner_bound": bound,
                      "prefix_cost": row[4] + row[5], "C_plus_B": 42,
                      "two_touch_cover": cover, "minimum_future_marked_touches": 3,
                      "total_size_lower_bound": 45})
    return {"schema": "native-three-marked-touch-certificate-v1", "agent": "six-sorting-1",
            "role": "researcher", "parent_files_sha256": PINS,
            "credited_fourteen_target_graph": "bafkreie4gyppvazofxko6ohk7jbbltjmae6caeamkvb3tqflb5x2l7qzre",
            "previous_nine_wire_ids": IDS, "excluded_kernel_ids": IDS,
            "remaining_nine_wire_ids": [], "native_prefix24_standard_size_lower_bound": 45,
            "cases": cases}


def main():
    start = time.monotonic()
    sources, anchor = load_sources()
    fixture = json.loads((ROOT / "fixture.json").read_bytes())
    result = generate(fixture, sources, anchor)
    path = ROOT / "certificate.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"agent": "six-sorting-1", "role": "researcher",
                      "status": "THREE_TOUCH_CERTIFICATE_REGENERATED", "new_kernel_exclusions": len(IDS),
                      "remaining_native_targets": 0, "certificate_bytes": path.stat().st_size,
                      "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "seconds": time.monotonic() - start,
                      "maximum_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == "__main__":
    main()
