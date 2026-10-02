"""Fresh serial P2 replay; full typed coverage, stream equality, source seal."""
from argparse import ArgumentParser
from pathlib import Path
import hashlib,json,os,resource,shutil,subprocess,sys,time
from cases import CASES
ORDINARY_CASES={'P2_8810_A3','P2_8810_A4'}
SEARCH_CASES=('P2_8910','P2_8910_J','P2_81010')

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'

def stable(value):
    if isinstance(value,dict):
        return {k:stable(v) for k,v in value.items() if k not in ['seconds','peak_rss_kib']}
    if isinstance(value,list):
        return [stable(v) for v in value]
    return value

def compare_streams(case,stem,left,right):
    a=Path(left).read_bytes();b=Path(right).read_bytes()
    if a!=b:
        raise ValueError('Entire '+case+' '+stem+' streams differ')
    return dict(bytes=len(a),sha256=hashlib.sha256(a).hexdigest(),whole_equal=True)

def verify_record(actual,expected):
    if canonical(stable(actual))!=canonical(stable(expected)):
        raise ValueError('Whole frozen mathematical record differs')

def verify_sources(root):
    seal=root/'SOURCE.json'
    if not seal.exists():
        return False
    for name,record in json.loads(seal.read_text())['files'].items():
        if Path(name).name!=name:
            raise ValueError('Source seal filename domain')
        raw=(root/name).read_bytes()
        if len(raw)!=record['bytes'] or hashlib.sha256(raw).hexdigest()!=record['sha256']:
            raise ValueError('Frozen source bytes differ: '+name)
    return True

def validate_replay(records):
    baseline=dict(vertices=21,edges=93,max_red_pages=3,max_blue_pages=6,spines=210)
    if canonical(records['primary_native'])!=canonical(baseline) or canonical(records['identity-controls']['primary21'])!=canonical(baseline):
        raise ValueError('Literal/set primary control record')
    if records['capacity-audit']['status']!='COMPLETE_DISTINCT_P2_ROOT_CAPACITY_AUDIT' or records['capacity-audit']['whole_typed_root_table_equal'] is not True:
        raise ValueError('Incomplete ordinary root-capacity bridge')
    if set(records['patterns'])!=set(SEARCH_CASES) or {c['case'] for c in records['root-capacity']['residual']}!=set(CASES):
        raise ValueError('Entire marked case coverage')
    cut=records['ordinary-cut']
    if cut['status']!='COMPLETE_ORDINARY_P2_8810_SUMMED_GRAM_CUT' or set(cut['cases'])!=ORDINARY_CASES or ORDINARY_CASES|set(SEARCH_CASES)!=set(CASES) or ORDINARY_CASES&set(SEARCH_CASES):
        raise ValueError('Entire ordinary/search case partition')
    if any(type(cut[k]) is not int for k in ['weighted_load_total','weighted_load_lower','maximum_full_Gram_upper','gap']):
        raise ValueError('Typed ordinary cut integers')
    if [cut[k] for k in ['weighted_load_total','weighted_load_lower','maximum_full_Gram_upper','gap']]!=[24,87,84,3] or cut['weighted_load_lower']-cut['maximum_full_Gram_upper']!=cut['gap']:
        raise ValueError('Exact ordinary summed-row gap')
    if cut['counts']!=dict(all_binary_H=4096,H12=495,H12_max_degree3=174,capacity_at_least63=58,high_triangle_forbidden=4,high_independent=54) or len(cut['literal_records'])!=54:
        raise ValueError('Complete ordinary cut literal coverage')
    for r in cut['literal_records']:
        if len(r['literal_full_upper_rows'])!=6 or sum(r['literal_full_upper_rows'])!=84 or r['sum_upper']!=84 or r['weighted_column_lower']!=87 or r['low_to_high']!=6:
            raise ValueError('Entire ordinary full-row records')
    if set(records['projections'])!={'P2_81010','P2_8910'}:
        raise ValueError('Entire root projection coverage')
    for case,record in records['patterns'].items():
        C=CASES[case];literal=record['literal'];cached=record['cached'];counts=cached['counts']
        if literal['status']!='COMPLETE_LITERAL_E102_MARKED_C3_CENSUS' or cached['status']!='COMPLETE_EXACT_CACHED_E102_COMPONENT_CENSUS' or literal['case']!=case or cached['mode']!=case:
            raise ValueError('Incomplete/scoped census status')
        beta=[d-a for d,a in zip(C['B'],C['alpha'])]
        if canonical([literal['A_orbits'],literal['B_orbits'],literal['column_sizes'],literal['B_degree_orbits']])!=canonical([C['A'],C['B'],C['alpha'],beta]):
            raise ValueError('Literal whole declared degree/column marks')
        if canonical([cached['column_sizes'],cached['B_degree_orbits']])!=canonical([C['alpha'],beta]):
            raise ValueError('Component whole declared degree/column marks')
        frames=record['incidence_audit']['frames']
        if not frames==record['incidence']['frames']==literal['frames']==cached['frames']==len(literal['per_frame_valid'])==len(cached['B_pair_counts']):
            raise ValueError('Whole frame coverage')
        if frames!=record['incidence']['counts']['A_pair_matches']:
            raise ValueError('Entire incidence coverage')
        for field in ['K_degree_words','K_local_cap_words','completion_choices','valid']:
            if field not in literal or field not in counts:
                raise ValueError('Missing exact completion counter')
            if type(literal[field]) is not int or type(counts[field]) is not int:
                raise ValueError('Typed exact census integer')
            if literal[field]!=counts[field]:
                raise ValueError('Entire domain/outcome count '+field)
        if literal['K_words_checked']!=4194304:
            raise ValueError('Full binary K domain')
        choices=frames*literal['K_local_cap_words']
        if choices!=literal['completion_choices'] or choices!=record['whole_streams']['outcomes']['bytes']:
            raise ValueError('Whole completion coverage')
        if choices!=literal['red_rejected']+literal['blue_rejected']+literal['valid']:
            raise ValueError('Entire literal verdict partition')
        if literal['valid'] or sum(literal['per_frame_valid']) or cached['valid']:
            raise ValueError('A valid graph refutes the candidate; preserve outputs')

