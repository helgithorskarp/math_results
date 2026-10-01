"""Entrywise dual replay and literal witness check. six-code-2, researcher."""
from pathlib import Path
import json
import resource
import sys
import time

import produce
import verify
from common import compact_manifest, digest, require


def main():
    root = Path(__file__).resolve().parent
    start = time.monotonic()
    given = json.loads((root / 'input.json').read_text())
    expected = json.loads((root / 'manifest.json').read_text())
    a, b = produce.run(given), verify.run(given)
    keys = sorted(set(a) - {'execution'})
    require(set(a) == set(b), 'producer/verifier schemas differ')
    for key in keys:
        require(a[key] == b[key], 'producer/verifier arrays differ entrywise: ' + key)
    require(not a['negative_carrier'], 'a gap<=13 family exists')
    require(compact_manifest(a) == compact_manifest(b) == expected, 'replay manifest differs')
    witness = json.loads((root / 'witness.json').read_text())
    require(witness['four_parts'] == given['sharp_four_parts']
            and witness['gaps'] == a['sharp_gaps'] and witness['words'] == a['sharp_code']
            and {k: witness[k] for k in ['size','s','a','t','g','R']}
            == {'size': 60, 's': 0, 'a': 0, 't': 6, 'g': 14, 'R': 14}, 'witness differs')
    print(json.dumps({'agent': 'six-code-2', 'role': 'researcher', 'status': 'COMPLETE',
                      'entrywise_arrays': keys, 'manifest_sha256': digest(expected),
                      'sharp_gap_cost': 14, 'sharp_code_size': 60,
                      'producer_seconds': a['execution']['seconds'],
                      'verifier_seconds': b['execution']['seconds'],
                      'pattern_cases': len(b['execution']['patterns']),
                      'largest_pattern_states': max(p['states'] for p in b['execution']['patterns']),
                      'literal_opposite_tests': b['execution']['opposite_tests_sum'],
                      'total_seconds': time.monotonic() - start,
                      'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'python': sys.version.split()[0], 'independent_peer_review': False,
                      'written_bridges_formalized': False}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(2 if 'INCOMPLETE' in str(error) else 1)
