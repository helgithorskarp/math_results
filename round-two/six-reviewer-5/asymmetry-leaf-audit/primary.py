"""Independent exact audit: infinity residues, divided differences, chain rule, partitions.
No producer imports, executable or fixture. SymPy 1.14.0; characteristic zero.
"""
import hashlib,json,sys
import sympy as s
from fractions import Fraction as Q

def need(ok,msg):
 if not ok:raise ValueError(msg)
def same(x,y,msg):need(s.cancel(x-y)==0,msg)
a,b,c,X=s.symbols('a b c X');r=X**3-s.Rational(3,8)*X**2+a*X/2+b/4
p=X**4-X**3/2+a*X**2+b*X+c
A=32*a-3;d=15-112*a;g=208*a-15
L=256*a**3-18*a**2+432*a*b+864*b**2-27*b
H=512*a**3-36*a**2+736*a*b+1344*b**2-45*b
U=16*a*a-a+6*b
W=4096*a**4-512*a**3+7680*a*a*b+18*a*a-816*a*b+1440*b*b+27*b
J=8192*a**4-1024*a**3+13312*a*a*b+36*a*a-1376*a*b+2496*b*b+45*b
V=8192*a**4+13312*a*a*b-36*a*a+96*a*b+5184*b*b-45*b
F=4*a*a+d*b;G=4*a*a*(64*a-5)+g*b;T=27648*a*a-4960*a+225
# Trace of v over simple roots of monic cubic r is coefficient X^2 of v*r' mod r.
# Thus sum p(root)^2/(root^2*r'(root)^2) is [X^2]p^2/(X^2*r') mod r.
K=s.QQ.frac_field(a,b,c);rp=s.Poly(r,X,domain=K)
inv=s.invert(s.Poly(X*X*s.diff(r,X),X,domain=K),rp)
need((inv*s.Poly(X*X*s.diff(r,X),X,domain=K)).rem(rp)==s.Poly(1,X,domain=K),'entire inverse')
weighted=s.Poly(p*p,X,domain=K).mul(inv).rem(rp)
eta=s.cancel(1024*c*c/(b*b)+32*weighted.nth(2))
eta_formula=768*H*c*c/(b*b*L)-3072*U*c/L-W/(2*L)
D=s.Rational(3,8)-4*a;n=2*b*b*U;cstar=n/H;Cbar=-4*V/(A*H);w=-6144*H/(A*b*b*L)
Na=s.expand(s.diff(V,a)*A*H-V*(32*H+A*s.diff(H,a)))
Nb=s.expand(s.diff(V,b)*H-V*s.diff(H,b))
# Polynomial divided-difference numerator, NOT native sparse kernel or native division.
# Compute F-lift as a difference of evaluation maps, then cancel before any specialization.
bF=-4*a*a/d
DF=s.cancel(d**4*(Na-Na.subs(b,bF))/(d*(b-bF)))
need(s.denom(DF)==1,'DF is undivided polynomial')
g0=4*a*a*(64*a-5);WG=s.expand(-27*G/16+27*g0/8-g*(432*a-27)/512)
HF=s.cancel(H.subs(b,bF));disc=s.discriminant(r,X)
identities={
 'disc':disc+L/512,'eta':eta-eta_formula,
 'WH':W*H+6144*b*b*U*U-L*J,'V':2*H+J-V,
 'completion':(1-eta)/D-Cbar+w*(c-cstar)**2,
 'Nb':Nb-768*F*G,
 'F_lift':d**4*Na+1075200*a**4*A**4*(56*a-5)**2-F*DF,
 'G_lift':g*g*disc+a*a*A*A*T/256-G*WG,
 'F_H':d*d*HF-8*a*a*A*(56*a-5)*(448*a-45),
 'T_square':T-27648*(a-s.Rational(155,1728))**2-s.Rational(275,108),
 'Ca_decomposition':s.diff(Cbar,a)-(67200*HF*HF/(H*H*(448*a-45)**2)-4*F*DF/(d**4*A*A*H*H)),
}
for k,v in identities.items():same(v,0,k)
# Entire chain-rule derivative in independent Laurent jet coordinates.
HH,JJ,mm,mv,q0,q1,q2,q3,lv,Hv,Jv=s.symbols('HH JJ mm mv q0 q1 q2 q3 lv Hv Jv')
first=-8*q0/HH-mm*q2/(8*HH)+mm*JJ*q1/(8*HH**2)
deriv={HH:Hv,JJ:Jv,mm:mv,q0:q1*lv,q1:q2*lv,q2:q3*lv}
jet=s.expand(sum(s.diff(first,z)*dz for z,dz in deriv.items()))
jet_terms=[-8*q1*lv/HH,8*q0*Hv/HH**2,-mv*q2/(8*HH),-mm*q3*lv/(8*HH),mm*q2*Hv/(8*HH**2),mv*JJ*q1/(8*HH**2),mm*Jv*q1/(8*HH**2),mm*JJ*q2*lv/(8*HH**2),-mm*JJ*q1*Hv/(4*HH**3)]
same(jet,sum(jet_terms),'all nine moving-node terms');need(len(s.Add.make_args(jet))==9,'nine monomials')
# Coefficients via the full partition formula sum (-1)^length mu_lambda/z_lambda.
mu={k:s.Symbol('mu'+str(k)) for k in range(3,8)};mu[1]=s.Integer(0);mu[2]=s.Integer(1)
def partitions(k,m=1):
 if k==0:yield ()
 else:
  for j in range(m,k+1):
   for tail in partitions(k-j,j):yield (j,)+tail
