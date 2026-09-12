"""Complete blue-K4 extension of every literal R(4,4) core of order eleven."""
from itertools import combinations
from pathlib import Path
import hashlib
CATALOG_SHA256='39e10a1bb2d6b36d556e646e12f0181b2bc3bd45b334ad7f495b8900d7680433'
CATALOG_COUNT=546356
PAIRS=list(combinations(range(15),2))
CROSS=[(u,v) for u in range(11) for v in range(11,15)]
VARIABLE={p:i+1 for i,p in enumerate(CROSS)}

def catalog(path):
 raw=Path(path).read_bytes()
 if len(raw)!=6556272 or hashlib.sha256(raw).hexdigest()!=CATALOG_SHA256:raise ValueError('catalog identity')
 records=raw.decode('ascii').splitlines()
 if len(records)!=CATALOG_COUNT:raise ValueError('catalog count')
 return records

def decode(record):
 if len(record)!=11 or ord(record[0])-63!=11:raise ValueError('graph6 dimensions')
 vals=[ord(x)-63 for x in record[1:]]
 if any(not 0<=x<=63 for x in vals) or vals[-1]&31:raise ValueError('graph6 alphabet/padding')
 return {(i,j):(vals[(j*(j-1)//2+i)//6]>>(5-(j*(j-1)//2+i)%6))&1 for j in range(1,11) for i in range(j)}

def fixed(record):
 return decode(record) | {p:0 for p in combinations(range(11,15),2)}

def physical(record):
 known=fixed(record)
 for k,color in ((4,1),(5,0)):
  for vertices in combinations(range(15),k):
   edges=list(combinations(vertices,2))
   if any(p in known and known[p]!=color for p in edges):continue
   yield vertices,color,[(-1 if color else 1)*VARIABLE[p] for p in edges if p not in known]

def formula(record):return [row for _,_,row in physical(record)]

def dimacs(record):
 rows=formula(record)
 return (f'p cnf 44 {len(rows)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in rows)).encode('ascii')

def universal():
 variables={p:i+1 for i,p in enumerate(PAIRS)}
 rows=[[(-1 if color else 1)*variables[p] for p in combinations(vertices,2)] for k,color in ((4,1),(5,0)) for vertices in combinations(range(15),k)]
 rows.extend([[-variables[p]] for p in combinations(range(11,15),2)])
 return variables,rows
