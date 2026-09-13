"""Exact candidates with two phases outside the base field, in E(sqrt(d))."""
from atoms import *
from contact_search import solve
from itertools import permutations

class Field:
 def __init__(self,d):self.d=d;self.s=scale(ONE,d);self.zero=(ZERO,ZERO);self.one=(ONE,ZERO)
 def mul(self,a,b):return emul(a,b,self.s)
 def norm(self,a):return self.mul(a,econj(a))
 def real_inv(self,z):
  a,b=z;require(a[2:]==b[2:]==(0,0),'nonreal inverse');q=K.inverse_real(sub(mul(a,a),scale(mul(b,b),self.d)));return mul(a,q),scale(mul(b,q),-1)
 def inv(self,z):return self.mul(econj(z),self.real_inv(self.norm(z)))
 def sign(self,z):
  a,b=z;sa,sb=sign(a),sign(b)
  if not sa:return sb
  if not sb:return sa
  if sa==sb:return sa
  return sa*sign(sub(mul(a,a),scale(mul(b,b),self.d)))
 def sqrt(self,z):
  a,b=z;require(a[2:]==b[2:]==(0,0),'nonreal square root')
  if b==ZERO:
   q=K.sqrt_real(a)
   if q is not None:return(q,ZERO)
   q=K.sqrt_real(scale(a,F(1,self.d)))
   return None if q is None else(ZERO,q)
  disc=K.sqrt_real(sub(mul(a,a),scale(mul(b,b),self.d)))
  if disc is None:return None
  for eps in(-1,1):
   c=K.sqrt_real(scale(add(a,scale(disc,eps)),F(1,2)))
   if c is not None and c!=ZERO:
    z0=(c,scale(mul(b,K.inverse_real(c)),F(1,2)))
    require(self.mul(z0,z0)==z,'square root identity');return z0
  return None

def differences(P):
 D={}
 for i,a in enumerate(P):
  for j,b in enumerate(P):D.setdefault(esub(a,b),[]).append((i,j))
 return D

