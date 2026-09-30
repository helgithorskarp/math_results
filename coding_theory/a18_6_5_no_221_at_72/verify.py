#!/usr/bin/env python3
"""Check complete regenerated records against compact stable evidence."""
from itertools import combinations
import json
from pathlib import Path
import helpers as p


def witness_check(words, template):
    if any(type(w) is not int or w < 0 or w >= 1 << 18 for w in words):
        raise RuntimeError('invalid eighteen-point word mask')
    blocks = [frozenset(p.points(w)) for w in words]
    if len(set(blocks)) != len(words) or any(len(b) != 5 for b in blocks) or any(
            len(a & b) > 2 for a, b in combinations(blocks, 2)):
        raise RuntimeError('invalid attaining packing')
    if sum({0, 17} <= b for b in blocks) != 3:
        raise RuntimeError('attaining pair multiplicity differs')
    for center, wanted in [(17, [2, 2, 1]), (0, [2, 1, 1, 1])]:
        if sum(center in b for b in blocks) != 20:
            raise RuntimeError('attaining replication differs')
        row = sorted((5 - sum({center, z} <= b for b in blocks)
                      for z in range(18) if z != center), reverse=True)
        if [k for k in row if k] != wanted:
            raise RuntimeError('attaining row differs')
    if sorted(sum(1 << z for z in b if z != 17) for b in blocks if 17 in b) != template['star']:
        raise RuntimeError('attaining first star differs')


def summarize(work):
    work = Path(work)
    templates = json.loads((work / 'first_star_templates.json').read_text())
    baseline = json.loads((work / 'mixed_row_baseline.json').read_text())['cases']
    shapes = []
    model_keys = ['c_index', 'c', 'p', 'c_orbit_size', 'stabilizer_order', 'raw_h', 'h_orbits',
                  'raw_h_sha256', 'h_representatives_sha256', 'native_nodes',
                  'native_max_nodes', 'covers', 'output_cover_batch_sha256s', 'positives']
    replay_keys = ['c_index', 'c', 'h_orbits', 'nodes', 'max_nodes', 'covers']
    residual_keys = ['index', 'orbit_size', 'star', 'candidates', 'candidate_sha256',
                     'residual_maximum', 'packing_maximum', 'maximum_nodes', 'binary_nodes',
                     'attaining_words']
    for shape in (0, 2):
        census = json.loads((work / f'census_s{shape}.json').read_text())
        replay = json.loads((work / f'replay_s{shape}.json').read_text())
        residual = json.loads((work / f'residual_s{shape}.json').read_text())
        models = census['completed_models']
        checks = replay['completed_models']
        if [q['c_index'] for q in models] != list(range(census['c_orbits'])) or \
                [q['c_index'] for q in checks] != list(range(census['c_orbits'])):
            raise RuntimeError('INCOMPLETE degree-model coverage')
        if not census['status'].startswith('COMPLETE') or not replay['status'].startswith('COMPLETE') or \
                residual['status'] != 'COMPLETE' or census['definition_sha256'] != replay['definition_sha256']:
            raise RuntimeError('INCOMPLETE or inconsistent result')
        if sum(q['c_orbit_size'] for q in models) != 560 or \
                sum(q['c_orbit_size'] * q['raw_h'] for q in models) != 2118918:
            raise RuntimeError('wrong weighted carrier coverage')
        if any((a['c'], a['h_orbits'], a['covers']) != (b['c'], b['h_orbits'], b['covers'])
               for a, b in zip(models, checks)):
            raise RuntimeError('second engine coverage/counts differ')
        rows = residual['records']
        if [q['index'] for q in rows] != list(range(residual['joint_star_orbits'])) or \
                sum(q['orbit_size'] for q in rows) != residual['raw_second_stars']:
            raise RuntimeError('INCOMPLETE joint-star coverage')
        for q in rows:
            witness_check(q['attaining_words'], templates[shape])
        best = max(rows, key=lambda q: (q['packing_maximum'], -q['index']))
        shapes.append(dict(shape=shape, definition_sha256=census['definition_sha256'],
            candidates=len(baseline[shape]['candidate_quadruples']),
            candidate_sha256=baseline[shape]['candidate_sha256'],
            group_order=len(json.loads((work / f'c_orbits_s{shape}.json').read_text())['groups']),
            c_orbits=census['c_orbits'], weighted_c_choices=560, weighted_labeled_leaves=2118918,
            h_orbits=sum(q['h_orbits'] for q in models),
            production_nodes=sum(q['native_nodes'] for q in models),
            production_max_nodes=max(q['native_max_nodes'] for q in models),
            sparse_nodes=sum(q['nodes'] for q in checks), sparse_max_nodes=max(q['max_nodes'] for q in checks),
            cover_counts_by_p=[sum(q['covers'] for q in models if q['p'] == i) for i in range(4)],
            production_record_sha256=p.digest([{k: q[k] for k in model_keys} for q in models]),
            sparse_record_sha256=p.digest([{k: q[k] for k in replay_keys} for q in checks]),
            raw_second_stars=residual['raw_second_stars'], joint_star_orbits=residual['joint_star_orbits'],
            residual_minimum=min(q['residual_maximum'] for q in rows),
            residual_maximum=max(q['residual_maximum'] for q in rows),
            restricted_maximum=residual['sharp_restricted_maximum'],
            maximum_nodes=residual['maximum_nodes'], max_case_maximum_nodes=residual['max_case_maximum_nodes'],
            binary_nodes=residual['binary_nodes'], max_case_binary_nodes=residual['max_case_binary_nodes'],
            residual_record_sha256=p.digest([{k: q[k] for k in residual_keys} for q in rows]),
            attaining_words=best['attaining_words']))
    audit = json.loads((work / 'dlx_audit.json').read_text())
    if audit['status'] != 'COMPLETE':
        raise RuntimeError('INCOMPLETE kernel controls')
    audit_keys = ['direct_subset_fibers', 'sanitized_boundary_rows', 'malformed_inputs_rejected',
                  'invalid_caps_rejected', 'node_guard_visibly_incomplete', 'sanitized_p3_fibers',
                  'sanitizer_diagnostics']
    return dict(schema=1, agent='six-code-3', role='researcher', selected_marked_shapes=[0, 2],
                baseline=p.historical_baseline(), dependency=p.manifest, shapes=shapes,
                controls={k: audit[k] for k in audit_keys})


def main():
    actual = summarize(p.WORK)
    expected = json.loads((p.BASE / 'expected.json').read_text())
    if actual != expected:
        p.write('verification_mismatch.json', actual)
        raise RuntimeError('regenerated stable record differs from expected.json')
    print(json.dumps(dict(status='VERIFIED', marked_shape_maxima=[q['restricted_maximum'] for q in actual['shapes']],
                          cover_fibers=sum(q['h_orbits'] for q in actual['shapes']),
                          joint_star_orbits=sum(q['joint_star_orbits'] for q in actual['shapes']),
                          expected_sha256=p.digest(actual)), sort_keys=True))


if __name__ == '__main__':
    main()
