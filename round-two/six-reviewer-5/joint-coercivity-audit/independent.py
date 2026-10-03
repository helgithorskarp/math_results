"""Fresh definition-level SymPy ring audit. No producer/checker imports."""
import hashlib,json,sys,time
from fractions import Fraction
import sympy as sp
from sympy.polys.rings import ring
from sympy.polys.domains import QQ
damage=sys.argv[sys.argv.index('--damage')+1] if '--damage' in sys.argv else None
tt=sp.Symbol('t'); dom=QQ.frac_field(tt)
A,B,E,r,s,F,G,J=ring('B,E,r,s,F,G,J',dom)
t=A.ground_new(dom.gens[0]);Z=A.zero;one=A.one
q=lambda n,d=1:A.ground_new(dom.convert(sp.Rational(n,d)))
def trim(a):
 a=list(a)
 while a and not a[-1]:a.pop()
 return a
def add(a,b):return trim([(a[i] if i<len(a) else Z)+(b[i] if i<len(b) else Z) for i in range(max(len(a),len(b)))])
def scale(a,c):return trim([v*c for v in a])
def mul(a,b):
 out=[Z]*(len(a)+len(b)-1) if a and b else []
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return trim(out)
def der(a):return trim([q(i)*a[i] for i in range(1,len(a))])
def coeff(a,i):return a[i] if i<len(a) else Z
def comp(p,g,v):return p.compose(g,v)
def maps(fv,gv,jv):
 h=[jv,gv,fv,E,B,q(-3,8),Z,one]
 p2=q(8)+t*(q(5,7)*B-q(27,56)*s-r*s)
 p0=q(-5,7)+t*(q(3,7)*B*r+q(75,392)*B+q(4,7)*E*s+q(5,7)*fv+q(3,28)*r*s+q(9,784)*s)
 p1=q(128,5)*B+t*(q(-8,7)*B**2-4*B*r*s+q(4,7)*B*s+q(16,3)*E*r+3*E+q(20,3)*fv*s+8*gv-q(3,8)*r-q(9,64))
 p=[p0,p1,p2,r*t,s*t,t]
 Q=[7*p1+t*(q(3,4)*r-3*B*s+q(9,32)-4*E),q(64)+t*(2*B-q(21,8)*s-7*r*s),t*(7*r+q(3,4)),7*s*t,7*t]
 O=add(add(mul(p,der(der(h))),mul(add(der(p),scale(Q,-one)),der(h))),mul(add([q(64)],scale(der(Q),-one)),h))
 def rho(a):
  a=trim(a)
  while len(a)>7:
   n=len(a)-8;v=a[-1];a=add(a,scale([Z]*n+h,-v))
  return a
 # Newton sums of the seven h roots, through degree five.
 tau=[q(7)]
 for k in range(1,7):
  tau.append(-sum((h[7-j]*tau[k-j] for j in range(1,k)),Z)-k*h[7-k])
 def T(a):
  a=rho(a);out=[]
  for k,v in enumerate(a):
   if k:out=add(out,scale([tau[k-1-i]-(k if i==k-1 else 0) for i in range(k)],v))
  return out
 K=add(scale(p,q(-16)),add(scale(T(T(rho(mul(p,p)))),q(-1,4)),scale(T(rho(mul(p,add(Q,scale(der(p),-one))))),q(1,4))))
 return h,p,Q,O,K
def need(ok,label):
 if not ok:raise ValueError(label)
start=time.monotonic()
h,p,Q,O,K=maps(F,G,J)
if damage=='G-pivot':K[4]+=t*t*G
a=comp(coeff(K,4),G,Z);need(coeff(K,4)==24*t*t*G+a,'full G pivot')
g0=-a/(24*t*t)
k3=comp(coeff(K,3),G,g0);b=comp(k3,F,Z)
need(k3==q(-15,14)*t*t*F+b,'full F pivot')
fs=q(14,15)*b/(t*t);gs=comp(g0,F,fs)
if damage=='F-recovery':fs+=B
o3=comp(comp(coeff(O,3),G,gs),F,fs);c=comp(o3,J,Z)
need(o3==-28*t*J+c,'full J pivot');js=c/(28*t)
h,p,Q,O,K=maps(fs,gs,js)
need(all(not coeff(O,k) for k in (3,4,5)) and all(not coeff(K,k) for k in (3,4,5)),'eliminated complete rows')
R=[t*coeff(O,2),t*coeff(O,1),t*coeff(O,0),coeff(K,1),coeff(K,0)+4]
if damage=='omitted-fourth-row':R[3]=Z
symbols=sp.symbols('B E r s t');bs,es,rr,ss,ts=symbols
def canon(v):
 if not v:return []
 expr=sp.expand(v.as_expr());terms=[]
 for x in sp.Add.make_args(expr):
  coef,rest=x.as_coeff_Mul();pw=rest.as_powers_dict();ex=tuple(int(pw.get(g,0)) for g in symbols)
  need(rest==sp.prod(g**k for g,k in zip(symbols,ex)),'sole Laurent variables')
  terms.append((ex,str(coef)))
 return sorted(terms)
