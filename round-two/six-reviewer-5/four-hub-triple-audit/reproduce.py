"""Independent compact source replay: four serial children, native threads1."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
P=pathlib.Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def main():
    manifest=json.loads((P/'MANIFEST.json').read_text())
    for f in manifest['files']:
        raw=(P/f['path']).read_bytes();need(len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256'],'source manifest '+f['path'])
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[key]='1'
    expectation={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ('EVIDENCE.json','PHYSICAL.json','CONTROLS.json')}
    seal=json.loads((P/'first-seal.json').read_text());support_sha=next(x['sha256'] for x in seal['files'] if x['path']=='SUPPORT.json')
    with tempfile.TemporaryDirectory(prefix='four-hub-audit-') as td:
        work=pathlib.Path(td)
        for name in ('audit.py','controls.py','prior_dp.py','prior_rows.py','prior_bit_rows.py','fixtures.json'):shutil.copyfile(P/name,work/name)
        for mode in ([],['-O']):
            for name in ('audit.py','controls.py'):
                r=subprocess.run([sys.executable]+mode+['-B',str(work/name)],cwd=work,env=env,capture_output=True,text=True,timeout=45)
                need(r.returncode==0,'incomplete child is not mathematical absence: '+r.stderr)
            for name,digest in expectation.items():need(hashlib.sha256((work/name).read_bytes()).hexdigest()==digest,'entire '+name+' differs')
            need(hashlib.sha256((work/'SUPPORT.json').read_bytes()).hexdigest()==support_sha,'whole reconstructed uncommitted support record')
    print(json.dumps(dict(actual_author='six-reviewer-5',role='independent mathematical reviewer',four_serial_normal_optimized_children_pass=True,native_threads=1,guard_seconds=45,whole_record_sha256=expectation['EVIDENCE.json'],support_record_sha256=support_sha,all_eight_semantic_controls_reject=True,ordinary_bridges_formalized=False)))
if __name__=='__main__':main()
