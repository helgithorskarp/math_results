"""Source-pinned reconstruction, serial 128-case batches, fixed 20s children.

The full regenerable CSV stays in the caller's private work directory.
Normal and -O modes compare whole CSV bytes and entire checker records.
"""
import argparse
import csv
import hashlib
import io
import json
import os
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path

FILES={'.gitignore','PROOF.md','README.md','VALIDATION.md','SOURCE_PINS.json',
    'generate.py','check.py','merge.py','expected.json','reproduce.py'}

def need(ok,message):
    if not ok:raise ValueError(message)

def verify_source(source):
    pins=json.loads((source/'SOURCE_PINS.json').read_text())
    need(pins['schema']==1 and pins['algorithm']=='sha256','source pin schema')
    need(set(pins['files'])==FILES-{'SOURCE_PINS.json'},'complete pinned source inventory')
    for name,wanted in pins['files'].items():
        path=source/name
        need(path.is_file() and not path.is_symlink(),'regular pinned file: '+name)
        need(hashlib.sha256(path.read_bytes()).hexdigest()==wanted,'source pin mismatch: '+name)

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--barrier-dir',type=Path,help='optional external directory containing PAUSED.json/HANDOVER.json')
    args=p.parse_args();source=Path(__file__).resolve().parent;verify_source(source)
    need(sys.version_info[:2]>=(3,11),'Python3.11 or later required')
    work=args.work.resolve();need(work!=source and source not in work.parents,'private work must be outside source directory')
    work.mkdir(parents=True,exist_ok=True);need(not any(work.iterdir()),'private work directory must be empty')
    env=dict(os.environ)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','BLIS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[key]='1'
    expected=(source/'expected.json').read_bytes();reference=json.loads(expected)
    record={'status':'INCOMPLETE','python':platform.python_version(),'implementation':platform.python_implementation(),
        'dependencies':'stdlib only','numerical_threads':1,'serial_children':True,'batch_size':128,
        'source_pins_checked_before_every_helper':True,'transport_batch_size':256,'children':[]}
    begun=time.monotonic()
    def save():
        (work/'verification.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    def child(mode,stage,argv):
        if args.barrier_dir:
            need(not any((args.barrier_dir/n).exists() for n in ('PAUSED.json','HANDOVER.json')),
                'external pause/handover barrier; incomplete evidence')
        verify_source(source);begin=time.monotonic()
        command=[sys.executable]+(['-O'] if mode=='optimized' else [])+argv
        try:result=subprocess.run(command,env=env,capture_output=True,text=True,timeout=20)
        except subprocess.TimeoutExpired as e:
            record['failure']='20s child timeout; evidence incomplete';save()
            raise ValueError(record['failure']) from e
        record['children'].append({'mode':mode,'stage':stage,'exit_code':result.returncode,
            'seconds':time.monotonic()-begin,'timeout_seconds':20})
        save();need(result.returncode==0,'helper failed; evidence incomplete: '+result.stdout+result.stderr)
    save()
    try:
        for mode in ('normal','optimized'):
            chunks=[]
            for first in range(0,2176,128):
                last=min(first+128,2176);path=work/(mode+'-batch-'+str(first)+'.csv')
                child(mode,'generate:'+str(first)+'..'+str(last),
                    [str(source/'generate.py'),'--first',str(first),'--last',str(last),'--out',str(path)])
                raw=path.read_bytes();rows=list(csv.reader(io.StringIO(raw.decode('ascii'))))
                need(len(rows)==last-first+1,'complete batch row count')
                need([int(row[0]) for row in rows[1:]]==list(range(first,last)),'complete ordered batch range')
                lines=raw.splitlines(keepends=True);chunks.append(raw if first==0 else b''.join(lines[1:]))
            full=b''.join(chunks);generated=work/(mode+'.csv');generated.write_bytes(full)
            need(len(full)==reference['certificate_bytes'],'full generated CSV byte size')
            need(hashlib.sha256(full).hexdigest()==reference['certificate_sha256'],'full generated CSV hash')
            if mode=='optimized':need(full==(work/'normal.csv').read_bytes(),'entire normal/O CSV bytes differ')
            parts=work/(mode+'-checks');parts.mkdir()
            for stage in ('cover','controls'):
                path=parts/(stage+'.json')
                child(mode,stage,[str(source/'check.py'),'--stage',stage,'--certificate',str(generated),'--out',str(path)])
            for first in range(0,2176,256):
                last=min(first+256,2176);path=parts/('transport-'+str(first)+'.json')
                child(mode,'transport:'+str(first)+'..'+str(last),[str(source/'check.py'),'--stage','transport',
                    '--first',str(first),'--last',str(last),'--certificate',str(generated),'--out',str(path)])
            if mode=='optimized':
                normal=work/'normal-checks'
                for path in sorted(parts.iterdir()):
                    need(path.read_bytes()==(normal/path.name).read_bytes(),'entire normal/O stage record differs: '+path.name)
            checked=work/(mode+'.json')
            child(mode,'merge',[str(source/'merge.py'),'--parts',str(parts),'--out',str(checked)])
            need(checked.read_bytes()==expected,'entire independent checker record differs')
        need((work/'normal.json').read_bytes()==(work/'optimized.json').read_bytes(),'entire normal/O checker records differ')
        record.update(status='FRESH_COMPLETE_BOOLEAN618_SOURCE_RECONSTRUCTION',generators_completed=34,
            checkers_completed=22,mergers_completed=2,entire_normal_optimized_CSV_bytes_identical=True,
            entire_normal_optimized_stage_records_identical=True,
            entire_expected_checker_records_identical=True,certificate_sha256=reference['certificate_sha256'],
            expected_record_sha256=hashlib.sha256(expected).hexdigest(),
            seconds=time.monotonic()-begun,peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        save();print(json.dumps(record,sort_keys=True))
    except Exception as e:
        record.update(status='INCOMPLETE_NO_MATHEMATICAL_EXCLUSION',failure=str(e),seconds=time.monotonic()-begun)
        save();raise

if __name__=='__main__':main()
