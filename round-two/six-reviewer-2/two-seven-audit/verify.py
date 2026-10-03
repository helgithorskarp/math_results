"""Empty-output source-only serial regeneration, two methods, fixed20s children."""
import argparse,datetime,hashlib,json,os,resource,shutil,subprocess,sys,time
from pathlib import Path
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE))
from semantic import need,equal,strict_read,controls

def dump(path,x):path.write_bytes(json.dumps(x,sort_keys=True,separators=(',',':')).encode()+b'\n')

def main():
    p=argparse.ArgumentParser();p.add_argument('--out-dir',required=True);a=p.parse_args();out=Path(a.out_dir).resolve();need(not out.exists(),'new empty directory required');out.mkdir(parents=True);start=time.monotonic();receipts=[];records={};pins={};env=os.environ.copy()
    for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
    def run(file,args,name,allowed_failure=False):
        cmd=[sys.executable,'-I','-B']+(['-O']if sys.flags.optimize else[])+[str(file),*args];t=time.monotonic()
        try:job=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=20)
        except subprocess.TimeoutExpired:
            dump(out/'INCOMPLETE.json',{'status':'TIMEOUT_NO_MATHEMATICAL_INFERENCE','child':name,'guard_seconds':20});raise
        r={'name':name,'seconds':time.monotonic()-t,'returncode':job.returncode,'stdout':job.stdout,'stderr':job.stderr,'guard_seconds':20,'native_threads':1,'child_cumulative_highwater_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss};receipts.append(r);dump(out/'RECEIPTS.json',receipts)
        if not allowed_failure:need(job.returncode==0,'arithmetic child failed '+name+' '+job.stderr)
        return job
    def pair(key,file,modes,extra=()):
        paths=[]
        for mode in modes:
            path=out/(key+'-'+mode+'.json');run(SOURCE/file,[mode,str(path),*extra]if file=='geometry.py'else([key if key=='shadows'else'inventory',mode,str(path),*extra]if file=='capacities.py'else[mode,str(out/'inventory37-literal.json'),str(path),*extra]),key+'-'+mode);paths.append(path)
        raws=[q.read_bytes()for q in paths];values=[strict_read(raw)for raw in raws];equal(*values);need(raws[0]==raws[1],'whole canonical bytes differ '+key)
        records[key]=values[0];pins[key]={'bytes':len(raws[0]),'sha256':hashlib.sha256(raws[0]).hexdigest(),'whole_typed_and_byte_equality':True}
    pair('inventory03','capacities.py',('literal','sets'),('0','3'))
    pair('inventory37','capacities.py',('literal','sets'),('3','7'))
    pair('shadows','capacities.py',('literal','sets'))
    pair('geometry','geometry.py',('lifts','progressions'))
    pair('branches','branches.py',('vectors','assignments'))
    pair('improvement','branches.py',('vectors','assignments'),('85',))
    # Bind the parent2 singleton reduction to fresh physical rows, rather
    # than transporting parent6's numerics as a mirrored result.
    C=records['inventory03']['single_maxima'];physical={p:{int(d):0 for d in C}for p in(2,6)}
    for row in records['geometry']['all_original_phase_rows']:
        d=row['original_modulus']//16
        if row['original_modulus']%16==0 and str(d)in C:
            physical[row['parent']][d]=max(physical[row['parent']][d],sum(mask!=0 for mask in row['all_four_quarter_masks']))
    for p in(2,6):equal({str(d):v for d,v in physical[p].items()},C)
    control=controls(records)
    # Actual changed arithmetic, tested against fresh data before hashes.
    bad=out/'damaged-source';bad.mkdir()
    for file in ('capacities.py','branches.py','geometry.py'):shutil.copyfile(SOURCE/file,bad/file)
    geometry=(bad/'geometry.py').read_text();need(geometry.count('for k in range(4):')==1,'one physical fault site');(bad/'geometry.py').write_text(geometry.replace('for k in range(4):','for k in range(3):'))
    job=run(bad/'geometry.py',['lifts',str(out/'bad-geometry.json')],'source-damage-fourth-lift',True)
    need(job.returncode!=0 and 'actual physical original phase disagrees with CRT row'in job.stderr,'must reject physical error mathematically')
    branch=(bad/'branches.py').read_text();need(branch.count('itertools.product((0,2),repeat=len(split))')==1,'one branch fault site');(bad/'branches.py').write_text(branch.replace('itertools.product((0,2),repeat=len(split))','itertools.product((0,),repeat=len(split))'))
    job=run(bad/'branches.py',['vectors',str(out/'inventory37-literal.json'),str(out/'bad-branches.json')],'source-damage-second-branch')
    wrong=strict_read((out/'bad-branches.json').read_bytes())
    try:equal(records['branches'],wrong)
    except ValueError:pass
    else:raise ValueError('fresh wrong branch census accepted')
    # Stored primary values are reproducibility gates only, never comparators
    # for the arithmetic source/evidence controls above.
    expected=strict_read((SOURCE/'EXPECTED.json').read_bytes());equal(expected['records'],pins)
    summary={'status':'COMPLETE_INDEPENDENT_REVIEWER_SOURCE_ONLY_REGENERATION','records':pins,'record_controls':control,'source_controls':['missing-fourth-lift-rejected-by-original-math','missing-second-branch-rejected-against-fresh-whole-census'],'parent6_uniform_capacity_bound':84,'total_BASE_hole_ceiling':174,'imported_BASE_lower':177,'target_original_body_and_tables_exposed_not_blind':True,'native_target_code_expected_corpus_required':False,'same_model_helpers_schema_and_Python_trust_base':True,'ordinary_reductions_unformalized':True}
    dump(out/'SUMMARY.json',summary);dump(out/'VALIDATION.json',{'utc':datetime.datetime.now(datetime.UTC).isoformat(),'seconds':time.monotonic()-start,'optimized':bool(sys.flags.optimize),'interpreter':sys.version,'guard_seconds':20,'native_threads':1,'serial_children':len(receipts),'receipts':receipts,'peak_cumulative_child_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'parent_peak_not_separately_measured':True});print(json.dumps({'status':summary['status'],'seconds':time.monotonic()-start,'negative_controls':len(control['negative']),'positive_controls':len(control['positive']),'source_controls':2,'pins':pins}),flush=True)

if __name__=='__main__':main()
