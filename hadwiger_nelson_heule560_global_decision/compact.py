"""Retain all family cones but minimality evidence for just the smallest core.

The omitted deletion witnesses are not premises of the public family claims.
This selects the evidence scope; it does not encode or archive the raw dump.
"""
import argparse
import copy
import json
from pathlib import Path


def compact(source):
    cert = copy.deepcopy(source)
    best = min(range(len(cert['negative_cores'])), key=lambda i: (cert['negative_cores'][i]['mask'].bit_count(), i))
    for i, row in enumerate(cert['negative_cores']):
        if i != best:
            del row['deletion_witnesses']
    cert['minimality_evidence_core_index'] = best
    return cert


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise ValueError('output must be fresh')
    args.output.write_text(json.dumps(compact(json.loads(args.input.read_text())), indent=2, sort_keys=True) + '\n')
