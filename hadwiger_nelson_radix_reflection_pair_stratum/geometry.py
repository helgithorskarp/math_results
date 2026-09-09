"""Exact Sylvester/Bareiss and quotient-ring Euclidean cover checker."""
from pathlib import Path
import json,math
from fractions import Fraction
from collections import Counter
from flint import fmpz_poly as Z,fmpq_poly as Q,fmpq
import colour as C
V=C.V;X=C.X
def need(x,msg):
 if not x:raise ValueError(msg)
def trim(a):
 a=list(a)
 while a and not a[-1]:a.pop()
 return a
# Polynomial dictionaries in (trace,radius), independent recurrence expansion.
def add(a,b,c=1):
 out=dict(a)
 for m,v in b.items():out[m]=out.get(m,0)+c*v
 return {m:v for m,v in out.items() if v}
def mul(a,b):
 out=Counter()
 for (i,j),v in a.items():
  for (k,l),w in b.items():out[i+k,j+l]+=v*w
 return dict(out)
TR=[{(0,0):2},{(1,0):1}]
for n in range(2,5):TR.append(add(mul({(1,0):1},TR[-1]),mul({(0,1):1},TR[-2]),-1))
def norm(coeff):
 out={(0,0):-1}
 for i,a in enumerate(coeff):
  if a:out=add(out,{(0,i):a*a})
  for j,b in enumerate(coeff[:i]):out=add(out,{(x,y+j):v for (x,y),v in TR[i-j].items()},a*b)
 return out
def shear(poly):
 # trace=u-radius; a list in radius with Z[u] coefficients.
 out=[Z([]) for _ in range(5)]
 for (i,j),c in poly.items():
  for k in range(i+1):out[j+k]+=Z([0]*(i-k)+[c*math.comb(i,k)*(-1)**k])
 return trim(out)
def resultant(f,g):
 m,n=len(f)-1,len(g)-1;size=m+n
 need(size>0,'nonconstant pair')
 rows=[]
 for k in range(n):rows.append([Z([])]*k+list(reversed(f))+[Z([])]*(n-k-1))
 for k in range(m):rows.append([Z([])]*k+list(reversed(g))+[Z([])]*(m-k-1))
 previous=Z([1]);sign=1
 for k in range(size-1):
  pivot=next((i for i in range(k,size) if rows[i][k]),None)
  if pivot is None:return Z([])
  if pivot!=k:rows[pivot],rows[k]=rows[k],rows[pivot];sign=-sign
  a=rows[k][k]
  for i in range(k+1,size):
   for j in range(k+1,size):
    num=rows[i][j]*a-rows[i][k]*rows[k][j]
    value,remainder=divmod(num,previous);need(not remainder,'Bareiss exact division');rows[i][j]=value
   rows[i][k]=Z([])
  previous=a
 return sign*rows[-1][-1]
