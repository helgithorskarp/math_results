from pathlib import Path
import sys,json,time
from collections import Counter,defaultdict
import os
W=Path(os.environ['HN_PAIR_RUN_DIR']).resolve();W.mkdir(parents=True,exist_ok=True)
R=Path(__file__).resolve().parents[1]
PARENT=R/'hadwiger_nelson_single_anchor_field_gate'
pins=json.loads((Path(__file__).resolve().parent/'SOURCE_PINS.json').read_text())
import hashlib
for rel,h in pins.items():
 if hashlib.sha256((R/rel).read_bytes()).hexdigest()!=h:raise ValueError('source pin '+rel)
sys.path.insert(0,str(PARENT))
from common import *
x=json.loads((W/'G_census.json').read_text());expected=json.loads((PARENT/'EXPECTED.json').read_text())['motifs']['G'];require(digest(x['outside_groups'])==expected['outside_sha256'],'source census pin')
if __name__=='__main__':
 st=time.time();P,word=seed();C=patterns('G');S=sorted({sc(parse(v['disc']),scale(ONE,F(1,3)))for v in x['outside_groups']});classes=[];lookup={}
 for s in S:
  require(sgn(s)>0 and sq(s)is None,'nontrivial positive class')
  for i,t in enumerate(classes):
   q=sq(em(s,ri(t)))
   if q is not None:
    if sgn(q)<0:q=sc(q,scale(ONE,-1))
    lookup[s]=(i,q);break
  else:lookup[s]=(len(classes),EO);classes.append(s)
 print('CLASSES',len(S),len(classes),[[ser(s)for s in classes]],'sec',time.time()-st,flush=True)
 copies={};pts={};count=Counter()
 for ri0,v in enumerate(x['outside_groups']):
  pp=v['p'];rr,jj=v['events'][0];A=C[v['pattern']];delta=es(P[pp],P[rr]);ci=ei(sc(ec(delta),A[jj]));T=parse(v['T']);s=sc(parse(v['disc']),scale(ONE,F(1,3)));cl,q=lookup[s];z0=sc(T,scale(ONE,F(1,2)));z1=em(sc(ci,scale(ALPHA,F(1,2))),q)
  require(ea(en(z0),em(classes[cl],en(z1)))==EO and ea(em(z0,ec(z1)),em(z1,ec(z0)))==EZ,'exact unit multiplier after class change')
  for sign in[-1,1]:
   image=tuple(sorted((cl,ea(P[pp],sc(z0,b)),sc(sc(z1,b),scale(ONE,sign)))for b in A[1:]));require(len(set(image))==9,'copy injectivity')
   if image not in copies:copies[image]={'record':ri0,'sign':sign,'class':cl,'cross':v['cross'],'inside':v['inside']}
   count['raw']+=1
  if ri0%1000==0:print('COPY',ri0,len(copies),'sec',time.time()-st,flush=True)
 points=sorted({p for C in copies for p in C});require(all(b!=EZ for cl,a,b in points),'new point inside seed field');ix={p:i for i,p in enumerate(points)};records=[]
 for image,wit in sorted(copies.items()):records.append({'points':[ix[p]for p in image],**wit})
 out={'classes':[ser(s)for s in classes],'points':[[cl,ser(a),ser(b)]for cl,a,b in points],'copies':records,'raw_copies':count['raw'],'source_cases':len(x['outside_groups']),'source_radicals':len(S),'class_point_counts':dict(Counter(p[0]for p in points)),'class_copy_counts':dict(Counter(v['class']for v in records)),'seconds':time.time()-st};(W/'inventory.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('DONE',len(points),len(copies),out['class_point_counts'],out['class_copy_counts'],'sec',time.time()-st,flush=True)
