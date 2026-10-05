"""Public-only normal/O/isolated-cold reproduction, exact defects, source binding."""
from source_binding import verify_source as _verify_source
_verify_source()
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

from source_binding import FILES, require
from source_adverse import invoke, barrier

CONTROLS = [(2, [5, 4]), (2, [7, 2]), (3, [4, 3, 2]),
            (3, [4, 3, 3]), (4, [4, 3, 2])]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), 'fresh complete source reproduction directory')
    args.out.mkdir(parents=True)
    base = Path(__file__).resolve().parent
    authority = hashlib.sha256((base / 'SOURCE.json').read_bytes()).hexdigest()
    env = dict(os.environ, SMALL_CUBE_SOURCE_SHA256=authority)
    completed = []

    def run(label, path, arguments, mode):
        barrier()
        _verify_source(base)
        command = invoke(path, arguments, mode)
        started = time.monotonic()
        try:
            child = subprocess.run(command, capture_output=True, text=True,
                                   timeout=60, env=env)
        except subprocess.TimeoutExpired:
            (args.out / 'INCOMPLETE.json').write_text(json.dumps({
                'label': label, 'status': 'TIMEOUT; incomplete, no mathematical absence',
                'completed': len(completed)}, indent=2) + '\n')
            raise
        observation = {'label': label, 'command': command, 'returncode': child.returncode,
                       'seconds': time.monotonic() - started,
                       'stdout': child.stdout, 'stderr': child.stderr}
        completed.append(observation)
        (args.out / 'CHILDREN.json').write_text(json.dumps(completed, indent=2) + '\n')
        require(child.returncode == 0, 'designated source child failed: ' + label)
        print(json.dumps({'label': label, 'complete': True,
                          'seconds': observation['seconds']}), flush=True)

    all_math = []
    observations = []
    adverse_records = []
    source_records = []
    for mode in ('normal', 'optimized', 'cold'):
        lane = (args.out / mode).resolve()
        source = lane / 'source'
        source.mkdir(parents=True)
        for name in FILES + ('SOURCE.json',):
            shutil.copyfile(base / name, source / name)
        whole = []
        for n, counts in CONTROLS:
            name = f'n{n}-' + '-'.join(str(k) for k in counts)
            destination = lane / name
            run(mode + '/' + name, source / 'control.py',
                ['--n', str(n), '--counts', ','.join(str(k) for k in counts),
                 '--out', str(destination)], mode)
            whole.append(json.loads((destination / 'WHOLE-MATH.json').read_text()))
            observations.append(json.loads((destination / 'OBSERVATION.json').read_text()))
        canonical = json.dumps(whole, sort_keys=True, separators=(',', ':')).encode() + b'\n'
        # All five original mathematical calculations finish before this parse/compare.
        require(canonical == (source / 'EXPECTED.json').read_bytes(),
                'ENTIRE paid mathematical record differs: ' + mode)
        (lane / 'WHOLE-MATH.json').write_bytes(canonical)
        all_math.append(canonical)
        run(mode + '/semantic', source / 'adverse.py',
            ['--input', str(lane / 'n2-5-4/UNTRUSTED-GEOMETRY.json'),
             '--out', str(lane / 'SEMANTIC.json')], mode)
        adverse_records.append((lane / 'SEMANTIC.json').read_bytes())
        run(mode + '/source', source / 'source_adverse.py',
            ['--out', str(lane / 'source-defects'), '--mode', mode], mode)
        source_records.append((lane / 'source-defects/WHOLE-REJECTIONS.json').read_bytes())
    require(all(x == all_math[0] for x in all_math), 'whole normal/O/cold mathematics')
    require(all(x == adverse_records[0] for x in adverse_records), 'whole semantic outcomes')
    require(all(x == source_records[0] for x in source_records), 'whole source outcomes')
    for n, counts in CONTROLS:
        name = f'n{n}-' + '-'.join(str(k) for k in counts)
        original = (args.out / 'normal' / name / 'UNTRUSTED-GEOMETRY.json').read_bytes()
        require(all((args.out / mode / name / 'UNTRUSTED-GEOMETRY.json').read_bytes() == original
                    for mode in ('optimized', 'cold')), 'ENTIRE source-only original geometry: ' + name)
    source_children = [json.loads((args.out / mode / 'source-defects/CHILDREN.json').read_text())
                       for mode in ('normal', 'optimized', 'cold')]
    semantic = json.loads(adverse_records[0])
    source_rejections = json.loads(source_records[0])
    require(len(completed) == 21 and semantic['count'] == 17
            and len(source_rejections['source_rejections']) == 5
            and all(len(x) == 5 for x in source_children), 'complete declared source gate census')
    result = {'agent': 'six-downset-1', 'role': 'researcher', 'complete': True,
              'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'outer_success_children': len(completed), 'designated_source_exit1_children': 15,
              'semantic_rejections': 51, 'source_before_arithmetic_rejections': 15,
              'total_exact_rejections': 66,
              'whole_normal_optimized_isolated_cold_equal': True,
              'whole_mathematics': {'bytes': len(all_math[0]),
                 'sha256': hashlib.sha256(all_math[0]).hexdigest()},
              'whole_semantic': {'bytes': len(adverse_records[0]),
                 'sha256': hashlib.sha256(adverse_records[0]).hexdigest()},
              'whole_source': {'bytes': len(source_records[0]),
                 'sha256': hashlib.sha256(source_records[0]).hexdigest()},
              'source_envelope_sha256': authority,
              'max_outer_seconds': max(x['seconds'] for x in completed),
              'max_control_RSS_KiB': max(x['peak_RSS_KiB'] for x in observations),
              'adverse_and_failed_source_RSS_measured': False,
              'all_native_threads': 1, 'parallel_intensive_children': 1,
              'per_child_seconds': 60, 'literal_guard': 'n<=6,h<=10,N<=80 BEFORE arrays',
              'local_generated_bound': '32MiB;512terms',
              'code_credit': 'b7d same-author adapted separate reader, no algorithmic/person independence claim',
              'formalized': False, 'independent_review': False,
              'source_commit': None, 'graph_ref': None,
              'publication_from_reproduction_is_new_discovery': False}
    (args.out / 'GATES.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
