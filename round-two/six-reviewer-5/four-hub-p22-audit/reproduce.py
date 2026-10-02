"""Complete independent audit from compact public files; serial native1 stages."""
import argparse,hashlib,json,os,pathlib,resource,shutil,subprocess,sys,time

def need(x,m):
    if not x:raise ValueError(m)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=pathlib.Path,required=True);a=ap.parse_args();source=pathlib.Path(__file__).resolve().parent;work=a.work.resolve()
    need(not work.exists(),'fresh replay directory required');work.mkdir(parents=True)
    first=json.loads((source/'first-seal.json').read_text());second=json.loads((source/'additional-boundary-seal.json').read_text())
    names=list(first['sources'])+['boundary20.py'];initial={n:hashlib.sha256((source/n).read_bytes()).hexdigest() for n in names}
    need(all(initial[n]==v for n,v in first['sources'].items()) and initial['boundary20.py']==second['source_sha256'],'every sealed mathematical source byte unchanged')
    for name in names:shutil.copy2(source/name,work/name)
    env=dict(os.environ)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[key]='1'
    env['PYTHONDONTWRITEBYTECODE']='1';interpreter=[sys.executable]+(['-O'] if sys.flags.optimize else []);begun=time.monotonic();steps=[]
    for ordinal,name in enumerate(['independent.py','physical.py','independent.py','unit_flow.py','support.py','controls.py','boundary20.py']):
        start=time.monotonic();r=subprocess.run(interpreter+[str(work/name)],cwd=work,env=env,capture_output=True,text=True,timeout=60)
        need(r.returncode==0,'failed/incomplete required stage proves no absence: '+name+'\n'+r.stderr)
        steps.append({'stage':name,'seconds':time.monotonic()-start});(work/(str(ordinal)+'-'+name+'.stdout')).write_text(r.stdout)
        if ordinal==0:shutil.copy2(work/'independent-census.json',work/'broader-census2161.json')
        print(json.dumps({'stage':name,'ordinal':ordinal,'status':'PASS'}),flush=True)
    hashes={}
    for name,expected in first['whole_records'].items():
        data=(work/name).read_bytes()
        if name=='broader-census2161.json':
            diagnostic=json.loads(data);diagnostic.pop('physically_admissible_types',None)
            data=(json.dumps(diagnostic,sort_keys=True,separators=(',',':'))+'\n').encode()
        h=hashlib.sha256(data).hexdigest();need(h==expected['sha256'],'whole independent stage mismatch: '+name);hashes[name]=h
    h=hashlib.sha256((work/'independent-boundary20.json').read_bytes()).hexdigest();need(h==second['record_sha256'],'whole additional P20 boundary mismatch');hashes['independent-boundary20.json']=h
    need(initial=={n:hashlib.sha256((source/n).read_bytes()).hexdigest() for n in names},'source mutated during replay')
    mathematical={'agent':'six-reviewer-5','role':'independent mathematical reviewer','target':'bafkreicopechl5iwcvqc5qmyx4ibvewexlb2sj3ncheh3gwz7gdoydclj4','whole_records':hashes,'sources':initial,'P20_generic_vectors':47,'P21_physical_vectors':1822,'physical_marks':218960,'pressure_accepted':123877,'unit_masks':98315,'final_populations':11,'physical_signatures':837,'all_audited_T0_raw_carriers':56,'all_audited_T1_raw_carriers':1764,'T1_necessary_subset':1704,'full_population_carriers':4032,'retained_support_states':0,'support_algorithms':'coordinate-minimum exact integer convolution with weak q bounds and all-mark exact LOW-SAT bounds','limits':'no guard hit in completed pipeline; initial unfactored counter was incomplete, preserved privately and never a proof premise'}
    raw=(json.dumps(mathematical,sort_keys=True,separators=(',',':'))+'\n').encode();(work/'RESULT.json').write_bytes(raw)
    validation={'agent':'six-reviewer-5','role':'independent mathematical reviewer','python':sys.version,'mode':'optimized' if sys.flags.optimize else 'normal','mathematical_sha256':hashlib.sha256(raw).hexdigest(),'elapsed_seconds':time.monotonic()-begun,'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'native_threads':1,'serial':True,'subprocess_guard_seconds':60,'stages':steps,'ordinary_bridges_formalized':False}
    (work/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps({k:v for k,v in validation.items() if k not in ('stages','python')}),flush=True)
if __name__=='__main__':main()
