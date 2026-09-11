#!/usr/bin/env python3
"""Exact certificates and independent coverage checks for the A2 reduction."""
import argparse,copy,hashlib,json
from collections import Counter
from fractions import Fraction
from itertools import combinations,combinations_with_replacement,product
from pathlib import Path
import a2_models as production
from verify import require
from verify_z12_distant_incidence import reconstructed_model,set_checks
from verify_a3 import four_sets_audit,colored_count_controls


def check_certificate(rec,case):
 name,(T,E,eq,eb,ub,bb),objective,meta=case
 require(rec['name']==name,'case name')
 require(rec['dimensions']==[len(T),len(E),len(eq),len(ub)],'model dimensions')
 D=rec['denominator'];require(type(D) is int and D>0,'denominator')
 require(rec['variable_budget']==428,'graph variable budget')
 n=len(T)+len(E);cs=[0]*n;rhs=0
 def twice(a):
  z=2*Fraction(a);require(z.denominator==1,'half-integral coefficient');return z.numerator
 for key,rows,bs in [('equality_multipliers',eq,eb),('inequality_multipliers',ub,bb)]:
  seen=set()
  for row,v in rec[key]:
   require(type(row) is int and 0<=row<len(rows) and row not in seen,'row index')
   require(type(v) is int and (key=='equality_multipliers' or v<=0),'multiplier sign');seen.add(row)
   rhs+=v*twice(bs[row])
   for i,a in rows[row].items():cs[i]+=v*twice(a)
 excess=max([0]+[cs[i]-D*twice(objective[i]) for i in range(n)])
 raw=Fraction(rhs,2*D);err=Fraction(excess,2*D);bound=raw-428*err
 require(raw==Fraction(rec['uncorrected_bound']),'raw bound')
 require(err==Fraction(rec['coefficient_excess']),'column excess')
 require(bound==Fraction(rec['corrected_bound']),'corrected bound')
 require(bound>(1 if any(objective) else 0),'strict exact conclusion')
 return {'name':name,'dimensions':rec['dimensions'],'raw_bound':str(raw),'coefficient_excess':str(err),'exact_bound':str(bound),'certificate_sha256':hashlib.sha256(json.dumps(rec,sort_keys=True,separators=(',',':')).encode()).hexdigest()}


