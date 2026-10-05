"""Bind the full local source before any mathematical module/data import."""
from pathlib import Path
import hashlib


def require(ok,message):
    if not ok:raise ValueError(message)


def source_files(root):
    root=Path(root);seen=set();result=[]
    for line in (root/'SHA256SUMS').read_text().splitlines():
        sha,name=line.split('  ',1)
        require(len(sha)==64 and all(c in '0123456789abcdef' for c in sha)
                and name==Path(name).name and name not in seen,
                'distinct exact full local source-manifest paths')
        seen.add(name);raw=(root/name).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==sha,
                'ENTIRE source seal before mathematical import: '+name)
        result.append((name,raw,sha))
    require(seen=={'binding.py','model.py','physical.py','COEFFICIENTS.json',
                  'encoding.py','check.py','chart.py','adverse.py','verify.py',
                  'PROOF.md','README.md','PROVENANCE.json','EXPECTED.json',
                  'CANDIDATE.json','CANDIDATE-TAU0.json'},
            'complete exact self-contained defining source set')
    return result


def check_current():
    return source_files(Path(__file__).resolve().parent)
