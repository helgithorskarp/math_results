import argparse,json,sys,math,itertools
from pathlib import Path
from pysat.solvers import Cadical195
w=Path(__file__).resolve().parent
def parse(line):
 a=list(map(int,line.split()));n,h=a[:2];ks=a[2:2+h];axis=a[2+h:2+2*h];es=[];pos=2+2*h
 for i,j in itertools.combinations(range(h),2):
  t=a[pos];pos+=1;es.append(a[pos:pos+t]);pos+=t
 if pos!=len(a):raise ValueError(line)
 return n,h,ks,axis,es
def reduce_case(line):
 n,h,ks,axis,es=parse(line);pairs=list(itertools.combinations(range(h),2));shifts={0:0}
 while len(shifts)<h:
  old=len(shifts)
  for (i,j),zs in zip(pairs,es):
   if zs:
    if i in shifts and j not in shifts:shifts[j]=shifts[i]+zs[0]
    if j in shifts and i not in shifts:shifts[i]=shifts[j]-zs[0]
  if len(shifts)==old:raise ValueError('disconnected ring graph')
 shifted=[[(z+shifts[i]-shifts[j])%n for z in zs] for (i,j),zs in zip(pairs,es)]
 g=math.gcd(n,*ks,*sum(shifted,[]));nn=n//g
 # Relabel reflected copies as well, preserving internal step distances.
 newks=[k//g for k in ks]
 ds=[sorted(z//g for z in zs) for zs in shifted]
 ds=min(ds,[sorted((-z)%nn for z in zs) for zs in ds])
 key=[nn,h,*newks,*axis]
 for zs in ds:key.extend([len(zs),*zs])
 return ' '.join(map(str,key))
def edges(line):
 n,h,ks,axis,es=parse(line);ed=set()
 for i,k in enumerate(ks):
  for v in range(n):
   if k:ed.add(tuple(sorted((i*n+v,i*n+(v+k)%n))))
   if axis[i]:ed.add((i*n+v,h*n))
 for (i,j),zs in zip(itertools.combinations(range(h),2),es):
  for v in range(n):
   for z in zs:ed.add((i*n+v,j*n+(v+z)%n))
 return h*n+1,sorted(ed)
def solve(line):
 N,ed=edges(line);clauses=[[4*v+c+1 for c in range(4)] for v in range(N)]
 clauses += [[-(4*u+c+1),-(4*v+c+1)] for u,v in ed for c in range(4)]
 clauses += [[1]]
 with Cadical195(bootstrap_with=clauses) as s:
  if not s.solve():return None
  model=set(s.get_model());cs=[next(c for c in range(4) if 4*v+c+1 in model) for v in range(N)]
 if any(cs[u]==cs[v] for u,v in ed):raise RuntimeError('invalid colour word')
 return ''.join(map(str,cs))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('cases',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 src=args.cases
 keys=sorted(set(map(reduce_case,src.read_text().splitlines())))
 out=[];bad=[]
 for key in keys:
  cs=solve(key)
  if cs is None:bad.append(key);print('UNSAT',key,flush=True)
  else:out.append([key,cs])
 if bad:raise RuntimeError(f'{len(bad)} upper graphs were not coloured; no geometric conclusion follows')
 args.output.write_text(json.dumps(out,indent=1)+'\n')
 print(json.dumps({'keys':len(keys),'coloured':len(out),'uncoloured':len(bad),'word_bytes':sum(len(x[1]) for x in out)}))
