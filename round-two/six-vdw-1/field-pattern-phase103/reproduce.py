"""Portable source-only serial replay with whole byte/record comparisons."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    here = Path(__file__).resolve().parent
    manifest = json.loads((here/'SOURCE_MANIFEST.json').read_bytes())
    actual = sorted(p.name for p in here.iterdir() if p.is_file() and p.name != 'SOURCE_MANIFEST.json')
    need(actual == sorted(manifest['files']), 'entire portable source file census')
    for name,pin in manifest['files'].items():
        raw = (here/name).read_bytes()
        need(len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'],
             'entire source/evidence bytes differ: '+name)
    expected = json.loads((here/'EXPECTED.json').read_bytes())
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
                 'VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    def child(command):
        proc = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                env=env,start_new_session=True)
        try:
            out,err = proc.communicate(timeout=20)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGKILL)
            proc.communicate()
            raise RuntimeError('source replay child timed out; no mathematical exclusion inferred')
        need(proc.returncode == 0 and err == b'', 'source replay child failed')
        return out,json.loads(out)
    modes = ['base','affine','packs','phases','controls']
    complete = {}
    with tempfile.TemporaryDirectory(prefix='field-pattern103-') as temp:
        for optimized in [False,True]:
            prefix = [sys.executable]+(['-O'] if optimized else [])
            file = Path(temp)/('optimized.csv' if optimized else 'normal.csv')
            _,proposal = child(prefix+[str(here/'produce.py'),str(file)])
            need(file.read_bytes() == (here/'five-packs.csv').read_bytes(), 'entire regenerated certificate bytes')
            need(proposal == expected['producer'], 'entire producer record')
            records = {}
            for mode in modes:
                command = prefix+[str(here/'controls.py')] if mode == 'controls' else (
                    prefix+[str(here/'check.py'),mode,str(file),str(here/'four-APs.json')])
                out,record = child(command)
                need(record == expected[mode], 'entire checker/control record: '+mode)
                if mode in complete:
                    need(out == complete[mode], 'entire normal/O checker/control stdout: '+mode)
                else:
                    complete[mode] = out
                records[mode] = record
            need(records == {mode:expected[mode] for mode in modes}, 'entire declared stage completion')
    return {'author':'six-vdw-1','role':'researcher','status':'SOURCE_ONLY_ENTIRE_NORMAL_O_BYTES_AND_RECORDS_VERIFIED',
            'source_files_checked':len(manifest['files'])+1,'modes':modes,'serial_children':12,
            'threads':1,'per_child_seconds_guard':20,
            'certificate_bytes':3735,'certificate_sha256':expected['base']['pack_sha256'],
            'repair_column_lower_bound':5,'phase6_point_edit_lower_bound':30,
            'source_only':True,'native_solver_used':False,'external_review_claimed':False,
            'numerical_W_improvement':False}


if __name__ == '__main__':
    print(json.dumps(main(),sort_keys=True))
