"""Source-pinned complete serial regeneration; stdlib, no stored corpus."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import subprocess
import sys
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    out = args.out.resolve()
    need(sys.version_info >= (3, 11), 'CPython3.11+ standard library')
    need(not out.exists() and source not in out.parents and out != source,
         'fresh external output directory; preserve all source/evidence')
    names = {'hypergraph.py', 'check_hypergraph.py', 'cover_enumerate.py',
             'check_cover.py', 'controls.py', 'minimum_masks.py',
             'check_minimum_masks.py', 'mask_controls.py', 'audit_bridges.py',
             'reproduce.py', 'PROOF.md', 'README.md', 'VALIDATION.md',
             'EXPECTED.json', '.gitignore'}
    pins = json.loads((source / 'SOURCE_PINS.json').read_text())
    need(pins['schema'] == 'PHASE72_REPAIR620_SOURCE_PINS_V1'
         and set(pins['files']) == names, 'entire mandatory source/input inventory')

    def freeze():
        for name, pin in pins['files'].items():
            path = source / name
            need(path.stat().st_size == pin['bytes'] and digest(path) == pin['sha256'],
                 'source/input changed: ' + name)

    freeze()  # No research source is imported or run before all pins pass.
    expected = json.loads((source / 'EXPECTED.json').read_text())
    need(expected['schema'] == 'PHASE72_REPAIR620_FULL_EXPECTED_V1', 'exact expected record schema')
    records = expected['records']
    out.mkdir(parents=True)
    for name in names:
        if name.endswith('.py') and name != 'reproduce.py':
            shutil.copyfile(source / name, out / name)
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[name] = '1'
    receipts = []
    obtained = {}
    started = time.monotonic()

    def run(name, key, script, parameters=(), optimized=False):
        freeze()
        for filename in names:
            if filename.endswith('.py') and filename != 'reproduce.py':
                need(digest(out / filename) == pins['files'][filename]['sha256'],
                     'local copied executable changed: ' + filename)
        barrier_dir = env.get('VDW_RESEARCH_BARRIER_DIR')
        if barrier_dir:
            root = Path(barrier_dir)
            need(not any((root / n).exists() for n in
                         ['PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json', 'STOP', 'STOP.json']),
                 'research operations stop barrier; no child launched')
        command = [sys.executable] + (['-O'] if optimized else []) + ['-B', str(out / script)] + list(parameters)
        child_started = time.monotonic()
        child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, env=env, start_new_session=True)
        timed_out = False
        try:
            stdout, stderr = child.communicate(timeout=35)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(child.pid, signal.SIGKILL)
            stdout, stderr = child.communicate()
        (out / (name + '.stdout')).write_text(stdout)
        (out / (name + '.stderr')).write_text(stderr)
        receipt = {'name': name, 'command': command, 'returncode': child.returncode,
                   'timeout': timed_out, 'seconds_guard': 35,
                   'elapsed_seconds': time.monotonic() - child_started,
                   'stdout_sha256': hashlib.sha256(stdout.encode()).hexdigest(),
                   'stderr_sha256': hashlib.sha256(stderr.encode()).hexdigest(),
                   'child_peak_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
        receipts.append(receipt)
        (out / 'receipts.json').write_text(json.dumps(receipts, indent=2, sort_keys=True) + '\n')
        need(not timed_out and child.returncode == 0, 'incomplete child: ' + name)
        result = json.loads(stdout)
        need(result == records[key], 'ENTIRE regenerated semantic record differs: ' + name)
        if key in obtained:
            need(obtained[key] == result, 'ENTIRE normal/optimized results differ: ' + key)
        obtained[key] = result
        print(json.dumps({'stage': name, 'status': 'COMPLETE_WHOLE_RECORD_MATCH',
                          'elapsed_seconds': receipt['elapsed_seconds']}, sort_keys=True), flush=True)

    graph = str(out / 'hypergraph72.json')
    run('hypergraph-producer', 'hypergraph_producer', 'hypergraph.py', ['--mask', '72', '--out', graph])
    for optimized, mode in [(False, 'normal'), (True, 'optimized')]:
        run('hypergraph-' + mode, 'hypergraph_audit', 'check_hypergraph.py', [graph, '--mask', '72'], optimized)
        run('tiny-' + mode, 'tiny_controls', 'controls.py', [graph, '--part', 'tiny'], optimized)
        run('physical-damages-' + mode, 'hypergraph_controls', 'controls.py', [graph, '--part', 'physical'], optimized)
    for size in range(5, 10):
        proposal = str(out / ('cover' + str(size) + '.json'))
        run('cover-producer-' + str(size), 'cover_producer_' + str(size), 'cover_enumerate.py',
            [graph, '--size', str(size), '--out', proposal])
        for optimized, mode in [(False, 'normal'), (True, 'optimized')]:
            run('cover-' + str(size) + '-' + mode, 'cover_audit_' + str(size),
                'check_cover.py', [graph, proposal], optimized)
    run('minimum-mask-producer', 'mask_producer', 'minimum_masks.py')
    for optimized, mode in [(False, 'normal'), (True, 'optimized')]:
        run('minimum-masks-' + mode, 'mask_audit', 'check_minimum_masks.py',
            [str(out / 'minimum-mask-proposal.json')], optimized)
        run('mask-damages-' + mode, 'mask_controls', 'mask_controls.py', optimized=optimized)
        run('bridges-' + mode, 'bridges', 'audit_bridges.py', optimized=optimized)
    freeze()
    need(set(obtained) == set(records) and len(receipts) == 29, 'entire expected record/stage inventory')
    result = {'author': 'six-vdw-1', 'role': 'researcher',
              'status': 'FRESH_COMPLETE_PHASE72_REPAIR620_RECONSTRUCTION',
              'full_semantic_records': obtained, 'completed_stages': len(receipts),
              'source_pin_manifest_sha256': digest(source / 'SOURCE_PINS.json'),
              'expected_sha256': digest(source / 'EXPECTED.json'),
              'elapsed_seconds': time.monotonic() - started,
              'child_peak_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (out / 'RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'full_semantic_records'}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
