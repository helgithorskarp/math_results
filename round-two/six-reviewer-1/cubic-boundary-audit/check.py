#!/usr/bin/env python3
"""Independent cubic/fourth boundary audit; imports only published reviewer kernels."""
import argparse,hashlib,importlib.util,json,pathlib
from fractions import Fraction as F
p=pathlib.Path(__file__).resolve().parent.parent/'profile-stability-audit'/'check.py'
if hashlib.sha256(p.read_bytes()).hexdigest()!='bb2c2a85b1718ab29a3ba25ccf6e79e18ae0d142d349ec0f1f586635d106c38e':raise ValueError('published reviewer polynomial kernel mismatch')
spec=importlib.util.spec_from_file_location('self_profile',p);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
Ring,P,Z,K,c,base=old.Ring,old.P,old.Z,old.K,old.c,old.prior
checks=[]
def reject(fn,label):
 try:fn()
 except (ValueError,RuntimeError):return label
 raise ValueError("undetected mathematical mutation: "+label)
def require(v,n):
 if not v:raise ValueError(n)
 checks.append(n)
def sub(p,values):
 r=p.ring.scalar()
 for key,a in p.a.items():
  term=p.ring.scalar(a)
  for j,k in enumerate(key):term*= (p.ring.variable(j) if j not in values else values[j])**k
  r+=term
 return r
def constant(p):
 require(all(sum(k)==0 for k in p.a),'scalar coefficient extraction')
 return p.a.get(p.ring.zero,K())
def rawrecord(poly):
 out=[]
 for zd,a in enumerate(poly):
  for key,v in a.a.items():out.append([[key[0],zd,*key[1:]],list(map(str,v.a))])
 return sorted(out)
def digest(v):return hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest()
def branches(poly,eta,order):
 result=[]
 for k in range(9):
  w=base.WROOT**k;z=eta.ring.scalar(w)
  for n in range(1,order+1):z-=old.evaluate(poly,z).coefficient_first(n)*eta**n*w/9
  require(old.evaluate(poly,z)==0,'full original-root residual'+str(k))
  result.append((z,(z*z.conjugate()-1)/2))
 return result
