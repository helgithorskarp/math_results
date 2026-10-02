"""Flat combination cover producer; all negative domains must be complete."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hypergraph', type=Path)
    parser.add_argument('--size', type=int, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(1 <= args.size <= 15 and not args.out.exists(), 'new size-specific proposal')
    record = json.loads(args.hypergraph.read_text())
    require(record['mask'] == 72 and record['edge_sha256'] ==
            'b44cf8af4cbb78425f5bfc3c4b82c9e050fe57bb82e691200c6756b5241d4846', 'frozen audited profile72 input')
    edges = record['edges']
    require(hashlib.sha256(json.dumps(edges, separators=(',', ':'), sort_keys=True).encode()).hexdigest()
            == record['edge_sha256'], 'whole actual edge bytes, not a self-reported hash')
    columns = {r: sum((1 << e) for e, support in enumerate(edges) if r in support)
               for r in range(1, 31)}
    target = (1 << len(edges)) - 1
    total = math.comb(29, args.size - 1)
    sha = hashlib.sha256()
    tested = 0
    first = None
    for rest in itertools.combinations(range(2, 31), args.size - 1):
        require(tested < 2000000, 'fixed two-million-candidate guard; incomplete is not an exclusion')
        hit = columns[1]
        for r in rest:
            hit |= columns[r]
        covers = hit == target
        sha.update(bytes(rest) + bytes([int(covers)]))
        tested += 1
        if covers:
            first = [1] + list(rest)
            break
    result = {'author': 'six-vdw-1', 'role': 'researcher',
              'schema': 'F31_PHASE72_NORMALIZED_COVER_PROPOSAL_V1',
              'status': 'DIRECT_POSITIVE_COVER' if first else 'COMPLETE_NO_NORMALIZED_COVER',
              'mask': 72, 'edge_sha256': record['edge_sha256'], 'size': args.size,
              'fixed_vertex': 1, 'candidate_domain_size': total,
              'tested_count': tested, 'complete': tested == total,
              'first_cover': first, 'covers_found': int(first is not None),
              'coverage_sha256': sha.hexdigest(), 'candidate_guard': 2000000,
              'scope': 'Normalized covers containing1 only. Whole scalar automorphisms justify the cover reduction; no coloring repair sufficiency.'}
    require(first is not None or tested == total, 'negative domain is incomplete')
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True))
