"""Complete source-to-certificate replay. All generated data stay outside Git."""
import argparse,json,subprocess,sys,time
from pathlib import Path
import model as m

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--sanitize',action='store_true');args=ap.parse_args()
    work=args.work.resolve();m.require(not work.is_relative_to(m.HERE.parent),'work must be outside repository');work.mkdir(parents=True,exist_ok=True)
    m.require(not (work/'input.txt').exists(),'use a fresh work directory')
    started=time.time();m.prepare(work,1000000271,838613109,767568613)
    cmd=['g++','-std=c++17','-O3','-Wall','-Wextra']
    if args.sanitize:cmd+=['-fsanitize=undefined','-fno-sanitize-recover=all']
    cmd += [str(m.HERE/'scan.cpp'),'-o',str(work/'scan')];subprocess.run(cmd,check=True)
    with (work/'scan_summary.json').open('w') as f:subprocess.run([str(work/'scan'),str(work/'input.txt'),str(work/'scan')],stdout=f,check=True)
    subprocess.run([sys.executable,'-O',str(m.HERE/'check.py'),str(work)],check=True)
    observed=json.loads((work/'verified.json').read_text());observed.pop('seconds')
    m.require(observed==json.loads((m.HERE/'expected.json').read_text()),'unexpected complete census')
    subprocess.run([sys.executable,'-O',str(m.HERE/'controls.py'),str(work)],check=True)
    print(json.dumps({'PASS':True,'seconds':time.time()-started}))
if __name__=='__main__':main()
