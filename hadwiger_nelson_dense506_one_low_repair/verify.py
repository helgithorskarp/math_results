#!/usr/bin/env python3
"""Verify the complete one-outside-point repair stratum for the dense506 hosts."""
from pathlib import Path
import argparse
import json
from engine import Census


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate-work', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    args = p.parse_args()
    args.work.mkdir(parents=True, exist_ok=False)
    census = Census(args.candidate_work)
    rows, screen = census.screen()
    centres, positive = census.exact(rows)
    table, result = census.check_pairs(centres, positive)
    result = {'screen': screen, **result}
    (args.work / 'centres.json').write_text(json.dumps(table, separators=(',', ':')) + '\n')
    (args.work / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