# Exact coefficients of exp(sum (-1)^(j-1) P_j t^j/j), by product of
# truncated exponential factors. No Newton elementary-symmetric recurrence.
def elementary_partition(moments,zero):
 es=[Z(zero.ring.scalar(1))]+[Z(zero) for _ in range(8)]
 for j in range(1,9):
  factor=[Z(zero.ring.scalar(1))]
  x=moments[j]*((-1)**(j-1))/j
  for n in range(1,8//j+1):factor.append(factor[-1]*x/n)
  nxt=[Z(zero) for _ in range(9)]
  for k in range(9):
   for n,a in enumerate(factor):
    if k+j*n<=8:nxt[k+j*n]+=es[k]*a
  es=nxt
 return es

def build():
 y=1/(3*(1+c));x=F(2,3)-y;H=14*y;U0=-8*x;rho=(c-5)/3
 C=F(8,3)+y;Bstar=F(2311,108)+F(4934,27)*c-F(1976,9)*c*c
 uz=(U0+rho*H)/8;up=uz-rho*H/2
 d=2*c*c-1;v=2*d*d-1;A=[K(F(3,2)),1+c];B=[K(F(3,2)),1-d]
 weights=[F(2,3)*(7-(1-d)/(c+d)),1/(c+d)]
 sigma=F(3,8)-(F(3,2)*weights[0]+(1-v)*weights[1])/20
 U2=6*uz**2+2*up**2;U3=6*uz**3+2*up**3;J21=H*up;J4=H*H/2
 J22=H*up*up;J41=H*H*up/2;J6=H**3/4
 TT=[]
 for k in [3,4]:
  rr,t=(K(-1),K(F(3,4))) if k==3 else(-2*c,1-c*c)
  C6,C5=(K(0),K(F(3,2))) if k==3 else(K(F(3,2)),1-v)
  TT.append(4+U0-H/2+B[k-3]*U0*U0/14+C6*(-U0*H/12+J21/6)+C5*(H*H/40-J4/20)-(F(7,2)*x*x+6*x*y*rr+F(5,2)*y*y*rr*rr)*t)
 aa,bb=A[0]/8,B[0]/14;ee,ff=A[1]/8,B[1]/14;det=aa*ff-bb*ee
 Ws=(TT[0]*ff-TT[1]*bb)/det;Ds=(aa*TT[1]-ee*TT[0])/det;gamma=(U2-Ds)/(2*H)
 # Six independently scaled imaginary moments, ten real moments.
 names=['U','H','W','D','J21','U3','J4','J22','J41','J6','Is','Ip','Ip3','Ip4','Ip5','Ip6']
 rg=Ring(17,first_cap=3);eta=rg.variable(0);t={n:rg.variable(i+1) for i,n in enumerate(names)};zero=rg.scalar()
 U,HH,W,D,j21,u3,j4,j22,j41,j6,Is,Ip,Ip3,Ip4,Ip5,Ip6=[t[n] for n in names]
 moments=[Z(zero),Z(U*eta+W*eta**2,Is*eta**2),Z(-HH*eta+D*eta**2,Ip*eta**2),Z(-3*j21*eta**2+u3*eta**3,Ip3*eta**2),Z(j4*eta**2-6*j22*eta**3,Ip4*eta**3),Z(5*j41*eta**3,Ip5*eta**3),Z(-j6*eta**3,Ip6*eta**3),Z(zero),Z(zero)]
 es=elementary_partition(moments,zero);primitive=[Z(zero) for _ in range(10)]
 for j in range(9):primitive[9-j]=es[j]*(9*(-1)**j)/(9-j)
 ar,ai=zero,zero
 for q in reversed(primitive):ar=ar*(1-eta)+q.r;ai=ai*(1-eta)+q.i
 primitive[0]=Z(-ar,-ai)
 K6=84+F(63,2)*U-F(27,2)*HH-9*W+F(9,2)*(U**2-D)-F(9,2)*U*HH+9*j21+F(9,8)*HH**2-F(9,4)*j4
 g6=[zero for _ in range(10)];g6[7]=9*U*W/7;g6[6]=-U**3/4+3*(U*D-HH*W)/4-u3/2
 g6[5]=F(9,5)*(U**2*HH/4-HH*D/4-U*j21+F(3,2)*j22)
 g6[4]=-F(9,4)*(U*HH**2/8-HH*j21/2-U*j4/4+j41);g6[3]=3*(HH**3/48-HH*j4/8+j6/6);g6[0]=K6-sum(g6[1:],zero)
 for j,q in enumerate(primitive):require(q.r.coefficient_first(3)==g6[j],'complete g6 partition coefficient'+str(j))
 values={'U':U0,'H':H,'W':Ws,'D':Ds,'J21':J21,'U3':U3,'J4':J4,'J22':J22,'J41':J41,'J6':J6,'Is':0,'Ip':0,'Ip3':0,'Ip4':0,'Ip5':0,'Ip6':0}
 mapping={i+1:K(values[n]) for i,n in enumerate(names)}
 # Independently sum the binomial expansion of each exact squared distance.
 sr=Ring(12,first_cap=3);se=sr.variable(0)
 snames=['U','H','W','D','U2','U3','J21','J4','J22','J41','J6']
 sv={name:sr.variable(i+1) for i,name in enumerate(snames)}
 point=Ring(3,first_cap=3);pe,pu,ph=[point.variable(i) for i in range(3)]
 inv=old.binomial((1-pe*(1+pu))**2+pe*ph,F(-1,2),3)
 moment={(0,0):sr.scalar(8),(1,0):sv['U']+se*sv['W'],(0,1):sv['H']+se*(sv['U2']-sv['D']),(2,0):sv['U2'],(3,0):sv['U3'],(1,1):sv['J21'],(2,1):sv['J22'],(0,2):sv['J4'],(1,2):sv['J41'],(0,3):sv['J6']}
 summed=sr.scalar()
 for (n,a,b),co in inv.a.items():summed+=co*se**n*moment[(a,b)]
 want2=sv['W']+sv['D']/2+sv['U2']/2+8+2*sv['U']-F(3,2)*sv['H']-F(3,2)*sv['J21']+F(3,8)*sv['J4']
 want3=2*sv['W']-F(3,2)*(sv['U2']-sv['D'])+8+3*sv['U']+3*sv['U2']+sv['U3']-3*sv['H']-6*sv['J21']-3*sv['J22']+F(15,8)*sv['J4']+F(15,8)*sv['J41']-F(5,16)*sv['J6']
 for n,want in [(0,sr.scalar(8)),(1,8+sv['U']-sv['H']/2),(2,want2),(3,want3)]:require(summed.coefficient_first(n)==want,'complete independently summed scalar jet'+str(n))
 # Convert the complete static real limiting jet to a univariate ring.
 rs=Ring(1,first_cap=3);ets=rs.variable(0);star=[]
 for q in primitive:
  specialized=sub(q.r,mapping);star.append(P(rs,{(key[0],):a for key,a in specialized.a.items()}))
 radstar=branches(star,ets,3);Rstar=[constant(radstar[k][1].coefficient_first(3)) for k in [3,4]]
 scalar=2*Ws-F(3,2)*(U2-Ds)+6*(1+uz)**3+2*((1+up)**3-3*(H/2)*(1+up)**2+F(15,8)*(H/2)**2*(1+up)-F(5,16)*(H/2)**3)
 normal=uz*Ws+(rho*up+sigma*H)*(U2-Ds)
 C3=scalar+normal+sum(weights[i]*Rstar[i] for i in range(2))
 require(C3== -F(60800959,17496)-F(307083769,17496)*c+F(10980067,486)*c*c,'complete independent cubic dual cost')
 base.negative(C3,'C3 negative');checks.append('C3 negative')
 # Independent free m/theta/common-fourth correction factor polynomial.
 rf=Ring(4,first_cap=4);ef,m,theta,repair=[rf.variable(i) for i in range(4)];one=rf.scalar(1)
 L0=uz*ef+Ws*ef**2/8+m*ef**3+repair*ef**4;Lp=up*ef+Ws*ef**2/8+m*ef**3+repair*ef**4
 derivative=[one]
 for _ in range(6):derivative=old.multiply(derivative,[-L0,one])
 pair=old.multiply([-Lp,one],[-Lp,one]);pair[0]+=H/2*ef*(1+gamma*ef+theta*ef**2)**2
 derivative=[9*q for q in old.multiply(derivative,pair)]
 family=[rf.scalar()]+[q/(j+1) for j,q in enumerate(derivative)];family[0]=-old.evaluate(family,1-ef)
 roots=branches(family,ef,4)
 def pick(p,key):return p.a.get(key,K())
 for k in [3,4,5,6]:
  rr=roots[k][1].coefficient_first(3);idx=0 if k in [3,6] else 1
  require(pick(rr,(0,1,0,0))==-A[idx],'all active independent common-third response')
  require(pick(rr,(0,0,1,0))==H*B[idx]/7,'all active independent pair-radius response')
  require(roots[k][1].coefficient_first(1)==0 and roots[k][1].coefficient_first(2)==0,'all active lower jets zero')
 p0=pick(roots[3][1].coefficient_first(3),(0,0,0,0));p1=pick(roots[4][1].coefficient_first(3),(0,0,0,0))
 a0,b0=-A[0],H*B[0]/7;a1,b1=-A[1],H*B[1]/7;det=a0*b1-b0*a1
 ms=(-p0*b1+b0*p1)/det;ts=(-a0*p1+p0*a1)/det
 require(ms== -F(17403419,34992)-F(45702565,17496)*c+F(180635,54)*c*c,'independent fitted cubic shift')
 require(ts== -F(1162307,23328)-F(5484833,11664)*c+F(52426519,93312)*c*c,'independent fitted pair-radius correction')
 objective=6*old.binomial(1-ef-L0,F(-1),4)+2*old.binomial((1-ef-Lp)**2+H/2*ef*(1+gamma*ef+theta*ef**2)**2,F(-1,2),4)
 constmap={1:ms,2:ts,3:K(10)};oraw=sub(objective,constmap)
 for n,expect in [(0,8),(1,C),(2,Bstar),(3,C3)]:require(constant(oraw.coefficient_first(n))==expect,'attaining objective coefficient'+str(n))
 radial=[];thresholds=[]
 for k,(z,r) in enumerate(roots):
  zs=sub(z,constmap);rr=sub(r,constmap)
  vals=[constant(rr.coefficient_first(n)) for n in range(1,5)]
  if k==0:require(zs==1-ef,'exact marked branch')
  elif k in [3,4,5,6]:
   require(vals[:3]==[K(0)]*3,'all active first3 zero')
   base.negative(vals[3],'active fourth inward');checks.append('active fourth inward'+str(k))
   idx=0 if k in [3,6] else 1
   generic4=sub(r.coefficient_first(4),{1:ms,2:ts})
   require(pick(generic4,(0,0,0,1))==-A[idx],'every fourth common-shift response')
   if k in [3,4]:thresholds.append(pick(generic4,(0,0,0,0))/A[idx])
  else:base.negative(vals[0],'inactive first inward');checks.append('inactive first inward'+str(k))
  radial.append({'index':k,'radial':[list(map(str,base.cubic(q))) for q in vals],'full_jet_hash':digest(rawrecord([zs]))})
 require(thresholds[0]!=thresholds[1],'unequal fourth thresholds')
 if base.enclosure(thresholds[0]-thresholds[1])[0]>0:threshold=thresholds[0];outer=3
 else:base.positive(thresholds[1]-thresholds[0],'dominant fourth threshold');threshold=thresholds[1];outer=4
 require(base.enclosure(threshold)[1]<10,'ten fourth repair sufficient')
 # The same defining polynomial with repair5 retains C3 and all-root containment.
 repaired5=[]
 for k,(z,r) in enumerate(roots):
  zs=sub(z,{1:ms,2:ts,3:K(5)});rr=sub(r,{1:ms,2:ts,3:K(5)})
  vals=[constant(rr.coefficient_first(n)) for n in range(1,5)]
  if k in [3,4,5,6]:
   require(vals[:3]==[K(0)]*3,'repair5 active first3 zero')
   base.negative(vals[3],'repair5 fourth inward');checks.append('repair5 fourth inward'+str(k))
  elif k==0:require(zs==1-ef,'repair5 exact marked root')
  else:base.negative(vals[0],'repair5 inactive first inward');checks.append('repair5 inactive first inward'+str(k))
  repaired5.append({'index':k,'radial':[list(map(str,base.cubic(q))) for q in vals],'full_jet_hash':digest(rawrecord([zs]))})
 fifth_objective=sub(objective,{1:ms,2:ts,3:K(5)})
 require(constant(fifth_objective.coefficient_first(3))==C3,'repair5 objective cubic unchanged')
 require(constant(oraw.coefficient_first(4)-fifth_objective.coefficient_first(4))==40,'repair5 fourth objective decreases by40')
 lo,hi=base.enclosure(threshold)
 require(F('4.4112082231864')<lo<hi<F('4.4112082231865'),'sharp fixed-family fourth threshold decimal enclosure')
 mutations=[reject(lambda:require((primitive[6].r+eta**3).coefficient_first(3)==g6[6],'damaged generic third moment'),'generic eta3 coefficient'),
 reject(lambda:require(C3-normal==C3,'normalization omitted'),'normalization cost omitted'),
 reject(lambda:require(old.evaluate(family,roots[4][0]+ef**3)==0,'damaged cubic root'),'original-root cubic jet'),
 reject(lambda:base.negative(-constant(sub(roots[4][1],constmap).coefficient_first(4)),'damaged radial sign'),'active fourth sign'),
 reject(lambda:require(hi<F(4),'insufficient fourth repair'),'repair4 fails')]
 rate=H*gamma*gamma+Ws*Ws/8;base.positive(rate,'profile_rate positive');checks.append('profile rate positive')
 constants={'C':C,'Bstar':Bstar,'C3':C3,'Dstar':Ds,'H':H,'U0':U0,'Wstar':Ws,'eta3_shift':ms,'gamma':gamma,'normalization_cost':normal,'profile_rate_squared':rate,'radial_eta3_cost':Rstar,'radius_eta2_correction':ts,'rho':rho,'scalar_eta3_cost':scalar,'u_pair':up,'u_zero':uz}
 encoded={n:([list(map(str,base.cubic(q))) for q in v] if isinstance(v,list) else list(map(str,base.cubic(v)))) for n,v in constants.items()}
 result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','constants':encoded,'checks':list(checks),'generic_scalar_eta3_hash':digest(rawrecord([summed])), 'generic_partition_g6':{'full_coefficient_hash':digest([[[j,list(key)],list(map(str,a.a))] for j,q in enumerate(g6) for key,a in sorted(q.a.items())]),'imaginary_symbols':6,'real_symbols':10,'terms':sum(len(q.a) for q in g6)},'all_nine_root_branches':radial,'repair5_all_nine_root_branches':repaired5,'damage_controls':mutations,'objective_eta4_repair10':list(map(str,base.cubic(constant(oraw.coefficient_first(4))))),'objective_eta4_repair5':list(map(str,base.cubic(constant(fifth_objective.coefficient_first(4))))),'construction':{'primitive_hash':digest(rawrecord(family)),'derivative_hash':digest(rawrecord(derivative)),'objective_hash':digest(rawrecord([objective]))},'fourth_repair_threshold':{'coefficients':list(map(str,base.cubic(threshold))),'active_pair':outer,'rational_enclosure':list(map(str,base.enclosure(threshold))),'other_threshold':list(map(str,base.cubic(thresholds[1] if outer==3 else thresholds[0])))} }
 result['checks']=list(checks)
 return result
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--fixture',type=pathlib.Path,default=pathlib.Path(__file__).with_name('expected.json'))
 parser.add_argument('--author',type=pathlib.Path)
 parser.add_argument('--write',action='store_true',help='development only: regenerate own full fixture')
 args=parser.parse_args()
 # Fail missing/malformed input before any mathematical work.
 expected=None if args.write else json.loads(args.fixture.read_text())
 r=build()
 text=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if args.write:args.fixture.write_text(text)
 elif r!=expected:raise ValueError('complete independent record differs from external fixture')
 if args.author:
  author=json.loads(args.author.read_text())
  require(r['constants']==author['constants'],'all17 author constants independently matched')
  require([p['radial'] for p in r['all_nine_root_branches']]==[p['radial'] for p in author['construction']['all_nine_root_branches']],'all36 author radial coefficients independently matched')
 print(f"PASS: {len(r['checks'])} independent exact checks; {len(r['damage_controls'])} mutations rejected; all nine roots through fourth order.")
 print('Complete record SHA256: '+hashlib.sha256(text.encode()).hexdigest())
 print('Sharp fixed-family fourth repair threshold lies in (4.4112082231864,4.4112082231865); repair5 suffices.')
 if args.author:print('All17 published constants and all36 published radial coefficients independently matched.')
if __name__=='__main__':main()
