#!/usr/bin/env python3
"""Recompute the complete theorem and compare deterministic compact evidence."""
import json,sys,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE=Path(__file__).resolve().parent

def run(name):
 p=subprocess.run([sys.executable,str(HERE/name)],cwd=HERE,text=True,capture_output=True)
 if p.returncode:
  sys.stderr.write(p.stderr);raise RuntimeError(name+' failed')
 return json.loads(p.stdout)

def main():
 if not __debug__:raise RuntimeError('Run without -O; assertions enforce proof obligations.')
 jobs=[('certificates','verify_certificates.py'),('coverage','verify_coverage.py'),('controls','audit.py')]
 with ThreadPoolExecutor(max_workers=2) as pool:
  fs=[(key,pool.submit(run,name)) for key,name in jobs]
  result={key:f.result() for key,f in fs}
 expected=json.loads((HERE/'expected.json').read_text())
 assert result==expected,'Output differs from expected.json'
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
