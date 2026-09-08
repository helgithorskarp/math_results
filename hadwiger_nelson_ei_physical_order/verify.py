"""Verifier for the EI physical-order obstruction and explicit union."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import model

ROOT = Path(__file__).resolve().parent


def verify():
    g40, g49, _, _, _ = model.inputs()
    kernel, copies = model.normalized_g49_kernel(g49)
    results = []
    for choices, outer, core in model.outer_cases():
        results.append({'choices': list(map(int, choices)),
                        'outer_points': len(outer),
                        'unavoidable_points': len(core),
                        'point_sha256': model.point_digest(core)})
    constructions = {}
    for mask in (151, 1682):
        construction, points = model.canonical_union(mask)
        construction['physical_point_sha256'] = model.point_digest(points)
        constructions[str(mask)] = construction
    case_stream = json.dumps(results, sort_keys=True, separators=(',', ':')).encode()
    return {
        'verified': True,
        'g49_attachment_isometries_per_pair': len(copies),
        'g49_orientation_independent_kernel_points': len(kernel),
        'outer_isometry_cases': len(results),
        'compulsory_pair_occurrences_per_case': 96,
        'unavoidable_order_histogram': {
            str(k): v for k, v in sorted(Counter(r['unavoidable_points'] for r in results).items())
        },
        'minimum_unavoidable_points': min(r['unavoidable_points'] for r in results),
        'target_508_excluded_by_unavoidable_core': min(r['unavoidable_points'] for r in results) > 508,
        'distinct_outer_core_point_hashes': len(set(r['point_sha256'] for r in results)),
        'outer_case_stream_sha256': hashlib.sha256(case_stream).hexdigest(),
        'explicit_non_four_colourable_unions': constructions,
        'minimum_physical_union_points': min(
            construction['physical_union_points'] for construction in constructions.values()
        ),
    }


def main():
    result = verify()
    expected = json.loads((ROOT / 'expected.json').read_text())
    if result != expected:
        raise ValueError('expected-result mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
