#!/usr/bin/env python3
import argparse,hashlib,json,signal,sys
from pathlib import Path
signal.alarm(45)
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root))
import core
p=argparse.ArgumentParser()
p.add_argument('--write',action='store_true')
p.add_argument('--expected',type=Path,default=root/'expected.json')
a=p.parse_args();r=core.run();raw=core.canonical(r)+'\n'
if a.write:
    if a.expected.exists():raise ValueError('refuse fixture overwrite')
    a.expected.write_text(raw)
if a.expected.read_text()!=raw:raise ValueError('entire typed fixture mismatch')
print(json.dumps({'status':'PASS','record_sha256':hashlib.sha256(raw[:-1].encode()).hexdigest(),'harmonic_degrees':len(r['sectors']),'literal_affine_controls':len(r['literal']['controls']),'full_upper_gap1_32':r['domain']['certified_gap1_32'],'ternary_matrices':r['arithmetic']['count']},sort_keys=True))
