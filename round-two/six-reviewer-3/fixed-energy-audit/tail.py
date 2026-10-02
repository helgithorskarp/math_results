"""Post-seal supplement: complete coefficients from two Legendre constructions.

This finite check corroborates indexing. The ALL-degree modulus/convergence proof
is the ordinary Laplace-integral argument in REVIEW.md, never finite sampling.
"""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from math import comb
sys.path.insert(0,str(Path(__file__).resolve().parent))
from polys import symbol,cast,need
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def build():
 x=symbol('x');rows=[]
 def choose(q,k):
  p=F(1)
  for i in range(k):p*=F(q-i,i+1)
  return p
 for n in range(13):
  series=cast(0)
  for k in range((n+1)//2,n+1):series+=choose(F(-1,2),k)*comb(k,n-k)*(-2*x)**(2*k-n)
  integral=cast(0)
  for l in range(n//2+1):integral+=F(comb(n,2*l)*comb(2*l,l)*(-1)**l,4**l)*x**(n-2*l)*(1-x*x)**l
  need(series==integral,'whole Legendre degree '+str(n))
  need(series.substitute({'x':1})==1,'positive endpoint '+str(n))
  need(series.substitute({'x':-1})==(-1)**n,'negative endpoint '+str(n))
  rows.append({'n':n,'coefficients':series.record(),'sha256':hashlib.sha256(canonical(series.record())).hexdigest()})
 need(rows[2]['coefficients']=={'1':['-1/2','0'],'x^2':['3/2','0']},'quadratic normalization')
 return {'degrees_zero_through_twelve':rows,'full_coefficient_equalities':13,'exact_endpoint_checks':26,'infinite_series_proof':'ordinary written proof, not established by these finite checks'}
if __name__=='__main__':
 data=build();expected=json.loads(Path(__file__).with_name('TAIL.json').read_text())
 if canonical(data)!=canonical(expected):raise ValueError('whole tail fixture mismatch')
 print(json.dumps({'passed':True,'full_coefficients':13,'endpoint_checks':26,'canonical_sha256':hashlib.sha256(canonical(data)).hexdigest()},sort_keys=True))
