"""Independent retained-core audit. Only the literal core is mathematical input.

Exact complete half-subset tables, literal left subsets, and cross-half merge.
No author search implementation, expected answers or maximum certificate used.
"""
import argparse
from array import array
from collections import Counter, deque
from itertools import combinations
import hashlib
import json
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def validate_words(words):
    require(all(type(w) is int and 0 < w < 1 << 18 and w.bit_count() == 5
                for w in words), "word domain")
    require(len(set(words)) == len(words), "duplicate word")
    require(all((a & b).bit_count() <= 2 for a, b in combinations(words, 2)),
            "packing intersection")


def adjacency(words):
    rows = [0] * len(words)
    for i, a in enumerate(words):
        for j in range(i):
            if (a & words[j]).bit_count() >= 3:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
    return rows


def merge(rows, forbidden=(0,), emit_maxima=False):
    """Return exact independence numbers/counts; forbidden masks delete vertices.

    Right table counts each subset via disjoint include/exclude branches. Left
    side visits every literal mask exactly once. A full set has a unique split.
    Unsigned counts cannot overflow: a right half has at most 18 vertices and
    hence at most 2**18 independent sets. Merged counts are Python integers.
    """
    n = len(rows)
    require(n <= 36, "fixed resource scope exceeded; no conclusion")
    require(all(type(m) is int and 0 <= m < 1 << n for m in rows), "adjacency domain")
    require(all(not (rows[i] >> i & 1) for i in range(n)), "graph self loop")
    require(all((rows[i] >> j & 1) == (rows[j] >> i & 1)
                for i in range(n) for j in range(i)), "asymmetric graph")
    require(all(type(f) is int and 0 <= f < 1 << n for f in forbidden), "forbidden domain")
    left = n // 2
    right = n - left
    lm = (1 << left) - 1
    rm = (1 << right) - 1
    ra = [rows[left + i] >> left for i in range(right)]
    size = bytearray(1 << right)
    count = array("I", [0]) * (1 << right)
    require(count.itemsize >= 4, "right count storage width")
    witness = array("I", [0]) * (1 << right)
    count[0] = 1
    for mask in range(1, 1 << right):
        bit = mask & -mask
        i = bit.bit_length() - 1
        absent = mask ^ bit
        present = absent & ~ra[i]
        s0, s1 = size[absent], 1 + size[present]
        if s0 > s1:
            size[mask], count[mask], witness[mask] = s0, count[absent], witness[absent]
        elif s1 > s0:
            size[mask], count[mask], witness[mask] = s1, count[present], witness[present] | bit
        else:
            size[mask] = s0
            count[mask] = count[absent] + count[present]
            witness[mask] = witness[absent]
    valid = bytearray(1 << left)
    allowed = array("I", [0]) * (1 << left)
    valid[0], allowed[0] = 1, rm
    maxsize = [-1] * len(forbidden)
    maxcount = [0] * len(forbidden)
    maxwitness = [0] * len(forbidden)
    left_forbid = [f & lm for f in forbidden]
    right_forbid = [f >> left for f in forbidden]
    eligible_left = [] if emit_maxima else None
    valid_left_count = 0
    for mask in range(1 << left):
        if mask:
            bit = mask & -mask
            i = bit.bit_length() - 1
            previous = mask ^ bit
            if not valid[previous] or previous & rows[i]:
                continue
            valid[mask] = 1
            allowed[mask] = allowed[previous] & ~(rows[i] >> left)
        valid_left_count += 1
        cardinality = mask.bit_count()
        for k, f in enumerate(left_forbid):
            if mask & f:
                continue
            rights = allowed[mask] & ~right_forbid[k]
            value = cardinality + size[rights]
            if value > maxsize[k]:
                maxsize[k], maxcount[k] = value, int(count[rights])
                maxwitness[k] = mask | int(witness[rights]) << left
            elif value == maxsize[k]:
                maxcount[k] += int(count[rights])
        if emit_maxima:
            eligible_left.append(mask)
    result = {"optima": [[a, c, w] for a, c, w in zip(maxsize, maxcount, maxwitness)],
              "left_masks": 1 << left, "right_masks": 1 << right,
              "valid_left_masks": valid_left_count}
    if emit_maxima:
        require(forbidden == (0,), "emit only unrestricted maximum inventory")
        def attain(mask):
            if not mask:
                yield 0
                return
            bit = mask & -mask
            i = bit.bit_length() - 1
            absent, present = mask ^ bit, (mask ^ bit) & ~ra[i]
            if size[absent] == size[mask]:
                yield from attain(absent)
            if 1 + size[present] == size[mask]:
                for value in attain(present):
                    yield value | bit
        maxima = []
        for mask in eligible_left:
            rights = allowed[mask]
            if mask.bit_count() + size[rights] == maxsize[0]:
                maxima.extend(mask | v << left for v in attain(rights))
        maxima.sort()
        require(len(maxima) == len(set(maxima)) == maxcount[0], "maximum inventory count")
        result["maxima"] = maxima
    return result


