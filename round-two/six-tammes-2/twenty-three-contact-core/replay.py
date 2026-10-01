"""Replay all pinned prior mathematics used in the endpoint consequence.

Run check.py separately for the new 23-contact curve. This command verifies
the immediate source pins and the complete prior two-point-completion chain.
"""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def require(ok,message):
 if not ok:raise ValueError(message)
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--prerequisite-root',type=Path,default=ROOT)
 args=parser.parse_args()
 inputs=json.loads((HERE/'INPUTS.json').read_text())
 count=0
 for which in ('core','completion'):
  item=inputs[which];base=args.prerequisite_root if which=='core' else ROOT
  for name,want in item['files_sha256'].items():
   path=base/item['directory']/name
   require(hashlib.sha256(path.read_bytes()).hexdigest()==want,'pinned endpoint prerequisite '+str(path))
   count+=1
 environment=os.environ.copy()
 for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):environment[key]='1'
 cmd=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
 cmd += [str(ROOT/inputs['completion']['directory']/'replay.py'),
         '--prerequisite-root',str(args.prerequisite_root)]
 child=subprocess.run(cmd,check=True,capture_output=True,text=True,env=environment,timeout=60)
 result=json.loads(child.stdout)
 require(result['status']=='VERIFIED' and result['core_cap_verified']
         and result['full_completion_and_local_chain_replayed']
         and result['reference_vectors_identified'],'complete prior completion replay')
 print(json.dumps({'status':'ENDPOINT_DEPENDENCIES_REPLAYED','immediate_pinned_files':count,
                   'parent_result':result},sort_keys=True))
