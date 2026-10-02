"""Post-target-data adapter. Independent simultaneous original star solve and exact roots.
No target module is imported; full native result categories are compared as data.
"""
from fractions import Fraction as Q
from math import comb
import json,pathlib,hashlib,sys
P=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(P/'core'))
from original import parameters,phi,need
from optimizer import slope
A=P/'author'
def choose(n,k):return comb(n,k) if 0<=k<=n else 0
def solve(rows):
 M=[row[:] for row in rows];n=len(M)
 for j in range(n):
  p=max(range(j,n),key=lambda i:abs(M[i][j]));need(M[p][j]!=0,'full-rank singleton system');M[p],M[j]=M[j],M[p]
  pivot=M[j][j];M[j]=[x/pivot for x in M[j]]
  for i in range(n):
   if i!=j:
    w=M[i][j]
    if w:M[i]=[x-w*y for x,y in zip(M[i],M[j])]
 return [row[-1] for row in M]
def table(n):
 doc=json.loads((A/f'fixtures/n{n}.json').read_text());r=n-2;s=2**(n-1)-n
 pairs=[(a,b) for a in range(2,r+1) for b in range(a,r+1) if a+b<=n]
 need(doc['free_pairs']==[list(x) for x in pairs],'complete original free-pair census')
 B={(a,b):Q(v) for (a,b),v in zip(pairs,doc['free_values'])};need(len(B)==len(pairs)==len(doc['free_values']),'all free values')
 def val(a,b):return B.get(tuple(sorted((a,b))),Q(0))
 rows=[]
 for a in range(1,r+1):
  coefficients=[]
  for j in range(1,r+1):
   b=j if a==1 else 1 if j==a else None
   coefficients.append(Q(b*choose(n-a,b)) if b else Q(0))
  rhs=(n-a)*s-sum(b*val(a,b)*choose(n-a,b) for b in range(2,r+1))
  rows.append(coefficients+[Q(rhs)])
 for a,v in enumerate(solve(rows),1):B[1,a]=v
 need(all(sum(b*val(a,b)*choose(n-a,b) for b in range(1,r+1))==(n-a)*s for a in range(1,r+1)),'every decoded star row')
 return doc,val

def dual(n,k,lam):
 s,h,N,r,Z,T,K,G,c=parameters(n,k);eps=Q(n*n*r*r,4*(r+Z)**2);need(lam>eps,'global root endpoint threshold');rows=[]
 for a in range(k+1,n-k):
  if lam>=a*(n-a):lo=hi=Q(0)
  else:
   l=0;u=Z*2**44
   while u-l>1:
    idx=(u+l)//2
    if slope(n,a,Q(idx,2**44))>lam:l=idx
    else:u=idx
   lo=Q(l,2**44);hi=Q(u,2**44)
   need(slope(n,a,lo)>lam>=slope(n,a,hi),'unique exact literal-grid root bracket')
  v=Q(n)*hi/(2*(r+hi));t=-Q(2*a-n,2)*hi/(N-hi);f=a-v-t;fc=n-a-v+t;w=f*fc;cost=r*v*v+N*t*t
  need(w<=lam and f>0 and fc>0,'whole arbitrary-real coefficient witness')
  rows.append(dict(a=a,lo=lo,hi=hi,v=v,t=t,f=f,fc=fc,w=w,cost=cost))
 by={q['a']:q for q in rows};need(all(p['f']<q['f'] for p,q in zip(rows,rows[1:])),'strict whole f monotonicity')
 need(all(q['hi']==by[n-q['a']]['hi'] and q['v']==by[n-q['a']]['v'] and q['t']==-by[n-q['a']]['t'] for q in rows),'every complementary profile convention')
 b=c+lam*T+sum(comb(n,q['a'])*q['cost'] for q in rows)
 weights=[(a,b,1-by[a]['f']*by[b]['f']/lam) for a in by for b in by if a<=b and a+b<n];need(all(0<q<1 for a,b,q in weights),'all proper-pair weights')
 maxrho=max([q for a,b,q in weights],default=Q(0));floor=-b/(2*h*lam*maxrho) if b<0 and maxrho else None
 lo_mass=sum(comb(n,q['a'])*q['lo'] for q in rows);hi_mass=sum(comb(n,q['a'])*q['hi'] for q in rows)
 return dict(bound=b,rows=rows,by=by,maxrho=maxrho,floor=floor,hi_mass=hi_mass,lo_mass=lo_mass)
