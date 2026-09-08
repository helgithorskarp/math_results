"""Independent exact verifier: half-angle roots and direct radical point-pair norms.
No geometry producer or SAT solver is imported.
"""
import argparse,collections,functools,hashlib,itertools,json,math,pathlib
from fractions import Fraction as F
HERE=pathlib.Path(__file__).resolve().parent

def require(x,msg):
 if not x:raise ValueError(msg)

@functools.lru_cache(None)
def squarepart(n):
 require(type(n) is int and n>=0,'nonnegative radicand')
 if n==0:return 0,0
 f=1;s=1;p=2
 while p*p<=n:
  e=0
  while n%p==0:n//=p;e+=1
  f*=p**(e//2)
  if e%2:s*=p
  p+=1
 if n>1:s*=n
 return f,s

def patch():return [(a,b) for a in range(-2,3) for b in range(-2,3) if -2<=a+b<=2]
def N(v):return v[0]**2+v[0]*v[1]+v[1]**2

def qadd(x,y):return x[0]+y[0],x[1]+y[1]
def qmul(x,y,s):return x[0]*y[0]+s*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def qdiv(x,y,s):
 z=y[0]*y[0]-s*y[1]*y[1];require(z!=0,'nonzero quadratic denominator')
 a,b=qmul(x,(y[0],-y[1]),s);return a/z,b/z

def angle(s,x,y):
 a,b=x;c,d=y
 if s in (0,1):a+=b*(s==1);c+=d*(s==1);b=d=F(0);s=0
 if b==d==0:s=0
 return s,F(a),F(b),F(c),F(d)

def parse_angle(v):
 require(type(v) is list and len(v)==6 and all(type(x)is int for x in v),'angle format')
 s,a,b,c,d,L=v;require(L>0 and math.gcd(*map(abs,v[1:]))==1,'primitive angle denominator')
 require(s==0 or (s>1 and squarepart(s)==(1,s)),'squarefree angle field')
 require(s!=0 or b==d==0,'canonical rational angle')
 require(a*a+s*b*b+3*c*c+3*s*d*d==L*L and 2*a*b+6*c*d==0,'unit rotation')
 k=angle(s,(F(a,L),F(b,L)),(F(c,L),F(d,L)))
 require(k[0]==s,'nonminimal field');return k

def orbit(k):
 ans=set()
 for _ in range(6):
  s,a,b,c,d=k;ans.add(k);ans.add((s,a,b,-c,-d))
  k=angle(s,((a-3*c)/2,(b-3*d)/2),((a+c)/2,(b+d)/2))
 return ans

def independent_roots(ds):
 """u=(1-3t^2+2 i sqrt(3)t)/(1+3t^2), t real or infinity."""
 roots=set();polynomials=0;real_roots=0
 for (a,b),(c,d) in itertools.product(ds,repeat=2):
  if (a,b)==(0,0) or (c,d)==(0,0):continue
  p=2*a*c+a*d+b*c+2*b*d;q=b*c-a*d;z=1-N((a,b))-N((c,d))
  A=3*(p+z);B=-6*q;C=z-p;polynomials+=1
  if z==-p:roots.add(angle(0,(-1,0),(0,0)))
  if A==0:
   if B==0:require(C!=0,'nonzero event polynomial');continue
   ts=[(0,(F(-C,B),F(0)))]
  else:
   disc=B*B-4*A*C
   if disc<0:continue
   f,s=squarepart(disc)
   ts=[(s,(F(-B,2*A),F(sign*f,2*A))) for sign in (-1,1)]
  for s,t in ts:
   tt=qmul(t,t,s);den=qadd((F(1),F(0)),(3*tt[0],3*tt[1]))
   x=qdiv((1-3*tt[0],-3*tt[1]),den,s);y=qdiv((2*t[0],2*t[1]),den,s)
   roots.add(angle(s,x,y));real_roots+=1
 return roots,{'difference_polynomials':polynomials,'finite_half_angle_roots_with_multiplicity':real_roots}

def radical(terms):
 out=collections.defaultdict(int)
 for coeff,n in terms:
  if not coeff or not n:continue
  f,s=squarepart(n);out[s]+=coeff*f
 return tuple(sorted((s,c) for s,c in out.items() if c))
def subtract(a,b):return radical([(c,s) for s,c in a]+[(-c,s) for s,c in b])
def square_sum(a,b):
 out=collections.defaultdict(int)
 for v in (a,b):
  for s,x in v:
   for t,y in v:
    f,r=squarepart(s*t);out[r]+=x*y*f
 return tuple(sorted((s,c) for s,c in out.items() if c))

def coordinates(h,v):
 s,A,B,C,D,L=v;out=[]
 for a,b in h:
  for c,d in h:
   p,q,r,t=2*a+b,b,2*c+d,d
   out.append((radical([(p*L+r*A-3*t*C,1),(r*B-3*t*D,s)]),
               radical([(q*L+t*A+r*C,3),(t*B+r*D,3*s)])))
 return out

def triangle_rigidity(h):
 edges={tuple(sorted((i,j))) for i,x in enumerate(h) for j,y in enumerate(h[:i]) if N((x[0]-y[0],x[1]-y[1]))==1}
 adj=[set() for _ in h]
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 triangles=sorted((a,b,c) for a in range(len(h)) for b in adj[a] if b>a for c in adj[a]&adj[b] if c>b)
 reached=set(triangles[0]);old=-1
 while len(reached)!=old:
  old=len(reached)
  for tri in triangles:
   if len(reached&set(tri))>=2:reached.update(tri)
 require(len(reached)==19,'triangle propagation covers the patch')
 q=[(a-b)%3 for a,b in h];require(all(q[a]!=q[b] for a,b in edges),'base residue colouring')
 return {'vertices':len(h),'edges':len(edges),'triangles':len(triangles),'triangle_propagation_vertices':len(reached)}

def validate(certificate):
 require(certificate.get('family')=='H2+uH2; |u|=1; all strict unit edges','fixed family')
 rows=certificate['cases'];require(type(rows)is list and len(rows)==15,'complete case count')
 h=patch();require(len(h)==19,'patch order');ds=sorted({(a-c,b-d) for a,b in h for c,d in h});require(len(ds)==61,'difference census')
 roots,rootstats=independent_roots(ds);expanded=set();orbit_sizes=[]
 for row in rows:
  k=parse_angle(row['angle']);o=orbit(k);require(not(expanded&o),'disjoint rotation orbits');expanded|=o;orbit_sizes.append(len(o))
 require(roots==expanded,'complete independent half-angle root census')
 base=triangle_rigidity(h);summaries=[];pairs=0
 for row in rows:
  v=row['angle'];L=v[-1];ps=coordinates(h,v);colour=row['colours']
  require(type(colour)is str and len(colour)==361 and set(colour)<=set('0123'),'361 valid colour symbols')
  chi=row['chi'];require(type(chi)is int and chi in (3,4),'chromatic value');require(all(int(c)<chi for c in colour),'palette bound')
  labels={};ids=[]
  for p in ps:
   if p not in labels:labels[p]=len(labels)
   ids.append(labels[p])
  patterns={e:[(a-b+e*(c-d))%3 for a,b in h for c,d in h] for e in (-1,1)}
  bad={};es=set();collisions=0;unit_label_pairs=0
  for i in range(361):
   for j in range(i):
    pairs+=1
    if ps[i]==ps[j]:
     collisions+=1;require(colour[i]==colour[j],'colour descends at coincidence')
     for e,w in patterns.items():
      if w[i]!=w[j]:bad.setdefault(e,['collision',j,i])
     continue
    dd=square_sum(subtract(ps[i][0],ps[j][0]),subtract(ps[i][1],ps[j][1]))
    if dd==((1,4*L*L),):
     unit_label_pairs+=1;require(colour[i]!=colour[j],'proper unit-edge colouring');es.add(tuple(sorted((ids[i],ids[j]))))
     for e,w in patterns.items():
      if w[i]==w[j]:bad.setdefault(e,['unit_edge',j,i])
  require(len(labels)==row['vertices'] and len(es)==row['edges'],'physical graph counts')
  good=sorted(set(patterns)-set(bad));require((chi==3)==bool(good),'exact three/four classification')
  summaries.append({'angle':v,'vertices':len(labels),'edges':len(es),'chi':chi,'three_colour_signs':good,'rejected_sign_witnesses':bad,'coincident_label_pairs':collisions,'unit_label_pairs':unit_label_pairs})
 return {'status':'ALL_ROTATIONAL_HEXAGON_SUMS_CLASSIFIED_THREE_OR_FOUR',
  'record_improvement':False,'base':base,'difference_vectors':len(ds),'exceptional_rotations':len(roots),'rotation_orbits':len(rows),'orbit_size_histogram':dict(collections.Counter(orbit_sizes)),
  'chromatic_orbit_histogram':dict(collections.Counter(r['chi'] for r in rows)),
  'all_label_pairs_checked':pairs,'generic_vertices':361,'generic_edges':1596,'generic_chromatic_number':3,'half_angle_census':rootstats,'cases':summaries}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=pathlib.Path,default=HERE/'certificate.json');ap.add_argument('--check-expected',action='store_true');args=ap.parse_args()
 out=validate(json.loads(args.certificate.read_text()))
 if args.check_expected:require(json.loads(json.dumps(out,sort_keys=True))==json.loads((HERE/'EXPECTED.json').read_text()),'expected receipt')
 print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
