"""Complete source census and whole bytes checked before mathematical input."""
from pathlib import Path
import hashlib
import json

REQUIRED={'.gitignore','README.md','PROOF.md','LITERATURE.md','EXPECTED.json',
          'BASE-DATA.json','COMPARISON.json','GEOMETRY.json','check.py','produce.py',
          'damage.py','sourcecheck.py','validate.py'}


def check_bundle(base):
    base=Path(base).resolve();meta=json.loads((base/'BUNDLE.json').read_bytes())
    raw=(base/'SHA256SUMS').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=meta['manifest_SHA256']:
        raise ValueError('entire defining source manifest changed')
    names=set();size=0
    for line in raw.decode().splitlines():
        digest,name=line.split('  ',1);p=Path(name)
        if p.is_absolute() or '..' in p.parts or name in names or (base/p).is_symlink():
            raise ValueError('invalid complete source path')
        data=(base/p).read_bytes()
        if hashlib.sha256(data).hexdigest()!=digest:
            raise ValueError('whole source file changed: '+name)
        names.add(name);size+=len(data)
    actual={p.name for p in base.iterdir() if p.is_file()}
    if names!=REQUIRED or len(names)!=meta['manifest_file_count'] or size!=meta['manifest_source_bytes'] or actual!=REQUIRED|{'BUNDLE.json','SHA256SUMS'}:
        raise ValueError('entire declared mathematical source closure required')
    return dict(manifest_SHA256=meta['manifest_SHA256'],
                all_source_bytes_verified_before_mathematical_input=True)
