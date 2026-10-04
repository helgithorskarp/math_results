"""Serial local/cold normal/optimized checks with a fixed45s guard per child.

Work records and all altered copies must remain outside this source directory.
Completed modes are resumable only against the same complete source fingerprint.
This is same-author validation, not independent review or formalization.
"""
from pathlib import Path
from hashlib import sha256
import argparse,datetime,json,os,shutil,subprocess,sys,time

HERE=Path(__file__).resolve().parent
STAGES=('algebra','lower_centers','literal','distance','roots',
        'real_center','imaginary_center','real_pair','imaginary_pair')
MODES=('local-n','local-o','cold-n','cold-o')
SEMANTIC=(('wrong_pair_compensation','literal','WHOLE'),
          ('omit_even_repair','literal','WHOLE'),
          ('omit_odd_center','roots','WHOLE'),
          ('wrong_radical_relation','distance','WHOLE'),
          ('wrong_fourth_binomial','distance','WHOLE'),
          ('missing_critical_slot','literal','CENSUS'),
          ('missing_ninth_original','roots','CENSUS'),
          ('wrong_skew_cubic','roots','WHOLE'),
          ('monomial_carry','algebra','NO monomial carry'),
          ('omit_lower_pair_cubic','lower_centers','WHOLE'),
          ('wrong_chi_payment','algebra','WHOLE'))
FIXTURES=('boolean_count','independent_review','formalization','universal_scope',
          'bad_stage_census','wrong_record_seal','own_proof_byte','parent_arithmetic_byte',
          'missing_source_manifest','duplicate_manifest_path','unlisted_critical_source')
PAUSE_FILES=[]
HANDOVER_FILES=[]


def need(test,message):
    if not test:raise RuntimeError(message)


def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()


def fingerprints():
    return {p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.iterdir())
            if p.is_file() and p.name not in ('SHA256SUMS','VALIDATION.json')}


def reseal(directory):
    (directory/'SHA256SUMS').write_text(''.join(
        sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n'
        for p in sorted(directory.iterdir()) if p.is_file() and p.name!='SHA256SUMS'))


def cold_copy(target):
    need(not target.exists(),'inspect existing cold copy before retry')
    source=target/'complex-profile-cap';parent=target/'optimal-cap-construction'
    source.mkdir(parents=True);parent.mkdir()
    for p in HERE.iterdir():
        if p.is_file():shutil.copyfile(p,source/p.name)
    deps=json.loads((HERE/'DEPENDENCIES.json').read_text())
    origin=(HERE/deps['parent_directory']).resolve()
    for name,digest in deps['parent_files'].items():
        data=(origin/name).read_bytes();need(sha256(data).hexdigest()==digest,'SOURCE parent before cold copy')
        (parent/name).write_bytes(data)
    return source


