"""Serial cold source-only replay; downloads pinned public inputs into fresh scratch."""
import argparse,hashlib,json,os,pathlib,resource,shutil,subprocess,sys,time,urllib.request
a=argparse.ArgumentParser();a.add_argument('--work-dir',type=pathlib.Path,required=True);a.add_argument('--packages',type=pathlib.Path);a.add_argument('--late-damages',action='store_true');a.add_argument('--primary-damages',action='store_true');args=a.parse_args()
source=pathlib.Path(__file__).resolve().parent;P=args.work_dir.resolve();P.mkdir(parents=True,exist_ok=False)
for name in ['independent.py','compare.py']:shutil.copyfile(source/name,P/name)
env=os.environ.copy()
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[k]='1'
runs=[];downloads=[]
def run(file,mode,extra=(),reject=False,label=None):
 label=label or file.stem+'-'+mode;command=[sys.executable,'-I','-B']+(['-O'] if mode=='optimized' else [])
 if args.packages:command+=['-c',"import sys,runpy; sys.path.insert(0,sys.argv.pop(1)); runpy.run_path(sys.argv.pop(1),run_name='__main__')",str(args.packages.resolve()),str(file)]
 else:command.append(str(file))
 command+=list(map(str,extra));tic=time.monotonic();r=subprocess.run(command,env=env,capture_output=True,timeout=55)
 (P/(label+'.stdout')).write_bytes(r.stdout);(P/(label+'.stderr')).write_bytes(r.stderr)
 if (r.returncode!=0)!=reject:raise RuntimeError(label+' '+r.stderr.decode())
 runs.append(dict(label=label,returncode=r.returncode,seconds=time.monotonic()-tic,peak_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,stdout_bytes=len(r.stdout),stdout_sha256=hashlib.sha256(r.stdout).hexdigest()))
 return r.stdout
raw=[]
for mode in ['normal','optimized']:
 raw.append(run(P/'independent.py',mode,label=mode))
 if raw[-1]!=(source/'EXPECTED.json').read_bytes():raise ValueError('ENTIRE frozen primary record')
 if args.primary_damages:
  for d in ['G-pivot','F-recovery','omitted-fourth-row','E-boundary','lift-sign','unit-coefficient']:run(P/'independent.py',mode,['--damage',d],True,label=mode+'-'+d)
if raw[0]!=raw[1]:raise ValueError('whole primary normal/O')
inputs=json.loads((source/'DATA_INPUTS.json').read_text())
for item in inputs['files']:
 path=P/item['local_path'];path.parent.mkdir(parents=True,exist_ok=True)
 url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+item['source_commit']+'/'+item['repository_path']
 with urllib.request.urlopen(url,timeout=20) as response:data=response.read()
 if hashlib.sha256(data).hexdigest()!=item['sha256']:raise ValueError('whole public input hash')
 path.write_bytes(data);downloads.append(dict(path=item['local_path'],bytes=len(data),sha256=item['sha256']))
for mode in ['normal','optimized']:run(P/'target-source/verify.py',mode,['--export',P/('native-'+mode+'.json')])
if (P/'native-normal.json').read_bytes()!=(P/'native-optimized.json').read_bytes():raise ValueError('entire native normal/O')
run(P/'degree-five-triangular/verify.py','normal',['--export',P/'pencil-export.json'])
checks=[]
for mode in ['normal','optimized']:
 checks.append(run(P/'compare.py',mode,[P]))
 if args.late_damages:
  for d in ['unit','witness','content']:run(P/'compare.py',mode,[P,'--damage',d],True,label='compare-'+mode+'-'+d)
if checks[0]!=checks[1]:raise ValueError('whole late comparison normal/O')
summary=dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',serial_math_children=True,native_threads=1,fixed_child_guard_seconds=55,scope='unchanged1CPU2GiB',primary_whole_records_equal=True,native_whole_records_equal=True,late_whole_records_equal=True,runs=runs,public_data_only_inputs=downloads)
(P/'REPLAY_RECEIPT.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
