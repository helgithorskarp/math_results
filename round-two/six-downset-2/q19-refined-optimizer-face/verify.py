"""NEW source-only cold refined reader, serial guarded normal/O children."""
from reader_binding import check_current, source_files, require
check_current()
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
import check_refined


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def validate(records, expected):
    require(canonical(records['refined']) == canonical(expected),
            'ENTIRE paid private mathematical record preserved in new reader')
    value = records['refined']
    g, v, e = (value['refined_geometry'], value['new_zero_degree_direction'],
               value['new_strict_endpoint'])
    require(g['full_affine_dimension'] == 24789 and g['invariant_affine_dimension'] == 108
            and g['fixed_coordinate_rows'] == 10910 and g['surviving_degree_rank'] == 165
            and g['independent_loop_rank'] == 1 and g['invariant_floor_rank'] == 6
            and g['invariant_minor_determinant'] == '8465264640'
            and g['both_entire_inverse_products'] and len(g['spanning_tree']) == 164,
            'complete refined original coordinate and floor-rank certificates')
    require(v['all303_original_degrees_zero'] and v['all_empty_anchor_and_loop_derivatives_zero']
            and v['affected_unordered_edges'] == 10620 and v['max_operator_norm_bound'] == 162
            and v['new_T_and_Bcap_floor'] == '943/1048576'
            and v['baseline_T_and_Bcap_floor'] == '1/1024'
            and e['allowed_ordered_positions'] == 72817 and e['forced_ordered_positions'] == 3391
            and e['all_original_L_positions_equal'] and e['all_original_T_positions_equal']
            and e['all_lower_and_upper_physical_differences_equal']
            and e['cost'] == '28529893/196608' and not e['new_LDL_claim'],
            'actual original zero-degree, strict-entry/cost and norm-transfer evidence')
    a = records['adverse']
    require(a['semantic_rejection_count'] == 22 and len(a['actual_semantic_rejections']) == 22
            and len({r['name'] for r in a['actual_semantic_rejections']}) == 22
            and all(r['exception'] == 'ValueError' and r['reason']
                    for r in a['actual_semantic_rejections'])
            and a['source_hash_crash_timeout_or_wrong_gate_not_counted']
            and a['all_rejections_post_complete_source_binding'],
            'all22 actual designated post-binding semantic controls')


