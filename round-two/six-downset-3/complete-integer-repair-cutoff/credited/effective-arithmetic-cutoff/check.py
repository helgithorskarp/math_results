"""Separate sparse arithmetic checks every whole transformation and sign.

Imports the published defining generator, never the new producer or a CAS.
Producer binomial and in-loop quotient reduction are replaced by full Horner
composition and end-of-composition quotient reduction. Same-author checking
is not an independent person review or a formal proof assistant.
"""
from pathlib import Path
from math import comb,gcd
import argparse,copy,hashlib,json,sys
SOURCE=Path(__file__).resolve().parent/'credited/uniform-repair-face'
sys.path.insert(0,str(SOURCE))
import source_gate
source_gate.verify()
import zero_generator
K0=128
ONE={(0,0):1}
def require(c,m):
 if not c:raise ValueError(m)
def clean(p):return {a:v for a,v in p.items() if v}
def add(*pp):
 out={}
 for p in pp:
  for a,v in p.items():out[a]=out.get(a,0)+v
 return clean(out)
def scale(p,c):return clean({a:c*v for a,v in p.items()})
def mul(p,r):
 out={}
 for (i,j),v in p.items():
  for (h,l),w in r.items():
   a=i+h,j+l;out[a]=out.get(a,0)+v*w
 return clean(out)
def encode(p):return [[list(a),str(v)] for a,v in sorted(p.items())]
def decode(rows):
 out={}
 for a,v in rows:
  require(isinstance(a,list) and len(a)==2 and all(type(e)is int and e>=0 for e in a),'Exact complete monomial domain')
  require(isinstance(v,str) and str(int(v))==v and int(v)!=0,'Canonical nonzero integer coefficient')
  require(tuple(a) not in out,'No duplicate entire coefficient')
  out[tuple(a)]=int(v)
 require(rows==encode(out),'Canonical complete coefficient order')
 return out

def derivative(p):return {(i-1,j):i*v for (i,j),v in p.items() if i}
def at(p,q,k):return sum(v*q**i*k**j for (i,j),v in p.items())
def sign7(a,b):
 if a==b==0:return 0
 if a>=0 and b>=0:return 1
 if a<=0 and b<=0:return -1
 diff=a*a-7*b*b;require(diff!=0,'Irrational sqrt7 with rational coefficients')
 return (1 if diff>0 else -1) if a>0 else (1 if diff<0 else -1)
def powers_by(p,axis):
 degree=max((a[axis] for a in p),default=0);groups=[{} for _ in range(degree+1)]
 for a,v in p.items():
  b=list(a);b[axis]=0;groups[a[axis]][tuple(b)]=v
 return degree,groups

def shift(p,axis):
 degree,groups=powers_by(p,axis)
 linear={(0,0):K0,((1,0) if axis==0 else (0,1)):1}
 out=groups[degree]
 for j in range(degree-1,-1,-1):out=add(mul(out,linear),groups[j])
 return out

def line(p,numer,den):
 # Entire homogeneous Horner, not the producer's binomial expansion.
 degree,groups=powers_by(p,0)
 L={(0,1):numer,(1,0):den}
 out=groups[degree]
 for j in range(degree-1,-1,-1):out=add(mul(out,L),scale(groups[j],den**(degree-j)))
 return out,degree

def compact(p):
 degree,groups=powers_by(p,0);L={(0,1):6,(1,1):11};M={(0,0):2,(1,0):2}
 out=groups[degree];mp=ONE
 for j in range(degree-1,-1,-1):
  mp=mul(mp,M);out=add(mul(out,L),mul(groups[j],mp))
 return out,degree

def curve(p,norm):
 degree=max(i for i,j in p);groups=[{} for _ in range(degree+1)]
 for (i,j),v in p.items():groups[i][j,0]=v
 L={(1,0):3,(0,0):-14,(0,1):1};out=groups[degree]
 for j in range(degree-1,-1,-1):out=add(mul(out,L),groups[j])
 # Reduce only AFTER the entire ordinary composition has been expanded.
 A,H={},{}
 for (i,j),v in out.items():
  target=H if j%2 else A;power=j//2
  for h in range(power+1):
   a=i+2*h,0;target[a]=target.get(a,0)+v*comb(power,h)*7**h*norm**(power-h)
 return clean(A),clean(H)

