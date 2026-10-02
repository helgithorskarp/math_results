"""Independent exact audit of LEMMA9620; manuscript visible, native code unseen.

Fraction/Gaussian sparse kernel copied unchanged from this reviewer's9588 audit.
New calculations use real coordinates, a sqrt(3) quotient, and literal derivatives.
"""
from fractions import Fraction as F
from math import comb
import hashlib,json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from polys import Poly,symbol,cast,need

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def real(p):return (p+p.conjugate_coefficients())/2
def norm2(p):return p*p.conjugate_coefficients()
def qr(p):return p.reduce_square('s',3)
def pairadd(a,b):return(a[0]+b[0],a[1]+b[1])
def pairmul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def cmul(a,b):
 out=[(F(0),F(0))]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]=pairadd(out[i+j],pairmul(x,y))
 return out
def evaluate(p,z):
 out=(F(0),F(0))
 for x in reversed(p):out=pairadd(pairmul(out,z),x)
 return out
def polynomial_from_criticals(crit,a):
 derivative=[(F(9),F(0))]
 for z in crit:derivative=cmul(derivative,[(-z[0],-z[1]),(F(1),F(0))])
 p=[(F(0),F(0))]+[(x[0]/(i+1),x[1]/(i+1)) for i,x in enumerate(derivative)]
 at=evaluate(p,(a,F(0)));p[0]=(-at[0],-at[1])
 return p,derivative

