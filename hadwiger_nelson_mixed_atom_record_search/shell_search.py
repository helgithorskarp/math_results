"""One-step exact circle-intersection augmentation of a specified physical seed."""
from field_contact import *
from geometry50 import Geometry
from math import comb
import random
import hashlib

def stream_hash(x):
 return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def checked_colouring(colour,n,edges):
 require(len(colour)==n and all(c in '0123'for c in colour),'malformed certificate')
 require(all(colour[a]!=colour[b]for a,b in edges),'invalid shell certificate')

def reject_bad_colouring(colour,n,edges):
 try:checked_colouring(colour,n,edges)
 except ValueError:return
 raise ValueError('bad colouring accepted')

def fixture_seed(tag):
 from build_sources import canon
 fixture=json.loads((Path(__file__).resolve().parent/'fixtures.json').read_text())[tag]
 if fixture['P_form']=='G_plus_uGbar_canonical_reflection':
  u=tuple(map(F,fixture['u']));Q={add(a,mul(u,K.conj(b)))for a,b in product(golomb(),repeat=2)}
  P=[(p,ZERO)for p in min(canon(Q),canon([K.conj(p)for p in Q]))]
 elif fixture['P_form']=='three_M_canonical':
  Q={ZERO}
  for _ in range(3):Q={add(a,b)for a,b in product(Q,spindle())}
  P=[(p,ZERO)for p in min(canon(Q),canon([K.conj(p)for p in Q]))]
 elif fixture['P_form']=='G_plus_uM':
  u=tuple(tuple(map(F,z))for z in fixture['u']);P=sorted({eadd((a,ZERO),ecscale(u,b))for a,b in product(golomb(),spindle())})
 else:raise ValueError('unknown fixture construction')
 v=tuple(tuple(map(F,z))for z in fixture['v']);s=tuple(map(F,fixture['radicand']))
 labels=[eadd(p,ecscale(v,c))for p,c in product(P,spindle())]
 return s,labels,fixture['seed_colour_word'],fixture['seed_edges'],fixture

class Extension(Field):
 def __init__(self,s):
  self.s=s;self.zero=(ZERO,ZERO);self.one=(ONE,ZERO)
 def real_inv(self,z):
  a,b=z;require(a[2:]==b[2:]==(0,0),'nonreal inverse');q=K.inverse_real(sub(mul(a,a),mul(self.s,mul(b,b))));return mul(a,q),scale(mul(b,q),-1)
 def sign(self,z):
  a,b=z;sa,sb=sign(a),sign(b)
  if not sa:return sb
  if not sb:return sa
  return sa if sa==sb else sa*sign(sub(mul(a,a),mul(self.s,mul(b,b))))
 def sqrt(self,z):
  a,b=z;require(a[2:]==b[2:]==(0,0),'nonreal square root')
  if b==ZERO:
   q=K.sqrt_real(a)
   if q is not None:return(q,ZERO)
   q=K.sqrt_real(mul(a,K.inverse_real(self.s)))
   return None if q is None else(ZERO,q)
  disc=K.sqrt_real(sub(mul(a,a),mul(self.s,mul(b,b))))
  if disc is None:return None
  for eps in(-1,1):
   c=K.sqrt_real(scale(add(a,scale(disc,eps)),F(1,2)))
   if c is not None and c!=ZERO:
    z0=(c,scale(mul(b,K.inverse_real(c)),F(1,2)));require(self.mul(z0,z0)==z,'square root identity');return z0
  return None

def main_seed(index,record_index):
 W=workdir();sources=json.loads((W/'sources.json').read_text());source=sources[index];rr=json.loads((W/f'result_{index}.json').read_text());r=next(r for r in rr['results']if r['index']==record_index);T,J=[tuple(map(F,x))for x in r['key']];P=[tuple(map(F,x))for x in source['P']];C=spindle()if source['C']=='M'else golomb()
 for a,b in product(K.differences(P),K.differences(C)):
  if a==ZERO or b==ZERO:continue
  ci=inv(mul(K.conj(a),b));S=sub(add(norm(a),norm(b)),ONE)
  if scale(mul(S,ci),-1)!=T or mul(mul(a,K.conj(b)),ci)!=J:continue
  ss=scale(sub(scale(mul(norm(a),norm(b)),4),mul(S,S)),F(1,3));v=(scale(T,F(1,2)),scale(mul(ALPHA,ci),F(1,2)));pts=[eadd((p,ZERO),ecscale(v,c))for p,c in product(P,C)];return ss,pts,rr['colour_library'][r['row']],r['edges']
 raise ValueError('contact witness missing')

def field_seed(d,kind,k):
 W=workdir();r=json.loads((W/f'field_result_{d}_{kind}.json').read_text());P=[(tuple(map(F,p[:4])),tuple(map(F,p[4:])))for p in r['P']];C=[tuple(map(F,c))for c in r['C']];record=r['records'][k];v=tuple(tuple(map(F,x))for x in record['v']);pts=[eadd(p,ecscale(v,c))for p,c in product(P,C)];return scale(ONE,d),pts,r['colour_library'][record['row']],record['edges']

