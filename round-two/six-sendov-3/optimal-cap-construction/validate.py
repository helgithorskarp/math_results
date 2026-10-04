"""Serial bounded same-author validation; one mathematical child at a time."""
from pathlib import Path
import argparse,copy,datetime,json,os,resource,shutil,subprocess,sys,tempfile,time
HERE=Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
         'BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
DAMAGES=('wrong_embedding','wrong_anchor','missing_ninth_root','wrong_even_repair',
         'wrong_odd_repair','wrong_inward_shift','wrong_pair_distance_sign',
         'wrong_fourth_binomial','wrong_skew_scaling')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
 parser.add_argument('--baseline-root',type=Path);args=parser.parse_args()
 start=time.monotonic();env=os.environ.copy()
 for name in THREADS:env[name]='1'
 rows=[];positive=[]
 def run(folder,optimized,extra,should_pass,description):
  command=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(folder/'verify.py')]+extra
  t=time.monotonic();result=subprocess.run(command,cwd=folder,env=env,capture_output=True,text=True,timeout=45)
  if (result.returncode==0)!=should_pass:
   raise RuntimeError(description+' unexpected outcome '+result.stdout+' '+result.stderr)
  row={'description':description,'optimized':optimized,'expected_pass':should_pass,
       'returncode':result.returncode,'seconds':time.monotonic()-t,'child_guard_seconds':45}
  if should_pass:
   summary=json.loads(result.stdout)
   if summary['status']!='PASS' or summary['original_root_count']!=9 or summary['field_identities']!=416:
    raise RuntimeError('incomplete positive coverage')
   row['summary']=summary;positive.append(summary)
  else:
   if 'REJECTED:' not in result.stderr:raise RuntimeError('negative did not reject through checker')
   row['reason']=result.stderr.strip()
  rows.append(row);print(description, 'PASS' if should_pass else 'REJECTED',flush=True)
 for optimized in (False,True):
  extra=['--baseline-root',str(args.baseline_root.resolve())] if args.baseline_root else []
  run(HERE,optimized,extra,True,'local complete record/baseline replay')
  for damage in DAMAGES:run(HERE,optimized,['--damage',damage],False,'mathematical '+damage)
 with tempfile.TemporaryDirectory(prefix='sendov-fourth-cap-cold-') as td:
  cold=Path(td)/'source';cold.mkdir()
  for p in HERE.iterdir():
   if p.is_file() and p.name!='VALIDATION.json':shutil.copyfile(p,cold/p.name)
  for optimized in (False,True):run(cold,optimized,[],True,'cold source-only complete replay')
  expected=json.loads((HERE/'EXPECTED.json').read_text());cases=[]
  data=copy.deepcopy(expected);g=data['all_nine_shrinking_roots_epsilon0to9'][8]['all_root_coefficients'][9]
  component=next(p for p in reversed(g) if p);old=component[-1][1][5];component[-1][1][5]='3' if old=='2' else '2'
  if data==expected:raise RuntimeError('external damage was a no-op')
  cases.append(('alter LAST root field coefficient',data))
  data=copy.deepcopy(expected);data['all_nine_shrinking_roots_epsilon0to9'].pop();cases.append(('remove ninth original',data))
  data=copy.deepcopy(expected);data['all_nine_shrinking_roots_epsilon0to9'][0]['label']=False;cases.append(('bool for integer label',data))
  data=copy.deepcopy(expected);data['ordinary_analytic_bridges_unformalized']=1;cases.append(('integer for boolean',data))
  data=copy.deepcopy(expected);data['unknown_field']=0;cases.append(('extra whole-record key',data))
  data=copy.deepcopy(expected);data['critical_multiplicities']=[6,1];cases.append(('omit pair critical multiplicity',data))
  data=copy.deepcopy(expected);data['direct_first_power_epsilon0to9'][9][0][0][1][0]='9';cases.append(('alter actual ninth FIRST-power coefficient',data))
  data=copy.deepcopy(expected);data['all_eight_Newton_powers_epsilon0to9'].pop();cases.append(('remove eighth Newton moment',data))
  for name,data in cases:
   damaged=Path(td)/'fixture.json';damaged.write_text(json.dumps(data))
   for optimized in (False,True):run(HERE,optimized,['--fixture',str(damaged)],False,name)
  duplicate=Path(td)/'duplicate.json';duplicate.write_text('{"schema":1,"schema":1}')
  run(HERE,False,['--fixture',str(duplicate)],False,'duplicate JSON object key')
  (cold/'cap.py').write_bytes(b'\n'+(cold/'cap.py').read_bytes())
  run(cold,False,[],False,'one source byte alteration')
 for summary in positive:
  if summary['whole_record_sha256']!=positive[0]['whole_record_sha256'] or summary['manifest_sha256']!=positive[0]['manifest_sha256']:
   raise RuntimeError('positive whole record/seal mismatch')
 out={'agent':'six-sendov-3','role':'researcher','status':'PASS','whole_summary':positive[0],
  'manifest_sha256':positive[0]['manifest_sha256'],'positive_modes':4,
  'mathematical_damage_cases':18,'distinct_mathematical_damages':9,
  'whole_external_fixture_rejections':17,'source_byte_rejections':1,
  'native_threads':1,'max_cpu_intensive_jobs':1,'child_guard_seconds':45,
  'scope':'existing individual1CPU2GiB unchanged; current shared3CPU9GiB respected',
  'whole_seconds':time.monotonic()-start,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
  'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'children':rows,
  'ordinary_proof_unformalized':True,'independent_review':False}
 if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ('children','whole_summary')},sort_keys=True))
if __name__=='__main__':main()
