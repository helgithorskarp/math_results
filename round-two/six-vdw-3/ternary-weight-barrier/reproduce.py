#!/usr/bin/env python3
"""Regenerate and independently verify the at-most23 word exclusion."""
import argparse,ctypes,hashlib,importlib.util,json,os,resource,subprocess,sys,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent
EXPECTED=json.loads((ROOT/'expected.json').read_text())
ENV=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')

def need(ok,message):
 if not ok:raise ValueError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def run(argv,seconds=40):
 p=subprocess.run(list(map(str,argv)),text=True,capture_output=True,env=ENV,timeout=seconds)
 need(p.returncode==0,'Child failed: '+p.stderr+p.stdout);return p.stdout

def pinned(info,path):
 data=path.read_bytes() if path.exists() else urllib.request.urlopen(info['url'],timeout=20).read()
 need(hashlib.sha256(data).hexdigest()==info['sha256'],'External source hash mismatch')
 path.write_bytes(data)

def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def solve(cnf,conflicts):
 import pysat
 from pysat.solvers import Solver
 need(pysat.__version__==EXPECTED['solver']['python_sat_version'],'Solver version differs')
 clauses=[list(map(int,row.split()[:-1])) for row in cnf.read_text().splitlines()[1:]]
 start=time.monotonic()
 with Solver(name='cadical195',bootstrap_with=clauses,with_proof=True) as s:
  s.conf_budget(conflicts);result=s.solve_limited();stats=s.accum_stats()
  if result is False:
   need(ctypes.CDLL(None).fflush(None)==0,'Proof stream flush failed')
   cnf.with_suffix('.drat').write_text('\n'.join(s.get_proof())+'\n')
  if result is True:cnf.with_suffix('.assignment.json').write_text(json.dumps(s.get_model())+'\n')
 status={None:'UNKNOWN',False:'UNSAT_PENDING_CHECK',True:'SAT_PENDING_CHECK'}[result]
 print(json.dumps({'status':status,'conflict_budget':conflicts,'stats':stats,
                   'seconds':time.monotonic()-start,'mathematical_exclusion':False},sort_keys=True))

