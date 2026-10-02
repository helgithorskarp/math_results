"""Standalone lower-witness checker; no search or producer import."""
import json
from itertools import combinations
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def packing(words):
    need(len(set(words)) == len(words), "duplicate word")
    triples = set()
    for word in words:
        need(type(word) is int and 0 < word < 2 ** 18 and word.bit_count() == 5, "word domain")
        points = [p for p in range(18) if word >> p & 1]
        for triple in combinations(points, 3):
            need(triple not in triples, "repeated physical triple")
            triples.add(triple)
    need(len(triples) == 10 * len(words), "triple cardinality")


def verify(core, tails, exceptions, witnesses):
    need(len(core) == len(set(core)) == 57, "core size")
    packing(core)
    need(len(tails) == len({tuple(t) for t in tails}) == 84, "84 tails")
    for tail in tails:
        need(len(tail) == 12 and not set(core) & set(tail), "tail scope")
        packing(core + tail)
    need(witnesses["size69_tail"] in tails, "full witness")
    single = witnesses["exact56_size68"]
    i, tail = single["omitted"], single["tail"]
    need(type(i) is int and 0 <= i < 57 and len(tail) == 12, "singleton scope")
    need(not set(core) & set(tail), "exact56 retention")
    packing([w for k, w in enumerate(core) if k != i] + tail)
    expect = [r[:2] for r in exceptions]
    actual = [r["omitted"] for r in witnesses["exact55_size68"]]
    need(len(expect) == len({tuple(p) for p in expect}) == 66 and actual == expect, "all66 sharp pair witnesses")
    for witness in witnesses["exact55_size68"]:
        pair, tail = witness["omitted"], witness["tail"]
        need(len(pair) == 2 and 0 <= pair[0] < pair[1] < 57 and len(tail) == 13, "pair scope")
        need(not set(core) & set(tail), "exact55 retention")
        packing([w for k, w in enumerate(core) if k not in pair] + tail)
    return {"standalone84_full69_codes": 84, "standalone_exact56_size68": 1,
            "standalone_exact55_size68": 66}


if __name__ == "__main__":
    root = Path(__file__).parent
    load = lambda name: json.loads((root / name).read_bytes())
    result = verify(load("CORE.json")["core_words"], load("FULL_CORE_TAILS.json"),
                    load("EXACT55_EXCEPTIONS.json"), load("SHARP_TAILS.json"))
    print(json.dumps(result, sort_keys=True))
