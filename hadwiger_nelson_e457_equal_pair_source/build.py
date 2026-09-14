#!/usr/bin/env python3
"""Rebuild the canonical E457 marked-different CNF."""
import argparse,json
from itertools import combinations
from pathlib import Path

HERE=Path(__file__).resolve().parent
def clauses(n,edges):
 def x(v,c):return 4*v+c+1
 out=[]
 for v in range(n):
  out.append([x(v,c) for c in range(4)])
  out.extend([-x(v,a),-x(v,b)] for a,b in combinations(range(4),2))
 for u,v in edges:out.extend([-x(u,c),-x(v,c)] for c in range(4))
 out.extend(([x(0,0)],[x(1,1)]));return out
def edges(rows):
 out=[]
 for i,j in combinations(range(len(rows)),2):
  a,b,c,d=(rows[i][q]-rows[j][q] for q in range(4))
  if 3*a*a+11*b*b+c*c+33*d*d==1296 and a*b+c*d==0:out.append((i,j))
 return out
def encode(n,formula):
 return (f'p cnf {4*n} {len(formula)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in formula)).encode()
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 rows=json.loads((HERE/'core.json').read_text())['points'];a.out.write_bytes(encode(len(rows),clauses(len(rows),edges(rows))))
if __name__=='__main__':main()

