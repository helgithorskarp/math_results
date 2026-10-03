"""Source-only normal/O replay. One serial mathematical child; each guard20s."""
from pathlib import Path
import tempfile,json,subprocess,os,time,hashlib,resource,sys

def need(ok,why):
    if not ok:raise ValueError(why)
def wire(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    src=Path(__file__).resolve().parent;seal=json.loads((src/'SEAL.json').read_text());expected=json.loads((src/'EXPECTED.json').read_text())
    for name,d in seal['files'].items():
        raw=(src/name).read_bytes();need(len(raw)==d['bytes']and sha(raw)==d['sha256'],'sealed source '+name)
    env=os.environ.copy()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
    receipts=[];outputs=[]
    with tempfile.TemporaryDirectory(prefix='review-nine-tail-')as root:
        root=Path(root)
        for name in ('literal.py','direct.py','controls.py'):(root/name).write_bytes((src/name).read_bytes())
        for optimized in (False,True):
            mode=['-O']if optimized else[]
            def run(name,args):
                started=time.monotonic();r=subprocess.run([sys.executable,'-B']+mode+[str(root/name)]+list(args),capture_output=True,env=env,timeout=20)
                need(r.returncode==0,'child failure '+name+': '+r.stderr.decode());value=json.loads(r.stdout)
                receipts.append({'program':name,'optimized':optimized,'seconds':time.monotonic()-started,'whole_stdout_bytes':len(r.stdout),'whole_stdout_sha256':sha(r.stdout),'peak_children_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'guard_seconds':20,'numerical_threads':1});return value,r.stdout
            record,raw=run('literal.py',[]);(root/'record.json').write_bytes(raw)
            need(sha(wire(record))==expected['whole_record_sha256']and len(wire(record))==expected['whole_record_bytes'],'whole primary expected record')
            audited,_=run('direct.py',[str(root/'record.json')]);need(audited==expected['direct_audit'],'whole direct mathematical audit')
            controls,_=run('controls.py',[str(root/'record.json')]);need(controls==expected['controls'],'whole interface controls')
            outputs.append({'record':record,'audit':audited,'controls':controls})
        need(outputs[0]==outputs[1],'ENTIRE normal/O mathematical products')
    print(wire({'status':'COMPLETE_COLD_SOURCE_ONLY_REPLAY','whole_record_sha256':expected['whole_record_sha256'],'whole_record_bytes':expected['whole_record_bytes'],'semantic_damages_per_mode':17,'malformed_damages_per_mode':5,'children':receipts,'all_sources_sealed':True,'all_whole_mode_records_equal':True}).decode())
if __name__=='__main__':main()
