"""Independent exact QQ(r,l,q) generator, SymPy1.14.0, Python3.11+.
No target imports. All data are independently checked by checker.py.
512 monomials per exported polynomial; separate degree180; each phase60s.
"""
import sys,json,signal,argparse
from pathlib import Path
import sympy as sp
from forms import arrow,model,tests
from linear import need,digest,canonical
r,l,q,u,v,w=sp.symbols('r l q u v w');K=sp.QQ.frac_field(r,l,q);xs=(u,v,w)
def converted(A):return [[K.convert(x) for x in row] for row in A]
def rec(poly,variables):
 P=sp.Poly(poly,*variables,domain=sp.QQ);need(len(P.terms())<=512,'fixed512 exported monomial guard');return [[*k,str(a)] for k,a in sorted(P.terms()) if a]
def shift(expr,boundary):
 # Polynomial-domain composition avoids generic expression expansion.
 # This is independently checked by binomial/multinomial substitution.
 from sympy.polys.rings import ring
 if expr==0:return sp.Poly(0,*xs,domain=sp.QQ)
 T,U,V,W=ring('u,v,w',sp.QQ);inputs=[2+U,T(1),8+4*U+W];P=sp.Poly(expr,r,l,q,domain=sp.QQ);degrees=P.degree_list();powers=[]
 for x,d in zip(inputs,degrees):
  a=[T.one]
  for _ in range(max(0,int(d))):a.append(a[-1]*x)
  powers.append(a)
 result=T.zero
 for k,c in P.terms():result+=sp.QQ.convert(c)*powers[0][k[0]]*powers[1][k[1]]*powers[2][k[2]]
 return sp.Poly(result.as_expr(),*xs,domain=sp.QQ)
def facts(expr,boundary):
 coeff,ff=sp.factor_list(expr,r,l,q);out=[]
 for f,power in ff:
  shifted=shift(f,boundary);constant=shifted.eval({u:0,v:0,w:0})
  if constant<0:f=-f;coeff*=(-1)**power;shifted=shift(f,boundary)
  out.append({'power':int(power),'original':rec(f,(r,l,q)),'shifted':rec(shifted.as_expr(),xs)})
 return {'constant':str(coeff),'factors':out}
def positive_list(data):
 need(any(tuple(x[:3])==(0,0,0) and sp.Rational(x[3])>0 for x in data),'positive constant');need(all(sp.Rational(x[3])>0 for x in data),'complete coefficient positivity')
def fraction_record(a,boundary):
 e=K.to_sympy(a);num,den=sp.fraction(e)
 if shift(den,boundary).eval({u:0,v:0,w:0})<0:num=-num;den=-den
 p=rec(shift(num,boundary).as_expr(),xs);positive_list(p);d=facts(den,boundary);need(sp.Rational(d['constant'])>0,'positive denominator constant')
 for f in d['factors']:positive_list(f['shifted'])
 return {'original_numerator':rec(num,(r,l,q)),'numerator':p,'denominator':d,'coefficient_count':len(p)}
def det(A):
 from itertools import permutations
 z=K.zero;n=len(A)
 for p in permutations(range(n)):
  a=K.convert((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
  for i in range(n):a*=A[i][p[i]]
  z+=a
 return z

def certify(name,A,boundary,orders=None):
 A=converted(A);out=[]
 for k in (orders if orders else range(1,len(A)+1)):
  sub=[row[:k] for row in A[:k]];value=det(sub);f=fraction_record(value,boundary);clearings=[];B=[]
  for row in sub:
   den=sp.Integer(1)
   for x in row:den=sp.lcm(den,sp.fraction(K.to_sympy(x))[1],r,l,q)
   if shift(den,boundary).eval({u:0,v:0,w:0})<0:den=-den
   clearings.append(facts(den,boundary));B.append([])
   for x in row:
    poly=sp.cancel(den*K.to_sympy(x));need(sp.fraction(poly)[1]==1,'exact positive row clearing');B[-1].append({'original':rec(poly,(r,l,q)),'shifted':rec(shift(poly,boundary).as_expr(),xs)})
  den_total=sp.prod(sp.prod(sp.Poly(sum(sp.Rational(a)*r**i*l**j*q**h for i,j,h,a in fact['original']),r,l,q).as_expr()**fact['power'] for fact in data['factors'])*sp.Rational(data['constant']) for data in clearings)
  den0=sp.fraction(K.to_sympy(value))[1]
  if shift(den0,boundary).eval({u:0,v:0,w:0})<0:den0=-den0
  remove=sp.cancel(den_total/den0);need(sp.fraction(remove)[1]==1,'polynomial removal')
  f.update(order=k,positive_row_clearings=clearings,polynomial_matrix=B,removed=facts(remove,boundary));out.append(f)
  print(name,k,len(f['numerator']),file=sys.stderr,flush=True)
 return out

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--case',choices=['signs','anti','triangle','fixed_inverse','final'],required=True);parser.add_argument('--order',type=int);args=parser.parse_args();rr=K.convert(r);ll=K.one;qq=K.convert(q)
 result={'sympy':sp.__version__,'boundary':False,'domain':'r=2+u,l=1,q=8+4u+w;u,w>=0','signs':{},'tests':{}}
 T=tests(rr,ll,qq)
 if args.case=='signs':T={k:T[k] for k in ['mu','alpha','beta','etaP','nuT']}
 else:T={args.case:T[args.case]}
 for name,A in T.items():result['tests'][name]=certify(name,A,False,[args.order] if args.order else None)
 result['whole_sha256']=digest(result);print(json.dumps(canonical(result),sort_keys=True,separators=(',',':')))
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed60s CAS phase')));signal.alarm(60);main()
