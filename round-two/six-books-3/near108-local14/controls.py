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
primary_red,primary_blue=page_counts_sets(a);r,b=primary_red,primary_blue; need((r,b)==page_counts_bits(a),'Positive baseline literal oracles disagree')
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

# Each raw miss incidence gives an invalid108-edge identity fixture when
# paired with the circulant four-regular graph on B. No book validity is assumed.
records=json.loads((OUT/'transfer14_records.json').read_text())
patterns={}; identity_counts={'root_blue':0,'root_red':0,'A_pairs':0,'A_B':0,'B_pairs':0}
for rec in records:
 rows=rec['rows'];g=[set() for _ in range(22)]
 def edge(u,v):g[u].add(v);g[v].add(u)
 for i in range(10):
  edge(0,i+1)
  for j in core[i]:
   if (i,j)!=(0,1) and (i,j)!=(1,0):edge(i+1,j+1)
  for b,z in enumerate(rows):
   if not z>>i&1:edge(i+1,b+11)
 for b in range(11):
  for step in (-2,-1,1,2):edge(b+11,11+(b+step)%11)
 vertices=set(range(22));blue=[vertices-{i}-g[i] for i in range(22)]
 delta=[10-len(s) for s in g];ks=[z.bit_count() for z in rows]
 need(sum(map(len,g))==216 and all(len(g[i])==10 for i in range(11)), '108 fixture/full degrees')
 need(sum(delta)==4 and all(0<=d<=4 for d in delta),'108 deficit range')
 need(delta[11:]==[k-4 for k in ks] and all(len(g[b+11]&set(range(11,22)))==4 for b in range(11)), '108 summed equality')
 tag=','.join(map(str,sorted(d for d in delta if d)));patterns[tag]=patterns.get(tag,0)+1
 local=[{j-1 for j in g[i+1]&set(range(1,11))} for i in range(10)]
 cols=[{b for b,z in enumerate(rows) if z>>i&1} for i in range(10)]
 stars=[{q-11 for q in g[b+11] if q>=11} for b in range(11)]
 for i in range(10):
  need(len(g[0]&g[i+1])==len(local[i]),'root red identity');identity_counts['root_red']+=1
 for b in range(11):
  need(len(blue[0]&blue[b+11])==10-ks[b]+delta[b+11]==6,'root blue equality');identity_counts['root_blue']+=1
 for i,j in itertools.combinations(range(10),2):
  formula=8-len(local[i])-len(local[j])+len(local[i]&local[j])+len(cols[i]&cols[j])
  literal=len(g[i+1]&g[j+1]) if j in local[i] else len(blue[i+1]&blue[j+1])
  need(formula==literal,'A pair identity');identity_counts['A_pairs']+=1
 for i in range(10):
  for b,z in enumerate(rows):
   t=sum(z>>j&1 for j in local[i]);s=len(stars[b]&cols[i]);h=len(local[i])
   if z>>i&1:formula=h+ks[b]-t-s;literal=len(blue[i+1]&blue[b+11])
   else:formula=h-t+4-s;literal=len(g[i+1]&g[b+11])
   need(formula==literal,'A--B page identity');identity_counts['A_B']+=1
 for b,c in itertools.combinations(range(11),2):
  miss=(rows[b]&rows[c]).bit_count()
  if c in stars[b]:formula=10-ks[b]-ks[c]+miss+len(stars[b]&stars[c]);literal=len(g[b+11]&g[c+11])
  else:formula=1+miss+len((set(range(11))-{b}-stars[b])&(set(range(11))-{c}-stars[c]));literal=len(blue[b+11]&blue[c+11])
  need(formula==literal,'B pair identity');identity_counts['B_pairs']+=1
