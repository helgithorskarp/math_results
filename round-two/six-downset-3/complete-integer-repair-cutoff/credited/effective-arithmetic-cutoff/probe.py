"""Whole-domain exact certificate probes for an effective arithmetic cutoff.

Complete exact coefficient certificates; failed checks imply neither
mathematical absence nor absence of a possible proof.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from math import comb,gcd
import argparse,hashlib,json,sys,time
BASE=Path(__file__).resolve().parent/'credited/uniform-repair-face'
sys.path.insert(0,str(BASE))
import source_gate
source_gate.verify()
import zero_generator,zero_check,zero_signs
z=zero_check.integer_tools()
def require(c,m):
 if not c:raise ValueError(m)
def decode(rows):return {tuple(a):int(b) for a,b in rows if int(b)}
def encode(p):return [[list(a),str(b)] for a,b in sorted(p.items())]
def stats(p):return {'terms':len(p),'degrees':[max((a[0] for a in p),default=0),max((a[1] for a in p),default=0)],'total_degree':max((sum(a) for a in p),default=0),'SHA256':z.digest(p)}
def derivative(p):return {(i-1,j):i*v for (i,j),v in p.items() if i}
def fields():
 raw=zero_generator.generated();N,D=(decode(raw['joint_residual_'+a]) for a in ('numerator','denominator'))
 scalar=0
 for value in list(N.values())+list(D.values()):scalar=gcd(scalar,value)
 require(scalar>0,'Positive common integer content')
 n={a:v//scalar for a,v in N.items()};d={a:v//scalar for a,v in D.items()}
 g={(0,0):scalar}
 require(z.mul(g,n)==N and z.mul(g,d)==D,'Every integer content division independently multiplied back')
 return n,d,{'raw_numerator':stats(N),'raw_denominator':stats(D),'scalar_gcd':str(scalar),'integer_content_divisions_multiplied_back':True}

def sign_record(p,goal):
 wrong=[a for a,v in sorted(p.items()) if goal*v<0]
 return {'entire_coefficients':encode(p),'wrong_sign_count':len(wrong),'wrong_sign_head':[list(a) for a in wrong[:12]],
 'strict_constant':goal*p.get((0,0),0)>0,'completed_certificate':not wrong and goal*p.get((0,0),0)>0,
 'goal_sign':goal,'stats':stats(p),'failed_proposal_is_not_mathematical_absence':bool(wrong)}
def shift_line(poly,numer=11,den=2):
 # den^degree * poly((numer*k+den*u)/den,k), variables(u,k).
 degree=max(i for i,j in poly);out={}
 for (i,j),v in poly.items():
  for h in range(i+1):
   a=h,i-h+j
   out[a]=out.get(a,0)+v*comb(i,h)*numer**(i-h)*den**(degree-i+h)
 return z.clean(out),degree

def negative_compact(poly):
 # [2(1+t)]^degree * poly(k*(6+11t)/(2(1+t)),k).
 # t>=0 parametrizes q/k in[3,11/2), with endpoint supplied by continuity.
 degree=max(i for i,j in poly);out={};recipes=[]
 for i in range(degree+1):
  row=[0]*(degree+1)
  for a in range(i+1):
   one=comb(i,a)*6**(i-a)*11**a*2**(degree-i)
   for b in range(degree-i+1):row[a+b]+=one*comb(degree-i,b)
  recipes.append(row)
 for (i,j),v in poly.items():
  for tdeg,w in enumerate(recipes[i]):
   if w:
    a=tdeg,i+j;out[a]=out.get(a,0)+v*w
 return z.clean(out),degree

def reduced_curve(N,norm):
 # Z[k,m]/(m^2-7k^2-norm), substitution q=3k-14+m.
 degree=max(i for i,j in N);by_q=[{} for _ in range(degree+1)]
 for (i,j),v in N.items():by_q[i][j,0]=v
 L={(1,0):3,(0,0):-14};B={(2,0):7,(0,0):norm}
 A,H=by_q[degree],{}
 for i in range(degree-1,-1,-1):A,H=z.add(z.mul(L,A),z.mul(B,H),by_q[i]),z.add(A,z.mul(L,H))
 return A,H

def pair_sign_record(a,b,goal):
 powers=set(a)|set(b);wrong=[power for power in sorted(powers) if goal*z.surd_sign(a.get(power,0),b.get(power,0))<0]
 strict=goal*z.surd_sign(a.get((0,0),0),b.get((0,0),0))>0
 return {'entire_rational_coefficients':encode(a),'entire_sqrt7_coefficients':encode(b),
 'wrong_sign_count':len(wrong),'wrong_sign_head':[list(p) for p in wrong[:12]],'strict_constant':strict,
 'completed_certificate':not wrong and strict,'goal_sign':goal,
 'coefficient_pairs':len(powers),'failed_proposal_is_not_mathematical_absence':bool(wrong)}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('phase',choices=('monotonicity','negative-zone','curves'));ap.add_argument('--k0',type=int,default=128);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 require(args.k0>=7,'Original k-domain maintained')
 start=time.monotonic();N,D,binding=fields();k0=args.k0
 result={'actual_agent':'six-downset-3','role':'researcher',
 'phase':args.phase,'k0':k0,'source_commit':'4b649cf0dccac41217b9b50317f389a7fc83d518',
 'source_graph_ref':'bafkreibz56ugbuasnwnmte34ryziqeurksmlidejla3hubzurgabvje37a',
 'source_field_binding':binding,'no_CAS_imported':True,'independent_review':False,'ordinary_bridges_unformalized':True}
 if args.phase=='monotonicity':
  P=z.add(z.mul(derivative(N),D),z.scale(z.mul(N,derivative(D)),-1))
  line,degree=shift_line(P)
  shifted=z.shift_k(line,k0)
  positive=sign_record(shifted,1)
  den0=z.shift_k(shift_line(D,3,1)[0],k0)
  den_sign=sign_record(den0,1)
  result.update(entire_derivative_numerator=encode(P),clearing_power_of2=degree,
   exact_domain='ALL REAL k>=k0,q>=11k/2, R=N/D with D>0',
   derivative_whole_sign=positive,denominator_entire_domain_sign=den_sign,
   completed=positive['completed_certificate'] and den_sign['completed_certificate'])
 elif args.phase=='negative-zone':
  poly,degree=negative_compact(N);shifted=z.shift_k(poly,k0)
  record=sign_record(shifted,-1)
  endpoint=sign_record({(0,j):v for (i,j),v in shifted.items() if i==degree},-1)
  result.update(exact_domain='ALL REAL k>=k0, 3k<=q<=11k/2; compact fractional parametrization with entire leading-t endpoint',
   clearing_power_of_2_times1plust=degree,whole_negative_sign=record,closed_endpoint_negative_sign=endpoint,completed=record['completed_certificate'] and endpoint['completed_certificate'])
 else:
  curves={}
  for norm,goal in ((32,-1),(36,1)):
   A,H=reduced_curve(N,norm);hs=z.shift_k(H,k0)
   hs=hs if all(j==0 for i,j in hs) else None
   require(hs is not None,'Entire univariate quotient-ring curve coefficients')
   # In these univariate polynomials the first coordinate is k, so shift_k
   # would shift an absent second coordinate. Use the ordinary univariate shift.
   import lower
   hshift=lower.shifted(H,k0);Hsign=sign_record(hshift,goal)
   if norm==32:
    aa,bb=A,z.mul({(1,0):1},H)
    bound='m>sqrt7*k, H<0: A+mH < A+sqrt7*kH'
   else:
    aa,bb=A,z.mul({(1,0):1},H)
    bound='m>sqrt7*k, H>0: A+mH > A+sqrt7*kH'
   aa,bb=lower.shifted(aa,k0),lower.shifted(bb,k0)
   signs=pair_sign_record(aa,bb,goal)
   controls=[]
   # New curve controls bind quotient-ring evaluation; no infinite sign
   # is inferred from these controls.
   seeds=((12,4),(180,68)) if norm==32 else ((22,8),(344,130))
   for m,k in seeds:
    require(m*m-7*k*k==norm,'Exact seed norm')
    q=3*k-14+m;v=z.evaluate(N,q,k)
    require(v==z.evaluate(A,k,0)+m*z.evaluate(H,k,0),'ENTIRE original numerator equals quotient-ring evaluation')
    controls.append({'m':m,'k':k,'q':q,'norm':norm,'whole_original_numerator':str(v),'in_effective_domain':k>=k0})
   curves[str(norm)]={'norm':norm,'goal_sign':goal,'entire_A':encode(A),'entire_H':encode(H),
    'whole_H_sign':Hsign,'exact_radical_bound':bound,'whole_radical_sign':signs,
    'completed':Hsign['completed_certificate'] and signs['completed_certificate'],'controls':controls}
  result.update(exact_domain='ALL REAL k>=k0 on both q=3k-14+sqrt(7k^2+norm) curves',
   curves=curves,completed=all(c['completed'] for c in curves.values()))
 if any(name=='sympy' or name.startswith('sympy.') for name in sys.modules):raise ValueError('CAS imported in whole coefficient probe')
 elapsed=time.monotonic()-start;args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 summary={k:result[k] for k in ('actual_agent','role','phase','k0','completed')}
 summary['seconds']=elapsed
 if args.phase=='monotonicity':summary.update(derivative_wrong=positive['wrong_sign_count'],denominator_wrong=den_sign['wrong_sign_count'],derivative_terms=positive['stats']['terms'])
 elif args.phase=='negative-zone':summary.update(wrong=record['wrong_sign_count'],terms=record['stats']['terms'])
 else:summary['curves']={norm:{'H_wrong':c['whole_H_sign']['wrong_sign_count'],'radical_wrong':c['whole_radical_sign']['wrong_sign_count'],'completed':c['completed']} for norm,c in curves.items()}
 print(json.dumps(summary))

if __name__=='__main__':main()
