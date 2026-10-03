"""Fresh serial exact reproduction, including verified published producer inputs.
Run python3 -B reproduce.py in an environment with requirements.txt installed.
The only downloaded files are the five pinned public mathematical source files.
"""
import datetime,hashlib,json,os,pathlib,resource,shutil,subprocess,sys,tempfile,time,urllib.request
D=pathlib.Path(__file__).resolve().parent

def need(ok,m):
 if not ok:raise ValueError(m)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
env=dict(os.environ)
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[k]='1'
rows=[];started=time.monotonic()
def run(name,args,expected_failure=False):
 t=time.monotonic();r=subprocess.run([sys.executable,'-B',*args],env=env,capture_output=True,timeout=55)
 if expected_failure:need(r.returncode>0 and b'ENTIRE typed mathematical record mismatch' in r.stderr,name+' bounded mathematical rejection')
 else:need(r.returncode==0,name+': '+r.stderr.decode())
 rows.append(dict(name=name,seconds=time.monotonic()-t,returncode=r.returncode,stdout_bytes=len(r.stdout),stdout_sha256=hashlib.sha256(r.stdout).hexdigest(),expected_failure=expected_failure));return r.stdout
pin=json.loads((D/'producer-pin.json').read_text());seal=json.loads((D/'primary-seal.json').read_text())
need(hashlib.sha256((D/'primary.py').read_bytes()).hexdigest()==seal['files']['primary.py']['sha256'],'primary source seal')
need(hashlib.sha256((D/'primary.json').read_bytes()).hexdigest()==seal['files']['primary.stdout']['sha256'],'primary certificate alias seal')
with tempfile.TemporaryDirectory(prefix='asymmetry-cold-',dir=D.parent) as tmp:
 T=pathlib.Path(tmp);producer=T/'producer';producer.mkdir()
 for row in pin['files']:
  url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+pin['commit']+'/'+row['path']
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'independent-asymmetry-audit'}),timeout=20) as r:raw=r.read()
  need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'whole pinned producer '+row['path'])
  (producer/pathlib.Path(row['path']).name).write_bytes(raw)
 outputs=[];comparisons=[]
 for mode in [[],['-O']]:
  suffix='O' if mode else 'normal'
  out=run('fresh-primary-'+suffix,[*mode,str(D/'primary.py')]);need(out==(D/'primary.json').read_bytes(),'ENTIRE sealed primary normal/O');outputs.append(out)
  run('native-original-'+suffix,[*mode,'-I',str(producer/'verify.py')])
  cmp=run('late-whole-comparison-'+suffix,[*mode,'-I',str(D/'compare_native.py'),'--primary',str(D/'primary.json'),'--producer',str(producer)]);comparisons.append(cmp)
 need(outputs[0]==outputs[1] and comparisons[0]==comparisons[1],'whole normal/O records')
 changed=json.loads((producer/'expected.json').read_text());last=changed['whole_algebra']['complete_polynomials']['DF'][-1];last[1]=str(__import__('fractions').Fraction(last[1])+1)
 fixture=T/'changed-last-DF.json';fixture.write_text(json.dumps(changed))
 for mode in [[],['-O']]:run('external-last-DF-'+('O' if mode else 'normal'),[*mode,'-I',str(producer/'verify.py'),'--expected',str(fixture)],True)
 comparison=json.loads(comparisons[0]);need(len(comparison['cross_method_damages'])==6 and len(comparison['native_six_mathematical_damages'])==6,'all semantic damages')
 result=dict(status='complete',cold_source_only=True,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-started,all_primary_seals_unchanged=True,whole_normal_O_equal=True,producer_inputs_full_pinned_hashes=True,top_level_serial_children=len(rows),max_child_seconds=max(r['seconds'] for r in rows),peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,native_threads=1,per_child_timeout_seconds=55,scope='unchanged 1 CPU/2 GiB; no search or timeout premise; ordinary bridges unformalized',comparison=comparison,runs=rows)
 print(json.dumps(result,sort_keys=True,separators=(',',':')))
