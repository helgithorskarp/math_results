#!/usr/bin/env python3
"""Regenerate, independently check, and compare all compact evidence."""
import json
from pathlib import Path
import sys
import cases
import branches
import check_cases
import check_branches
import controls


def main():
    root = Path(__file__).resolve().parent
    case_doc = cases.certificate()
    branch_doc = branches.certificate()
    for name, generated in (("cases.json", case_doc), ("branches.json", branch_doc)):
        if json.loads((root / name).read_text()) != generated:
            raise ValueError("regenerated certificate differs: " + name)
    result = {"status": "PASS", "cases": check_cases.check(case_doc),
              "branches": check_branches.check(branch_doc),
              "controls": controls.run(case_doc, branch_doc)}
    if (root / "expected.json").exists():
        if json.loads((root / "expected.json").read_text()) != result:
            raise ValueError("expected report differs")
    elif "--bootstrap-expected" not in sys.argv:
        raise ValueError("missing expected report")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
