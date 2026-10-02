"""Own complete original star system and physical harmonic forms.

Exact225-coordinate public seed is author mathematical input; no author imports.
Old reviewer original-allocation guards are not touched. No n32 dense matrix.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
from linear import need,canonical,digest,mv,psd,inverse
ROOT=Path(__file__).resolve().parent

def choose(n,k):return comb(n,k)if 0<=k<=n else 0

def domain(n):need(type(n)is int and n in [6,32],'ONLY chosen original n6/n32 domains')
def constants(n):
 domain(n);r=n-2;N=2**n-n-1;s=2**(n-1)-n;return r,N,s,N-s

def pairs(n):
 r,N,s,h=constants(n);return[(a,b)for a in range(1,r+1)for b in range(a,r+1)if a+b<=n]

def complete(n,free):
 r,N,s,h=constants(n);supported=pairs(n);wanted=[p for p in supported if p[0]>=2];need(sorted(free)==wanted,'ENTIRE free supported coordinate census');need(all(type(v)is int or isinstance(v,F)for v in free.values()),'exact rational seed')
 # Solve ALL singleton unknowns simultaneously from actual point-star rows.
 unknown=[(1,b)for b in range(1,r+1)];A=[];rhs=[]
 for a in range(1,r+1):
  row=[F(0)]*r;target=F((n-a)*s)
  for b in range(1,r+1):
   key=tuple(sorted((a,b)));factor=b*choose(n-a,b)
   if key in free:target-=factor*free[key]
   elif key in unknown:row[unknown.index(key)]+=factor
   else:need(factor==0,'unsupported star contribution')
  A.append(row);rhs.append(target)
 sol=mv(inverse(A),rhs);beta={p:F(v)for p,v in free.items()};beta.update(dict(zip(unknown,sol)));need(sorted(beta)==supported,'all supported decoded coordinates')
 # Independent physical point-star excluded-row equation, different factors.
 checks=[]
 for a in range(1,r+1):
  got=sum(beta.get(tuple(sorted((a,b))),F(0))*choose(n-a-1,b-1)for b in range(1,r+1));need(got==s,'EVERY actual point-star excluded-row action');checks.append(got)
 return beta,{'full_singleton_system_sha256':digest([A,rhs]),'rank':r,'all_star_actions':checks,'whole_supported_table':[[a,b,str(beta[a,b])]for a,b in supported]}

def read_seed(path=ROOT/'seed.json'):
 z=json.loads(Path(path).read_text());need(z['n']==32 and type(z['n'])is int and z['r']==30 and z['N']==4294967263 and z['s']==2147483616,'seed original n32 metadata');need(z['common_denominator']==10**24 and z['proper_support_cutoff']==8 and z['star_only']is True and z['upper_floor']=='1/1024','defining mathematical seed metadata');keys=z['free_pairs'];vals=z['free_values'];wanted=[list(p)for p in pairs(32)if p[0]>=2];need(keys==wanted and len(vals)==len(keys)==225 and all(type(v)is str for v in vals),'ALL ordered original225 rational coordinates');free={tuple(key):F(v)for key,v in zip(keys,vals)};need(all(10**24%v.denominator==0 for v in free.values()),'every exact common denominator');return free

def sector(n,beta,j):
 r,N,s,h=constants(n);need(type(j)is int and 0<=j<=n//2,'exact harmonicdegree');layers=list(range(max(1,j),min(r,n-j)+1));metric=[choose(n-2*j,a-j)for a in layers];need(all(v>0 for v in metric),'every physical norm positive');K=[];U=[]
 for a in layers:
  low=[];cap=[]
  for b in layers:
   dis=(-1)**j*beta.get(tuple(sorted((a,b))),F(0))*choose(n-a-j,b-j);mean=choose(n,b)if j==0 else 0
   low.append(F(s*(a==b)-mean)+dis);cap.append(F(h*(a==b))-dis)
  K.append(low);U.append(cap)
 G=[[metric[i]*v for v in row]for i,row in enumerate(K)];H=[[metric[i]*v for v in row]for i,row in enumerate(U)]
 need(all(A[i][t]==A[t][i]for A in [G,H]for i in range(len(layers))for t in range(len(layers))),'every physical harmonic form symmetric')
 return {'degree':j,'layers':layers,'metric':metric,'K':K,'U':U,'G':G,'H':H,'multiplicity':choose(n,j)-choose(n,j-1)}

def floor(g,d):return psd([[g['H'][i][t]-d*g['metric'][i]*(i==t)for t in range(len(g['layers']))]for i in range(len(g['layers']))])

def lift_rows(n,beta):
 r,N,s,h=constants(n);sizes=[choose(n,a)for a in range(1,r+1)];rows=[F(s-(N-1))+sum(beta.get(tuple(sorted((a,b))),F(0))*choose(n-a,b)for b in range(1,r+1))for a in range(1,r+1)];empty=1+sum(w*x for w,x in zip(sizes,rows));entries=[1-x for x in rows]
 # Every original layer row and empty row of actual L sum to N.
 need(empty+sum(w*x for w,x in zip(sizes,entries))==N,'actual empty full row equation');need(all(1-row+(N-1)+row==N for row in rows),'all nonempty row equations')
 return {'all_core_constant_rows':rows,'all_actual_empty_L_entries':entries,'actual_empty_L_loop':empty,'actual_empty_M_loop':(empty-s)/h,'N':N,'s':s,'h':h}

def mass(n,beta,k):
 r,N,s,h=constants(n);classes=[]
 for (a,b),v in sorted(beta.items()):
  if a<k or b<k or a+b>=n or v<=0:continue
  count=choose(n,a)*choose(n-a,b)
  if a==b:need(count%2==0,'literal unordered diagonal class parity');count//=2
  classes.append({'a':a,'b':b,'count':count,'original_M_entry':v/h,'mass':count*v/h})
 return {'all_positive_original_classes':classes,'total_mass':sum(t['mass']for t in classes),'scope':'ALL unordered ORIGINAL proper disjoint pairs both sizes>=k'}

def audit():
 n=32;free=read_seed();beta,decode=complete(n,free);r,N,s,h=constants(n);bulk=[p for p in free if p[0]>=9 and sum(p)<32];need(len(bulk)==56 and all(beta[p]==0 for p in bulk),'everyS8 proper bulk zero');need(len(free)-len(bulk)==169 and len(beta)==255,'entire S8 architecture')
 rows=[];orders=[];dim=0;null=0;refinement=[]
 for j in range(17):
  g=sector(n,beta,j);d=len(g['layers']);lower=psd(g['G']);upper=floor(g,F(1,1024));need(lower['rank']==d-int(j in [0,1])and upper['rank']==d,'ALL original lower ranks/full cap floors')
  ker=[F(a)for a in g['layers']]if j==0 else[F(1)]*d if j==1 else None
  if ker is not None:need(not any(mv(g['K'],ker)),'EVERY forced lower harmonic kernel row')
  orders.append(d);dim+=d*g['multiplicity'];null+=(d-lower['rank'])*g['multiplicity']
  rows.append({'degree':j,'layers':g['layers'],'metric':g['metric'],'multiplicity':g['multiplicity'],'lower':lower,'original_cap_floor_certificate':upper,'whole_coefficient_fields_sha256':digest([g['K'],g['U'],g['G'],g['H']])})
  # One exact specified stronger floor; no threshold hunt or optimum inference.
  strong=floor(g,F(1,512));need(strong['rank']==d,'NEW doubled full cap floor');refinement.append({'degree':j,'full_shifted_upper':strong})
 need(orders==[30,30,29,27,25,23,21,19,17,15,13,11,9,7,5,3,1]and dim==N-1 and null==32,'complete ORIGINAL harmonic dimensions/nullity')
 li=lift_rows(n,beta);need(li['actual_empty_L_loop']==F(76835252354714493188190030403,31250000000000000000),'original empty diagonal');ma=mass(n,beta,8);need(ma['total_mass']==F(85123475537199307595320786983,107374182350000000000000000000)and ma['total_mass']>F(1,2048)and all(t['a']==8 or t['b']==8 for t in ma['all_positive_original_classes']),'entire original mass/class scope')
 ordinary={(a,b):F(0)for a,b in pairs(n)if a>=2}
 for a,b in ordinary:
  if a+b==n:ordinary[a,b]=s-1
 reference_beta,reference=complete(n,ordinary);reference_forms=[]
 for j in range(17):
  rg=sector(n,reference_beta,j);low=psd(rg['G']);need(low['rank']==len(rg['layers'])-int(j in[0,1]),'ALL ordinary8106 reference lower ranks');up=psd(rg['H'])if j else None
  if j:need(up['rank']==len(rg['layers']),'ALL sixteen ordinary8106 reference nonmean cap ranks')
  reference_forms.append({'degree':j,'lower':low,'nonmean_cap':up,'whole_coefficient_fields_sha256':digest([rg['K'],rg['U'],rg['G'],rg['H']])})
 ordinary_cap_mean=sector(n,reference_beta,0)['U'][0][0];need(ordinary_cap_mean==F(-31138511967),'ordinary8106 uncapped reference actual singleton cap coefficient');B=203204256;R=s-12*n*n;need(B==sum(a*a*choose(n,a)for a in range(3,8))and 6*B<=R==2147471328,'imported9471 n32 control scalar');
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','original_seed_sha256':digest([[a,b,str(v)]for(a,b),v in sorted(free.items())]),'decoder':decode,'supported_pairs':len(beta),'bulk_zero_pairs':bulk,'active_free_count':169,'all17_full_sector_certificates':rows,'whole_core_dimension':dim,'whole_core_nullity':null,'greatest_original_lower_rank':N-32,'original_cap_rank':N-1,'noncentered':any(li['all_core_constant_rows']),'lift':li,'original_positive_mass':ma,'new_doubled_cap_floor':F(1,512),'all17_new_full_cap_certificates':refinement,'whole_unit_gap_new':F(1,512*h),'all17_ordinary_uncapped_reference_sectors':reference_forms,'ordinary_uncapped_reference_U0_singleton':ordinary_cap_mean,'imported_necessity_control':{'B':B,'R':R,'6B':6*B,'trust':'9471 all-realS7 exclusion with sufficient9513 scoped prior audit, not rerun/global reassessed here'},'scope':'No literaln32 originalallocation. Complete ordinary harmonic/lift/rank bridge in PROOF.md; mathematicalseed explicitauthorinput, owncode noauthorimports. New same-seedgap ONLY, not optimum/alln/fixedcenteredfeasibility.'}

if __name__=='__main__':
 import signal
 def alarm(*args):raise TimeoutError('fixed45s wholeexactsectorphase; incomplete is not exclusion')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(45);print(json.dumps(canonical(audit()),sort_keys=True,separators=(',',':')))
