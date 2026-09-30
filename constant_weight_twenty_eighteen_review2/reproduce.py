#!/usr/bin/env python3
"""Complete public reproduction; expected output contains only mathematical data."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace

import audit
import marked
import validate
from exact import insist, encoded


def stable(x):
    if isinstance(x, dict):
        return {k: stable(v) for k, v in x.items() if k not in
                ('seconds', 'native_seconds', 'peak_child_rss_kib', 'fingerprint')}
    if isinstance(x, list):
        return [stable(v) for v in x]
    return x


def collect(work):
    result = {'main': stable(json.loads((work / 'summary.json').read_text())),
              'marked': stable(json.loads((work / 'marked-summary.json').read_text())),
              'validation': stable(json.loads((work / 'validation/validation.json').read_text()))}
    result['proof_status'] = 'COMPLETE computer-assisted independent review'
    return result


def run(args):
    audit.run(SimpleNamespace(engine=args.engine, target=args.target, work=args.work, limit=None))
    marked.run(args.work, args.work)
    validate.run(SimpleNamespace(engine=args.sanitized_engine or args.engine, target=args.target,
                                 work=args.work, output=args.work / 'validation'))
    result = collect(args.work)
    data = encoded(result)
    if args.record:
        args.expected.write_bytes(data)
    else:
        insist(data == args.expected.read_bytes(), 'complete independent expected record mismatch')
    print(json.dumps({'status': result['proof_status'], 'cases': result['main']['cases'],
                      'covers': result['main']['cover_counts'], 'marked_star_pairs': result['marked']['normalized_star_pairs'],
                      'expected_sha256': sha256(data).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', type=Path, required=True)
    parser.add_argument('--sanitized-engine', type=Path)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--target', type=Path, default=Path(__file__).resolve().parents[1] / 'coding_theory/a18_6_5_twenty_eighteen_absent_pair')
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--record', action='store_true', help='Explicit baseline recording, not expected-record comparison')
    run(parser.parse_args())
