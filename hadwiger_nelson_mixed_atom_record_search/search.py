"""Reproduce the finite mixed-atom search. Raw output goes to HN_MIXED_RUN_DIR."""
import os,subprocess,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE=Path(__file__).resolve().parent
WORK=Path(os.environ['HN_MIXED_RUN_DIR']).resolve();WORK.mkdir(parents=True,exist_ok=True)
def run(name,*args):
 with (WORK/(name.replace('.py','')+'_'+('_'.join(args)or 'all')+'.log')).open('w')as log:
  subprocess.run([sys.executable,str(HERE/name),*args],check=True,stdout=log,stderr=subprocess.STDOUT)
if __name__=='__main__':
 run('atoms.py');run('build_sources.py')
 # Two-worker main batch and two fixed-field tasks: at most four solver processes.
 with ThreadPoolExecutor(max_workers=2)as pool:
  fields=[pool.submit(run,'field_contact.py',str(d),kind)for d in(5,13)for kind in('GMM','MMG')]
  run('run_batch.py')
  for result in fields:result.result()
 run('summarize.py');print((WORK/'summarize_all.log').read_text())
