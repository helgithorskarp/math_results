#!/usr/bin/env python3
"""Compare full case keys, domain sizes, thresholds, and completion sets."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('fast', type=Path, nargs='?', default=HERE / 'report.json')
    ap.add_argument('literal', type=Path, nargs='?', default=HERE / 'literal_report.json')
    args = ap.parse_args()
    fast, literal = (json.loads(p.read_text()) for p in (args.fast, args.literal))
    require(fast['engine'] == 'fast' and literal['engine'] == 'literal', 'engine identity')
    require(len(fast['cases']) == len(literal['cases']) == 45, 'complete case counts')
    for a, b in zip(fast['cases'], literal['cases']):
        for key in ('H_mask', 'B_complement_mask', 'domains', 'need', 'solutions'):
            require(a[key] == b[key], ('entry-level case mismatch', key, a, b))
        require(a['solutions'] == [] and b['literal_four_sets'] == 1365, 'exact case verdict')
    for key in fast.keys() - {'engine', 'cases', 'total_nodes'}:
        require(fast[key] == literal[key], ('shared audit mismatch', key))
    print('PASS all 45 ordered case keys, row-domain sizes, thresholds, and empty completion sets agree')
    print('PASS small census, 82-model control, sharpness, and density-correction audits agree')


if __name__ == '__main__':
    main()
