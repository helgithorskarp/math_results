"""Verify the entire declared local source snapshot before mathematical imports."""
from pathlib import Path
import hashlib


def require(ok, message):
    if not ok:raise ValueError(message)


def source_files(root):
    root=Path(root)
    seen=set();result=[]
    lines=(root/'SHA256SUMS').read_text().splitlines()
    require(len(lines)>=18,'complete self-contained source set')
    for line in lines:
        sha,name=line.split('  ',1)
        require(len(sha)==64 and name==Path(name).name and name not in seen,
                'distinct exact local source-manifest paths')
        seen.add(name);raw=(root/name).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==sha,'ENTIRE source seal before mathematical import: '+name)
        result.append((name,raw,sha))
    require({'model.py','joint.py','entries.py','polyhedron.py','geometry.py',
             'affine_check.py','physical.py','diagnose.py','COEFFICIENTS.json',
             'certify.py','defects.py','verify.py','binding.py','PROOF.md'}<=seen,
            'all defining proof, input and reader sources bound')
    return result


def check_current():
    return source_files(Path(__file__).resolve().parent)
