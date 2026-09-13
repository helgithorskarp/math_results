from itertools import combinations,permutations
from pathlib import Path
import sys,time,json,hashlib
start=time.perf_counter();total=1<<25;nb=total//8
edges=list(combinations(range(5),2))
cycles=set()
for p in permutations(range(1,5)):
 q=(0,)+p;cycles.add(frozenset(tuple(sorted((q[i],q[(i+1)%5]))) for i in range(5)))
patterns=set()
for S in combinations(range(10),5):
 if S[0]>=5 or S[-1]<5:continue
 for cyc in cycles:
  mask=value=0;ok=True
  for i,j in edges:
   u,v=S[i],S[j];want=int((i,j) in cyc)
   if (u<5)==(v<5):
    fixed=int((v-u)%5 in (1,4))
    if fixed!=want:ok=False;break
   else:
    bit=5*(v-5)+u;mask|=1<<bit;value|=want<<bit
  if ok:patterns.add((mask,value))

vars=[]
for j in range(25):
 if j<3:b=bytes([sum(1<<i for i in range(8) if i>>j&1)])*nb
 else:
  span=1<<(j-3);b=(bytes(span)+b'\xff'*span)*(nb//(2*span))
 vars.append(int.from_bytes(b,'little'))
allbits=(1<<total)-1;remain=allbits
for mask,value in sorted(patterns):
 hit=allbits
 for j in range(25):
  if mask>>j&1:hit&=vars[j] if value>>j&1 else allbits^vars[j]
 remain&=allbits^hit
encoded=remain.to_bytes(nb,'little')
want=bytearray(nb);hist=[0]*26;count=0;seen=set()
for line in Path(sys.argv[1]).read_text().splitlines():
 m=int(line)
 if not 0<=m<total or m in seen:raise ValueError('invalid or repeated matrix')
 seen.add(m);want[m//8]|=1<<(m%8);hist[m.bit_count()]+=1;count+=1
if bytes(want)!=encoded:raise ValueError('full assignment-space mismatch')
print(json.dumps({'status':'EXACT_LOCAL_CROSS_CATALOGUE_CHECKED','assignments':total,'forbidden_partial_patterns':len(patterns),'survivors':count,'edge_histogram':hist,'truth_vector_sha256':hashlib.sha256(encoded).hexdigest()},indent=2))