def independent_model(kind,p,profile=None,m=None,k=None):
 # Generate types as bounded multisets. Fill each row from incident edges,
 # independently of the production recursive compositions and column updates.
 r=1 if kind=='one' else 2;nx=1 if kind=='shared' else 2
 sizes=[16-nx+p,26-p,12-r,r];ds=[6,7,8,8]
 if nx-p:sizes.append(nx-p);ds.append(6)
 if p:sizes.append(p);ds.append(7)
 nc=len(ds);T=[]
 for cl,d in enumerate(ds):
  counts=[]
  for word in combinations_with_replacement(range(nc),d):
   ct=Counter(word);v=tuple(ct[a] for a in range(nc));xx=sum(v[4:]);weighted=sum(v[a]*ds[a] for a in range(nc))
   if any(v[a]>sizes[a]-(a==cl) for a in range(nc)) or weighted>53:continue
   if cl==2 and (weighted!=53 or xx!=0):continue
   if cl==3 and (weighted!=(51 if kind=='one' else 52) or xx!=int(kind=='matching')):continue
   if cl>=4 and (v[2]!=0 or v[3]!=int(kind=='matching')):continue
   if kind=='matching':
    if cl==3 and v[3]!=0:continue
    if cl>=4 and xx!=0:continue
    if cl<2 and v[3]*xx!=0:continue
   if profile is not None and d in (6,7) and (d,v[2]+v[3]) not in {(dd,c) for dd,c,num in profile}:continue
   counts.append(v)
  T.extend((cl,v) for v in sorted(counts))
 nt=len(T);edges=[(i,j) for i in range(nt) for j in range(i,nt) if T[i][1][T[j][0]]>0 and T[j][1][T[i][0]]>0]
 incident=[[] for t in T]
 for col,(i,j) in enumerate(edges,nt):
  incident[i].append((col,j))
  if i!=j:incident[j].append((col,i))
 eq=[];eb=[];ub=[];bb=[]
 def add(ex,row,b):
  (eq if ex else ub).append({i:v for i,v in row.items() if v});(eb if ex else bb).append(b)
 for a in range(nc):add(True,{i:1 for i,(cl,v) in enumerate(T) if cl==a},sizes[a])
 for a,b in combinations(range(nc),2):add(True,{i:(cl==a)*v[b]-(cl==b)*v[a] for i,(cl,v) in enumerate(T)},0)
 for a in range(nc):add(False,{i:v[a]*(v[a]-1)+(cl==a)*v[a] for i,(cl,v) in enumerate(T)},sizes[a]*(sizes[a]-1))
 for a,b in combinations(range(nc),2):add(False,{i:v[a]*v[b]+(cl==a)*v[b] for i,(cl,v) in enumerate(T)},sizes[a]*sizes[b])
 for i,(cl,v) in enumerate(T):
  for a in range(nc):
   row={i:-v[a]}
   for col,j in incident[i]:
    if T[j][0]==a:row[col]=1
   add(True,row,0)
   ex=cl==2 or a in (2,3) or (cl==3 and a<4)
   missed=(r if kind=='shared' else 1) if cl>=4 and a==3 else 0
   if cl==3 and a>=4:
    if kind in ('one','shared'):ex=True;missed=sizes[a]
    elif kind=='matching':ex=True;missed=sizes[a]-v[a]
    elif len(ds)==5:ex=True;missed=1
   row={i:v[a]-sizes[a]+missed-(ds[cl]-1)*(cl==a)}
   for col,j in incident[i]:row[col]=T[j][1][a]
   add(ex,row,0)
 inventory={};epssum={};balance={};gap={};negm={}
 for i,(cl,v) in enumerate(T):
  d=ds[cl];c=v[2]+v[3];s=sum(v[a]*(ds[a]-6) for a in range(nc))
  if d==8:
   inventory[i]=Fraction(c,2)+int(c==2);balance[i]=-c*(6-s);negm[i]=-Fraction(c,2)
  else:
   eps=s-(8 if d==6 else 7);epssum[i]=eps;balance[i]=c*eps
   inventory[i]=((c-3)*(c-2) if d==6 else (c-1)*(c-2))//2
   gap[i]=eps**2 if d==6 else eps*(eps-1)
 p7=p*r if kind=='shared' else p
 add(True,inventory,6);add(True,epssum,6);add(True,balance,-p7)
 add(False,gap,(16 if kind=='one' else 18)-4*p7);add(False,negm,-2)
 if profile is not None:
  for d,c,num in profile:add(True,{i:1 for i,(cl,v) in enumerate(T) if ds[cl]==d and v[2]+v[3]==c},num)
  add(True,{i:Fraction(v[2]+v[3],2) for i,(cl,v) in enumerate(T) if ds[cl]==8},m)
  add(True,{i:1 for i,(cl,v) in enumerate(T) if ds[cl]==8 and v[2]+v[3]==2},k)
  b1={};b2={};ct={(d,c):num for d,c,num in profile}
  for i,(cl,v) in enumerate(T):
   if ds[cl]!=7:continue
   c=v[2]+v[3];eps=sum(v[a]*(ds[a]-6) for a in range(nc))-7
   if (c,eps)==(2,2):add(False,{i:1},0)
   if (c,eps)==(1,1):b1[i]=1
   if (c,eps)==(2,1):b2[i]=1
  n5=ct.get((6,5),0);n4=ct.get((6,4),0);n74=ct.get((7,4),0)
  add(False,{**b2,**{i:2 for i in b1}},14*n5+9*n4+3*n74)
  if n5:add(False,b1,7)
  elif n4+n74<2 or (n4==2 and n74==0):add(False,b1,0)
  elif n4==3 and n74==0:add(False,b1,3)
 return sizes,ds,T,edges,eq,eb,ub,bb


