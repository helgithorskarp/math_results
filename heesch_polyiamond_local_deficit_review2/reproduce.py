"""Bounded sequential reproduction for six-reviewer-2's T214 audit.

Generated formulas, traces and run reports stay in --work outside source.
Use --stage native once, then --stage audit. The latter uses stdlib only.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent


def invariant_result(value):
    """Native proof bytes/step counts are provenance, not mathematical invariants."""
    if isinstance(value, list):
        return [invariant_result(x) for x in value]
    if isinstance(value, dict):
        result = {k: invariant_result(v) for k, v in value.items() if k != 'trace_sha256'}
        if 'rup' in result:
            result['rup'] = {k: v for k, v in result['rup'].items()
                             if k not in ('additions', 'deletions', 'explicit_empty_clause')}
        return result
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=BASE.parent)
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--stage', choices=('native', 'audit', 'all'), default='all')
    ap.add_argument('--checker', type=Path)
    ap.add_argument('--optimized', action='store_true')
    a = ap.parse_args()
    root = a.root.resolve(); work = a.work.resolve()
    if work.is_relative_to(BASE):
        raise ValueError('generated files must stay outside this source directory')
    work.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    plan = []
    if a.stage in ('native', 'all'):
        if not a.checker or not a.checker.is_file() or a.optimized:
            raise ValueError('native replay needs DRAT-trim and assertions enabled')
        script = root/'heesch_polyiamond_local_deficit/verify.py'
        for phase, extra in [('lower', []), ('oracle', []),
                             ('pairs', ['--start', '0', '--stop', '12']),
                             ('pairs', ['--start', '12', '--stop', '24']),
                             ('pairs', ['--start', '24', '--stop', '38']), ('deficit', [])]:
            plan.append(('native-'+phase+'-'+'-'.join(extra),
                         [sys.executable, '-B', str(script), '--phase', phase,
                          '--work', str(work), '--checker', str(a.checker.resolve())]+extra))
        export = ('import sys,json; from pathlib import Path; '
                  'sys.path.insert(0,sys.argv[1]); import geometry as g; '
                  's,_=g.inputs(); _,_,_,raw,wide=g.catalogues(s); '
                  'flat=lambda p:p["matrix"]+p["translation"]; '
                  'Path(sys.argv[2]).write_text(json.dumps({"raw":[flat(p) for p in raw],'
                  '"wide":[flat(p) for p in wide]}))')
        plan.append(('native-inventory', [sys.executable, '-B', '-c', export,
                     str(root/'heesch_polyiamond_local_deficit'), str(work/'native-inventory.json')]))
    if a.stage in ('audit', 'all'):
        for phase, extra in [('geometry', []), ('selectors', []),
                             ('pairs', ['--start', '0', '--stop', '12']),
                             ('pairs', ['--start', '12', '--stop', '24']),
                             ('pairs', ['--start', '24', '--stop', '38']), ('deep', [])]:
            label = phase+'-'+'-'.join(extra).replace('--', '')
            output = work/(label+'.audit.json')
            options = ['-B']+(['-O'] if a.optimized else [])
            plan.append((label, [sys.executable]+options+[str(BASE/'audit.py'),
                         '--root', str(root), '--work', str(work), '--phase', phase,
                         '--output', str(output)]+extra))
    records = []
    for label, command in plan:
        started = time.monotonic()
        try:
            p = subprocess.run(command, env=env, capture_output=True, text=True, timeout=55)
        except subprocess.TimeoutExpired:
            raise RuntimeError('incomplete bounded phase: '+label+'; no mathematical conclusion')
        (work/(label+'.reproduction.log')).write_text(p.stdout+p.stderr)
        if p.returncode:
            raise RuntimeError(label+' failed: '+p.stdout[-1500:]+p.stderr[-3000:])
        records.append({'label': label, 'seconds': time.monotonic()-started})
        print('PASS', label, round(records[-1]['seconds'], 3), 'seconds', flush=True)
    if a.stage in ('audit', 'all'):
        combined = {}
        for phase, extras in [('geometry', ''), ('selectors', ''),
                              ('pairs', 'start-0-stop-12'), ('pairs', 'start-12-stop-24'),
                              ('pairs', 'start-24-stop-38'), ('deep', '')]:
            data = json.loads((work/(phase+'-'+extras+'.audit.json')).read_text())
            combined[phase+('-'+extras if extras else '')] = data
        encoded = json.dumps(combined, indent=2, sort_keys=True)+'\n'
        expected = json.loads((BASE/'expected.json').read_text())
        if invariant_result(combined) != invariant_result(expected):
            raise ValueError('compact expected output mismatch')
        (work/'independent-results.json').write_text(encoded)
        print('PASS: all 53 RUP traces, 48 geometric CNFs, geometry, exact selectors and credited upper385.',
              'SHA256', hashlib.sha256(encoded.encode()).hexdigest(), flush=True)
    (work/('reproduction-'+a.stage+('-optimized' if a.optimized else '')+'.json')).write_text(
        json.dumps(records, indent=2)+'\n')


if __name__ == '__main__':
    main()
