"""Entire exact dual identities over characteristic0 QQ(q,k), no interpolation."""
import json,sys,pathlib
if len(sys.argv)>1:sys.path.insert(0,sys.argv[1])
import sympy
from sympy import QQ,symbols
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from energy import forms,constant_vectors,plane,beta,energy,need
qs,ks=symbols('q k');K=QQ.frac_field(qs,ks);q,k=map(K.convert,(qs,ks));N,m,out=forms(q,k)
y,v,z=constant_vectors();py,pv,pz=plane(out,y),plane(out,v,True),plane(out,z)
alpha=q*(q+1)/2+3*(q+1)/(3*q+5);d=2*q*(q+1)+4*(3*q+1-2*k)/(3*q+5)
A=3*q*q-12*k*q+4*k*k+69*q/2-14*k+K.convert(QQ(121,4))
need(py==[3*q/2+K.convert(QQ(9,4)),0,0,0,2],'complete lower affine identity')
need(pv==[3*q*q+33*q+28-12*k*q+4*k*k-14*k,-d,0,0,-2],'complete cap affine identity')
need(pz==[0,alpha,0,0,0],'complete orientation affine identity')
need([a+b for a,b in zip(py,pv)]==[A,-d,0,0,0],'all five combined coefficients')
# No optimized residue/short-form/target-native engine is imported.
by,bv,bz=(beta(N,m,x) for x in (y,v,z));S=by+bv+d*bz/alpha
need(by and bv and bz and S,'nonzero original lifted norms')
need(by==(6*q+9)/4-(3*q+5)**2/(4*N),'complete actual-empty lower norm')
need(bv==4*N-10-(2*N-4)**2/N,'complete actual-empty cap norm')
need(bz==q*(q+1)/2+1-(q*(q+1)/2-1)**2/N,'complete actual-empty orientation norm')
# Exact individual sums, useful for a human proof of the original metric.
need(sum((a*b for a,b in zip(m,y)),q*0)==(3*q+5)/2,'whole lower member sum')
need(sum((a*b*b for a,b in zip(m,y)),q*0)==(6*q+9)/4,'whole lower member square')
need(sum((a*b for a,b in zip(m,v)),q*0)==2*N-4,'whole cap member sum')
need(sum((a*b*b for a,b in zip(m,v)),q*0)==4*N-10,'whole cap member square')
need(sum((a*b for a,b in zip(m,z)),q*0)==q*(q+1)/2-1,'whole orientation member sum')
need(sum((a*b*b for a,b in zip(m,z)),q*0)==q*(q+1)/2+1,'whole orientation member square')
# Algebraic endpoint polynomials verified by coefficient comparison in QQ[x].
x=symbols('x');AA=A.as_expr()
shifts=[sympy.Poly(AA.subs({qs:ks}).subs(ks,x+17),x).all_coeffs(),sympy.Poly(AA.subs(qs,3*ks-1).subs(ks,x+17),x).all_coeffs(),sympy.Poly(AA.subs(qs,2*ks).subs(ks,x+8),x).all_coeffs()]
need(shifts==[[-5,-sympy.Rational(299,2),-sympy.Rational(4265,4)],[-5,-sympy.Rational(173,2),-sympy.Rational(107,4)],[-8,-73,-sympy.Rational(167,4)]],'all endpoint/q2k polynomial coefficients')
# Full cleared numerator/denominator coefficients, not only scalar numerical checks.
def enc(f):
 f=K.convert(f);return {'numerator':[[list(e),str(c)] for e,c in sorted(f.numer.to_dict().items())],'denominator':[[list(e),str(c)] for e,c in sorted(f.denom.to_dict().items())]}
r={'domain':'QQ(q,k); variable order q,k; characteristic0','sympy':sympy.__version__,'lower_plane':[enc(t) for t in py],'cap_plane':[enc(t) for t in pv],'orientation_plane':[enc(t) for t in pz],'lifted_norms':{'lower':enc(by),'cap':enc(bv),'orientation':enc(bz)},'unrestricted_parameter_separation_denominator':enc(S),'shifts':[[str(c) for c in a] for a in shifts]}
# A new quantitative corollary on the target's initial q=2k frontier.
separation=-A/S;scaled=separation/(N-(3*q+4))
limits=[];onevar=[]
for f,expected_degree,expected_leading in ((separation,1,QQ(8,47)),(scaled,-1,QQ(4,47))):
 g=sympy.cancel(f.as_expr().subs(qs,2*ks));num,den=map(lambda h:sympy.Poly(h,ks,domain=QQ),sympy.fraction(g))
 need(num.degree()-den.degree()==expected_degree and num.LC()/den.LC()==expected_leading,'whole exact margin leading coefficients')
 onevar.append({'numerator':[str(c) for c in num.all_coeffs()],'denominator':[str(c) for c in den.all_coeffs()]})
 limits.append(str(num.LC()/den.LC()))
r['q2k_separation_polynomials']=onevar;r['endpoint_separation_over_k_limit']=limits[0];r['k_M_separation_limit']=limits[1]
print(json.dumps(r,sort_keys=True,separators=(',',':')))