def independent_partner():
 sizes=[16,24,9,1,1,1,1,1];ds=[6,7,8,8,8,7,7,8];nc=8
 core=[8,8,7,7,8];adj=[{2,4},{3},{0},{1},{0}];far=[{3},{2}]
 profile=[(6,2,4),(6,3,10),(6,4,2),(7,1,10),(7,2,16)]
 T=[]
 for cl,d in enumerate(ds):
  vectors=[]
  for word in combinations_with_replacement(range(nc),d):
   count=Counter(word);v=tuple(count[a] for a in range(nc));w=sum(v[a]*ds[a] for a in range(nc))
   if w>53 or any(v[a]>sizes[a]-(cl==a) for a in range(nc)):continue
   if cl==2 and (w!=53 or any(v[3:])):continue
   if cl>=3:
    u=cl-3
    if v[2] or any(v[3+j]!=int(j in adj[u]) for j in range(5)):continue
    if core[u]==8 and w!=(52 if u<2 else 53):continue
   high=sum(v[a] for a in range(nc) if ds[a]==8)
   if d==8 and high>1:continue
   if d in (6,7) and (d,high) not in {(a,b) for a,b,n in profile}:continue
   eps=w-6*d-(8 if d==6 else 7)
   if d==7 and ((high,eps)==(1,1) or (high,eps)==(2,2)):continue
   neighbors={a for a in range(5) if v[3+a]};bad=False
   for a,b in combinations(neighbors,2):
    if b in adj[a] or (a<2 and b in far[a]) or (b<2 and a in far[b]):bad=True;break
    existing=adj[a]&adj[b]
    if existing and (cl<3 or cl-3 not in existing):bad=True;break
   if not bad:vectors.append(v)
  T.extend((cl,v) for v in sorted(vectors))
 nt=len(T);edges=[(i,j) for i in range(nt) for j in range(i,nt) if T[i][1][T[j][0]] and T[j][1][T[i][0]]]
 incident=[[] for t in T]
 for col,(i,j) in enumerate(edges,nt):
  incident[i].append((col,j))
  if i!=j:incident[j].append((col,i))
 eq=[];eb=[];ub=[];bb=[]
 def add(ex,row,b):
  (eq if ex else ub).append({i:v for i,v in row.items() if v});(eb if ex else bb).append(b)
 for a in range(nc):add(True,{i:1 for i,(cl,v) in enumerate(T) if cl==a},sizes[a])
 for a,b in combinations(range(nc),2):add(True,{i:(cl==a)*v[b]-(cl==b)*v[a] for i,(cl,v) in enumerate(T)},0)
 for a in range(nc):add(False,{i:v[a]*(v[a]-1)+(cl==a)*v[a] for i,(cl,v) in enumerate(T)},sizes[a]*(sizes[a]-1))
 for a,b in combinations(range(nc),2):add(False,{i:v[a]*v[b]+(cl==a)*v[b] for i,(cl,v) in enumerate(T)},sizes[a]*sizes[b])
 for i,(cl,v) in enumerate(T):
  for a in range(nc):
   row={i:-v[a]}
   for col,j in incident[i]:
    if T[j][0]==a:row[col]=1
   add(True,row,0)
   exact=(a==2 or cl==2);miss=0
   if cl in (3,4,7):
    exact=True;miss=int(cl in (3,4) and a>=3 and a-3 in far[cl-3])
   elif a in (3,4,7):
    exact=True;miss=int(a in (3,4) and cl>=3 and cl-3 in far[a-3])
   row={i:v[a]-sizes[a]+miss-(ds[cl]-1)*(cl==a)}
   for col,j in incident[i]:row[col]=T[j][1][a]
   add(exact,row,0)
 inv={};es={};ce={};gap={}
 for i,(cl,v) in enumerate(T):
  d=ds[cl];c=sum(v[a] for a in range(nc) if ds[a]==8);s=sum(v[a]*(ds[a]-6) for a in range(nc))
  if d==8:inv[i]=Fraction(c,2)+int(c==2);ce[i]=-c*(6-s)
  else:
   e=s-(8 if d==6 else 7);inv[i]=((c-3)*(c-2) if d==6 else (c-1)*(c-2))//2
   es[i]=e;ce[i]=c*e;gap[i]=e**2 if d==6 else e*(e-1)
 add(True,inv,6);add(True,es,6);add(True,ce,-2);add(False,gap,10)
 for d,c,num in profile:add(True,{i:1 for i,(cl,v) in enumerate(T) if ds[cl]==d and sum(v[a] for a in range(nc) if ds[a]==8)==c},num)
 add(True,{i:Fraction(sum(v[a] for a in range(nc) if ds[a]==8),2) for i,(cl,v) in enumerate(T) if ds[cl]==8},4)
 return T,edges,eq,eb,ub,bb


def normalize(x):
 return [{i:v for i,v in z.items() if v} if isinstance(z,dict) else z for z in x]