def run(d,kind):
 W=workdir();K2=Field(d);M=spindle();G=golomb();A,B,C=(G,M,M)if kind=='GMM'else(M,M,G)
 u=(scale(ONE,F(7 if d==5 else 5,8)),scale(ALPHA,F(1,8)))
 require(K2.norm(u)==K2.one,'seed phase');P=sorted({eadd((a,ZERO),ecscale(u,b))for a,b in product(A,B)});m=len(C);N=len(P)*m;require(N<=508,'budget');st=time.time()
 DP=differences(P);DC=K.differences(C);dp=[a for a in DP if a!=K2.zero];dc=[b for b in DC if b!=ZERO];NP={a:K2.norm(a)for a in dp};NC={b:(norm(b),ZERO)for b in dc};shapes={};stats=Counter();phases={}
 for an,bn in product(set(NP.values()),set(NC.values())):
  S=esub(eadd(an,bn),K2.one);delta=esub(ecscale(K2.mul(an,bn),scale(ONE,4)),K2.mul(S,S));root=K2.sqrt(ecscale(delta,scale(ONE,F(1,3))))if K2.sign(delta)>=0 else None;shapes[an,bn]=(S,root)
 ia={a:K2.inv(a)for a in dp};ib={b:inv(b)for b in dc};ui=econj(u)
 def put(v,mode,a,b):
  if v[1]==ZERO or K2.mul(v,ui)[1]==ZERO:stats['base_related_phase_equations']+=1;return
  require(K2.norm(v)==K2.one,'candidate unit phase');phases.setdefault(v,{'unit':[],'collision':[]})[mode].append((a,b))
 for a,b in product(dp,dc):
  if NP[a]==NC[b]:put(ecscale(a,scale(ib[b],-1)),'collision',a,b)
  S,root=shapes[NP[a],NC[b]]
  if root is None:continue
  ci=ecscale(econj(ia[a]),ib[b]);base=ecscale(K2.mul(S,ci),scale(ONE,F(-1,2)));tail=ecscale(K2.mul(root,ci),scale(ALPHA,F(1,2)))
  for eps in((-1,1)if root!=K2.zero else(1,)):
   v=eadd(base,ecscale(tail,scale(ONE,eps)));require(K2.norm(eadd(a,ecscale(v,b)))==K2.one,'unit contact identity');put(v,'unit',a,b)
 print('FIELD_INVENTORY',d,kind,'P',len(P),'phases',len(phases),'seconds',time.time()-st,flush=True)
 ep=[(i,j)for i,j in combinations(range(len(P)),2)if K2.norm(esub(P[i],P[j]))==K2.one];ec=[(i,j)for i,j in combinations(range(m),2)if norm(sub(C[i],C[j]))==ONE];base={(m*i+k,m*j+k)for i,j in ep for k in range(m)}|{(m*k+i,m*k+j)for i,j in ec for k in range(len(P))}
 status,cp,_=solve(ep,len(P));require(status=='SAT','coefficient source not four-coloured')
 cc=[(K.residue(x)[0]&1)+2*(K.residue(x)[1]&1)for x in C];library=[]
 for perm in permutations((1,2,3)):
  f=(0,)+perm;w=''.join(str(int(a)^f[b])for a,b in product(cp,cc));require(all(w[a]!=w[b]for a,b in base),'base palette');library.append(w)
 records=[];tally=Counter();ordered=sorted(phases.items(),key=lambda x:-sum(len(DP[a])*len(DC[b])for a,b in x[1]['unit']))
 for k,(v,events)in enumerate(ordered):
  cm=[ecscale(v,c)for c in C];labels=[eadd(p,c)for p,c in product(P,cm)];pts=sorted(set(labels));ix={p:i for i,p in enumerate(pts)};lm=[ix[p]for p in labels];es=set(base)
  for a,b in events['unit']:
   for i,ii in DP[a]:
    for j,jj in DC[b]:es.add(tuple(sorted((m*i+j,m*ii+jj))))
  physical=sorted({tuple(sorted((lm[a],lm[b])))for a,b in es});require(all(a!=b for a,b in physical),'collapsed unit edge')
  colpairs=[(i,ii)for a,b in events['collision']for i0,i1 in DP[a]for j0,j1 in DC[b]for i,ii in[(m*i0+j0,m*i1+j1)]]
  row=next((j for j,w in enumerate(library)if all(w[a]!=w[b]for a,b in es-base)and all(w[a]==w[b]for a,b in colpairs)),None);solverstats={}
  if row is None:
   status,w,solverstats=solve(physical,len(pts))
   if status=='SAT':formal=''.join(w[x]for x in lm);library.append(formal);row=len(library)-1;tally['solver_words']+=1
   else:
    out={'d':d,'kind':kind,'u':[[str(x)for x in z]for z in u],'v':[[str(x)for x in z]for z in v],'points':[[str(x)for z in p for x in z]for p in pts],'edges':physical,'status':status,'solver_stats':solverstats};(W/f'field_candidate_{d}_{kind}_{k}.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('CANDIDATE',d,kind,k,status,len(pts),len(physical),flush=True)
  else:status='SAT';tally['library']+=1
  if row is not None:
   word=library[row];col=[None]*len(pts)
   for i,x in enumerate(lm):require(col[x]is None or col[x]==word[i],'colour collision descent');col[x]=word[i]
   require(all(col[a]!=col[b]for a,b in physical),'physical colouring failure')
  tally[status]+=1;records.append({'v':[[str(x)for x in z]for z in v],'vertices':len(pts),'edges':len(physical),'status':status,'row':row,'solver_stats':solverstats})
  if status=='UNSAT':break
 out={'d':d,'kind':kind,'u':[[str(x)for x in z]for z in u],'P':[[str(x)for z in p for x in z]for p in P],'C':[[str(x)for x in c]for c in C],'phases':len(phases),'records':records,'colour_library':library,'tally':dict(tally),'filter_stats':dict(stats),'seconds':time.time()-st}
 (W/f'field_result_{d}_{kind}.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('FIELD_DONE',d,kind,dict(tally),'seconds',time.time()-st,flush=True)
if __name__=='__main__':run(int(sys.argv[1]),sys.argv[2])
