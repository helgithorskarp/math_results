#!/usr/bin/env python3
"""Reproduce three counter-free ascent refutations and explicit conditional corollaries."""
import argparse,ctypes,hashlib,importlib.metadata,importlib.util,json,os,resource,subprocess,sys,time,urllib.request
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
 paths={'RUP_checker':work/'check_rup_lrat.py','drat_converter':work/'drat-trim.c'}
 for key,path in paths.items():pinned(EXPECTED['sources'][key],path)
 run(['gcc','-O2','-std=gnu99',paths['drat_converter'],'-o',work/'drat-trim'])
 for flags in ([],['-O']):
  need(json.loads(run([sys.executable,*flags,ROOT/'structural.py']))==EXPECTED['structural'],'Local phase/group controls differ')
 small=[]
 for ref in EXPECTED['small']:
  q,case=ref['q'],ref['case'];cnf=work/(str(q)+'-'+case+'.cnf')
  run([sys.executable,ROOT/'generate.py','--q',q,'--case',case,'--output',cnf])
  results=[json.loads(run([sys.executable,*flags,ROOT/'check.py',cnf,'--q',q,'--case',case,'--small'])) for flags in ([],['-O'])]
  need(results[0]==results[1]==ref,'Complete small branch controls differ');small.append(ref)
 checker=module(paths['RUP_checker'],'credited_strict_RUP_checker');cases=[]
 for ref in EXPECTED['cases']:
  case=ref['name'];cnf=work/(case+'.cnf');drat=cnf.with_suffix('.drat');lrat=cnf.with_suffix('.lrat')
  model=json.loads(run([sys.executable,ROOT/'generate.py','--case',case,'--output',cnf]))
  need(model==ref['model'],'Production model differs')
  audits=[json.loads(run([sys.executable,*flags,ROOT/'check.py',cnf,'--case',case,'--controls'])) for flags in ([],['-O'])]
  need(audits[0]==audits[1]==ref['audit'],'Production normal/optimized definition audits differ')
  proposal={'status':'RESUMED_PROPOSAL','mathematical_exclusion':False}
  if not(a.resume and drat.exists() and lrat.exists()):
   proposal=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',cnf],seconds=35))
   need(proposal['status']=='UNSAT_PENDING_CHECK','Proposal is incomplete; no exclusion follows')
   conversion=run([work/'drat-trim',cnf,drat,'-t','25','-L',lrat],seconds=30)
   cnf.with_suffix('.conversion.log').write_text(conversion)
  need(sha(drat)==ref['drat_sha256'],'Native reference trace differs')
  proofs=[]
  for flags in ([],['-O']):
   d=json.loads(run([sys.executable,*flags,paths['RUP_checker'],cnf,lrat],seconds=50));d.pop('seconds',None);proofs.append(d)
  need(proofs[0]==proofs[1]==ref['proof'],'Strict production proof differs')
  bad=proof_controls(checker,work,cnf,lrat)
  unknown=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',cnf,'--conflicts',1],seconds=35))
  need(unknown['status']=='UNKNOWN' and not unknown['mathematical_exclusion'],'UNKNOWN control misclassified')
  cases.append({'name':case,'model':model,'audit':audits[0],'proposal':proposal,'proof':proofs[0],
                'normal_and_optimized_audits_and_replays':True,'reference_trace_match':True,
                'controls':bad,'one_conflict_UNKNOWN_control':True})
 damaged=work/'changed_checker.py';damaged.write_bytes(paths['RUP_checker'].read_bytes()+b'\n# changed pin\n')
 try:pinned(EXPECTED['sources']['RUP_checker'],damaged)
 except ValueError:pass
 else:raise ValueError('Changed checker pin accepted')
 damaged.unlink()
 result={'agent':'six-vdw-3','role':'researcher','status':EXPECTED['success_status'],'cases':cases,
         'small':small,'structural':EXPECTED['structural'],'claim':EXPECTED['claim'],
         'mathematical_dependencies_not_recomputed_by_runner':EXPECTED['mathematical_dependencies_not_recomputed_by_runner'],
         'changed_checker_pin_rejected':True,'seconds':time.monotonic()-start,
         'parent_peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'child_peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
         'runtime':{'python':sys.version.split()[0],'python_sat':importlib.metadata.version('python-sat'),'six':importlib.metadata.version('six')}}
 (work/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
