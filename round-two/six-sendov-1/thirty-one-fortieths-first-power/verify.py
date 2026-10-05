"""Serial source-bound replay; finite controls are not a formal proof."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as Q
import argparse,importlib.util,json,os,subprocess,sys
HERE=Path(__file__).resolve().parent
GUARD=45
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
BASE_FILES=('.gitignore','README.md','PROOF.md','ENTRY-PROOF.md','core.py','origin.py','product.py','coupled.py','entry_fixed.py','face_fixed.py','face_fixed_00.py','face_fixed_01.py','face_fixed_02.py','literal.py','homothety.py','ENTRY_COVER.json','FACE_COVER.json','verify.py')

def need(ok,why):
    if not ok:raise ValueError(why)
def unique(pairs):
    out={}
    for key,value in pairs:
        need(key not in out,'duplicate JSON key');out[key]=value
    return out
def read(path):return json.loads(path.read_text(),object_pairs_hook=unique)
def raw_record(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def clean(value):
    if isinstance(value,Q):return str(value)
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v) for v in value]
    return value
def same(a,b):
    need(type(a) is type(b),'whole typed record type mismatch')
    if isinstance(a,dict):
        need(set(a)==set(b),'whole typed record key mismatch')
        for k in a:same(a[k],b[k])
    elif isinstance(a,list):
        need(len(a)==len(b),'whole typed vector length mismatch')
        for x,y in zip(a,b):same(x,y)
    else:need(a==b,'whole typed exact record mismatch')
def source_rows(names):
    return {name:{'bytes':(HERE/name).stat().st_size,'sha256':sha256((HERE/name).read_bytes()).hexdigest()} for name in names}
def seal():
    m=read(HERE/'MANIFEST.json');need(set(m)=={'files','status','scope'} and m['status']=='SEALED','source seal schema')
    need(set(m['files'])==set(BASE_FILES)|{'EXPECTED.json'},'all defining sources and expected envelope sealed')
    same(source_rows(m['files']),m['files']);return m

def local(name):
    spec=importlib.util.spec_from_file_location('annular_delivery_'+name,HERE/(name+'.py'))
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result

def calculate(records):
    # Every child reconstructs its whole geometry and pays complete analytic
    # coefficients before this coordinator compares records or fingerprints.
    env=os.environ.copy();env.update({key:'1' for key in THREAD_KEYS});env['PYTHONDONTWRITEBYTECODE']='1'
    collected=[];parts=[]
    for script in ('entry_fixed.py','face_fixed_00.py','face_fixed_01.py','face_fixed_02.py'):
        command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(HERE/script)]
        p=subprocess.run(command,cwd=HERE,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=GUARD)
        need(p.returncode==0,'math child failed '+script+': '+p.stderr.decode()[-1000:])
        row=json.loads(p.stdout,object_pairs_hook=unique)
        need(row['agent']=='six-sendov-1' and row['role']=='researcher','author and role scope')
        collected.append(row);parts.append({'part':script,'bytes':len(p.stdout),'sha256':sha256(p.stdout).hexdigest()})
        if records:(records/(script+'.json')).write_bytes(p.stdout)
        print('paid '+script,file=sys.stderr,flush=True)
    entry=collected[0];faces=collected[1:]
    need(entry['status']=='ALL_FIXED_CLOSED_ENTRY_ESTIMATES_PASS' and len(entry['all390_whole_leaf_payments'])==390,'complete entry payment')
    paths=faces[0]['all450_paths'];selected=[];roles={};margins=[]
    for batch,row in enumerate(faces):
        need(row['status']=='ALL_FIXED_SHARD_LEAVES_PAID' and row['batch']==batch and row['shard_count']==3,'every fixed shard paid')
        for name in ('root','all449_closed_cut_payments','all450_leaf_geometry','all450_paths','centered_constants','all_centered_derivations'):
            same(row[name],faces[0][name])
        same(row['selected150_paths'],paths[150*batch:150*(batch+1)])
        same([r['path'] for r in row['all150_full_leaf_payments']],row['selected150_paths'])
        selected.extend(row['selected150_paths'])
        for leaf in row['all150_full_leaf_payments']:
            margin=Q(leaf['margin']);need(margin>0,'strict exact final face margin')
            margins.append(margin);role=leaf['role'];roles[role]=roles.get(role,0)+1
    same(selected,paths);need(len(set(selected))==450,'disjoint exhaustive final face partition')
    need(roles=={'retained-mean-product-origin':276,'joint-energy-polar':164,'standard-polar':10},'all final analytic roles')
    coupled=local('coupled');literal=local('literal');hom=local('homothety')
    controls={'coupled':coupled.clean(coupled.payment()),'literal':{str(a):literal.compute(endpoint=a) for a in (Q(3,4),Q(31,40))},'homothety':hom.compute()}
    damage_rows=[]
    for name in literal.DAMAGES:
        for endpoint in (Q(3,4),Q(31,40)):
            try:literal.compute(name,endpoint)
            except ValueError as exc:damage_rows.append({'component':'literal','damage':name,'endpoint':str(endpoint),'gate':str(exc)})
            else:raise ValueError('literal intended semantic damage accepted '+name)
    for name in hom.DAMAGES:
        try:hom.compute(name)
        except ValueError as exc:damage_rows.append({'component':'homothety','damage':name,'gate':str(exc)})
        else:raise ValueError('homothety intended semantic damage accepted '+name)
    for name,_ in coupled.DAMAGES:
        if name=='J-underpaid-bound':continue # Valid sharper bound, not a defect.
        try:coupled.payment(name)
        except ValueError as exc:damage_rows.append({'component':'coupled','damage':name,'gate':str(exc)})
        else:raise ValueError('coupled intended semantic damage accepted '+name)
    controls['valid_sharper_J_bound']=coupled.clean(coupled.payment('J-underpaid-bound'))
    controls['all_intended_semantic_rejections']=damage_rows
    raw=raw_record(controls)
    if records:(records/'physical-and-clipping.json').write_bytes(raw)
    parts.append({'part':'physical-and-clipping','bytes':len(raw),'sha256':sha256(raw).hexdigest()})
    expected={'agent':'six-sendov-1','role':'researcher','result':'PASS','degree':9,'interval':['3/4','31/40'],'epsilon':'1/10000','entry_shells':86,'entry_cuts':304,'entry_leaves':390,'face_cuts':449,'face_leaves':450,'roles':roles,'minimum_face_margin':str(min(margins)),'parts':parts,'physical_semantic_rejections':len(damage_rows),'ordinary_author_proof_supplied':True,'formalized':False,'independently_reviewed':False,'global_FIRST_proved':False}
    return expected

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');parser.add_argument('--records',type=Path);args=parser.parse_args()
    if args.records:
        records=args.records.resolve();need(records!=HERE and HERE not in records.parents,'large records outside source directory');records.mkdir(parents=True,exist_ok=True)
    else:records=None
    before=None if args.emit else seal() # No mathematical imports before seal.
    expected=calculate(records)
    if args.emit:
        need(not (HERE/'MANIFEST.json').exists(),'author generation does not silently overwrite a sealed source')
        (HERE/'EXPECTED.json').write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
        (HERE/'MANIFEST.json').write_text(json.dumps({'status':'SEALED','scope':'CLOSED[3/4,31/40], epsilon1/10000; ordinary/unformalized/unreviewed','files':source_rows(BASE_FILES+('EXPECTED.json',))},indent=2,sort_keys=True)+'\n')
    else:
        same(expected,read(HERE/'EXPECTED.json'));same(seal(),before)
    print(json.dumps(expected,sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,ZeroDivisionError,json.JSONDecodeError,subprocess.TimeoutExpired) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
