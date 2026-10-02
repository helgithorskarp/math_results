"""Independent complete polar and sum-eight radial certificates; stdlib only."""
from fractions import Fraction as F
from math import comb
import hashlib,json,sys
from pathlib import Path
from polys import cast,symbol,need
from radial import WINDOW,radial,majorant,coefficients

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def scalar(p):
 need(not p.terms or set(p.terms)=={()},'constant result')
 return p.terms.get((),(F(0),F(0)))
def integral(p,var='t'):return p.integral(var).substitute({var:1})-p.integral(var).substitute({var:0})
def norm2(p):return scalar(p*p.conjugate_coefficients())[0]
def product(xs):
 out=cast(1)
 for x in xs:out*=x
 return out
def communication(q,a):
 t=symbol('t');b=1-a*a
 return integral(product(a+b*t*x for x in q)),9*integral(product(1-a*t*x for x in q))

def polar():
 eta,t=symbol('eta'),symbol('t');a=1-eta;b=1-a*a;L=8+3*eta;mu=L/8;d=a**7*b/2
 T=sum((F(comb(8,k),k+1)*a**(8-k)*b**k*mu**k for k in range(2,9)),cast(0));B=a**8+d*L+T
 balanced=integral(product(a+b*t*mu for _ in range(8)))
 need(B==balanced,'all balanced coefficients from eight multiplied factors')
 need(9*b*mu*B==(a+b*mu)**9-a**9,'independent division-free antiderivative')
 ps={
  'mean':1-a**16-d*d*L*L-2*(a**8+d*L)*T-T*T-(8-6*eta)*a**15*b,
  'modulus':1+9*eta*eta-B,
  'variance_old':13*a**6*b*b-6*(B-1),
  'variance_improved':F(63,5)*a**6*b*b-6*(B-1)}
 out={}
 for name,p in ps.items():
  cert=majorant(p);need(cert['valuation']==2 and cert['strict_positive'],'whole polar '+name)
  floor={'mean':F(1),'modulus':F(1,2),'variance_old':F(1),'variance_improved':F(1,3)}[name]
  need(F(cert['lower_after_factoring'])>floor,'strict polar margin '+name)
  out[name]={'whole':p.record(),'certificate':cert,'claimed_factored_floor':str(floor)}
 need([out[x]['certificate']['degree'] for x in ps]==[48,24,24,24],'complete degrees')
 need([out[x]['certificate']['leading'] for x in ps]==['4/3','2/3','2','2/5'],'leading terms')
 return out,{'B':B.record(),'T':T.record(),'balanced':balanced.record()}

def scalar_margins():
 eta,t=symbol('eta'),symbol('t');a=1-eta;e=WINDOW
 K1=scalar(9*integral(t*(1+F(8,7)*t)**7))[0]
 K2=scalar(9*integral(t*t*(1+F(4,3)*t)**6))[0]
 K9=scalar(9*integral(t*(1+F(9,7)*t)**7))[0]
 grad=F(9,7)**7
 need(K1==F(570801247,1647086) and K2==F(1199851,5103),'whole phase integrals')
 ndefect=F(256*60000)*F(5,39)
 nvariance=F(56,11)*ndefect
 ovariance=F(65,64)*nvariance
 energy=8*(ovariance+18)+52*e
 annulus=F(1,512*82000000)
 margins={
 'phase_first':350-K1,'phase_second':2*K1-K2,'origin_gradient':600-K9,
 'product_gradient':6-grad,'origin_total':60000-(350*160+(600+6)*6),
 'left_critical':1-165*e,'radial_original':2-10*e-81*e*e,
 'phase_normalized':10-9*(1+3*e/2),'variance_rescale':F(65,64)-F(256,255)**2,
 'lambda_above_a':8-3*(2-e),'a_positive':1-e,
 'E2_above_11_over_4':28*(1-e)**2-F(126,5)-F(11,4),
 'energy_improved':82000000-energy,'annulus_in_window':e-annulus,
 'original_energy':2**28-energy,'fixed_slope':F(8,3)-F(13,5)-F(4,3)*annulus,
 'largeF_refined_slope':3-(F(8,3)+F(9,57820)),
 'appendix_slope':F(17,6)-F(14,5)-F(1,16384),
 'appendix_small_sqrt':F(1,2**36)-F(1,2**37)}
 # The exact zero entry margins rely on strict H.
 need(82000000*annulus==F(1,512),'exact improved energy entry, strict H supplies strictness')
 need(2**28*F(1,2**37)==F(1,512),'exact old energy entry')
 for k,v in margins.items():need(v>0,'scalar margin '+k)
 return {'K1':str(K1),'K2':str(K2),'K9':str(K9),'product_gradient':str(grad),
  'strict_margins':{k:str(v) for k,v in sorted(margins.items())},
  'defect_budget':str(ndefect),'normalized_variance_budget':str(nvariance),
  'original_variance_budget':str(ovariance),'energy_unrounded_budget':str(energy),
  'energy_clean_budget':'82000000','annulus':str(annulus)}

