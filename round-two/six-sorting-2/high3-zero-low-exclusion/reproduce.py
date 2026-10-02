"""Portable full serial reproduction with exact whole-record comparison."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

SOURCE = Path(__file__).resolve().parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def run_child(args, env, output):
    with output.open('w') as stream:
        try:
            done = subprocess.run(args, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=55)
        except subprocess.TimeoutExpired:
            raise SystemExit('OPERATIONAL_TIMEOUT: incomplete replay, not exclusion; inspect ' + str(output))
    need(done.returncode == 0, 'child failed; incomplete replay: ' + str(output))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=SOURCE / 'generated')
    args = parser.parse_args()
    started = time.monotonic()
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((SOURCE / 'source-manifest.json').read_text())
    for name, expected in manifest['owned_sha256'].items():
        need(hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() == expected, 'owned whole-byte source pin differs: ' + name)
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    python = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
    regenerated = args.output / 'regenerated-certificate.json'
    run_child(python + [str(SOURCE / 'generate.py'), '--output', str(regenerated)], env, args.output / 'generate.log')
    raw = (SOURCE / 'certificate.json').read_bytes()
    need(regenerated.read_bytes() == raw, 'entire regenerated certificate differs')
    certificate = json.loads(raw)
    whole_ids = []
    binding_hashes = []
    kinds = Counter()
    assignments = Counter()
    telemetry = []
    units = 0
    for offset in range(0, 181, 40):
        count = min(40, 181 - offset)
        output = args.output / ('verify-' + str(offset) + '-' + str(offset + count) + '.json')
        run_child(python + [str(SOURCE / 'verify.py'), '--certificate', str(regenerated), '--offset', str(offset), '--functions', str(count), '--output', str(output)], env, output.with_suffix('.log'))
        data = json.loads(output.read_text())
        result = data['mathematical_result']
        expected = certificate['state_heads'][offset:offset + count]
        ids = [s for s, heads in expected]
        bindings = [[s, h, -1 if type(refs) is int else t, refs if type(refs) is int else ref]
                    for s, heads in expected for h, refs in enumerate(heads)
                    for t, ref in ([(None, refs)] if type(refs) is int else enumerate(refs))]
        need(result['completed_function_ids'] == ids and result['checked_bindings_sha256'] == digest(bindings), 'complete entry-level batch coverage differs')
        need(result['checked_units'] == len(bindings), 'batch unit count differs')
        whole_ids.extend(ids)
        binding_hashes.append(digest(bindings))
        kinds.update(result['kind_counts'])
        assignments.update(result['original_cube_assignments'])
        units += result['checked_units']
        telemetry.append({k: data[k] for k in ('seconds', 'maximum_rss_kib')})
        print('COMPLETE_FUNCTION_RANGE', offset, offset + count, flush=True)
    need(whole_ids == [s for s, h in certificate['state_heads']] and len(whole_ids) == 181 and units == 5295, 'whole domain incomplete')
    control_path = args.output / 'controls.json'
    run_child(python + [str(SOURCE / 'controls.py')], env, control_path)
    controls = json.loads(control_path.read_text())['mathematical_result']
    math = {'all_function_ids': whole_ids, 'negative_units': units, 'kind_counts': dict(kinds),
            'cube_assignments': dict(assignments), 'batch_binding_hashes': binding_hashes, 'controls': controls}
    expected = json.loads((SOURCE / 'checks.json').read_text())
    need(digest(math) == expected['mathematical_result_sha256'], 'entire expected mathematical record differs')
    result = {'agent': 'six-sorting-2', 'role': 'researcher',
              'status': 'COMPLETE_ZERO_PRIOR_LOW_HEAD_TAIL_EXCLUSION_CERTIFICATES_VERIFIED',
              'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'mathematical_result': math,
              'mathematical_result_sha256': digest(math), 'telemetry': telemetry,
              'seconds': time.monotonic() - started, 'python': sys.version.split()[0], 'optimized': bool(sys.flags.optimize)}
    (args.output / 'full-check.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('mathematical_result', 'telemetry')}), flush=True)


if __name__ == '__main__':
    main()
