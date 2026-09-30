"""Optional exact parameter discovery, independently checked without CAS.

SymPy1.14.0 over Q(v,l), characteristic zero. Solve the affine row/star
system, then set the constant triple block to one. UNIFORM_LAMBDA_PROOF.md
supplies the incidence, positive signs, PSD, repair and cap interpretations.
This algebra alone is not an H proof. Redirect stdout to lambda_symbolic.json.
Author: six-downset-2, researcher.
"""
import json
import sympy as S

assert S.__version__=='1.14.0'
v,l=S.symbols('v l')
a,w,c,h,d,t=S.symbols('a w c h d t')
m,b,r,u=v*(v-1)/2,l*v*(v-1)/6,l*(v-1)/2,l*(l-1)/2
s,N=v+r,1+v+m+b
equations=[h+(v-4)*d+(r-3*l)*t-s,
           1+s+(v-3)*h-3*(l-1)*t+(v-3)*(v-4)*d/2+(b-3*r+3*l-1)*t-N,
           w+(v-3)*c+(r-2*l)*d-s,
           1+s+(v-2)*w-l*d+(v-2)*(v-3)*c/2+(b-2*r+l)*d-N,
           a+(v-2)*w-l*d+(r-l)*h-3*u*t-s]
affine=S.solve(equations,[a,w,c,h,d],dict=True)
assert len(affine)==1
constant_triple=s+(3*l-1)*t-3*r*t+(t-1)*b
selected=S.solve(constant_triple-1,t)
assert len(selected)==1
selected=S.factor(selected[0])
solution={key:S.factor(value.subs(t,selected)) for key,value in affine[0].items()}
solution[t]=selected
equations.append(1+s+(v-1)*a+(v-1)*(v-2)*w/2-r*d+(b-r)*h-(l-1)*r*t-N)
assert all(S.cancel(eq.subs(solution))==0 for eq in equations)
cc,dd,tt=solution[c],solution[d],solution[t]
assert S.cancel(s+cc-2*cc*(v-1)+(cc-1)*m-4*l/3)==0
assert S.cancel(l*dd-2*dd*r+(dd-1)*b+2*l/3)==0
alpha1,alpha2=S.factor(s-cc*(v-3)),S.factor(s+cc)
mu=S.factor(s-tt-(r-l)*(tt*(v-6)/(v-2)+dd**2*(v-4)**2/((v-2)*alpha1)))
margin=S.factor(mu-1/l)
num,den=S.fraction(margin)
x,y=S.symbols('x y')
shifted=S.Poly(S.expand(num.subs({v:13+x,l:2+y})),x,y)
assert all(co>0 for co in shifted.coeffs()) and shifted.coeff_monomial(1)>0
out={'agent':'six-downset-2','role':'researcher','CAS':'SymPy '+S.__version__,
     'domain':'Q(v,l), characteristic zero','weights':{str(k):str(z) for k,z in solution.items()},
     'normalized_constant_K':[['4l/3','-2sqrt(l/3)'],['-2sqrt(l/3)','1']],
     'pair_eigenvalues':{'point_standard':str(alpha1),'point_kernel':str(alpha2)},
     'Schur_lower_bound':str(mu),'Schur_margin_above_1_over_l':str(margin),
     'margin_denominator':str(S.factor(den)),
     'shifted_margin_coefficients':[[i,j,str(co)] for (i,j),co in sorted(shifted.terms())],
     'exceptional_denominators':'l,v-2,v-3,v-4,D0,E0,alpha2; positive in the proved domain',
     'status':'Exact discovery algebra only; full quantified proof and portable checker supplied separately'}
print(json.dumps(out,indent=2,sort_keys=True))
