"""Whole NEW reader source consistency before parent mathematical imports."""
from pathlib import Path
import hashlib

DEFINING = {'check_refined.py', 'reader_binding.py', 'verify.py', 'adverse.py',
            'PROOF.md', 'README.md', 'EXPECTED.json', 'SOURCE.json', '.gitignore'}


def require(ok, why):
    if not ok:
        raise ValueError(why)


def source_files(root):
    root = Path(root)
    names, files = set(), []
    for line in (root / 'SHA256SUMS').read_text().splitlines():
        pin, name = line.split('  ', 1)
        require(name == Path(name).name and name not in names and len(pin) == 64 and
                all(c in '0123456789abcdef' for c in pin),
                'exact distinct NEW reader defining source manifest')
        names.add(name)
        blob = (root / name).read_bytes()
        require(hashlib.sha256(blob).hexdigest() == pin,
                'ENTIRE NEW reader source before math import: ' + name)
        files.append((name, blob, pin))
    require(names == DEFINING, 'all nine NEW reader defining sources')
    return files


def check_current():
    return source_files(Path(__file__).resolve().parent)
