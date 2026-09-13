"""Exact displayed-coordinate comparison with the archived Parts509 source.

SymPy1.14.0 is used by the pinned earlier parser solely to denest coordinates.
No assertion about other placements or abstract graph isomorphism is made.
"""
from pathlib import Path
from hashlib import sha256
import sys,json
HERE=Path(__file__).resolve().parent

def compare(points):
 pins=json.loads((HERE/'SOURCE_PINS.json').read_text())
 for name,digest in pins.items():
  if sha256((HERE/name).read_bytes()).hexdigest()!=digest:raise ValueError('source pin '+name)
 source=HERE.parent/'hadwiger_nelson_parts509_criticality';sys.path.insert(0,str(source))
 import parts509 as R
 old=R.parse_points(source/'parts509.vtx');where={p:i for i,p in enumerate(points)};mapping={};missing=[]
 for v,(x,y) in enumerate(old):
  if any(x[k] for k in (1,3,4,6)) or any(y[k] for k in (0,2,5,7)):raise ValueError('coordinate subspace')
  values=tuple(q*96 for q in (x[0],x[2],x[5],x[7],y[1],y[3],y[4],y[6]))
  if any(q.denominator!=1 for q in values):raise ValueError('coordinate scale')
  p=tuple(map(int,values))
  if p in where:mapping[str(v)]=where[p]
  else:missing.append(v)
 return {'map':mapping,'missing':missing}
if __name__=='__main__':
 import radical_check as G
 result=compare(G.generate(False));c=json.loads((HERE/'certificate.json').read_text())
 if result['map']!=c['record_map'] or result['missing']!=c['missing_original_indices']:raise ValueError('record comparison mismatch')
 print(json.dumps({'matched_vertices':len(result['map']),'missing_original_indices':result['missing'],'scope':'displayed exact coordinates'},indent=2))
