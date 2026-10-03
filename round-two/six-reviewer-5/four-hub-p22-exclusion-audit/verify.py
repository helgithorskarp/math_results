"""Portable cold source-only independent replay; all large outputs in scratch.
No researcher executable is needed for the independent proof.
"""
import argparse,hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
SOURCE=pathlib.Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=pathlib.Path,required=True)
    args=parser.parse_args();work=args.work.resolve()
    need(not work.exists(),'fresh workspace scratch required; preserve failed prefixes')
    manifest=json.loads((SOURCE/'SOURCE_MANIFEST.json').read_text())['files']
    need(all(hashlib.sha256((SOURCE/n).read_bytes()).hexdigest()==d for n,d in manifest.items()),'frozen public source changed')
    expected=json.loads((SOURCE/'EXPECTED.json').read_text());work.mkdir(parents=True)
    for r in json.loads((SOURCE/'PRE_NATIVE_SEAL.json').read_text())['files']:
        b=(SOURCE/r['name']).read_bytes();need(hashlib.sha256(b).hexdigest()==r['sha256'],'pre-native primary pin')
        (work/r['name']).write_bytes(b)
    flags=['-O'] if sys.flags.optimize else [];env=dict(os.environ)
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
    # This bounded parent can take several minutes; each mathematical child
    # retains its fixed60s external and all smaller internal guards.
    result=subprocess.run([sys.executable,*flags,str(work/'reproduce.py')],env=env,capture_output=True)
    (work/'independent-primary.log').write_bytes(result.stdout+result.stderr)
    need(result.returncode==0,'incomplete independent replay is no absence: '+result.stderr.decode())
    control=subprocess.run([sys.executable,*flags,str(work/'controls22.py')],env=env,capture_output=True,timeout=60)
    (work/'independent-controls.log').write_bytes(control.stdout+control.stderr)
    need(control.returncode==0,'incomplete controls are no absence: '+control.stderr.decode())
    mode='optimized' if sys.flags.optimize else 'normal'
    actual=json.loads((work/('whole-'+mode+'.json')).read_text())
    need(actual==expected['primary'],'ALL ordered primary record bytes/counts/individual digests differ')
    b=(work/'controls22.json').read_bytes()
    need(len(b)==expected['controls']['bytes'] and hashlib.sha256(b).hexdigest()==expected['controls']['sha256'],'whole literal/coefficient/control record differs')
    need(all(hashlib.sha256((SOURCE/n).read_bytes()).hexdigest()==d for n,d in manifest.items()),'public source changed during cold replay')
    receipt=dict(actual_reviewer='six-reviewer-5',role='independent mathematical reviewer',mode=mode,
                 status='COMPLETE_COLD_SOURCE_ONLY_INDEPENDENT_REPLAY',
                 primary=actual,controls=expected['controls'],one_serial_mathematical_child=True,
                 threads=1,scope='unchanged1CPU2GiB',all_guards_unchanged=True)
    (work/'COLD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status=receipt['status'],mode=mode,primary_mathematical_bytes=actual['mathematical_stream_bytes'],
                         primary_sha256=actual['mathematical_stream_sha256'],controls_sha256=expected['controls']['sha256']),sort_keys=True))

if __name__=='__main__':main()