def fixture(source,name):
    p=source/'EXPECTED.json';value=json.loads(p.read_text())
    if name=='boolean_count':value['stages']['algebra']['identity_count']=True
    elif name=='independent_review':value['independent_review']=True
    elif name=='formalization':value['formalization']=True
    elif name=='universal_scope':value['scope']='arbitrary-polynomials'
    elif name=='bad_stage_census':del value['stages']['roots']
    elif name=='wrong_record_seal':value['stages']['algebra']['whole_record_sha256']='0'*64
    else:value=None
    if value is not None:
        p.write_text(json.dumps(value,indent=2)+'\n');reseal(source)
        return 'RECORD' if name=='wrong_record_seal' else 'TYPE'
    if name=='own_proof_byte':
        with (source/'PROOF.md').open('a') as stream:stream.write('\nbyte-control\n')
    elif name=='parent_arithmetic_byte':
        with (source.parent/'optimal-cap-construction/arithmetic.py').open('a') as stream:stream.write('\n# byte control\n')
    elif name=='missing_source_manifest':(source/'SHA256SUMS').unlink()
    elif name=='duplicate_manifest_path':
        lines=(source/'SHA256SUMS').read_text().splitlines()
        (source/'SHA256SUMS').write_text('\n'.join(lines+[lines[0]])+'\n')
    elif name=='unlisted_critical_source':
        lines=[v for v in (source/'SHA256SUMS').read_text().splitlines() if not v.endswith('  checks.py')]
        (source/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
    else:raise RuntimeError('unknown fixture')
    return 'SOURCE'


def child(work,source,tag,stage,optimized=False,control=None,marker=None):
    for path in PAUSE_FILES:need(not path.exists(),'OPERATIONS pause barrier; checkpoint and return')
    for path in HANDOVER_FILES:
        if path.exists():need(json.loads(path.read_text()).get('phase')=='completed','OPERATIONS incomplete handover; checkpoint and return')
    receipt=work/(tag+'.json');need(not receipt.exists(),'inspect prior child receipt before retry')
    flags=['-I']+(['-O'] if optimized else [])+['-B']
    command=[sys.executable,*flags,str(source/'verify.py'),'--stage',stage]
    if control:command+=['--control',control]
    env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[name]='1'
    t=time.monotonic();code=None;out='';err='';status='finished'
    try:
        process=subprocess.run(command,cwd=source.parent,env=env,capture_output=True,text=True,timeout=45)
        code,out,err=process.returncode,process.stdout,process.stderr
    except subprocess.TimeoutExpired as failure:
        status='fixed45s timeout; incomplete, no mathematical absence'
        out=failure.stdout.decode() if isinstance(failure.stdout,bytes) else (failure.stdout or '')
        err=failure.stderr.decode() if isinstance(failure.stderr,bytes) else (failure.stderr or '')
    record={'tag':tag,'stage':stage,'optimized':optimized,'control':control,'status':status,
            'returncode':code,'guard_seconds':45,'native_threads':1,'seconds':time.monotonic()-t,
            'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,
            'stdout':out,'stderr':err}
    receipt.write_text(json.dumps(record,indent=2)+'\n')
    need(status=='finished','operational limit; halt expensive work')
    if marker:
        need(code is not None and code!=0 and marker in err,'CONTROL intended mathematical/typed/source gate was not reached: '+tag)
        record['intended_rejection']=True;record['gate_marker']=marker
    else:
        need(code==0,'POSITIVE complete stage failed: '+tag)
        value=json.loads(out);record['compact']=value
    receipt.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ('stdout','stderr','command')}),flush=True)
    return record


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-root',required=True,type=Path)
    parser.add_argument('--mode',choices=(*MODES,'controls','seal'),required=True)
    parser.add_argument('--pause-file',action='append',type=Path,default=[])
    parser.add_argument('--handover-file',action='append',type=Path,default=[])
    args=parser.parse_args();work=args.work_root.resolve()
    PAUSE_FILES.extend(args.pause_file);HANDOVER_FILES.extend(args.handover_file)
    need(not work.is_relative_to(HERE),'SOURCE validation output must be outside source directory')
    work.mkdir(parents=True,exist_ok=True)
    pin=fingerprints();pin_hash=sha256(canonical(pin)).hexdigest()
    mode_path=work/(args.mode+'-complete.json')
    if args.mode=='seal':
        records={mode:json.loads((work/(mode+'-complete.json')).read_text()) for mode in (*MODES,'controls')}
        need(all(r['source_fingerprint']==pin_hash and r['complete'] is True for r in records.values()),'SOURCE stale or incomplete validation mode')
        need(all([r['stage'] for r in records[m]['rows']]==list(STAGES) for m in MODES),'CENSUS entire9-stage positive modes')
        expected=json.loads((HERE/'EXPECTED.json').read_text())
        positives=[]
        for mode in MODES:
            for r in records[mode]['rows']:
                v=r['compact'];target=expected['stages'][r['stage']]
                need(all(v[k]==target[k] for k in target),'RECORD all-mode full map seal differs')
                positives.append({'mode':mode,'stage':r['stage'],'seconds':r['seconds'],
                                  'peak_rss_kib':v['peak_rss_kib'],**target})
        rejects=[{'tag':r['tag'],'stage':r['stage'],'optimized':r['optimized'],
                  'gate_marker':r['gate_marker'],'seconds':r['seconds']} for r in records['controls']['rows']]
        need(len(rejects)==2*(len(SEMANTIC)+len(FIXTURES)),'CENSUS complete negative matrix')
        result={'agent':'six-sendov-3','role':'researcher','python':sys.version.split()[0],
                'formalization':False,'independent_review':False,'same_author_validation':True,
                'source_fingerprint':pin_hash,'source_files':pin,'native_threads':1,
                'max_cpu_intensive_children':1,'child_guard_seconds':45,
                'positive_modes':4,'positive_stage_jobs':len(positives),'negative_controls':len(rejects),
                'positives':positives,'rejections':rejects,
                'full_records_published':False,'ordinary_bridges':'uniform analytic remainders, simple-root implicit functions, strict containment and finite stability remain unformalized'}
        (HERE/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');reseal(HERE)
        print('SEALED complete4 positive modes and44 intended rejections; no mathematical child active.');return
    need(not mode_path.exists(),'inspect completed mode instead of repeating it')
    rows=[]
    def checkpoint(complete=False):
        value={'agent':'six-sendov-3','role':'researcher','mode':args.mode,'source_fingerprint':pin_hash,
               'complete':complete,'rows':rows,'active_jobs':[]}
        (work/(args.mode+'-checkpoint.json')).write_text(json.dumps(value,indent=2)+'\n')
        if complete:mode_path.write_text(json.dumps(value,indent=2)+'\n')
    if args.mode in MODES:
        source=cold_copy(work/(args.mode+'-copy')) if args.mode.startswith('cold') else HERE
        for stage in STAGES:
            rows.append(child(work,source,args.mode+'-'+stage,stage,args.mode.endswith('-o')));checkpoint()
    else:
        for optimized in (False,True):
            suffix='o' if optimized else 'n'
            for name,stage,marker in SEMANTIC:
                rows.append(child(work,HERE,'semantic-'+suffix+'-'+name,stage,optimized,name,marker));checkpoint()
            for name in FIXTURES:
                tag='fixture-'+suffix+'-'+name;source=cold_copy(work/(tag+'-copy'))
                marker=fixture(source,name)
                rows.append(child(work,source,tag,'algebra',optimized,marker=marker));checkpoint()
    need(pin==fingerprints(),'SOURCE source changed during validation')
    checkpoint(True)
    print('COMPLETE mode '+args.mode+'; all receipts saved outside source.',flush=True)


if __name__=='__main__':main()
