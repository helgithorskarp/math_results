"""Pinned author inputs; recursive physical census (standard library only)."""
from pathlib import Path
from itertools import combinations
import argparse,collections,gzip,hashlib,json,urllib.request
HERE=Path(__file__).resolve().parent

def specs():return json.loads((HERE/'INPUTS.json').read_text())
def inputs(cache):
 out={}
 for s in specs():
  raw=(Path(cache)/s['name']).read_bytes()
  if len(raw)!=s['bytes'] or hashlib.sha256(raw).hexdigest()!=s['sha256']:raise ValueError('catalog identity '+s['name'])
  out[s['n']]=raw
 return out

def download(cache):
 cache=Path(cache);cache.mkdir(parents=True,exist_ok=True)
 for s in specs():
  p=cache/s['name']
  if p.exists():continue
  wire=urllib.request.urlopen(s['url'],timeout=60).read()
  if hashlib.sha256(wire).hexdigest()!=s['download_sha256']:raise ValueError('download identity')
  p.write_bytes(gzip.decompress(wire) if s['url'].endswith('.gz') else wire)
 inputs(cache)

def parse(line,n):
 if not isinstance(line,bytes) or not line.endswith(b'\n'):raise ValueError('newline')
 data=line[:-1];m=n*(n-1)//2
 if len(data)!=1+(m+5)//6 or data[0]!=n+63 or any(not 63<=c<=126 for c in data):raise ValueError('graph6 shape')
 bits=''.join(format(x-63,'06b') for x in data[1:])
 if any(c!='0' for c in bits[m:]):raise ValueError('padding')
 a=[0]*n;k=0
 for j in range(1,n):
  for i in range(j):
   if bits[k]=='1':a[i]|=1<<j;a[j]|=1<<i
   k+=1
 return a

def get(cache,n,index):
 s=next(x for x in specs() if x['n']==n)
 if type(index) is not int or not 0<=index<s['count']:raise ValueError('core index')
 raw=(Path(cache)/s['name']).read_bytes()
 if len(raw)!=s['bytes'] or hashlib.sha256(raw).hexdigest()!=s['sha256']:raise ValueError('catalog identity')
 line=raw[index*s['line_bytes']:(index+1)*s['line_bytes']]
 return parse(line,n)

def cliques(a,k,remaining=None):
 if k==0:return 1
 if remaining is None:remaining=(1<<len(a))-1
 if remaining.bit_count()<k:return 0
 if k==1:return remaining.bit_count()
 total=0
 while remaining:
  bit=remaining&-remaining;remaining-=bit
  total+=cliques(a,k-1,remaining&a[bit.bit_length()-1])
 return total

def statistics(a):
 n=len(a);b=[((1<<n)-1)^(1<<i)^row for i,row in enumerate(a)]
 if cliques(a,4) or cliques(b,4):raise ValueError('not Ramsey(4,4)')
 return sum(x.bit_count() for x in a)//2,cliques(a,3),cliques(b,3)

def census(cache,rows_path):
 blobs=inputs(cache);summary=[]
 with Path(rows_path).open('wb') as out:
  for s in specs():
   n=s['n'];lines=blobs[n].splitlines(keepends=True)
   if len(lines)!=s['count'] or len(set(lines))!=s['count']:raise ValueError('count/literal uniqueness')
   hist=collections.Counter();digest=hashlib.sha256()
   for idx,line in enumerate(lines):
    a=parse(line,n);e,tr,tb=statistics(a);hist[e,tr,tb]+=1
    bits=sum(((a[i]>>j)&1)<<k for k,(i,j) in enumerate(combinations(range(n),2)))
    row=f'{n} {idx} {e} {tr} {tb} {bits&((1<<64)-1)} {bits>>64}\n'.encode();out.write(row);digest.update(row)
   summary.append(dict(n=n,count=len(lines),records_sha256=digest.hexdigest(),histogram=[list(k)+[v] for k,v in sorted(hist.items())]))
 return summary

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('--download',action='store_true');p.add_argument('--rows');p.add_argument('--summary');a=p.parse_args()
 if a.download:download(a.cache)
 if a.rows:
  s=census(a.cache,a.rows)
  if a.summary:Path(a.summary).write_text(json.dumps(s,indent=2)+'\n')
  print(json.dumps([{'n':x['n'],'count':x['count'],'records_sha256':x['records_sha256']} for x in s]))
