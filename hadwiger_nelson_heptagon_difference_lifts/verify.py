#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();here=Path(__file__).resolve().parent
for actual,expected in [('build_result.json','expected_build.json'),('count_lifts.json','expected_classify.json'),('audit_result.json','expected_audit.json'),('controls_result.json','expected_controls.json')]:
 x=json.loads((a.work/actual).read_text());x.pop('seconds',None)
 assert x==json.loads((here/expected).read_text()),actual
assert json.loads((a.work/'count_lifts.json').read_text())['complete']
v=json.loads((here/'validation.json').read_text())
assert sha256((a.work/'graph.json').read_bytes()).hexdigest()==v['graph_stream']['sha256']
assert sha256((a.work/'normalized_lifts.json').read_bytes()).hexdigest()==v['normalized_lift_stream_sha256']
print('EXACT421-POINT GRAPH AND COMPLETE42-LIFT CLASSIFICATION VERIFIED')
print('Unrestricted sqrt(3)-pair forcing remains unresolved.')
