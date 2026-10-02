"""Portable primary replay: one serial bounded exact child at a time.

Compares the WHOLE compact mathematical record, not selected digests.
Does not access target source or a graph/ledger/network.
"""
import os,sys,json,argparse,pathlib,subprocess,time,hashlib
ROOT=pathlib.Path(__file__).resolve().parent
FIXTURES=[(3,2),(4,2),(4,3),(5,4),(6,2),(6,5)]
def run():
 env=dict(os.environ)
 for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
 def child(file,*args):
  start=time.monotonic();command=[sys.executable,'-B']+(['-O']if sys.flags.optimize else [])+[str(ROOT/file),*map(str,args)]
  p=subprocess.run(command,capture_output=True,timeout=55,env=env)
  if p.returncode:sys.stderr.buffer.write(p.stderr);raise RuntimeError('bounded exact phase failed '+repr(command))
  print(file+' '+repr(args)+' '+format(time.monotonic()-start,'.3f')+'s',file=sys.stderr,flush=True)
  return json.loads(p.stdout)
 signs=[child('signs.py',name)for name in ['anti','standard','arrow','final']]
 shared=signs[0]
 for x in signs:
  if x['all_scalar_norms']!=shared['all_scalar_norms']or x['every_registered_positive_denominator']!=shared['every_registered_positive_denominator']:raise ValueError('complete shared norm/denominator records differ')
 records=[child('original.py',n,l,phase)for n,l in FIXTURES for phase in ['physical','seed','old','new']]
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','proof_status':'exact all-quadrant certificates plus ordinary unformalized complete original Gram/frame/lift/rank reductions','new_target_code_exposure':'NONE through primary seal; signed written proof/formulas/counts visible, own prior helper/method credited, not blind','all_scalar_norms':shared['all_scalar_norms'],'every_registered_positive_denominator':shared['every_registered_positive_denominator'],'all_uniform_tests':[{k:v for k,v in x.items()if k not in ['all_scalar_norms','every_registered_positive_denominator']}for x in signs],'all_original_controls':records,'repair_controls':child('repair.py'),'semantic_controls':child('controls.py')}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',type=pathlib.Path);p.add_argument('--write',type=pathlib.Path);a=p.parse_args();record=run();data=json.dumps(record,sort_keys=True,separators=(',',':')).encode()+b'\n'
 if a.check and a.check.read_bytes()!=data:raise ValueError('WHOLE expected mathematical record differs')
 if a.write:a.write.write_bytes(data)
 print(json.dumps({'whole_record_sha256':hashlib.sha256(data).hexdigest(),'whole_record_bytes':len(data),'whole_expected_match':bool(a.check),'uniform_tests':len(record['all_uniform_tests']),'original_phases':len(record['all_original_controls'])},sort_keys=True))