def normalization_identities():
 # Division-free versions cover every F in its stated case, including V=0.
 a,f,r,mu=symbol('a'),symbol('f'),symbol('r'),symbol('mu');den=(1+a)*f-8
 need(8*den+(8*a)*((1+a)*f-8)==8*(1+a)*den,'sum radii after subtract-floor contraction')
 need(den+(8*a)*((1+a)*r-1)-den*(1+a)==8*a*(1+a)*(r-f/8),'centered contraction numerator')
 # Pairwise variance and signed deficit identities, with no division by variance.
 x,y,m=symbol('x'),symbol('y'),symbol('m')
 need((x-m)**2+(y-m)**2==(x*x+y*y)-2*m*(x+y)+2*m*m,'variance centering')
 z=symbol('z');need((x-1)**2+(y*y)==(x*x+y*y)-2*x+1,'reciprocal squared distance')
 return {'sum_contraction_numerator':'zero','centered_contraction_numerator':'zero',
  'variance_centering':'zero','reciprocal_distance':'zero','zero_variance_division':False}

def controls():
 eta=F(1,2**38);a=1-eta
 real=[F(3,4)]*4+[F(5,4)]*4
 complexq=[(F(35,37),F(12,37))]*8
 out=[]
 for label,qs,drop in [('drop_origin',real,'origin'),('drop_polar',complexq,'polar')]:
  q=list(map(cast,qs));C,O=communication(q,a);P=product(cast(1) for _ in q)
  if label=='drop_origin':P=product(q)
  rs=real if label=='drop_origin' else [F(1)]*8
  H=sum(norm2(cast(a)-cast((scalar(x)[0]/norm2(x),-scalar(x)[1]/norm2(x)))) for x in q)
  cn,on,pn=norm2(C),norm2(O),norm2(P)
  need(sum(rs)==8 and min(rs)>1/(1+a),'control sum and floor')
  need(H>2**28*eta and H>82000000*eta,'control violates discarded-channel carrier')
  need((cn>1 and on>pn) if drop=='origin' else (cn<1 and on<pn),'single discarded communication channel')
  out.append({'label':label,'abstract_only':True,'eta':str(eta),'q':[x.record() for x in q],
   'C':C.record(),'O':O.record(),'polar_norm_squared':str(cn),'origin_norm_squared':str(on),
   'product_norm_squared':str(pn),'H':str(H),'dropped_channel':drop})
 # Whole actual disk-rooted multiple-root family, independent of reciprocal division.
 t,aa,bb=symbol('t'),symbol('a'),symbol('b');p=(t-aa)*(t+bb)**8
 need(p.derivative('t')==9*(t+bb)**7*(t-(8*aa-bb)/9),'actual eightfold original multiplicity')
 # Exact actual instance b=1: both communication identities checked, low-F excluded.
 roots=[cast(-1)]*8;crit=[cast(-1)]*7+[cast((8*a-1)/9)]
 qs=[cast(1/scalar(cast(a)-z)[0]) for z in crit];C,O=communication(qs,a)
 ratio=product(cast((1-a*scalar(z)[0])/(a-scalar(z)[0])) for z in roots)
 need(C==ratio,'actual polar identity')
 need(O==product(qs)*product(roots),'actual origin identity')
 need(sum(scalar(x)[0] for x in qs)==16/(1+a)>8+3*eta,'actual example excluded from low-F')
 out.append({'label':'actual_eightfold_minus_one','disk_feasible':True,'low_F':False,
  'whole_derivative':p.derivative('t').record(),'C':C.record(),'O':O.record(),
  'F':str(16/(1+a)),'eta':str(eta),'critical_multiplicities':[7,1]})
 return out

def build():
 p,b=polar()
 return {'schema':1,'actual_agent':'six-reviewer-3','method':'full coefficient absolute tails and eight near-boundary sum-eight radial faces',
  'window':str(WINDOW),'polar':p,'balanced':b,'radial':radial(),
  'scalars':scalar_margins(),'normalization':normalization_identities(),'controls':controls()}

def broken_budgets():
 eta=symbol('eta');a=1-eta;b=1-a*a;L=8+3*eta;d=a**7*b/2
 T=sum((F(comb(8,k),k+1)*a**(8-k)*b**k*(L/8)**k for k in range(2,9)),cast(0));B=a**8+d*L+T
 bad=[('mean_5',1-a**16-d*d*L*L-2*(a**8+d*L)*T-T*T-(8-5*eta)*a**15*b),
  ('modulus_8',1+8*eta*eta-B),('variance_12',12*a**6*b*b-6*(B-1))]
 out={}
 for k,p in bad:
  cert=majorant(p);need(not cert['strict_positive'],'broken budget rejected '+k);out[k]='rejected negative leading coefficient'
 row=radial()[1];gap=F(row['interval_certificate']['coefficients'][0]);D=32
 need(gap-(8-F(39,5))*D<0,'radial penalty8 rejected on m2 at boundary')
 out['radial_penalty_8']='rejected exact boundary face';out['phase_constant300']='rejected' if F(570801247,1647086)>300 else 'wrong'
 need(F(11648000000,143)>80000000,'energy clean80m cannot follow this budget');out['energy80m']='rejected insufficient rounding'
 return out

def main():
 here=Path(__file__).resolve().parent;record=build();data=canonical(record);digest=hashlib.sha256(data).hexdigest()
 if '--generate' in sys.argv:
  (here/'EXPECTED.json').write_bytes(data+b'\n')
 else:
  expected=json.loads((here/'EXPECTED.json').read_text());need(expected==record,'complete external record differs')
 print(json.dumps({'schema':1,'sha256':digest,'bytes':len(data),'polar_certificates':4,'radial_faces':8,
  'controls':len(record['controls']),'broken_budgets':broken_budgets(),
  'energy_budget':record['scalars']['energy_clean_budget'],'annulus':record['scalars']['annulus']},sort_keys=True))
if __name__=='__main__':main()
