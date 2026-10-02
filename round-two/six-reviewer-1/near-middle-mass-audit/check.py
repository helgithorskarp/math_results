#!/usr/bin/env python3
import argparse,hashlib,importlib.util,json,signal,sys
from pathlib import Path
signal.alarm(45)
root=Path(__file__).resolve().parent
# Explicit local imports in isolated mode; target source is never on this path.
sys.path.insert(0,str(root))
import core
p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--expected',type=Path,default=root/'expected.json');a=p.parse_args()
r=core.record();raw=json.dumps(r,indent=2,sort_keys=True)+'\n'
if a.write:
 if a.expected.exists():raise ValueError('refuse to overwrite sealed fixture')
 a.expected.write_text(raw)
if a.expected.read_text()!=raw:raise ValueError('entire typed canonical fixture mismatch')
print(json.dumps({'status':'PASS','whole_record_sha256':hashlib.sha256(core.canonical(r)).hexdigest(),'layer_cases':len(r['original_layer_coefficient_cases']),'literal_original_positions':sum(c['all_original_positions'] for c in r['literal_original_controls']),'math_damages':len(r['mathematical_damage_rejections'])},sort_keys=True))
