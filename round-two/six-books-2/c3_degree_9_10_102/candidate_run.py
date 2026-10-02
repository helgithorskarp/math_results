"""Serial exact candidate replay; preserve partial stages and fail on incompleteness."""
from argparse import ArgumentParser
from pathlib import Path
import hashlib,json,os,resource,subprocess,sys,time

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'

def stable(value):
    if isinstance(value,dict):return {k:stable(v) for k,v in value.items() if k not in ['seconds','peak_rss_kib']}
    if isinstance(value,list):return [stable(v) for v in value]
    return value

def compare_streams(mode,stem,left,right):
    a=Path(left).read_bytes();b=Path(right).read_bytes()
    if a!=b:raise ValueError('Entire '+mode+' '+stem+' streams differ')
    return dict(bytes=len(a),sha256=hashlib.sha256(a).hexdigest(),whole_equal=True)

def verify_record(actual,expected):
    if canonical(stable(actual))!=canonical(stable(expected)):
        raise ValueError('Whole frozen mathematical record differs')

def verify_sources(root):
    seal=root/'SOURCE.json'
    if not seal.exists():return False
    for name,record in json.loads(seal.read_text())['files'].items():
        if Path(name).name!=name:raise ValueError('Source seal filename domain')
        raw=(root/name).read_bytes()
        if len(raw)!=record['bytes'] or hashlib.sha256(raw).hexdigest()!=record['sha256']:
            raise ValueError('Frozen source bytes differ: '+name)
    return True

def validate_replay(records):
    baseline=dict(vertices=21,edges=93,max_red_pages=3,max_blue_pages=6,spines=210)
    if canonical(records['primary_native'])!=canonical(baseline):raise ValueError('Literal primary control record')
    if canonical(records['identity-controls']['primary21'])!=canonical(baseline):raise ValueError('Set primary control record')
    if set(records['patterns'])!={'A9910','G7','GM','G6'}:raise ValueError('Entire marked case coverage')
    for mode,record in records['patterns'].items():
        literal=record['literal'];cached=record['cached'];counts=cached['counts']
        if literal['status']!='COMPLETE_LITERAL_E102_MARKED_C3_CENSUS' or cached['status']!='COMPLETE_EXACT_CACHED_E102_COMPONENT_CENSUS':
            raise ValueError('Incomplete census status')
        frames=record['incidence_audit']['frames']
        if not frames==literal['frames']==cached['frames']==len(literal['per_frame_valid'])==len(cached['B_pair_counts']):
            raise ValueError('Whole frame coverage')
        if frames!=record['incidence']['counts']['A_pair_matches']:raise ValueError('Entire incidence coverage')
        for field in ['K_degree_words','K_local_cap_words','completion_choices','valid']:
            if literal[field]!=counts[field]:raise ValueError('Entire domain/outcome count '+field)
        if literal['K_words_checked']!=4194304:raise ValueError('Full binary K domain')
        choices=frames*literal['K_local_cap_words']
        if choices!=literal['completion_choices'] or choices!=record['whole_streams']['outcomes']['bytes']:
            raise ValueError('Whole completion coverage')
        if choices!=literal['red_rejected']+literal['blue_rejected']+literal['valid']:
            raise ValueError('Entire literal verdict partition')
        if literal['valid'] or sum(literal['per_frame_valid']) or cached['valid']:
            raise ValueError('A valid graph refutes the candidate; preserve outputs')

