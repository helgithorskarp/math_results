"""Optional literal author comparison; this does not supply independence.

Pass a separately downloaded pinned profile_16_19_exclusion directory.
Routine proof verification uses check.py and local_pair.py without it.
"""
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json
import time
import check


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--author', type=Path, required=True)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    start = time.monotonic()
    provenance = json.loads((check.HERE/'INPUTS.json').read_text())['author_comparison']
    for name, expected in provenance['files'].items():
        check.require(sha256((args.author/name).read_bytes()).hexdigest() == expected, 'author input integrity')
    rows = check.reconstruct()
    raw, cut = check.inventories(rows)
    producer = load_module('credited_producer', args.author/'produce.py')
    verifier = load_module('credited_verifier', args.author/'verify.py')
    check.require(rows == producer.carriers() == verifier.carriers(), 'literal mark comparison')
    check.require(raw == producer.screen(rows) == verifier.screen(rows, False), 'literal raw inventory comparison')
    check.require(cut == producer.screen(rows, True) == verifier.screen(rows, True), 'literal cut inventory comparison')
    record = dict(agent='six-reviewer-5', role='independent mathematical reviewer',
                  scope='Entrywise comparison only; credited author code supplies no independent charge proof',
                  author_commit=provenance['source_commit'], three_readouts_equal=True,
                  marks=len(rows), raw=len(raw), cut=len(cut), seconds=time.monotonic()-start)
    if args.out:
        args.out.write_bytes(check.encode(record))
    print(json.dumps(record, sort_keys=True))


if __name__ == '__main__':
    main()
