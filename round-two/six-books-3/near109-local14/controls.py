"""Positive prior-art baseline and damaged certificate/input rejection controls.
Actual author six-books-3, researcher. Python3.11 standard library.
"""
import argparse,hashlib,itertools,json,shutil,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(); parser.add_argument('--output-dir',type=Path,default=HERE/'_work'); parser.add_argument('--expected',type=Path,default=HERE/'expected.json'); args=parser.parse_args()
OUT=args.output_dir

def need(p,why):
    if not p: raise RuntimeError(why)

def page_counts_sets(a):
    vertices=set(range(len(a))); red=[]; blue=[]
    for i,j in itertools.combinations(vertices,2):
        if j in a[i]: red.append(len(a[i]&a[j]))
        else: blue.append(len((vertices-{i}-a[i])&(vertices-{j}-a[j])))
    return red,blue

def page_counts_bits(a):
    n=len(a); u=(1<<n)-1; masks=[sum(1<<v for v in ns) for ns in a]; red=[]; blue=[]
    for i,j in itertools.combinations(range(n),2):
        if masks[i]>>j&1: red.append((masks[i]&masks[j]).bit_count())
        else: blue.append(((u^(1<<i)^masks[i])&(u^(1<<j)^masks[j])).bit_count())
    return red,blue

raw=(HERE/'primary21.txt').read_bytes(); mat=json.loads(raw.decode().split('\n\n')[0])
need(hashlib.sha256(raw).hexdigest()=='3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55','Primary21 fixture changed')
need(len(mat)==21 and all(len(r)==21 for r in mat),'Baseline dimensions')
need(all(type(mat[i][j]) is int and mat[i][j] in (0,1) and mat[i][j]==mat[j][i] for i in range(21) for j in range(21)),'Baseline matrix entries/symmetry')
a=[{j for j in range(21) if i!=j and mat[i][j]==0} for i in range(21)]
r,b=page_counts_sets(a); need((r,b)==page_counts_bits(a),'Positive baseline literal oracles disagree')
need((len(r),len(b),max(r),max(b))==(93,117,3,6),'Known21-host baseline differs')
# Both literal oracles must detect a red B4 and a blue B7.
badred=[set() for _ in range(6)]
for i,j in [(0,1)]+[(u,v) for u in (0,1) for v in range(2,6)]:
    badred[i].add(j); badred[j].add(i)
need(page_counts_sets(badred)==page_counts_bits(badred) and max(page_counts_sets(badred)[0])==4,'Red B4 control')
badblue=[set() for _ in range(9)]
need(page_counts_sets(badblue)==page_counts_bits(badblue) and max(page_counts_sets(badblue)[1])==7,'Blue B7 control')
# Check that restoring the missing low-low edge is literally Petersen.
core=[set() for _ in range(10)]
for i,j in ((0,2),(0,3),(1,4),(1,5),(0,1)):
    core[i].add(j); core[j].add(i)
for bit,(i,j) in enumerate(itertools.combinations(range(8),2)):
    if 51317328>>bit&1: core[i+2].add(j+2); core[j+2].add(i+2)
need(all(len(s)==3 for s in core),'Restored core degrees')
need(all(len(core[i]&core[j])==(0 if j in core[i] else 1) for i,j in itertools.combinations(range(10),2)),'Restored Petersen intersections')
kg=list(itertools.combinations(range(5),2)); ka=[{j for j,t in enumerate(kg) if not(set(s)&set(t))} for s in kg]
def iso(mapping):
    if len(mapping)==10: return mapping
    u=max((i for i in range(10) if i not in mapping),key=lambda i:(len(core[i]&set(mapping)),-i))
    for v in range(10):
        if v in mapping.values(): continue
        if all((t in core[u])==(q in ka[v]) for t,q in mapping.items()):
            answer=iso(mapping|{u:v})
            if answer is not None: return answer
    return None
mapping=iso({}); need(mapping is not None,'Restored core not isomorphic to KG(5,2)')
rejections=[]
with tempfile.TemporaryDirectory(prefix='books109-controls-') as temp:
    root=Path(temp)
    def replay(name,script,mutate,source_copy=False):
        p=root/name; p.mkdir()
        for f in ('transfer14_records.json','coupled14_cases.json'):
            shutil.copyfile(OUT/f,p/f)
        if source_copy:
            for f in ('generate.py','certificate.json','expected.json'):
                shutil.copyfile(HERE/f,p/f)
        mutate(p)
        executable=p/script if source_copy else HERE/script
        cp=subprocess.run([sys.executable,'-O',str(executable),'--output-dir',str(p)],capture_output=True,text=True,timeout=30)
        need(cp.returncode!=0 and 'RuntimeError' in cp.stderr,name+' was not explicitly rejected')
        rejections.append({'name':name,'exit_code':cp.returncode,'reason':cp.stderr.splitlines()[-1]})
    def missing(p):
        q=p/'transfer14_records.json'; x=json.loads(q.read_text()); x.pop(); q.write_text(json.dumps(x))
    replay('missing_incidence','verify_multicover.py',missing)
    def duplicate(p):
        q=p/'transfer14_records.json'; x=json.loads(q.read_text()); x[1]=x[0]; q.write_text(json.dumps(x))
    replay('duplicate_incidence','verify_literal.py',duplicate)
    def baddef(p):
        q=p/'coupled14_cases.json'; x=json.loads(q.read_text()); b=next(i for i,d in enumerate(x[0]['deficits']) if d); x[0]['deficits'][b]-=1; q.write_text(json.dumps(x))
    replay('incorrect_total_deficit','verify_literal.py',baddef)
    def domain(p):
        q=p/'coupled14_cases.json'; x=json.loads(q.read_text()); x[0]['domain_sizes'][0]+=1; q.write_text(json.dumps(x))
    replay('altered_star_domain','verify_literal.py',domain)
    def noninteger(p):
        q=p/'certificate.json'; x=json.loads(q.read_text()); x['cut']['beta'][0][2]=0.5; q.write_text(json.dumps(x))
    replay('noninteger_cut','generate.py',noninteger,True)
    def bound(p):
        q=p/'certificate.json'; x=json.loads(q.read_text()); x['cut']['gamma']-=1; q.write_text(json.dumps(x))
    replay('incorrect_cut_bound','generate.py',bound,True)
result={'agent':'six-books-3','role':'researcher','positive21':{'red_edges':len(r),'blue_edges':len(b),'max_red_pages':max(r),'max_blue_pages':max(b),'raw_sha256':hashlib.sha256(raw).hexdigest()},'book_controls':{'redB4':True,'blueB7':True},'restored_core_KG5_2_isomorphism':[mapping[i] for i in range(10)],'rejections':rejections,'all_pass':True}
need(result==json.loads(args.expected.read_text())['controls'],'Control results differ')
print(json.dumps(result,indent=2))