def normdegree(v):
 rows=canon(v);return sum((sp.Rational(c) .__abs__() for e,c in rows),sp.S.Zero),max((sum(map(abs,e)) for e,c in rows),default=0)
bar=[comp(comp(v,B,Z),s,Z) for v in R]
e0=-(10976*r*r+7344*r+1143)/2112
if damage=='E-boundary':e0+=one
aa=[comp(v,E,e0) for v in bar]
need(bar[3]==q(-88,7)*t*(E-e0),'complete E slice pivot')
pc=4934272*r**3+4606896*r*r+1459368*r+157599
need(aa[1]==-t*pc/9504,'slice cubic')
# Extract the coefficient-field t^2 and t^0 terms through exact Laurent data.
def tcoef(v,k):
 out=Z
 for ex,co in canon(v):
  if ex[4]==k:out+=q(int(sp.Rational(co).p),int(sp.Rational(co).q))*B**ex[0]*E**ex[1]*r**ex[2]*s**ex[3]
 return out
a2,b2=tcoef(aa[0],2),tcoef(aa[0],0)
a0,b0=tcoef(aa[2],2),tcoef(aa[2],0)
Sc=(a2*b0-a0*b2)*q(1254528,5)
Psp=sp.Poly(pc.as_expr(),rr,domain=sp.QQ);Ssp=sp.Poly(Sc.as_expr(),rr,domain=sp.QQ)
uu,vv,gg=sp.gcdex(Psp,Ssp);need(gg==1,'fresh rational Euclid unit')
def frompoly(pol):
 return sum((q(int(co.p),int(co.q))*r**mon[0] for mon,co in pol.terms()),Z)
U,V=frompoly(uu),frompoly(vv)
W=[-q(1254528,5)*V*a0,-9504*U/t,q(1254528,5)*V*a2,Z,Z]
need(sum((w*v for w,v in zip(W,aa)),Z)==one,'full specialized unit')
diff=[]
for v,w in zip(bar,aa):
 quotient,remainder=(v-w).div(E-e0);need(not remainder,'entire E difference quotient');diff.append(quotient)
unit=W.copy();unit[3]=q(7,88)/t*sum((w*d for w,d in zip(W,diff)),Z)
if damage=='lift-sign':unit[3]=-unit[3]
if damage=='unit-coefficient':unit[2]+=r**6/t
need(sum((w*v for w,v in zip(unit,bar)),Z)==one,'full lifted row unit')
zd=[normdegree(v) for v in unit];rd=[normdegree(v.diff(g)) for v in R for g in (B,E,s)];fd=normdegree(fs.diff(B))
N_Z=202506888;N_R=16583;CU=Fraction(1,10**13);CP=1814727936;Qn=14913669297722925580854623
need(sum(n for n,d in zd)<=N_Z and max(d for n,d in zd)<=9,'all unit coefficient bounds')
need(sum(n for n,d in zd)==sp.Rational(108740454076928799436912812725247921959,536971633427366372750524416000),'entire exact unit norm')
need([len(canon(v)) for v in unit]==[8,6,7,24,0],'all forty-five fresh unit coefficients')
need([len(canon(v)) for v in R]==[43,54,71,29,44] and all(e[4]>=0 for v in R for e,c in canon(v)),'complete polynomial rows')
need(max(n for n,d in rd)<=N_R and max(d for n,d in rd)<=9,'all fifteen derivative bounds')
need(fd==(sp.Rational(321,140),2),'full F derivative bound')
need(fs.diff(E).compose(B,Z)==q(-83,60)*s,'full projection E pivot')
av=Fraction(1,2*N_Z*N_R);cv=av**2/(3*512*CU*Qn*CP*N_R*(1+Fraction(180,83)/av))
need(cv>=Fraction(1,10**68) and av>=Fraction(1,10**68) and Fraction(83,180)*av>=Fraction(1,10**68),'all universal rational constants')
need(cv<=av and cv<=Fraction(83,180)*av,'proved retained constant refinement')
record=dict(method='fresh SymPy coefficient-field defining ODE/kernel reconstruction and rational gcdex; no producer implementation or fixture input',domain='QQ(t)[B,E,r,s,F,G,J]; all final coefficients verified QQ[B,E,r,s,t,t^-1]',python=sys.version.split()[0],sympy=sp.__version__,full_residuals=[canon(v) for v in R],full_Fstar=canon(fs),full_row_unit=[canon(v) for v in unit],all_five_difference_quotients=[canon(v) for v in diff],unit_norms_degrees=[[str(n),d] for n,d in zd],derivative_norms_degrees=[[str(n),d] for n,d in rd],F_derivative_norm_degree=[str(fd[0]),fd[1]],slice_E0=canon(e0),fresh_Bezout=[canon(U),canon(V)],constants={'a0':str(av),'c0':str(cv),'claimed':str(Fraction(1,10**68))})
print(json.dumps(record,sort_keys=True,separators=(',',':')))
