from atoms import *
from itertools import permutations
W=workdir()

def solve(es,n,budget=100000):
 from pysat.solvers import Solver
 adj=[set()for _ in range(n)]
 for a,b in es:adj[a].add(b);adj[b].add(a)
 tri=next((a,b,min(adj[a]&adj[b]))for a,b in es if adj[a]&adj[b])
 clauses=[[4*i+c+1 for c in range(4)]for i in range(n)]+[[-4*a-c-1,-4*b-c-1]for a,b in es for c in range(4)]+[[4*v+c+1]for c,v in enumerate(tri)]
 with Solver(name='cadical195',bootstrap_with=clauses)as s:
  s.conf_budget(budget);r=s.solve_limited();stats=s.accum_stats()
  if r:
   model=set(s.get_model());word=''.join(str(next(c for c in range(4) if 4*i+c+1 in model))for i in range(n));require(all(word[a]!=word[b]for a,b in es),'bad decoded colouring');return 'SAT',word,stats
  return 'UNSAT'if r is False else 'UNKNOWN',None,stats

def geometry_case(key,g,P,C):
 T,J=key; a,b=g['witness'];ci=inv(mul(K.conj(a),b));v=(scale(T,F(1,2)),scale(mul(ALPHA,ci),F(1,2)));ss=g['ss']
 for signum in(-1,1):
  vv=(v[0],scale(v[1],signum));require(emul(vv,econj(vv),ss)==(ONE,ZERO),'phase norm');require(eadd(esub(emul(vv,vv,ss),ecscale(vv,T)),(J,ZERO))==(ZERO,ZERO),'phase polynomial')
 cm=[ecscale(v,c)for c in C];pts=[(add(p,z[0]),z[1])for p,z in product(P,cm)];require(len(set(pts))==len(pts),'unexpected point collision')
 return v,ss,pts

def source_run(index):
 sources=json.loads((W/'sources.json').read_text());source=sources[index];P=[tuple(map(F,p))for p in source['P']];C={'M':spindle(),'G':golomb(),'Gbar':[K.conj(g)for g in golomb()]}[source['C']];m=len(C);n=len(P)*m;require(n<=508,'vertex budget');st=time.time()
 Dp=K.differences(P);Dc=K.differences(C);dp=[x for x in Dp if x!=ZERO];dc=[x for x in Dc if x!=ZERO];Np={a:norm(a)for a in dp};Nc={b:norm(b)for b in dc};shapes={};stats=Counter();groups={}
 vals={x:f_local(x)[0]for x in set(Np.values())|set(Nc.values())}
 for an,bn in product(set(Np.values()),set(Nc.values())):
  S=sub(add(an,bn),ONE)
  if S==ZERO:shapes[an,bn]=('trace_zero',None);continue
  require(vals[an]%2==vals[bn]%2==0,'norm valuation parity');vv=f_local(S)[0]-(vals[an]+vals[bn])//2
  if vv>=-1:shapes[an,bn]=('local_trace',None);continue
  delta=sub(scale(mul(an,bn),4),mul(S,S))
  if sign(delta)<=0:shapes[an,bn]=('nonphysical_or_E',None);continue
  ss=scale(delta,F(1,3))
  shapes[an,bn]=('E',None)if K.sqrt_real(ss)is not None else('event',(S,ss,vv))
 ip={a:inv(a)for a in dp};ic={b:inv(b)for b in dc}
 for a,b in product(dp,dc):
  kind,extra=shapes[Np[a],Nc[b]];stats[kind]+=1
  if kind!='event':continue
  S,ss,vv=extra;ci=mul(K.conj(ip[a]),ic[b]);T=scale(mul(S,ci),-1);J=mul(mul(a,K.conj(b)),ci)
  groups.setdefault((T,J),{'ss':ss,'trace_valuation':vv,'witness':(a,b),'directions':[]})['directions'].append((a,b))
 ep=[(i,j)for i,j in combinations(range(len(P)),2)if norm(sub(P[i],P[j]))==ONE];ec=[(i,j)for i,j in combinations(range(m),2)if norm(sub(C[i],C[j]))==ONE]
 base={(m*i+k,m*j+k)for i,j in ep for k in range(m)}|{(m*k+i,m*k+j)for i,j in ec for k in range(len(P))}
 def residue(x):
  a,b=K.residue(x);return(a&1)+2*(b&1)
 cp=list(map(residue,P));cc=list(map(residue,C));library=[]
 for perm in permutations((1,2,3)):
  f=(0,)+perm;word=''.join(str(a^f[b])for a,b in product(cp,cc));require(all(word[a]!=word[b]for a,b in base),'bad product palette');library.append(word)
 records=[];ranked=[]
 for gi,(key,g)in enumerate(sorted(groups.items())):
  extras=set()
  for a,b in g['directions']:
   for i,ii in Dp[a]:
    for j,jj in Dc[b]:extras.add(tuple(sorted((m*i+j,m*ii+jj))))
  extras-=base;ranked.append((gi,key,g,sorted(extras)))
 ranked.sort(key=lambda z:-len(z[3]));print('SOURCE',index,'n',n,'base',len(base),'quad',len(groups),'max_extra',max((len(x[3])for x in ranked),default=0),'setup_seconds',time.time()-st,flush=True)
 tally=Counter();unresolved=[]
 for gi,key,g,extra in ranked:
  row=next((j for j,w in enumerate(library)if all(w[a]!=w[b]for a,b in extra)),None)
  solver_stats={};bad=sum(not all(w[a]!=w[b]for a,b in extra)for w in library[:6])
  if row is None:
   es=sorted(base|set(extra));status,word,solver_stats=solve(es,n)
   if status=='SAT':library.append(word);row=len(library)-1;tally['solver_words']+=1
   else:
    v,ss,pts=geometry_case(key,g,P,C);out={'source_index':index,'source':source,'key':[[str(x)for x in y]for y in key],'v':[[str(x)for x in y]for y in v],'ss':list(map(str,ss)),'points':[[str(x)for y in p for x in y]for p in pts],'edges':es,'status':status,'stats':solver_stats};(W/f'candidate_{index}_{gi}.json').write_text(json.dumps(out,separators=(',',':'))+'\n');unresolved.append(gi);print('CANDIDATE',index,gi,status,'extra',len(extra),solver_stats,flush=True)
  else:status='SAT';tally['library']+=1
  tally[status]+=1;records.append({'key':[[str(x)for x in y]for y in key],'index':gi,'edges':len(base)+len(extra),'extra_edges':len(extra),'row':row,'status':status,'product_palettes_eliminated':bad,'solver_stats':solver_stats})
  if status=='UNSAT':break
 out={'source_index':index,'vertices':n,'base_edges':len(base),'total_quadratics':len(groups),'direction_filters':dict(stats),'results':sorted(records,key=lambda z:z['index']),'colour_library':library,'tally':dict(tally),'seconds':time.time()-st,'unresolved':unresolved}
 (W/f'result_{index}.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('DONE',index,dict(tally),'words',len(library),'seconds',time.time()-st,flush=True);return out
if __name__=='__main__':source_run(int(sys.argv[1]))
