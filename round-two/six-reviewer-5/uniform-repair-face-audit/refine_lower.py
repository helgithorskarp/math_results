"""New private normalization refinement, independently derived lower fields."""
import json
from pathlib import Path
from sympy import symbols, sympify, Poly, QQ
from fractions import Fraction
import original_field as O
P=Path(__file__).resolve().parent
q,k,x,u=symbols('q k x u')
rec=json.loads((P/'lower-signs.json').read_text())
F=sympify(rec['F'],locals={'q':q});a=sympify(rec['a0'],locals={'q':q,'k':k})
Fn,Fd=F.as_numer_denom();an,ad=a.as_numer_denom()
point=-21**5*F.subs(q,21)
cert={}
def signs(name,expr,subs,variables,strict=True):
    p=Poly(expr.subs(subs,simultaneous=True),*variables,domain=QQ)
    O.require(all(c>=0 for c in p.coeffs()), name+' all coefficients')
    O.require(p.TC()>0 if strict else p.TC()==0,name+' endpoint constant')
    O.require(any(c>0 for c in p.coeffs()),name+' nonzero sign certificate')
    cert[name]={'variables':[str(v) for v in variables],'degree':p.total_degree(),
                'coefficients':[[list(e),str(c)] for e,c in p.terms()]}
signs('a_gt_7q_over5',5*an-7*q*ad,{k:7+x,q:3*(7+x)+u},[x,u])
signs('F_lt_minus25_over49q5',-49*q**5*Fn-25*Fd,{q:21+x},[x])
signs('sharp_F_normalization',-q**5*Fn-point*Fd,{q:21+x},[x],False)
out=dict(point_sharp_constant=str(point),new_bound='a0_prime<-1/q^4',
         sharp_scope='-q^5 F(q)>=c21 for all real q>=21, equality exactly21; infimum attained21',
         a_bound='a0>7q/5 for k>=7,q>=3k; sharp uniform coefficient7/5 via k7,q->infinity',
         certificates=cert)
(P/'lower-refinement.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'independent refined lower certificates pass','sharp_F_constant':str(point),
                  'coefficients':{n:len(c['coefficients']) for n,c in cert.items()},'new_bound':out['new_bound']},indent=2))
