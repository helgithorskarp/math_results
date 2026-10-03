"""Source-only cold audit; optional pinned native replay; one bounded child at a time."""
import argparse,hashlib,json,os,pathlib,resource,subprocess,sys,time
S=pathlib.Path(__file__).resolve().parent
def need(ok,why):
    if not ok:raise ValueError(why)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--work',type=pathlib.Path,required=True);ap.add_argument('--native-dir',type=pathlib.Path);a=ap.parse_args()
    work=a.work.resolve();work.mkdir(parents=True,exist_ok=True)
    expected=json.loads((S/'EXPECTED.json').read_text());manifest=json.loads((S/'SOURCE_MANIFEST.json').read_text())
    for name,sha in manifest['files'].items():need(digest(S/name)==sha,'entire pinned source '+name)
    env=dict(os.environ)
    for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
    receipts=[]
    def child(label,script,flags,args,cwd=S):
        start=time.monotonic();cmd=[sys.executable,*flags,'-B',str(script),*map(str,args)]
        proc=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=45)
        (work/(label+'.stdout')).write_text(proc.stdout);(work/(label+'.stderr')).write_text(proc.stderr)
        need(proc.returncode==0,'bounded '+label+' failed: '+proc.stderr+proc.stdout)
        receipts.append(dict(label=label,seconds=time.monotonic()-start,peak_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,exit=0))
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        out=work/('primary-'+mode+'.json');child('primary-'+mode,S/'independent.py',flags,['--output',out]);raw=out.read_bytes()
        need(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())==expected['primary'],'ENTIRE primary record')
    need((work/'primary-normal.json').read_bytes()==(work/'primary-optimized.json').read_bytes(),'WHOLE independent normal/O bytes')
    if a.native_dir:
        src=a.native_dir.resolve();bindings=json.loads((S/'AUTHOR_SOURCE.json').read_text())
        for row in bindings['files']:need(digest(src/pathlib.Path(row['path']).name)==row['sha256'],'entire pinned native input')
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            out=work/('native-'+mode+'.json');mr=work/('native-'+mode+'-mode.json')
            child('native-'+mode,src/'verify.py',['-I',*flags],['--check',src/'expected.json','--output',out,'--mode-receipt',mr],src)
            md=json.loads(mr.read_text());need(md['optimize']==int(mode=='optimized') and set(md['native_threads'].values())=={'1'},'actual native flags/threads')
            raw=out.read_bytes();need(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())==expected['native'],'ENTIRE native record')
        need((work/'native-normal.json').read_bytes()==(work/'native-optimized.json').read_bytes(),'WHOLE native normal/O bytes')
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            child('late-'+mode,S/'late_check.py',flags,['--work',work])
            raw=(work/'late-comparison.json').read_bytes();need(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())==expected['late'],'ENTIRE late correspondence record')
    result=dict(actual_reviewer='six-reviewer-5',all_full_record_checks=True,native_and_late_completed=bool(a.native_dir),receipts=receipts,python=sys.version,fixed_child_guard_seconds=45,native_threads=1,one_serial_math_child=True,scope='unchanged1CPU2GiB',no_guard_hit=True)
    (work/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
