"""Whole strict typed-record comparison, effective under python -O as well."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build import build,canonical
def pairs(items):
 d={}
 for k,v in items:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def bad(x):raise ValueError('nonfinite JSON value')
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('EXPECTED.json')
expected=json.loads(path.read_text(),object_pairs_hook=pairs,parse_constant=bad)
actual=build()
if canonical(expected)!=canonical(actual):raise ValueError('whole typed mathematical record mismatch')
print(json.dumps({'verified':True,'counts':actual['counts'],'canonical_sha256':hashlib.sha256(canonical(actual)).hexdigest()},sort_keys=True))
