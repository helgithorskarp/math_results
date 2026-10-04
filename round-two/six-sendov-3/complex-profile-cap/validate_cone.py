"""Serial bounded checks for the complex-cone addition to a frozen profile suite.

No base mathematical file is modified or rechecked by this addition. The
base329 whole-map suite remains recorded separately in VALIDATION.json.
Run with an external work directory; all generated copies stay there.
"""
from pathlib import Path
from hashlib import sha256
import argparse,datetime,json,os,subprocess,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate as base
HERE=Path(__file__).resolve().parent
SEMANTIC=('wrong_row','wrong_ray','wrong_norm','wrong_dual','missing_ray','wrong_sine_ratio')
FIXTURES=('boolean_count','review_status','universal_scope','missing_count','wrong_seal',
          'unlisted_cone','proof_byte','parent_byte')


def pin():
    return {p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.iterdir())
        if p.is_file() and p.name not in ('SHA256SUMS','VALIDATION_SUPPLEMENT.json')}


def run(work,source,tag,opt=False,control=None,marker=None,source_only=False):
    for p in base.PAUSE_FILES:base.need(not p.exists(),'OPERATIONS pause barrier')
    for p in base.HANDOVER_FILES:
        if p.exists():base.need(json.loads(p.read_text()).get('phase')=='completed','OPERATIONS incomplete handover')
    target=work/(tag+'.json');base.need(not target.exists(),'inspect prior receipt before retry')
    flags=['-I']+(['-O'] if opt else [])+['-B']
    command=[sys.executable,*flags,str(source/('verify.py' if source_only else 'cone.py'))]
    if source_only:command+=['--source-only']
    if control:command+=['--control',control]
    env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[name]='1'
    start=time.monotonic();status='finished';code=None;out='';err=''
    try:
        p=subprocess.run(command,cwd=source.parent,env=env,capture_output=True,text=True,timeout=45)
        code,out,err=p.returncode,p.stdout,p.stderr
    except subprocess.TimeoutExpired as failure:
        status='fixed45s timeout; incomplete, no mathematical absence'
        out=failure.stdout.decode() if isinstance(failure.stdout,bytes) else (failure.stdout or '')
        err=failure.stderr.decode() if isinstance(failure.stderr,bytes) else (failure.stderr or '')
    row={'tag':tag,'optimized':opt,'status':status,'returncode':code,'seconds':time.monotonic()-start,
         'guard_seconds':45,'native_threads':1,'command':command,'stdout':out,'stderr':err}
    target.write_text(json.dumps(row,indent=2)+'\n')
    base.need(status=='finished','operational limit; checkpoint and return')
    if marker:
        base.need(code is not None and code!=0 and marker in err,'CONTROL intended gate '+tag)
        row['intended_rejection']=True;row['gate_marker']=marker
    else:
        base.need(code==0 and not err,'POSITIVE complete cone/source check '+tag)
        row['compact']=json.loads(out)
    target.write_text(json.dumps(row,indent=2)+'\n')
    print(json.dumps({k:v for k,v in row.items() if k not in ('command','stdout','stderr')}),flush=True)
    return row