def run(mode,arg1,arg2):
 W=workdir();st=time.time()
 fixture=None
 if mode=='fixture':s,labels,word,ne,fixture=fixture_seed(arg1);tag=arg1
 elif mode=='main':s,labels,word,ne=main_seed(int(arg1),int(arg2));tag=f'main_{arg1}_{arg2}'
 else:d,kind=arg1.split('_');s,labels,word,ne=field_seed(int(d),kind,int(arg2));tag=f'field_{arg1}_{arg2}'
 X=Extension(s);pts=sorted(set(labels));ix={p:i for i,p in enumerate(pts)};col=[None]*len(pts)
 for p,c in zip(labels,word):require(col[ix[p]]is None or col[ix[p]]==c,'seed collision colour');col[ix[p]]=c
 geo=Geometry(W/'geometry.so');es=geo.graph(pts,s);require(len(es)==ne,'seed edge count');require(all(col[a]!=col[b]for a,b in es),'seed physical colour')
 # Exact real square-root controls include rational and extension components.
 rng=random.Random(20260913)
 for _ in range(60):
  z=tuple((F(rng.randrange(-5,6)),F(rng.randrange(-5,6)),F(0),F(0))for j in range(2));q=X.sqrt(X.mul(z,z));require(q is not None and X.mul(q,q)==X.mul(z,z),'extension square control')
 old=set(pts);pairs={};roots={};n=len(pts)
 for i,j in combinations(range(n),2):
  delta=esub(pts[j],pts[i]);nn=X.norm(delta)
  if nn not in roots:
   if X.sign(esub((scale(ONE,4),ZERO),nn))<0:roots[nn]=None
   else:roots[nn]=X.sqrt(ecscale(esub(ecscale(X.real_inv(nn),scale(ONE,4)),X.one),scale(ONE,F(1,3))))
  z=roots[nn]
  if z is None:continue
  mid=ecscale(eadd(pts[i],pts[j]),scale(ONE,F(1,2)));tail=ecscale(X.mul(delta,z),scale(ALPHA,F(1,2)))
  for eps in((-1,1)if z!=X.zero else(1,)):
   q=eadd(mid,ecscale(tail,scale(ONE,eps)))
   if q in old:continue
   if q not in pairs:pairs[q]=[0,(i,j)]
   pairs[q][0]+=1
 print('SHELL_INVENTORY',tag,'seed',n,ne,'distinct_external',len(pairs),'degree4_candidates',sum(v[0]>=6 for v in pairs.values()),'seconds',time.time()-st,flush=True)
 extra=sorted(q for q,(cnt,pair)in pairs.items()if cnt>=6);edges=list(es);degrees=[]
 # Check exact distances independently of multiplicity, including every seed vertex.
 for k,q in enumerate(extra):
  nbr=[i for i,p in enumerate(pts)if X.norm(esub(p,q))==X.one];require(len(nbr)>=4 and comb(len(nbr),2)==pairs[q][0],'circle multiplicity');degrees.append(len(nbr));edges.extend((i,n+k)for i in nbr)
  for j,r in enumerate(extra[:k]):
   if X.norm(esub(q,r))==X.one:edges.append((n+j,n+k))
 print('SHELL_GRAPH',tag,'vertices',n+len(extra),'edges',len(edges),'added_degrees',dict(Counter(degrees)),'seconds',time.time()-st,flush=True)
 physical=pts+extra
 actual=geo.graph(physical,s)
 require(actual==sorted(edges),'shell complete physical edge disagreement')
 if fixture is None:status,colour,stats=solve(edges,n+len(extra),1000000)
 else:
  colour=fixture['shell_colour_word'];stats={};status='SAT'
  checked_colouring(colour,len(physical),actual)
  reject_bad_colouring('0'*len(physical),len(physical),actual)
  reject_bad_colouring(colour[:-1],len(physical),actual)
 out={'tag':tag,'radicand':list(map(str,s)),'seed_vertices':n,'seed_edges':ne,'external_intersections':len(pairs),'added_vertices':len(extra),'added_degree_counts':dict(Counter(degrees)),'vertices':n+len(extra),'edges':len(edges),'status':status,'solver_stats':stats,'colouring':colour,'points':[[str(x)for z in p for x in z]for p in pts+extra],'edge_list':sorted(edges),'seconds':time.time()-st}
 if fixture is not None:
  for key,value in fixture['expected'].items():require(json.loads(json.dumps(out[key]))==value,'fixture census mismatch: '+key)
  require(stream_hash(out['points'])==fixture['point_stream_sha256'],'point stream mismatch')
  require(stream_hash(out['edge_list'])==fixture['edge_stream_sha256'],'edge stream mismatch')
 (W/f'shell_{tag}.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('SHELL_DONE',tag,status,stats,'seconds',time.time()-st,flush=True)
if __name__=='__main__':run(*sys.argv[1:])
