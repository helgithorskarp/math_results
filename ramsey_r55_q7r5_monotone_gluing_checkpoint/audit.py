"""Definition-level full input audit. No producer, solver, or normalization code imported."""

if not __debug__:
    raise RuntimeError('Run this research program without -O or -OO; its exact checks require assertions.')
from pathlib import Path
from itertools import combinations,product
from math import comb
import hashlib,json,sys,time
root=Path(sys.argv[1]);repo=Path(sys.argv[2]);cache=Path(sys.argv[3]);t=time.monotonic()
meta=json.loads((root/'INPUT.json').read_text());rawcat=(cache/'r44_15.g6').read_bytes();assert hashlib.sha256(rawcat).hexdigest()=='53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1'
taskraw=(repo/'ramsey_r55_q7r5_tail_decisions/TASKS.json').read_bytes();assert hashlib.sha256(taskraw).hexdigest()=='3d6e4497ea449f3831a66e1e2832976ca35ec61128c4cc36468e7a7ee5558544';ids=json.loads(taskraw)['retained_core_indices'];assert len(ids)==122
assert meta['original_ids']==[f'bo1-q7-r5-c{i:06d}' for i in ids]
fixed={};edges=[];var={};inv={};nextv=2
for i in range(43):
 for j in range(i+1,43):
  edges.append((i,j))
  if j<28 and i//4==j//4:fixed[i,j]=int(i<20)
  else:var[i,j]=nextv;inv[nextv]=(i,j);nextv+=1
assert nextv==863
f=(root/'input.cnf').open();head=list(f.readline().split());assert head==['p','cnf','115104','2576821'];read=0

def take():
 global read
 a=tuple(map(int,f.readline().split()));assert a and a[-1]==0 and all(0<abs(z)<=115104 for z in a[:-1]);read+=1;return a[:-1]
assert take()==(1,)
for b in range(1,7):
 for col in range(3):
  for low in range(16):
   for high in range(low+1,16):
    clause=take();assignment={var[i,4*b+col]:low>>i&1 for i in range(4)}|{var[i,4*b+col+1]:high>>i&1 for i in range(4)}
    assert len(clause)==8 and {abs(z) for z in clause}==set(assignment)
    assert all(assignment[abs(z)]!=int(z>0) for z in clause)
seen=bytearray(2*comb(43,5));counts=[0,0]
for _ in range(848232+686493):
 clause=take();color=int(clause[0]<0);assert all((z<0)==bool(color) and abs(z) in inv for z in clause)
 S=tuple(sorted({v for z in clause for v in inv[abs(z)]}));assert len(S)==5
 pairs=list(combinations(S,2));assert all(fixed[e]==color for e in pairs if e in fixed)
 assert clause==tuple((-1 if color else 1)*var[e] for e in pairs if e not in fixed)
 rank=sum(comb(v,k+1) for k,v in enumerate(S));key=2*rank+color;assert not seen[key];seen[key]=1;counts[color]+=1
# Complete independent forbidden-set census; each compatible set must have appeared once.
for S in combinations(range(43),5):
 colors={fixed[e] for e in combinations(S,2) if e in fixed};rank=sum(comb(v,k+1) for k,v in enumerate(S))
 for c in (0,1):assert seen[2*rank+c]==int(not colors or colors=={c})
for S in combinations(range(20,43),4):
 pairs=tuple(combinations(S,2))
 if not any(e in fixed for e in pairs):assert take()==tuple(-var[e] for e in pairs)
# Truth-table audit of the actual six-clause prefix gates and comparator condition.
z=863
for a,b in [(1,2),(2,3),(3,4),(5,6)]:
 aa=[var[u,4*a+v] for u in (3,2,1,0) for v in (3,2,1,0)];bb=[var[u,4*b+v] for u in (3,2,1,0) for v in (3,2,1,0)];prev=1
 for i,(x,y) in enumerate(zip(aa,bb)):
  clause=take();assert clause==(-prev,x,-y)
  if i==15:break
  gates=[take() for _ in range(5)];assert set(abs(t) for c in gates for t in c)<={prev,x,y,z}
  for pp,xx,yy,zz in product((0,1),repeat=4):
   vals={prev:pp,x:xx,y:yy,z:zz};truth=all(any(vals[abs(t)]==int(t>0) for t in c) for c in gates);assert truth==(zz==int(pp and xx==yy))
  prev=z;z+=1
assert z==923
selectors=take();assert selectors==tuple(range(923,1045));lines=rawcat.splitlines()
for sel,idx in zip(selectors,ids):
 line=lines[idx];assert len(line)==19 and line[0]-63==15;bits=[(c-63)>>b&1 for c in line[1:] for b in range(5,-1,-1)];assert not any(bits[105:])
 for i,j in combinations(range(15),2):assert take()==(-sel,var[i+28,j+28] if bits[j*(j-1)//2+i] else -var[i+28,j+28])
# Each witness block is reconstructed from actual binary clauses, then identified by its physical five-set.
witness={}
for _ in range(1020060):
 clause=take();assert len(clause)==2 and clause[0]<0 and 1045<=-clause[0]<=115104 and clause[1]<0 and -clause[1] in inv
 witness.setdefault(-clause[0],[]).append(-clause[1])
assert set(witness)==set(range(1045,115105));claimed=set();wc=0
expected= sum(comb(4,j)*4**j*comb(22,3-j) for j in range(4));assert expected==7604
for c in range(28,43):
 cl=take();assert cl[0]==-var[0,c] and len(cl)==1+expected;sets=set()
 for wid in cl[1:]:
  assert wid in witness and wid not in claimed;claimed.add(wid);vs=tuple(sorted({v for x in witness[wid] for v in inv[x]}));assert len(vs)==5 and 0 in vs and c in vs
  pairs=tuple(e for e in combinations(vs,2) if e!=(0,c));assert all(fixed[e]==0 for e in pairs if e in fixed)
  assert witness[wid]==[var[e] for e in pairs if e not in fixed]
  S=tuple(v for v in vs if v not in (0,c));assert S not in sets;sets.add(S);wc+=1
 assert len(sets)==expected
assert len(claimed)==114060 and read==2576821 and f.read()=='';f.close()
h=hashlib.sha256()
with (root/'input.cnf').open('rb') as f:
 for buf in iter(lambda:f.read(2**20),b''):h.update(buf)
assert h.hexdigest()==meta['input_sha256']
r={'status':'VERIFIED_COMPLETE_122_PARENT_NORMALIZED_INPUT','originals':len(ids),'physical_five_clauses':sum(counts),'red_five':counts[1],'blue_five':counts[0],'critical_edges':15,'witnesses':wc,'witnesses_per_edge':expected,'clauses':read,'input_sha256':h.hexdigest(),'seconds':time.monotonic()-t,'no_original_decision':True,'trust':'Finite monotone-descent theorem plus explicit original-clause projection; this audit is not a UNSAT proof.'}
(root/'AUDIT.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