def run(output, parent):
    root = Path(__file__).resolve().parent
    frozen = source_files(root)
    parent = Path(parent).resolve()
    parent_record = check_refined.bind_parent(parent)
    output = Path(output).resolve()
    require(output != root and root not in output.parents,
            'fresh verification outputs kept outside defining source')
    require(output != parent and parent not in output.parents,
            'fresh verification output outside published theorem dependency')
    output.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.pop('PYTHONPATH', None)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    observations, modes, controls = [], [], []
    whole = None
    with tempfile.TemporaryDirectory(prefix='q19-refined-source-only-', dir=output) as temp:
        coldroot = Path(temp)
        cold = coldroot / 'q19-refined-optimizer-face'
        dependency = coldroot / 'q19-sharp-ceiling'
        cold.mkdir()
        dependency.mkdir()
        for name, raw, pin in frozen:
            (cold / name).write_bytes(raw)
            require(hashlib.sha256((cold / name).read_bytes()).hexdigest() == pin,
                    'ENTIRE new isolated reader source copied: ' + name)
        (cold / 'SHA256SUMS').write_bytes((root / 'SHA256SUMS').read_bytes())
        for r in parent_record['records']:
            raw = (parent / r['file']).read_bytes()
            (dependency / r['file']).write_bytes(raw)
            require(hashlib.sha256(raw).hexdigest() == r['sha256'],
                    'entire published parent defining input copied: ' + r['file'])
        (dependency / 'SHA256SUMS').write_bytes((parent / 'SHA256SUMS').read_bytes())
        expected = json.loads((cold / 'EXPECTED.json').read_bytes())
        for optimized in (False, True):
            mode = 'optimized' if optimized else 'normal'
            records = {}
            for tag, script in [('refined', 'check_refined.py'), ('adverse', 'adverse.py')]:
                command = [sys.executable, '-B', '-s'] + (['-O'] if optimized else []) + [str(cold / script)]
                start = time.monotonic()
                result = subprocess.run(command, cwd=cold, env=env, capture_output=True, timeout=45)
                (output / (mode + '-' + tag + '.json')).write_bytes(result.stdout)
                (output / (mode + '-' + tag + '.stderr')).write_bytes(result.stderr)
                require(result.returncode == 0,
                        'new isolated child completed: ' + tag + ' ' + result.stderr.decode())
                record = json.loads(result.stdout)
                runtime = record.pop('runtime')
                require(set(runtime) == {'observed_seconds', 'peak_RSS_KiB'},
                        'only two explicitly named observational fields removed')
                records[tag] = record
                raw = canonical(record)
                observation = dict(mode=mode, tag=tag, seconds=time.monotonic() - start,
                    runtime=runtime, whole_mathematical_bytes=len(raw),
                    whole_mathematical_sha256=hashlib.sha256(raw).hexdigest(),
                    returncode=result.returncode, stderr=result.stderr.decode(),
                    fixed_child_guard_seconds=45, native_threads_one=True)
                observations.append(observation)
                print(json.dumps(observation), flush=True)
            validate(records, expected)
            raw = canonical(records)
            if whole is None:
                whole = records
            else:
                require(raw == canonical(whole), 'ENTIRE normal/O new source-only mathematics equal')
            modes.append(dict(mode=mode, whole_mathematical_bytes=len(raw),
                              whole_mathematical_sha256=hashlib.sha256(raw).hexdigest()))
        for optimized in (False, True):
            mode = 'optimized' if optimized else 'normal'
            command = [sys.executable, '-B', '-s'] + (['-O'] if optimized else []) + [str(cold / 'check_refined.py')]
            cases = [
                (cold, 'check_refined.py', 'ENTIRE NEW reader source before math import: check_refined.py'),
                (cold, 'EXPECTED.json', 'ENTIRE NEW reader source before math import: EXPECTED.json'),
                (dependency, 'model.py', 'entire credited parent input before import: model.py'),
                (dependency, 'BOUNDARY-CANDIDATE.json',
                 'entire credited parent input before import: BOUNDARY-CANDIDATE.json'),
            ]
            for directory, name, reason in cases:
                target = directory / name
                saved = target.read_bytes()
                target.write_bytes(saved + b'\nraise RuntimeError("SOURCE_CONTROL_MATH_REACHED")\n')
                try:
                    result = subprocess.run(command, cwd=cold, env=env, capture_output=True, timeout=45)
                    error = result.stderr.decode()
                    require(result.returncode != 0 and result.stdout == b''
                            and 'ValueError: ' + reason in error
                            and 'RuntimeError: SOURCE_CONTROL_MATH_REACHED' not in error,
                            'designated pre-math source corruption gate: ' + name)
                    controls.append(dict(mode=mode, source='new-reader' if directory == cold else 'parent',
                        file=name, reason=reason, returncode=result.returncode, mathematical_import_not_reached=True))
                finally:
                    target.write_bytes(saved)
    require([(name, pin) for name, raw, pin in source_files(root)] ==
            [(name, pin) for name, raw, pin in frozen], 'whole new reader source remains frozen')
    require(check_refined.bind_parent(parent) == parent_record,
            'whole published parent source remains frozen')
    raw = canonical(whole)
    (output / 'MATHEMATICS.json').write_bytes(raw)
    receipt = dict(agent='six-downset-2', role='researcher', all_completed=True,
        python_version=platform.python_version(), isolated_source_only=True,
        compact_new_reader_files=len(frozen), compact_new_reader_bytes=sum(len(blob) for name, blob, pin in frozen),
        frozen_new_reader_manifest_sha256=hashlib.sha256((root / 'SHA256SUMS').read_bytes()).hexdigest(),
        published_dependency_commit=check_refined.PARENT_COMMIT,
        dependency_full_manifest_sha256=check_refined.PARENT_SEAL,
        dependency_defining_files=parent_record['entire_files'], dependency_defining_bytes=parent_record['bytes'],
        entire_new_and_dependency_sources_bound_before_math_import=True,
        dependency_is_already_published_sibling_not_hidden_private_input=True,
        dependency_spectral_floor_is_explicit_published_theorem_premise=True,
        closed_dependency_factor_positive_checker_and_EXPECTED_not_math_replayed=True,
        complete_private_mathematical_record_bytes_preserved=30552,
        complete_private_mathematical_record_sha256='9a3503ca17cab704038f9998f8e923caab8dc8e1af674d068f3a6f383e0756a0',
        normal_optimized_entire_mathematics_equal=True,
        only_two_explicit_runtime_observations_removed=True,
        whole_mathematical_bytes=len(raw), whole_mathematical_sha256=hashlib.sha256(raw).hexdigest(),
        modes=modes, observations=observations, actual_semantic_rejections=44,
        distinct_pre_math_source_rejections=8, pre_math_source_controls=controls,
        fixed_child_guard_seconds=45, serial_mathematical_children=1, native_threads_one=True,
        completed_mathematical_children=4,
        max_observed_child_seconds=max(r['seconds'] for r in observations),
        peak_observed_child_RSS_KiB=max(r['runtime']['peak_RSS_KiB'] for r in observations),
        ordinary_bridges_unformalized=True, independent_review=False,
        private_creation_metadata_not_a_live_publication_or_graph_claim=True,
        packaging_not_new_mathematical_progress=True, no_publication_or_graph_submission_by_checker=True,
        resource_limits_timeout_crash_wrong_gate_never_nonexistence_or_success=True)
    (output / 'VALIDATION.json').write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    print(json.dumps({key: value for key, value in receipt.items() if key != 'observations'}), flush=True)
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--parent', type=Path,
                        default=Path(__file__).resolve().parent.parent / 'q19-sharp-ceiling')
    args = parser.parse_args()
    run(args.out, args.parent)
