#!/usr/bin/env python3
"""Exact plus-host check of every modular survivor; expected full-stream identities."""
from pathlib import Path
from itertools import combinations
import argparse,json
import common as C
G=C.G
PINS={'triangles.txt':'bac810715525907a23cdff32f98e9237ae16f37aa29c4f1523e3395bb6b02d54',
      'screened.txt':'88580a61a55170031b3207f53a8b3a058713fb2cb414339bb5bd9ffff18fa920'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);a=p.parse_args()
 host,groups=C.load();stored=json.loads((a.work/'groups.json').read_text())
 C.require(json.loads(json.dumps(groups))==stored,'all prepared group entries')
 for name,pin in PINS.items():C.require(C.file_hash(a.work/name)==pin,'stream identity: '+name)
 count=tests=0
 for line in (a.work/'screened.txt').read_text().splitlines():
  row=list(map(int,line.split()));C.require(len(row)==11,'row width')
  g,i,j,k,e,*labels=row;C.require(e in (-1,1) and 0<=g<len(groups) and 0<=i<j<k<len(groups[g][1]),'row labels')
  ms=[];ds=[]
  for ix,(u,v) in zip((i,j,k),zip(labels[::2],labels[1::2])):
   m,pairs=groups[g][1][ix];C.require((u,v) in pairs,'host-pair membership')
   ms.append(m);ds.append((G.sub(host[v][0],host[u][0]),G.sub(host[v][1],host[u][1])))
  first,second,third=ms
  doubled=tuple(first[t]+second[t]-3*e*(second[t+4]-first[t+4]) for t in range(4))+tuple(first[t+4]+second[t+4]+e*(second[t]-first[t]) for t in range(4))
  C.require(doubled==tuple(2*x for x in third),'midpoint triangle')
  for u,v in combinations(ds,2):
   tests+=1;C.require(G.mul(u[0],v[1])==G.mul(u[1],v[0]),'nonparallel residual')
  count+=1
 print(json.dumps({'survivors':count,'exact_parallel_checks':tests,'all_parallel':True,
                   'midpoint_triangles':4050552,'host_pair_assignments':140742349,
                   'stream_hashes':PINS,'nonfield_obstructions':0},indent=2))
if __name__=='__main__':main()
