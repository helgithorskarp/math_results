"""Preimport source gate and entire independent record seal; remains active with -O."""
import json,hashlib,sys,argparse
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path,default=HERE/'EXPECTED.json');a=p.parse_args()
def need(ok,msg):
 if not ok:raise ValueError(msg)
f=json.loads(a.fixture.read_text())
need(type(f)is dict and set(f)=={'agent','role','checks','whole_record_bytes','whole_record_sha256','source_hashes'},'entire fixture schema')
need(f['agent']=='six-reviewer-1'and f['role']=='independent mathematical reviewer','explicit methodology identity')
need(type(f['checks'])is int and f['checks']==83 and type(f['whole_record_bytes'])is int and f['whole_record_bytes']==187990,'strict typed full record sizes')
need(type(f['whole_record_sha256'])is str and len(f['whole_record_sha256'])==64,'entire canonical record digest')
need(type(f['source_hashes'])is dict and set(f['source_hashes'])=={'field.py','poly.py','intervals.py','derive.py'},'entire source gate schema')
for n,h in f['source_hashes'].items():
 need(type(h)is str and len(h)==64 and hashlib.sha256((HERE/n).read_bytes()).hexdigest()==h,'preimport source '+n)
sys.path.insert(0,str(HERE))
from derive import run
r=run();raw=json.dumps(r,sort_keys=True,separators=(',',':')).encode()
need(len(r['checks'])==f['checks']and len(raw)==f['whole_record_bytes']and hashlib.sha256(raw).hexdigest()==f['whole_record_sha256'],'entire exact independent record')
print(json.dumps({'agent':f['agent'],'role':f['role'],'checks':f['checks'],'whole_record_bytes':len(raw),'whole_record_sha256':hashlib.sha256(raw).hexdigest(),'all_source_and_entire_record_checks_passed':True},sort_keys=True,separators=(',',':')))
