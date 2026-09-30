#!/usr/bin/env python3
"""Check rejection at the certificate's mathematical trust boundaries."""
import copy
import itertools
import json
import tempfile
from pathlib import Path

from verify import ROOT, verify


def nodes(tree):
    yield tree
    if "v" in tree:
        yield from nodes(tree["i"])
        yield from nodes(tree["o"])


def main():
    original = json.loads((ROOT / "certificates.json").read_text())
    mutations = []
    bad = copy.deepcopy(original)
    bad["seed_sha256"] = "0" * 64
    mutations.append(("wrong seed identity", bad))
    bad = copy.deepcopy(original)
    bad["cases"].pop()
    mutations.append(("missing coordinate pair", bad))
    bad = copy.deepcopy(original)
    bad["cases"][0]["proofs"][0]["avoid"] = 17
    mutations.append(("wrong side orientation", bad))
    bad = copy.deepcopy(original)
    first = bad["cases"][0]["proofs"][0]["tree"]
    leaf = next(n for n in nodes(first) if n.get("c"))
    leaf["c"][0] &= leaf["c"][0] - 1
    mutations.append(("uncovered active word", bad))
    bad = copy.deepcopy(original)
    branch = next(n for n in nodes(bad["cases"][0]["proofs"][0]["tree"]) if "v" in n)
    branch["v"] = 1000
    mutations.append(("out-of-range branch vertex", bad))
    bad = copy.deepcopy(original)
    branch = next(n for n in nodes(bad["cases"][0]["proofs"][0]["tree"]) if "v" in n)
    del branch["o"]
    mutations.append(("missing exclusion branch", bad))
    bad = copy.deepcopy(original)
    coupled = next(c for c in bad["cases"] if c["mode"] == "coupled")
    witness = next(n for n in nodes(coupled["proofs"][0]["tree"]) if "w" in n)
    witness["w"] = []
    mutations.append(("incomplete terminal witness", bad))
    bad = copy.deepcopy(original)
    coupled = next(c for c in bad["cases"] if c["mode"] == "coupled")
    coupled["mode"] = "one-side"
    coupled["proofs"].pop()
    mutations.append(("false empty side classification", bad))

    # Preserve the partition while merging two classes containing compatible words.
    seed = [frozenset(i for i, c in enumerate(row) if c == "1")
            for row in (ROOT / "acl69.txt").read_text().splitlines()]
    p, q = original["cases"][0]["coordinates"]
    core = [w for w in seed if p not in w and q not in w]
    words = [frozenset(t) for t in itertools.combinations(range(18), 5)
             if q not in t and frozenset(t) not in core
             and all(len(frozenset(t) & fixed) <= 2 for fixed in core)]
    words.sort(key=lambda w: sum(1 << v for v in w))
    bad = copy.deepcopy(original)
    merged = False
    for leaf in nodes(bad["cases"][0]["proofs"][0]["tree"]):
        if "c" not in leaf:
            continue
        parts = leaf["c"]
        for i, j in itertools.combinations(range(len(parts)), 2):
            if any(len(words[u] & words[v]) <= 2
                   for u in range(len(words)) if parts[i] >> u & 1
                   for v in range(len(words)) if parts[j] >> v & 1):
                parts[i] |= parts[j]
                parts.pop(j)
                merged = True
                break
        if merged:
            break
    if not merged:
        raise RuntimeError("could not construct a conflicting-color audit mutation")
    mutations.append(("compatible words in a conflict class", bad))
    rejected = []
    with tempfile.TemporaryDirectory(prefix="acl-pair-audit-", dir=ROOT) as temporary:
        path = Path(temporary) / "bad.json"
        for name, bad in mutations:
            path.write_text(json.dumps(bad))
            try:
                verify(ROOT / "acl69.txt", path)
            except ValueError:
                rejected.append(name)
            else:
                raise RuntimeError(f"checker accepted {name}")
    print(json.dumps({"rejected_mutations": rejected}, indent=2))


if __name__ == "__main__":
    main()
