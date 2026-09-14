"""Standard-library proof replay, without the producer or a SAT library.

Source reconstruction uses square-free real radicals; graph edges use a
separate coefficient equation. Negative evidence is a complete finite search.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
from math import gcd,lcm
from collections import Counter
import argparse,hashlib,json,time,sys

HERE=Path(__file__).resolve().parent
KEEP=(0,5,6,9,12,13,16,17,18,19,20,22,24,25,26,27,28,30,31,33,34,35,36,37,38,39,40,41,42)
R=(1,3,11,33)
def need(ok,msg):
 if not ok:raise ValueError(msg)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def point(x=None,y=None):
 x=x or {};y=y or {}
 return tuple(F(x.get(r,0))for r in R)+tuple(F(y.get(r,0))for r in R)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def conj(x):return x[:4]+tuple(-a for a in x[4:])
def rmul(x,y):
 z=[F(0)]*4
 for i,a in enumerate(x):
  for j,b in enumerate(y):
   if a and b:
    d=gcd(R[i],R[j]);z[R.index(R[i]*R[j]//(d*d))]+=a*b*d
 return tuple(z)
def mul(x,y):
 xx=rmul(x[:4],y[:4]);yy=rmul(x[4:],y[4:])
 return tuple(a-b for a,b in zip(xx,yy))+add(rmul(x[:4],y[4:]),rmul(x[4:],y[:4]))
ZERO=point();ONE=point({1:1})
def ecoord(x):
 need(x[1]==x[2]==x[4]==x[7]==0,'point escaped source field')
 return x[0],x[3],x[5],x[6]
def source():
 omega=point({1:F(1,2)},{3:F(1,2)})
 eta=point({33:F(1,6)},{3:F(1,6)})
 powers=[ONE]
 for _ in range(5):powers.append(mul(powers[-1],omega))
 need(mul(powers[-1],omega)==ONE,'sixth root')
 need(mul(eta,conj(eta))==ONE,'eta unit')
 eta_w2=mul(eta,powers[2])
 seeds=[ONE,add(eta,neg(conj(eta))),add(eta,neg(mul(conj(eta),omega))),eta,
        add(ONE,eta_w2),conj(eta),add(ONE,conj(eta_w2))]
 pool={mul(a,b)for a in seeds for b in powers}
 need(len(pool)==42 and ZERO not in pool,'source coset count')
 full=[ZERO]+sorted(pool,key=ecoord)
 return full,[full[i]for i in KEEP]
def integral(P):
 rows=[ecoord(p)for p in P];den=lcm(*(x.denominator for row in rows for x in row))
 return den,[tuple(int(x*den)for x in row)for row in rows]
def edges(P):
 # x=(a+b sqrt33)/den, y=(c sqrt3+d sqrt11)/den.
 # Independence of 1,sqrt33 gives these two simultaneous equations.
 den,rows=integral(P);es=[]
 for i,x in enumerate(rows):
  for j in range(i):
   a,b,c,d=(u-v for u,v in zip(x,rows[j]))
   if a*a+33*b*b+3*c*c+11*d*d==den*den and a*b+c*d==0:es.append((j,i))
 return es
def unit(z):return mul(z,conj(z))==ONE
def normalized(word):
 seen={};return tuple(seen.setdefault(c,len(seen))for c in word)
def bare_patterns(es,T):
 pos={v:i for i,v in enumerate(T)}
 te=[(pos[u],pos[v])for u,v in es if u in pos and v in pos]
 return sorted({normalized(w)for w in product(range(4),repeat=4)if all(w[a]!=w[b]for a,b in te)})
def check_word(w,n,E,omitted=None):
 need(isinstance(w,str)and len(w)==n,'word length/type')
 for i,c in enumerate(w):need(c=='.'if i==omitted else c in '0123','word alphabet/deletion')
 need(all(w[u]!=w[v]for u,v in E if omitted not in (u,v)),'monochromatic unit edge')
 return tuple(-1 if c=='.'else int(c)for c in w)
def search(n,E,allowed):
 """Complete search over finite colour domains; no symmetry reduction."""
 adj=[[]for _ in range(n)]
 for u,v in E:adj[u].append(v);adj[v].append(u)
 counts={'nodes':0,'conflicts':0}
 def dfs(dom):
  counts['nodes']+=1
  if any(d==0 for d in dom):counts['conflicts']+=1;return None
  queue=[i for i,d in enumerate(dom)if d&(d-1)==0]
  done=set()
  while queue:
   v=queue.pop()
   if v in done:continue
   done.add(v)
   for u in adj[v]:
    new=dom[u]&~dom[v]
    if new!=dom[u]:
     if new==0:counts['conflicts']+=1;return None
     dom[u]=new
     if new&(new-1)==0:queue.append(u)
  pending=[i for i,d in enumerate(dom)if d&(d-1)]
  if not pending:return tuple(d.bit_length()-1 for d in dom)
  v=min(pending,key=lambda i:(dom[i].bit_count(),-len(adj[i]),i))
  choices=dom[v]
  while choices:
   bit=choices&-choices;choices-=bit;child=list(dom);child[v]=bit
   ans=dfs(child)
   if ans is not None:return ans
  return None
 answer=dfs(list(allowed));return answer,counts
def palette_proof(E,N):
 """Four explicit terminal cases; singleton and tight edge palette rules."""
 adj={i:set()for i in range(1,29)}
 for a,b in E:
  if a and b:adj[a].add(b);adj[b].add(a)
 cases=[]
 for bits in product(range(2),repeat=len(N)):
  nc=dict(zip(N,bits))
  if bits[0]or any(nc[a]==nc[b]for a,b in E if a in nc and b in nc):continue
  dom={i:({nc[i]}if i in nc else set(range(4)))for i in adj}
  def singles():
   changed=True
   while changed:
    changed=False
    for a in adj:
     if len(dom[a])==1:
      for b in adj[a]:
       if dom[b]&dom[a]:dom[b]-=dom[a];changed=True
    need(all(dom.values()),'unexpected singleton contradiction')
  singles();steps=[]
  if nc[4]==nc[5]:cycle=[1,11,23]
  else:
   rules=[(16,21,24),(20,26,23)]if nc[22]==0 else [(13,19,23),(20,27,24)]
   for a,b,c in rules:
    pal=dom[a]|dom[b]
    need(b in adj[a]and c in adj[a]&adj[b]and len(pal)==2,'invalid tight-pair rule')
    steps.append([a,b,c,sorted(pal)]);dom[c]-=pal;need(bool(dom[c]),'unexpected pair contradiction');singles()
   need(dom[23]=={1}and dom[24]=={0},'transfer colours')
   cycle=[1,3,2,8,11]
  need(len(cycle)%2==1 and len(set(cycle))==len(cycle),'odd simple cycle')
  need(all(b in adj[a]for a,b in zip(cycle,cycle[1:]+cycle[:1])),'cycle unit edges')
  need(all(dom[v]<=set((2,3))for v in cycle),'cycle not forced to two colours')
  cases.append({'terminal_word':''.join(map(str,bits)),'tight_pairs':steps,'odd_cycle':cycle})
 need(len(cases)==4,'palette case coverage')
 return cases
def run(certificate=None):
 cert_path=certificate or HERE/'certificate.json';cert=json.loads(cert_path.read_text())
 need(set(cert)=={'format','source_word','source_deletions','frames'},'certificate fields')
 need(cert['format']=='literal-colour-words-v1','certificate format')
 full,S=source();FE=edges(full);E=edges(S);N=[i for i,z in enumerate(S)if unit(z)]
 need((len(full),len(FE),len(S),len(E),len(N))==(43,126,29,75,14),'source dimensions')
 need(len(set(S))==len(S),'source collisions')
 fixture=[list(map(int,line.split()))for line in (HERE/'points.tsv').read_text().splitlines()if line and not line.startswith('#')]
 den,coords=integral(S)
 need(den==12 and fixture==[[i]+list(row)for i,row in enumerate(coords)],'readable point fixture')
 base=check_word(cert['source_word'],len(S),E)
 need(len({base[i]for i in N})==3,'base neighbour palette')
 # Delete the centre and forbid colours 2,3 on its neighbours.
 PE=[(u-1,v-1)for u,v in E if u!=0 and v!=0]
 PN=[i-1 for i in N];allowed=[3 if i in PN else 15 for i in range(28)]
 ans,search_counts=search(28,PE,allowed)
 need(ans is None,'three-colour neighbour requirement failed')
 cases=palette_proof(E,N)
 # The induced terminal graph really permits the forbidden palette.
 NE=[(N.index(u),N.index(v))for u,v in E if u in N and v in N]
 twocolour,_=search(len(N),NE,[3]*len(N));need(twocolour is not None,'bare terminals not two-colourable')
 need(len(cert['source_deletions'])==28,'deletion count')
 inequalities=len(E)
 for v,w in enumerate(cert['source_deletions'],1):
  word=check_word(w,len(S),E,v)
  need(word[0]==0 and all(word[i]in (1,2)for i in N if i!=v),'deletion palette')
  inequalities+=sum(v not in e for e in E)
 # Bounded reflected-chord family. All addresses become physical points first.
 rows=cert['frames'];counter=0;orders=Counter();sizes=Counter();pattern_counts=Counter()
 point_hashes=[];edge_hashes=[];pair_checks=43*42//2+29*28//2
 for a,b in combinations(N,2):
  A,B=S[a],S[b];newroot=add(A,B)
  if newroot==ZERO:continue
  need(counter<len(rows),'missing frame');row=rows[counter];counter+=1
  need(set(row)=={'chord','words'}and row['chord']==[a,b],'chord inventory')
  AB=mul(A,B)
  transform=lambda z:add(newroot,neg(mul(AB,conj(z))))
  need(transform(A)==A and transform(B)==B,'chord reflection pins')
  moved=[transform(z)for z in S]
  need(len(set(moved))==len(S),'noninjective copy')
  P=list(S)+sorted(set(moved)-set(S),key=ecoord)
  need(len(P)==len(set(P))and len(P)<=56,'physical quotient')
  es=edges(P);T=(0,P.index(newroot),a,b);need(len(set(T))==4,'terminal collisions')
  patterns=bare_patterns(es,T);ws=row['words']
  need(len(ws)==len(patterns),'boundary witness count')
  for pat,w in zip(patterns,ws):
   word=check_word(w,len(P),es)
   need(tuple(word[i]for i in T)==pat,'boundary pin mismatch')
   inequalities+=len(es)
  need(any(w[T[0]]!=w[T[1]]for w in ws),'centres never distinguished')
  orders[len(P)]+=1;sizes[len(es)]+=1;pattern_counts[len(patterns)]+=1
  point_hashes.append(digest(integral(P)));edge_hashes.append(digest(es));pair_checks+=len(P)*(len(P)-1)//2
 need(counter==len(rows)==86,'extra/missing reflected frame')
 den,coords=integral(S)
 return {'status':'VERIFIED_FROZEN_CENTRE_SOURCE_AND_JOINT_TRANSFER_BOUNDARY',
  'source_order':29,'source_edges':75,'deleted_centre_order':28,'deleted_centre_edges':len(PE),
  'terminal_count':14,'terminal_edges':len(NE),'bare_terminal_two_colouring':list(twocolour),
  'human_palette_cases':cases,
  'forbidden_palette_search':search_counts,'essential_noncentral_vertices':28,
  'source_denominator':den,'source_point_sha256':digest([den,coords]),'source_edge_sha256':digest(E),
  'reflected_frames':counter,'order_histogram':dict(sorted(orders.items())),
  'edge_histogram':dict(sorted(sizes.items())),'boundary_pattern_histogram':dict(sorted(pattern_counts.items())),
  'joint_pattern_frame_pairs':sum(k*v for k,v in pattern_counts.items()),
  'all_pair_distance_checks':pair_checks,'checked_edge_inequalities':inequalities,
  'point_inventory_sha256':digest(point_hashes),'edge_inventory_sha256':digest(edge_hashes),
  'certificate_sha256':hashlib.sha256(cert_path.read_bytes()).hexdigest()}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--check-expected',action='store_true')
 parser.add_argument('--certificate',type=Path);args=parser.parse_args();t=time.monotonic();result=run(args.certificate)
 if args.check_expected:need(json.loads(json.dumps(result))==json.loads((HERE/'expected.json').read_text()),'expected result mismatch')
 print(json.dumps(result,sort_keys=True,indent=2));print('seconds %.3f'%(time.monotonic()-t),file=sys.stderr)
