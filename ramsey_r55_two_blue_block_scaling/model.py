"""Complete H_11 plus two prescribed blue K4 blocks; no symmetry restrictions."""
from pathlib import Path
from itertools import combinations
import importlib.util
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'ramsey_r55_q8_blue_block_obstruction'
spec=importlib.util.spec_from_file_location('_one_blue_model',PRIOR/'encode.py')
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
N=19
PAIRS=list(combinations(range(N),2))
BLOCK_EDGES={p for start in (11,15) for p in combinations(range(start,start+4),2)}
FREE=[p for p in PAIRS if p[1]>=11 and p not in BLOCK_EDGES]
VARIABLE={p:i+1 for i,p in enumerate(FREE)}

def catalog(path):return prior.catalog(path)
def decode(record):return prior.decode(record)
def fixed(record):return decode(record)|{p:0 for p in BLOCK_EDGES}

def physical(record):
 known=fixed(record)
 for size,color in ((4,1),(5,0)):
  for vs in combinations(range(N),size):
   edges=list(combinations(vs,2))
   if any(p in known and known[p]!=color for p in edges):continue
   yield vs,color,[(-1 if color else 1)*VARIABLE[p] for p in edges if p not in known]

def dimacs(record):
 rows=[c for _,_,c in physical(record)]
 return (f'p cnf 104 {len(rows)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in rows)).encode('ascii')

def universal():
 variables={p:i+1 for i,p in enumerate(PAIRS)}
 clauses=[[(-1 if color else 1)*variables[p] for p in combinations(vs,2)] for size,color in ((4,1),(5,0)) for vs in combinations(range(N),size)]
 clauses += [[-variables[p]] for p in sorted(BLOCK_EDGES)]
 return variables,clauses
