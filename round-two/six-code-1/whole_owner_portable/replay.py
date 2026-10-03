"""Cold serial replay; only compact source and literal fixtures are inputs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def put(path, value):
    Path(path).write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def sources():
    manifest = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_bytes())
    for pin in manifest['source_files']:
        name = pin['name']
        need(not Path(name).is_absolute() and '..' not in Path(name).parts, 'literal relative source')
        raw = (ROOT / name).read_bytes()
        need(len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'],
             'entire frozen source: ' + name)


def campaign_barrier(state):
    if state is None:
        return None
    health = json.loads((state / 'monitor/health.json').read_bytes())
    hand = json.loads((state / 'monitor/HANDOVER.json').read_bytes())
    need(health['campaign_state'] == 'running' and hand['phase'] == 'completed' and
         health.get('credit_budget', {}).get('status') in (None, 'authorized') and
         not any((state / p).exists() for p in ['PAUSED', 'PAUSED.json', 'monitor/PAUSED', 'monitor/PAUSED.json']),
         'campaign pause/handover/budget barrier')
    return health['checked_at']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--mode', choices=['normal', 'optimized', 'both'], default='both')
    ap.add_argument('--campaign-state', type=Path)
    args = ap.parse_args()
    sources()
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=False)
    domain = json.loads((ROOT / 'DOMAIN.json').read_bytes())
    modes = ['normal', 'optimized'] if args.mode == 'both' else [args.mode]
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS',
                 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    progress = {'actual_agent': 'six-code-1', 'role': 'researcher', 'complete': False,
                'status': 'INCOMPLETE_NOT_ABSENCE', 'completed_children': [], 'modes': modes,
                'original_guards': domain['original_guards']}
    put(args.out / 'progress.json', progress)

    def child(mode, name, script, arguments):
        sources()
        health = campaign_barrier(args.campaign_state)
        work = args.out / mode
        target = work / name
        cmd = [sys.executable] + (['-O'] if mode == 'optimized' else []) + [str(ROOT / script)]
        cmd += [str(a) for a in arguments] + ['--out', str(target)]
        progress['active_child'] = {'mode': mode, 'name': name, 'command': cmd}
        put(args.out / 'progress.json', progress)
        t0 = time.monotonic()
        timing = {'actual_agent': 'six-code-1', 'role': 'researcher', 'mode': mode, 'name': name,
                  'command': cmd, 'started_at': datetime.now(timezone.utc).isoformat(),
                  'original_guards': domain['original_guards'], 'health_checked_at': health,
                  'complete': False}
        try:
            with (work / (name + '-stdout.txt')).open('w') as stdout, (work / (name + '-stderr.txt')).open('w') as stderr:
                result = subprocess.run(cmd, env=env, stdout=stdout, stderr=stderr, timeout=65)
            timing.update(exit_code=result.returncode, elapsed_seconds=time.monotonic() - t0)
            p = json.loads((target / 'progress.json').read_bytes())
            need(result.returncode == 0 and p['complete'], 'incomplete child is not absence: ' + name)
            timing.update(complete=True, mathematical_sha256=p['mathematical_sha256'])
        except BaseException as exc:
            timing.update(error_type=type(exc).__name__, error=str(exc), elapsed_seconds=time.monotonic() - t0)
            put(work / (name + '-timing.json'), timing)
            raise
        else:
            put(work / (name + '-timing.json'), timing)
        progress['completed_children'].append({'mode': mode, 'name': name,
                                               'mathematical_sha256': p['mathematical_sha256']})
        progress.pop('active_child', None)
        put(args.out / 'progress.json', progress)
        print(json.dumps({'mode': mode, 'child': name, 'complete': True,
                          'seconds': timing['elapsed_seconds']}), flush=True)

    try:
        for mode in modes:
            work = args.out / mode
            work.mkdir()
            dirs = []
            for fi in domain['fixture_indices']:
                name = 'fixture-%02d' % fi
                child(mode, name, 'inventory/inventory.py', ['fixture', '--index', fi])
                dirs.append(str(work / name))
            put(work / 'fixtures.json', dirs)
            child(mode, 'aggregate', 'inventory/inventory.py', ['aggregate', '--fixtures', work / 'fixtures.json'])
            child(mode, 'derived', 'derive.py', ['generate', '--work', work])
            for t in domain['base_type_ids']:
                input_path = work / 'derived' / ('input-%d.json' % t)
                data = json.loads(input_path.read_bytes())
                child(mode, 'prepare-%d' % t, 'literal/run.py', ['prepare', '--input', input_path])
                cases = []
                n = data['representative_whole_case_count']
                slab = domain['case_slab_size']
                for j, first in enumerate(range(0, n, slab)):
                    index_path = work / ('indices-%d-%02d.json' % (t, j))
                    put(index_path, list(range(first, min(first + slab, n))))
                    name = 'cases-%d-%02d' % (t, j)
                    child(mode, name, 'literal/run.py', ['cases', '--input', input_path, '--indices', index_path])
                    cases.append(str(work / name))
                put(work / ('case-dirs-%d.json' % t), cases)
                child(mode, 'assemble-%d' % t, 'derive.py', ['assemble', '--type', t, '--work', work])
                child(mode, 'interfaces-%d' % t, 'literal/interfaces.py', ['--input', input_path,
                      '--spec', work / ('assemble-%d' % t) / 'interface-spec.json'])
                child(mode, 'gate-spec-%d' % t, 'derive.py', ['gate_spec', '--type', t, '--work', work])
                child(mode, 'gate-%d' % t, 'literal/inventory_gate.py', ['--spec', work / ('gate-spec-%d' % t) / 'gate-spec.json'])
            child(mode, 'transport-spec', 'derive.py', ['transport_spec', '--work', work])
            child(mode, 'transport', 'literal/hub_transport.py', ['--spec', work / 'transport-spec/transport-spec.json'])
        sources()
        progress.update(complete=True, status='COMPLETE_COLD_DECLARED_MODES')
        put(args.out / 'progress.json', progress)
        print(json.dumps({'complete': True, 'completed_children': len(progress['completed_children']), 'modes': modes}), flush=True)
    except BaseException as exc:
        progress.update(error_type=type(exc).__name__, error=str(exc))
        put(args.out / 'progress.json', progress)
        raise


if __name__ == '__main__':
    main()
