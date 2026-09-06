"""Replay compact solver-status parser controls, without invoking a solver."""
import json
import hashlib
from pathlib import Path
from generate import status, need

data = json.loads((Path(__file__).resolve().parent/'controls.json').read_text())
for code,body in data['invalid_status_cases']:
    try:
        status(code,body)
    except ValueError:
        pass
    else:
        raise ValueError('bad transcript accepted')
for code,body,expected in data['valid_status_cases']:
    need(status(code,body) == expected,'valid status')
source = (Path(__file__).resolve().parent/'generate.py').read_bytes()
public_location = b"ROOT = Path(__file__).resolve().parent.parent\nPARENT = ROOT/'ramsey_r55_antipodal_degree_projection'"
original_location = b"ROOT = Path(__file__).resolve().parent\nPARENT = ROOT/'math_results/ramsey_r55_antipodal_degree_projection'"
need(source.count(public_location) == 1,'exact two-line source adapter')
original_sha = hashlib.sha256(source.replace(public_location,original_location,1)).hexdigest()
need(original_sha == 'b28a1077d8d201943a5c25376f9480ded1e8419f00f75d1e3373ebe288368176','reconstructed original run source')
print(json.dumps({'invalid_status_cases_rejected':len(data['invalid_status_cases']),
                  'valid_status_cases_checked':len(data['valid_status_cases']),
                  'original_run_source_sha256':original_sha},sort_keys=True))
