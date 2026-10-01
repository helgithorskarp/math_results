"""Solver-free arithmetic/sign certificate check; Python3.11 stdlib only."""
from pathlib import Path
import hashlib,json
from audit import verify as audit
from signs import verify as signs
HERE=Path(__file__).resolve().parent
def result():
    data=json.loads((HERE/'certificate.json').read_text())
    canonical=json.dumps(data,sort_keys=True,separators=(',',':')).encode()
    return {'status':'AUTHOR_CHECKED_BOUNDARY_LEMMAS','authoring_agent':'six-tammes-2','role':'researcher',
            'canonical_certificate_sha256':hashlib.sha256(canonical).hexdigest(),
            'arithmetic_audit':audit(data),'sign_witnesses':signs(),
            'two_arbitrary_extensions_excluded':False,'global_tammes15_bound':False,
            'independent_researcher_review':False}
if __name__=='__main__':
    actual=result();expected=json.loads((HERE/'EXPECTED.json').read_text())
    if actual!=expected:raise ValueError('complete expected exact result differs')
    print(json.dumps(actual,sort_keys=True))
