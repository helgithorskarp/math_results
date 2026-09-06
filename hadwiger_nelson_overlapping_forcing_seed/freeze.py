"""Preserve the geometric support at the documented target-gate pivot."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
w=ROOT/'out';x=json.loads((w/'equality_union_reduced.json').read_text())
if x['status']!='frozen_for_target_gate':raise ValueError('Wrong discovery boundary')
c=json.loads((ROOT/'certificate.json').read_text())
if x['points']!=c['equal']['points']:raise ValueError('Discovery differs from published support')
(w/'equality_frozen.json').write_text(json.dumps(x,separators=(',',':'))+'\n')
