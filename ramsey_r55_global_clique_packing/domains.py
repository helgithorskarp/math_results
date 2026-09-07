"""Exact binary cross-matrix domains between fixed atoms of order three or four."""
from functools import lru_cache
from itertools import combinations
import hashlib,json,time
from pathlib import Path

TYPES={'R4':(4,63),'B4':(4,0),'R3':(3,7),'B3':(3,0),'E3':(3,1),'P3':(3,3)}

def inside(kind):
 n,mask=TYPES[kind]
 return {p:(mask>>k)&1 for k,p in enumerate(combinations(range(n),2))}

@lru_cache(maxsize=None)
def patterns(left,right):
 n,_=TYPES[left];m,_=TYPES[right];a=inside(left);b=inside(right);out=[]
 for q in combinations(range(n+m),5):
  fixed=[];cross=0
  for i,j in combinations(q,2):
   if j<n:fixed.append(a[i,j])
   elif i>=n:fixed.append(b[i-n,j-n])
   else:cross|=1<<(i*m+j-n)
  for color in (0,1):
   if all(x==color for x in fixed):out.append((cross,cross if color else 0))
 return tuple(sorted(set(out)))

@lru_cache(maxsize=None)
def states(left,right):
 n,_=TYPES[left];m,_=TYPES[right];forbidden=patterns(left,right)
 return tuple(x for x in range(1<<(n*m)) if all((x&mask)!=bad for mask,bad in forbidden))

def comparable_columns(kind):
 n,_=TYPES[kind]
 if kind=='E3':return [(0,1)]
 if kind=='P3':return [(1,2)]
 return [(j,j+1) for j in range(n-1)]

def root_signatures(kind,state):
 m=TYPES[kind][0]
 return [sum(((state>>(i*m+j))&1)<<i for i in range(4)) for j in range(m)]

@lru_cache(maxsize=None)
def root_states(kind):
 return tuple(x for x in states('R4',kind) if all(root_signatures(kind,x)[a]>=root_signatures(kind,x)[b] for a,b in comparable_columns(kind)))

def root_certificate():
 result=[]
 for kind in TYPES:
  bits=4*TYPES[kind][0];xs=root_states(kind);bitmap=sum(1<<x for x in xs);h=format(bitmap,f'0{(1<<bits)//4}x')
  result.append({'child':kind,'count':len(xs),'allowed_bitmap_hex':h,'bitmap_sha256':hashlib.sha256(bytes.fromhex(h)).hexdigest()})
 return result

def certificate():
 result=[]
 for a in TYPES:
  for b in TYPES:
   n,_=TYPES[a];m,_=TYPES[b];xs=states(a,b);bitmap=sum(1<<x for x in xs)
   h=format(bitmap,f'0{(1<<(n*m))//4}x')
   result.append({'left':a,'right':b,'matrix_bits':n*m,'count':len(xs),'forbidden_patterns':len(patterns(a,b)),
                  'allowed_bitmap_hex':h,'bitmap_sha256':hashlib.sha256(bytes.fromhex(h)).hexdigest()})
 return result

if __name__=='__main__':
 t=time.monotonic();d=certificate();Path(__file__).with_name('DOMAINS.json').write_text(json.dumps(d,indent=2)+'\n')
 print(json.dumps({'seconds':time.monotonic()-t,'counts':{x['left']+'/'+x['right']:x['count'] for x in d}}))
