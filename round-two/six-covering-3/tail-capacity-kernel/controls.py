"""Semantic source/certificate rejection controls, executed in both modes."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path

import audit
import check
import separate


def main():
    here = Path(__file__).resolve().parent
    original = json.loads((here / "fixture.json").read_text())
    expected = json.loads((here / "expected.json").read_text())
    damages = []
    def damaged(name, mutate):
        f = deepcopy(original); mutate(f); damages.append((name, f))
    damaged("changed owned prefix", lambda f: f["prefix"][4].__setitem__(1, 4))
    damaged("missing original base", lambda f: f["base_phases"].pop())
    damaged("repeated original base", lambda f: f["base_phases"].__setitem__(1, f["base_phases"][0][:]))
    damaged("tail substituted for base", lambda f: f["base_phases"][0].__setitem__(0, 16))
    damaged("boolean original phase", lambda f: f["base_phases"][0].__setitem__(1, True))
    damaged("phase outside family", lambda f: f["base_phases"][0].__setitem__(1, 15))
    damaged("fractional kernel point", lambda f: f["kernel_cofactor_fibers"][1].__setitem__(0, 2.5))
    damaged("repeated kernel point", lambda f: f["kernel_cofactor_fibers"][1].__setitem__(1, 2))
    damaged("uncovered ternary ban", lambda f: f["kernel_cofactor_fibers"][1].__setitem__(0, 1))
    damaged("missing kernel point", lambda f: f["kernel_cofactor_fibers"][1].pop())
    damaged("unexpected odd fiber", lambda f: f["kernel_cofactor_fibers"].__setitem__(0, [2]))
    # This legal original15 class meets kernel cofactor point2.
    damaged("base now covers kernel", lambda f: f["base_phases"][0].__setitem__(1, 2))
    for name, f in damages:
        for verifier in (check.verify, audit.verify):
            try:
                verifier(f, expected)
            except ValueError:
                continue
            raise ValueError("damaged source accepted: "+name)
    sample = (0, 1, 2, 3, 5, 6, 8, 9)
    cases = 0
    for mask in range(1 << len(sample)):
        H = [x for i, x in enumerate(sample) if mask & (1 << i)]
        literal = next((list(t) for t in combinations(H, 3) if
                        all(len({x % d for x in t}) == 3 for d in (5, 7, 9)) and
                        len({x % 3 for x in t}) > 1), None)
        if separate.admissible_triple(H) != literal:
            raise ValueError("bit-mask separator misses or invents a literal triple")
        cases += 1
    result = separate.separate(original["base_phases"])
    if (result["status"] != "EXACT TAIL CAPACITY OBSTRUCTION" or
        result["kernel_cofactor_fibers"] != original["kernel_cofactor_fibers"] or
        result["base_clause_canonical_sha256"] != expected["hitting_clause_sha256"]):
        raise ValueError("separator does not reconstruct the frozen original certificate")
    return {"damages_rejected_by_each_engine": len(damages), "engines": 2,
            "separator_tiny_truth_cases": cases, "frozen_stage_separation": True}


if __name__ == "__main__":
    print(json.dumps(main(), sort_keys=True, separators=(",", ":")))
