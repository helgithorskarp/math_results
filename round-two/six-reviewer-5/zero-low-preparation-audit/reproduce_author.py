"""Optional exact pinned native replay, strictly serial, with owned comparison."""
import argparse,pathlib,json,hashlib,concurrent.futures,urllib.request,subprocess,sys,os,time
import compare_author
P=pathlib.Path(__file__).resolve().parent
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--scratch',required=True);args=parser.parse_args()
 dest=pathlib.Path(args.scratch).resolve()
 if dest.exists() and any(dest.iterdir()):raise ValueError('fresh empty scratch directory required')
 dest.mkdir(parents=True,exist_ok=True)
 meta=json.loads((P/'AUTHOR_SOURCE.json').read_text())
 def fetch(e):
  url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+meta['commit']+'/'+e['path']
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'six-reviewer-5-independent-replay'}),timeout=20) as response:raw=response.read()
  if len(raw)!=e['bytes'] or hashlib.sha256(raw).hexdigest()!=e['sha256']:raise ValueError('pinned full native source bytes differ')
  (dest/e['name']).write_bytes(raw)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,meta['files']))
 env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
 outputs=[];costs=[]
 for optimized in (False,True):
  for name in ('generate.py','verify.py'):
   started=time.monotonic()
   completed=subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+[str(dest/name)],cwd=dest,env=env,capture_output=True,timeout=45)
   if completed.returncode:raise ValueError(completed.stderr.decode())
   result=json.loads(completed.stdout)
   outputs.append({k:v for k,v in result.items() if k not in ('seconds','maximum_rss_kib')})
   costs.append(dict(program=name,optimized=optimized,seconds=time.monotonic()-started,guard_seconds=45))
 if outputs[:2]!=outputs[2:]:raise ValueError('whole native normal/optimized results differ')
 for e in meta['files']:
  if hashlib.sha256((dest/e['name']).read_bytes()).hexdigest()!=e['sha256']:raise ValueError('native source or regenerated certificate changed')
 print(json.dumps(dict(strictly_serial=True,native_results=outputs[:2],costs=costs,independent_comparison=compare_author.compare(dest)),sort_keys=True))
if __name__=='__main__':main()
