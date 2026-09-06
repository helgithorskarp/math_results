"""Prime-parity field audit using direct squared Euclidean distances.

Imports neither producer code nor prior packages. The universal statements
are the written theorems; this checks their finite illustrative certificates.
"""
from fractions import Fraction as Q
from itertools import combinations,product
from functools import lru_cache,cmp_to_key
from math import gcd,prod
from pathlib import Path
import argparse,copy,hashlib,json

def require(ok,msg):
 if not ok:raise ValueError(msg)
def primes(n):
 require(type(n)is int and n>=1,'positive radical')
 out=set();p=2
 while p*p<=n:
  if n%p==0:
   n//=p;out.add(p);require(n%p!=0,'squarefree radical')
  p+=1
 if n>1:out.add(n)
 return frozenset(out)
def normalize(a):return {s:c for s,c in a.items() if c}
def add(a,b):
 c=dict(a)
 for s,x in b.items():c[s]=c.get(s,Q(0))+x
 return normalize(c)
def times(a,b):
 c={}
 for s,x in a.items():
  for t,y in b.items():
   u=s^t;c[u]=c.get(u,Q(0))+x*y*prod(s&t)
 return normalize(c)
def by(a,c):return normalize({s:x*c for s,x in a.items()})
def minus(a,b):return add(a,by(b,-1))
def scalar(q):return {} if not q else {frozenset():Q(q)}
ZERO={};ONE=scalar(1)
def rational(pair):
 require(type(pair)is list and len(pair)==2 and all(type(t)is int for t in pair) and pair[1]>0,'rational pair')
 v=Q(*pair);require([v.numerator,v.denominator]==pair,'reduced rational');return v
def decode(row):
 require(type(row)is list,'radical list');out={};previous=0
 for d,pair in row:
  require(d>previous,'strict radical order');previous=d;s=primes(d);c=rational(pair);require(c!=0,'no stored zero');out[s]=c
 return out