def model_audit():
 actual=production.m_case()[0];ref=reconstructed_model()
 T,E,eq,eb,ub,bb=ref
 eq.append({i:5-ns[1]-2*ns[2] for i,(d,ns) in enumerate(T) if d==8});eb.append(2)
 for a,b in zip(actual,ref):require(normalize(a)==normalize(b),'ordinary A2 model reconstruction')
 cols=0;count=0
 for name,(T,E,eq,eb,ub,bb),obj,meta in production.cases():
  if meta is None:continue
  kind,p,m,k,prof=meta
  if kind=='partner':rebuild=independent_partner()
  elif kind=='residual':
   rebuild=independent_model('matching',p,prof,m,0)[2:]
   tt,ee,qe,be,qu,bu=rebuild
   qe.append({i:v[2]+v[3] for i,(cl,v) in enumerate(tt) if cl==3});be.append(k)
  else:rebuild=independent_model(kind,p,prof,m,k)[2:]
  for a,b in zip((T,E,eq,eb,ub,bb),rebuild):require(normalize(a)==normalize(b),'colored row reconstruction '+name)
  cols+=len(T)+len(E);count+=1
 return {'ordinary_columns':1710,'colored_models':count,'colored_columns':cols,'independent_types':'neighbor multisets','independent_rows':'direct incident-edge formulas'}


def independent_profiles(p):
 charged=[(6,0,3),(6,1,1),(6,4,1),(6,5,3),(7,0,1),(7,3,1),(7,4,3)]
 found=[]
 for m in range(2,7):
  for k in range(m):
   B=6-m-k
   if B<0:continue
   for length in range(B+1):
    for word in combinations_with_replacement(range(7),length):
     if sum(charged[j][2] for j in word)!=B:continue
     ct=Counter((charged[j][0],charged[j][1]) for j in word)
     if ct[6,1]<2-p:continue
     for n63 in range(17):
      n62=16-sum(v for (d,c),v in ct.items() if d==6)-n63
      if n62<0 or 2*n62+3*n63+sum(c*v for (d,c),v in ct.items() if d==6)!=38+2*m:continue
      for n72 in range(27):
       n71=26-sum(v for (d,c),v in ct.items() if d==7)-n72
       if n71<p or n71+2*n72+sum(c*v for (d,c),v in ct.items() if d==7)!=58-4*m:continue
       whole=ct.copy();whole.update({(6,2):n62,(6,3):n63,(7,1):n71,(7,2):n72})
       found.append((m,k,tuple((d,c,n) for (d,c),n in sorted(whole.items()) if n)))
 return found


def profile_audit():
 records=[];totals=[];arithmetic=[];survive=[]
 for p in range(3):
  pr=list(production.profiles(p));ind=independent_profiles(p)
  require({(m,k,tuple(t)) for m,k,t in pr}==set(ind) and len(pr)==len(ind),'complete integer profile cover')
  n=0
  for i,(m,k,prof) in enumerate(pr):
   ct={(d,c):num for d,c,num in prof};b1=ct.get((7,1),0);n5=ct.get((6,5),0);n4=ct.get((6,4),0);n74=ct.get((7,4),0)
   if n5:b1=min(b1,7)
   elif n4+n74<2 or (n4==2 and n74==0):b1=0
   elif n4==3 and n74==0:b1=min(b1,3)
   pos=0
   for d,c,num in prof:
    lo,hi=(2*c-8,c-2) if d==6 else (2*c-7,c)
    pos+=num*min(max(0,(c-3)*e) for e in range(lo,hi+1))
   lower=18-2*m-min(m,2+k)+p+pos
   upper=min(14*n5+9*n4+3*n74,6+18-4*p+b1,2*b1+ct.get((7,2),0))
   require((lower,upper)==production.bounds(p,m,k,prof),'independent sign bounds')
   if lower<=upper:
    n+=1;records.append({'p':p,'index':i,'m':m,'k':k,'profile':prof,'lower':lower,'upper':upper})
    if (p,i) in production.RESIDUAL_PROFILES:survive.append(records[-1])
  totals.append(len(pr));arithmetic.append(n)
 require(totals==[16,40,94] and arithmetic==[1,5,17],'profile counts')
 return {'all_profile_counts':totals,'after_arithmetic_counts':arithmetic,'arithmetic_excluded':sum(totals)-sum(arithmetic),'certificate_profiles':sum(arithmetic)-len(survive),'remaining_profiles':survive,'cover_sha256':hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()}


