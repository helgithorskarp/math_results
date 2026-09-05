from pathlib import Path
from itertools import combinations
from hashlib import sha256
import json,importlib.util,sys,time,resource
sys.dont_write_bytecode=True
import argparse
from review_geometry import R,host
p=argparse.ArgumentParser(description='Independent exact parallelism verification of both screens.')
p.add_argument('--work',type=Path,required=True);a=p.parse_args();w=a.work;H=host()
assert (w/'screened.txt').read_bytes()==(w/'audit_screened.txt').read_bytes()
alpha=(0,0,1,0,0,0,0,0);count=tests=0;t=time.perf_counter()
for line in (w/'audit_screened.txt').read_text().splitlines():
 g,i,j,k,e,*hs=map(int,line.split());pairs=list(zip(hs[::2],hs[1::2]));ms=[R.add(H[a],H[b]) for a,b in pairs];ds=[R.sub(H[b],H[a]) for a,b in pairs]
 assert len(set(ms))==3
 assert R.scale(ms[2],2)==R.add(R.add(ms[0],ms[1]),R.scale(R.multiply(alpha,R.sub(ms[1],ms[0])),e))
 for a,b in combinations(ds,2):
  tests+=1;assert R.multiply(a,R.conjugate(b))==R.multiply(b,R.conjugate(a))
 count+=1
out={'root':-1,'rows':count,'parallel_checks':tests,'all_chords_parallel':True,'all_midpoint_triangles_valid':True,'screen_streams_byte_identical':True,'stream_sha256':sha256((w/'audit_screened.txt').read_bytes()).hexdigest()}
print(json.dumps(out,indent=2))
