"""Reproduce14 serial search-free jobs with normal/optimized agreement."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).absolute().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    expected = json.loads((HERE/'expected.json').read_text())
    env = dict(os.environ)
    for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    started = time.monotonic()
    results = []
    evidence = {}
    for optimized in (False, True):
        for engine, part in [*[(e, p) for e in ('uv', 'axial') for p in ('core', 'array', 'controls')], ('joint', 'audit')]:
            command = [sys.executable]+(['-O'] if optimized else [])+[str(HERE/'run.py'), '--engine', engine, '--part', part]
            run = subprocess.run(command, cwd=HERE, env=env, text=True, capture_output=True, timeout=47)
            require(run.returncode == 0, 'Proof job failed: '+run.stdout+'\n'+run.stderr)
            result = json.loads(run.stdout)
            require(result['complete'], 'Incomplete proof job')
            key = engine+'-'+part
            require(result['mathematics_sha256'] == expected['mathematics_sha256'][key], 'Wrong exact proof-job hash: '+key)
            mode = 'optimized' if optimized else 'normal'
            saved = json.loads((HERE/'generated'/f'{engine}-{part}-{mode}.json').read_text())
            if key in evidence:
                require(saved['evidence'] == evidence[key], 'Normal/optimized mathematical evidence differs')
            else:
                evidence[key] = saved['evidence']
            results.append(result)
    uv = evidence['uv-core']['contact_inventory']
    axial = evidence['axial-core']['contact_inventory']
    require(uv['types'] == axial['types'] and uv['touching_pairs'] == axial['touching_pairs'],
            'UV/axial E1 contact inventories disagree')
    require(len(uv['types']) == 11 and len(uv['touching_pairs']) == 19, 'Wrong E2 contact counts')
    for key in ('uv-controls', 'axial-controls'):
        require(evidence[key]['count'] == 7, 'A damaged-witness control is missing')
    out = {'agent': 'six-heesch-2', 'role': 'researcher', 'complete': True,
           'serial_jobs': len(results), 'normal_optimized_agree': True,
           'E2_surround_copies': 8, 'E1_contact_types': 11, 'touching_pairs': 19,
           'damaged_controls_per_engine': 7, 'all_k_minimum': 6,
           'Heesch_number_conclusion': False, 'mathematics_sha256': expected['mathematics_sha256'],
           'seconds': round(time.monotonic()-started, 3),
           'max_child_rss_kib': max(x['max_rss_kib'] for x in results),
           'verification_sha256': hashlib.sha256(json.dumps(evidence, sort_keys=True, separators=(',', ':')).encode()).hexdigest()}
    (HERE/'generated/verification.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