def compare():
 expected=json.loads((A/'expected.json').read_text());out={};allprofiles=[];decoded=0
 layers=[]
 for record in expected['credited_complete_layer_controls']:
  n=record['n'];k=record['k'];lam=Q(record['lambda']);s,h,N,r,Z,T,K,G,c=parameters(n,k);doc,B=table(n);q=dual(n,k,lam);by=q['by'];sizes=range(1,n-1);bulk=range(k+1,n-k)
  u={a:Q(a) if a<=k else Q(s*(n-a),h) if a>=n-k else by[a]['v']+by[a]['t'] for a in sizes};ell={a:Q(0 if a<=k else 2 if a>=n-k else 1) for a in sizes}
  upper=h*sum(comb(n,a)*u[a]**2 for a in sizes)-sum(comb(n,a)*choose(n-a,b)*u[a]*u[b]*B(a,b) for a in sizes for b in sizes)
  lower=s*sum(comb(n,a)*ell[a]**2 for a in sizes)-sum(comb(n,a)*ell[a] for a in sizes)**2+sum(comb(n,a)*choose(n-a,b)*ell[a]*ell[b]*B(a,b) for a in sizes for b in sizes)
  term=sum(comb(n,a)*(by[a]['w']-lam)*(s-B(a,n-a)) for a in bulk)
  proper=sum(comb(n,a)*choose(n-a,b)*(lam-by[a]['f']*by[b]['f'])*B(a,b) for a in bulk for b in bulk if a+b<n)
  mass=sum(comb(n,a)*choose(n-a,b)*max(Q(0),B(a,b)) for a in bulk for b in bulk if a+b<n)/(2*h)
  need(upper+lam*lower==q['bound']+term+proper,'complete decoded original energies')
  row=dict(n=n,k=k,credited_construction_cutoff=doc['proper_support_cutoff'],seed_sha256=hashlib.sha256((A/f'fixtures/n{n}.json').read_bytes()).hexdigest(),lambda_=str(lam),upper_energy=str(upper),lower_energy=str(lower),bound=str(q['bound']),deficit_term=str(term),proper_term=str(proper),positive_original_mass=str(mass),signed_weighted_original_mass=str(proper/(2*h*lam)),exact_mass_floor=str(q['floor']))
  row['lambda']=row.pop('lambda_');need(row==record,'ALL native credited-layer fields');layers.append(row);decoded+=(n-2)**2;allprofiles.append(q)
 out['credited_complete_layer_controls']=layers
 comparisons=[]
 for record in expected['fixed_profile_comparisons']:
  n=record['n'];k=record['k'];lam=Q(record['lambda']);s,h,N,r,Z,T,K,G,c=parameters(n,k);mu=Q((2*n-5)**2,16);q=dual(n,k,lam)
  prior=c+mu*T+r*sum(comb(n,a)*max(Q(0),Q(5,4)-Q((2*a-n)**2,4*n))**2 for a in range(k+1,n-k))
  row=dict(n=n,k=k,lambda_=str(lam),credited_fixed_eta=str(prior),new_safe_bound=str(q['bound']),positive_original_mass_floor=str(q['floor']),proper_weight_maximum=str(q['maxrho']),scope=record['scope']);row['lambda']=row.pop('lambda_');need(prior>=0 and q['bound']<0 and row==record,'ALL native fixed-comparison fields');comparisons.append(row);allprofiles.append(q)
 out['fixed_profile_comparisons']=comparisons
 schedules=[];frontiers=[]
 for record in expected['strict_partial_schedules']:
  n=record['n'];k=record['k'];lam=Q(record['lambda']);s,h,N,r,Z,T,K,G,c=parameters(n,k);q=dual(n,k,lam);delta=Q(1,4*n*n);theta=(T*(1-delta)-delta*G)/q['hi_mass'];zs={a:delta+theta*z['hi'] for a,z in q['by'].items()};energy=c+sum(comb(n,a)*phi(n,a,z) for a,z in zs.items());mass=sum(comb(n,a)*z for a,z in zs.items());gam=sum(comb(n,a)*z/(2*s-z) for a,z in zs.items())
  pin=hashlib.sha256(json.dumps({str(a):str(z) for a,z in zs.items()},sort_keys=True,separators=(',',':')).encode()).hexdigest()
  row=dict(n=n,k=k,lambda_=str(lam),delta_floor=str(delta),theta=str(theta),energy=str(energy),lower_budget_slack=str(T-mass),free_lower_curvature_slack=str(2-gam),profile_sha256=pin,is_H=False);row['lambda']=row.pop('lambda_');need(row==record and energy>0 and gam<2 and all(0<z<Z for z in zs.values()),'ALL native strict-schedule fields');schedules.append(row)
  predecessor=dual(n,k-1,lam);f=next(x for x in expected['sharp_scalar_frontiers'] if x['n']==n);fr=dict(n=n,first_positive_relaxed_cutoff=k,lower_cutoff=k-1,lambda_=str(lam),negative_lower_bound=str(predecessor['bound']),strict_profile_sha256=pin,scope=f['scope']);fr['lambda']=fr.pop('lambda_');need(fr==f and predecessor['bound']<0,'ALL native relaxation-frontier fields');frontiers.append(fr);allprofiles.extend([q,predecessor])
 out['strict_partial_schedules']=schedules;out['sharp_scalar_frontiers']=frontiers
 compression=[]
 for record in expected['complete_cap_compression_controls']['credited_layers']:
  n=record['n'];k=record['k'];s,h,N,r,Z,T,K,G,c=parameters(n,k);doc,B=table(n);zs={a:s-B(a,n-a) for a in range(k+1,n-k)};E=c+sum(comb(n,a)*phi(n,a,z) for a,z in zs.items());even=E+sum(comb(n,a)*Q(2*a-n,2)**2*z*z/(N-z) for a,z in zs.items());mass=sum(comb(n,a)*z for a,z in zs.items());controls=[]
  for perturb in [False,True]:
   u={a:Q(a) for a in range(1,n-1)}
   for a in range(n-k,n-1):u[a]=Q(s*(n-a),h)+(Q(a-n+k+1,7) if perturb else 0)
   for a,z in zs.items():u[a]=Q(n)*z/(2*(r+z))-Q(2*a-n,2)*z/(N-z)+(Q((2*a-n)**2+3,13)+Q(2*a-n,11) if perturb else 0)
   energy=h*sum(comb(n,a)*u[a]**2 for a in u)-sum(comb(n,a)*choose(n-a,b)*B(a,b)*u[a]*u[b] for a in u for b in u)
   controls.append(dict(perturbed=perturb,energy=str(energy),squares=str(energy-E)))
  row=dict(n=n,k=k,seed_sha256=hashlib.sha256((A/f'fixtures/n{n}.json').read_bytes()).hexdigest(),compressed_upper_minimum=str(E),complement_even_minimum=str(even),odd_refinement=str(even-E),lower_budget_slack=str(T-mass),controls=controls);need(row==record,'ALL native credited-compression fields');compression.append(row)
 out['credited_cap_compression']=compression;out['decoded_table_positions_in_six_layer_cases']=decoded;out['exact_profile_cases']=len(allprofiles)
 stream=json.dumps([{key:str(value) for key,value in row.items()} for q in allprofiles for row in q['rows']],sort_keys=True,separators=(',',':')).encode();out['entire_exact_profile_field_stream']=dict(bytes=len(stream),sha256=hashlib.sha256(stream).hexdigest(),rows=sum(len(q['rows']) for q in allprofiles),fields=sum(len(row) for q in allprofiles for row in q['rows']))
 return out
if __name__=='__main__':
 out=json.dumps(compare(),indent=2,sort_keys=True)+'\n';(P/'COMMON.json').write_text(out);print(json.dumps(dict(bytes=len(out.encode()),sha256=hashlib.sha256(out.encode()).hexdigest(),categories=5)))
