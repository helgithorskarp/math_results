#!/usr/bin/env python3
"""Generate the full exact interface locally; generated output is not committed."""
from pathlib import Path
import argparse,hashlib,json
import verify as V
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if a.out.exists():raise FileExistsError(a.out)
 result=V.run(V.HERE/'certificate.json')
 rows,events,factors,fe,base,collisions,_,circle=V.build()
 cert=json.loads((V.HERE/'certificate.json').read_text())
 _,_,_,pairs=V.finite_cover(cert['colour_specs'],factors,fe,base)
 representative={}
 for r,f in zip(rows,events):
  if f:representative.setdefault(f,r)
 data={'schema':'hn-complex-radix-exact-interface-v1','parameter':'z=x+i*sqrt(3)*y; x,y real',
  'curves':[{'id':i,'polynomial':f,'displacement':representative[f]} for i,f in enumerate(factors)],
  'circle_id':circle,'pair_systems':pairs,'nonzero_collision_polynomials':collisions,
  'injective_nonfour_minimum_active_curves':4,
  'radial_constraint':'1/2 < |z| <= 2',
  'Q_x_y_degree_bound':64,'source_certificate_sha256':result['certificate_sha256']}
 raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(raw)
 print(json.dumps({'path':str(a.out),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'pairs':len(pairs),'curves':len(factors),'collision_polynomials':len(collisions)},indent=2,sort_keys=True))
