#!/usr/bin/env python3
"""Regenerate triplet growth controls and the two exact cover/refutation models."""
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
  need(json.loads(run([sys.executable,*flags,ROOT/'structural.py']))==EXPECTED['structural'],'Structural controls differ')
 small=[]
 for ref in EXPECTED['small_field']:
  q,L=ref['q'],ref['minority_weight_cap'];cnf=work/f'small-{q}-{L}.cnf'
  run([sys.executable,ROOT/'generate.py','--q',q,'--limit',L,'--output',cnf])
  checked=json.loads(run([sys.executable,ROOT/'check.py',cnf,'--q',q,'--limit',L,'--counter-source',paths['counter_auditor'],'--small']))
  need(checked==ref,'Complete seeded field controls differ');small.append(checked)
 need(any(x['accepted_seeded_words'] for x in small),'Missing positive cyclic field controls')
 cnf=work/'mixed9.cnf';run([sys.executable,ROOT/'generate.py','--mixed-n',9,'--output',cnf])
 mixed9=json.loads(run([sys.executable,ROOT/'check.py',cnf,'--mixed-n',9,'--counter-source',paths['counter_auditor'],'--small']))
 need(mixed9==EXPECTED['small_mixed'],'Complete mixed Boolean controls differ')
 auditor=module(ROOT/'check.py','triplet_definition_auditor');counter=auditor.load_counter(paths['counter_auditor'])
 positive=EXPECTED['positive45'];bits=tuple(map(int,positive['word']))
 need(len(bits)==45 and sha_bytes(positive['word'].encode())==positive['word_sha256'] and auditor.mixed_valid(bits),'Known45-point positive control failed')
 cnf=work/'mixed45.cnf';run([sys.executable,ROOT/'generate.py','--mixed-n',45,'--output',cnf])
 auditor.mixed_audit(cnf.read_text(),45,counter);_,clauses=counter.parse(cnf.read_text())
 need(counter.satisfied(clauses,{i+1:bool(b) for i,b in enumerate(bits)}),'Positive mixed CNF differs')
 print('TRIPLET_AND_COMPLETE_SMALL_POSITIVE_CONTROLS_PASSED',flush=True)
 damaged=work/'bad_counter.py';damaged.write_bytes(paths['counter_auditor'].read_bytes()+b'\n# damaged pinned source\n')
 try:auditor.load_counter(damaged)
 except ValueError:pass
 else:raise ValueError('Changed helper was accepted')
 damaged.unlink();checker=module(paths['RUP_checker'],'positive_RUP_checker');results=[]
 for ref in EXPECTED['cases']:
  name,params=ref['name'],ref['params'];cnf=work/(name+'.cnf')
  generated=json.loads(run([sys.executable,ROOT/'generate.py',*params,'--output',cnf]))
  need(generated==ref['model'],'Generated model differs')
  flags_controls=['--controls'] if name=='seeded25' else []
  for flags in ([],['-O']):
   audited=json.loads(run([sys.executable,*flags,ROOT/'check.py',cnf,*params,'--counter-source',paths['counter_auditor'],*flags_controls]))
   need(audited==ref['audit'],'Independent model coverage differs')
  print(name+'_NORMAL_AND_OPTIMIZED_MODEL_AUDITED',flush=True)
  drat=cnf.with_suffix('.drat');lrat=cnf.with_suffix('.lrat');proposal={'status':'RESUMED_PROPOSAL','mathematical_exclusion':False}
  if not(a.resume and drat.exists() and lrat.exists()):
   proposal=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',cnf],seconds=35))
   need(proposal['status']=='UNSAT_PENDING_CHECK','SAT/UNKNOWN is not an exclusion')
   conversion=run([work/'drat-trim',cnf,drat,'-t',25,'-L',lrat],seconds=30)
   cnf.with_suffix('.conversion.log').write_text(conversion);need('VERIFIED' in conversion,'Incomplete conversion')
  proofs=[]
  for flags in ([],['-O']):
   checked=json.loads(run([sys.executable,*flags,paths['RUP_checker'],cnf,lrat]));checked.pop('seconds',None)
   need(checked['mathematical_exclusion'] and checked['cnf_sha256']==generated['model_sha256'],'Proof/model mismatch');proofs.append(checked)
  need(proofs[0]==proofs[1],'Optimized replay differs');bad=proof_controls(checker,work,cnf,lrat)
  unknown=json.loads(run([sys.executable,Path(__file__).resolve(),'--solve',cnf,'--conflicts',1]))
  need(unknown['status']=='UNKNOWN' and not unknown['mathematical_exclusion'],'Incomplete proposal was promoted')
  results.append({'name':name,'model':generated,'audit':audited,'proof':proofs[0],'proposal':proposal,'controls':bad,
                  'normal_and_optimized_audits_and_replays':True,'one_conflict_UNKNOWN_control':True,
                  'reference_trace_match':sha(drat)==ref['drat_sha256'] and proofs[0]==ref['proof']})
  print(name+'_EXACT_REFUTATION_AND_CORRUPTION_CONTROLS_PASSED',flush=True)
 summary={'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_SEPARABLE_WEIGHT_26_77_AND_TRIPLET_GROWTH',
          'cases':results,'structural':EXPECTED['structural'],'small_field':small,'small_mixed':mixed9,'positive45':positive,
          'changed_counter_pin_rejected':True,'full_separable_orientation_weight_range':[26,77],'broader_T_weight_range':[24,79],
          'seconds':time.monotonic()-start,'parent_peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'child_peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
          'full_family_excluded':False,'length3704_witness_found':False,'new_W_bound':False}
 (work/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k not in ('cases','structural','small_field','small_mixed','positive45')},sort_keys=True))

def sha_bytes(raw):return hashlib.sha256(raw).hexdigest()

if __name__=='__main__':main()