def proof_controls(checker,work,cnf,lrat):
 tiny=work/'control.cnf';proof=work/'control.lrat'
 tiny.write_text('p cnf 2 3\n1 2 0\n-1 0\n-2 0\n');proof.write_text('4 0 2 3 1 0\n')
 need(checker.verify(tiny,proof)['mathematical_exclusion'],'Positive proof control failed')
 invalid=['4 1 0 3 1 0\n','4 0 -1 2 0\n','4 3 0 1 0\n','4 0 99 0\n',
          '4 0 2 3 1\n','4 0 1 0\n','4 d 2 0\n5 0 2 3 1 0\n','3 0 2 3 1 0\n']
 for body in invalid:
  proof.write_text(body)
  try:checker.verify(tiny,proof)
  except (ValueError,KeyError,IndexError):pass
  else:raise ValueError('Malformed proof was accepted')
 lines=lrat.read_text().splitlines();changed=lines.copy();n=int(cnf.read_text().splitlines()[0].split()[2])
 for i,row in enumerate(changed):
  words=row.split()
  if words[1] not in ('d','0'):
   words[1]=str(n+1);changed[i]=' '.join(words);break
 else:raise ValueError('No nonempty production addition')
 damaged=['\n'.join(changed)+'\n','\n'.join(row for row in lines if row.split()[1]!='0')+'\n']
 for body in damaged:
  proof.write_text(body)
  try:checker.verify(cnf,proof)
  except (ValueError,KeyError,IndexError):pass
  else:raise ValueError('Corrupted production proof was accepted')
 tiny.unlink();proof.unlink()
 return {'generic_bad_proofs_rejected':len(invalid),'production_corruptions_rejected':len(damaged)}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workdir',type=Path,default=ROOT/'build')
 p.add_argument('--resume',action='store_true');p.add_argument('--solve',type=Path)
 p.add_argument('--conflicts',type=int,choices=(1,100000),default=100000);a=p.parse_args()
 if a.solve:solve(a.solve,a.conflicts);return
 start=time.monotonic();work=a.workdir.resolve();work.mkdir(parents=True,exist_ok=True)
 paths={'counter_auditor':work/'counter_audit.py','RUP_checker':work/'check_rup_lrat.py','drat_converter':work/'drat-trim.c'}
 for key,path in paths.items():pinned(EXPECTED['sources'][key],path)
 run(['gcc','-O2','-std=gnu99',paths['drat_converter'],'-o',work/'drat-trim'])
 for flags in ([],['-O']):
  need(json.loads(run([sys.executable,*flags,ROOT/'elementary.py']))==EXPECTED['elementary'],'Elementary controls differ')
 small=[]
 for ref in EXPECTED['small_family']:
  q,L,e=ref['q'],ref['weight_limit'],ref['encoding'];cnf=work/f'small-{q}-{L}-{e}.cnf'
  run([sys.executable,ROOT/'generate.py','--q',q,'--limit',L,'--encoding',e,'--output',cnf])
  result=json.loads(run([sys.executable,ROOT/'check.py',cnf,'--q',q,'--limit',L,'--encoding',e,'--counter-source',paths['counter_auditor'],'--small']))
  need(result==ref,'Complete small Boolean/product controls differ');small.append(result)
 need(any(x['accepted_fiber_words'] for x in small),'Missing positive controls')
 print('ELEMENTARY_AND_COMPLETE_SMALL_CONTROLS_PASSED',flush=True)
 models=[]
 for ref in EXPECTED['models']:
  e=ref['model']['encoding'];cnf=work/f'weight23-{e}.cnf'
  generated=json.loads(run([sys.executable,ROOT/'generate.py','--limit',23,'--encoding',e,'--output',cnf]))
  need(generated==ref['model'],'Exact generated model differs')
  for flags in ([],['-O']):
   audited=json.loads(run([sys.executable,*flags,ROOT/'check.py',cnf,'--limit',23,'--encoding',e,'--counter-source',paths['counter_auditor'],'--controls']))
   need(audited==ref['audit'],'Definition-level model audit differs')
  models.append({'model':generated,'audit':audited,'normal_and_optimized_audits':True})
  print(e.upper()+'_MODEL_DEFINITION_AUDITED',flush=True)
 damaged=work/'bad_counter.py';damaged.write_bytes(paths['counter_auditor'].read_bytes()+b'\n# changed pinned source\n')
 rejected=subprocess.run([sys.executable,ROOT/'check.py',work/'weight23-cut.cnf','--limit','23','--counter-source',damaged],capture_output=True,text=True,env=ENV)
 need(rejected.returncode!=0 and 'Pinned independent counter auditor differs' in rejected.stderr,'Changed helper was accepted');damaged.unlink()
 cnf=work/'weight23-cut.cnf';drat=cnf.with_suffix('.drat');lrat=cnf.with_suffix('.lrat')
 proposal={'status':'RESUMED_PROPOSAL','mathematical_exclusion':False}
 if not (a.resume and drat.exists() and lrat.exists()):
  proposal=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',cnf],seconds=35))
  need(proposal['status']=='UNSAT_PENDING_CHECK','SAT/UNKNOWN is not a refutation')
  conversion=run([work/'drat-trim',cnf,drat,'-t','25','-L',lrat],seconds=30)
  cnf.with_suffix('.conversion.log').write_text(conversion);need('VERIFIED' in conversion,'Conversion did not complete')
 print('PROOF_PROPOSED_OR_RESUMED_PENDING_EXACT_REPLAY',flush=True)
 replays=[]
 for flags in ([],['-O']):
  checked=json.loads(run([sys.executable,*flags,paths['RUP_checker'],cnf,lrat]));checked.pop('seconds',None)
  need(checked['mathematical_exclusion'] and checked['cnf_sha256']==models[0]['model']['model_sha256'],'Proof/model mismatch')
  replays.append(checked)
 need(replays[0]==replays[1],'Normal/optimized proof replay differs')
 bad=proof_controls(module(paths['RUP_checker'],'positive_RUP_checker'),work,cnf,lrat)
 unknown=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',cnf,'--conflicts',1]))
 need(unknown['status']=='UNKNOWN' and not unknown['mathematical_exclusion'],'Incomplete proof proposal was promoted')
 summary={'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_TERNARY_CRITERION_WEIGHT_24_79',
          'models':models,'proof':replays[0],'proposal':proposal,'controls':bad,'small_family':small,
          'elementary':EXPECTED['elementary'],'changed_counter_pin_rejected':True,'one_conflict_UNKNOWN_control':True,
          'normal_and_optimized_proof_replays':True,'reference_trace_match':sha(drat)==EXPECTED['drat_sha256'] and replays[0]==EXPECTED['proof'],
          'seconds':time.monotonic()-start,'parent_peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'child_peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
          'criterion_weight_range':[24,79],'full_family_excluded':False,'length3704_witness_found':False,'new_W_bound':False}
 (work/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k not in ('models','small_family','elementary','proof','proposal')},sort_keys=True))

if __name__=='__main__':main()