def expected():
 raw=zero_generator.generated();N0,D0=(decode(raw['joint_residual_'+side]) for side in ('numerator','denominator'))
 content=0
 for v in list(N0.values())+list(D0.values()):content=gcd(content,v)
 require(content==65536,'Entire defining integer content reproduced')
 N,D=({a:v//content for a,v in p.items()} for p in (N0,D0))
 require(scale(N,content)==N0 and scale(D,content)==D0,'Entire raw original numerator/denominator reconstructed')
 P=add(mul(derivative(N),D),scale(mul(N,derivative(D)),-1))
 slope,degree=line(P,11,2);slope=shift(slope,1)
 den=shift(line(D,3,1)[0],1)
 zone,zone_degree=compact(N);zone=shift(zone,1)
 endpoint={(0,j):v for (i,j),v in zone.items() if i==zone_degree}
 curves={}
 for norm in (32,36):
  A,H=curve(N,norm)
  curves[str(norm)]={'A':A,'H':H,'Hshift':shift(H,0),'a':shift(A,0),'b':shift(mul({(1,0):1},H),0)}
 return {'N':N,'D':D,'P':P,'slope':slope,'den':den,'slope_degree':degree,
 'zone':zone,'zone_degree':zone_degree,'endpoint':endpoint,'curves':curves}

def sign_record(record,p,goal):
 require(record['goal_sign']==goal,'Original sign obligation')
 require(decode(record['entire_coefficients'])==p,'ENTIRE independent polynomial identity')
 require(all(goal*v>=0 for v in p.values()) and goal*p.get((0,0),0)>0,'All coefficient signs and strict constant')
 require(record['completed_certificate'] and record['wrong_sign_count']==0 and record['strict_constant'],'Complete author sign receipt agrees with exact checks')

def check_records(records,E):
 for phase,p in records.items():
  require(p['phase']==phase and p['k0']==K0 and p['completed'],'Complete phase and declared effective domain')
  require(p['actual_agent']=='six-downset-3' and p['role']=='researcher','Actual author/role')
  require(p['source_commit']=='4b649cf0dccac41217b9b50317f389a7fc83d518','Pinned defining source')
 m=records['monotonicity']
 require(decode(m['entire_derivative_numerator'])==E['P'] and m['clearing_power_of2']==E['slope_degree'],'ENTIRE original derivative and positive clearing')
 sign_record(m['derivative_whole_sign'],E['slope'],1)
 sign_record(m['denominator_entire_domain_sign'],E['den'],1)
 n=records['negative-zone'];require(n['clearing_power_of_2_times1plust']==E['zone_degree'],'Compact positive clearing power')
 sign_record(n['whole_negative_sign'],E['zone'],-1)
 sign_record(n['closed_endpoint_negative_sign'],E['endpoint'],-1)
 curves=records['curves']['curves'];require(set(curves)=={'32','36'},'Both entire norm curves required')
 for norm,goal in ((32,-1),(36,1)):
  c=curves[str(norm)];e=E['curves'][str(norm)]
  require(c['norm']==norm and c['goal_sign']==goal and c['completed'],'Original complete curve obligation')
  require(decode(c['entire_A'])==e['A'] and decode(c['entire_H'])==e['H'],'Whole ordinary composition/end-reduction equals producer quotient-ring solve')
  sign_record(c['whole_H_sign'],e['Hshift'],goal)
  pairs=c['whole_radical_sign']
  require(decode(pairs['entire_rational_coefficients'])==e['a'] and decode(pairs['entire_sqrt7_coefficients'])==e['b'],'Every shifted radical coefficient bound')
  keys=set(e['a'])|set(e['b'])
  require(all(goal*sign7(e['a'].get(a,0),e['b'].get(a,0))>=0 for a in keys) and goal*sign7(e['a'].get((0,0),0),e['b'].get((0,0),0))>0,'Whole positive-embedding signs and strict constant')
  require(pairs['goal_sign']==goal and pairs['completed_certificate'] and pairs['wrong_sign_count']==0 and pairs['strict_constant'],'Entire radical sign receipt')
  require(pairs['coefficient_pairs']==len(keys),'Full radical pair census')
  for row in c['controls']:
   k,m,q=row['k'],row['m'],row['q'];require(m*m-7*k*k==norm and q==3*k-14+m,'Exact declared norm controls')
   actual=at(E['N'],q,k)
   require(actual==at(e['A'],k,0)+m*at(e['H'],k,0)==int(row['whole_original_numerator']),'Whole curve and actual original numerator control')
   if k>=K0:require(goal*actual>0,'Declared effective control sign')
 require(at(E['N'],32,8)<0,'Known k8 norm36 exception remains absent')
 # A squared rational comparison puts both radical curves above11k/2.
 require(7*64**2>167**2 and K0==128,'sqrt7>5/2+14/128, entire increasing-count bridge')
 residues7={m*m%7 for m in range(7)};residues4={(m*m-7*k*k)%4 for m in range(4) for k in range(4)}
 require(33%7 not in residues7 and 34%7 not in residues7 and 35%4 not in residues4,'All intervening integer norms impossible')
 return True

def damaged(records,name):
 x=copy.deepcopy(records)
 if name=='wrong-domain':x['monotonicity']['k0']=127
 elif name=='derivative-coefficient':x['monotonicity']['derivative_whole_sign']['entire_coefficients'][31][1]=str(int(x['monotonicity']['derivative_whole_sign']['entire_coefficients'][31][1])+1)
 elif name=='denominator-prefix':x['monotonicity']['denominator_entire_domain_sign']['entire_coefficients'].pop()
 elif name=='negative-zone-endpoint':x['negative-zone'].pop('closed_endpoint_negative_sign')
 elif name=='norm32-H-coefficient':x['curves']['curves']['32']['entire_H'][25][1]=str(int(x['curves']['curves']['32']['entire_H'][25][1])+1)
 elif name=='norm36-wrong-H-sign':x['curves']['curves']['36']['whole_H_sign']['goal_sign']=-1
 elif name=='radical-sqrt7-coefficient':x['curves']['curves']['36']['whole_radical_sign']['entire_sqrt7_coefficients'][20][1]=str(int(x['curves']['curves']['36']['whole_radical_sign']['entire_sqrt7_coefficients'][20][1])+1)
 elif name=='missing-norm36-curve':x['curves']['curves'].pop('36')
 else:raise ValueError('Unknown damage obligation')
 return x

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--curves',type=Path,required=True);ap.add_argument('--monotonicity',type=Path,required=True);ap.add_argument('--negative-zone',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 records={phase:json.loads(p.read_text()) for phase,p in [('curves',args.curves),('monotonicity',args.monotonicity),('negative-zone',args.negative_zone)]}
 E=expected();check_records(records,E)
 rejects=[]
 for name in ('wrong-domain','derivative-coefficient','denominator-prefix','negative-zone-endpoint','norm32-H-coefficient','norm36-wrong-H-sign','radical-sqrt7-coefficient','missing-norm36-curve'):
  try:check_records(damaged(records,name),E)
  except (ValueError,KeyError):rejects.append(name)
  else:raise ValueError('Altered complete certificate accepted: '+name)
 require('probe' not in sys.modules and not any(n=='sympy' or n.startswith('sympy.') for n in sys.modules),'Separate stdlib checking, no producer/CAS import')
 out={'actual_agent':'six-downset-3','role':'researcher','k0':K0,'completed':True,
 'every_whole_producer_polynomial_matched_independent_Horner_and_end_reduction':True,
 'derivative_sign_coefficients':len(E['slope']),'denominator_sign_coefficients':len(E['den']),
 'negative_zone_sign_coefficients':len(E['zone']),'strict_closed_endpoint_coefficients':len(E['endpoint']),
 'curve_signs':{norm:{'H_coefficients':len(e['Hshift']),'radical_coefficient_pairs':len(set(e['a'])|set(e['b']))} for norm,e in E['curves'].items()},
 'all_eight_semantic_damages_rejected':rejects,'no_CAS_or_new_producer_import':True,
 'all_real_count_extension_and_original_face_bridge_unformalized':True,'independent_person_review':False,
 'proved_original_domain':'ALL integer k>=128,q>=3k,every exception subsetZ',
 'greatest_rank_cutoff':'3k-14+ceil(sqrt(7k^2+36))','whole_face_absent_below_cutoff':True,
 'known_k8_norm36_exception_preserved':True,'optimal_onset_not_claimed':True}
 args.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
