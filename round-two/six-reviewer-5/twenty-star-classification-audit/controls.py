"""Damages, full point-map positive checks and deterministic relabelings."""
from itertools import combinations
import random,subprocess
from audit import blocks, properties, normalized, key, classify, require, ANCHORS, COLS

def literal_map(source,destination,g):
 require(len(g)==17 and sorted(g)==list(range(17)),'bad point bijection')
 require(tuple(sorted(tuple(sorted(g[x] for x in b)) for b in source))==blocks(destination),'false point-map image')

def controls(leaves,fixtures,binary,graph):
 done=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError):done.append(name);return
  raise ValueError('damage was accepted: '+name)
 q=blocks(fixtures[7]);bad=list(q);bad[1]=bad[0]
 reject('duplicate-block',lambda:blocks(bad))
 bad=list(q);bad[0]=(0,1,2,17)
 reject('out-of-domain-block',lambda:blocks(bad))
 bad=list(q);bad[0]=(0,0,1,2)
 reject('repeated-point-block',lambda:blocks(bad))
 # Independently build a distinct block sharing an existing pair.
 bad=list(q)
 bad[0]=next(b for b in combinations(range(17),4) if len(set(b)&set(q[1]))>=2 and b not in q)
 reject('repeated-covered-pair',lambda:blocks(bad))
 badmap=list(range(17));badmap[0]=1
 reject('nonbijective-point-map',lambda:literal_map(q,q,badmap))
 badmap=next([b if x==a else a if x==b else x for x in range(17)] for a,b in combinations(range(17),2) if tuple(sorted(tuple(sorted((b if x==a else a if x==b else x) for x in B)) for B in q))!=q)
 reject('false-positive-point-map',lambda:literal_map(q,q,badmap))
 reject('omitted-target-clique',lambda:classify(leaves[1:],fixtures))
 reject('omitted-fixture-class',lambda:classify(leaves,fixtures[:-1]))
 reject('duplicated-fixture-class',lambda:classify(leaves,fixtures+[fixtures[0]]))
 for name,arguments,data in [('fixed-node-guard',[str(binary),'--guard-zero'],graph),('asymmetric-graph',[str(binary)],'2 1\n1 1\n0\n'),('trailing-graph',[str(binary)],'1 1\n0\nwrong\n')]:
  r=subprocess.run(arguments,input=data,text=True,capture_output=True,timeout=35)
  require(r.returncode==2 and not r.stderr.startswith('COMPLETE '),'native rejection failed: '+name);done.append(name)
 # Point labels deliberately no longer match the carrier. All roots must normalize anyway.
 rng=random.Random(1018720);transports=0;relabels=0
 for raw in fixtures:
  q=blocks(raw);g=list(range(17));rng.shuffle(g)
  moved=blocks(tuple(tuple(g[x] for x in B) for B in q));literal_map(q,moved,g)
  reference={k for k,f in normalized(q)};got=set()
  for k,f in normalized(moved):
   destination=blocks(ANCHORS+tuple(COLS[i] for i in k));literal_map(moved,destination,f);got.add(k);transports+=1
  require(reference==got,'relabeling changed rooted class');relabels+=1
 return dict(damages=done,small_graph_cases=6144,random_relabelings=relabels,literal_transports=transports)
