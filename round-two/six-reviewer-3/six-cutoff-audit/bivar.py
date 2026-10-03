"""Fresh sparse Q[q,k] arithmetic, lex division and exact substitution."""
from fractions import Fraction as F
from exact import need

class P:
 def __init__(self,x=0):
  if isinstance(x,P):self.c=dict(x.c);return
  need(not isinstance(x,float),'no floating coefficients')
  d=x if isinstance(x,dict) else {(0,0):x}
  self.c={tuple(k):F(v) for k,v in d.items() if v}
  need(all(len(k)==2 and all(type(i)is int and i>=0 for i in k) for k in self.c),'nonnegative bivariate exponents')
 def __add__(self,x):
  d=dict(self.c)
  for k,v in P(x).c.items():d[k]=d.get(k,F(0))+v
  return P(d)
 __radd__=__add__
 def __neg__(self):return P({k:-v for k,v in self.c.items()})
 def __sub__(self,x):return self+-P(x)
 def __rsub__(self,x):return P(x)+-self
 def __mul__(self,x):
  d={}
  for a,b in self.c.items():
   for c,v in P(x).c.items():
    k=(a[0]+c[0],a[1]+c[1]);d[k]=d.get(k,F(0))+b*v
  return P(d)
 __rmul__=__mul__
 def __pow__(self,n):
  need(type(n)is int and n>=0,'nonnegative power');r=P(1);a=self
  while n:
   if n&1:r*=a
   a*=a;n//=2
  return r
 def __eq__(self,x):return self.c==P(x).c
 def exact_divide(self,x):
  d=P(x);need(bool(d.c),'nonzero divisor');r=P(self);out=P(0);lead=max(d.c)
  while r.c:
   top=max(r.c);e=(top[0]-lead[0],top[1]-lead[1]);need(min(e)>=0,'entire exact polynomial division')
   t=P({e:r.c[top]/d.c[lead]});out+=t;r-=t*d
  need(out*d==self,'whole quotient multiplied back');return out
 def subs(self,q,k):
  q,k=P(q),P(k);return sum((v*q**a*k**b for (a,b),v in self.c.items()),P(0))
 def at(self,q,k):return sum((v*F(q)**a*F(k)**b for (a,b),v in self.c.items()),F(0))
 def record(self):return [[a,b,str(v)] for (a,b),v in sorted(self.c.items())]

def derive():
 q=P({(1,0):1});k=P({(0,1):1});ell=5*q+4-k;gap=(q*q+7*q+8-2*k)*F(1,2)
 T=2*q*gap;V=2*ell*gap-8*q*(3*q+4);Aq=(2*k+1)*q*q+k*q-2*k;Bq=q*((q-k)*(3*q+4)+3*k)+2*k
 e2=q*q+(13-6*k)*q+2*k*k-10*k+14;C=(1-k)*ell;S2=(3*q+5)*q*(q+1)+6*(q+1)-4*k
 d0=3*(12*q**3+19*q*q+4*q-4);c0=(3*q+2)*(3*q+4)*(3*q*q+3*q-2)
 vp=d0*V+4*c0;cp=d0*C+2*c0;Dn=q*q*T*vp-4*d0*Bq*Bq
 an=2*q*(vp*Aq+2*Bq*cp);bn=2*(q*q*T*cp+2*d0*Bq*Aq)
 dn=S2*Dn-4*(an*q+bn*(2*q-k))
 Rn=q*(d0*e2+4*c0)*Dn-2*d0*an*Aq-2*q*bn*cp;quot=Rn.exact_divide(q*d0)
 # Stationarity identities after ALL rational denominators are cleared.
 need(q*T*an-2*Bq*bn==2*Aq*Dn,'first original adjusted minimizer equation')
 need(-2*d0*Bq*an+q*vp*bn==2*q*cp*Dn,'second original adjusted minimizer equation')
 x=P({(1,0):1});u=P({(0,1):1});shiftD=Dn.subs(6+3*x+u,2+x);shiftS=dn.subs(6+3*x+u,2+x)
 need(len(shiftD.c)==78 and len(shiftS.c)==120 and len(quot.c)==50,'whole shifted/quotient census')
 need(all(v>0 for v in shiftD.c.values()) and all(v>0 for v in shiftS.c.values()),'every complete shifted coefficient positive')
 need(shiftD.c[(0,0)]==265718691840 and shiftS.c[(0,0)]==265060016013312,'whole exact constants')
 # Fresh strictness refinement: the old optimizing b0 is NEVER1 on this quadrant.
 oldD=q*q*T*V-4*Bq*Bq
 oldnonzero=oldD-2*q*q*T*C-4*Bq*Aq
 oldshift=oldD.subs(6+3*x+u,2+x);nzshift=oldnonzero.subs(6+3*x+u,2+x)
 need(all(v>0 for v in oldshift.c.values()) and oldshift.c.get((0,0),0)>0,'whole old homogeneous determinant strictly positive')
 need(all(v>0 for v in nzshift.c.values()) and nzshift.c.get((0,0),0)>0,'whole old residual b0 never1: positive numerator')
 controls=[]
 for kk,qq in [(2,6),(2,7),(3,9),(6,18),(6,19),(6,20),(6,21),(6,22),(6,23),(7,21),(11,34)]:
  c=F(c0.at(qq,kk),d0.at(qq,kk));tt=F(T.at(qq,kk),2);vv=F(V.at(qq,kk),2);aa=F(Aq.at(qq,kk),qq);bb=F(-Bq.at(qq,kk),qq);cc=C.at(qq,kk);ee=F(e2.at(qq,kk),2)
  det=tt*(vv+2*c)-bb*bb;a=((vv+2*c)*aa-bb*(cc+2*c))/det;b=(tt*(cc+2*c)-bb*aa)/det
  residual=ee+2*c-a*aa-b*(cc+2*c);slope=F(S2.at(qq,kk),2*(3*qq+5))-F(2,3*qq+5)*(a*qq+b*(2*qq-kk))
  need(Dn.at(qq,kk)==4*qq*qq*d0.at(qq,kk)*det and an.at(qq,kk)==Dn.at(qq,kk)*a and bn.at(qq,kk)==Dn.at(qq,kk)*b,'full rational denominator controls')
  need(residual==quot.at(qq,kk)/(2*Dn.at(qq,kk)) and dn.at(qq,kk)==2*(3*qq+5)*Dn.at(qq,kk)*slope,'full residual/slope controls')
  olddet=tt*vv-bb*bb;olda=(vv*aa-bb*cc)/olddet;oldb=(tt*cc-bb*aa)/olddet;oldQ=ee-olda*aa-oldb*cc
  need(residual==oldQ+2*c*(1-oldb)**2*olddet/(olddet+2*c*tt),'adjusted rank-one residual calibration')
  need(oldQ+2*c*(1-oldb)**2-residual==4*c*c*tt*(1-oldb)**2/(olddet+2*c*tt),'residual dominance calibration')
  controls.append({'k':kk,'q':qq,'a':str(a),'b':str(b),'Qstar':str(residual),'dstar':str(slope)})
 return {'Dn':Dn.record(),'an':an.record(),'bn':bn.record(),'dn':dn.record(),'P':quot.record(),'shifted_denominator':shiftD.record(),'shifted_slope':shiftS.record(),'shifted_old_determinant':oldshift.record(),'shifted_b0_not1_numerator':nzshift.record(),'proved_strict_domination_entire_quadrant':True,'controls':controls,'all_integer_k_ge2_q_ge3k':True,'ordinary_rank_one_identity_requires_separate_proof':True}