def build():
 identities={};margins={};quantities={}
 def identity(name,p,q):
  p,q=qr(cast(p)),qr(cast(q));need(p==q,'identity:'+name)
  identities[name]={'coefficients':p.record(),'sha256':hashlib.sha256(canonical(p.record())).hexdigest()}
 def margin(name,v):
  v=F(v);need(v>0,'margin:'+name);margins[name]=str(v)
 a,M,D,Q,J,V,eta,s,x,y=(symbol(n) for n in ['a','M','D','Q','J','V','eta','s','x','y'])
 mean=M+cast((0,1))*D;u=a-mean;w=-F(1,2)+cast((0,F(1,2)))*s
 identity('cube_relation',w*w+w+1,0)
 identity('cube_power9',w**9,1)
 for j in range(1,8):
  identity('cube_average_'+str(j),real(qr(w**j))-1,0 if j%3==0 else -F(3,2))
 base=(norm2(mean+u*w)-1)/2
 lead=real((Q+cast((0,1))*J)*(w-1))/14
 P=(a*a-1)/2-F(3,2)*a*M+F(3,2)*(M*M+D*D)-F(3,28)*Q
 identity('individual_actual_normal',base+lead,P+s*(a*D-J/14)/2)
 identity('pair_actual_normal',real(qr((base+lead)+(base+lead).substitute({'s':-s})))/2,P)
 identity('radial_pair',4*P,3*norm2(u)-a*a-2+3*norm2(mean)-F(3,7)*Q)
 identity('marked_radius',norm2(u),a*a-2*a*M+M*M+D*D)
 identity('quadratic_reciprocal',F(3,2)*x*x-F(1,2)*(x*x+y*y),(x*x+y*y+3*(x*x-y*y))/4)
 identity('trace_ellipse', (12*eta-5*Q)**2-49*Q*Q,294*eta*eta-24*(Q+F(5,2)*eta)**2)
 identity('slack_discard',-F(3,64)*V-F(15,448)*Q,-F(3,224)*V-F(15,448)*(Q+V))
 identity('eta_anchor', (a*a-1).substitute({'a':1-eta}),-2*eta+eta*eta)
 r3,tail0,E0,K=(symbol(n) for n in ['r3','tail','E','K'])
 # Complete convexity/pair substitution before bounding the signed trace.
 reciprocal=F(8,3)*eta-F(4,3)*eta*eta+4*K-F(4,7)*Q-F(16,3)*E0+(V+3*Q)*r3/4-tail0
 regroup=F(8,3)*eta-F(4,3)*eta*eta+4*K+V*r3/4+(F(3,4)*r3-F(4,7))*Q-F(16,3)*E0-tail0
 identity('convexity_trace_regroup',reciprocal,regroup)
 identity('variance_replace_Q_minus_V',regroup.substitute({'Q':-V}),F(8,3)*eta-F(4,3)*eta*eta+4*K+(F(4,7)-r3/2)*V-F(16,3)*E0-tail0)
 aeta=1-eta
 slack_base=eta-eta*eta/2+F(3,16)*(8*aeta**3+3*eta*aeta**3-8*aeta*aeta)
 identity('individual_slack_base',slack_base,eta/16+F(13,16)*eta*eta+F(3,16)*eta**3-F(9,16)*eta**4)
 identity('mean_sign_base',aeta*aeta*(8+3*eta)/8-aeta,-F(5,8)*aeta*aeta*eta-aeta*eta*eta)
 # Pair normal d_j: cancel omega^9 before averaging, retaining all coefficients.
 for j in range(1,8):
  identity('bar_u_cube_linear_'+str(j),qr(w.conjugate_coefficients()*(w**j-1)*w),qr(w**j-1))
 # Full shifted-coefficient map gives c8 and c7, with d7=-9T/14.
 z=symbol('z');t=symbol('t');shift=z-mean
 centered=shift**9-F(9,14)*t*shift**7
 identity('original_c8',centered.coefficient('z',8),-9*mean)
 identity('original_c7',centered.coefficient('z',7),F(9,14)*(56*mean*mean-t))
 e=F(1,65536);rho=F(1,64);h=F(1,512);amin=1-e
 lo=amin-rho;hi=1+rho;L=F(1,2);outer=hi+L*h
 A={j:F(9,8*j)*comb(8,9-j)*rho**(7-j) for j in range(1,7)};A[7]=F(9,14)
 Cd=sum(j*A[j]*outer**(j-1) for j in A)
 margin('rouche_all_nine',9*lo**8*L-36*outer**7*L*L*h-sum(A[j]*(outer**j+hi**j) for j in A))
 margin('disjoint_circles',F(4,9)*lo-2*L*h)
 margin('centered_radius',F(17,384)**2-h)
 denom=9*lo**8-36*outer**7*L*h-Cd*h
 Nc=F(7,4)*sum(A[j]*hi**j for j in [1,2,4,5,7])
 margin('cube_displacement_denominator',denom)
 margin('cube_displacement_one_sixth',denom/6-Nc)
 margin('cube_linear_one_sixth',9*lo**8/6-Nc)
 B=outer**7/(9*lo**8)+Cd/(54*lo**8)
 Bs={5:F(63,32),4:F(63,32)*rho,2:F(9,128)*rho*h,1:F(9,4096)*h*h}
 C=(1+2*rho)*B+F(1,72)
 margin('full_pair_normal_error',1-C-F(1,6)*sum(Bs[j]*lo**(j-7) for j in Bs))
 margin('full_individual_normal_error',1-C-F(1,5)*sum(Bs[j]*lo**(j-7) for j in Bs))
 r0=F(6399,6400)
 tail=lambda tau,r:tau/((r-tau)*r**3)
 margin('positive_Q_multiplier',F(3,4)/hi**3-F(4,7))
 margin('initial_reciprocal_loss',F(3,5)-F(1,2)/lo**3-tail(F(17,384),lo))
 margin('r0_from_objective',1-(3*e+F(3,5)*h)/8-r0)
 stages=[('initial',rho,h,F(17,384),700),('second',F(1,800),h,F(17,384),26),('third',F(1,800),26*e,F(1,50),8),('fourth',F(1,800),8*e,F(1,90),6)]
 gamma={}
 for name,b,c,tau,k in stages:
  g=F(4,7)-F(1,2)/r0**3-tail(tau,r0)-F(16,3)*(b/6+c)
  margin(name+'_positive_variance',g)
  margin(name+'_variance_contraction',k*g-F(1,3)-4*e/3)
  gamma[name]=str(g)
 margin('mean_square_eleven',F(1,11)-F(1,12)-e/3)
 margin('mean_800',F(1,800)**2-e/11)
 for k,tau in [(26,F(1,50)),(8,F(1,90)),(6,F(1,96))]:margin('centered_radius_'+str(k),tau*tau-k*e)
 margin('mean_strict_negative',amin*amin/10-F(1,22)/amin)
 eps=F(1,800)+36*e;ts=tail(F(1,96),amin)
 margin('radial_upper_box',2-F(6,7)-F(4,3)*eps)
 margin('r_inverse_cubic_derivative',4-3/amin**4)
 budget=F(28,3)+F(112,3)*e+28*(24*e+6*ts)+F(448,3)*eps
 margin('trace_ellipse_budget',12-budget)
 margin('individual_slack_budget',F(1,12)-F(1,16)-F(171,16)*e-F(9,8)*ts-eps)
 margin('individual_slack_base_domination',F(45,16)-F(13,16)-F(3,16)*e)
 margin('radial_mean',F(4,5)-(F(2,3)+F(1,14)+F(2,3)*eps)/amin)
 margin('imaginary_mean',F(1,3)-(F(5,28)+F(7,72))/amin)
 need(F(4,5)**2+F(1,3)**2==F(13,15)**2,'mean Pythagorean identity')
 identity('mean_pythagorean',F(4,5)**2+F(1,3)**2,F(13,15)**2)
 margin('c8_cap',8-F(39,5))
 margin('c7_cap',4-F(9,14)*(6+56*F(169,225)*e))
 margin('energy7',7-6-8*F(169,225)*e)
 for j in range(1,7):
  k=9-j;coeff=F(9,j)*comb(8,k)
  margin('coefficient_'+str(j),64-coeff*coeff*F(7,8)**k*e**(k-2))
 margin('firstpower_slope_13_5',F(8,3)-F(4,3)*e-F(13,5))
 # Explicit quantitative consequence, conditional on the low-F hypotheses.
 g=F(gamma['initial']);margin('quantitative_variance_1_2100',g-F(1,2100))
 quantities={'A':{str(j):str(v) for j,v in A.items()},'Cd':str(Cd),'rouche':{'lo':str(lo),'hi':str(hi),'outer':str(outer)},'cube_N':str(Nc),'cube_denominator':str(denom),'nonlinear_B':str(B),'B_j':{str(j):str(v) for j,v in Bs.items()},'variance_divisors':gamma,'individual_epsilon':str(eps),'final_tail':str(ts),'trace_budget':str(budget)}
 controls=[]
 lists=[[(0,0)]*8,[(F(1,1000),F(1,2000))]*8,[(F(1,32),0)]+[(0,0)]*7,[(F((-1)**j*(j+1),4096),F(j-3,8192)) for j in range(8)],[(F(1,128),F(1,256))]*4+[(-F(1,128),-F(1,256))]*4,[(F(j-3,2048),F((j*j)%7-3,4096)) for j in range(8)],[(-rho,0)]*8]
 for ci,crit0 in enumerate(lists):
  crit=[(F(v[0]),F(v[1])) for v in crit0];mean0=(sum(v[0] for v in crit)/8,sum(v[1] for v in crit)/8)
  nu=[(v[0]-mean0[0],v[1]-mean0[1]) for v in crit]
  V0=sum(v[0]**2+v[1]**2 for v in nu);T0=tuple(sum(pairmul(v,v)[k] for v in nu) for k in [0,1])
  H0=sum(v[0]**2+v[1]**2 for v in crit)
  need(H0==V0+8*(mean0[0]**2+mean0[1]**2),'literal mean variance')
  for eta0 in [e,e/2]:
   a0=1-eta0;p,der=polynomial_from_criticals(crit,a0)
   need(evaluate(p,(a0,F(0)))==(0,0),'literal anchor')
   for critical in crit:need(evaluate(der,critical)==(0,0),'literal derivative root')
   shifted=[(F(0),F(0))]*10
   for j,c in enumerate(p):
    for k in range(j+1):
     power=(F(1),F(0))
     for _ in range(j-k):power=pairmul(power,mean0)
     shifted[k]=pairadd(shifted[k],pairmul(c,(power[0]*comb(j,k),power[1]*comb(j,k))))
   need(shifted[8]==(0,0),'literal centering')
   need(shifted[7]==(-F(9,14)*T0[0],-F(9,14)*T0[1]),'literal Newton d7')
   up=(a0-mean0[0],-mean0[1])
   need(evaluate(shifted,up)==(0,0),'literal translated anchor')
   controls.append({'case':ci,'eta':str(eta0),'H':str(H0),'V':str(V0),'criticals':[[str(t) for t in v] for v in crit],'polynomial':[[str(t) for t in v] for v in p],'translated':[[str(t) for t in v] for v in shifted]})
 boundary_controls=[]
 for eta0 in [e,e/2]:
  a0=1-eta0;base0=8+F(8,3)*eta0-F(4,3)*eta0*eta0
  cyclic=8/a0;bad=8/(a0+rho);badcube=a0*a0+3*a0*rho+3*rho*rho
  need(cyclic>base0,'physical cyclic baseline');need(bad<8 and badcube>1,'disk hypothesis countercontrol')
  boundary_controls.append({'eta':str(eta0),'physical_cyclic_F':str(cyclic),'firstpower_baseline':str(base0),'nondisk_H':str(8*rho*rho),'nondisk_F':str(bad),'nondisk_original_cube_norm2':str(badcube)})
 return {'identities':identities,'strict_margins':margins,'quantities':quantities,'literal_controls':controls,'physical_and_nondisk_controls':boundary_controls,'proved_low_sublevel_consequences':{'variance_cost':'1/2100','all_original_motion_from_a_omega':'71/15','nonreal_cube_original_motion_from_a_omega':'151/60'},'counts':{'full_polynomial_identities':len(identities),'strict_scalar_margins':len(margins),'literal_anchored_polynomials':len(controls),'literal_critical_evaluations':8*len(controls),'boundary_physical_and_nondisk_pairs':len(boundary_controls)}}

if __name__=='__main__':print(json.dumps(build(),sort_keys=True,indent=2))
