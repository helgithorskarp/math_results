"""Separate physical colored-page checker for the complete primary record.
Uses ordinal adjacency masks and explicit five-point subsets. Does not import audit.
"""
import itertools,json,argparse
from pathlib import Path
NAMES=('u','v','a')+tuple('x'+str(i) for i in range(6))+('sx0','sx1','sy0','sy1','t0','t1','t2');KALL=(1<<16)-1;QROLES=('A0','A1','B0','B1','C0','C1')
SUBSETS=[s for s in range(32)];MIN={}
for a in range(6):
 for b in range(6):
  aa=[s for s in SUBSETS if s.bit_count()==a];bb=[s for s in SUBSETS if s.bit_count()==b]
  MIN[a,b,'red']=min((x&y).bit_count() for x in aa for y in bb)
  MIN[a,b,'blue']=min((31&~(x|y)).bit_count() for x in aa for y in bb)
def fail(ok,msg):
 if not ok:raise ValueError(msg)
def frame(r,swap):
 rows=[0]*16
 def e(a,b):rows[a]|=1<<b;rows[b]|=1<<a
 for b in (1,2,3,4,5,6,7,8,9,10):e(0,b)
 for b in (1,9,10,11,12,13,14,15):e(2,b)
 for b in (11,12):e(1,b)
 for a,b in ((3,7),(7,6),(6,4),(4,5),(5,8),(8,3),(9,6),(9,8),(10,5),(10,7),(11,14),(11,15),(12,13),(12,14),(9,14-r),(9,15),(10,13+r),(10,15)):e(a,b)
 xrows=[{0,2,3},{1,4,5},{0,1,3,5},{0,1,2,4},{0,1}]
 if swap:xrows[:2]=xrows[1::-1]
 perm={2:3,3:2,4:5,5:4} if r else {}
 for a,row in zip((11,12,13,14,15),xrows):
  for x in row:e(a,3+perm.get(x,x))
 return rows