def primitive(poly):
 vals=[Fraction(str(v)) for v in poly]
 need(vals and vals[-1],'nonzero canonical polynomial')
 den=math.lcm(*(v.denominator for v in vals));ints=[int(v*den) for v in vals];g=math.gcd(*ints)
 if ints[-1]<0:g=-g
 return tuple(v//g for v in ints)
def rats(poly):return tuple(map(str,poly)) if poly else ('0',)
def factor(poly):
 z=Z(list(primitive(poly)));content,terms=z.factor();product=Z([int(content)])
 for q,e in terms:product*=q**e
 need(product==z,'factor product over Z')
 return [(primitive(q),int(e)) for q,e in terms]
def monic_gcd(f,g,mod):
 def inv(a):
  h,b,c=a.xgcd(mod);need(h==1,'leading coefficient invertible modulo parameter block');need((a*b)%mod==1,'inverse identity');return b
 def rem(a,b):
  a=list(a);b=list(b);b_inv=inv(b[-1])
  while len(a)>=len(b):
   c=(a[-1]*b_inv)%mod;off=len(a)-len(b)
   for j,v in enumerate(b):a[off+j]=(a[off+j]-c*v)%mod
   a=trim(a)
  return a
 a=trim([Q(c)%mod for c in f]);b=trim([Q(c)%mod for c in g])
 while b:a,b=b,rem(a,b)
 need(a,'not a whole vertical fibre');inverse=inv(a[-1]);return [(x*inverse)%mod for x in a]

def primitive_bivariate(poly):
    values={k:v for k,v in poly.items() if v};g=math.gcd(*values.values())
    if values[max(values)]<0:g=-g
    return tuple((i,j,v//g) for (i,j),v in sorted(values.items()))

def transform(f,rotation):
    degree=max(i+j for i,j,c in f);out=Counter()
    for i,j,c in f:
        if not rotation:out[i,j]+=c*(-1)**j;continue
        for a in range(i+1):
            for b in range(j+1):
                out[a+b,i+j-a-b]+=c*2**(degree-i-j)*math.comb(i,a)*math.comb(j,b)*(-1)**a*(-3)**(i-a)*(-1)**(j-b)
    return primitive_bivariate(out)

def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))

def inventory(pairs):
    _,factors,circle,monos,rowids=V.reconstruct_inventory();byid={c:r for r,c in rowids.items()}
    power=(1,0);shifts=[]
    for j in range(5):
        points=[V.e_mul(power,d) for d in V.DIGITS]
        candidates=[s for s in points if {(a-s[0],b-s[1]) for a,b in points}==set(V.DIGITS)]
        need(len(candidates)==1,'digit triangle translates under parameter rotation')
        shifts.append(candidates[0]);power=V.e_mul(power,(-1,1))
    need(shifts==[(0,0),(-1,0),(0,-1),(0,0),(-1,0)],'exact physical A5 rotation translation')
    need({V.e_mul((0,1),(a+b,-b)) for a,b in V.DIGITS}==set(V.DIGITS),'conjugation is a physical A5 isometry')
    ident=tuple(range(len(factors)));rot=list(ident);conj=list(ident)
    for row,c in rowids.items():
        power=(1,0);out=[]
        for d in row:out.append(V.e_mul(d,power));power=V.e_mul(power,(-1,1))
        rot[c]=rowids[V.canonical_row(tuple(out))]
        conj[c]=rowids[V.canonical_row(tuple((a+b,-b) for a,b in row))]
    rot=tuple(rot);conj=tuple(conj);lookup={primitive_bivariate({(i,j):v for i,j,v in f}):c for c,f in enumerate(factors)}
    need(rot==tuple(lookup[transform(f,True)] for f in factors),'row and bivariate rotation agree')
    need(conj==tuple(lookup[transform(f,False)] for f in factors),'row and bivariate conjugation agree')
    group=(ident,rot,compose(rot,rot),conj,compose(rot,conj),compose(compose(rot,rot),conj))
    need(len(set(group))==6 and all(compose(g,h) in group for g in group for h in group),'exact closed D3 action')
    need(pairs==sorted(pairs) and len(set(tuple(row[:2]) for row in pairs))==len(pairs),'distinct sorted pair rows')
    normalized=[];polys={};coeff={};images=set()
    for a,b,mask,bound,allowance in pairs:
        need(type(a)is int and type(b)is int and 0<=a<b<len(factors),'valid source pair')
        orbit=[tuple(sorted((g[a],g[b]))) for g in group]
        actual=sum(1<<i for i,im in enumerate(orbit) if im==(a,b))
        need((a,b)==min(orbit) and actual==mask and mask.bit_count()==2 and mask&56,'canonical reflection-stabilizer pair')
        da=max(i+j for i,j,v in factors[a]);db=max(i+j for i,j,v in factors[b])
        need(bound==da*db//2 and allowance==bound//2,'source product-surface allowance')
        choices=[(i,g[a],g[b]) for i,g in enumerate(group[:3]) if conj[g[a]]==g[a] and conj[g[b]]==g[b]]
        need(len(choices)==1,'unique rotation to conjugation-fixed individual curves')
        k,c,d=choices[0];c,d=sorted((c,d));normalized.append([a,b,k,c,d]);images.update(orbit)
        for index in (c,d):
            if index in polys:continue
            E,O=C.project(factors[index]);need(not O,'conjugation-fixed curve is even in y')
            # Reconstruct source equations from the reviewed bivariate norms,
            # independent of the producer's power-trace recurrence.
            polys[index]=shear({(i,j):v for i,j,v in E})
            row=byid[index];aa,bb=next(v for v in row if v!=(0,0))
            rr=[V.e_mul(v,(aa+bb,-bb)) for v in row]
            need(all(b==0 and a in (-1,0,1) for a,b in rr),'real coefficient polynomial after unit scaling')
            coeff[index]=[a for a,b in rr]
    return factors,normalized,polys,coeff,sorted(images)

def keytext(key):return json.dumps(key,separators=(',',':'))

def compile(pairs):
    factors,normalized,polys,coeff,images=inventory(pairs)
    entries=[];components={};hist=Counter();eliminants=[]
    for a,b,rotation,c,d in normalized:
        E=resultant(polys[c],polys[d]);need(E,'nonzero eliminant');keys=[]
        eliminants.append(primitive(E))
        for q,m in factor(E):
            mod=Q(list(q));g=monic_gcd(polys[c],polys[d],mod);hist[len(g)-1]+=1
            if len(g)==1:continue
            if len(g)==2:
                R=-g[0];T=Q([0,1])-R;key=(q,rats(T),rats(R));components[keytext(key)]=key;keys.append(keytext(key))
            else:
                need(len(q)==2,'rational exceptional projection fibre');value=-fmpq(q[0],q[1]);h=Q([v[0] if v else 0 for v in g])
                for qq,mm in factor(h):
                    key=(qq,rats(Q([value,-1])),('0','1'));components[keytext(key)]=key;keys.append(keytext(key))
        entries.append([[a,b],sorted(set(keys))])
    ordered=sorted(components);ids={key:i for i,key in enumerate(ordered)}
    cover=[[pair,[ids[k] for k in keys]] for pair,keys in entries]
    return {'components':[components[k] for k in ordered],'coverage':cover,'normalizations':normalized,
            'curve_inventory_sha256':X.digest(factors),'eliminants_sha256':X.digest(eliminants),
            'real_coefficient_curves':len(polys),'fibre_degree_histogram':{str(k):v for k,v in sorted(hist.items())},
            'physical_pair_exclusions':images}
