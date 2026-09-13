#!/usr/bin/env python3
"""Exact native-field contact enlargement; discovery-side integer formulas."""
from pathlib import Path
from hashlib import sha256
import json
HERE=Path(__file__).resolve().parent
INPUT=HERE.parent/'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv'
INPUT_SHA='4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02'

def source():
 raw=INPUT.read_bytes()
 if sha256(raw).hexdigest()!=INPUT_SHA:raise ValueError('source coordinate hash')
 A=[]
 for line in raw.decode().splitlines():
  if not line or line.startswith('#'):continue
  p=tuple(map(int,line.split()))
  if len(p)!=16 or any(p[k] for k in range(16) if k not in (0,5,9,12)):raise ValueError('source basis')
  A.append(tuple(p[k] for k in (0,5,9,12)))
 if len(A)!=159 or len(set(A))!=159:raise ValueError('source cardinality')
 return A

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def unitE(p):
 a,b,c,d=p
 return a*b+c*d==0 and a*a+33*b*b+3*c*c+11*d*d==144

def sign33(a,b):
 if not b:return (a>0)-(a<0)
 if not a:return (b>0)-(b<0)
 if (a>0)==(b>0):return (a>0)-(a<0)
 d=a*a-33*b*b
 return ((a>0)-(a<0))*((d>0)-(d<0))

def within(p):
 a,b,c,d=p
 return sign33(a*a+33*b*b+3*c*c+11*d*d-576,2*(a*b+c*d))<=0

def generate(truncate=True):
 A=source();dirs=sorted({sub(a,b) for a in A for b in A if unitE(sub(a,b))})
 if len(dirs)!=30 or not all(map(within,A)):raise ValueError('native controls')
 L=sorted(set(A)|{add(a,d) for a in A for d in dirs if not truncate or within(add(a,d))})
 native=[(8*a,0,8*b,0,8*c,0,8*d,0) for a,b,c,d in L]
 rotated=[(7*a,-3*c,7*b,-d,7*c,a,7*d,3*b) for a,b,c,d in L]
 points=list(dict.fromkeys(native+rotated))
 return points,{'source_vertices':len(A),'directions':len(dirs),'one_copy':len(L),'host_vertices':len(points),'denominator':96}

def unit(p):
 a,b,c,d,e,f,g,h=p
 return (a*a+5*b*b+33*c*c+165*d*d+3*e*e+15*f*f+11*g*g+55*h*h==96**2
  and a*b+33*c*d+3*e*f+11*g*h==0
  and a*c+5*b*d+e*g+5*f*h==0
  and a*d+b*c+e*h+f*g==0)

def edges(points):
 return [(j,i) for i,p in enumerate(points) for j in range(i) if unit(sub(p,points[j]))]

def cnf(n,ee):
 clauses=[];adj=[set() for _ in range(n)]
 for v in range(n):
  clauses.append([4*v+c+1 for c in range(4)])
  clauses.extend([-4*v-a-1,-4*v-b-1] for a in range(4) for b in range(a))
 for a,b in ee:
  clauses.extend([-4*a-c-1,-4*b-c-1] for c in range(4));adj[a].add(b);adj[b].add(a)
 tri=next((a,b,c) for a,b in ee for c in sorted(adj[a]&adj[b]) if c>b)
 clauses.extend([[4*v+c+1] for c,v in enumerate(tri)])
 text=f'p cnf {4*n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
 return text,tri

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 points,summary=generate();ee=edges(points);text,tri=cnf(len(points),ee)
 (args.out/'host.json').write_text(json.dumps({'points':points,'edges':ee},separators=(',',':'))+'\n')
 (args.out/'host.cnf').write_text(text)
 print(json.dumps(summary|{'edges':len(ee),'triangle':tri,'cnf_sha256':sha256(text.encode()).hexdigest()},indent=2))
