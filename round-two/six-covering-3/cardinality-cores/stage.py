"""Check the15 necessary predicates at one fully specified base assignment."""

import argparse
import json
from pathlib import Path

from model import evaluate

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("base_phases", type=Path)
    args = ap.parse_args()
    print(json.dumps(evaluate(json.loads(args.base_phases.read_text())), sort_keys=True))