def core_oracle(core):
    validate_words(core)
    require(len(core) == 57, "core size")
    universe = sorted(sum(1 << p for p in t) for t in combinations(range(18), 5))
    owner = {}
    for i, word in enumerate(core):
        for t in combinations(bits(word), 3):
            mask = sum(1 << p for p in t)
            require(mask not in owner, "repeated core triple")
            owner[mask] = i
    oracle = []
    for word in universe:
        direct = sum(1 << i for i, c in enumerate(core) if (word & c).bit_count() >= 3)
        triples = 0
        for t in combinations(bits(word), 3):
            i = owner.get(sum(1 << p for p in t))
            if i is not None:
                triples |= 1 << i
        require(direct == triples, "independent triple/intersection oracle disagreement")
        oracle.append([word, direct])
    return oracle


def domain(oracle, deleted):
    mask = sum(1 << i for i in deleted)
    return [word for word, conflicts in oracle if not conflicts & ~mask]


def run(core, out, pilot):
    started = time.monotonic()
    oracle = core_oracle(core)
    whole = {"core": core, "oracle_sha256": hashlib.sha256(encoded(oracle)).hexdigest(),
             "universe_words": len(oracle),
             "blocker_histogram": dict(sorted(Counter(m.bit_count() for _, m in oracle).items()))}
    fullwords = domain(oracle, ())
    full = merge(adjacency(fullwords), emit_maxima=True)
    tails = [sorted(fullwords[i] for i in bits(m)) for m in full["maxima"]]
    for tail in tails:
        validate_words(core + tail)
    whole["full_core"] = {"words": fullwords, "maximum": full["optima"][0][:2],
                           "tails": sorted(tails),
                           "left_masks": full["left_masks"], "right_masks": full["right_masks"]}
    pairs = list(combinations(range(len(core)), 2))
    if pilot:
        pairs = pairs[:5] + [p for p in pairs if len(domain(oracle, p)) == 36]
    records = []
    chunk_start = time.monotonic()
    for case_index, pair in enumerate(pairs):
        words = domain(oracle, pair)
        a, b = (1 << words.index(core[p]) for p in pair)
        result = merge(adjacency(words), (0, a, b, a | b))
        optima = []
        for forbidden, (size, count, wit) in zip((0, a, b, a | b), result["optima"]):
            tail = [words[i] for i in bits(wit)]
            require(not wit & forbidden and len(tail) == size, "forbidden/witness alignment")
            retained = [word for i, word in enumerate(core) if i not in pair]
            validate_words(retained + tail)
            optima.append([size, count, tail])
        records.append({"deleted": list(pair), "candidate_words": words, "optima": optima,
                        "left_masks": result["left_masks"], "right_masks": result["right_masks"],
                        "valid_left_masks": result["valid_left_masks"]})
        require(time.monotonic() - chunk_start <= 45, "fixed45-second chunk guard; incomplete is no theorem")
        if (case_index + 1) % 50 == 0:
            print(json.dumps({"complete_pairs": case_index + 1,
                              "seconds": time.monotonic() - started}), flush=True)
            chunk_start = time.monotonic()
    whole["two_deleted"] = records
    if not pilot:
        require([r["deleted"] for r in records] == [list(p) for p in combinations(range(57), 2)],
                "complete unique pair case coverage")
        singles = []
        for i in range(57):
            words = domain(oracle, (i,))
            f = 1 << words.index(core[i])
            result = merge(adjacency(words), (0, f))
            maxima = []
            for forbidden, (size, count, wit) in zip((0, f), result["optima"]):
                tail = [words[j] for j in bits(wit)]
                require(not wit & forbidden and len(tail) == size, "single witness")
                validate_words([w for j, w in enumerate(core) if j != i] + tail)
                maxima.append([size, count, tail])
            singles.append({"deleted": i, "candidate_words": words, "optima": maxima})
        whole["one_deleted"] = singles
    out.write_bytes(encoded(whole))
    summary = {"complete": not pilot, "pairs": len(records),
               "pair_domain_histogram": dict(sorted(Counter(len(r["candidate_words"]) for r in records).items())),
               "pair_unrestricted": dict(sorted(Counter(tuple(r["optima"][0][:2]) for r in records).items())),
               "pair_forbid_either": dict(sorted(Counter(tuple(o[:2]) for r in records for o in r["optima"][1:3]).items())),
               "pair_forbid_both": dict(sorted(Counter(tuple(r["optima"][3][:2]) for r in records).items())),
               "full_core_maximum": full["optima"][0][:2],
               "whole_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
               "whole_bytes": out.stat().st_size, "seconds": time.monotonic() - started}
    # JSON keys cannot be pairs. Encode distributions as literal sorted rows.
    for k in ("pair_unrestricted", "pair_forbid_either", "pair_forbid_both"):
        summary[k] = [[list(key), value] for key, value in summary[k].items()]
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--pilot", action="store_true")
    args = parser.parse_args()
    literal = json.loads(args.core.read_bytes())["core_words"]
    run(literal, args.out, args.pilot)
