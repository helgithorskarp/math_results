"""Complete self-contained defining-source consistency before math imports."""
from pathlib import Path
import hashlib


DEFINING={'binding.py','model.py','physical.py','COEFFICIENTS.json','encoding.py',
          'check_boundary.py','check_postline.py','check_structure.py',
          'BOUNDARY-CANDIDATE.json','POSTLINE-CANDIDATE.json','DUAL.json',
          'ENTRY-PRIMAL.json','EXPECTED.json','SOURCE.json','adverse.py',
          'verify.py','PROOF.md','README.md','.gitignore'}


def require(ok,message):
    if not ok:raise ValueError(message)


def source_files(root):
    root=Path(root);seen=set();result=[]
    for line in (root/'SHA256SUMS').read_text().splitlines():
        pin,name=line.split('  ',1)
        require(len(pin)==64 and all(c in '0123456789abcdef' for c in pin)
                and name==Path(name).name and name not in seen,
                'distinct exact complete source manifest paths')
        seen.add(name);raw=(root/name).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==pin,
                'ENTIRE source seal before mathematical import: '+name)
        result.append((name,raw,pin))
    require(seen==DEFINING,'complete exact self-contained ceiling defining source')
    return result


def check_current():
    return source_files(Path(__file__).resolve().parent)
