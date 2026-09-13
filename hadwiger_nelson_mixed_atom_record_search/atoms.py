from pathlib import Path
import sys,json,time,os,hashlib
from fractions import Fraction as F
from itertools import product,combinations
from collections import Counter
R=Path(__file__).resolve().parents[1]
pins=json.loads((Path(__file__).resolve().parent/'SOURCE_PINS.json').read_text())
for name,expected_hash in pins['files'].items():
 if hashlib.sha256((R/pins['dependency_directory']/name).read_bytes()).hexdigest()!=expected_hash:
  raise ValueError('arithmetic dependency hash mismatch: '+name)
sys.path.insert(0,str(R/'hadwiger_nelson_independent_moser_sum_collisions'))
from family import *
from local import f_local

def workdir():
 p=Path(os.environ['HN_MIXED_RUN_DIR']).resolve();p.mkdir(parents=True,exist_ok=True);return p

def golomb():
 rows=[(0,0,0,0),(36,0,0,0),(18,0,18,0),(-18,0,18,0),(-36,0,0,0),(-18,0,-18,0),(18,0,-18,0),(6,0,0,2),(-3,-3,3,-1),(-3,3,-3,-1)]
 A=[(F(a,36),F(b,36),F(c,36),F(d,12))for a,b,c,d in rows]
 require(len(set(A))==10,'Golomb points');require(sum(norm(sub(a,b))==ONE for a,b in combinations(A,2))==18,'Golomb edges')
 return A

def phase_inventory(A,B):
 da=sorted({sub(a,b)for a,b in product(A,repeat=2)if a!=b});db=sorted({sub(a,b)for a,b in product(B,repeat=2)if a!=b});na={a:norm(a)for a in da};nb={b:norm(b)for b in db};ia={a:inv(a)for a in da};ib={b:inv(b)for b in db};U=set();stats=Counter()
 shapes={}
 for an,bn in product(set(na.values()),set(nb.values())):
  S=sub(add(an,bn),ONE);delta=sub(scale(mul(an,bn),4),mul(S,S));root=K.sqrt_real(scale(delta,F(1,3)))if sign(delta)>=0 else None
  shapes[an,bn]=(S,root)
 for a,b in product(da,db):
  if na[a]==nb[b]:U.add(scale(mul(a,ib[b]),-1));stats['collision_equations']+=1
  S,root=shapes[na[a],nb[b]]
  if root is None:continue
  ci=mul(K.conj(ia[a]),ib[b]);base=scale(mul(S,ci),F(-1,2));tail=scale(mul(mul(ALPHA,root),ci),F(1,2))
  for eps in((-1,1)if root!=ZERO else(1,)):
   u=add(base,scale(tail,eps));require(norm(u)==ONE,'phase unit');require(norm(add(a,mul(u,b)))==ONE,'unit contact');U.add(u);stats['E_unit_equations']+=1
 out=[]
 for u in sorted(U):
  P=sorted({add(a,mul(u,b))for a,b in product(A,B)});edges=sum(norm(sub(a,b))==ONE for a,b in combinations(P,2));out.append({'u':list(map(str,u)),'vertices':len(P),'edges':edges})
 return {'records':out,'summary':dict(stats,phase_count=len(U),pair_sizes=Counter(r['vertices']for r in out))}
if __name__=='__main__':
 W=workdir();st=time.time();M=spindle();G=golomb();out={}
 for name,A,B in [('GM',G,M),('MM',M,M),('GG',G,G),('GGbar',G,[K.conj(x)for x in G])]:
  z=phase_inventory(A,B);out[name]=z;print(name,z['summary'],'best',sorted([(r['edges'],r['vertices'])for r in z['records']],reverse=True)[:10],time.time()-st,flush=True);(W/'phase_inventory.json').write_text(json.dumps(out,indent=2)+'\n')
