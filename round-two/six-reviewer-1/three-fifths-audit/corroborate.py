"""Late native corroboration; never supplies the primary proof or perturbed gap."""
import argparse,hashlib,json,os,resource,subprocess,sys,tempfile,time
from fractions import Fraction as F
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def run(native):
    here=Path(__file__).resolve().parent
    pins=json.loads((here/'PROVENANCE.json').read_text())['all10_target_file_whole_byte_pins']
    for n,pin in pins.items():
        data=(native/n).read_bytes()
        require(len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256'],'native whole source pin '+n)
    require((here/'PLAN.json').read_bytes()==(native/'COVER.json').read_bytes(),'whole signed tree/native tree equality')
    env=os.environ.copy()
    for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
              'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[n]='1'
    rows=[]
    with tempfile.TemporaryDirectory(prefix='three-fifths-native-') as tmp:
        def child(script,opt,options=(),negative=False):
            start=time.monotonic()
            p=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(script),*options],
                             env=env,capture_output=True,timeout=45)
            elapsed=time.monotonic()-start
            if negative:require(p.returncode==1 and p.stderr.startswith(b'FAIL: '),'native semantic rejection '+repr(options))
            else:require(p.returncode==0 and not p.stderr,'positive native/independent child')
            rows.append(dict(script=script.name,optimized=opt,negative=negative,options=[x for x in options if not str(x).startswith(tmp)],
                             seconds=round(elapsed,6),returncode=p.returncode,
                             cumulative_peak_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss))
        own=Path(tmp)/'own.json';child(here/'check.py',False,['--output',str(own)])
        fresh=[]
        for opt in [False,True]:
            file=Path(tmp)/('native-'+str(opt)+'.json');child(native/'verify.py',opt,['--record',str(file)]);fresh.append(file.read_bytes())
        require(json.loads(fresh[0])==json.loads(fresh[1]) and fresh[0]==fresh[1],'whole native normal/optimized parsed and byte equality')
        author=json.loads(fresh[0]);ind=json.loads(own.read_bytes());base=ind['two_exact_mass_budgets'][0]
        require(author['cover']==json.loads((here/'PLAN.json').read_text()),'whole declared cover equality')
        require(author['mass_coefficients']==ind['mass_floor']['coefficients'] and author['mass_integral']==ind['mass_floor']['integral'],'every mass coefficient/integral')
        require(author['centered_constants']==['1','0']+[x['chosen']for x in base['all_newton_maclaurin_minima']],'whole centered constants')
        for x,y in zip(author['constant_derivations'],base['all_newton_maclaurin_minima']):
            require(x['l']==y['l'] and x['newton']==y['newton'] and x['cauchy_maclaurin']==y['maclaurin'] and x['chosen']==y['chosen'],'every Newton/Maclaurin minimum')
            for k,v in x['power_caps'].items():
                k=int(k);eta=F(7,8)**((k-2)//2)*(F(479,512)if k%2 else 1)
                require(F(v)==eta,'every retained power cap')
        require(len(author['polar_cells'])==len(base['polar'])==63,'whole polar count')
        coefficients=0
        for x,y in zip(author['polar_cells'],base['polar']):
            require(x['k']==y['k'] and all(x[n]==y[n]for n in ['L','U','P','delta','integral']) and x['d']==y['D'],'every polar interval/payment/integral')
            require(x['all_coefficients']==y['coefficients'],'entire native/independent polar vector')
            require(x['all19_coefficients_sha256']==hashlib.sha256(json.dumps(x['all_coefficients'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),'native vector fingerprint after full comparison')
            coefficients+=len(x['all_coefficients'])
        xs={x['path']:x for x in author['origin_leaves']};ys={y['path']:y for y in base['origin']}
        require(set(xs)==set(ys) and len(xs)==272,'all origin paths')
        for path,x in xs.items():
            y=ys[path]
            for key,other in [('box','box'),('smax','s'),('Smax','S'),('dmean','ds'),('dbeta','db'),('dS','dS'),
                              ('beta','beta'),('odd_root','Q'),('D','D'),('R','R'),('score','bound')]:
                require(x[key]==y[other],'every origin mathematical field '+path+' '+key)
            require(len(x['terms'])==len(y['terms'])==7,'every centered order count')
            for a,b in zip(x['terms'],y['terms']):
                require(a['l']==b['l'],'same centered order')
                weighted=[str(F(v)*F(b['weight']))for v in b['coefficients']]
                require(a['all_coefficients']==weighted and F(a['integral'])==F(b['integral'])*F(b['weight']),'entire weighted centered vector/integral')
                require(a['coefficients_sha256']==hashlib.sha256(json.dumps(weighted,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'centered fingerprint after full comparison')
                coefficients+=len(weighted)
        for opt in [False,True]:
            for damage in ['last-polar-coefficient','drop-polar-series','newton-eighth','origin-drop-eighth',
                           'origin-odd-root','uncouple-energy','omit-leaf','radial-lower-cap','radial-coefficient','centered-third']:
                child(native/'verify.py',opt,['--damage',damage],True)
    return dict(agent='six-reviewer-1',role='independent mathematical reviewer',
                role_of_native_execution='late exposed corroboration only; no source of new perturbed margin',
                all10_native_source_pins_verified=True,all_primary_native_math_fields_equal=True,
                full_polynomial_vectors=63+272*7,full_coefficients=coefficients,
                fresh_native_bytes=len(fresh[0]),fresh_native_sha256=hashlib.sha256(fresh[0]).hexdigest(),
                entire_native_normal_optimized_records_equal=True,positive_children=3,semantic_rejections=20,
                fixed_guard_seconds=45,native_threads=1,serial=True,rows=rows,
                total_child_seconds=round(sum(x['seconds']for x in rows),6),maximum_child_seconds=max(x['seconds']for x in rows))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);a=p.parse_args()
    print(json.dumps(run(a.native.resolve()),sort_keys=True,indent=2))
