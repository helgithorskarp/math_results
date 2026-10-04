"""Recompute every original coefficient and every tensor control, without corpora."""
from pathlib import Path
import hashlib,json,sys,signal,time,resource
signal.alarm(45)
here=Path(__file__).resolve().parent
seal=json.loads((here/'PRIMARY_SEAL.json').read_text())
if set(seal['files'])!={'integers.py','controls.py','check.py'}:raise ValueError('primary source census')
for name,digest in seal['files'].items():
    if hashlib.sha256((here/name).read_bytes()).hexdigest()!=digest:raise ValueError('source seal before import')
sys.path.insert(0,str(here))
from check import math_record
start=time.monotonic();rec=math_record()
raw=(json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n').encode()
expected=json.loads((here/'EXPECTED.json').read_text())
if len(raw)!=expected['whole_bytes']or hashlib.sha256(raw).hexdigest()!=expected['whole_sha256']:raise ValueError('entire regenerated record agreement')
Path(sys.argv[1]).write_bytes(raw)
print(json.dumps({'whole_bytes':len(raw),'whole_sha256':hashlib.sha256(raw).hexdigest(),
 'all6786_controls_and_whole_original_maps':True,'all_original_reality_and_full_mass_controls':True,
 'seconds':round(time.monotonic()-start,6),'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
