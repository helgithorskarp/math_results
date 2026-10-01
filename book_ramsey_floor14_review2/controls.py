"""Independent literal weighted-graph and incidence controls, reviewer2."""
from pathlib import Path
from itertools import combinations,product
from random import Random
from collections import defaultdict
import argparse,json,subprocess,resource,time
import cores as c
from audit import inputs,encode_case
HERE=Path(__file__).resolve().parent

def native_input(cases,cap=200000):
 return str(len(cases))+' '+str(cap)+'\n'+''.join('\n'.join([' '.join(map(str,r)) for r in b]+[' '.join(map(str,d))])+'\n' for b,d in cases)
def controlled(work,target):
 start=time.monotonic();work.mkdir(parents=True,exist_ok=True);expected,cert=inputs(target)
 exe=work/'controls-native'
 subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Werror',str(HERE/'paired_stubs.cpp'),'-lcrypto','-o',str(exe)],check=True,timeout=60)
 rng=Random(3308218);cases=[];truth=[];p4=list(combinations(range(4),2));cartesian=0
 for trial in range(256):
  caps=[rng.randrange(3) for _ in p4];base=[[0]*10 for _ in range(10)]
  for (i,j),cap in zip(p4,caps):base[i][j]=base[j][i]=cap
  groups=defaultdict(list)
  for ws in product(*(range(x+1) for x in caps)):
   d=[0]*10;edges=[];cartesian+=1
   for (i,j),w in zip(p4,ws):
    d[i]+=w;d[j]+=w
    if w:edges.append([i,j,w])
   if max(d)<=5:groups[tuple(d)].append(edges)
  possible=sorted(groups);ds=[possible[rng.randrange(len(possible))],tuple([rng.randrange(6) for _ in range(4)]+[0]*6)]
  for d in ds:cases.append((base,list(d)));truth.append(sorted(groups.get(d,[])))
 out=subprocess.run([str(exe),'--pairing'],input=native_input(cases),capture_output=True,text=True,check=True,timeout=30).stdout.splitlines()
 c.need(len(out)==512 and [json.loads(x) for x in out]==truth,'paired-stub and Cartesian weighted graphs differ entrywise')
 profiles,_=c.build(expected);relabeled=0
 for p in profiles:
  stars=p['stars'];high=list(range(6));low=list(range(4));rng.shuffle(high);rng.shuffle(low)
  mask=c.moved(p['F_mask'],high);mapped=[None]*4
  for i,pair in enumerate(stars):mapped[low[i]]=tuple(sorted(high[x] for x in pair))
  s=c.local(mask,mapped);old=p['matrix'];point=low+[4+x for x in high]
  c.need(all(old[i][j]==s[point[i]][point[j]] for i in range(10) for j in range(10)),'normalization matrix conjugacy failed');relabeled+=1
 # Arbitrary regular controls check identities even when epsilon is negative.
 identities=0;roots=0
 for trial in range(16):
  red=[{(i+j)%22 for j in range(-5,6) if j} for i in range(22)]
  for step in range(64):
   a,b,d,e=rng.sample(range(22),4)
   if b in red[a] and e in red[d] and d not in red[a] and e not in red[b]:
    for u,v in [(a,b),(d,e)]:red[u].remove(v);red[v].remove(u)
    for u,v in [(a,d),(b,e)]:red[u].add(v);red[v].add(u)
  blue=[set(range(22))-{i}-red[i] for i in range(22)]
  c.need(all(len(x)==10 for x in red),'control regularity failed')
  for v in range(22):
   aa=sorted(red[v]);bb=sorted(blue[v]);local=[red[i]&set(aa) for i in aa];h=list(map(len,local));M=[[int(i not in red[b]) for i in aa] for b in bb]
   for i in range(10):c.need(sum(row[i] for row in M)==h[i]+2,'control column misses');c.need(all(sum(M[k])==len(red[b]&set(bb)) for k,b in enumerate(bb)), 'control outside degree')
   for i,j in c.P10:
    u,w=aa[i],aa[j];pages=len((red[u]&red[w]) if w in red[u] else (blue[u]&blue[w]));eps=(3 if w in red[u] else 6)-pages
    s0=h[i]+h[j]-(5 if w in red[u] else 2)-len(local[i]&local[j]);gram=sum(row[i]*row[j] for row in M)
    c.need(s0-eps==gram,'literal red/blue pair Gram bridge');identities+=1
   for u in range(22):
    deficit_red=sum(3-len(red[u]&red[w]) for w in red[u]);deficit_blue=sum(6-len(blue[u]&blue[w]) for w in blue[u]);c.need(deficit_red+deficit_blue==6,'regular six-budget identity')
   roots+=1
 rejections=0
 sample=None
 for i,profile in enumerate(profiles):
  if not expected['profiles'][i]['states']:continue
  for a,b,base,d in c.row_pairs(profile):
   caps=[row[:] for row in base]
   for k in range(10):caps[k][k]=0
   probe=subprocess.run([str(exe),'--pairing'],input=native_input([(caps,d)]),capture_output=True,text=True,check=True,timeout=30)
   if json.loads(probe.stdout):sample=(i,a,b,base,d);break
  if sample is not None:break
 c.need(sample is not None,'no positive real control fiber')
 i,a,b,base,d=sample;pool=[cert['vectors'][k] for k in cert['profiles'][i]['vector_indices']]
 valid='1 200000\n'+encode_case(i,a,b,base,d,pool)
 for bad in [valid[:-25],valid+'999\n',valid.replace('1 200000','1 200001',1),'1 200000\n'+encode_case(i,[0]*5,b,base,d,pool),'1 200000\n'+encode_case(i,a,b,base,d,[]),'1 200000\n'+encode_case(i,a,b,base,[0]*10,pool)]:
  p=subprocess.run([str(exe)],input=bad,capture_output=True,text=True,timeout=30);c.need(p.returncode!=0,'malformed/noncertifying input accepted');rejections+=1
 incomplete=0
 for mode,data in [([],valid.replace('1 200000','1 0',1)),(['--pairing'],native_input(cases[:1],0))]:
  p=subprocess.run([str(exe)]+mode,input=data,capture_output=True,text=True,timeout=30);c.need(p.returncode!=0 and 'INCOMPLETE' in p.stderr,'tiny guard not visibly incomplete');incomplete+=1
 # A genuine fiber exercises all proof checks under sanitizers.
 san=work/'controls-sanitized'
 subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer',str(HERE/'paired_stubs.cpp'),'-lcrypto','-o',str(san)],check=True,timeout=60)
 p=subprocess.run([str(san)],input=valid,capture_output=True,text=True,check=True,timeout=30);c.need(not p.stderr and 'COMPLETE' in p.stdout,'sanitizer diagnostics or no complete fiber')
 result=dict(agent='six-reviewer-2',role='independent mathematical reviewer',status='COMPLETE literal controls',Cartesian_graphs=cartesian,weighted_domains=512,core_conjugacies=relabeled,regular_control_graphs=16,roots=roots,pair_identities=identities,malformed_or_noncertifying_rejections=rejections,visible_INCOMPLETE=incomplete,sanitized_real_fibers=1,sanitizer_diagnostics=0)
 (work/'controls.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');metrics=dict(seconds=time.monotonic()-start,parent_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
 (work/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(dict(result,**metrics),indent=2));return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--target',type=Path,default=HERE.parent/'book_ramsey_b4_b7_regular110_neighborhood_floor14');a=p.parse_args();controlled(a.work.resolve(),a.target.resolve())
