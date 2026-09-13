"""Exact Moser-spindle insertions into the two frozen 490-point physical seeds."""
from pathlib import Path
import os,sys,json,time,hashlib
W=Path(os.environ['HN_INSERT_RUN_DIR']).resolve();W.mkdir(parents=True,exist_ok=True)
os.environ['HN_MIXED_RUN_DIR']=str(W)
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'hadwiger_nelson_mixed_atom_record_search'))
pins=json.loads((Path(__file__).resolve().parent/'SOURCE_PINS.json').read_text())
for name,expected in pins['files'].items():
 if hashlib.sha256((R/name).read_bytes()).hexdigest()!=expected:raise ValueError('dependency mismatch: '+name)
from shell_search import *
from collections import defaultdict
from math import lcm


def seed(tag):
 s,labels,word,ne,_=fixture_seed(tag);pp=sorted(set(labels));ix={p:i for i,p in enumerate(pp)};cc=[None]*len(pp)
 for p,c in zip(labels,word):require(cc[ix[p]] is None or cc[ix[p]]==c,'seed colour descent');cc[ix[p]]=c
 require(len(pp)==490,'seed count');return s,pp,''.join(cc),ne

def patterns():
 M=spindle();out=defaultdict(set)
 for A in (M,[K.conj(m)for m in M]):
  for i,j in product(range(7),repeat=2):
   if i==j:continue
   delta=sub(A[j],A[i]);nn=norm(delta);ii=inv(delta);P=tuple(sorted(mul(sub(x,A[i]),ii)for x in A));out[nn].add(P)
 return {k:sorted(v)for k,v in out.items()}

def generate(tag):
 st=time.time();s,P,word,ne=seed(tag);X=Extension(s);pat=patterns();old=set(P);old_index={p:i for i,p in enumerate(P)};pairs=defaultdict(list)
 for i,j in combinations(range(len(P)),2):
  d=esub(P[j],P[i]);nn=X.norm(d)
  if nn[1]==ZERO and nn[0]in pat:pairs[d].append((i,j))
 print('MATCHING_PAIR_INVENTORY',tag,'norms',len(pat),'patterns',sum(map(len,pat.values())),'directions',len(pairs),'pairs',sum(map(len,pairs.values())),'seconds',time.time()-st,flush=True)
 additions={};count=0
 for d,pplist in sorted(pairs.items()):
  nn=X.norm(d)[0]
  for normalized in pat[nn]:
   offsets=[ecscale(d,x)for x in normalized]
   for i,j in pplist:
    image=tuple(eadd(P[i],x)for x in offsets);new=tuple(sorted(set(image)-old))
    if not new:continue
    require(len(new)<=5,'attachment budget');count+=1
    if new not in additions:additions[new]={'witness_pair':(i,j),'image':image,'multiplicity':0}
    additions[new]['multiplicity']+=1
 print('PLACEMENT_INVENTORY',tag,'unique',len(additions),'raw',count,'new_counts',dict(Counter(map(len,additions))),'seconds',time.time()-st,flush=True)
 newpoints=sorted({p for A in additions for p in A});ni={p:i for i,p in enumerate(newpoints)}
 out={'tag':tag,'radicand':list(map(str,s)),'seed_points':[[str(x)for z in p for x in z]for p in P],'seed_word':word,'seed_edges':ne,'new_points':[[str(x)for z in p for x in z]for p in newpoints],'placements':[{'new':[ni[p]for p in A],'witness_pair':v['witness_pair'],'old':[old_index[p]for p in v['image']if p in old],'multiplicity':v['multiplicity']}for A,v in sorted(additions.items())],'raw_placements':count,'seconds':time.time()-st}
 (W/f'placements_{tag}.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('PLACEMENTS_SAVED',tag,'points',len(newpoints),'seconds',time.time()-st,flush=True)
if __name__=='__main__':generate(sys.argv[1])
