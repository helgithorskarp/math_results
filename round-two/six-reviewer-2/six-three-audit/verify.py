"""Source-only reconstruction of the independent six/three audit.

All arithmetic is fresh in an empty output directory, serial fixed20s children.
Primary pins are consulted only after full two-method and semantic checks.
"""
import argparse,datetime,hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE))
from semantic import equal,need,check_bundle,CONTEXT
from controls import record_controls,source_controls

def dump(path,obj):path.write_bytes(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()+b'\n')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=('normal','optimized'),required=True);parser.add_argument('--out-dir',required=True);a=parser.parse_args();optimized=a.mode=='optimized';need(optimized==bool(sys.flags.optimize),'mode must agree with actual interpreter -O');out=Path(a.out_dir).resolve();need(not out.exists(),'empty new output directory required');out.mkdir(parents=True);start=time.monotonic();receipts=[];comparisons=[];env=os.environ.copy()
    for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
    def run(script,args,name,allow_failure=False):
        cmd=[sys.executable,'-I','-B']+(['-O']if optimized else[])+[str(script),*args];begin=time.monotonic()
        try:p=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=20)
        except subprocess.TimeoutExpired:
            dump(out/'INCOMPLETE.json',{'status':'TIMEOUT_NO_MATHEMATICAL_OR_REJECTION_INFERENCE','child':name,'guard_seconds':20,'threads':1,'resource_escalation':False});raise
        row={'child':name,'returncode':p.returncode,'seconds':time.monotonic()-begin,'guard_seconds':20,'threads':1,'RSS_kib_cumulative_children':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'stdout':p.stdout,'stderr':p.stderr};receipts.append(row);dump(out/'RECEIPTS.json',receipts);print(json.dumps({'child':name,'returncode':p.returncode,'seconds':row['seconds']}),flush=True)
        if not allow_failure:need(p.returncode==0,'arithmetic child failed: '+name+' '+p.stderr)
        return p
    def pair(kind,modes,extra=()):
        paths=[]
        for mode in modes:
            product=out/(kind+'-'+mode+'.json');run(SOURCE/(kind+'.py'),[mode,*extra,str(product)],kind+'-'+mode);paths.append(product)
        raw=[p.read_bytes()for p in paths];obj=[json.loads(r)for r in raw];equal(obj[0],obj[1]);need(raw[0]==raw[1],'full canonical byte products differ: '+kind);comparisons.append({'kind':kind,'bytes':len(raw[0]),'sha256':hashlib.sha256(raw[0]).hexdigest(),'whole_typed_equal':True,'whole_byte_equal':True});return obj[0],paths[0]
    first,firstpath=pair('first_stage',('partition','matching'))
    phases=[]
    for lo,hi in((0,5),(5,10),(10,16),(16,21),(21,26)):
        paths=[]
        for mode in('prefix','component'):
            product=out/('phases-'+mode+'-'+str(lo)+'.json');run(SOURCE/'phase_rows.py',[mode,str(firstpath),str(lo),str(hi),str(product)],'phases-'+mode+'-'+str(lo));paths.append(product)
        raw=[p.read_bytes()for p in paths];obj=[json.loads(r)for r in raw];equal(obj[0],obj[1]);need(raw[0]==raw[1],'all canonical phase rows differ');comparisons.append({'kind':'phases','block_interval':[lo,hi],'bytes':len(raw[0]),'sha256':hashlib.sha256(raw[0]).hexdigest(),'whole_typed_equal':True,'whole_byte_equal':True});phases.extend(obj[0])
    phasepath=out/'phases-whole.json';dump(phasepath,phases);del obj,raw
    shapes=sorted({r['repair_mask_hex']for b in phases for r in b['rows']if r['survives_necessary_tests']},key=lambda h:int(h,16))
    shapepath=out/'fresh-shapes.json';dump(shapepath,shapes)
    sym,sympath=pair('symmetry',('literal','crt'));glue,gluepath=pair('gluing',('bitmap','histogram'),(str(firstpath),str(shapepath)))
    semantic=check_bundle(first,phases,sym,glue,CONTEXT);bundle={'context':CONTEXT,'first':first,'phases':phases,'symmetry':sym,'gluing':glue};controls=record_controls(bundle);sources=source_controls(SOURCE,out/'source-damages',run,bundle,firstpath)
    pins={key:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for key,p in(('first',firstpath),('phases',phasepath),('symmetry',sympath),('gluing',gluepath))};expected=json.loads((SOURCE/'EXPECTED.json').read_bytes());equal(pins,expected['records']);equal(CONTEXT,expected['context'])
    summary={'status':'COMPLETE_SOURCE_ONLY_TWO_METHOD_AUDIT','records':pins,'semantic':semantic,'record_controls':controls,'arithmetic_source_controls':sources,'complete_two_method_comparisons':comparisons,'guard_seconds':20,'threads':1,'serialized_arithmetic_children':len(receipts),'shared_model_helpers_driver_schema':True,'same_Python_trust_base':True,'target_native_code_or_corpus_required':False,'written_proof_exposed_not_blind':True};dump(out/'SUMMARY.json',summary);validation={'utc':datetime.datetime.now(datetime.UTC).isoformat(),'mode':a.mode,'interpreter':sys.version,'total_seconds':time.monotonic()-start,'child_RSS_kib_cumulative_maximum':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'parent_RSS_not_separately_measured':True,'receipts':receipts,'source_only':True};dump(out/'VALIDATION.json',validation);print(json.dumps({'status':summary['status'],'seconds':validation['total_seconds'],'records':pins,'negative_record_controls':len(controls['negative_controls']),'positive_controls':len(controls['positive_controls']),'arithmetic_source_controls':len(sources)}),flush=True)
if __name__=='__main__':main()