def fixture(source,name):
    target=source/'CONE.json';v=json.loads(target.read_text());marker='TYPE'
    if name=='boolean_count':v['identity_count']=True
    elif name=='review_status':v['independent_review']=True
    elif name=='universal_scope':v['scope']='all-disk-rooted-polynomials'
    elif name=='missing_count':del v['sign_count']
    elif name=='wrong_seal':v['whole_record_sha256']='0'*64;marker='RECORD'
    else:v=None;marker='SOURCE'
    if v is not None:target.write_text(json.dumps(v,indent=2)+'\n');base.reseal(source)
    elif name=='unlisted_cone':
        m=source/'SHA256SUMS';m.write_text(''.join(line+'\n' for line in m.read_text().splitlines() if not line.endswith('  cone.py')))
    elif name=='proof_byte':
        with (source/'CONE_PROOF.md').open('a') as f:f.write('\nbyte-control\n')
    elif name=='parent_byte':
        with (source.parent/'optimal-cap-construction/arithmetic.py').open('a') as f:f.write('\n# byte-control\n')
    else:raise RuntimeError('unknown fixture')
    return marker


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-root',required=True,type=Path)
    parser.add_argument('--phase',required=True,choices=('checks','seal','source'))
    parser.add_argument('--pause-file',action='append',type=Path,default=[])
    parser.add_argument('--handover-file',action='append',type=Path,default=[])
    args=parser.parse_args();work=args.work_root.resolve();work.mkdir(parents=True,exist_ok=True)
    base.need(not work.is_relative_to(HERE),'SOURCE external validation workspace')
    base.PAUSE_FILES.extend(args.pause_file);base.HANDOVER_FILES.extend(args.handover_file)
    current=pin();fingerprint=sha256(base.canonical(current)).hexdigest()
    frozen=json.loads((HERE/'VALIDATION.json').read_text())
    critical={name:old for name,old in frozen['source_files'].items()
              if name.endswith('.py') or name in ('EXPECTED.json','DEPENDENCIES.json')}
    base.need(all(current.get(n)==d for n,d in critical.items()),'SOURCE frozen329-map runtime/data files changed')
    additions={n:d for n,d in current.items() if n not in frozen['source_files']}
    amendments={n:{'frozen_sha256':old,'current_sha256':current.get(n)}
                for n,old in frozen['source_files'].items() if current.get(n)!=old}
    if args.phase=='seal':
        completed=json.loads((work/'complete.json').read_text())
        base.need(completed['complete'] is True and completed['source_fingerprint']==fingerprint,'SOURCE incomplete/stale cone checks')
        rows=completed['rows'];positives=[r for r in rows if 'compact' in r];rejects=[r for r in rows if r.get('intended_rejection')]
        base.need(len(positives)==4 and len(rejects)==28,'CENSUS complete cone matrix')
        result={'agent':'six-sendov-3','role':'researcher','formalization':False,'independent_review':False,
            'same_author_validation':True,'python':sys.version.split()[0],
            'source_fingerprint_excluding_self_and_manifest':fingerprint,'source_files_excluding_self_and_manifest':current,
            'frozen_base_source_fingerprint':frozen['source_fingerprint'],
            'frozen_base_positive_stage_jobs':36,'frozen_base_negative_controls':44,
            'unchanged_base_runtime_and_data_files':critical,'written_metadata_amendments':amendments,
            'new_files':additions,'cone_positive_modes':4,'cone_negative_controls':28,
            'positives':[{'tag':r['tag'],'seconds':r['seconds'],**r['compact']} for r in positives],
            'rejections':[{'tag':r['tag'],'seconds':r['seconds'],'gate_marker':r['gate_marker']} for r in rejects],
            'native_threads':1,'max_cpu_intensive_children':1,'child_guard_seconds':45,
            'no_base_math_replay_claim_for_amended_docs':True,
            'ordinary_unformalized_bridges':'cone/equality completeness, analytic uniformity, actual all9 containment, weighted15Dcap and finite stability',
            'source_only_phase':'Run after seal in local/cold normal/O; external receipts do not enter this self-referential record.'}
        (HERE/'VALIDATION_SUPPLEMENT.json').write_text(json.dumps(result,indent=2)+'\n');base.reseal(HERE)
        print('SEALED four whole-cone modes and28 intended controls; frozen329-map math unchanged.');return
    rows=[]
    def checkpoint(complete=False):
        value={'agent':'six-sendov-3','role':'researcher','source_fingerprint':fingerprint,'complete':complete,'rows':rows,'active_jobs':[]}
        (work/(('source' if args.phase=='source' else 'checks')+'-checkpoint.json')).write_text(json.dumps(value,indent=2)+'\n')
        if complete:(work/('source-complete.json' if args.phase=='source' else 'complete.json')).write_text(json.dumps(value,indent=2)+'\n')
    for cold,opt,mode in ((False,False,'local-n'),(False,True,'local-o'),(True,False,'cold-n'),(True,True,'cold-o')):
        tag=('final-source-' if args.phase=='source' else 'cone-')+mode
        source=base.cold_copy(work/(tag+'-copy')) if cold else HERE
        rows.append(run(work,source,tag,opt,source_only=args.phase=='source'));checkpoint()
    if args.phase=='checks':
        for opt in (False,True):
            suffix='o' if opt else 'n'
            for name in SEMANTIC:
                tag='cone-semantic-'+suffix+'-'+name
                rows.append(run(work,HERE,tag,opt,name,'CENSUS' if name=='missing_ray' else 'WHOLE'));checkpoint()
            for name in FIXTURES:
                tag='cone-fixture-'+suffix+'-'+name;source=base.cold_copy(work/(tag+'-copy'))
                rows.append(run(work,source,tag,opt,marker=fixture(source,name)));checkpoint()
    base.need(current==pin(),'SOURCE changed during cone validation')
    checkpoint(True);print('COMPLETE '+args.phase+'; no mathematical child active.')


if __name__=='__main__':main()
