"""Contact sieve on exactly the full family retained by the previous global sieve."""
from collections import Counter
import json
import sys
import base_model


def classify(data):
    old = base_model.classify(data)
    if not old.get("baseline") or not old.get("keep"):
        return {"baseline": False, "previous": old}
    a, b, _ = base_model.factors(data)
    ca = Counter(a)
    violations = []
    for x, population in sorted(ca.items()):
        contacts = sum(base_model.dot(x, y) for y in b)
        if population >= 3 and not 10 <= contacts <= 13:
            violations.append({"type": x, "multiplicity": population, "red_contacts": contacts})
    return {"baseline": True, "keep": not violations, "violations": violations}


def physical(data):
    return base_model.physical(data)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    print(json.dumps({"classification": classify(data), "graph": physical(data)}, sort_keys=True))
