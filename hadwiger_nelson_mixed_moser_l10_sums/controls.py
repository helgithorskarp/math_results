from pathlib import Path
from itertools import combinations
import json,subprocess,sys
from build import palette,PZERO,add,norm
from reference_geometry import squared_norm
from native_geometry import candidates
from verify import word_check
ROOT=Path(__file__).resolve().parent

def main():
 a,b=palette();U=sorted(set(a+b));checked=0
 for p in U:
  if list(norm(p))!=squared_norm(p) or squared_norm(p)!=[144,0,0,0,0,0,0,0]:raise ValueError('Direction norm disagreement')
  checked+=1
 # Compare candidate-filtered edges to direct exact distances on a small
 # palette and sum fixture, without using producer edges or a floating filter.
 ps=sorted(set(U+[PZERO]+[add(U[i],U[j]) for i,j in combinations(range(12),2)]))
 expected=[[i,j] for i,j in combinations(range(len(ps)),2) if squared_norm([x-y for x,y in zip(ps[i],ps[j])])==[144,0,0,0,0,0,0,0]]
 found=[e for e in candidates(ps) if squared_norm([x-y for x,y in zip(ps[e[0]],ps[e[1]])])==[144,0,0,0,0,0,0,0]]
 if found!=expected:raise ValueError('Small exact graph mismatch')
 bad=['','0','0124','0012',[0,1,2,3]];rejected=0
 for w in bad:
  try:word_check(w,4,[[0,1],[1,2],[2,3]])
  except ValueError:rejected+=1
  else:raise RuntimeError('Bad word accepted')
 raw=subprocess.check_output([sys.executable,str(ROOT/'interval_controls.py')],text=True)
 print(json.dumps({'unit_direction_norms_checked':checked,'exact_small_points':len(ps),
                   'exact_small_pairs':len(ps)*(len(ps)-1)//2,'exact_small_edges':len(expected),
                   'malformed_colourings_rejected':rejected,'native_interval_controls':json.loads(raw)},sort_keys=True))
if __name__=='__main__':main()
