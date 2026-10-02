"""Cold exact replay of the nine-regular C3 type3^7 1 exclusion."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json,os,resource,subprocess,sys,time

HERE=Path(__file__).resolve().parent

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
    raw=(HERE/'primary21.rows').read_bytes()
    fixture=raw.decode().splitlines()
    if len(fixture)!=21 or any(len(row)!=21 or set(row)-{'0','1'} for row in fixture):raise ValueError('Binary primary21 row schema')
    rows=[{j for j,value in enumerate(row) if value=='1'} for row in fixture]
    if any(i in row for i,row in enumerate(rows)):raise ValueError('Primary21 loop')
    if any((j in rows[i])!=(i in rows[j]) for i,j in combinations(range(21),2)):raise ValueError('Primary21 symmetry')
    red=[];blue=[]
    for i,j in combinations(range(21),2):
        if j in rows[i]:red.append(len(rows[i]&rows[j]))
        else:blue.append(sum(k not in rows[i] and k not in rows[j] for k in range(21) if k not in [i,j]))
    if len(red)!=93 or max(red)!=3 or max(blue)!=6:raise ValueError('Primary21 exact book caps')
    return dict(edges=93,max_red_pages=3,max_blue_pages=6,sha256=hashlib.sha256(raw).hexdigest())

def mathematical_summary(work,expected=None):
    if expected is None:expected=strict_json(HERE/'EXPECTED.json')
    p=strict_json(work/'projection.json');i=strict_json(work/'incidence-summary.json')
    a=strict_json(work/'audit-summary.json');b=strict_json(work/'block-summary.json');d=strict_json(work/'direct-summary.json')
    required_statuses=['COMPLETE_EXACT_NECESSARY_A9_PROJECTION','COMPLETE_EXACT_A_INCIDENCE_PROJECTION','COMPLETE_INDEPENDENT_PROJECTION_AND_INCIDENCE_AUDIT','COMPLETE_EXACT_COMPONENT_PAGE_CENSUS','COMPLETE_LITERAL_REGULAR9_C3_CENSUS']
    if [v['status'] for v in [p,i,a,b,d]]!=required_statuses:raise ValueError('Incomplete mathematical phase')
    for left,right in [('block-K-words.txt','direct-K-words.txt'),('block-outcomes.txt','direct-outcomes.txt')]:
        if (work/left).read_bytes()!=(work/right).read_bytes():raise ValueError('Entire native/component stream differs: '+left)
    outcomes=(work/'direct-outcomes.txt').read_bytes()
    if len(outcomes)!=d['completion_choices'] or set(outcomes)-{ord('0'),ord('1')}:
        raise ValueError('Complete typed outcome stream')
    if outcomes.count(ord('1'))!=d['valid'] or d['valid']!=b['counts']['valid']:raise ValueError('Outcome/valid count')
    actual=dict(schema=1,primary21_sha256=baseline()['sha256'],projection_counts=p['counts'],
                A_groups={key:sorted(value) for key,value in p['canonical_groups'].items()},
                incidence_counts=i['counts'],incidence_by_word=i['by_word'],audit_counts=a['counts'],audit_groups=a['representative_groups'],
                audit_by_word=a['by_word'],frames=strict_json(work/'frames.json'),
                frames_sha256=hashlib.sha256((work/'frames.txt').read_bytes()).hexdigest(),block_counts=b['counts'],
                direct={key:value for key,value in d.items() if key!='seconds'},
                K_stream_sha256=hashlib.sha256((work/'direct-K-words.txt').read_bytes()).hexdigest(),
                outcome_stream_sha256=hashlib.sha256(outcomes).hexdigest())
    if canonical(actual)!=canonical(expected):raise ValueError('Whole typed frozen mathematical summary differs')
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
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:environment[key]='1'
    python=[sys.executable]+(['-O'] if args.optimized else [])
    commands=[python+[str(HERE/'projection.py'),'--work',str(work)],
              python+[str(HERE/'incidences.py'),'--work',str(work)],
              python+[str(HERE/'audit.py'),'--work',str(work)],
              python+[str(HERE/'block.py'),'--work',str(work)],
              ['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow',str(HERE/'direct.cpp'),'-o',str(work/'direct')],
              [str(work/'direct'),str(work/'frames.txt'),str(work)]]
    for index,command in enumerate(commands):
        result=subprocess.run(command,env=environment,capture_output=True,text=True,timeout=30)
        (work/('phase-'+str(index)+'.stdout')).write_text(result.stdout)
        (work/('phase-'+str(index)+'.stderr')).write_text(result.stderr)
        result.check_returncode()
        if index==4 and result.stderr:raise ValueError('Compiler warnings')
    mathematical=mathematical_summary(work,expected)
    (work/'mathematical-summary.json').write_text(json.dumps(mathematical,sort_keys=True,indent=2)+'\n')
    report=dict(status='COMPLETE_COLD_REGULAR9_C3_REPLAY',seconds=time.monotonic()-start,
                primary21=control,optimized_python=args.optimized,threads=1,child_guard_seconds=30,soft_phase_seconds=25,
                peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,python=sys.version.split()[0],
                mathematical_summary_sha256=hashlib.sha256((work/'mathematical-summary.json').read_bytes()).hexdigest(),
                source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.iterdir() if p.is_file()},
                trust='Same-author distinct local/pair-join, weighted-mask/native-word and component/literal algorithms; written completeness and relabeling bridges unformalized; independent peer review pending.')
    (work/'replay-summary.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='source_hashes'},indent=2))

if __name__=='__main__':main()