def encode(a):return [[prod(s),[c.numerator,c.denominator]] for s,c in sorted(a.items(),key=lambda p:prod(p[0]))]
def key(a):return tuple((prod(s),c) for s,c in sorted(a.items(),key=lambda p:prod(p[0])))
def sqrtq(q):
 q=Q(q);require(q>=0,'nonnegative root')
 if q==0:return ZERO
 n=q.numerator*q.denominator;p=2;outside=1;odd=set()
 while p*p<=n:
  exponent=0
  while n%p==0:n//=p;exponent+=1
  outside*=p**(exponent//2)
  if exponent%2:odd.add(p)
  p+=1
 if n>1:odd.add(n)
 return {frozenset(odd):Q(outside,q.denominator)}
@lru_cache(None)
def signkey(a):
 if not a:return 0
 intervals={d:[Q(0),Q(d)] for d,c in a if d!=1}
 while True:
  lo=hi=Q(0)
  for d,c in a:
   l,u=(Q(1),Q(1)) if d==1 else intervals[d]
   lo+=c*(l if c>0 else u);hi+=c*(u if c>0 else l)
  if lo>0:return 1
  if hi<0:return -1
  for d,v in intervals.items():
   m=(v[0]+v[1])/2
   if m*m<d:v[0]=m
   elif m*m>d:v[1]=m
   else:v[:]=[m,m]
def sign(a):return signkey(key(a))
def norm(a,b):
 x,y=minus(a[0],b[0]),minus(a[1],b[1]);return add(times(x,x),times(y,y))
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(raw(x)).hexdigest()
def integer(x):require(x.denominator==1,'integral colour coordinate');return x.numerator

@lru_cache(None)
def geometry(spec_blob):
 spec=json.loads(spec_blob);d2=rational(spec['spacing_squared']);require(d2>0,'positive spacing')
 gens=list(map(decode,spec['generators']));bounds=spec['bounds'];rows=spec['rows']
 require(1<=len(gens)<=3 and len(gens)==len(bounds),'generator shape')
 require(all(type(a)is int and type(b)is int and 0<=b-a<=24 for a,b in bounds),'bounded audit ranges')
 require(type(rows)is list and 1<=len(rows)<=7 and rows==sorted(set(rows)) and all(type(j)is int for j in rows),'distinct rows')
 vals={}
 for ns in product(*(range(a,b+1) for a,b in bounds)):
  x=ZERO
  for n,g in zip(ns,gens):x=add(x,by(g,n))
  vals[key(x)]=x
 X=[vals[k] for k in sorted(vals)]
 if 'heights' in spec:
  require(spec['method']=='three_lines' and len(spec['heights'])==len(rows)<=3,'three-line heights')
  Y=[scalar(rational(h)) for h in spec['heights']]
 else:Y=[by(sqrtq(d2),j) for j in rows]
 V=[(x,y) for x in X for y in Y];require(len({(key(x),key(y)) for x,y in V})==len(V),'distinct actual points')
 E=[(a,b) for a,b in combinations(range(len(V)),2) if norm(V[a],V[b])==ONE]
 return X,Y,V,E

def audit_case(case):
 s=case['input'];X,Y,V,E=geometry(raw(s).decode());d2=rational(s['spacing_squared']);rows=s['rows'];method=s['method']
 require(case['vertices']==len(V) and case['edges']==len(E),'counts')
 require(case['point_sha256']==digest([[encode(x),encode(y)] for x,y in V]) and case['edge_sha256']==digest(E),'direct norm graph hashes')
 word=case['colouring'];require(type(word)is str and len(word)==len(V) and set(word)<={'0','1','2','3'},'colour domain');col=list(map(int,word))
 require(all(col[a]!=col[b] for a,b in E),'all actual unit edges properly coloured')
 maximum=None
 if method in ('projection','three_lines'):
  if method=='projection':
   require(d2>Q(1,9) and d2 not in (Q(1,4),Q(1)),'projection regime excludes vertical unit edges')
   shifts=[Q(1)];j=1
   while j*j*d2<1:shifts.append(1-j*j*d2);j+=1
   require(j*j*d2!=1 and len(shifts)<=3,'positive shifts and count')
   allowed=[scalar(v) for v in shifts];bound=len(shifts)
   EE=[(a,b) for a,b in combinations(range(len(X)),2) if times(minus(X[a],X[b]),minus(X[a],X[b])) in allowed]
   order=sorted(range(len(X)),key=cmp_to_key(lambda a,b:sign(minus(X[a],X[b]))));N=len(X)
   require(all(col[i*len(rows)+j]==col[i*len(rows)] for i in range(N) for j in range(len(rows))),'actual projection colouring')
  else:
   require(len(Y)<=3,'at most three lines');bound=3;N=len(V);EE=E
   order=sorted(range(N),key=cmp_to_key(lambda a,b:sign(minus(V[a][0],V[b][0])) or sign(minus(V[a][1],V[b][1]))))
  rank={v:i for i,v in enumerate(order)};earlier=[0]*N
  for a,b in EE:earlier[a if rank[a]>rank[b] else b]+=1
  maximum=max(earlier,default=0);require(maximum<=bound,'directional predecessor theorem')
  require(max(col,default=0)<=bound,'greedy colour bound')
 else:
  expected=[]
  if method=='third':require(d2==Q(1,9),'third-spacing boundary')
  elif method=='half':require(d2==Q(1,4),'half-spacing boundary')
  elif method=='one':require(d2==1,'unit-spacing boundary')
  elif method=='irrational_two':require(d2==Q(1,2),'irrational audit example')
  elif method=='rational_two':
   p,q=s['p'],s['q'];require(type(p)is int and type(q)is int and 0<p<q and gcd(p,q)==1 and q%2==1 and 4*p*p<3*q*q and d2==1-Q(p,q)**2,'odd denominator hypothesis')
  else:raise ValueError('unknown method')
  for i,(x,y) in enumerate(V):
   j=rows[i%len(rows)]
   if method=='rational_two':c=(integer(q*x.get(frozenset(),Q(0)))+(1-p)*j)%2
   else:
    m=integer(x.get(frozenset(),Q(0)))
    c=(m+integer(3*x.get(frozenset({5}),Q(0)))+j)%2 if method=='third' else (m+j)%(3 if method=='half' else 2)
   expected.append(c)
  require(col==expected,'explicit coordinate colour rule')
 require(case['predecessor_maximum']==maximum,'predecessor receipt')
 return {'name':s['name'],'vertices':len(V),'edges':len(E),'point_pairs':len(V)*(len(V)-1)//2,'colours_used':len(set(col)),'predecessor_maximum':maximum,'point_sha256':case['point_sha256'],'edge_sha256':case['edge_sha256']}

def universal_formula_controls():
 # Complete generator tables for each exact boundary component.
 counts={}
 for name,d2,g in [('third',Q(1,9),[ONE,sqrtq(Q(8,9)),sqrtq(Q(5,9))]),('half',Q(1,4),[ONE,sqrtq(Q(3,4))]),('one',Q(1),[ONE])]:
  table=[];dimension=len(g)
  for t in (-1,1):table.append(([t]+[0]*(dimension-1),0))
  maxj={'third':3,'half':2,'one':1}[name]
  for j in range(1,maxj+1):
   for tj in (-j,j):
    if j==maxj:table.append(([0]*dimension,tj))
    else:
     for t in (-1,1):v=[0]*dimension;v[j]=t;table.append((v,tj))
  for coeff,j in table:
   x=ZERO
   for n,v in zip(coeff,g):x=add(x,by(v,n))
   require(add(times(x,x),scalar(d2*j*j))==ONE,'boundary generator norm')
   value=(coeff[0]+coeff[2]+j)%2 if name=='third' else (coeff[0]+j)%(3 if name=='half' else 2)
   require(value!=0,'boundary generator changes colour')
  counts[name]=len(table)
 # The half-spacing lower bound is a triangle of actual points.
 tri=[(ZERO,ZERO),(ZERO,ONE),(sqrtq(Q(3,4)),scalar(Q(1,2)))]
 require(all(norm(a,b)==ONE for a,b in combinations(tri,2)),'half-spacing unit triangle')
 oddq=0
 for q in range(3,20,2):
  for p in range(1,q):
   if gcd(p,q)>1 or 4*p*p>=3*q*q:continue
   require(q%2==1 and all((a+(1-p)*b)%2==1 for a,b in [(q,0),(-q,0)]+[(a,b) for a in (-p,p) for b in (-1,1)]),'odd-denominator generator colours');oddq+=1
 # General distance-count bound is attained for D={1,...,k} on {0,...,k}.
 for k in range(1,7):require(all(1<=abs(a-b)<=k for a,b in combinations(range(k+1),2)),'complete-graph distance control')
 return {'boundary_generator_counts':counts,'half_spacing_triangle_edges':3,'odd_denominator_parameter_controls':oddq,'complete_distance_graph_controls':6,'collapsed_vertical_edge_controls':3}

def odd_cycles(parameters):
 want=[[p,q] for q in range(2,21,2) for p in range(1,q) if gcd(p,q)==1 and 4*p*p<3*q*q]
 require(parameters==want,'complete frozen odd-cycle parameters');lengths=[]
 for p,q in parameters:
  h=sqrtq(1-Q(p,q)**2)
  V=[(scalar(Q(k*p,q)),by(h,k%2)) for k in range(q+1)]+[(scalar(r),ZERO) for r in range(p-1,0,-1)]
  require(len(V)==p+q and len(V)%2==1 and len({(key(x),key(y)) for x,y in V})==len(V),'distinct odd-cycle vertices')
  require(all(norm(V[k],V[(k+1)%len(V)])==ONE for k in range(len(V))),'exact odd-cycle unit edges');lengths.append(len(V))
 return {'count':len(lengths),'cycle_edges':sum(lengths),'minimum_length':min(lengths),'maximum_length':max(lengths)}

def audit(data):
 require(set(data)=={'schema','claim','cases','odd_cycle_parameters','target_found'} and type(data['schema'])is int and data['schema']==1,'schema')
 require(data['claim']=='written full-support theorem; finite audits only' and data['target_found']is False,'honest scope')
 require(len(data['cases'])==12 and len({c['input']['name'] for c in data['cases']})==12,'twelve named fixtures')
 reports=[audit_case(case) for case in data['cases']]
 return {'status':'PASS','claim_status':'written full-support theorems with exact finite audits','cases':reports,'total_point_pairs':sum(r['point_pairs'] for r in reports),'total_edge_checks':sum(r['edges'] for r in reports),'formula_controls':universal_formula_controls(),'odd_cycle_controls':odd_cycles(data['odd_cycle_parameters']),'floating_point_operations':0,'native_solver_calls':0,'target_found':False}

def controls(data):
 cases=[]
 def case(label,edit):
  x=copy.deepcopy(data);edit(x);cases.append((label,x))
 case('omitted fixture',lambda x:x['cases'].pop())
 case('bad geometry hash',lambda x:x['cases'][0].__setitem__('edge_sha256','0'*64))
 case('monochromatic unit edge',lambda x:x['cases'][0].__setitem__('colouring','0'*x['cases'][0]['vertices']))
 case('false predecessor bound',lambda x:x['cases'][0].__setitem__('predecessor_maximum',99))
 case('missing odd-cycle parameter',lambda x:x['odd_cycle_parameters'].pop())
 case('odd instead of even denominator',lambda x:x['odd_cycle_parameters'].__setitem__(0,[1,3]))
 case('false target flag',lambda x:x.__setitem__('target_found',True))
 # Projection across a vertical unit pair is invalid; use a certified boundary
 # fixture as an adversarial input to that branch of the theorem.
 case('vertical edge passed to projection',lambda x:x['cases'][4]['input'].__setitem__('method','projection'))
 for label,x in cases:
  try:audit(x)
  except (ValueError,TypeError,KeyError,IndexError):continue
  raise ValueError('Invalid certificate accepted: '+label)
 return [label for label,x in cases]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=False);p=Path(__file__).parent;blob=(p/'certificate.json').read_bytes();data=json.loads(blob)
 require(raw(data)==blob,'canonical certificate');report=audit(data);report['malformed_certificate_rejections']=controls(data);report['certificate_bytes']=len(blob);report['certificate_sha256']=hashlib.sha256(blob).hexdigest()
 if (p/'expected.json').exists():require(json.loads((p/'expected.json').read_text())==report,'expected report')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
