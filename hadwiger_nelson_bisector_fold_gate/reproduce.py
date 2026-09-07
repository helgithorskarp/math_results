#!/usr/bin/env python3
"""Check the complete one-axis reflection gate for the nine-move509 seed."""
import argparse
import json
from pathlib import Path
import folds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    expected = json.loads((folds.HERE / 'expected.json').read_text())
    data = (folds.SEED / 'certificate.json').read_bytes()
    folds.require(folds.seed.digest(data) == expected['seed_certificate_sha256'], 'seed certificate hash')
    certificate = json.loads(data)
    _, rows, _ = folds.seed.construct(certificate, folds.seed.load_inputs(certificate))
    edges = folds.unit_edges(rows, 96)
    result = folds.analyse(rows, edges)
    folds.require(result == expected['result'], 'complete fold-gate result mismatch')
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
