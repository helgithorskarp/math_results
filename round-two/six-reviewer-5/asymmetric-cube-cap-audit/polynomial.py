"""Standard-library whole-coefficient checks of fresh pivots; no CAS import."""
from fractions import Fraction as R
from functools import lru_cache
from math import comb
import hashlib,json,pathlib,time
P=pathlib.Path(__file__).resolve().parent
def need(t,why):
 if not t:raise ValueError(why)
def read(v):
 need(isinstance(v,list),'polynomial list');out={}
 for mon,c in v:
  need(len(mon)==2 and all(type(i) is int and i>=0 for i in mon),'monomial')
  need(tuple(mon) not in out,'duplicate monomial');out[tuple(mon)]=R(c)
  need(out[tuple(mon)]!=0,'zero polynomial term')
 return out
def add(a,b):
 out=a.copy()
 for m,c in b.items():out[m]=out.get(m,R(0))+c
 return {m:c for m,c in out.items() if c}
def neg(a):return {m:-c for m,c in a.items()}
def mul(a,b):
 out={}
 for (i,j),x in a.items():
  for (ii,jj),y in b.items():out[i+ii,j+jj]=out.get((i+ii,j+jj),R(0))+x*y
 return {m:c for m,c in out.items() if c}
def shift(a):
 out={}
 for (i,j),c in a.items():
  for ii in range(i+1):
   for jj in range(j+1):out[ii,jj]=out.get((ii,jj),R(0))+c*comb(i,ii)*3**(i-ii)*comb(j,jj)*4**(j-jj)
 return {m:c for m,c in out.items() if c}
def sign(v):
 for k in ('numerator','denominator'):
  a=read(v[k]);b=shift(a);need(b==read(v['shifted_'+k]),'whole shifted coefficient reconstruction');need(b.get((0,0),0)>0 and all(c>0 for c in b.values()),'whole positive shift')
def determinant(a,n):
 @lru_cache(None)
 def sub(row,cols):
  if not cols:return {(0,0):R(1)}
  out={}
  for j,col in enumerate(cols):
   term=mul(a[row][col],sub(row+1,cols[:j]+cols[j+1:]));out=add(out,neg(term) if j%2 else term)
  return out
 return sub(0,tuple(range(n)))
def check(r):
 need(set(r['scalars'])=={'tau'}|{f'{g}-{k}' for g in (0,1) for k in ('mu','alpha','beta','nu')},'entire scalar set')
 sizes={'0-odd':2,'1-odd':2,'0-standard':4,'1-standard':4,'0-trace':2,'1-trace':2,'aggregate-five':5,'mean':1,'old-sum':1,'old-difference':1}
 need(set(r['blocks'])==set(sizes) and r['pivot_count']==33,'whole block/pivot coverage')
 for v in r['scalars'].values():sign(v)
 sign(r['inverse_bound']);coefficients=0;identities=0
 for key,dim in sizes.items():
  b=r['blocks'][key];need(len(b['pivots'])==dim and len(b['entries'])==dim and len(b['cleared'])==dim and len(b['row_denominators'])==dim,'whole block dimensions')
  Ds=[read(v) for v in b['row_denominators']];a=[[read(v) for v in row] for row in b['cleared']]
  for i in range(dim):
   need(len(a[i])==dim and len(b['entries'][i])==dim,'whole rows')
   for j in range(dim):
    e=b['entries'][i][j];need(mul(a[i][j],read(e['denominator']))==mul(Ds[i],read(e['numerator'])),'complete original row clearing');identities+=1
  prev={(0,0):R(1)}
  for i,piv in enumerate(b['pivots']):
   sign(piv);det=determinant(a,i+1)
   need(mul(det,read(piv['denominator']))==mul(mul(prev,read(piv['numerator'])),Ds[i]),'whole leading-minor pivot identity');identities+=1;prev=det
  coefficients+=sum(len(read(v[k])) for v in b['pivots'] for k in ('shifted_numerator','shifted_denominator'))
 return dict(whole_polynomial_identities=identities,positive_obligations=34,leading_cap_pivots=24,block_count=10,shifted_cap_coefficients=coefficients)
if __name__=='__main__':
 t=time.monotonic();r=json.loads((P/'work/fresh-field-record.json').read_text());v=check(r);(P/'work/polynomial-record.json').write_text(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps(dict(**v,seconds=time.monotonic()-t)))
