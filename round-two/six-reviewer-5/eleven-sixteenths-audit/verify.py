"""Independent adjacent-annulus audit: exact data/source gate precedes imports."""
import hashlib,json,os,pathlib,sys
P=pathlib.Path(__file__).resolve().parent
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    if os.environ.get(name,'1')!='1':raise ValueError('native threads must be one')
seals=json.loads((P/'SOURCE.json').read_text())
for name,row in seals.items():
    raw=(P/name).read_bytes()
    if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('PREIMPORT SOURCE '+name)
cover=(P/'COVER.json').read_bytes();deps=json.loads((P/'DEPENDENCIES.json').read_text());pin=next(x for x in deps['written_target_inputs'] if x['path'].endswith('/COVER.json'))
if len(cover)!=pin['bytes'] or hashlib.sha256(cover).hexdigest()!=pin['sha256']:raise ValueError('COMPLETE AUTHOR MATHEMATICAL DATA PIN')
sys.path.insert(0,str(P));import face,bridges
summary,full=face.make(json.loads(cover));payment=bridges.make()
result=dict(face=summary,bridges=payment)
raw=face.canon(result);expected=face.canon(json.loads((P/'EXPECTED.json').read_text()))
if raw!=expected:raise ValueError('COMPLETE INDEPENDENT FIXTURE')
print(json.dumps(dict(status='PASS',canonical_bytes=len(raw),canonical_sha256=hashlib.sha256(raw).hexdigest(),record=result),sort_keys=True,separators=(',',':')))
