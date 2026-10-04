"""Independent full moving Newton/root jets and local coercivity, exposed written proof.

Author six-reviewer-1, independent reviewer. NO author program/fixture import.
Own Q(zeta_36) field and sparse operations are credited to uniform-profile-audit.
Moment slots U0,H,W,D,J21,J4,U3,J22,J41,J6,U2,extra; chart uses first six.
"""
from fractions import Fraction as Q
from math import comb
import json,hashlib
from field import E,C,W,I,Z,need
import poly as P
from intervals import Box,physical_cosine
U,H,Wv,D,J21,J4,U3,J22,J41,J6,U2,X=[P.var(j)for j in range(12)]
y=1/(3*(1+C));x=E(Q(2,3))-y;hh=14*y;uu=-8*x
k=-Q(7,18)*(1+2*C);rho=(C-5)/3;ell=k+rho
alpha=-E(Q(527,360))+Q(41,90)*C+Q(13,90)*C*C
tau=ell*ell/2;kappa=tau+Q(10,27)*alpha;sigma=alpha+rho*rho/2
bs=E(Q(2311,108))+Q(4934,27)*C-Q(1976,9)*C*C
uz=(uu+rho*hh)/8;up=uz-rho*hh/2
ws=E(Q(2512,27))+Q(5840,9)*C-Q(21392,27)*C*C
ds=-E(Q(4270,27))-Q(29492,27)*C+Q(4012,3)*C*C
ts=-E(Q(60800959,17496))-Q(307083769,17496)*C+Q(10980067,486)*C*C
w4=1/(C+2*C*C-1);w3=Q(2,3)*(7-(2-2*C*C)*w4)
zero={};one=P.const(1)
def sc(p,a):return P.scale(p,a)
def A(*p):return P.add(*p)
def M(a,b):return P.mul(a,b)
def pw(p,n):return P.power(p,n)
def series_add(*ss):return [A(*(s[j]for s in ss))for j in range(4)]
def series_mul(a,b):return [A(*(M(a[i],b[j-i])for i in range(j+1)))for j in range(4)]
def series_scale(a,c):return [sc(p,c)for p in a]
def series_power(a,n):
 o=[one,zero,zero,zero]
 for _ in range(n):o=series_mul(o,a)
 return o
def evalz(g,z,der=0):
 return A(*(sc(p, Q(comb(j,der))*_factorial(der)*z**(j-der))for j,p in enumerate(g)if j>=der))
def _factorial(n):
 o=1
 for j in range(1,n+1):o*=j
 return o
def at(p,values):return P.evaluate(p,values)
def constrows(g):return [P.const(v)for v in g]
def record(p):return P.record(p)
def real_coordinates(value):
    # Independent rational 12-by-6 linear solve in the real cyclotomic subfield.
    sine=(Z**2-Z**34)/(2*I)
    basis=[E(1),C,C*C,sine,sine*C,sine*C*C]
    rows=[[b.v[j]for b in basis]+[value.v[j]]for j in range(12)]
    pivot=0
    for col in range(6):
        chosen=next((j for j in range(pivot,12)if rows[j][col]),None)
        need(chosen is not None,'real-subfield basis independence')
        rows[pivot],rows[chosen]=rows[chosen],rows[pivot]
        v=rows[pivot][col];rows[pivot]=[a/v for a in rows[pivot]]
        for j in range(12):
            if j!=pivot and rows[j][col]:
                v=rows[j][col];rows[j]=[a-v*b for a,b in zip(rows[j],rows[pivot])]
        pivot+=1
    need(all(not any(r[:6])and not r[6]for r in rows[6:]),'whole real-subfield reconstruction')
    values=[rows[j][-1]for j in range(6)]
    need(sum((b*a for b,a in zip(basis,values)),E(0))==value,'all twelve reconstructed coordinates')
    return values

def root_box(box):
    # Rational sqrt enclosure; bisection maintains endpoints, no float input.
    lo=Q(0);hi=Q(1)
    need(0<=box.lo<=box.hi<=1,'bounded sine-square enclosure')
    for _ in range(100):
        mid=(lo+hi)/2
        if mid*mid<box.lo:lo=mid
        else:hi=mid
    upper_lo=Q(0);upper_hi=Q(1)
    for _ in range(100):
        mid=(upper_lo+upper_hi)/2
        if mid*mid>box.hi:upper_hi=mid
        else:upper_lo=mid
    need(lo*lo<=box.lo and upper_hi*upper_hi>=box.hi,'rational square-root endpoints')
    return Box(lo,upper_hi)

