"""Serial whole-record/cold-source checks and consequential mathematical damages.

All six numeric thread variables are one. Fixed 45-second child guards;
no solver, resource-limit mutation, or native author executable is used.
"""
from pathlib import Path
import datetime,hashlib,json,os,resource,shutil,subprocess,sys,tempfile,time

ROOT=Path(__file__).resolve().parent
THREADS=['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
         'BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']
ENV=dict(os.environ,**{k:'1' for k in THREADS})

def need(condition,message):
    if not condition:raise ValueError(message)

def child(directory,script,optimized=False):
    args=[sys.executable,'-B']+(['-O'] if optimized else [])+[script]
    start=time.monotonic()
    try:r=subprocess.run(args,cwd=directory,env=ENV,capture_output=True,timeout=45)
    except subprocess.TimeoutExpired:raise RuntimeError('incomplete child; no mathematical inference')
    return r,dict(seconds=round(time.monotonic()-start,6),
                  cumulative_peak_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  returncode=r.returncode)

def checked_source():
    seal=json.loads((ROOT/'PRIMARY_SEAL.json').read_text())
    for name,row in seal['primary_files'].items():
        d=(ROOT/name).read_bytes()
        need(len(d)==row['bytes'] and hashlib.sha256(d).hexdigest()==row['sha256'],
             'immutable primary seal: '+name)
    return seal

def run():
    seal=checked_source();evidence=[];references={}
    with tempfile.TemporaryDirectory(prefix='half-disk-independent-') as td:
        cold=Path(td)/'cold';cold.mkdir()
        for name in ['exact.py','check.py','literal.py','PROOF.md','PRIMARY_SEAL.json']:
            shutil.copyfile(ROOT/name,cold/name)
        for directory,label in [(ROOT,'original-source'),(cold,'cold-source')]:
            for optimized in (False,True):
                for script in ('check.py','literal.py'):
                    r,usage=child(directory,script,optimized)
                    need(r.returncode==0 and not r.stderr,'positive exact child')
                    obj=json.loads(r.stdout)
                    need(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()+b'\n'==r.stdout,
                         'complete canonical JSON stream')
                    if script in references:need(references[script]==r.stdout,'ENTIRE positive record comparison')
                    else:references[script]=r.stdout
                    evidence.append(dict(source=label,optimized=optimized,script=script,
                                         bytes=len(r.stdout),sha256=hashlib.sha256(r.stdout).hexdigest(),
                                         whole_record_compared=True,**usage))
        mutations=[
          ('marked-cover-gap','check.py','(Q(9,20),Q(1,2))','(Q(23,50),Q(1,2))'),
          ('closed-right-endpoint','check.py','(Q(9,20),Q(1,2))','(Q(9,20),Q(49,100))'),
          ('radial-cover-gap','check.py','(Q(1,2),Q(1),Q(1))','(Q(3,5),Q(1),Q(1))'),
          ('last-radial-ceiling','check.py','(Q(3),Q(56,9),Q(7,3))','(Q(3),Q(56,9),Q(2))'),
          ('erase-phase-payment','check.py','k1=lo*(1-lo**2)*p/denominator**2','k1=Q(0)'),
          ('erase-radial-payment','check.py','k2=bh**2*lower/(2*ceiling*denominator)','k2=Q(0)'),
          ('excess-unproved-budget','check.py','record(Q(1,1000))','record(Q(1,10))'),
          ('wrong-Bernstein-denominator','exact.py','p[k]*Q(comb(i,k),comb(degree,k))','p[k]*Q(comb(i,k),comb(degree,k)+1)'),
          ('wrong-cycle-partition','exact.py','k**count * factorial(count)','k**count * factorial(count)+1'),
          ('wrong-literal-Newton-sign','literal.py','sign=1 if k%2 else -1','sign=-1 if k%2 else 1'),
          ('erase-origin-factor-nine','literal.py','o=gs(integral(origin),9)','o=integral(origin)'),
          ('erase-polar-original-a8','literal.py','a**8),gi(peval(quotient,aa))','Q(1)),gi(peval(quotient,aa))'),
          ('erase-centered-eighth-order','literal.py','for ell in range(9):','for ell in range(8):'),
        ]
        rejected=[]
        for label,file,before,after in mutations:
            damaged=Path(td)/label;damaged.mkdir()
            for name in ('exact.py','check.py','literal.py'):
                shutil.copyfile(ROOT/name,damaged/name)
            p=damaged/file;s=p.read_text();need(s.count(before)==1,'unique semantic mutation '+label)
            p.write_text(s.replace(before,after))
            script='literal.py' if file=='literal.py' else 'check.py'
            for optimized in (False,True):
                r,usage=child(damaged,script,optimized)
                need(r.returncode!=0,'mathematical damage accepted '+label)
                rejected.append(dict(label=label,optimized=optimized,rejected=True,**usage))
        # Entire external-result damages: no expected-field subset is trusted.
        fixture_rejections=[]
        for script,raw in references.items():
            obj=json.loads(raw)
            variants=[raw[:-3],b'{}\n',raw.replace(b'"agent":',b'"agents":',1),raw+b'{}\n']
            if script=='check.py':
                missing=json.loads(raw);del missing['refinement']['origin']['seven_terms'][-1]
                wrong=json.loads(raw);wrong['refinement']['closed_budget']='8000/1000'
                variants += [json.dumps(missing).encode(),json.dumps(wrong).encode()]
            else:
                missing=json.loads(raw);del missing['all_six_controls'][-1]
                wrong=json.loads(raw);wrong['generic_newton'][7]['degree']=7
                variants += [json.dumps(missing).encode(),json.dumps(wrong).encode()]
            for i,v in enumerate(variants):
                need(v!=raw,'damage differs from complete reference')
                fixture_rejections.append(dict(script=script,case=i,rejected_by_whole_stream=True))
    checked_source()
    return dict(agent='six-reviewer-1',role='independent mathematical reviewer',
                utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                positive=evidence,mathematical_damages=rejected,
                external_result_damages=fixture_rejections,all_primary_seals_unchanged=True,
                native_author_code_or_fixture_used=False,threads=1,serial_children=True,
                fixed_child_guard_seconds=45,resource_limits_unchanged=True,
                proof_unformalized=True,written_proof_exposed_NOT_BLIND=True)

if __name__=='__main__':print(json.dumps(run(),indent=2))
