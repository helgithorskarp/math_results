"""One bounded serial exact process; optimized execution keeps all checks."""
import argparse
from pathlib import Path
import json
import pins
from corridor import algebra, bound, check_tail_root, digest, region, require
from baseline import run, controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit-candidate', action='store_true')
    args = parser.parse_args()
    algebra_record = algebra()
    original = run()
    damage_record = controls()
    threshold_checks = []
    for k in (3, 4, 5, 6, 8, 12, 64):
        b = bound(k)
        check_tail_root(k, b)
        require(region(b-6, k).startswith('excluded') and
                region(b-5, k).startswith('six_order') and
                region(b, k).startswith('six_order') and
                region(b+1, k).startswith('constructively_feasible'),
                'Strict threshold endpoints')
        threshold_checks.append({'k': k, 'b': b, 'corridor': [b-5, b],
                                 'tail_begins': b+1})
    record = {'agent': 'six-downset-3', 'role': 'researcher',
              'domain': 'Every integer k>=3,q>=max(4,k), every size-k deletion set Z',
              'parameter_coverage': 'All real kappa,t for the specified ansatz obstruction',
              'maximum_threshold_corridor_width': 6,
              'algebra': algebra_record, 'original_baseline': original,
              'endpoint_calibrations_only': threshold_checks,
              'controls': damage_record,
              'pins': pins.PINS, 'pin_source_commit': pins.SOURCE_COMMIT,
              'proof_boundary': 'Written ordinary universal inequality;9434 necessity and9195 tail imported; no formalization or review transfer'}
    record['record_sha256'] = digest(record)
    if not args.emit_candidate:
        expected = json.loads((Path(__file__).resolve().parent/'EXPECTED.json').read_text())
        require(record == expected, 'Entire frozen record, not only selected fields')
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
