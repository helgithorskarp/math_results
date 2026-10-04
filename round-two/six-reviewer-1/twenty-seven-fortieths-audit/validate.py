"""Bounded serial exact replays and consequential mathematical defect controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time


def require(ok,label):
    if not ok:raise ValueError(label)


def main():
    p=argparse.ArgumentParser();p.add_argument('--private-dir',type=Path,required=True)
    args=p.parse_args();root=Path(__file__).resolve().parent;out=args.private_dir.resolve()
    require(out!=root and root not in out.parents,'generated records must be outside source directory')
    out.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
                 'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:env[name]='1'
    original={n:hashlib.sha256((root/n).read_bytes()).hexdigest()
              for n in json.loads((root/'PRIMARY_SEAL.json').read_text())['files']}
    cold=out/'cold';cold.mkdir(exist_ok=True)
    for name in [*original,'PRIMARY_SEAL.json','verify.py','refine.py']:
        shutil.copyfile(root/name,cold/name)
    rows=[];positive=[];negative=[]
    def child(label,program,argv,optimized=False,expect=0,reason=None):
        command=[sys.executable,'-I','-B']+(['-O']if optimized else[])+[str(program),*map(str,argv)]
        t=time.monotonic();r=subprocess.run(command,capture_output=True,env=env,timeout=45)
        seconds=time.monotonic()-t
        (out/(label+'.stdout')).write_bytes(r.stdout);(out/(label+'.stderr')).write_bytes(r.stderr)
        require((r.returncode==0)==(expect==0),'unexpected child result '+label)
        if expect:
            require(b'ValueError'in r.stderr and reason.encode()in r.stderr,
                    'intended mathematical/schema/preimport rejection '+label)
        row={'label':label,'exit':r.returncode,'seconds':round(seconds,6),
             'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest()}
        if reason:row['intended_rejection']=reason
        rows.append(row);(positive if not expect else negative).append(row)
        (out/'progress.json').write_text(json.dumps({'rows':rows,'primary_hashes':original},indent=2)+'\n')
        return r.stdout
    reference=literal_reference=refined_reference=None
    for location,directory in [('local',root),('cold',cold)]:
        for optimized in [False,True]:
            label=location+('-O'if optimized else'-normal')
            record=out/(label+'.record.json')
            summary=child(label,directory/'verify.py',['--record',record],optimized)
            raw=record.read_bytes()
            if reference is None:reference=(summary,raw)
            require((summary,raw)==reference,'ENTIRE independent records differ across execution modes')
            lit=child('literal-'+label,directory/'literal.py',[],optimized)
            if literal_reference is None:literal_reference=lit
            require(lit==literal_reference,'ENTIRE Gaussian/original/clipping controls differ')
            rr=out/('refined-'+label+'.record.json')
            refined=child('refined-'+label,directory/'refine.py',['--record',rr],optimized)
            if refined_reference is None:refined_reference=(refined,rr.read_bytes())
            require((refined,rr.read_bytes())==refined_reference,'ENTIRE refined leaf-surplus records differ')
    semantic={
        'product-lost-fifth':'all five positive lower-exponential terms',
        'product-inverted-exponential':'positive exponential reciprocal direction',
        'gap-overreach':'whole clipped leaf surpluses',
        'lost-eighth':'whole typed independent summary and record seal',
        'beta-as-norm':'whole typed independent summary and record seal',
        'mean-lost-eighth':'whole typed independent summary and record seal',
        'mean-wrong-denominator':'whole typed independent summary and record seal',
        'lost-phase-coupling':'whole typed independent summary and record seal',
    }
    for damage,reason in semantic.items():
        for optimized in [False,True]:
            child('damage-'+damage+('-O'if optimized else'-normal'),root/'verify.py',
                  ['--damage',damage],optimized,expect=1,reason=reason)
    baseline=json.loads((root/'COVER.json').read_text())
    variants=[]
    def altered(label,reason,change):
        z=json.loads(json.dumps(baseline));change(z);variants.append((label,reason,z))
    altered('root-radius','whole closed root domain',lambda z:z['root'].__setitem__(1,'2/3'))
    altered('boolean-axis','cut axis',lambda z:z['splits'][''].__setitem__('axis',True))
    altered('noncanonical-cut','canonical rational',lambda z:z['splits'][''].__setitem__('cut','2/4'))
    altered('missing-last-leaf','unvisited/missing branch',lambda z:z['leaves'].pop(sorted(z['leaves'])[-1]))
    altered('unreachable-extra','all listed and reachable nodes exactly agree',lambda z:z['leaves'].__setitem__('00000','origin-passes'))
    altered('unknown-status','leaf scope/type',lambda z:z['leaves'].__setitem__(next(iter(z['leaves'])),'unproved'))
    altered('extra-schema','complete cover schema',lambda z:z.__setitem__('unpaid',[]))
    for label,reason,z in variants:
        path=out/(label+'.cover.json');path.write_text(json.dumps(z))
        for optimized in [False,True]:
            child('cover-'+label+('-O'if optimized else'-normal'),root/'verify.py',
                  ['--cover',path],optimized,expect=1,reason=reason)
    expected=json.loads((root/'EXPECTED.json').read_text());expected['nodes']=True
    path=out/'typed-expected.json';path.write_text(json.dumps(expected))
    for optimized in [False,True]:
        child('expected-type'+('-O'if optimized else'-normal'),root/'verify.py',
              ['--expected',path],optimized,expect=1,reason='whole typed independent summary and record seal')
    for damage,reason in [('lost-terminal','all eight exact seven-factor coefficients'),
                          ('wrong-product-direction','clipped product ratio loss direction'),
                          ('gap-overreach','refined gap against every entire defining leaf')]:
        for optimized in [False,True]:
            child('refined-damage-'+damage+('-O'if optimized else'-normal'),root/'refine.py',
                  ['--damage',damage],optimized,expect=1,reason=reason)
    for optimized in [False,True]:
        damaged=out/('source-O'if optimized else'source-normal');damaged.mkdir(exist_ok=True)
        for name in [*original,'PRIMARY_SEAL.json','verify.py']:shutil.copyfile(root/name,damaged/name)
        (damaged/'arithmetic.py').write_text((damaged/'arithmetic.py').read_text()+'\nraise RuntimeError("must not be imported")\n')
        child('source-preimport'+('-O'if optimized else'-normal'),damaged/'verify.py',[],optimized,
              expect=1,reason='preimport source pin')
    require(original=={n:hashlib.sha256((root/n).read_bytes()).hexdigest()for n in original},
            'primary source changed during validation')
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','result':'PASS',
            'python':sys.version.split()[0],'positive_children':positive,'rejections':negative,
            'entire_records_equal':True,'entire_literal_outputs_equal':True,
            'entire_refinement_records_equal':True,
            'refinement_record_bytes':len(refined_reference[1]),
            'refinement_record_sha256':hashlib.sha256(refined_reference[1]).hexdigest(),
            'actual_refined_gap':'1/131072',
            'record_bytes':len(reference[1]),'record_sha256':hashlib.sha256(reference[1]).hexdigest(),
            'literal_bytes':len(literal_reference),'literal_sha256':hashlib.sha256(literal_reference).hexdigest(),
            'max_child_seconds':max(r['seconds']for r in rows),
            'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'primary_seals_unchanged':True,'children_serial':True,'all_native_threads':1,
            'fixed_child_timeout_seconds':45,'resource_limit_hit':False,
            'trust':'Ordinary analytic bridges and external real Hilbert Banach identity remain unformalized.'}
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':main()
