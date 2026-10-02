#!/usr/bin/env python3
import argparse,hashlib,json,signal,sys
from pathlib import Path
signal.alarm(45)
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root))
import core
p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--expected',type=Path,default=root/'expected.json');a=p.parse_args()
r=core.record();raw=json.dumps(r,indent=2,sort_keys=True)+'\n'
if a.write:
 if a.expected.exists():raise ValueError('refuse to overwrite sealed fixture')
 a.expected.write_text(raw)
if a.expected.read_text()!=raw:raise ValueError('entire typed canonical fixture mismatch')
canonical=json.dumps(r,sort_keys=True,separators=(',',':')).encode()
print(json.dumps({'status':'PASS','record_sha256':hashlib.sha256(canonical).hexdigest(),'original_section_order':r['cyclic_all_nine_original_sections']['series_order'],'whole_window_margins':len(r['entire_window_budgets']['entire_strict_margin_table']),'literal_controls':len(r['literal_multiplicity_chamber_original_controls']),'math_damages':len(r['mathematical_damage_rejections'])},sort_keys=True))