moments={}
for k in range(1,8):
 value=s.Integer(0)
 for part in partitions(k):
  denom=1
  for j in set(part):denom*=j**part.count(j)*s.factorial(part.count(j))
  value+=(-1)**len(part)*s.prod(mu[j] for j in part)/denom
 moments[str(8-k)]=s.expand(value)
same(moments['5'],-mu[3]/3,'full f5');same(moments['3'],mu[3]/6-mu[5]/5,'full f3');same(moments['1'],(mu[4]/12-s.Rational(1,24))*mu[3]+mu[5]/10-mu[7]/7,'full f1')
def poly(e,vars):
 return [[list(pows),str(coeff)] for pows,coeff in s.Poly(s.expand(e),*vars,domain=s.QQ).terms()]
def rat(e,vars):
 num,den=s.fraction(s.cancel(e));return {'numerator':poly(num,vars),'denominator':poly(den,vars)}
def norm(e):return sum(abs(co) for co in s.Poly(e,a,b,domain=s.QQ).coeffs())
polys=dict(A=A,d=d,g=g,L=L,H=H,U=U,W=W,J=J,V=V,F=F,G=G,T=T,Na=Na,Nb=Nb,DF=DF,WG=WG,n=n,Ha=s.diff(H,a),Hb=s.diff(H,b),La=s.diff(L,a),Lb=s.diff(L,b),na=s.diff(n,a),nb=s.diff(n,b))
norms={k:str(norm(v)) for k,v in polys.items()}
need(norm(DF)==5615304682700256,'whole DF norm');need(norm(WG)==s.Rational(533493,512),'whole WG norm')
# Portable rational budgets: inequalities are derived from domain powers, not samples.
weights=[Q(40,36),Q(8*1347,36**2),Q(20,8*36),Q(60,8*36),Q(20*1347,8*36**2),Q(1344*5,8*36**2),Q(3368*5,8*36**2),Q(1344*20,8*36**2),Q(2*1344*5*1347,8*36**3)]
need(sum(weights)==Q(18913,288),'entire nine-term budget')
S0=Q(224,27)-Q(4,10**8)*Q(norm(DF))/((Q(9,2)**4)*16*Q(2048,3)**2)
small_H=Q(3469,10**8)/(Q(9,2)*Q(2048,3))
Gfloor=Q(275,12804096);R=Q(3072)*Q(1,10**8)*Gfloor/(3*2673**2)
need(R==Q(1,32487342624000000),'full complement margin')
wa=Q(2344)/Q(2048,3)+8+Q(1236,512);wb=Q(3469)/Q(2048,3)+Q(1,2)+Q(2187,512)
center=Q(104)/Q(2048,3)+Q(46*3469)/Q(2048,3)**2
transfer=2+Q(10240,2048**2)
rho=R/transfer;hessian=4*(7+sum(weights))+64+256;chi=rho/(hessian*2**116)
need(hessian==Q(43969,72),'sharper Hessian')
comparisons={
 'small_H':(small_H,Q(1,2)),'small_error':(Q(4,10**8)*Q(norm(DF))/((Q(9,2)**4)*16*Q(2048,3)**2),Q(1)),
 'small_margin':(Q(1),S0),'R_original':(Q(1,10**17),R),'w_upper':(Q(8019,16),Q(512)),
 'wlog_a':(wa,Q(20)),'wlog_b':(wb,Q(20)),'center':(center,Q(1)),
 'transfer':(transfer,Q(3)),'node_speed':(Q(5,288),Q(1)),
 'mass_first':(Q(203,216),Q(1)),'node_H':(Q(20,8)+1344,Q(1347)),
 'node_J':(Q(60,8)+3360,Q(3368)),'nine_second':(sum(weights),Q(100)),
 'original_Hessian':(Q(748),Q(1000)),
 'root_path':(Q(3125,1024),Q(19683,4096)),
 'original_B':(Q(10**21*2**116),Q(10**56)),
 'distance':(Q(128**2*8),Q(384**2)),
 'rho_improves':(Q(1,10**18),rho),'chi_improves':(Q(3,10**55),chi)
}
for k,(lo,hi) in comparisons.items():need(lo<hi,k)
need(Q(13,24)**2+Q(3,10)**2+Q(1,7)**2==Q(284929,705600),'whole odd-moment weight')
record={'schema':'six-reviewer-5/asymmetry/v1','sympy':s.__version__,'method':'infinity-residue coefficient; divided difference; symbolic full chain rule; integer partitions',
'polynomials':{k:poly(v,(a,b)) for k,v in polys.items()},'norms':norms,
'eta':rat(eta,(a,b,c)),'inverse':rat(inv.as_expr(),(a,b,c,X)),'weighted_remainder':rat(weighted.as_expr(),(a,b,c,X)),
'full_even_derivatives':{k:rat(s.diff((1-eta_formula)/D,z),(a,b,c)) for k,z in [('a',a),('b',b),('c',c)]},
'jet':rat(jet,(HH,JJ,mm,mv,q0,q1,q2,q3,lv,Hv,Jv)),
'moments':{k:poly(v,tuple(mu[j] for j in range(3,8))) for k,v in moments.items()},
'zero_identities':{k:'0' for k in identities},'all_nine_jet':True,
'comparisons':{k:{'lower':str(x),'upper':str(y),'strict':True} for k,(x,y) in comparisons.items()},
'jet_budgets':list(map(str,weights)),
'refinements':{'reduced_margin':str(R),'even_margin':str(rho),'hessian':str(hessian),'joint_margin':str(chi),'moment_weight':str(Q(284929,705600))}}
print(json.dumps(record,sort_keys=True,separators=(',',':')))
