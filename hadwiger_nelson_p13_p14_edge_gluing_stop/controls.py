#!/usr/bin/env python3
"""Small malformed-evidence controls for the independent checker."""

from copy import deepcopy
import json

from verify import HERE, verify


def main():
    expected = json.loads((HERE / "expected.json").read_text())
    verify(expected)
    rejected = []

    def reject(name, mutation):
        bad = deepcopy(expected)
        mutation(bad)
        try:
            verify(bad)
        except ValueError as error:
            rejected.append({"case": name, "reason": str(error)})
        else:
            raise ValueError("accepted malformed evidence: " + name)

    reject("monochromatic positive word", lambda x: x.update(three_word="0" * 253))
    reject("even alleged odd cycle", lambda x: x.update(odd_cycle=x["odd_cycle"][:-1]))
    reject("wrong physical order", lambda x: x["report"].update(physical_vertices=254))
    reject("wrong edge hash", lambda x: x["report"].update(edge_sha256="0" * 64))
    print(json.dumps({"verified": True, "rejected": rejected,
                      "rejection_count": len(rejected)},
                     sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
