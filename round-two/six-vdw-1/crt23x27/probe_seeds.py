"""Exact cost census of 54 invalid near-product construction seeds."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from check import qr_word, require


def probe(words, output):
    u = qr_word(23)
    u_patterns = Counter(sum(u[(a + j * r) % 23] << j for j in range(7))
                         for a in range(23) for r in range(23))
    values = []
    for word in words:
        v = [word >> j & 1 for j in range(27)]
        v_patterns = Counter(sum(v[(a + j * r) % 27] << j for j in range(7))
                             for a in range(27) for r in range(27))
        cost = sum(n * (v_patterns[p] + v_patterns[p ^ 127]) for p, n in u_patterns.items()) - 621
        values.append((cost, word))
    require(len(values) == 54 and len(set(words)) == 54, "wrong seed coverage")
    cost, v = min(values)
    bits = [u[n % 23] ^ (v >> (n % 27) & 1) for n in range(621)]
    # Independent direct definition-level count, with all nonzero steps,
    # including cyclic tuples with repeated residues.
    actual = sum(len({bits[(a + j * d) % 621] for j in range(7)}) == 1
                 for a in range(621) for d in range(1, 621))
    require(actual == cost and cost > 0, "invalid seed cost assertion")
    text = ("".join(map(str, bits)) + "\n").encode()
    output.write_bytes(text)
    return {"status": "INVALID_CONSTRUCTION_SEEDS_EXACTLY_COUNTED", "seeds": 54,
            "cost_histogram": sorted([cost, n] for cost, n in Counter(c for c, _ in values).items()),
            "best_v_word": v, "ordered_monochromatic_windows": actual,
            "word_sha256": hashlib.sha256(text).hexdigest(), "valid_witness": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("checked", type=Path)
    parser.add_argument("--word", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.checked.read_text())
    print(json.dumps(probe(data["result"]["v_after_step2"], args.word), sort_keys=True))
