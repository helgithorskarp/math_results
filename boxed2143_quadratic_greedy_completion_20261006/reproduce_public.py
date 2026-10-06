#!/usr/bin/env python3
"""Portable I/O orchestration; all mathematical sources remain unchanged."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from time import perf_counter

HERE = Path(__file__).resolve().parent


def fp(p):
    data = p.read_bytes()
    return {'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output-directory', type=Path, required=True)
    args = ap.parse_args()
    out = args.output_directory.resolve()
    if out.exists():
        raise SystemExit('Preserve the existing output; choose a fresh directory.')
    out.mkdir(parents=True)
    public = json.loads((HERE / 'PUBLIC_FILE_MANIFEST.json').read_text())
    for rel, expected in public['files'].items():
        assert fp(HERE / rel) == expected, ('public source pin', rel)
    shutil.copytree(HERE / 'author_packet', out / 'author_input')
    shutil.copytree(HERE / 'internal_review', out / 'internal_review')
    copies = {str(p.relative_to(out)): fp(p) for p in sorted(out.rglob('*')) if p.is_file()}
    author = out / 'author_input'
    commands = [
        [sys.executable, '-B', str(author / 'workday7_fixed_interval_v1/fixed_interval_controls_v1.py'),
         '--output-directory', str(out / 'author_reproduction_v1')],
        [sys.executable, '-B', str(author / 'workday7_fixed_interval_v1/fixed_interval_controls_v2.py'),
         '--output-directory', str(out / 'author_reproduction_v2')],
        [sys.executable, '-B', str(out / 'internal_review/check_quinn_fixed_interval_birth_groups_v1.py'),
         '--packet', str(author), '--output-directory', str(out / 'internal_reproduction')],
    ]
    env = dict(os.environ)
    env.update({k: '1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')})
    plan = {'at': datetime.now(timezone.utc).isoformat(), 'mathematical_source_changes': [],
            'commands': commands, 'input_copy_pins': copies, 'processes_at_once': 1,
            'native_threads': 1, 'child_outer_timeout_seconds': 70,
            'historical_internal_review_is_separate': True, 'full_target_solved': False}
    (out / 'prerun.json').write_text(json.dumps(plan, indent=2) + '\n')
    operations, first_failure = [], None
    for i, argv in enumerate(commands):
        started = perf_counter()
        stdout, stderr = out / f'command{i+1}.stdout', out / f'command{i+1}.stderr'
        try:
            with stdout.open('wb') as so, stderr.open('wb') as se:
                done = subprocess.run(argv, cwd=out, env=env, stdout=so, stderr=se, timeout=70)
            operation = {'command': argv, 'exit_code': done.returncode, 'seconds': perf_counter()-started}
            operations.append(operation)
            assert done.returncode == 0 and stderr.read_bytes() == b'', ('reproduction command', i+1)
            if i < 2:
                version = i + 1
                stem = f'workday7_fixed_interval_v1/controls_v{version}'
                original_report = json.loads((author / stem / 'report_v1.json').read_text())
                generated = out / f'author_reproduction_v{version}'
                generated_report = json.loads((generated / 'report_v1.json').read_text())
                documentary = {'seconds_including_certificate_before_report','peak_rss_kib_linux_before_final_serialization'}
                assert {k:v for k,v in generated_report.items() if k not in documentary} == {
                    k:v for k,v in original_report.items() if k not in documentary}
                assert fp(generated / 'all_records_v1.ndjson') == original_report['certificate']
                # Preserve the historical compact report/stdout. Only the omitted
                # certificate is added to this temporary scientific input mirror.
                target = author / stem / 'all_records_v1.ndjson'
                assert not target.exists()
                shutil.copyfile(generated / 'all_records_v1.ndjson', target)
            else:
                report = json.loads((out / 'internal_reproduction/report_v1.json').read_text())
                original_report = json.loads((HERE / 'internal_review/quinn_fixed_interval_birth_groups_reproduction_v1/report_v1.json').read_text())
                documentary = {'seconds_before_final_report_serialization','peak_rss_kib_linux_before_final_report_serialization'}
                assert {k:v for k,v in report.items() if k not in documentary} == {
                    k:v for k,v in original_report.items() if k not in documentary}
        except (AssertionError, subprocess.TimeoutExpired) as error:
            first_failure = repr(error)
            break
    assert all(fp(out / rel) == expected for rel, expected in copies.items()), 'original copy bytes changed'
    receipt = {'at': datetime.now(timezone.utc).isoformat(), 'status': 'PASS portable original scientific sources' if first_failure is None else 'FAIL preserve first reproduction failure',
               'first_failure': first_failure, 'operations': operations,
               'mathematical_source_changes': [], 'all_original_copies_unchanged': True,
               'new_same_operator_mathematical_executions': len(operations),
               'new_independent_reviews': 0, 'full_target_solved': False}
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))
    if first_failure is not None:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
