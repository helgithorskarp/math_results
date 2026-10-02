"""Cold exact replay: the balanced near-regular C3 E99 exclusion."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json,os,resource,subprocess,sys,time

HERE=Path(__file__).resolve().parent
SCHEMA_SCOPE='No valid ordinary redB4/blueB7 graph22 with red degree multiset8^3,9^16,10^3 and an automorphism of cycle type3^7 1.'

def strict_json(path):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ValueError('Duplicate JSON key')
            result[key]=value
        return result
    def constant(value):raise ValueError('Nonfinite JSON constant '+value)
    return json.loads(Path(path).read_text(),object_pairs_hook=unique,parse_constant=constant)

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)

def baseline():
    raw=(HERE/'primary21.rows').read_bytes();fixture=raw.decode().splitlines()
    if len(fixture)!=21 or any(len(row)!=21 or set(row)-{'0','1'} for row in fixture):raise ValueError('Binary primary21 schema')
    rows=[{j for j,value in enumerate(row) if value=='1'} for row in fixture]
    if any(i in row for i,row in enumerate(rows)):raise ValueError('Primary21 loop')
    if any((j in rows[i])!=(i in rows[j]) for i,j in combinations(range(21),2)):raise ValueError('Primary21 symmetry')
    red=[];blue=[]
    for i,j in combinations(range(21),2):
        if j in rows[i]:red.append(len(rows[i]&rows[j]))
        else:blue.append(sum(k not in rows[i] and k not in rows[j] for k in range(21) if k not in [i,j]))
    if len(red)!=93 or max(red)!=3 or max(blue)!=6:raise ValueError('Primary21 exact book caps')
    return dict(edges=93,max_red_pages=3,max_blue_pages=6,sha256=hashlib.sha256(raw).hexdigest())

def mathematical_summary(work,expected=None,check_frozen=True):
    work=Path(work)
    analytic=strict_json(work/'analytic.json')
    actual=dict(schema=1,scope=SCHEMA_SCOPE,primary21_sha256=baseline()['sha256'],analytic=analytic,by_mode={})
    for mode in ['AA','BB']:
        w=work/mode
        p=strict_json(w/'projection.json');pa=strict_json(w/'projection-audit.json')
        i=strict_json(w/'incidence-summary.json')
        a=strict_json(w/('audit-summary.json' if mode=='AA' else 'incidence-audit.json'))
        b=strict_json(w/'block-summary.json');d=strict_json(w/'direct-summary.json')
        statuses=['COMPLETE_EXACT_NECESSARY_A9_PROJECTION','COMPLETE_DISTINCT_MARKED_A_PROJECTION_AUDIT',
                  'COMPLETE_EXACT_A_INCIDENCE_PROJECTION' if mode=='AA' else 'COMPLETE_EXACT_BB_INCIDENCE_CENSUS',
                  'COMPLETE_INDEPENDENT_PROJECTION_AND_INCIDENCE_AUDIT' if mode=='AA' else 'COMPLETE_DIFFERENT_BB_PAIR_JOIN_AUDIT',
                  'COMPLETE_EXACT_NEAR_COMPONENT_PAGE_CENSUS','COMPLETE_LITERAL_NEAR_C3_CENSUS']
        if [s['status'] for s in [p,pa,i,a,b,d]]!=statuses:raise ValueError('Incomplete mathematical phase')
        if p['mode']!=mode or pa['mode']!=mode or b['mode']!=mode or p['H_edges']!=12:raise ValueError('Marked mode schema')
        if p['global_A_degrees']!=([8]*3+[9]*3+[10]*3 if mode=='AA' else [9]*9):raise ValueError('A degree marks')
        for flag in ['whole_survivor_set_equal','whole_transport_groups_equal','whole_semantic_fields_equal']:
            if pa[flag] is not True:raise ValueError('Projection equality not verified')
        for flag in (['entire_local_sets_equal','entire_transport_groups_equal','entire_incidence_sets_equal'] if mode=='AA' else ['whole_typed_column_domains_equal','whole_typed_incidence_sets_equal','whole_native_input_equal']):
            if a[flag] is not True:raise ValueError('Incidence equality not verified')
        for left,right in [('block-K-words.txt','direct-K-words.txt'),('block-outcomes.txt','direct-outcomes.txt')]:
            if (w/left).read_bytes()!=(w/right).read_bytes():raise ValueError('Entire component/native stream differs')
        word_bytes=(w/'direct-K-words.txt').read_bytes();words=[int(v) for v in word_bytes.splitlines()]
        if len(words)!=d['K_local_cap_words'] or any(not 0<=v<2**22 for v in words) or words!=sorted(set(words)):
            raise ValueError('Entire K stream domain/order')
        outcomes=(w/'direct-outcomes.txt').read_bytes()
        if len(outcomes)!=d['completion_choices'] or set(outcomes)-{ord('0'),ord('1')}:raise ValueError('Complete typed outcome stream')
        if outcomes.count(ord('1'))!=d['valid'] or d['valid']!=b['counts']['valid']:raise ValueError('Outcome/valid count')
        if d['red_rejected']+d['blue_rejected']+d['valid']!=d['completion_choices']:raise ValueError('Whole literal count')
        if [len(r['valid_K_words']) for r in b['by_frame']]!=d['per_frame_valid']:raise ValueError('Whole per-frame outcomes')
        for key in ['completion_choices','valid','K_degree_words','K_local_cap_words']:
            if b['counts'][key]!=d[key]:raise ValueError('Whole block/native semantic fields')
        frames=strict_json(w/'frames.json')
        if len(frames)!=d['frames'] or d['completion_choices']!=len(frames)*len(words):raise ValueError('Complete frame product')
        actual['by_mode'][mode]=dict(projection_counts=p['counts'],A_groups={k:sorted(v) for k,v in p['canonical_groups'].items()},
                    allowed_A_orbit_permutations=p['allowed_A_orbit_permutations'],projection_audit_counts=pa['counts'],
                    projection_audit_groups=pa['groups'],incidence_counts=i['counts'],incidence_by_word=i['by_word'],
                    incidence_audit_by_word=a['by_word'],frames=frames,frames_sha256=hashlib.sha256((w/'frames.txt').read_bytes()).hexdigest(),
                    block_counts=b['counts'],direct={k:v for k,v in d.items() if k!='seconds'},
                    K_stream_sha256=hashlib.sha256(word_bytes).hexdigest(),outcome_stream_sha256=hashlib.sha256(outcomes).hexdigest())
    if check_frozen:
        if expected is None:expected=strict_json(HERE/'EXPECTED.json')
        if canonical(actual)!=canonical(expected):raise ValueError('Whole typed frozen mathematical record differs')
    return actual

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);parser.add_argument('--optimized',action='store_true')
    args=parser.parse_args();work=args.work.resolve()
    if work==HERE or HERE in work.parents:raise ValueError('Generated work outside public source')
    if work.exists() and any(work.iterdir()):raise ValueError('Use an EMPTY work directory')
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    expected=strict_json(HERE/'EXPECTED.json');control=baseline()
    if control['sha256']!=expected['primary21_sha256']:raise ValueError('Frozen primary fixture')
    environment=os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:environment[key]='1'
    python=[sys.executable]+(['-O'] if args.optimized else [])
    commands=[python+[str(HERE/'analytic.py'),'--work',str(work)],
              ['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow',str(HERE/'direct.cpp'),'-o',str(work/'direct')]]
    for mode in ['AA','BB']:
        w=work/mode;w.mkdir()
        commands += [python+[str(HERE/'projection.py'),'--mode',mode,'--work',str(w)],
                     python+[str(HERE/'projection_audit.py'),'--mode',mode,'--work',str(w)],
                     python+[str(HERE/('incidences_'+mode.lower()+'.py')),'--work',str(w)],
                     python+[str(HERE/('audit_'+mode.lower()+'.py')),'--work',str(w)],
                     python+[str(HERE/'block.py'),'--mode',mode,'--work',str(w)],
                     [str(work/'direct'),str(w/'frames.txt'),str(w),mode]]
    for index,command in enumerate(commands):
        result=subprocess.run(command,env=environment,capture_output=True,text=True,timeout=30)
        (work/('phase-'+str(index)+'.stdout')).write_text(result.stdout)
        (work/('phase-'+str(index)+'.stderr')).write_text(result.stderr)
        result.check_returncode()
        if index==1 and result.stderr:raise ValueError('Compiler warnings')
    mathematical=mathematical_summary(work,expected)
    (work/'mathematical-summary.json').write_text(json.dumps(mathematical,sort_keys=True,indent=2)+'\n')
    report=dict(status='COMPLETE_COLD_NEAR_REGULAR_C3_REPLAY',seconds=time.monotonic()-start,
                primary21=control,optimized_python=args.optimized,threads=1,child_guard_seconds=30,soft_phase_seconds=25,
                completion_choices=sum(v['direct']['completion_choices'] for v in mathematical['by_mode'].values()),
                valid_choices=sum(v['direct']['valid'] for v in mathematical['by_mode'].values()),
                peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,python=sys.version.split()[0],
                mathematical_summary_sha256=hashlib.sha256((work/'mathematical-summary.json').read_bytes()).hexdigest(),
                source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.iterdir() if p.is_file()},
                trust='Same-author distinct set/load-DP/orbit-expansion, nested/keyed column, weighted-mask/native-word and component/literal methods. Ordinary completeness/relabeling/code bridges unformalized; independent peer review pending.')
    (work/'replay-summary.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='source_hashes'},indent=2))

if __name__=='__main__':main()
