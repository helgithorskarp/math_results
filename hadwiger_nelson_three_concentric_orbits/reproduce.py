"""Regenerate the finite gate and verify its compact positive certificate."""
import argparse,hashlib,json,subprocess,sys,time
from pathlib import Path
from verify import verify

def main():
 p=argparse.ArgumentParser();p.add_argument('--work-dir',type=Path,required=True);a=p.parse_args()
 src=Path(__file__).resolve().parent;work=a.work_dir.resolve()
 if work==src or src in work.parents:raise ValueError('Choose a generated-work directory outside the contribution')
 work.mkdir(parents=True,exist_ok=True);start=time.monotonic()
 with (work/'tables.txt').open('w') as out:
  subprocess.run([sys.executable,str(src/'tables.py')],stdout=out,check=True)
 subprocess.run(['g++','-O3','-std=c++17',str(src/'enumerate.cpp'),'-o',str(work/'enumerate')],check=True)
 with (work/'cases.txt').open('w') as out,(work/'enumeration_progress.txt').open('w') as log:
  subprocess.run([str(work/'enumerate'),str(work/'tables.txt')],stdout=out,stderr=log,check=True)
 result=verify(work/'cases.txt',src/'certificate.json')
 expected=json.loads((src/'expected.json').read_text())
 if result!=expected:raise ValueError({'actual':result,'expected':expected})
 print(json.dumps({'verified':result,'elapsed_seconds':round(time.monotonic()-start,3)},indent=2))

if __name__=='__main__':main()
