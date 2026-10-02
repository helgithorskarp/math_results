"""Covered odd normal block and both imaginary Hessian sectors.

The analytic family, moving-root and metric interpretations are proved in
PROOF.md. Exact arithmetic/real-response modules are attributed dependencies
from source8a29091f0c1fdf3b310c3788987b3441a13fc1d6, hash-checked by verify.py.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import sys
DEPENDENCY=Path(__file__).resolve().parent.parent/'centered-real-sector'
sys.path.insert(0,str(DEPENDENCY))
from arithmetic import K,require
from centered import exact,certify,embedding,enclose,matvec,norm
from interval import I,C,DEN

def cpow(z,n):
 out=C(1)
 for _ in range(n):out*=z
 return out

def cheby(poly,t):
 S=type(t);U=[S(1),2*t];V=[S(1),t]
 for _ in range(2,len(poly)):
  U.append(2*t*U[-1]-U[-2]);V.append(2*t*V[-1]-V[-2])
 return (sum((poly[j]*U[j-1] for j in range(1,len(poly))),S(0)),
         sum((poly[j]*V[j] for j in range(len(poly))),S(0)))

def anchored(terms,r,a):
 S=type(r);poly=[S(0)]*10
 for n,m in terms:
  for j in range(n+1):poly[j]+=m*comb(n,j)*(-r)**(n-j)
 poly[0]=-sum((poly[j]*a**j for j in range(1,10)),S(0))
 return poly

def correction_poly(eta,values,V,M):
 x,y,T,_,_,_=values;r=eta*x;s=eta*y;n=(M-eta*V*y+6*(y-x))/2
 return anchored([(7,-F(9,7)*(eta*V*V/2+n*n/T)),
                  (6,54*(x-y)-9*(V*(r-2*s)+M)),
                  (5,-F(162,5)*(T+eta*(x-y)**2))],r,1-eta),n

def certificate(damage=None):
 values,Yexact,w0,w1,initial=exact();real=certify(values,Yexact,w0,w1,'lost-second-mixed' if damage=='lost-second-mixed' else None)
 c=embedding();box=[enclose(v,c)+I.bounds(-F(1,1024),F(1,1024)) for v in values]
 eta=I.bounds(0,F(1,65536));x,y,T,xi3,xi4,omega=box
 r=eta*x;s=eta*y;A=1-eta-r;D=1-eta-s;W=1+eta*omega;Btilde=T+eta*(x-y).square()
 roots=[];rows=[];forcing=[]
 for t in (-I(F(1,2))+eta*xi3,-c+eta*xi4):
  sine=(1-t.square()).sqrt();z=C(t,sine);X=z-r
  pz=9*cpow(X,6)*(cpow(z-s,2)+eta*T)
  qV=-F(9,8)*(cpow(X,8)-A**8)+(cpow(X,7)-A**7)*(-F(9,7)*(r-2*s))
  qM=-F(9,7)*(cpow(X,7)-A**7)
  qd=(cpow(X,6)-A**6)*(-9*Btilde)
  rows.append([(q/(z*pz)).im/sine for q in (qV,qM)])
  forcing.append((qd/(z*pz)).im/sine)
  roots.append((z,sine,pz,qV,qM,qd))
 if damage=='odd-normal-sign':rows[0][0]=-rows[0][0]
 det=rows[0][0]*rows[1][1]-rows[0][1]*rows[1][0]
 require(det.hi<I(-F(1,100)).lo,'odd normal determinant below-minus1/100')
 V=(-forcing[0]*rows[1][1]+rows[0][1]*forcing[1])/det
 M=(-rows[0][0]*forcing[1]+forcing[0]*rows[1][0])/det
 V0=8*(2*K((0,1,0))+1)*values[2];M0=7*(2*K((0,1,0))+1)*values[2]
 poly0,n0=correction_poly(K(0),values,V0,M0)
 f0=[cheby(poly0,t) for t in (K(-F(1,2)),-K((0,1,0)))]
 R0=[f0[0][0],f0[1][0],f0[0][1],f0[1][1],K(0)]
 t1star=[-3*w1[i]-sum((Yexact[i][j]*R0[j] for j in range(5)),K(0)) for i in range(5)]
 poly,n=correction_poly(eta,box,V,M)
 f=[];phase_second=[];phase_first=[]
 for z,sine,pz,qV,qM,qd in roots:
  X=z-r;q=qd+qV*V+qM*M
  b=(q/(z*pz)).re
  qp=cpow(X,5)*(-54*Btilde)-9*cpow(X,6)*((z-2*s)*V+M)
  pzz=54*cpow(X,5)*(cpow(z-s,2)+eta*T)+18*cpow(X,6)*(z-s)
  Croot=z*qp*b-(z*pz+cpow(z,2)*pzz)*(b.square()/2)
  value=C(0)
  for coeff in reversed(poly):value=value*z+coeff
  value+=Croot*eta
  f.append((value.im/sine,value.re));phase_second.append((Croot.im/sine,Croot.re));phase_first.append(b)
 R=[f[0][0],f[1][0],f[0][1],f[1][1],I(0)]
 B=[[I.bounds(*map(F,v)) for v in row] for row in real['five_block_enclosure']]
 B1=[[I.bounds(*map(F,v)) for v in row] for row in real['five_block_eta_difference_quotient_enclosure']]
 U1=[I.bounds(*map(F,v)) for v in real['forcing_eta_difference_quotient_enclosure']]
 Y=[[enclose(v,c) for v in row] for row in Yexact]
 rhs=[3*u+3*v-r for u,v,r in zip(U1,matvec(B1,[enclose(v,c) for v in w0]),R)]
 star=[enclose(v,c) for v in t1star]
 residual=[v-w for v,w in zip(rhs,matvec(B,star))]
 pre=matvec(Y,residual);beta=F(real['five_block_beta'])
 error=F(max(v.absmax() for v in pre),DEN)/(1-beta)
 tail=[v+I.bounds(-error,error) for v in star]
 mh=eta*V/2-3
 odd_cost=-n.square()/(T*W**3)+(2 if damage=='heavy-variance-bound' else 3)*(mh*T-D*n).square()/(T*W**5)
 alpha=1+x
 cost=-3*alpha*(3-3*eta*alpha+eta.square()*alpha.square())/A**3-3*omega*(2+eta*omega)/W.square()-2*tail[-1]/W.square()+odd_cost
 require(cost.lo>I(400).hi and cost.hi<I(650).lo,'common-imaginary scaled sigma cost in(400,650)')
 pair_response=I.bounds(*map(F,real['response_next_eta_coefficient_enclosure'][-1]))
 pair=-alpha*(3-3*eta*alpha+eta.square()*alpha.square())/A**3-omega*(2+eta*omega)/W.square()+2*pair_response/W.square()
 require(pair.lo>I(3).hi and pair.hi<I(6).lo,'centered-imaginary scaled sigma cost in(3,6)')
 require((eta.square()*x.square()).hi<I(F(1,1024)).lo and (eta.square()*y.square()+eta*T).hi<I(F(1,1024)).lo,'all branch critical moduli below1/32')
 require(F(3,160000*8)<F(1,1024) and F(128,127)/(1+F(65535,65536))<F(2,3) and F(70,33)>F(3,512),'reciprocal-domain separation margins')
 cost0=-9*(1+values[0])-6*values[5]-2*t1star[-1]-n0*n0/values[2]+3*(-3*values[2]-n0)**2/values[2]
 aa=K((-F(11564,405),-F(20482,81),F(123284,405)))
 bb=K((F(49,180),-F(105889,486),F(305123,1215)))
 require(cost0==6*(aa+6*bb)/values[2],'common initial coefficient agrees with prior8921 finite Hessian')
 pair0=3*(1+values[0])-K([F(t) for t in initial['reviewed_ell']])
 require(pair0==2*aa/values[2],'centered imaginary initial coefficient agrees with prior8921 finite Hessian')
 record={'agent':'six-sendov-3','role':'researcher','status':'covered interval certificate; ordinary analytic bridges in PROOF.md',
  'odd_matrix':[[v.record() for v in row] for row in rows],'odd_determinant':det.record(),
  'odd_response_V_M':[V.record(),M.record()],'odd_response_initial':[V0.record(),M0.record()],
  'even_correction_initial':[v.record() for v in R0],'even_tail_next_initial':[v.record() for v in t1star],
  'even_tail_error':str(error),'even_tail_next_enclosure':[v.record() for v in tail],
  'moving_unit_phase_first_scaled':[v.record() for v in phase_first],
  'moving_unit_phase_second_terms':[[v.record() for v in row] for row in phase_second],
  'real_initial':initial,'real_interval':real,
  'centered_imaginary_sigma_cost_div_eta2':pair.record(),'centered_imaginary_initial':pair0.record(),
  'branch_critical_modulus_squared_enclosures':[(eta.square()*x.square()).record(),(eta.square()*y.square()+eta*T).record()],
  'common_sigma_cost_div_eta2':cost.record(),'common_sigma_cost_initial':cost0.record(),
  'common_hessian_eigenvalue_normalization':'sigma=delta^2; norm(delta*ones_6)^2=6delta^2; eigenvalue=F_sigma/3',
  'eta_max':'1/65536','cube_radius':'1/1024','native_threads':1,'math_jobs':1}
 return record
