"""Independent literal adjacency and lifted colour-word checker. No SAT dependency."""
import argparse, hashlib, itertools, json, math
from pathlib import Path

def require(ok,msg):
 if not ok:raise ValueError(msg)

def parse(line):
 a=[int(z) for z in line.split()]
 require(len(a)>=2,'short row');n,h=a[:2]
 require(3<=n<=254 and h in (2,3),'bad order')
 require(len(a)>=2+2*h,'short ring data')
 ks=a[2:2+h];axis=a[2+h:2+2*h];pos=2+2*h;es={}
 require(all(0<=k<=n//2 for k in ks),'bad internal step')
 require(all(x in (0,1) for x in axis),'bad apex flag')
 for i,j in itertools.combinations(range(h),2):
  require(pos<len(a),'missing contact count');m=a[pos];pos+=1
  require(0<=m<=n and pos+m<=len(a),'bad contact count')
  zs=a[pos:pos+m];pos+=m
  require(zs==sorted(set(zs)) and all(0<=z<n for z in zs),'bad contact offsets')
  es[i,j]=zs
 require(pos==len(a),'trailing fields')
 return n,h,ks,axis,es

def check_word(line,word):
 n,h,ks,axis,es=parse(line);N=n*h+1
 require(len(word)==N and all(c in '0123' for c in word),'invalid word')
 # Every same-colour pair is checked by the adjacency predicate. This does not
 # generate edges by the producer's forward step/matching loops.
 classes=[[i for i,c in enumerate(word) if c==str(a)] for a in range(4)]
 checked=0
 for group in classes:
  for u,v in itertools.combinations(group,2):
   checked+=1;i,x=divmod(u,n)
   if v==n*h:adjacent=axis[i]==1
   else:
    j,y=divmod(v,n)
    if i==j:adjacent=ks[i]!=0 and ((y-x)%n in (ks[i],(-ks[i])%n))
    else:adjacent=(y-x)%n in es[i,j]
   require(not adjacent,'monochromatic edge')
 edge_count=sum(n//2 if 2*k==n else n for k in ks if k)+n*sum(axis)+n*sum(map(len,es.values()))
 return checked,edge_count

def lift_key(line):
 n,h,ks,axis,es=parse(line);offset=[None]*h;offset[0]=0
 for _ in range(h):
  for (i,j),zs in es.items():
   if zs:
    if offset[i] is not None and offset[j] is None:offset[j]=offset[i]+zs[0]
    if offset[j] is not None and offset[i] is None:offset[i]=offset[j]-zs[0]
 require(all(x is not None for x in offset),'disconnected ring graph')
 dd=[[(z+offset[i]-offset[j])%n for z in zs] for (i,j),zs in es.items()]
 g=math.gcd(n,*ks,*sum(dd,[]));N=n//g
 fwd=[sorted(z//g for z in zs) for zs in dd]
 rev=[sorted((-z)%N for z in zs) for zs in fwd]
 sign=-1 if rev<fwd else 1;norm=rev if sign<0 else fwd
 out=[N,h,*(k//g for k in ks),*axis]
 for zs in norm:out.extend([len(zs),*zs])
 indices=[t*N+(sign*(((v-offset[t])%n)//g))%N for t in range(h) for v in range(n)]+[h*N]
 return ' '.join(map(str,out)),indices

def verify(cases,certificate):
 raw=Path(cases).read_bytes();lines=raw.decode().splitlines();payload=Path(certificate).read_bytes()
 rows=json.loads(payload);require(isinstance(rows,list),'certificate must be a list')
 cert={};c_checks=c_edges=0
 for item in rows:
  require(isinstance(item,list) and len(item)==2 and all(isinstance(x,str) for x in item),'bad certificate row')
  key,word=item;require(key not in cert,'duplicate certificate key')
  z,e=check_word(key,word);c_checks+=z;c_edges+=e;cert[key]=word
 require(len(lines)==len(set(lines)),'duplicate emitted row')
 checks=edges=0;used=set();max3=max2=0
 for line in lines:
  key,indices=lift_key(line);require(key in cert,'uncovered geometry case');used.add(key)
  word=''.join(cert[key][v] for v in indices)
  z,e=check_word(line,word);checks+=z;edges+=e
  n,h,*_=parse(line)
  if h==3:max3=max(max3,n)
  else:max2=max(max2,n)
 require(used==set(cert),'unused certificate key')
 return {'emitted_cases':len(lines),'certificate_words':len(cert),'certificate_bytes':len(payload),
  'case_sha256':hashlib.sha256(raw).hexdigest(),'certificate_sha256':hashlib.sha256(payload).hexdigest(),
  'lifted_same_colour_pairs_checked':checks,'lifted_edges':edges,'small_word_pairs_checked':c_checks,
  'small_word_edges':c_edges,'largest_emitted_three_ring_n':max3,'largest_emitted_two_ring_n':max2}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cases');p.add_argument('--certificate',default=str(Path(__file__).with_name('certificate.json')))
 a=p.parse_args();print(json.dumps(verify(a.cases,a.certificate),indent=2))