rejections=[]
with tempfile.TemporaryDirectory(prefix='books108-controls-') as temp:
 root=Path(temp)
 def replay(name,script,mutate,source_copy=False):
  p=root/name;p.mkdir()
  for f in ('transfer14_records.json','coupled14_cases.json'):shutil.copyfile(OUT/f,p/f)
  if source_copy:
   for f in ('generate.py','certificate.json','expected.json'):shutil.copyfile(HERE/f,p/f)
  mutate(p)
  executable=p/script if source_copy else HERE/script
  cp=subprocess.run([sys.executable,'-O',str(executable),'--output-dir',str(p)],capture_output=True,text=True,timeout=30)
  need(cp.returncode!=0 and 'RuntimeError' in cp.stderr,name+' was not explicitly rejected')
  rejections.append({'name':name,'exit_code':cp.returncode,'reason':cp.stderr.splitlines()[-1]})
 def mutate_json(p,name,func):
  q=p/name;x=json.loads(q.read_text());func(x);q.write_text(json.dumps(x))
 replay('missing_incidence','verify_multicover.py',lambda p:mutate_json(p,'transfer14_records.json',lambda x:x.pop()))
 replay('duplicate_incidence','verify_literal.py',lambda p:mutate_json(p,'transfer14_records.json',lambda x:x.__setitem__(1,x[0])))
 def baddef(x):
  b=next(i for i,d in enumerate(x[0]['deficits']) if d);x[0]['deficits'][b]-=1
 replay('incorrect_total_deficit','verify_literal.py',lambda p:mutate_json(p,'coupled14_cases.json',baddef))
 def wrongtag(x):
  ds=x[0]['deficits'];b=next(i for i,d in enumerate(ds) if d);c=next(i for i,d in enumerate(ds) if not d);ds[b]-=1;ds[c]+=1
 replay('wrong_unique_tag_preserving_total','verify_literal.py',lambda p:mutate_json(p,'coupled14_cases.json',wrongtag))
 def badmask(x):x[0]['domain_masks'][0][0]^=1
 replay('altered_exact_star_domain','verify_literal.py',lambda p:mutate_json(p,'coupled14_cases.json',badmask))
 def falsemin(p):
  mutate_json(p,'transfer14_records.json',lambda x:[r.__setitem__('deficit_assignments',[]) for r in x if any(max(ds)>2 for ds in r['deficit_assignments'])])
  mutate_json(p,'coupled14_cases.json',lambda x:x.__setitem__(slice(None),[c for c in x if max(c['deficits'])<=2]))
 replay('false_minimum_eight','verify_literal.py',falsemin)
 def badcached(x):
  r=next(r for r in x if max(z.bit_count() for z in r['rows'])==8);b=next(i for i,z in enumerate(r['rows']) if z.bit_count()==8);r['star_counts'][b][4]+=1
 replay('altered_deficit_four_star_count','verify_literal.py',lambda p:mutate_json(p,'transfer14_records.json',badcached))
 def noninteger(x):x['cut']['beta'][0][2]=0.5
 replay('noninteger_cut','generate.py',lambda p:mutate_json(p,'certificate.json',noninteger),True)
 def bound(x):x['cut']['gamma']-=1
 replay('incorrect_cut_bound','generate.py',lambda p:mutate_json(p,'certificate.json',bound),True)
result={'agent':'six-books-3','role':'researcher','positive21':{'red_edges':len(primary_red),'blue_edges':len(primary_blue),'max_red_pages':max(primary_red),'max_blue_pages':max(primary_blue),'raw_sha256':hashlib.sha256(raw).hexdigest()},'book_controls':{'redB4':True,'blueB7':True},'restored_core_KG5_2_isomorphism':[mapping[i] for i in range(10)],'signed108_identity_fixtures':len(records),'fixture_deficit_patterns':patterns,'literal_identity_counts':identity_counts,'rejections':rejections,'all_pass':True}
(OUT/'controls_result.json').write_text(json.dumps(result,indent=2)+'\n')
need(result==json.loads(args.expected.read_text())['controls'],'Control results differ')
print(json.dumps(result,indent=2))
