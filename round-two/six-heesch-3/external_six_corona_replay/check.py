#!/usr/bin/env python3
"""Source identification and whole polygon replay of two public positives."""
from hashlib import sha256
import json
from pathlib import Path
import resource
import time
import decoder
import geometry as b
import polygon

HERE = Path(__file__).resolve().parent


def seal(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def run():
    start = time.monotonic()
    expected = json.loads((HERE / 'expected.json').read_text())
    cases = {}
    for tag, m, cap in [('h7', 7, False), ('h8l', 8, True)]:
        original = HERE / ('witness_' + tag + '.txt')
        e = expected[tag]
        b.require(sha256(original.read_bytes()).hexdigest() == e['foreign_sha256'],
                  'primary witness integrity mismatch')
        witness, decoded = decoder.decode(original, m, cap, HERE / 'drafter_tables.py')
        serialized = (json.dumps(witness, indent=2) + '\n').encode()
        b.require(sha256(serialized).hexdigest() == e['normalized_witness_sha256'],
                  'entire normalized placement list differs')
        projection = {'source_cycle42': decoded['source_cycle_scaled42'],
            'prototype_atoms': decoded['prototype_atoms'], 'affine_rows': decoded['affine_rows'],
            'source_isometry_orientation': decoded['prototype_to_G_source_orientation'],
            'source_isometry_translation42': decoded['prototype_to_G_source_translation_scaled42']}
        b.require(seal(projection) == e['source_geometry_and_all_affine_rows_sha256'],
                  'entire source/affine identification differs')
        result = polygon.check(witness)
        b.require(result['stable_mathematical_sha256'] == e['stable_full_polygon_sha256'],
                  'whole polygon result differs')
        prefixes = [{k: v for k, v in r.items() if k != 'whole_boundary_cycle'}
                    for r in result['prefixes']]
        b.require(prefixes == e['prefixes'] and result['level_counts'] == e['level_counts'] and
                  result['copies'] == e['copies'] and result['verified_coronas'] == 6,
                  'prefix record differs')
        cases[tag] = {'source_cells': decoded['source_cells'], 'hexagons': m, 'left_cap': cap,
            'copies': result['copies'], 'level_counts': result['level_counts'],
            'verified_disc_coronas': 6, 'prefixes': prefixes,
            'normalized_witness_sha256': e['normalized_witness_sha256'],
            'source_geometry_and_all_affine_rows_sha256': seal(projection),
            'whole_polygon_mathematical_sha256': result['stable_mathematical_sha256'],
            'whole_foreign_cell_vertex_equalities': decoded['whole_placement_cell_vertex_equalities'],
            'original_header_used_as_upper_proof': False}
    out = {'actual_author': 'six-heesch-3', 'role': 'researcher',
        'status': 'reproduction of existing public six-corona positives', 'cases': cases,
        'source_similarity_scale_and_rotation_exact': True,
        'every_prefix_disc_strict_surround_packing_grounding_and_no_skips_checked': True,
        'foreign_checker_or_solver_executed': False,
        'finite_upper_or_record_claimed': False, 'independently_peer_reviewed': False}
    out['stable_full_record_sha256'] = seal(out)
    out['elapsed_seconds'] = time.monotonic() - start
    out['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return out


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
