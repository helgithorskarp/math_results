"""Bounded serial replays and targeted mathematical/schema rejection controls."""
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parent
THREADS=['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
         'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS']
ENV=os.environ|{k:'1'for k in THREADS}
runs=[]


def run(name,args,good=True):
    start=time.monotonic()
    try:r=subprocess.run([sys.executable,*args],capture_output=True,env=ENV,timeout=45)
    except subprocess.TimeoutExpired as e:
        raise RuntimeError('operational timeout; no mathematical verdict: '+name)from e
    elapsed=time.monotonic()-start
    if good and r.returncode!=0:
        raise ValueError(name+' positive replay failed '+r.stderr.decode()[-1200:])
    if not good and (r.returncode==0 or b'ValueError'not in r.stderr):
        raise ValueError(name+' intended mathematical/schema rejection not established')
    row={'name':name,'exit':r.returncode,'seconds':round(elapsed,6),
         'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),
         'positive':good}
    if good:row['result']=json.loads(r.stdout)
    else:row['reason']=r.stderr.decode().strip().splitlines()[-1]
    runs.append(row);return r.stdout


def main():
    rec=ROOT/'EXPECTED.json'
    if not rec.is_file():raise ValueError('own complete record required')
    raw=rec.read_bytes();whole=json.loads(raw)
    primary={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
             for name in ['audit.py','portable.py','validate.py','EXPECTED.json']}
    outputs={}
    with tempfile.TemporaryDirectory(prefix='quartet-audit-')as tmp:
        tmp=Path(tmp);cold=tmp/'cold';cold.mkdir()
        for name in primary:shutil.copyfile(ROOT/name,cold/name)
        for mode,flags in [('normal',['-B']),('optimized',['-B','-O'])]:
            outputs['CAS '+mode]=run('CAS '+mode,[*flags,str(ROOT/'audit.py'),'--expected',str(rec)])
            outputs['portable '+mode]=run('portable '+mode,['-I',*flags,str(ROOT/'portable.py'),str(rec)])
        outputs['CAS cold']=run('CAS cold',['-B',str(cold/'audit.py'),'--expected',str(cold/'EXPECTED.json')])
        outputs['portable cold']=run('portable cold',['-I','-B',str(cold/'portable.py'),str(cold/'EXPECTED.json')])
        if outputs['CAS normal']!=outputs['CAS optimized'] or outputs['CAS normal']!=outputs['CAS cold']:
            raise ValueError('entire CAS output differs')
        if outputs['portable normal']!=outputs['portable optimized'] or outputs['portable normal']!=outputs['portable cold']:
            raise ValueError('entire portable output differs')
        for mode,flags in [('normal',['-B']),('optimized',['-B','-O'])]:
            for damage in ['critical-cubic','odd-octic','dependent-opening']:
                run('method damage '+mode+' '+damage,[*flags,str(ROOT/'audit.py'),'--damage',damage],False)
        fixtures=[]
        def make(label,change):
            r=copy.deepcopy(whole);change(r);fixtures.append((label,r))
        make('missing identity',lambda r:r['identities'].pop('wzero forced negative variance'))
        make('missing final moment',lambda r:r['polynomials'].pop('original_moment_8'))
        make('changed final moment coefficient',lambda r:r['polynomials']['original_moment_8']['terms'][-1].update(coefficient='999'))
        make('last Bernstein sign',lambda r:r['bernstein']['opening3 gain numerator']['coefficients'].__setitem__(-1,'-1'))
        make('missing last Sturm coefficient',lambda r:r['root_controls']['outside triple singleton 1']['sturm_chain'][-1]['terms'].clear())
        make('root count Boolean',lambda r:r['root_controls']['outside triple singleton 1'].update(positive_root_count=True))
        make('omitted zero endpoint control',lambda r:r['root_controls'].pop('excluded zero boundary'))
        make('duplicate root bracket',lambda r:r['root_controls']['distinct fiber 1']['brackets'].__setitem__(1,copy.deepcopy(r['root_controls']['distinct fiber 1']['brackets'][0])))
        make('zero clearing denominator',lambda r:r['identities']['pencil invariant R']['clearing_denominator']['terms'][0].update(coefficient='0'))
        def coupled(r):
            for side in ['left','right']:
                r['identities']['original octic coefficient 1'][side]['terms'][0]['coefficient']='999'
        make('changed both copies of odd coefficient',coupled)
        for label,r in fixtures:
            f=tmp/'fixture.json';f.write_text(json.dumps(r))
            for mode,flags in [('normal',['-I','-B']),('optimized',['-I','-B','-O'])]:
                run('fixture '+mode+' '+label,[*flags,str(ROOT/'portable.py'),str(f)],False)
    if any(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h for name,h in primary.items()):
        raise ValueError('primary source bytes changed during validation')
    print(json.dumps({'agent':'six-reviewer-1','role':'independent mathematical reviewer',
         'python':sys.version.split()[0],'sympy':'1.14.0','native_threads':1,'serial_children':True,
         'fixed_per_child_seconds':45,'whole_record_bytes':len(raw),'whole_record_sha256':hashlib.sha256(raw).hexdigest(),
         'primary_files':primary,'positive_children':6,'method_rejections':6,'fixture_rejections':20,
         'total_child_seconds':round(sum(r['seconds']for r in runs),6),
         'max_child_seconds':max(r['seconds']for r in runs),
         'cumulative_child_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
         'runs':runs,'all_primary_files_unchanged':True,
         'CAS_full_record_bytes_equal_normal_optimized_cold':True,
         'portable_whole_reconstructions_agree_normal_optimized_cold':True},indent=2))


if __name__=='__main__':main()
