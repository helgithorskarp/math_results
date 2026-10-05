"""New isolated source-only ceiling checks; one mathematical child at a time."""
from binding import source_files, require
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import time


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def validate_whole(records, expected):
    for tag in ('structure', 'boundary', 'postline'):
        raw = canonical(records[tag])
        require(len(raw) == expected[tag]['canonical_mathematical_bytes']
                and hashlib.sha256(raw).hexdigest() == expected[tag]['canonical_mathematical_sha256'],
                'ENTIRE new mathematical record preserved: ' + tag)
    r = records['structure']
    require(r['original_LP_inequalities'] == 220 and r['original_LP_equalities'] == 30
            and r['complete_dual_objective_coordinates'] == 144
            and r['inequality_weights_nonnegative'] and r['original_free_coordinate_count'] == 35865
            and r['additional_independent_GG_equations'] == 9000
            and r['new_boundary_affine_dimension'] == 15969
            and r['new_boundary_invariant_affine_dimension'] == 104
            and r['exact_original_cost_slope'] == 848
            and r['both_whole_inverse_products_checked'] and r['full143_exact_affine_line_coordinates'],
            'whole new dual, original-coordinate census, rank and cost-line evidence')
    for tag, tau in (('boundary', '42901/98304'), ('postline', '5363/12288')):
        r = records[tag]
        require(r['tau'] == tau and r['original_ranks'] == [302, 302]
                and r['original_entries']['all_allowed_ordered_positions'] == 72817
                and len(r['original_entries']['tight_actual_positions']) == 3391
                and r['full_original_actions']['entire_original_action_positions'] == 181202
                and r['full_original_Schur']['full_original_schur_action_positions'] == 58081
                and r['full_physical_floor'] == '1/1024'
                and len(r['all_six_Schur_PD']) == 6 and len(r['all_twelve_shifted_forms']) == 12
                and all(v['positive_definite'] for v in r['all_six_Schur_PD'].values())
                and all(v['positive_definite'] for v in r['all_twelve_shifted_forms'].values()),
                'both new full-original entry, physical and Schur certificates')
    require(records['boundary']['sharp_cost_attained']
            and records['postline']['refined_piecewise_cost_bound_attained']
            and records['postline']['refined_cost_excess'] == '405/16384'
            and records['postline']['original_negative_GG_count'] == 3240,
            'actual new sharp and refined cost attainment')
    r = records['adverse']
    require(r['semantic_rejection_count'] == 17 and len(r['actual_semantic_rejections']) == 17
            and len({v['name'] for v in r['actual_semantic_rejections']}) == 17
            and all(v['exception'] == 'ValueError' and v['reason'] for v in r['actual_semantic_rejections'])
            and r['KG_countermodel_all180_floors_and_all8_equations_verified']
            and r['negative_forced_GG_countermodel_all180_floors_and_five_sharp_equations_verified']
            and r['source_hash_crash_timeout_and_resource_status_not_counted_as_math_rejection'],
            'all17 actual new post-binding mathematical controls')


