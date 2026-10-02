"""Exact QQ derivation for a uniform integer gap in the physical Q scalar."""
from pathlib import Path
import sys,json,time
SOURCE=Path(__file__).resolve().parent
import source_pins
if Path(source_pins.__file__).resolve().parent!=SOURCE:raise ValueError('Wrong source-local pin helper')
source_pins.check(optional=True)
public=SOURCE.parent/'three-vector-residual-cap'
sys.path.insert(0,str(public))
import residual,check_coefficients as cc,polynomial_slack as ps,pell_norm as pn
for helper in (residual,cc,ps,pn):
 if Path(helper.__file__).resolve().parent!=public:raise ValueError('Wrong defining parent helper: '+helper.__name__)
from algebra import mul,add,scale
F=residual.F;require=residual.require;sp=ps.sp;q,k=ps.q,ps.k;P=pn.P


def norm57(poly,minimum=25):
 replaced=sp.Poly(poly.as_expr().subs(q,(6*k+P-25)/2),P,k,domain=sp.QQ)
 relation=sp.Poly(P*P-28*k*k-36*k-57,P,k,domain=sp.QQ)
 quotient,remainder=sp.div(replaced.as_expr(),relation.as_expr(),P)
 require(sp.Poly(quotient*relation.as_expr()+remainder-replaced.as_expr(),P,k,domain=sp.QQ).is_zero,'entire norm57 quotient')
 rp=sp.Poly(remainder,P);require(rp.degree()<=1,'linear norm57 remainder')
 x=sp.Symbol('x');ff=sp.Poly(rp.coeff_monomial(1).subs(k,minimum+x),x,domain=sp.QQ);gg=sp.Poly(rp.coeff_monomial(P).subs(k,minimum+x),x,domain=sp.QQ)
 pos=sp.Poly.from_dict({p:c for p,c in gg.terms() if c>0},x,domain=sp.QQ);neg=sp.Poly.from_dict({p:c for p,c in gg.terms() if c<0},x,domain=sp.QQ)
 bound=ff+pos*sp.Poly(5*(minimum+x)+9,x,domain=sp.QQ)+neg*sp.Poly((16*(minimum+x)+9)/3,x,domain=sp.QQ)
 return {'minimum_k':minimum,'norm_constant':57,'quotient_coefficients':ps.coefficient_list(sp.Poly(quotient,P,k,domain=sp.QQ)),'remainder_coefficients':ps.coefficient_list(sp.Poly(remainder,P,k,domain=sp.QQ)),'shifted_f':ps.coefficient_list(ff),'shifted_g':ps.coefficient_list(gg),'coefficient_sandwich':ps.coefficient_list(bound),'negative_count':sum(bool(c<0) for p,c in bound.terms()),'constant':str(bound.coeff_monomial(1)),'passed':bool(bound.coeff_monomial(1)>0 and all(c>=0 for p,c in bound.terms()))}


def run():
 start=time.perf_counter()
 public=SOURCE.parent/'three-vector-residual-cap'
 raw=json.loads((public/'POLYNOMIAL-SLACK.json').read_text());saved=raw.pop('record_sha256');require(residual.digest(raw)==saved=='9accb1e7993765314f92a27597b05a44e6701f03d0fd42aee9aec4be068e2ac6','published complete scalar-form source')
 numerator,denominator=(cc.decode(raw['forms'][name]) for name in ('Q_numerator','Q_denominator'))
 derivative=lambda p:{(i-1,j):c*i for (i,j),c in p.items() if i}
 dn=add(mul(derivative(numerator),denominator),scale(mul(numerator,derivative(denominator)),-1))
 shifted=cc.shift_global(dn,25)
 derivative_certificate={'substitution':'k=25+x,q=5k+u','coefficient_count':len(shifted),'negative_count':sum(c<0 for c in shifted.values()),'constant':str(shifted.get((0,0),F(0))),'coefficients':[[list(p),str(c)] for p,c in sorted(shifted.items())],'passed':bool(shifted.get((0,0),F(0))>0 and all(c>=0 for c in shifted.values()))}
 np=sp.Poly.from_dict({p:sp.Rational(c.numerator,c.denominator) for p,c in numerator.items()},q,k,domain=sp.QQ)
 negative=norm57(-np)
 modular=[]
 for norm,prime,squared,forced in ((65,11,121,(8,0)),(73,5,25,(4,0))):
  pairs=[(kk,pp) for kk in range(prime) for pp in range(prime) if (pp*pp-28*kk*kk-36*kk-norm)%prime==0]
  require(pairs==[forced],'entire prime residue list')
  big=[(kk,pp) for kk in range(squared) for pp in range(squared) if (pp*pp-28*kk*kk-36*kk-norm)%squared==0]
  require(not big,'complete squared-modulus exclusion')
  modular.append({'norm':norm,'prime':prime,'squared_modulus':squared,'entire_prime_solutions':pairs,'entire_squared_solutions':big})
 result={'agent':'six-downset-3','role':'researcher','status':'whole exact derivation; ordinary proof supplied; independent review and formalization pending','derivative':derivative_certificate,'negative_norm57':negative,'modular_exclusions':modular,'all_coefficient_tests_pass':bool(derivative_certificate['passed'] and negative['passed'])}
 result['record_sha256']=residual.digest(result)
 Path(__file__).with_name('INTEGER-GAP.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'derivative_count':derivative_certificate['coefficient_count'],'derivative_negative':derivative_certificate['negative_count'],'derivative_pass':derivative_certificate['passed'],'norm57_count':len(negative['coefficient_sandwich']),'norm57_negative':negative['negative_count'],'norm57_pass':negative['passed'],'modular_norms':[65,73],'seconds':time.perf_counter()-start,'digest':result['record_sha256']}))


if __name__=='__main__':run()
