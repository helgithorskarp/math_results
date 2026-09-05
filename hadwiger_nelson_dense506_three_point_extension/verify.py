#!/usr/bin/env python3
"""Compare completed run summaries and regenerated file bytes to compact expectations."""
from pathlib import Path
import argparse,json,sys
sys.dont_write_bytecode=True
import common as C
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
for actual,expected in [('summary.json','expected.json'),('audit_result.json','expected_audit.json'),('controls_result.json','expected_controls.json')]:
 x=json.loads((a.work/actual).read_text());y=json.loads((C.HERE/expected).read_text())
 if x!=y:raise AssertionError('Expected result differs: '+actual)
s=json.loads((a.work/'summary.json').read_text())
for name,row in s['files'].items():
 p=a.work/name
 if p.stat().st_size!=row['bytes'] or C.file_hash(p)!=row['sha256']:raise AssertionError('Generated stream differs: '+name)
print('ARBITRARY THREE-POINT EXTENSION: COMPLETE FIELD CENSUS AND AUDIT VERIFIED')
