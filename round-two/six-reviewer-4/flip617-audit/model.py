"""Reviewer4's fresh exact field model; no target code or certificate imports."""
import hashlib,json
P=617
def need(ok,why):
 if not ok: raise ValueError(why)
def digest(value):
 return hashlib.sha256((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
def squares():
 return {(x*x)%P for x in range(1,P)}
def gauss(x):
 need(0<x<P,'nonzero Gauss argument')
 return sum((2*((x*j)%P)>P) for j in range(1,(P+1)//2))%2
def inv(x):
 need(0<x<P,'inverse argument')
 a,b=P,x;u,v=0,1
 while b:
  q=a//b;a,b=b,a-q*b;u,v=v,u-q*v
 need(a==1,'invertible');return u%P
def endpoint():
 sq=squares();need(len(sq)==308,'square class size')
 for x in range(1,P):need(gauss(x)==int(x not in sq),'independent character agreement')
 out=[]
 for d in range(1,P):
  support=[(1+j*d)%P for j in range(1,7)]
  if all(x and gauss(x)==1 for x in support):out.append([d,sorted(support)])
 need(len(out)==6,'six endpoint supports')
 first=[set(s) for _,s in out[:5]]
 need(len(set.union(*first))==30,'five disjoint supports')
 V=set().union(*(set(s) for _,s in out));Vi={inv(x) for x in V}
 need(len(V)==33 and not(V&Vi),'no reciprocal arcs')
 need(all(x not in sq and x for x in V|Vi),'opposite class')
 return out,V,V|Vi
def neighbors(D):
 sq=sorted(squares());ns=sorted(set(range(1,P))-set(sq));index={x:i for i,x in enumerate(ns)}
 masks={q:sum(1<<index[x] for x in ns if (x*inv(q))%P in D) for q in sq}
 need(all(m.bit_count()==66 for m in masks.values()),'ratio graph degree')
 # Multiplication-based sets are an independent control on literal ratio masks.
 for q,m in masks.items():need({x for x in ns if m>>index[x]&1}=={q*d%P for d in D},'literal/product neighbors')
 return sq,ns,masks
