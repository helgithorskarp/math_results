"""Standard-library audit of root counts and all certified pole loci.

This does not rederive the geometric factorization or resultants; check.py
does that with SymPy. The two implementations have the same author.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse,hashlib,json,math
HERE=Path(__file__).resolve().parent
LO,HI=Q(14,25),Q(593,1000)
def require(ok,message):
 if not ok:raise ValueError(message)
def trim(p):
 p=list(map(Q,p))
 while p and p[-1]==0:p.pop()
 return p
def value(p,x):
 v=Q(0)
 for c in reversed(p):v=v*x+c
 return v
def remainder(a,b):
 a,b=trim(a),trim(b);require(b,'nonzero Sturm divisor')
 while len(a)>=len(b):
  c=a[-1]/b[-1];k=len(a)-len(b)
  for i,z in enumerate(b):a[k+i]-=c*z
  a=trim(a)
 return a
def real_roots(p):
 p=trim(p);require(p,'nonzero fixed-parameter polynomial')
 d=trim([i*p[i] for i in range(1,len(p))]);seq=[p,d]
 if not d:return 0
 while seq[-1]:
  r=trim([-a for a in remainder(seq[-2],seq[-1])])
  if not r:break
  seq.append(r)
 def changes(signs):return sum(a!=b for a,b in zip(signs,signs[1:]))
 minus=[(1 if a[-1]>0 else -1)*((-1)**(len(a)-1)) for a in seq]
 plus=[1 if a[-1]>0 else -1 for a in seq]
 return changes(minus)-changes(plus)
def bernstein(p,left,right):
 p=trim(p);require(p,'nonzero pole factor')
 n=len(p)-1
 a=[sum(p[j]*math.comb(j,k)*left**(j-k)*(right-left)**k for j in range(k,n+1)) for k in range(n+1)]
 return [sum(a[k]*Q(math.comb(i,k),math.comb(n,k)) for k in range(i+1)) for i in range(n+1)]
def no_roots(p,left=LO,right=HI,depth=0):
 c=bernstein(p,left,right)
 if all(a>0 for a in c) or all(a<0 for a in c):return 1
 require(depth<12,'pole-factor sign unresolved within bounded refinement')
 mid=(left+right)/2
 return no_roots(p,left,mid,depth+1)+no_roots(p,mid,right,depth+1)
def verify(data):
 require(data['format']==1 and data['interval']==['14/25','593/1000'] and data['deleted_edge']==[9,13], 'fixed geometric/domain hypotheses')
 counts={};polynomials=set();pieces=0
 for sign,expected in [('-1',[2,2]),('1',[1,1,2])]:
  rows=data['loci'][sign]['factors'];require(len(rows)==len(expected),'complete orientation factor list')
  actual=[]
  for f,count in zip(rows,expected):
   p=[value(c,LO) for c in f['table']]
   require(len(p)==f['degree']+1 and p[-1]!=0,'literal fixed-endpoint factor degree')
   got=real_roots(p)
   require(got==count==f['real_roots_at_lo'],'all real roots counted by direct rational Sturm arithmetic')
   actual.append(got)
   loci=[f['leading_coefficient_locus'],f['discriminant_locus'],*f['gram_resultant_loci']]
   for locus in loci:
    require([a['kind'] for a in locus]==['numerator','denominator'],'both exceptional-locus parts')
    for part in locus:
     require(Q(part['constant'])!=0,'nonzero locus constant')
     for a in part['factors']:
      require(a['multiplicity']>=1 and a['roots_on_I']==0,'nonvanishing locus metadata')
      polynomial=tuple(a['coefficients']);require(value(polynomial,LO)!=0 and value(polynomial,HI)!=0,'closed locus endpoints')
      if polynomial not in polynomials:
       pieces+=no_roots(polynomial);polynomials.add(polynomial)
  counts[sign]=sum(actual)
  for label in ['orientation_denominator_locus','gram_denominator_locus']:
   for part in data['loci'][sign][label]:
    require(Q(part['constant'])!=0,'nonzero global denominator constant')
    for a in part['factors']:
     require(a['roots_on_I']==0 and a['multiplicity']>=1,'global denominator metadata')
     p=tuple(a['coefficients'])
     if p not in polynomials:pieces+=no_roots(p);polynomials.add(p)
 # The surviving factor has exactly two real roots. The negative root is
 # accounted for by its packing-exclusion trace; this fixed positive
 # bracket isolates the other root for every t in the entire I.
 table=data['loci']['-1']['factors'][0]['table']
 leftq,rightq=Q(29,5),Q(39,5)
 def atq(x):return [sum(Q(row[j])*x**i for i,row in enumerate(table)) for j in range(len(table[0]))]
 pa,pb=atq(leftq),atq(rightq)
 for i in range(16):
  left=LO+(HI-LO)*i/16;right=LO+(HI-LO)*(i+1)/16
  a,b=bernstein(pa,left,right),bernstein(pb,left,right)
  sa=1 if all(x>0 for x in a) else -1 if all(x<0 for x in a) else 0
  sb=1 if all(x>0 for x in b) else -1 if all(x<0 for x in b) else 0
  require(sa*sb==-1,'entire positive-root chart interval certified')
 return {'status':'AUDITED','real_roots_by_orientation':counts,
         'distinct_pole_factors':len(polynomials),'closed_sign_pieces':pieces,
         'formal_orientation_models':8,'positive_root_bracket_pieces':16,
         'geometric_factorization_rederived':False}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
 args=p.parse_args();print(json.dumps(verify(json.loads(args.certificate.read_text())),sort_keys=True))
