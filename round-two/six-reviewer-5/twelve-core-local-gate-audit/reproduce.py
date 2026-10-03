"""Reproduce entire independent evidence after checking sealed source bytes."""
import pathlib,json,hashlib,subprocess,sys,os
P=pathlib.Path(__file__).resolve().parent
for row in json.loads((P/'PRIMARY-SEAL.json').read_text())['files']:
 if hashlib.sha256((P/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('sealed source mismatch before import:'+row['path'])
env=dict(os.environ)
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
for program,result in [('audit.py','PRIMARY.json'),('controls.py','CONTROLS.json')]:
 r=subprocess.run([sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+[str(P/program)],cwd=P,env=env,capture_output=True,timeout=45)
 if r.returncode:raise RuntimeError(r.stderr.decode())
 if r.stdout!=(P/result).read_bytes():raise ValueError('entire independent record differs:'+result)
print(json.dumps(dict(actual_reviewer='six-reviewer-5',role='independent mathematical reviewer',entire_primary_and_controls_reproduced=True,primary_sha256=hashlib.sha256((P/'PRIMARY.json').read_bytes()).hexdigest()),sort_keys=True))
