"""Bounded serial source-only reproduction and meaningful adverse controls."""
from pathlib import Path
from hashlib import sha256
import argparse,datetime,json,os,resource,shutil,subprocess,sys,time

HERE=Path(__file__).resolve().parent
NATIVE=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
        'VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
FILES=('arithmetic.py','series.py','constants.py','family.py','calculation.py','verify.py',
       'validate.py','EXPECTED.json','SOURCE.json','README.md','PROOF.md',
       'DEPENDENCIES.json','LITERATURE.md','.gitignore')

def need(condition,message):
    if not condition:raise RuntimeError(message)

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode('ascii')

def seal_expected(copy):
    p=copy/'SOURCE.json';x=json.loads(p.read_bytes());blob=(copy/'EXPECTED.json').read_bytes()
    x['files']['EXPECTED.json']={'bytes':len(blob),'sha256':sha256(blob).hexdigest()}
    p.write_bytes(canonical(x)+b'\n')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--scratch',type=Path,required=True)
    args=ap.parse_args();work=args.scratch.resolve()
    need(not work.is_relative_to(HERE),'validation scratch must be outside source')
    work.mkdir(parents=True,exist_ok=True)
    need(not any(work.iterdir()),'validation scratch must be empty')
    env=os.environ.copy()
    for key in NATIVE:env[key]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    cold=work/'cold';cold.mkdir()
    for name in FILES:shutil.copyfile(HERE/name,cold/name)
    before={name:(HERE/name).read_bytes() for name in FILES}
    results=[];records={}
    def run(label,source,stage='forcing',optimized=True,damage=None,expected=None,reject=None):
        output=work/(label+'.json')
        command=[sys.executable,'-I','-B']
        if optimized:command.append('-O')
        command.extend([str(source/'verify.py'),'--stage',stage,'--output',str(output)])
        if damage:command.extend(['--damage',damage])
        if expected:command.extend(['--expected',str(expected)])
        started=time.monotonic()
        try:
            p=subprocess.run(command,cwd=work,env=env,capture_output=True,text=True,timeout=45)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError('incomplete computation: unchanged45s timeout, not a mathematical conclusion') from exc
        row={'label':label,'stage':stage,'optimized':optimized,'returncode':p.returncode,
             'seconds':time.monotonic()-started,'expected_rejection':reject,'timeout':False}
        (work/(label+'.stdout')).write_text(p.stdout);(work/(label+'.stderr')).write_text(p.stderr)
        if reject:
            alternatives=(reject,) if type(reject) is str else reject
            matched=next((term for term in alternatives if term in p.stderr),None)
            need(p.returncode!=0 and matched is not None and not output.exists(),
                 'intended adverse control failed '+label+' '+p.stdout+p.stderr)
            row['matched_rejection']=matched
        else:
            need(p.returncode==0 and output.exists(),'complete positive failed '+label+' '+p.stdout+p.stderr)
            blob=output.read_bytes();value=json.loads(blob)
            if stage in records:
                # Complete nested record and complete bytes, before digest.
                need(type(value) is dict and value==json.loads(records[stage]),
                     'whole generated positive record mismatch '+label)
                need(blob==records[stage],'whole positive canonical bytes mismatch '+label)
            else:records[stage]=blob
            row['whole_bytes']=len(blob)-1;row['whole_sha256']=sha256(blob[:-1]).hexdigest()
        results.append(row)
        (work/'progress.json').write_bytes(canonical(results)+b'\n')
        print('passed',label,round(row['seconds'],3),flush=True)
    for source,prefix in ((HERE,'local'),(cold,'cold')):
        for stage in ('forcing','unit'):
            for optimized in (False,True):
                run(prefix+'-'+stage+('-O' if optimized else '-normal'),source,stage,optimized)
    damages={
      'keep_ninth':'WHOLE coupled mixed lower FIRST epsilon0to9',
      'omit_fifth_binomial':'WHOLE independent positive-branch physical scalar',
      'omit_pair_variance':'WHOLE independent positive-branch physical scalar',
      'reverse_skew_forcing':'ALL4 new mixed tenth ratio coefficient strictly negative',
      'missing_ninth':'ALL9 original root census',
      'omit_seventh':('ALL4 displayed complete mixed tenth terms','ALL4 active lower half normals zero'),
      'omit_ninth_center':('ALL4 displayed complete mixed tenth terms','ALL4 active lower half normals zero'),
      'omit_ninth_scale':('ALL4 displayed complete mixed tenth terms','ALL4 active lower half normals zero'),
      'wrong_cost_cross':'WHOLE coupled mixed lower FIRST epsilon0to9',
      'wrong_motion_winner':'WHOLE positive ideal winning norm',
      'outward_tenth':'WHOLE common tenth primitive column 10'}
    for damage,reject in damages.items():
        run('math-'+damage,cold,'unit' if damage=='outward_tenth' else 'forcing',
            damage=damage,reject=reject)
    original=json.loads((HERE/'EXPECTED.json').read_bytes())
    for label in ('extra-member','boolean-count','wrong-nested-stage','bad-digest','duplicate-member'):
        data=json.loads(canonical(original));path=work/(label+'-expected.json')
        if label=='extra-member':data['unexpected']=0;reject='exact expected members'
        elif label=='boolean-count':data['records']['forcing']['original_roots']=True;reject='integer original_roots'
        elif label=='wrong-nested-stage':data['records']['unit']['unexpected']=0;reject='exact expected stage members'
        elif label=='bad-digest':data['records']['forcing']['whole_sha256']='wrong';reject='SHA256 whole exact record'
        else:reject='duplicate JSON member'
        blob=canonical(data)+b'\n'
        if label=='duplicate-member':blob=blob.replace(b'{',b'{"schema":1,',1)
        path.write_bytes(blob)
        run('schema-'+label,cold,expected=path,reject=reject)
    damaged=work/'source-damage';damaged.mkdir()
    for name in FILES:shutil.copyfile(cold/name,damaged/name)
    with (damaged/'constants.py').open('a') as f:f.write('\nGmean=s.N1\n')
    run('source-pin',damaged,reject='whole pre-import source seal constants.py')
    bad=work/'sealed-bad-fixture';shutil.copytree(cold,bad)
    changed=json.loads((bad/'EXPECTED.json').read_bytes());changed['extra']=0
    (bad/'EXPECTED.json').write_bytes(canonical(changed)+b'\n');seal_expected(bad)
    run('sealed-fixture-schema',bad,reject='exact expected members')
    for name,raw in before.items():need((HERE/name).read_bytes()==raw,'source changed during validation '+name)
    result={'agent':'six-sendov-3','role':'researcher','status':'ordinary author replay controls, not independent review',
        'positive_replays':8,'mathematical_rejections':len(damages),'schema_rejections':6,'source_rejections':1,
        'all_entire_positive_records_and_source_bytes_compared_before_hash':True,
        'fixed_timeout_seconds':45,'one_serial_child':True,'native_threads':{key:1 for key in NATIVE},
        'maximum_child_seconds':max(r['seconds'] for r in results),
        'peak_child_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        'source_manifest_sha256':sha256(before['SOURCE.json']).hexdigest(),
        'results':results,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (work/'VALIDATION.json').write_bytes(canonical(result)+b'\n')
    print('complete',len(results),'controls; all complete records unchanged',flush=True)

if __name__=='__main__':main()