def check_record(rec):
 k,typ,r,swap=rec['type'];fail(k in (3,4) and typ in range(3) and r in (0,1) and type(swap) is bool,'type')
 rows=frame(r,swap);known={NAMES[i]:[NAMES[j] for j in range(16) if rows[i]>>j&1] for i in range(16)}
 fail({x:sorted(v) for x,v in known.items()}==rec['known_red_rows'],'physical literal rows')
 roleperm=rec['role_permutation'] or {};t0={roleperm.get(x,x) for x in ({'A0'}|set((('C0','C1'),('A1','C0'),('A1','C1'))[typ]))};t2={roleperm.get(x,x) for x in ({'A1','B0','B1'}|({'C0'} if k==4 else set()))}
 fail(sorted(t0)==rec['T0Q'] and sorted(t2)==rec['T2Q'],'role map')
 qr={0:set(),1:set(QROLES),2:set(),11:{'A0','A1'},12:{'B0','B1'},13:t0,14:{'C0','C1'},15:t2}
 degrees=[10,10,9]+[10]*8+[rows[i].bit_count()+len(qr[i]) for i in range(11,16)]
 ranks=[degrees[i]-rows[i].bit_count() for i in range(16)]
 fail(dict(zip(NAMES,degrees))==rec['degrees'] and dict(zip(NAMES,ranks))==rec['ranks'],'actual degrees/ranks')
 fail(rec['target']==ranks[3:11],'rank target')
 pairs=list(itertools.combinations(range(16),2));allow=[]
 for a,b in pairs:allow.append({'spine':[NAMES[a],NAMES[b]],'pages':(rows[a]&rows[b]).bit_count(),'cap':3 if rows[a]>>b&1 else degrees[a]+degrees[b]-14})
 fail(allow==rec['known_allowances'],'all120 allowances')
 domains=[]
 for q in QROLES:
  fixed=sum(1<<i for i in qr if q in qr[i]);s=sum(fixed>>i&1 for i in (11,12));t=sum(fixed>>i&1 for i in (13,14,15));dom=[]
  for h in range(max(0,4-s-t),4-s):
   for bits in itertools.product((0,1),repeat=8):
    red=fixed|sum(bit<<(3+i) for i,bit in enumerate(bits));ok=True
    for a,b in pairs:
     ba=red>>a&1;bb=red>>b&1
     if rows[a]>>b&1:pages=(rows[a]&rows[b]).bit_count()+ba*bb+MIN[ranks[a]-ba,ranks[b]-bb,'red'];cap=3
     else:pages=((KALL&~((1<<a)|(1<<b)|rows[a]|rows[b])).bit_count())+(1-ba)*(1-bb)+MIN[ranks[a]-ba,ranks[b]-bb,'blue'];cap=6
     if pages>cap:ok=False;break
    if not ok:continue
    for a in range(16):
     ba=red>>a&1
     if ba:pages=(rows[a]&red).bit_count()+MIN[ranks[a]-ba,h,'red'];cap=3
     else:pages=(KALL&~((1<<a)|rows[a]|red)).bit_count()+MIN[ranks[a],h,'blue'];cap=6
     if pages>cap:ok=False;break
    if ok:dom.append({'h':h,'word':list(bits),'degree':red.bit_count()+h})
  domains.append(dom)
 fail(domains==rec['domains'],'complete physical column domains')
 balanced=[];cuts=[]
 for tup in itertools.product(*domains):
  if [sum(d['word'][j] for d in tup) for j in range(8)]!=ranks[3:11]:continue
  balanced.append(list(tup));cut=[];qrcols=[]
  for q,d in zip(QROLES,tup):qrcols.append(sum(1<<i for i in qr if q in qr[i])|sum(bit<<(j+3) for j,bit in enumerate(d['word'])))
  for a,b in pairs:
   redpages=(rows[a]&rows[b]).bit_count()+sum((v>>a&1)*(v>>b&1) for v in qrcols)
   bluepages=(KALL&~((1<<a)|(1<<b)|rows[a]|rows[b])).bit_count()+sum((1-(v>>a&1))*(1-(v>>b&1)) for v in qrcols)
   rededge=rows[a]>>b&1
   if (redpages>3 if rededge else bluepages>6):cut.append({'spine':[NAMES[a],NAMES[b]],'red_common':redpages,'allowed':3 if rededge else degrees[a]+degrees[b]-14,'color':'red' if rededge else 'blue'})
  fail(bool(cut),'balanced columns unexcluded');cuts.append(cut)
 fail(balanced==rec['balanced'] and cuts==rec['cuts'] and rec['completions']==[],'whole balanced terminal/cuts')
 return (tuple(sorted(t0)),tuple(sorted(t2)),r,swap)
def check(x):
 fail(x['schema']==1 and x['actual_agent']=='six-reviewer-3' and x['role']=='independent mathematical reviewer','schema/authorship')
 z=x['terminal'];seen=set()
 for rec in z['labeled_cases']:
  tag=check_record(rec);fail(tag not in seen,'duplicate role case');seen.add(tag)
 # Independently enumerate all rank3 T0 rows avoiding B and both rank types.
 expected=set()
 for k in (3,4):
  for a in itertools.combinations(QROLES,3):
   aa=set(a)
   if aa&{'B0','B1'}:continue
   for b in itertools.combinations(QROLES,k):
    bb=set(b)
    if not {'B0','B1'}<=bb or len(bb&{'A0','A1'})>1 or len(bb&{'C0','C1'})>k-3 or aa|bb|{'C0','C1'}!=set(QROLES):continue
    for r,sw in itertools.product((0,1),(False,True)):expected.add((tuple(sorted(aa)),tuple(sorted(bb)),r,sw))
 fail(seen==expected and len(seen)==72,'whole72 actual-role cover')
 for rec in z['canonical']:check_record(rec)
 fail(len(z['canonical'])==6 and len(z['transports'])==72 and all(t['full_domain_transport'] is True for t in z['transports']),'canonical/transports coverage')
 print(json.dumps({'whole_physical_records_checked':78,'labeled_cases':72,'explicit_subset_minima':len(MIN),'complete_domains_and_terminals':True}))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('record',type=Path);args=ap.parse_args();check(json.loads(args.record.read_bytes()))
if __name__=='__main__':main()