def main():
    p=ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args()
    root=Path(__file__).resolve().parent;sealed=verify_sources(root);work=args.work.resolve()
    if work.exists() and any(work.iterdir()):
        raise ValueError('Use a fresh work directory; previous stages are preserved')
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic();stage='initial';records={}
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',
             VECLIB_MAXIMUM_THREADS='1',BLIS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    python=[sys.executable]+(['-O'] if sys.flags.optimize else [])
    def run(name,command):
        nonlocal stage
        stage=name;t=time.monotonic()
        result=subprocess.run(list(map(str,command)),env=env,capture_output=True,text=True,timeout=30)
        (work/(name+'.stdout')).write_text(result.stdout);(work/(name+'.stderr')).write_text(result.stderr)
        if result.returncode:
            raise RuntimeError('INCOMPLETE/FAILED '+name+'; no mathematical verdict')
        print(name,'PASS',round(time.monotonic()-t,3),'seconds',flush=True)
    def script(name,file,*argv):
        run(name,python+[root/file,*argv])
    def load(directory,name):
        return json.loads((directory/name).read_text())
    try:
        run('compile',['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic',root/'direct.cpp','-o',work/'direct'])
        run('page-native',[work/'direct','--page-controls']);records['page_native']=load(work,'page-native.stdout')
        run('primary-native',[work/'direct','--fixture21',root/'primary21.rows']);records['primary_native']=load(work,'primary-native.stdout')
        directory=work/'identity-controls';script('identity-controls','identity_controls.py','--work',directory)
        records['identity-controls']=load(directory,'identity-controls.json')
        directory=work/'root-cuts'
        script('root-capacity','root_capacity.py','--work',directory)
        script('capacity-audit','capacity_audit.py','--work',directory)
        records['root-capacity']=load(directory,'root-capacity.json');records['capacity-audit']=load(directory,'capacity-audit.json')
        records['projections']={}
        directory=work/'ordinary-cut'
        script('ordinary-cut','ordinary_cut.py','--work',directory)
        records['ordinary-cut']=load(directory,'ordinary-cut.json')
        for mode in ['P2_81010','P2_8910']:
            directory=work/mode
            script(mode+'-projection','projection.py','--work',directory,'--mode',mode)
            script(mode+'-projection-audit','projection_audit.py','--work',directory,'--mode',mode)
            primary=load(directory,'projection.json');primary.pop('records')
            records['projections'][mode]=dict(primary=primary,audit=load(directory,'projection-audit.json'))
        records['patterns']={}
        for case in SEARCH_CASES:
            C=CASES[case]
            directory=work/case;directory.mkdir(parents=True,exist_ok=True)
            original=work/C['projection']
            if original!=directory:
                for name in ['projection.json','projection-audit.json']:
                    shutil.copyfile(original/name,directory/name)
            script(case+'-incidence','marked_incidences.py','--work',directory,'--case',case)
            script(case+'-incidence-audit','marked_incidence_audit.py','--work',directory,'--case',case)
            script(case+'-cached','block_cached.py','--work',directory,'--mode',case)
            frames=load(directory,'frames.json')
            run(case+'-native',[work/'direct',directory/'frames.txt',directory,case,len(frames)])
            streams={stem:compare_streams(case,stem,directory/('cached-'+stem+'.txt'),directory/('direct-'+stem+'.txt')) for stem in ['K-words','outcomes']}
            cached=load(directory,'cached-summary.json');cached['B_pair_counts']=[v['B_pair_survivors'] for v in cached.pop('by_frame')]
            records['patterns'][case]=dict(incidence=load(directory,'incidence-summary.json'),incidence_audit=load(directory,'incidence-audit.json'),
                                           cached=cached,literal=load(directory,'direct-summary.json'),whole_streams=streams)
        validate_replay(records)
        (work/'PRE-CONTROLS.json').write_text(canonical(stable(records)))
        script('corruption-controls','corruption_controls.py','--source-work',work,'--work',work/'corruption-controls')
        records['corruption-controls']=load(work/'corruption-controls','controls.json')
        raw=canonical(stable(records));(work/'MATHEMATICAL.json').write_text(raw)
        expected=root/'EXPECTED.json';status='UNSEALED_CANDIDATE_REPLAY_COMPLETE'
        if expected.exists():
            verify_record(records,json.loads(expected.read_text()));status='REPRODUCTION_PASS'
        receipt=dict(status=status,agent='six-books-2',role='researcher',mathematical_bytes=len(raw.encode()),
                     mathematical_sha256=hashlib.sha256(raw.encode()).hexdigest(),seconds=time.monotonic()-start,
                     peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,threads=1,intensive_children='serial',
                     program_guard_seconds=25,child_guard_seconds=30,frozen_source_verified=sealed,
                     corruption_controls=records['corruption-controls']['damage_rejections'],
                     trust='Written ordinary/completeness bridges unformalized; new independent review pending.')
        (work/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2),flush=True)
    except BaseException as exc:
        (work/'INCOMPLETE.json').write_text(json.dumps(dict(status='INCOMPLETE_NO_VERDICT',stage=stage,exception=type(exc).__name__,
            message=str(exc),seconds=time.monotonic()-start,guard_unchanged=True,automatic_retry=False),indent=2)+'\n')
        raise

if __name__=='__main__':
    main()