def field_box(value,c):
    a=real_coordinates(value);sine=root_box(1-c*c)
    return a[0]+a[1]*c+a[2]*c*c+sine*(a[3]+a[4]*c+a[5]*c*c)

def run(damage=None):
 checks=[];out={}
 def equal(a,b,name):need(a==b,name);checks.append(name)
 # Formal Newton identity route: ten independent moving moments, all ten columns.
 sums=[[zero]*4 for _ in range(9)]
 sums[1]=[zero,U,Wv,zero];sums[2]=[zero,sc(H,-1),D,zero]
 sums[3]=[zero,zero,sc(J21,-3),U3]
 sums[4]=[zero,zero,J4,sc(J22,-6)]
 sums[5]=[zero,zero,zero,sc(J41,5)]
 sums[6]=[zero,zero,zero,sc(J6,-1)]
 es=[[one,zero,zero,zero]]
 for n in range(1,9):
  es.append(series_scale(series_add(*(series_scale(series_mul(es[n-j],sums[j]),(-1)**(j-1))for j in range(1,n+1))),Q(1,n)))
 primitive=[[zero]*10 for _ in range(4)]
 for n,e in enumerate(es):
  j=9-n
  for order,p in enumerate(e):
   p=sc(p,(-1)**n*Q(9,j));primitive[order][j]=A(primitive[order][j],p)
   for t in range(4-order):primitive[order+t][0]=A(primitive[order+t][0],sc(p,-(-1)**t*comb(j,t)))
 # Independent exponential generating series: E(t)=exp(sum (-1)^(m-1)P_m t^m/m).
 expmap=[[zero]*4 for _ in range(9)];expmap[0]=[one,zero,zero,zero]
 logarithm=[[zero]*4]+[series_scale(sums[j],Q((-1)**(j-1),j))for j in range(1,9)]
 term=[[zero]*4 for _ in range(9)];term[0]=[one,zero,zero,zero]
 for n in range(1,4):
  term=[series_add(*(series_mul(term[i],logarithm[j-i])for i in range(j+1)))for j in range(9)]
  for j in range(9):expmap[j]=series_add(expmap[j],series_scale(term[j],Q(1,_factorial(n))))
 for j in range(9):equal(es[j],expmap[j],'all formal elementary coefficients '+str(j))
 # Entire anchor equals zero as a formal truncated eta polynomial.
 anchor=[zero]*4
 for j in range(10):
  value=series_mul([primitive[o][j]for o in range(4)],[P.const((-1)**o*comb(j,o))if o<=j else zero for o in range(4)])
  anchor=series_add(anchor,value)
 equal(anchor,[zero]*4,'whole actual marked-root anchor')
 out['ten_formal_moment_primitive']=[[record(p)for p in row]for row in primitive]
 g=[ [P.substitute(p,{0:P.const(uu),1:P.const(hh)})for p in row]for row in primitive]
 literal1=[zero]*10;literal1[0]=P.const(9-9*x-9*y);literal1[8]=P.const(9*x);literal1[7]=P.const(9*y)
 equal(g[1],literal1,'whole moving first jet')
 literal2=[zero]*10
 literal2[8]=sc(Wv,-Q(9,8));literal2[7]=sc(A(P.const(uu*uu),sc(D,-1)),Q(9,14))
 literal2[6]=A(P.const(-3*uu*hh/4),sc(J21,Q(3,2)))
 literal2[5]=A(P.const(9*hh*hh/40),sc(J4,-Q(9,20)))
 literal2[0]=A(P.const(-36-9*uu+9*hh/2),sc(A(*literal2[1:]),-1))
 equal(g[2],literal2,'whole moving second jet')
 if damage=='freeze-third':g[3]=[P.const(at(p,[uu,hh,ws,ds,hh*up,hh*hh/2,6*uz**3+2*up**3,hh*up*up,hh*hh*up/2,hh**3/4,6*uz*uz+2*up*up,0]))for p in g[3]]
 moving_roots=[];moving_normals=[]
 # All nine whole coefficient equations and normals, no sampled roots.
 for j in range(9):
  z=W**j;L=sc(evalz(g[1],z),-1/(9*z**8))
  d=sc(A(evalz(g[2],z),M(evalz(g[1],z,1),L),sc(pw(L,2),36*z**7)),-1/(9*z**8))
  e=sc(A(evalz(g[3],z),M(evalz(g[2],z,1),L),M(evalz(g[1],z,1),d),sc(M(evalz(g[1],z,2),pw(L,2)),Q(1,2)),sc(M(L,d),72*z**7),sc(pw(L,3),84*z**6)),-1/(9*z**8))
  if damage=='third-cross' and j==3:e=A(e,one)
  proposed=[P.const(z),L,d,e]
  residual=[zero]*4
  for power in range(10):
   residual=series_add(residual,series_mul([g[o][power]for o in range(4)],series_power(proposed,power)))
  equal(residual,[zero]*4,'all moving root residuals '+str(j))
  n1=P.real(sc(L,z.conjugate()));n2=A(P.real(sc(d,z.conjugate())),sc(M(L,P.conj(L)),Q(1,2)))
  n3=A(P.real(sc(e,z.conjugate())),P.real(M(L,P.conj(d))))
  moving_roots.append([record(L),record(d),record(e)]);moving_normals.append([n1,n2,n3])
 out['all_nine_moving_roots']=moving_roots
 out['all_nine_moving_normals']=[[record(v)for v in row]for row in moving_normals]
 # Whole second normal rows and reflection at ALL four active labels.
 radial=[]
 for j in [3,4]:
  z=W**j;a=E(Q(3,2))if j==3 else 1+C;b=E(Q(3,2))if j==3 else 2-2*C*C
  q,s=(E(-1),E(Q(3,4)))if j==3 else(-2*C,1-C*C)
  K=-(7*x*x/2+6*x*y*q+5*y*y*q*q/2)*s
  row=A(P.const(4+uu-hh/2+b*uu*uu/14+K),sc(A(P.const(-uu*hh/12),sc(J21,Q(1,6))),1-(z**6).real()),sc(A(P.const(hh*hh/40),sc(J4,-Q(1,20))),1-(z**5).real()))
  normal=A(row,sc(Wv,-a/8),sc(D,-b/14))
  for label in [j,9-j]:equal(moving_normals[label][0],zero,'active first normal '+str(label));equal(moving_normals[label][1],normal,'whole moving second normal '+str(label))
  equal(moving_normals[j][2],moving_normals[9-j][2],'whole moving third reflection '+str(j))
  radial.append(row)
 out['full_second_radial_rows']=[record(p)for p in radial]
 equal(w3*E(Q(3,2))+w4*(1+C),E(8),'positive dual W payment')
 equal(w3*E(Q(3,2))+w4*(2-2*C*C),E(7),'positive dual D payment')
 # Independently expand one squared-distance binomial series in eta, with u,h² formal.
 u,h2=P.var(0),P.var(1)
 V=[zero,A(h2,sc(A(one,u),-2)),pw(A(one,u),2),zero]
 binomial=[one,zero,zero,zero];power=[one,zero,zero,zero];binc=Q(1)
 for n in range(1,4):
  power=series_mul(power,V);binc*=Q(-(2*n-1),2*n);binomial=series_add(binomial,series_scale(power,binc))
 direct=[one,A(one,u,sc(h2,-Q(1,2))),A(pw(A(one,u),2),sc(M(A(one,u),h2),-Q(3,2)),sc(pw(h2,2),Q(3,8))),A(pw(A(one,u),3),sc(M(pw(A(one,u),2),h2),-3),sc(M(A(one,u),pw(h2,2)),Q(15,8)),sc(pw(h2,3),-Q(5,16)))]
 equal(binomial,direct,'entire first-power inverse-distance scalar jet')
 base=bs-4*uz*uz-alpha*hh*hh/2
 scalar=A(sc(U2,Q(1,2)),P.const(8+2*uu-3*hh/2),sc(J21,-Q(3,2)),sc(J4,Q(3,8)),sc(radial[0],w3),sc(radial[1],w4))
 equal(scalar,A(P.const(base),sc(U2,Q(1,2)),sc(J21,rho),sc(J4,sigma)),'whole scalar dual elimination')
 # Stationary specialization and BOTH normalization payments.
 vals=[uu,hh,ws,ds,hh*up,hh*hh/2,6*uz**3+2*up**3,hh*up*up,hh*hh*up/2,hh**3/4,6*uz*uz+2*up*up,0]
 f3=lambda u,h2:(1+u)**3-3*(1+u)**2*h2+Q(15,8)*(1+u)*h2**2-Q(5,16)*h2**3
 scalar3=2*ws-Q(3,2)*vals[10]+Q(3,2)*ds+6*f3(uz,E(0))+2*f3(up,hh/2)
 mean_payment=uz*ws;norm_payment=(rho*up+sigma*hh)*(vals[10]-ds)
 if damage=='omit-mean':mean_payment=E(0)
 if damage=='omit-norm':norm_payment=E(0)
 total=scalar3+w3*at(moving_normals[3][2],vals)+w4*at(moving_normals[4][2],vals)+mean_payment+norm_payment
 equal(total,ts,'full stationary third coefficient and two normalization payments')
 equal(up+rho*hh/2,uz,'all-eight stationary u gradient')
 out['stationary_payments']={n:v.record()for n,v in {'scalar':scalar3,'mean':mean_payment,'norm':norm_payment,'Tstar':total,'n3':at(moving_normals[3][2],vals),'n4':at(moving_normals[4][2],vals)}.items()}
 # Independent all-nine affine motion norm table and whole-line winner signs.
 affine=[]
 for j in range(9):
     z=W**j;lj=at(sc(evalz(g[1],z),-1/(9*z**8)),vals)
     dj=at(sc(A(evalz(g[2],z),M(evalz(g[1],z,1),P.const(lj)),P.const(36*z**7*lj*lj)),-1/(9*z**8)),vals)
     odd=I*((1+2*C)*(z**8+z**7-2)+(z**6-1))/2
     hj=-odd/(9*z**8)
     explicit=I*((3+4*C)*z-(1+2*C)*(1+z**-1)-z**-2)/18
     equal(hj,explicit,'entire inherited odd harmonic '+str(j))
     affine.append([dj*dj.conjugate(),2*(dj*hj.conjugate()).real(),hj*hj.conjugate()])
 equal(affine[2][0],affine[7][0],'reflected pair zero-skew norm equality')
 equal(affine[2][1],-affine[7][1],'reflected pair opposite linear cusp')
 equal(affine[2][2],affine[7][2],'reflected pair identical quadratic norm')
 physical=physical_cosine();signs={}
 cusp=field_box(affine[7][1],physical);need(cusp.lo>0,'physical positive winning cusp');checks.append('positive motion cusp')
 for j in [0,1,3,4,5,6,8]:
     gaps=[a-b for a,b in zip(affine[7],affine[j])]
     for order,gap in enumerate(gaps):
         box=field_box(gap,physical)
         # Some odd coefficients vanish identically; a strict constant gap still suffices.
         need(gap==0 or box.lo>0,'whole real-line nonwinner gap '+str((j,order)))
         signs[str((j,order))]={'zero':gap==0,'box':box.record()};checks.append('real-line nonwinner coefficient '+str((j,order)))
 out['all_nine_motion_quadratics']=[[v.record()for v in row]for row in affine]
 out['motion_winner_signs']=signs;out['positive_cusp']=cusp.record()
 # Formal unconstrained projection using aggregate moments, then exact balance/norm/mean.
 # slots S0,S2,S3,S4,Umean,U2,Vdot,J21,delta are all independent here.
 S0,S2,S3,S4,Um,Usq,Vdot,Jmix,delta=[P.var(j)for j in range(9)]
 t=sc(S3,ell/hh)
 umin_norm=A(P.const(8*uz*uz),sc(S2,-2*uz*rho),sc(M(t,S0),2*uz),sc(S4,rho*rho),sc(M(t,S3),-2*rho),M(pw(t,2),S2))
 udot=A(sc(Um,uz),sc(Jmix,-rho),M(t,Vdot))
 square=A(Usq,sc(udot,-2),umin_norm)
 left=A(P.const(base),sc(Usq,Q(1,2)),sc(Jmix,rho),sc(S4,sigma))
 right=A(P.const(bs-alpha*hh*hh/2),sc(S4,alpha),sc(pw(S3,2),tau/hh),sc(square,Q(1,2)),sc(M(S3,delta),ell/hh))
 sub={0:zero,1:P.const(hh),4:P.const(uu),6:A(sc(S3,k),delta)}
 if damage=='mixed-sign':right=A(right,sc(M(S3,delta),-2*ell/hh))
 equal(P.substitute(left,sub),P.substitute(right,sub),'whole signed mixed projection under only exact constraints')
 out['projection_defect'] = record(P.sub(P.substitute(left,sub),P.substitute(right,sub)))
 # Literal balanced pair chart after eliminating q²; exact six-coordinate polynomial.
 tt=[P.var(j)for j in range(6)];r=sc(A(*tt),-Q(1,2));R=[A(*(pw(t,j)for t in tt))for j in range(7)]
 q2=A(P.const(hh/2),sc(R[2],-Q(1,2)),sc(pw(r,2),-1))
 cubic=A(sc(pw(r,3),2),sc(M(r,q2),6),R[3])
 quartic=A(sc(pw(r,4),2),sc(M(pw(r,2),q2),12),sc(pw(q2,2),2),R[4],P.const(-hh*hh/2))
 cubic2=A(sc(r,3*hh),sc(M(r,R[2]),-3),sc(pw(r,3),-4),R[3])
 quartic2=A(sc(R[2],-hh),sc(pw(r,2),4*hh),R[4],sc(pw(R[2],2),Q(1,2)),sc(M(pw(r,2),R[2]),-4),sc(pw(r,4),-8))
 equal(cubic,cubic2,'whole balanced cubic chart')
 equal(quartic,quartic2,'whole balanced quartic chart')
 cost=A(sc(quartic,alpha),sc(pw(cubic,2),tau/hh))
 quadratic={e:v for e,v in cost.items()if sum(e)==2}
 residual=P.sub(cost,quadratic)
 positive=A(sc(pw(r,2),9*hh*kappa),sc(A(*(pw(A(t,sc(r,Q(1,3))),2)for t in tt)),-alpha*hh))
 if damage=='chart-kappa':positive=A(positive,pw(r,2))
 equal(quadratic,positive,'whole positive definite local quadratic form')
 need(all(sum(e)>=4 for e in residual),'no concealed cubic/lower chart remainder');checks.append('all entire chart remainder degrees at least four')
 out['exact_chart']={n:record(v)for n,v in {'J3':cubic,'J4minus':quartic,'cost':cost,'quadratic':quadratic,'higher':residual}.items()}
 # Exact normalization of the mixed defect: h=m1+s v, u=uhat+n1.
 # Variables s,m,n,J3(v), vdotuhat, sumuhat, with sumv=0,normv²=H.
 ss,mm,nn,jj,vv,um=[P.var(j)for j in range(6)]
 actual_mixed=A(M(ss,vv),M(mm,um),sc(M(mm,nn),8))
 actual_j3=A(M(pw(ss,3),jj),sc(M(pw(ss,2),mm),3*hh),sc(pw(mm,3),8))
 solve_delta=P.sub(P.sub(actual_mixed,sc(actual_j3,k)),M(ss,P.sub(vv,sc(jj,k))))
 prescribed=A(sc(M(P.sub(ss,pw(ss,3)),jj),k),M(mm,um),sc(M(mm,nn),8),sc(M(pw(ss,2),mm),-3*k*hh),sc(pw(mm,3),-8*k))
 equal(solve_delta,prescribed,'whole actual centered mixed-defect change')
 out['centered_mixed_change']=record(prescribed)
 # Physical sign bounds use rational bisection, never numerical embedding.
 c=physical_cosine();hy=14/(3*(1+c));ar=-Q(527,360)+Q(41,90)*c+Q(13,90)*c*c
 kr=-Q(7,18)*(1+2*c);rr=(c-5)/3;tr=(kr+rr)**2/2;kap=tr+Q(10,27)*ar
 den=c+2*c*c-1;rw4=1/den;rw3=Q(2,3)*(7-(2-2*c*c)*rw4)
 quantities={'H':hy,'negative_alpha':-ar,'kappa':kap,'w3':rw3,'w4':rw4,'normal_row_determinant_magnitude':3*den/224}
 for name,box in quantities.items():need(box.lo>0,'positive physical '+name);checks.append('positive physical '+name)
 out['physical_signs']={n:v.record()for n,v in quantities.items()}
 if damage=='freeze-third':
  # A moving U3 column survives in the third polynomial; freezing must be rejected.
  need(any(e[6]>0 for p in g[3]for e in p),'moving third U3 column was discarded')
 out['checks']=checks
 return out
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--damage');p.add_argument('--record');a=p.parse_args()
 result=run(a.damage);raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode()
 if a.record:
  from pathlib import Path
  Path(a.record).write_bytes(raw)
 receipt={'agent':'six-reviewer-1','role':'independent mathematical reviewer','checks':len(result['checks']),'whole_record_bytes':len(raw),'whole_record_sha256':hashlib.sha256(raw).hexdigest(),'author_native_or_EXPECTED_imported':False,'field':'Q(zeta_36), Phi36=X^12-X^6+1, exact Fraction','status':'all exact identities and signs verified'}
 print(json.dumps(receipt,sort_keys=True,separators=(',',':')))
