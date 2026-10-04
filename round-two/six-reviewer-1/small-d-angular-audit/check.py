"""Verify sealed independent source, rebuild and compare the entire record."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
seal=json.loads((ROOT/'PRIMARY_SEAL.json').read_text())
for name,pin in seal['files'].items():
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=pin:
        raise ValueError('primary source seal '+name)
sys.path.insert(0,str(ROOT))
from verify import build
record=build()
encoded=(json.dumps(record,sort_keys=True,indent=2)+'\n').encode()
if encoded!=(ROOT/'EXPECTED.json').read_bytes():
    raise ValueError('entire deterministic expected record mismatch')
print(json.dumps({'gate_count':record['gate_count'],'bytes':len(encoded),
                  'sha256':hashlib.sha256(encoded).hexdigest(),'whole_record_equal':True}))
