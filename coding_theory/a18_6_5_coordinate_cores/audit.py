#!/usr/bin/env python3
"""Require rejection of incomplete or mathematically invalid certificates."""
import copy
import itertools
import json
import tempfile
from pathlib import Path

from verify import ALPHABET, ROOT, verify


def main():
    original = json.loads((ROOT / "certificates.json").read_text())
    mutations = []
    bad = copy.deepcopy(original)
    bad["seed_sha256"] = "0" * 64
    mutations.append(("wrong seed identity", bad))
    bad = copy.deepcopy(original)
    bad["covers"].pop()
    mutations.append(("missing support", bad))
    bad = copy.deepcopy(original)
    bad["covers"][0]["colors"] = bad["covers"][0]["colors"][:-1]
    mutations.append(("missing residual word", bad))
    bad = copy.deepcopy(original)
    bad["covers"][0]["colors"] = "Z" + bad["covers"][0]["colors"][1:]
    mutations.append(("out-of-range color", bad))
    bad = copy.deepcopy(original)
    bad["covers"][0]["colors"] = "?" + bad["covers"][0]["colors"][1:]
    mutations.append(("unknown color", bad))
    seed = [frozenset(i for i, c in enumerate(s) if c == "1")
            for s in (ROOT / "acl69.txt").read_text().splitlines()]
    core = [b for b in seed if 0 not in b]
    removed = [b for b in seed if 0 in b]
    candidates = [frozenset(b) for b in itertools.combinations(range(18), 5)
                  if frozenset(b) not in seed
                  and all(len(frozenset(b) & a) <= 2 for a in core)]
    v, c = next((v, c) for v, b in enumerate(candidates)
                for c, old in enumerate(removed) if len(b & old) <= 2)
    bad = copy.deepcopy(original)
    labels = list(bad["covers"][0]["colors"])
    labels[v] = ALPHABET[c]
    bad["covers"][0]["colors"] = "".join(labels)
    mutations.append(("compatible pair in one class", bad))
    rejected = []
    with tempfile.TemporaryDirectory(prefix="audit-tmp-", dir=ROOT) as tmp:
        path = Path(tmp) / "bad.json"
        for name, bad in mutations:
            path.write_text(json.dumps(bad))
            try:
                verify(path)
            except ValueError:
                rejected.append(name)
            else:
                raise RuntimeError(f"checker accepted {name}")
    print(json.dumps({"rejected_mutations": rejected}, indent=2))


if __name__ == "__main__":
    main()
