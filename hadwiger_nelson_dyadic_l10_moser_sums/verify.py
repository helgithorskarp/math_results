"""Solver-free exact physical and complete source-interface certificate replay."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import gcd
from collections import Counter
import base64,hashlib,json,time,argparse
import census
import geometry as g

HERE=Path(__file__).resolve().parent
def need(ok,message):
 if not ok:raise ValueError(message)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

# Separate square-free-radicand arithmetic, with no producer multiplication.
R=(1,2,3,6,5,10,15,30,11,22,33,66,55,110,165,330)
def ref_mul(a,b):
 out=[F(0)]*16
 for i,x in enumerate(a):
  if not x:continue
  for j,y in enumerate(b):
   if not y:continue
   d=gcd(R[i],R[j]);r=R[i]*R[j]//(d*d)
   out[R.index(r)]+=d*x*y
 return tuple(out)
def ref_add(a,b):return tuple(x+y for x,y in zip(a,b))
def ref_cmul(a,b):
 xu=ref_mul(a[:16],b[:16]);yv=ref_mul(a[16:],b[16:])
 return tuple(x-y for x,y in zip(xu,yv))+ref_add(ref_mul(a[:16],b[16:]),ref_mul(a[16:],b[:16]))
def ref_points(phase):
 def p(x={},y={}):
  return tuple(F(x.get(r,0))for r in R)+tuple(F(y.get(r,0))for r in R)
 zero=p();one=p({1:1});omega=p({1:F(1,2)},{3:F(1,2)});eta=p({1:F(5,6)},{11:F(1,6)})
 L=[zero,one,p(y={2:1}),p({1:1},{2:1}),p({2:F(-1,2)},{2:F(1,2)}),p({1:1,2:F(-1,2)},{2:F(1,2)})]
 L +=[p({1:F(1,2),6:F(sx,6)},{2:F(1,2),3:F(sy,6)})for sx,sy in product((-1,1),repeat=2)]
 M=[zero,one,omega,ref_add(one,omega)]+[ref_cmul(eta,a)for a in (one,omega,ref_add(one,omega))]
 P=sorted({ref_add(a,b)for a,b in product(L,M)})
 x,y=phase;v=ref_add(x,ref_cmul(p({5:1}),y))
 ps=[ref_add(a,ref_cmul(v,b))for a,b in product(P,M)]
 return ps

def ref_edges(den,ps):
 # All pairs, first checking the rational coefficient, then all remaining
 # radical coefficients using sqrt(r)sqrt(s)=gcd(r,s)sqrt(rs/gcd(r,s)^2).
 target=den*den;es=[];survivors=0
 for i,a in enumerate(ps):
  for j in range(i+1,len(ps)):
   d=tuple(x-y for x,y in zip(a,ps[j]))
   if sum(r*(d[k]*d[k]+d[k+16]*d[k+16])for k,r in enumerate(R))!=target:continue
   survivors+=1;coeff=[0]*16;coeff[0]=target
   for block in (d[:16],d[16:]):
    nz=[(k,x)for k,x in enumerate(block)if x]
    for ii,(k,x)in enumerate(nz):
     for l,y in nz[ii+1:]:
      common=gcd(R[k],R[l]);rad=R[k]*R[l]//(common*common)
      coeff[R.index(rad)]+=2*x*y*common
   if not any(coeff[1:]):es.append((i,j))
 return es,survivors

def normalize(word):
 seen={};out=[]
 for c in word:
  if c not in seen:seen[c]=len(seen)
  out.append(seen[c])
 return tuple(out)

def patterns(points,triangle):
 den,ps=g.integral(points);es,_=ref_edges(den,ps)
 rest=[i for i in range(len(ps))if i not in triangle];found=set()
 for cs in product(range(4),repeat=len(rest)):
  w=[0]*len(ps)
  for c,i in enumerate(triangle):w[i]=c
  for c,i in zip(cs,rest):w[i]=c
  if all(w[a]!=w[b]for a,b in es):found.add(normalize(w))
 return sorted(found)

def decode(s,n):
 need(isinstance(s,str),'word is not text')
 try:b=base64.b64decode(s,validate=True)
 except Exception as e:raise ValueError('invalid base64')from e
 need(len(b)==(n+3)//4,'wrong colour-word length')
 need(base64.b64encode(b).decode()==s,'noncanonical base64')
 if n%4:need(b[-1]>>(2*(n%4))==0,'nonzero padding')
 return tuple((b[i//4]>>(2*(i%4)))&3 for i in range(n))

def check_certificate(cert,graphs,ids,source_patterns):
 need(set(cert)=={'format','phase_sha256','words'},'certificate fields')
 need(cert['format']=='two-bit-little-endian-v1','certificate format')
 need(isinstance(cert['words'],list)and len(cert['words'])>0,'empty certificate')
 complete=(1<<len(graphs))-1;covered={name:{p:0 for p in pats}for name,pats in source_patterns.items()}
 inequalities=0;seen=set()
 for row in cert['words']:
  need(isinstance(row,list)and len(row)==2,'word row shape')
  mask,s=row;need(type(mask)is int and 0<mask<=complete,'invalid phase mask')
  w=decode(s,448);need(s not in seen,'duplicate word');seen.add(s)
  for j,es in enumerate(graphs):
   if mask>>j&1:
    need(all(w[a]!=w[b]for a,b in es),'improper colour word')
    inequalities+=len(es)
  for name,vertices in ids.items():
   pat=normalize(w[i]for i in vertices)
   need(pat in covered[name],'invalid source pattern')
   covered[name][pat]|=mask
 for name,rows in covered.items():
  need(all(mask==complete for mask in rows.values()),'incomplete source coverage: '+name)
 return {'words':len(seen),'checked_edge_inequalities':inequalities,
         'source_patterns':{k:len(v)for k,v in covered.items()},
         'pattern_phase_pairs':sum(len(v)for v in covered.values())*len(graphs)}

def run(certificate=None):
 phases,summary=census.phases();need(summary=={'rational_P_differences':94,'rational_M_differences':22,'phases':28,'equation_multiplicities':{2:28}},'census mismatch')
 phase_rows=[[[str(z)for z in x],[str(z)for z in y]]for x,y in phases]
 cert=json.loads((certificate or HERE/'certificate.json').read_text());need(cert['phase_sha256']==digest(phase_rows),'phase inventory hash')
 graphs=[];counts=[];idstream=[];point_hashes=[];edge_hashes=[];candidates=0
 for phase in phases:
  den,ps,ids=census.construct(phase)
  need(len(ps)==448 and len(set(ps))==448,'point count/collision')
  reference=ref_points(phase)
  need([[F(a,den)for a in p]for p in ps]==[list(p)for p in reference],'point arithmetic disagreement')
  es=g.exact_edges(den,ps);ref,c=ref_edges(den,ps)
  need(es==ref,'edge arithmetic disagreement');candidates+=c
  graphs.append(es);counts.append([len(ps),len(es)]);idstream.append(ids)
  point_hashes.append(digest([den,ps]));edge_hashes.append(digest(es))
 need(all(ids==idstream[0]for ids in idstream),'address labels changed')
 L,M,P=census.sources();pd,pi=g.integral(P);pe=g.exact_edges(pd,pi)
 need(len(P)==64 and len(pe)==212,'coefficient source')
 pats={'L':patterns(L,(0,7,8)),'first_M':patterns(M,(0,1,2)),'last_M':patterns(M,(0,1,2))}
 need([len(pats[x])for x in pats]==[178,16,16],'source colour pattern count')
 out=check_certificate(cert,graphs,idstream[0],pats)
 out.update(status='VERIFIED_EXACT_CONTACT_CLASS_AND_FULL_SOURCE_PATTERN_EXTENSION',
            phases=len(phases),physical_order=448,edge_histogram={str(k):v for k,v in sorted(Counter(m for n,m in counts).items())},
            cartesian_edges=212*7+64*11,all_unordered_pairs=28*448*447//2,
            rational_coefficient_survivors=candidates,phase_sha256=digest(phase_rows),
            point_inventory_sha256=digest(point_hashes),edge_inventory_sha256=digest(edge_hashes),
            certificate_sha256=hashlib.sha256((certificate or HERE/'certificate.json').read_bytes()).hexdigest())
 return out

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--check-expected',action='store_true');parser.add_argument('--certificate',type=Path);args=parser.parse_args()
 st=time.monotonic();out=run(args.certificate)
 if args.check_expected:need(out==json.loads((HERE/'expected.json').read_text()),'expected output mismatch')
 print(json.dumps(out,sort_keys=True,indent=2))
 print('seconds %.3f'%(time.monotonic()-st),file=__import__('sys').stderr)
