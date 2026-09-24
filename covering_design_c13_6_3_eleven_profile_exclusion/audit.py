"""Independent full audit, optionally partitioned into deterministic ranges."""
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
import argparse
import json
from pathlib import Path

from audit_joins import prepare, join, digest
from audit_residual import Space, solve

ROOT = Path(__file__).resolve().parent


def run_range(bounds):
    lo, hi = bounds
    roots, templates = prepare()
    if len(roots) != 704:
        raise ValueError('unexpected full marked-root count')
    primary_rows = json.loads((ROOT / 'ROOTS.json').read_text())['rows']
    primary = {tuple(row[:4]): row[6] for row in primary_rows}
    spaces = {}
    records = []
    for root in roots[lo:hi]:
        configurations, raw = join(root, templates)
        code = digest(configurations)
        key = (root['design'], root['h'], root['q'], root['r'])
        if key in primary and primary[key] != code:
            raise ValueError('independent joined configuration sets disagree')
        if root['r'] not in spaces:
            spaces[root['r']] = Space(12, root['r'])
        totals = Counter()
        for fixed in configurations:
            answer = solve(spaces[root['r']], fixed, root['h'], root['q'])
            if answer['status'] != 'UNSAT':
                raise ValueError(('unexpected independent completion', root, answer))
            totals['point_states'] += answer['point_states']
            totals['bundle_states'] += answer['bundle_states']
        records.append(dict(**root, raw=raw, configurations=len(configurations),
                            configurations_sha256=code, primary_set_match=key in primary,
                            status='UNSAT', **dict(totals)))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--write-reference', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.workers <= 704:
        parser.error('workers must be between 1 and 704')
    bounds = [(704 * i // args.workers, 704 * (i + 1) // args.workers) for i in range(args.workers)]
    if args.workers == 1:
        parts = [run_range(bounds[0])]
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            parts = list(pool.map(run_range, bounds))
    records = sorted((record for part in parts for record in part), key=lambda r: r['id'])
    if [r['id'] for r in records] != list(range(704)) or any(r['status'] != 'UNSAT' for r in records):
        raise ValueError('incomplete independent audit')
    summary = dict(status='INDEPENDENT_NO_11_10_9_PROFILE', roots=len(records),
                   second_link_pointed_templates=899,
                   raw_identifications=sum(r['raw'] for r in records),
                   compatible_joins=sum(r['configurations'] for r in records),
                   roots_without_compatible_joins=sum(not r['configurations'] for r in records),
                   primary_join_sets_matched=sum(r['primary_set_match'] for r in records),
                   point_states=sum(r.get('point_states', 0) for r in records),
                   bundle_states=sum(r.get('bundle_states', 0) for r in records),
                   root_records_sha256=sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest(),
                   links_file_sha256=sha256((ROOT / 'LINKS.json').read_bytes()).hexdigest())
    if args.write_reference:
        (ROOT / 'AUDIT_EXPECTED.json').write_text(json.dumps(summary, indent=2) + '\n')
    elif summary != json.loads((ROOT / 'AUDIT_EXPECTED.json').read_text()):
        raise ValueError('independent audit summary mismatch')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
