"""Complete source and immutable mathematical input gates, before math imports.

The trusted entry point is the source at the reader's chosen repository commit.
SHA256SUMS detects accidental damage; the inline pins bind the prior publication
and the finite rational witness even if the outer manifest is rewritten.
"""
from pathlib import Path, PurePosixPath
import hashlib

ANCESTOR='ancestral/uniform-zero-cap-cutoff'
ANCESTOR_PIN='b783ede83b894ba80936d6d11ad25a7be2c437602234e23aa95ebc3d4c454cb5'
CERTIFICATE_PIN='b1736a349e42999cf2301fa6dd2c719152e7c95a1b30f9bcf93ffa635a664c73'


def digest(content):
    return hashlib.sha256(content).hexdigest()


def manifest(base):
    raw=(base/'SHA256SUMS').read_bytes()
    expected={}
    for line in raw.decode().splitlines():
        value,name=line.split('  ',1)
        path=PurePosixPath(name)
        if (len(value)!=64 or any(c not in '0123456789abcdef' for c in value)
            or name in expected or path.is_absolute() or '..' in path.parts
            or path.as_posix()!=name or name=='SHA256SUMS'):
            raise ValueError('malformed complete source manifest')
        expected[name]=value
    if not expected:
        raise ValueError('empty complete source manifest')
    actual=set()
    for path in base.rglob('*'):
        relative=path.relative_to(base)
        if 'work' in relative.parts or '__pycache__' in relative.parts or path.suffix=='.pyc':
            continue
        if path.is_symlink():
            raise ValueError('source symlink outside input closure')
        if path.is_file() and relative.as_posix()!='SHA256SUMS':
            actual.add(relative.as_posix())
    if actual!=set(expected):
        raise ValueError('omitted or unexpected source path')
    for name,value in expected.items():
        if digest((base/name).read_bytes())!=value:
            raise ValueError('changed complete source: '+name)
    return raw,expected


def check_bundle(base=None):
    base=Path(base) if base is not None else Path(__file__).resolve().parent
    raw,files=manifest(base)
    old=base/ANCESTOR
    if digest((old/'SHA256SUMS').read_bytes())!=ANCESTOR_PIN:
        raise ValueError('changed immutable credited whole-source manifest')
    oldraw,oldfiles=manifest(old)
    if len(oldfiles)!=43 or digest(oldraw)!=ANCESTOR_PIN:
        raise ValueError('incomplete credited source closure')
    if digest((base/'CERTIFICATE.json').read_bytes())!=CERTIFICATE_PIN:
        raise ValueError('changed immutable seven-deletion rational witness')
    return {'actual_agent':'six-downset-3','role':'researcher',
            'complete_source_manifest_sha256':digest(raw),
            'complete_source_file_count':len(files),
            'credited_source_file_count':len(oldfiles),
            'credited_manifest_sha256':ANCESTOR_PIN,
            'certificate_sha256':CERTIFICATE_PIN,
            'entire_sources_checked_before_mathematical_import':True}
