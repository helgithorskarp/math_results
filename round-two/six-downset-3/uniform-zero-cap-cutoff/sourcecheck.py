"""Check the complete compact contribution before mathematical imports."""
from pathlib import Path,PurePosixPath
import hashlib


def digest(content):return hashlib.sha256(content).hexdigest()


def check_bundle(base=None):
    base=Path(base) if base is not None else Path(__file__).resolve().parent
    content=(base/'SHA256SUMS').read_bytes()
    expected={}
    for line in content.decode().splitlines():
        value,name=line.split('  ',1)
        path=PurePosixPath(name)
        if (len(value)!=64 or any(c not in '0123456789abcdef' for c in value)
            or name in expected or path.is_absolute() or '..' in path.parts
            or path.as_posix()!=name or name=='SHA256SUMS'):
            raise ValueError('malformed complete source manifest')
        expected[name]=value
    if not expected:raise ValueError('empty complete source manifest')
    actual=set()
    for path in base.rglob('*'):
        relative=path.relative_to(base)
        if 'work' in relative.parts or '__pycache__' in relative.parts or path.suffix=='.pyc':
            continue
        if path.is_symlink():raise ValueError('source symlink outside input closure')
        if path.is_file() and relative.as_posix()!='SHA256SUMS':
            actual.add(relative.as_posix())
    if actual!=set(expected):raise ValueError('omitted or unexpected source path')
    for name,value in expected.items():
        if digest((base/name).read_bytes())!=value:
            raise ValueError('changed complete source: '+name)
    return {'complete_source_manifest_sha256':digest(content),
            'complete_source_file_count':len(expected),
            'entire_sources_checked_before_mathematical_import':True}
