#!/usr/bin/env python3
import argparse,hashlib,json,sys,time,threading
from fractions import Fraction
from pathlib import Path
from itertools import combinations
PARSER=argparse.ArgumentParser()
PARSER.add_argument('--work',type=Path,required=True)
ARGS=PARSER.parse_args()
HERE=ARGS.work.resolve()
HERE.mkdir(parents=True,exist_ok=True)
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'hadwiger_nelson_snail_mixed_boxes'))
import geometry as G
from pysat.solvers import Glucose42
P=G.PRIME

def save(name,x):
 (HERE/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def encoded(x):return [[v.numerator,v.denominator] for v in x]
def motion(f):
 a,u,k=f
 return (G.evaluate(a),G.evaluate(G.bar(a)),G.evaluate(u),G.evaluate(G.bar(u)),int(k))
def comp(f,g):
 a,b,u,v,k=f;c,d,x,y,l=g
 if k:c,d=d,c;x,y=y,x
 return ((a+u*c)%P,(b+v*d)%P,u*x%P,v*y%P,k^l)
def inv(f):
 a,u,k=f
 v=G.bar(u)
 if k:return (G.scale(G.mul(u,G.bar(a)),-1),u,True)
 return (G.scale(G.mul(v,a),-1),v,False)
SEED=tuple((G.evaluate(x),G.evaluate(G.bar(x))) for x in G.POINTS)
def cloud(f):
 a,b,u,v,k=f
 return tuple(((a+u*(y if k else x))%P,(b+v*(x if k else y))%P) for x,y in SEED)
def sha(b):return hashlib.sha256(b).hexdigest()

def main():
 if (HERE/'QUERY_STARTED').exists():raise RuntimeError('Frozen gate; use saved certificate')
 start=time.monotonic()
 high=G.high_generators();aug=G.augmentation_generators()
 gs={t for _,_,t in high}|set(aug)
 gs |= {inv(t) for t in tuple(gs)}
 gs.discard(G.IDENTITY);generators=sorted(gs,key=repr)
 mods=[motion(t) for t in generators]
 if len(set(mods))!=len(mods):raise RuntimeError('generator residue collision')
 save('generators.json',{'source_high_indices':[i for _,i,_ in high],'source_high_overlaps':[o for o,_,_ in high],'count':len(generators),'motions':[[encoded(a),encoded(u),bool(k)] for a,u,k in generators]})
 print(json.dumps({'phase':'generators','count':len(gs),'seconds':time.monotonic()-start}),flush=True)
 transforms=[G.IDENTITY];ms=[motion(G.IDENTITY)];selected=set(ms)
 physical=set(G.POINTS);residues=set(SEED);trace=[];tape=[]
 for step in range(1,64):
  offers={}
  for ai,a in enumerate(ms):
   for gi,g in enumerate(mods):
    f=comp(a,g)
    if f not in selected:offers.setdefault(f,(ai,gi))
  ranked=[]
  for f,parent in offers.items():
   cp=set(cloud(f));new=len(cp-residues)
   if not new:continue
   gain=2*sum(comp(f,g) in selected for g in mods)
   ranked.append((Fraction(gain,new),gain,29-new,f,parent))
  ranked.sort(key=lambda x:(-x[0],-x[1],-x[2],x[3]))
  rejected=0;chosen=None
  for score,gain,overlap,f,(ai,gi) in ranked:
   if len(residues)+29-overlap>508:continue
   exact=G.compose(transforms[ai],generators[gi]);cp=set(G.cloud(exact));union=physical|cp
   if len(union)>508:rejected+=1;continue
   if len(union)==len(physical):continue
   if motion(exact)!=f:raise RuntimeError('motion composition mismatch')
   nr=residues|set(cloud(f))
   # Injectivity of modular address map on this chosen physical set is audited.
   if len(nr)!=len(union):raise RuntimeError('selected point residue collision')
   chosen=(exact,f,union,nr,ai,gi,gain,overlap,score);break
  if chosen is None:
   stop='NO_ADMISSIBLE_FRONTIER';break
  exact,f,physical,residues,ai,gi,gain,overlap,score=chosen
  transforms.append(exact);ms.append(f);selected.add(f);tape.append([ai,gi])
  trace.append({'copies':len(transforms),'points':len(physical),'parent':ai,'generator':gi,'gain':gain,'overlap':overlap,'score':str(score),'frontier_count':len(offers),'exact_rejections':rejected})
  print(json.dumps(trace[-1]),flush=True)
  save('growth.json',{'tape':tape,'trace':trace})
  if len(physical)==508:stop='PHYSICAL_CAP';break
 else:stop='COPY_CAP'
 points=sorted(physical);values=[G.evaluate(x) for x in points];bars=[G.evaluate(G.bar(x)) for x in points]
 edges=[(i,j) for i,j in combinations(range(len(points)),2) if (values[i]-values[j])*(bars[i]-bars[j])%P==G.F.D**2%P]
 clauses=[[4*i+c+1 for c in range(4)] for i in range(len(points))]
 clauses += [[-4*i-c-1,-4*i-d-1] for i in range(len(points)) for c,d in combinations(range(4),2)]
 clauses += [[-4*i-c-1,-4*j-c-1] for i,j in edges for c in range(4)]
 dimacs=f'p cnf {4*len(points)} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
 (HERE/'candidate.cnf').write_text(dimacs)
 save('candidate.json',{'points':[encoded(x) for x in points],'tape':tape,'copies':len(transforms),'modular_edges':len(edges),'stop':stop})
 (HERE/'QUERY_STARTED').write_text(sha(dimacs.encode())+'\n')
 with Glucose42(bootstrap_with=clauses) as s:
  s.conf_budget(1000000);timer=threading.Timer(180,s.interrupt);timer.start();t=time.monotonic()
  try:answer=s.solve_limited(expect_interrupt=True)
  finally:timer.cancel()
  stats=s.accum_stats();elapsed=time.monotonic()-t
  word=None
  if answer:
   model=set(s.get_model());word=[next(c for c in range(4) if 4*i+c+1 in model) for i in range(len(points))]
   if any(word[i]==word[j] for i,j in edges):raise RuntimeError('bad word')
 internal=sum(comp(f,g) in selected for f in ms for g in mods)
 result={'answer':answer,'physical_points':len(points),'modular_edges':len(edges),'copies':len(ms),'generators':len(mods),'closed_directed_generator_transitions':internal,'all_directed_generator_transitions':len(ms)*len(mods),'stop':stop,'cnf_variables':4*len(points),'cnf_clauses':len(clauses),'cnf_sha256':sha(dimacs.encode()),'word':word,'solver':'Glucose42 python-sat 1.9.dev15','stats':stats,'solver_seconds':elapsed,'total_seconds':time.monotonic()-start}
 save('RESULT.json',result)
 if answer:
  source_index={x:i for i,x in enumerate(G.POINTS)};anchors=[]
  for f in generators:
   hits=[(i,source_index[x]) for i,x in enumerate(G.cloud(f)) if x in source_index]
   (i,k),(j,l)=hits[:2];anchors.append([i,j,k,l,int(f[2])])
  colour=dict(zip(points,word))
  address_word=''.join(str(colour[x]) for f in transforms for x in G.cloud(f))
  cert={'version':1,'generator_anchors':anchors,'copy_tape':tape,'address_colours':address_word,'physical_vertices':len(points),'copies':len(transforms),'producer_modular_edges':len(edges)}
  (HERE/'certificate.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
 print(json.dumps(result),flush=True)

if __name__=='__main__':main()
