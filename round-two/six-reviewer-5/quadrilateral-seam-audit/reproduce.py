"""Complete own replay in four serial one-thread mathematical children."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
P=pathlib.Path(__file__).resolve().parent
def main():
    for f in json.loads((P/'MANIFEST.json').read_text())['files']:
        b=(P/f['path']).read_bytes()
        if len(b)!=f['bytes'] or hashlib.sha256(b).hexdigest()!=f['sha256']:raise ValueError('source manifest '+f['path'])
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
    expected=hashlib.sha256((P/'EVIDENCE.json').read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='tqq-audit-') as td:
        w=pathlib.Path(td)
        for n in ('audit.py','controls.py','kernel.py','prior_annulus.py'):shutil.copyfile(P/n,w/n)
        for mode in ([],['-O']):
            for n in ('audit.py','controls.py'):
                r=subprocess.run([sys.executable]+mode+['-B',str(w/n)],cwd=w,env=env,capture_output=True,text=True,timeout=45)
                if r.returncode:raise ValueError('incomplete or failed child: '+r.stderr)
            if hashlib.sha256((w/'EVIDENCE.json').read_bytes()).hexdigest()!=expected:raise ValueError('whole evidence mismatch')
    print(json.dumps(dict(actual_author='six-reviewer-5',role='independent mathematical reviewer',four_serial_normal_optimized_children=True,native_threads=1,guard_seconds=45,evidence_sha256=expected,ports=27,seams=81,semantic_damages_rejected_per_mode=10,ordinary_geometry_formalized=False)))
if __name__=='__main__':main()
