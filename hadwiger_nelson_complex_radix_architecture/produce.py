#!/usr/bin/env python3
"""Deterministically emit the compact curve-cover certificate; no CAS/SAT."""
from pathlib import Path
import argparse,json
import verify as V
SPECS=[{'field':3,'weights':[1,0,0,0,0]},
 {'field':4,'weights':[1,0,1,0,1]},
 {'field':4,'weights':[1,1,0,0,1]},
 {'field':4,'weights':[1,1,0,0,2]},
 {'field':4,'weights':[1,1,1,1,1]}]
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 _,_,factors,fe,base,_,_,_=V.build();_,_,protect,pairs=V.finite_cover(SPECS,factors,fe,base)
 c={'schema':'hn-complex-radix-v1','factor_inventory_sha256':V.digest(factors),'colour_specs':SPECS,'protectors':protect}
 target=a.out/'certificate.json';target.write_text(json.dumps(c,sort_keys=True,separators=(',',':'))+'\n')
 result=V.run(target);(a.out/'EXPECTED.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,indent=2,sort_keys=True))
