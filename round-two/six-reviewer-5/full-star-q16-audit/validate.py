"""Serial full independent replays and input/semantic rejection controls."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time


def require(p, label):
    if not p:
        raise ValueError(label)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    root = Path(__file__).resolve().parent
    expected = (root/'RECORD.json').read_bytes()
    env = dict(os.environ)
    for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        env[name] = '1'
    receipt = {'guard_seconds': 45, 'native_threads': 1, 'serial_children': 1,
               'interpreter': sys.version, 'positive_children': [], 'controls': []}
    cert = json.loads((root/'CERTIFICATE.json').read_text())
    def run(mode, extra, dest):
        cmd = [sys.executable, '-I', '-B']+(['-O'] if mode == 'optimized' else [])
        cmd += [str(root/'check.py'), '--out', str(dest)]+extra
        t = time.monotonic()
        child = subprocess.run(cmd, env=env, capture_output=True, timeout=45)
        return child, {'mode': mode, 'seconds': time.monotonic()-t,
                       'exit_code': child.returncode,
                       'peak_child_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    with tempfile.TemporaryDirectory(prefix='capped-h-audit-') as tmp:
        tmp = Path(tmp)
        for mode in ('normal', 'optimized', 'cold'):
            dest = tmp/(mode+'.json')
            child, row = run(mode, [], dest)
            require(child.returncode == 0, child.stderr.decode())
            require(dest.read_bytes() == expected, 'entire independent mathematical record differs')
            row['record_bytes'] = len(expected)
            row['record_sha256'] = hashlib.sha256(expected).hexdigest()
            receipt['positive_children'].append(row)
        controls = [('semantic-'+name, ['--damage', name], None)
                    for name in ('anchor', 'intersection', 'empty-loop', 'omit-basis', 'cross-sector')]
        def mutated(name, fn):
            c = copy.deepcopy(cert)
            fn(c)
            f = tmp/(name+'.json')
            f.write_text(json.dumps(c))
            controls.append((name, ['--certificate', str(f)], f))
        mutated('wrong-domain', lambda c: c.__setitem__('k', 7))
        mutated('wrong-entry-scale', lambda c: c.__setitem__('free_original_entry_denominator', 512))
        mutated('missing-orbit', lambda c: c['free_original_entry_orbit_keys'].pop())
        mutated('negative-free-entry', lambda c: c['free_original_entry_numerators'].__setitem__(0, -10**9))
        for sector in ('TT_lower', 'TT_upper', 'Z_lower', 'Z_upper', 'W_lower', 'W_upper'):
            mutated('factor-'+sector, lambda c, s=sector:
                    c['positive_sector_certificates'][s]['factor_lower_triangle_numerators'][0].__setitem__(0, 10**16))
        for sector in ('ZZ_lower', 'ZZ_upper', 'WW_lower', 'WW_upper', 'ZW_lower', 'ZW_upper'):
            mutated('scalar-'+sector, lambda c, s=sector:
                    c['positive_sector_certificates'][s].__setitem__('scalar_gram_numerator', 0))
        for mode in ('normal', 'optimized'):
            for name, extra, unused in controls:
                child, row = run(mode, extra, tmp/'damaged-output.json')
                require(child.returncode != 0 and b'ValueError' in child.stderr,
                        'damaged certificate or semantic identity did not reject: '+name)
                row['name'] = name
                row['rejected'] = True
                row['failure'] = child.stderr.decode().strip().splitlines()[-1]
                receipt['controls'].append(row)
    a.out.write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'positive': len(receipt['positive_children']),
                      'rejections': len(receipt['controls']),
                      'record_sha256': hashlib.sha256(expected).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