def main():
    p=ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args()
    root=Path(__file__).resolve().parent;source_sealed=verify_sources(root);work=args.work.resolve()
    if work.exists() and any(work.iterdir()):raise ValueError('Use a fresh work directory; previous stages are preserved')
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic();stage='initial';records={}
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',
             VECLIB_MAXIMUM_THREADS='1',BLIS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    python=[sys.executable]+(['-O'] if sys.flags.optimize else [])
    def run(name,command):
        nonlocal stage
        stage=name;t=time.monotonic()
        r=subprocess.run(command,env=env,capture_output=True,text=True,timeout=30)
        (work/(name+'.stdout')).write_text(r.stdout);(work/(name+'.stderr')).write_text(r.stderr)
        if r.returncode:raise RuntimeError('INCOMPLETE/FAILED '+name+'; no mathematical verdict')
        print(name,'PASS',round(time.monotonic()-t,3),'seconds',flush=True)
    def script(name,file,*argv):run(name,python+[str(root/file),*map(str,argv)])
    def load(directory,file):return json.loads((directory/file).read_text())
    try:
        run('compile',['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic',str(root/'direct.cpp'),'-o',str(work/'direct')])
        run('page-native',[str(work/'direct'),'--page-controls'])
        records['page_native']=json.loads((work/'page-native.stdout').read_text())
        run('primary-native',[str(work/'direct'),'--fixture21',str(root/'primary21.rows')])
        records['primary_native']=json.loads((work/'primary-native.stdout').read_text())
        for name,file,result in [('analytic','analytic.py','analytic.json'),('low-profile','low_profile.py','low-profile.json'),
                                 ('seven-nine-profile','seven_nine_profile.py','seven-nine-profile.json'),
                                 ('identity-controls','identity_controls.py','identity-controls.json')]:
            directory=work/name
            script(name,file,'--work',directory);records[name]=load(directory,result)
        records['projections']={}
        for mode in ['A9910','A999']:
            directory=work/mode
            script(mode+'-projection','projection.py','--work',directory,'--mode',mode)
            script(mode+'-projection-audit','projection_audit.py','--work',directory,'--mode',mode)
            record=load(directory,'projection.json');record.pop('records')
            records['projections'][mode]=dict(primary=record,audit=load(directory,'projection-audit.json'))
        records['patterns']={}
        for mode in ['A9910','G7','GM','G6']:
            directory=work/mode
            if mode=='A9910':
                script(mode+'-incidence','incidences.py','--work',directory)
                script(mode+'-incidence-audit','incidence_audit.py','--work',directory)
            else:
                script(mode+'-incidence','all9_incidences.py','--projection',work/'A999','--work',directory,'--mode',mode)
                script(mode+'-incidence-audit','all9_incidence_audit.py','--projection',work/'A999','--work',directory,'--mode',mode)
            script(mode+'-cached','block_cached.py','--work',directory,'--mode',mode)
            frames=load(directory,'frames.json')
            run(mode+'-native',[str(work/'direct'),str(directory/'frames.txt'),str(directory),mode,str(len(frames))])
            equal={}
            for stem in ['K-words','outcomes']:
                equal[stem]=compare_streams(mode,stem,directory/('cached-'+stem+'.txt'),directory/('direct-'+stem+'.txt'))
            cached=load(directory,'cached-summary.json')
            cached['B_pair_counts']=[r['B_pair_survivors'] for r in cached.pop('by_frame')]
            direct=load(directory,'direct-summary.json')
            if cached['counts']['valid'] or direct['valid']:raise ValueError('A valid graph refutes the candidate; preserve outputs')
            records['patterns'][mode]=dict(incidence=load(directory,'incidence-summary.json'),
                                           incidence_audit=load(directory,'incidence-audit.json'),
                                           cached=cached,literal=direct,whole_streams=equal)
        validate_replay(records)
        (work/'PRE-CONTROLS.json').write_text(canonical(stable(records)))
        script('corruption-controls','corruption_controls.py','--source-work',work,'--work',work/'corruption-controls')
        records['corruption-controls']=load(work/'corruption-controls','controls.json')
        raw=canonical(stable(records));(work/'MATHEMATICAL.json').write_text(raw)
        expected=root/'EXPECTED.json';status='UNSEALED_CANDIDATE_REPLAY_COMPLETE'
        if expected.exists():
            verify_record(records,json.loads(expected.read_text()))
            status='REPRODUCTION_PASS'
        receipt=dict(status=status,agent='six-books-2',role='researcher',mathematical_bytes=len(raw.encode()),
                     mathematical_sha256=hashlib.sha256(raw.encode()).hexdigest(),seconds=time.monotonic()-start,
                     peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                     intensive_children='serial',threads=1,program_guard_seconds=25,child_guard_seconds=30,
                     frozen_source_verified=source_sealed,
                     corruption_controls=records['corruption-controls']['damage_rejections'],trust='Ordinary/code completeness bridges unformalized; independent review pending.')
        (work/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2),flush=True)
    except BaseException as exc:
        (work/'INCOMPLETE.json').write_text(json.dumps(dict(status='INCOMPLETE_NO_VERDICT',stage=stage,
            exception=type(exc).__name__,message=str(exc),seconds=time.monotonic()-start,
            guard_unchanged=True,automatic_retry=False),indent=2)+'\n')
        raise

if __name__=='__main__':main()
