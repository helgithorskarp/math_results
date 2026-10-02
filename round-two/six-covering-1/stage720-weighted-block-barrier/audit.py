"""Compile/run the separate full-group, individual-point C++ certificate audit."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise RuntimeError(message)

def encode(c):
    D=c['probability_common_denominator'];rows=[f"720 {D} 2880 377 370 {len(c['terms'])}"]
    for t in c['terms']:
        num,den=t['probability'];rows.append(' '.join(map(str,[t['group'],num*(D//den),len(t['classes'])]+[v for pair in t['classes'] for v in pair])))
    return '\n'.join(rows)+'\n'

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--sanitizers',action='store_true');a=ap.parse_args()
    c=json.loads((HERE/'certificate.json').read_text());need(encode(c)==(HERE/'certificate.txt').read_text(),'JSON/text data differ')
    env=os.environ.copy()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[k]='1'
    flags=['-std=c++17','-Wall','-Wextra','-Wpedantic','-Werror','-O2']
    if a.sanitizers:flags=['-std=c++17','-Wall','-Wextra','-Wpedantic','-Werror','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-fno-pie','-no-pie']
    with tempfile.TemporaryDirectory(prefix='six-covering-1-weighted-') as td:
        binary=Path(td)/'audit';command=['g++',*flags,str(HERE/'audit.cpp'),'-o',str(binary)]
        p=subprocess.run(command,env=env,capture_output=True,text=True,timeout=12);need(p.returncode==0,'C++ compile failed: '+p.stderr)
        p=subprocess.run([str(binary),str(HERE/'certificate.txt')],env=env,capture_output=True,text=True,timeout=10);need(p.returncode==0,'C++ audit failed: '+p.stderr)
        result=json.loads(p.stdout);expected=json.loads((HERE/'expected.json').read_text())
        for k in ('terms','original_class_occurrences','group_average_size','compulsory_points','common_denominator','scaled_point_mass','full_cover_found'):need(result[k]==expected[k],'separate pointwise audit mismatch: '+k)
        damages=[];text=(HERE/'certificate.txt').read_text();lines=text.splitlines()
        changes=[]
        q=lines.copy();row=q[1].split();row[3]=str(int(row[3])+1);q[1]=' '.join(row);changes.append(('original-phase',q))
        q=lines.copy();row=q[1].split();row[1]=str(int(row[1])+1);q[1]=' '.join(row);changes.append(('probability',q))
        q=lines.copy();row=q[1].split();row[5]='0';q[1]=' '.join(row);changes.append(('forbidden-twelve',q))
        q=lines.copy();row=q[0].split();row[3]='378';q[0]=' '.join(row);changes.append(('stronger-ratio',q))
        for name,q in changes:
            path=Path(td)/'damaged.txt';path.write_text('\n'.join(q)+'\n')
            p=subprocess.run([str(binary),str(path)],env=env,capture_output=True,text=True,timeout=10);need(p.returncode!=0,'damaged certificate accepted: '+name);damages.append(name)
        result['semantic_damages_rejected']=damages;result['sanitizers']=a.sanitizers
        print(json.dumps(result))
