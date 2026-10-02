"""Compile and run a distinct raw-original C++ audit with literal controls."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parent
EXPECTED={'status':'RAW_ORIGINAL_CORE_AND_PAIR_AUDIT_PASSED','raw_core_visited':13131888,'raw_core_accepted':2560,
          'canonical_cores':14,'pair_tuples':4729438,'map_points':2073600,'transport_controls':103680,
          'core_progression_points':12136320,'all14_strict_exclusions':True}

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--sanitizers',action='store_true');a=ap.parse_args()
    cert=json.loads((ROOT/'certificate.json').read_text());lines=['14']
    for row in cert['cores']:
        values=row['original_phases']+[row['Fgain'],row['Sgain'],row['raw_count']]+[p['capacity'] for p in row['pairs']]+[p['accepted_raw'] for p in row['pairs']]
        lines.append(' '.join(map(str,values)))
    text='\n'.join(lines)+'\n'
    need(text==(ROOT/'certificate.txt').read_text(),'two exact certificate encodings differ')
    env=os.environ.copy()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[k]='1'
    if a.sanitizers:
        env['ASAN_OPTIONS']='detect_leaks=0:halt_on_error=1'
        env['UBSAN_OPTIONS']='halt_on_error=1'
    with tempfile.TemporaryDirectory(prefix='covering-core-audit-') as directory:
        binary=Path(directory)/'audit'
        flags=['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-fno-pie','-no-pie'] if a.sanitizers else ['-O2']
        subprocess.run(['g++','-std=c++17','-Wall','-Wextra','-Werror',*flags,str(ROOT/'audit.cpp'),'-o',str(binary)],
                       check=True,env=env,capture_output=True,text=True,timeout=12)
        process=subprocess.run([str(binary),str(ROOT/'certificate.txt')],env=env,capture_output=True,text=True,timeout=10)
        need(process.returncode==0 and not process.stderr,'C++ replay failed: '+process.stderr)
        need(json.loads(process.stdout)==EXPECTED,'C++ exact output differs')
        damaged=0
        if not a.sanitizers:
            rows=[line.split() for line in lines]
            fixtures=[]
            bad=[r[:] for r in rows];bad[1][1]='12';fixtures.append('\n'.join(' '.join(r) for r in bad)+'\n')
            bad=[r[:] for r in rows];bad[1][8]=str(int(bad[1][8])+1);fixtures.append('\n'.join(' '.join(r) for r in bad)+'\n')
            bad=[r[:] for r in rows];bad[1][9]=str(int(bad[1][9])+1);fixtures.append('\n'.join(' '.join(r) for r in bad)+'\n')
            fixtures.append(text+'999\n')
            for i,fixture in enumerate(fixtures):
                path=Path(directory)/('damaged-'+str(i)+'.txt');path.write_text(fixture)
                result=subprocess.run([str(binary),str(path)],env=env,capture_output=True,text=True,timeout=10)
                need(result.returncode==1 and result.stderr.strip(),'damaged literal certificate accepted or failed unexpectedly')
                damaged+=1
        print(json.dumps({**EXPECTED,'semantic_damages_rejected':damaged,'sanitizers':a.sanitizers}))

if __name__=='__main__':main()
