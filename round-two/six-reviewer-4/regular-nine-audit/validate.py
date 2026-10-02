"""Consequential coverage/record damages and native input-domain controls."""
import argparse
import copy
import json
import subprocess
import itertools as it
from pathlib import Path
from reproduce import ROOT, check
import inventory


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=False)
    actual = json.loads((args.replay / "RESULTS.json").read_bytes())
    expected = json.loads((ROOT / "RESULTS.json").read_bytes())
    check(actual, expected)
    transport_checks = 0
    wrong_local_reversal_witness = None
    for word in (g["local_word"] for g in actual["inventory"]["local_classes"]):
        rows = inventory.adjacency(word, 3)
        for p in it.permutations(range(3)):
            for o in it.product(range(3), repeat=3):
                for a in (1, 2):
                    mapping = [3 * p[i] + (a * t + o[i]) % 3 for i in range(3) for t in range(3)]
                    moved = [0] * 9
                    for u, v in it.combinations(range(9), 2):
                        if (rows[u] >> v) & 1:
                            moved[mapping[u]] |= 1 << mapping[v]
                            moved[mapping[v]] |= 1 << mapping[u]
                    decoded = inventory.adjacency(inventory.relabel_word(rows, p, o, a), 3)
                    if decoded != moved:
                        raise ValueError("physical transport is not the encoded graph")
                    transport_checks += 1
        mapping = [3 * i + ((-t) % 3 if i == 0 else t) for i in range(3) for t in range(3)]
        moved = [set() for _ in range(9)]
        for u, v in it.combinations(range(9), 2):
            if (rows[u] >> v) & 1:
                moved[mapping[u]].add(mapping[v]); moved[mapping[v]].add(mapping[u])
        shift = lambda u: 3 * (u // 3) + (u % 3 + 1) % 3
        if any((v in moved[u]) != (shift(v) in moved[shift(u)]) for u, v in it.combinations(range(9), 2)):
            wrong_local_reversal_witness = word
    if wrong_local_reversal_witness is None:
        raise ValueError("missing control for forbidden partial reversal")
    damages = []
    for name in ("omit_frame", "alter_A_word", "change_column", "omit_local_word", "positive_completion", "omit_K_word", "lost_matrix_case"):
        bad = copy.deepcopy(actual)
        if name == "omit_frame": bad["inventory"]["frames"].pop()
        if name == "alter_A_word": bad["inventory"]["frames"][0]["local_word"] ^= 1
        if name == "change_column": bad["inventory"]["frames"][0]["columns"][0] ^= 1
        if name == "omit_local_word": bad["inventory"]["local_classes"][0]["labeled_words"].pop()
        if name == "positive_completion": bad["completion"]["per_frame_valid"][0] = 1
        if name == "omit_K_word": bad["completion"]["k_candidates"] -= 1
        if name == "lost_matrix_case": bad["structure"]["regular_matrix_controls"].pop()
        try:
            check(bad, expected)
        except ValueError:
            damages.append(name)
        else:
            raise ValueError("damaged complete record accepted")
    source = (args.replay / "frames.txt").read_text().splitlines()
    native = []
    for name in ("column_not_four", "wrong_H_degrees", "noninteger_frame"):
        fields = source[0].split()
        if name == "column_not_four": fields[1] = "1"
        if name == "wrong_H_degrees": fields[0] = "0"
        if name == "noninteger_frame": fields[1] = "garbage"
        path = args.work / (name + ".txt")
        path.write_text(" ".join(fields) + "\n")
        result = subprocess.run([str((args.replay / "complete").resolve()), str(path.resolve()),
                                 str(ROOT / "primary21.rows"), str((args.work / name).resolve())],
                                capture_output=True, timeout=60)
        if result.returncode == 0:
            raise ValueError("damaged native domain accepted")
        native.append({"damage": name, "message": result.stderr.decode().strip()})
    record = {"status": "VALIDATION_PASS", "whole_record_damages": damages, "native_domain_damages": native,
              "complete_physical_representative_transports": transport_checks,
              "forbidden_partial_reversal_breaks_C3_on_word": wrong_local_reversal_witness}
    (args.work / "validation.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()
