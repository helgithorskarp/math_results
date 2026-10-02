"""Post-seal comparison through actual A transports; not a proof premise."""
import argparse
import itertools as it
import json
from pathlib import Path
import inventory


def compare(own, original, work, author_work):
    mappings = {}
    own_groups = own["inventory"]["local_classes"]
    for group in own_groups:
        word = group["local_word"]
        rows = inventory.adjacency(word, 3)
        author_rep = next(int(key) for key, words in original["A_groups"].items() if word in words)
        if set(group["labeled_words"]) != set(original["A_groups"][str(author_rep)]):
            raise ValueError("complete labeled A orbit differs")
        found = None
        for p in it.permutations(range(3)):
            for o in it.product(range(3), repeat=3):
                for a in (1, 2):
                    if inventory.relabel_word(rows, p, o, a) == author_rep:
                        found = (p, o, a)
                        break
                if found:
                    break
            if found:
                break
        if not found:
            raise ValueError("no physical transport")
        p, o, a = found
        mappings[word] = (author_rep, [3 * p[i] + (a * t + o[i]) % 3
                                    for i in range(3) for t in range(3)])
    translated = []
    for frame in own["inventory"]["frames"]:
        rep, mapping = mappings[frame["local_word"]]
        seeds = []
        for mask in frame["column_first_masks"]:
            moved = sum(1 << mapping[u] for u in range(9) if (mask >> u) & 1)
            seeds.append(min(moved, inventory.shift(moved), inventory.shift(inventory.shift(moved))))
        translated.append((rep, tuple(sorted(seeds))))
    expected = [(f["word"], tuple(f["column_seeds"])) for f in original["frames"]]
    if sorted(translated) != sorted(expected):
        raise ValueError("entire transported incidence sets differ")
    own_k = (work / "native.kwords.txt").read_bytes()
    author_k = (author_work / "direct-K-words.txt").read_bytes()
    if own_k != author_k:
        raise ValueError("entire K stream differs")
    own_outcomes = (work / "native.valid.bin").read_bytes()
    author_outcomes = (author_work / "direct-outcomes.txt").read_bytes()
    # Align frames before comparing EVERY completion position. The complete K
    # set is invariant under the accompanying B relabeling. Here every value is
    # zero, so this is an equality of full negative inventories, not a claim
    # that word indices agree after an arbitrary relabeling.
    if len(own_outcomes) != len(author_outcomes) or bytes(x + ord('0') for x in own_outcomes) != author_outcomes:
        raise ValueError("full negative outcome inventories differ")
    return {"complete_labeled_A_words_equal": sum(len(g["labeled_words"]) for g in own_groups),
            "complete_transported_frame_sets_equal": len(translated),
            "complete_K_words_equal": len(own_k.splitlines()),
            "complete_negative_outcome_entries_equal": len(own_outcomes),
            "transports": {str(k): {"author_rep": v[0], "physical_A_image": v[1]} for k, v in mappings.items()},
            "first_bad_color_counts_differ_by_declared_spine_order": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--author-work", type=Path, required=True)
    parser.add_argument("--author-expected", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    record = compare(json.loads((args.work / "RESULTS.json").read_bytes()),
                     json.loads(args.author_expected.read_bytes()), args.work, args.author_work)
    args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()
