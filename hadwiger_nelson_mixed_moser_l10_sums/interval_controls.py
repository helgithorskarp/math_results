from pathlib import Path
from itertools import combinations
from random import Random
import subprocess,json,sys
W=Path(__file__).resolve().parent/'out';S=12*(1<<20);UNIT=S*S

def brute(points):
 def sq(a,b):return (0 if a<=0<=b else min(a*a,b*b),max(a*a,b*b))
 es=[]
 for i,j in combinations(range(len(points)),2):
  a,b,c,d=points[i];e,f,g,h=points[j]
  l,u=sq(a-f,b-e);v,w=sq(c-h,d-g)
  if l+v<=UNIT<=u+w:es.append([i,j])
 return es

def main():
 binary=Path(sys.argv[1]) if len(sys.argv)>1 else W/'interval_pairs'
 rng=Random(20260907);pts=[(0,0,0,0),(S,S,0,0),(0,0,S,S),(-S,-S,0,0),
                         (S-1,S+1,-1,1),(S+1,S+2,0,0),
                         (-1000000000,-1000000000,-1000000000,-1000000000),
                         (1000000000,1000000000,1000000000,1000000000)]
 for _ in range(192):
  a=rng.randrange(-2*S,2*S);b=rng.randrange(-2*S,2*S)
  pts.append((a,a+rng.randrange(0,S),b,b+rng.randrange(0,S)))
 def run(text):return subprocess.run([str(binary)],input=text,text=True,capture_output=True)
 text=str(len(pts))+'\n'+''.join(' '.join(map(str,p))+'\n' for p in pts)
 p=run(text)
 if p.returncode:raise RuntimeError(p.stderr)
 es=[list(map(int,s.split())) for s in p.stdout.splitlines()]
 if es!=brute(pts):raise RuntimeError('Interval pair disagreement')
 bad=['','-1\n','200001\n','1\n','1\n0 0 0\n','1\n1 0 0 0\n',
      '1\n0 0 1 0\n','1\n-1000000001 0 0 0\n','1\n0 1000000001 0 0\n','0\nextra\n']
 for s in bad:
  p=run(s)
  if p.returncode!=2:raise RuntimeError('Malformed input not rejected correctly: '+p.stderr)
 print(json.dumps({'exact_interval_pairs_compared':len(pts)*(len(pts)-1)//2,
                   'interval_candidates':len(es),'malformed_rejected':len(bad),
                   'boundary_overflow_controls':True},sort_keys=True))
if __name__=='__main__':main()
