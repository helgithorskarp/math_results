"""Source-pinned independent review replay, with serial fixed-guard children."""
import argparse,hashlib,json,os,platform,resource,subprocess,sys,time
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--native-source',type=Path,required=True);parser.add_argument('--work',type=Path,required=True);parser.add_argument('--native-csv',type=Path,help='optional already regenerated complete CSV, still decoded and fully verified; otherwise pinned native source is freshly run')
    a=parser.parse_args();source=Path(__file__).resolve().parent;work=a.work.resolve();native=a.native_source.resolve()
    need(work!=source and source not in work.parents,'private work outside source');work.mkdir(parents=True,exist_ok=True);need(not any(work.iterdir()),'new empty work directory')
    env=dict(os.environ)
    for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
    manifest=json.loads((source/'MANIFEST.json').read_text());author=json.loads((source/'AUTHOR_SOURCE.json').read_text());seal=json.loads((source/'FIRST_SEAL.json').read_text())
    def pins():
        for name,p in manifest['files'].items():
            f=source/name;need(f.is_file()and not f.is_symlink()and hashlib.sha256(f.read_bytes()).hexdigest()==p['sha256']and f.stat().st_size==p['bytes'],'whole independent source pin: '+name)
        for name,p in author['files'].items():
            f=native/name;need(f.is_file()and not f.is_symlink()and hashlib.sha256(f.read_bytes()).hexdigest()==p['sha256']and f.stat().st_size==p['bytes'],'whole native source pin: '+name)
        for name,p in seal['files'].items():need(hashlib.sha256((source/name).read_bytes()).hexdigest()==p['sha256'],'unchanged pre-native independent seal')
    pins();record={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','status':'INCOMPLETE_NO_VERDICT','python':platform.python_version(),'numerical_threads':1,'serial_children':True,'native_source_pinned_before_import':True,'children':[]};begun=time.monotonic()
    def save():(work/'runtime.json').write_text(json.dumps(record,indent=2)+'\n')
    def child(mode,stage,args,guard):
        pins();t=time.monotonic();cmd=[sys.executable]+(['-O']if mode=='optimized'else[])+args
        try:r=subprocess.run(cmd,env=env,capture_output=True,timeout=guard)
        except subprocess.TimeoutExpired:record['failure']='fixed guard hit: '+stage;save();raise ValueError(record['failure'])
        record['children'].append({'mode':mode,'stage':stage,'seconds':time.monotonic()-t,'exit_code':r.returncode,'process_guard_seconds':guard});save();need(r.returncode==0,'incomplete helper: '+stage+' '+r.stderr.decode(errors='replace'));return r.stdout
    save()
    if a.native_csv:
        csv=a.native_csv.resolve();record['native_reconstruction']='supplied positive table; its whole pinned bytes and every AP are checked, no native verdict is assumed'
    else:
        child('normal','fresh-native-source-reconstruction',[str(native/'reproduce.py'),'--work',str(work/'native')],180)
        csv=work/'native/normal.csv';receipt=json.loads((work/'native/verification.json').read_text());need(receipt['status']=='FRESH_COMPLETE_BOOLEAN618_SOURCE_RECONSTRUCTION','complete native replay status');record['native_reconstruction']='fresh pinned58-child native wrapper, original20s mathematical children'
    # Data-only late adapter; all proof kernels below are the byte-identical pre-native sources.
    from adapter import decode
    from geometry import canonical
    from merge import merge
    neutral=canonical(decode(csv.read_bytes()));(work/'neutral.json').write_bytes(neutral)
    for mode in('normal','optimized'):
        outputs={};parts=[]
        for script,expected,guard in[('parameters.py','PARAMETERS.json',40),('controls.py','CONTROLS.json',20),('consequences.py','CONSEQUENCES.json',10)]:
            target=work/(mode+'-'+expected)
            args=[str(source/script)]+(['--output',str(target)]if script=='parameters.py'else[])
            raw=child(mode,script,args,guard)
            if script!='parameters.py':target.write_bytes(raw)
            need(target.read_bytes()==(source/expected).read_bytes(),'whole expected independent record: '+expected);outputs[expected]=target
        for first in range(0,2176,256):
            last=min(first+256,2176);p=work/(mode+'-'+str(first)+'.json');child(mode,'AP9:'+str(first)+'..'+str(last),[str(source/'positive.py'),'--certificate',str(work/'neutral.json'),'--start',str(first),'--end',str(last),'--output',str(p)],30);parts.append(json.loads(p.read_text()))
            if mode=='optimized':need(p.read_bytes()==(work/('normal-'+str(first)+'.json')).read_bytes(),'whole positive batch normal/O')
        out=canonical(merge(parts));(work/(mode+'-result.json')).write_bytes(out);need(out==(source/'RESULT.json').read_bytes(),'whole merged independent result')
        for script,expected,args,guard in[
            ('comparison.py','COMPARISON.json',['--native-source',str(native),'--csv',str(csv)],15),
            ('coverage_controls.py','COVERAGE.json',['--work',str(work)],30),
            ('source_controls.py','SOURCE_CONTROLS.json',['--certificate',str(work/'neutral.json'),'--work',str(work/(mode+'-source-damages'))],45)]:
            p=work/(mode+'-'+expected);flag='--output'if script=='comparison.py'else'--out';child(mode,script,[str(source/script),*args,flag,str(p)],guard);need(p.read_bytes()==(source/expected).read_bytes(),'whole late expected record: '+expected)
    need((work/'normal-result.json').read_bytes()==(work/'optimized-result.json').read_bytes(),'whole normal/O final records');pins()
    record.update(status='COMPLETE_INDEPENDENT_BOOLEAN618_AP9_REPRODUCTION',result_bytes=len(out),result_sha256=hashlib.sha256(out).hexdigest(),whole_expected_and_normal_optimized_records_equal=True,seconds=time.monotonic()-begun,peak_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,maximum_direct_child_seconds=max(z['seconds']for z in record['children']))
    save();print(json.dumps({k:v for k,v in record.items()if k!='children'},sort_keys=True))
if __name__=='__main__':main()