def frame_audit():
 # Complete labeled core cover; endpoint labels are not quotiented.
 tally=Counter(high_pair=1)
 for deficit in ((2,),(1,1)):
  r=len(deficit);owners=[i for i,a in enumerate(deficit) for j in range(a)]
  for labels in ((0,0),(0,1)):
   F=[{r+labels[j] for j,t in enumerate(owners) if t==i} for i in range(r)]
   if any(len(F[i])!=deficit[i] for i in range(r)):continue
   nx=max(labels)+1;n=r+nx;pairs=list(combinations(range(n),2))
   for bits in product((0,1),repeat=len(pairs)):
    adj=[set() for _ in range(n)]
    for (a,b),bit in zip(pairs,bits):
     if bit:adj[a].add(b);adj[b].add(a)
    if any(x in adj[t] or adj[t]&adj[x] for t in range(r) for x in F[t]):continue
    if any(len(adj[a]&adj[b])>1 or (b in adj[a] and adj[a]&adj[b]) for a,b in pairs):continue
    if any(len(adj[a]&F[b])!=len(adj[b]&F[a]) for a,b in combinations(range(r),2)):continue
    if r==1:tag='one'
    elif nx==1:tag='shared'
    elif any(adj[t]&set(range(r,n)) for t in range(r)):tag='matching';require(sum(map(len,adj))==4,'two-edge frame')
    else:tag='zero'
    for ds in product((6,7),repeat=nx):tally[tag]+=1
 require(dict(tally)=={'high_pair':1,'one':8,'shared':4,'zero':16,'matching':4},'complete far-core cover')
 return {'labeled_core_cases':sum(tally.values()),'families':dict(tally),'quotient_assumption':'none; merged colors contain all labelings'}


def high_pair_audit():
 # Once c5 / seven-c4 are excluded by the written incidence argument,
 # these exhaust all integer m,k,f with B>=0 and f>=2.
 remaining=[]
 for m in range(2,6):
  for k in range(m+1):
   B=5-m-k;W=22-2*m
   if B<0:continue
   if m>=4:require(W>9*B,'large m contradiction');continue
   for fours in range(2,4):
    if fours>B:continue
    b1=0 if fours==2 else 2 # three fours force the displayed profile's n71=2.
    if W>16+b1:continue
    require((m,k,fours) in ((3,0,2),(2,0,3)),'high-pair equality list')
    # Equality forces ten negative epsilon=-1 c3 six-vertices.
    six_c3=38+2*m-4*fours-2*(16-fours)
    require(six_c3<10,'too few c3 six-vertices')
    remaining.append([m,k,fours,six_c3,10])
 return {'terminal_cases':remaining,'weighted_low_gap_max':10,'required_negative_c3_vertices':10}


def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--certificates',type=Path,required=True);args=parser.parse_args()
 records=json.loads(args.certificates.read_text());cases=list(production.cases());require(len(records)==len(cases)==36,'complete certificate bundle')
 checked=[check_certificate(rec,case) for rec,case in zip(records,cases)]
 bad=[]
 x=copy.deepcopy(records[0]);x['name']='m_at_A3';bad.append((x,cases[0]))
 x=copy.deepcopy(records[1]);x['inequality_multipliers'][0][1]=1;bad.append((x,cases[1]))
 x=copy.deepcopy(records[-1]);x['equality_multipliers'][0][1]+=10**8;bad.append((x,cases[-1]))
 x=copy.deepcopy(records[2]);x['equality_multipliers'].append(x['equality_multipliers'][0]);bad.append((x,cases[2]))
 for rec,case in bad:
  try:check_certificate(rec,case)
  except ValueError:pass
  else:raise ValueError('corrupted certificate accepted')
 output={'claim':'Every z12 A2 graph has two disjoint sink-nonsink-seven paths, both seven endpoints have one six-neighbor, and one of two high-matching profiles; no realization asserted','certificates':checked,'models':model_audit(),'profiles':profile_audit(),'frames':frame_audit(),'high_pair':high_pair_audit(),'four_sets':four_sets_audit(),'colored_controls':colored_count_controls(),'tampered_certificates_rejected':len(bad),'residual_integer_controls':{'rho_values':[0,1,2],'remaining_rho':2,'endpoint_six_neighbor_pairs':[list(x) for x in product(range(1,7),repeat=2) if sum(2-a for a in x)>1]}}
 print(json.dumps(output,indent=2,sort_keys=True))

if __name__=='__main__':main()
