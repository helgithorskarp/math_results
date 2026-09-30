#!/usr/bin/env python3
"""Proof-critical binary corruptions and a proper-subrange positive control."""
import argparse
import json
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile


def main():
    parser=argparse.ArgumentParser();parser.add_argument('workdir',type=Path);args=parser.parse_args()
    work=args.workdir.resolve();executable=work/'check-lifts';sources=[work/'full44.bin',work/'local18.bin']
    rejected=[]
    with tempfile.TemporaryDirectory(prefix='dilation-controls-',dir=work) as temporary:
        directory=Path(temporary);fixture=directory/'bad.bin'
        cases=[('bad_full_magic',0,0,b'X'),('bad_local_magic',1,0,b'X'),
               ('wrong_packing_bound',0,12,struct.pack('<H',43)),('wrong_local_radius',1,14,struct.pack('<H',309)),
               ('missing_base_phase',0,14,struct.pack('<H',1)),('wrong_base_case_count',0,18,struct.pack('<I',760760)),
               ('constant_AP',0,24,struct.pack('<H',0)),('AP_outside_base_window',0,24,struct.pack('<H',65535)),
               ('AP_at_pole',0,22,struct.pack('<HH',0,103)),('nonmonochromatic_AP',0,22,struct.pack('<HH',1,103))]
        with sources[0].open('rb') as stream:stream.seek(22);first=stream.read(4)
        cases.append(('duplicated_AP_support',0,26,first))
        for name,index,offset,bytes_ in cases:
            shutil.copyfile(sources[index],fixture)
            with fixture.open('r+b') as stream:stream.seek(offset);stream.write(bytes_)
            inputs=sources[:];inputs[index]=fixture
            r=subprocess.run([str(executable),'--range','0','1',*map(str,inputs)],capture_output=True,text=True,timeout=90)
            if r.returncode==0:raise ValueError('corruption accepted: '+name)
            if not r.stderr.startswith('dilation verification failed:'):raise ValueError('unexpected failure: '+name)
            rejected.append(name)
        for name,delta in [('truncated_base',-1),('trailing_base_bytes',1)]:
            shutil.copyfile(sources[0],fixture)
            with fixture.open('r+b') as stream:stream.truncate(fixture.stat().st_size+delta)
            r=subprocess.run([str(executable),'--range','0','1',str(fixture),str(sources[1])],capture_output=True,text=True,timeout=90)
            if r.returncode==0 or not r.stderr.startswith('dilation verification failed:'):raise ValueError('corruption not properly rejected: '+name)
            rejected.append(name)
    r=subprocess.run([str(executable),'--range','0','1',*map(str,sources)],capture_output=True,text=True,check=True,timeout=90)
    positive=json.loads(r.stdout)
    if positive['full_domain'] or positive['incompatible_keys_per_profile']!=1233 or len(positive['profiles'])!=9:raise ValueError('partial-domain control')
    result={'agent':'six-vdw-3','role':'researcher','status':'ALL_BINARY_CORRUPTIONS_REJECTED','rejected_count':len(rejected),
            'rejected':rejected,'proper_subrange_positive_control':{'full_domain':False,'keys_per_profile':1233,'profiles':9}}
    (work/'controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
