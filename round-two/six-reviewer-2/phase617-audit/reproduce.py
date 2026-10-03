"""Fresh source-only whole normal/optimized replay with separate raw receipts."""
from pathlib import Path
import argparse,subprocess,os,json,time,resource,hashlib,sys

def need(ok,why):
    if not ok:raise ValueError(why)

def run(output,pause):
    here=Path(__file__).resolve().parent;need(not output.exists(),'fresh output directory required');output.mkdir(parents=True)
    expected=json.loads((here/'EXPECTED.json').read_text());seal=json.loads((here/'INDEPENDENCE.json').read_text())
    for name,pin in seal['files'].items():
        b=(here/name).read_bytes();need(len(b)==pin['bytes']and hashlib.sha256(b).hexdigest()==pin['sha256'],'entire frozen primary source '+name)
    env=os.environ.copy()
    for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
    receipts=[];records={}
    def pair(key,script,args):
        previous=None
        for mode in [0,1]:
            need(not any(p.exists()for p in pause),'new pause barrier; incomplete replay')
            argv=[sys.executable]+(['-O']if mode else [])+[str(here/script)]+[str(v)for v in args(mode)]
            started=time.monotonic();stdout=output/(key+'_'+str(mode)+'.json');stderr=output/(key+'_'+str(mode)+'.stderr')
            try:r=subprocess.run(argv,capture_output=True,env=env,timeout=35)
            except subprocess.TimeoutExpired as e:
                stdout.write_bytes(e.stdout or b'');stderr.write_bytes(e.stderr or b'');raise RuntimeError('incomplete35s child '+key)
            stdout.write_bytes(r.stdout);stderr.write_bytes(r.stderr);need(r.returncode==0 and not r.stderr,'failed child '+key)
            wanted=expected['cases'][key];need(len(r.stdout)==wanted['bytes']and hashlib.sha256(r.stdout).hexdigest()==wanted['sha256'],'ENTIRE expected mathematical record '+key)
            if previous is None:previous=r.stdout
            else:need(previous==r.stdout,'ENTIRE saved normal/optimized bytes '+key)
            records[key]=json.loads(r.stdout);receipts.append({'key':key,'mode':mode,'seconds':time.monotonic()-started,'sha256':wanted['sha256'],'bytes':len(r.stdout)})
            (output/'execution.json').write_text(json.dumps({'status':'running','receipts':receipts},indent=2)+'\n')
    pair('rows','rows.py',lambda mode:[3704]);pair('sync','synchronize.py',lambda mode:[632])
    for N in [3702,3703,3704]:pair('roots_'+str(N),'roots.py',lambda mode,N=N:[N])
    for key in ['basis','seeds','rup']:pair(key,key+'.py',lambda mode:[])
    for key,kind in [('rows','rows'),('sync','sync')]+[('roots_'+str(N),'roots')for N in [3702,3703,3704]]:
        pair('verify_'+key,'verify.py',lambda mode,key=key,kind=kind:[kind,output/(key+'_'+str(mode)+'.json')])
    for key,kind in [('rows','rows'),('sync','sync'),('roots_3704','roots')]:
        pair('controls_'+key,'controls.py',lambda mode,key=key,kind=kind:[kind,output/(key+'_'+str(mode)+'.json')])
    need(set(records)==set(expected['cases'])and len(receipts)==32,'complete16-pair source-only domain')
    summary={'status':expected['status'],'children':len(receipts),'whole_mode_pairs':16,'all_full_records_checked':True,'guards_seconds':35,'threads':1,'maximum_child_seconds':max(r['seconds']for r in receipts),'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'semantic_record_damages_per_mode':11,'generic_RUP_DIMACS_damages_per_mode':10,'literal_positive_endpoint_words':4,'coloring_counts':[384,252,0],'common_regular_phase_choices':6}
    result={'summary':summary,'receipts':receipts,'records':records};(output/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--pause-file',type=Path,action='append',default=[]);a=p.parse_args();run(a.output,a.pause_file)
