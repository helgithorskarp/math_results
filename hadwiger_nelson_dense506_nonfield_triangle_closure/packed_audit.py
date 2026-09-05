from pathlib import Path
from hashlib import sha256
import json,time,resource
import argparse
p=argparse.ArgumentParser(description='Complete independent integer-packing midpoint census.')
p.add_argument('--work',type=Path,required=True);args=p.parse_args()
w=args.work;groups=json.loads((w/'groups.json').read_text());B=1<<18
powers=[B**i for i in range(8)]
def pack(v):return sum(a*b for a,b in zip(v,powers))
t=time.perf_counter();counts=[];digest=sha256()
with (w/'triangles.txt').open() as expected:
 for g,(_,rs) in enumerate(groups):
  ms=[tuple(m) for m,_ in rs];M=max(abs(x) for m in ms for x in m);assert 10*M<B-1
  left=[];right=[]
  for m in ms:
   jm=tuple(-3*x for x in m[4:])+m[:4]
   left.append(pack(tuple(a-b for a,b in zip(m,jm))));right.append(pack(tuple(a+b for a,b in zip(m,jm))))
  index={2*pack(m):i for i,m in enumerate(ms)};assert len(index)==len(ms)
  get=index.get;n=len(ms);pairs=triangles=0
  for i in range(n):
   li=left[i];ri=right[i]
   for j in range(i+1,n):
    pairs+=1
    k=get(ri+left[j],-1)
    if k>j:
     line=f'{g} {i} {j} {k} -1\n';assert next(expected)==line;digest.update(line.encode());triangles+=1
    k=get(li+right[j],-1)
    if k>j:
     line=f'{g} {i} {j} {k} 1\n';assert next(expected)==line;digest.update(line.encode());triangles+=1
  counts.append({'group':g,'pairs':pairs,'triangles':triangles});pass
 assert next(expected,None) is None
out={'encoding_base':B,'groups':counts,'triangles':sum(c['triangles'] for c in counts),'all_rows_match':True,'stream_sha256':digest.hexdigest()}
print(json.dumps(out,indent=2))
