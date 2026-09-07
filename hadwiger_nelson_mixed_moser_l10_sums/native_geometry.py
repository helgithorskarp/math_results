"""Complete point-pair check with an integer-interval native filter."""
from pathlib import Path
from math import isqrt
from hashlib import sha256
import json,sys,subprocess,time
from reference_geometry import squared_norm,RAD
W=Path(__file__).resolve().parent/'out'
Q=1<<20
LOW=[isqrt(d*Q*Q) for d in RAD]
HIGH=[v if v*v==d*Q*Q else v+1 for d,v in zip(RAD,LOW)]

def interval(co):
 return (sum(v*(LOW[i] if v>=0 else HIGH[i]) for i,v in enumerate(co)),
         sum(v*(HIGH[i] if v>=0 else LOW[i]) for i,v in enumerate(co)))

def candidates(ps,binary=W/'interval_pairs'):
 iv=[interval(p[:8])+interval(p[8:]) for p in ps]
 if any(abs(v)>1000000000 for row in iv for v in row):raise ValueError('Interval outside audited range')
 text=str(len(ps))+'\n'+''.join(' '.join(map(str,row))+'\n' for row in iv)
 result=subprocess.run([str(binary)],input=text,capture_output=True,text=True,check=True)
 es=[list(map(int,line.split())) for line in result.stdout.splitlines()]
 if es!=sorted(es) or any(len(e)!=2 or not(0<=e[0]<e[1]<len(ps)) for e in es):raise ValueError('Malformed native output')
 return es

def main():
 t=time.monotonic();path=Path(sys.argv[1]);g=json.loads(path.read_text());ps=g['points'];n=len(ps)
 if g['denominator']!=12 or g['radicands']!=RAD:raise ValueError('Wrong convention')
 if any(len(p)!=16 or any(type(v) is not int for v in p) for p in ps):raise ValueError('Bad coordinates')
 if len(set(map(tuple,ps)))!=n:raise ValueError('Duplicate point')
 es=candidates(ps);out=[]
 for a,b in es:
  if squared_norm([x-y for x,y in zip(ps[a],ps[b])])==[144,0,0,0,0,0,0,0]:out.append([a,b])
 if out!=g['edges']:
  missing=sorted(set(map(tuple,out))-set(map(tuple,g['edges'])))
  bad=sorted(set(map(tuple,g['edges']))-set(map(tuple,out)))
  (W/(path.stem+'_extra_edges.json')).write_text(json.dumps({'missing':missing,'bad':bad},separators=(',',':'))+'\n')
  raise ValueError(f'Incomplete declared edges: missing {len(missing)}, bad {len(bad)}')
 ans={'vertices':n,'edges':len(out),'all_pairs':n*(n-1)//2,'interval_survivors':len(es),
      'complete_exact_edges_match':True,'native_filter':'Q=2^20, abs interval endpoint<=10^9',
      'seconds':time.monotonic()-t,
      'points_sha256':sha256(json.dumps(ps,separators=(',',':')).encode()).hexdigest(),
      'edges_sha256':sha256(json.dumps(out,separators=(',',':')).encode()).hexdigest()}
 colour=path.parent/(path.stem+'_colour.json')
 if colour.exists():
  x=json.loads(colour.read_text());word=x.get('colouring')
  if word is not None:
   if len(word)!=n or any(c not in '0123' for c in word) or any(word[a]==word[b] for a,b in out):raise ValueError('Bad word')
   ans['four_colouring_verified']=True
 (W/(path.stem+'_native_verified.json')).write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps(ans,indent=2))
if __name__=='__main__':main()
