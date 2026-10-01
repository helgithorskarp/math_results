"""Standalone arithmetic audit: raw polynomials, Taylor bounds, binary square roots.

Imports no production model/checker or prerequisite arithmetic. Model derivation
is the primary checker's responsibility; this audits its certificate identities
and rational/radical enclosures by another implementation from the same author.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import comb
from pathlib import Path
import argparse,json

HERE=Path(__file__).resolve().parent
LO,HI=Q(14,25),Q(593,1000)
F=(-1,-3,2,6,-1,13)
EDGES=((0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),(2,4),
       (2,8),(2,10),(2,13),(4,8),(5,7),(5,9),(5,11),(6,11),
       (7,12),(8,13),(9,10),(9,11),(9,13),(10,12))
BOUNDS={
 'kappa':('-3/10','-1/5'),'mu':('-3/5','-11/20'),
 'common_w':('1/3','2/5'),'common_height2':('49/100','3/5'),
 'plane_gram':('9/10','1'),'normal_squared_norm':('2','3'),
 'rho':('9/50','23/100'),'detH':('3/10','1/2'),
 'reflection_determinant':('1','2'),'Fprime':('10','14'),
 '-1_-1_1_7_a':('-1/10','-1/50'),'-1_-1_1_7_b':('9/10','6/5'),
 '-1_-1_1_7_square':('-1/4','-1/5'),
 '1_1_10_11_a':('1/10','3/20'),'1_1_10_11_b':('1/2','2/3'),
 '1_-1_6_8_a':('-3/4','-2/5'),'1_-1_6_8_b':('4/3','8/5'),
 'packing_threshold_factor':('1/2','4/5')}

def require(ok,message):
 if not ok:raise ValueError(message)
def trim(p):
 p=list(p)
 while p and p[-1]==0:p.pop()
 return tuple(p)
def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def neg(a):return tuple(-x for x in a)
def mul(a,b):
 if not a or not b:return ()
 out=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return trim(out)
def ra(a,b):return add(mul(a[0],b[1]),mul(b[0],a[1])),mul(a[1],b[1])
def rm(a,b):return mul(a[0],b[0]),mul(a[1],b[1])
def rn(a):return neg(a[0]),a[1]
def equal(a,b):return not add(mul(a[0],b[1]),neg(mul(b[0],a[1])))
def scalar(x):return (x,),(1,)

@lru_cache(maxsize=None)
def polynomial(p,left,right):
 middle=(left+right)/2;radius=(right-left)/2
 shifted=[sum(Q(p[j])*comb(j,k)*middle**(j-k) for j in range(k,len(p))) for k in range(len(p))]
 if not shifted:return Q(0),Q(0)
 low=high=shifted[0]
 for k,a in enumerate(shifted[1:],1):
  v=a*radius**k
  if k%2:low-=abs(v);high+=abs(v)
  else:low+=min(Q(0),v);high+=max(Q(0),v)
 return low,high
def interval(f,left,right):
 a,b=polynomial(f[0],left,right);c,d=polynomial(f[1],left,right)
 require(not c<=0<=d,'Taylor denominator has strict sign')
 q=(a/c,a/d,b/c,b/d)
 return min(q),max(q)
def whole(f,pieces=16):
 spans=[interval(f,LO+(HI-LO)*k/pieces,LO+(HI-LO)*(k+1)/pieces) for k in range(pieces)]
 return min(a for a,b in spans),max(b for a,b in spans)
def floor_sqrt_scaled(q,scale):
 require(0<q<1,'bounded positive radical for binary root rounding')
 low,high=0,scale+1
 while high-low>1:
  middle=(low+high)//2
  if middle*middle*q.denominator<=q.numerator*scale*scale:low=middle
  else:high=middle
 require(low*low*q.denominator<=q.numerator*scale*scale<high*high*q.denominator,
         'binary floor square-root postcondition')
 return low
def sqrt_interval(low,high,scale):
 a=Q(floor_sqrt_scaled(low,scale),scale)
 b=Q(floor_sqrt_scaled(high,scale)+1,scale)
 require(a*a<=low<=high<=b*b,'outward binary-root enclosure')
 return a,b
def audit(c):
 require(c['format']==1 and c['interval']==[[14,25],[593,1000]],'closed fixed domain')
 require(c['edges']==[list(e) for e in EDGES],'all twenty-three literal edges')
 require(c['bernstein_pieces']==8 and c['noncontact_pieces']==16 and c['sqrt_scale']==10**6,
         'fixed coverage and root-rounding configuration')
 require(0<Q(c['noncontact_upper'])<=Q(1,2),'strict all-pair gap')
 lo,hi=map(Q,c['root_bracket'])
 require(LO<lo<hi<HI and sum(Q(a)*lo**i for i,a in enumerate(F))<0
         <sum(Q(a)*hi**i for i,a in enumerate(F)),'root bracket checked independently')
 raw=c['functions'];require(len(raw)==157,'complete fixed rational table')
 f={n:(tuple(x['n']),tuple(x['d'])) for n,x in raw.items()}
 require(all(bool(d) and all(type(x) is int for x in n+d) for n,d in f.values()),'integer rational-polynomial data')
 require(equal(f['Fprime'],((-3,4,18,-4,65),(1,))),'quintic derivative identity')
 require(equal(rm(f['normal_squared_norm'],f['detH']),f['plane_gram']),'metric normal identity')
 one_plus_k=ra(scalar(1),f['kappa'])
 require(equal(rm(rm(f['mu'],f['mu']),rm(one_plus_k,one_plus_k)),
               rm(f['detH'],ra(scalar(1),rm(scalar(2),f['kappa'])))),'equilateral orientation identity')
 for eps in (-1,1):
  for sig in (-1,1):
   for pair in ('1_7','10_11','6_8'):
    tag=f'{eps}_{sig}_{pair}';a,b=f[tag+'_a'],f[tag+'_b']
    require(equal(ra(rm(a,a),rn(rm(f['rho'],rm(b,b)))),f[tag+'_square']),
            'every squared-gap identity '+tag)
 require(equal(f['-1_-1_1_7_a'],f['-1_1_1_7_a']) and equal(f['-1_-1_1_7_b'],f['-1_1_1_7_b']),
         'both wrong W choices have the advertised gap')
 require(equal(f['1_-1_6_8_square'],rm(f['packing_threshold_factor'],(F,(1,)))),
         'exact canceled threshold factor identity')
 for n,(low,high) in BOUNDS.items():
  a,b=whole(f[n]);require(Q(low)<=a<=b<=Q(high),'Taylor sign enclosure '+n)
 names=sorted(n for n in f if n.startswith('noncontact_') and n.endswith('_a'))
 require(len(names)==54,'complete fifty-four noncontact products')
 worst=Q(-10);pair=None
 for n in names:
  for k in range(16):
   left=LO+(HI-LO)*k/16;right=LO+(HI-LO)*(k+1)/16
   a=interval(f[n],left,right);b=interval(f[n[:-1]+'b'],left,right)
   theta=sqrt_interval(*interval(f['rho'],left,right),c['sqrt_scale'])
   upper=a[1]+max(q*z for q in b for z in theta)
   require(upper<Q(c['noncontact_upper']),'Taylor all-pair noncontact bound '+n)
   if upper>worst:worst,pair=upper,n
 return {'status':'AUDITED','raw_polynomial_gap_identities':12,'threshold_identity':True,
         'rational_bounds':len(BOUNDS),'closed_Taylor_pieces':16,'noncontact_pairs':54,
         'worst_noncontact_pair':pair,'worst_noncontact_upper':str(worst),
         'same_author_arithmetic_audit':True}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
 args=parser.parse_args()
 print(json.dumps(audit(json.loads(args.certificate.read_text())),sort_keys=True))