def run(output):
    root = Path(__file__).resolve().parent
    frozen = source_files(root)
    output = Path(output).resolve()
    require(output != root and root not in output.parents,
            'verification output kept outside defining source')
    output.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.pop('PYTHONPATH', None)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    observations = []
    modes = []
    controls = []
    complete = None
    with tempfile.TemporaryDirectory(prefix='q19-ceiling-source-only-', dir=output) as temp:
        cold = Path(temp) / 'source'
        cold.mkdir()
        for name, raw, sha in frozen:
            (cold / name).write_bytes(raw)
            require(hashlib.sha256((cold / name).read_bytes()).hexdigest() == sha,
                    'ENTIRE isolated defining file copied: ' + name)
        (cold / 'SHA256SUMS').write_bytes((root / 'SHA256SUMS').read_bytes())
        expected = json.loads((cold / 'EXPECTED.json').read_bytes())
        programs = [('structure', 'check_structure.py', []),
                    ('boundary', 'check_boundary.py', ['--candidate', 'BOUNDARY-CANDIDATE.json']),
                    ('postline', 'check_postline.py', ['--candidate', 'POSTLINE-CANDIDATE.json']),
                    ('adverse', 'adverse.py', [])]
        for optimized in (False, True):
            mode = 'optimized' if optimized else 'normal'
            records = {}
            for tag, script, args in programs:
                target = output / (mode + '-' + tag + '.json')
                log = target.with_suffix('.stdout')
                command = [sys.executable, '-B', '-s'] + (['-O'] if optimized else []) + [str(cold / script)] + args
                if tag != 'adverse':
                    command += ['--out', str(target)]
                began = time.monotonic()
                with log.open('wb') as stdout, target.with_suffix('.stderr').open('wb') as stderr:
                    p = subprocess.run(command, cwd=cold, env=env, stdout=stdout, stderr=stderr, timeout=45)
                error = target.with_suffix('.stderr').read_text()
                require(p.returncode == 0, 'new cold mathematical child completed: ' + tag + ' ' + error)
                if tag == 'adverse':
                    target.write_bytes(log.read_bytes())
                record = json.loads(target.read_bytes())
                runtime = {k: record.pop(k) for k in ('observed_seconds', 'peak_RSS_KiB')}
                records[tag] = record
                raw = canonical(record)
                obs = dict(mode=mode, tag=tag, seconds=time.monotonic() - began, runtime=runtime,
                    whole_mathematical_bytes=len(raw), whole_mathematical_sha256=hashlib.sha256(raw).hexdigest(),
                    returncode=p.returncode, stderr=error, fixed_child_guard_seconds=45, native_threads_one=True)
                observations.append(obs)
                print(json.dumps(obs), flush=True)
            validate_whole(records, expected)
            raw = canonical(records)
            if complete is None:
                complete = records
            else:
                require(raw == canonical(complete),
                        'ENTIRE new normal/optimized cold mathematics equality before hashing')
            modes.append(dict(mode=mode, whole_mathematical_bytes=len(raw),
                              whole_mathematical_sha256=hashlib.sha256(raw).hexdigest()))
        # Distinct source controls; never counted as semantic mathematical rejects.
        for optimized in (False, True):
            mode = 'optimized' if optimized else 'normal'
            for name in ('model.py', 'DUAL.json'):
                target = cold / name
                original = target.read_bytes()
                target.write_bytes(original + b'\nraise RuntimeError("SOURCE_CONTROL_MATH_IMPORT_REACHED")\n')
                try:
                    command = [sys.executable, '-B', '-s'] + (['-O'] if optimized else []) + [
                        str(cold / 'check_structure.py'), '--out', str(output / 'unreachable.json')]
                    p = subprocess.run(command, cwd=cold, env=env, capture_output=True, text=True, timeout=45)
                    require(p.returncode != 0 and p.stdout == ''
                            and 'ValueError: ENTIRE source seal before mathematical import: ' + name in p.stderr
                            and 'RuntimeError: SOURCE_CONTROL_MATH_IMPORT_REACHED' not in p.stderr,
                            'actual whole source rejection before mathematical import: ' + name)
                    controls.append(dict(mode=mode, file=name, returncode=p.returncode,
                        mathematical_import_not_reached=True,
                        reason='ENTIRE source seal before mathematical import: ' + name))
                finally:
                    target.write_bytes(original)
    require([(n, sha) for n, raw, sha in source_files(root)] == [(n, sha) for n, raw, sha in frozen],
            'entire defining source unchanged through new verification')
    raw = canonical(complete)
    (output / 'MATHEMATICS.json').write_bytes(raw)
    receipt = dict(agent='six-downset-2', role='researcher', all_completed=True,
        python_version=platform.python_version(), source_only_cold=True,
        frozen_source_files=len(frozen), frozen_source_bytes=sum(len(v) for n, v, s in frozen),
        frozen_manifest_sha256=hashlib.sha256((root / 'SHA256SUMS').read_bytes()).hexdigest(),
        entire_source_bytes_checked_before_mathematical_import=True,
        complete_private_mathematical_record_bytes_preserved=True,
        normal_optimized_entire_mathematics_equal=True,
        only_two_explicit_top_level_runtime_observation_fields_removed=True,
        mathematical_record_bytes=len(raw), mathematical_record_sha256=hashlib.sha256(raw).hexdigest(),
        modes=modes, observations=observations, total_mathematical_children=8, actual_semantic_rejections=34,
        distinct_source_binding_children=4, source_binding_rejections=controls,
        ordinary_bridges_unformalized=True, independent_review=False,
        fixed_child_guard_seconds=45, native_threads_one=True, serial_mathematical_children=1,
        max_observed_child_seconds=max(o['seconds'] for o in observations),
        peak_observed_child_RSS_KiB=max(o['runtime']['peak_RSS_KiB'] for o in observations),
        no_solver_or_old_factor_needed=True, no_publication_or_graph_submission=True,
        resource_status_never_mathematical_nonexistence=True)
    (output / 'VALIDATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'observations'}), flush=True)
    return receipt


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    run(p.parse_args().out)
