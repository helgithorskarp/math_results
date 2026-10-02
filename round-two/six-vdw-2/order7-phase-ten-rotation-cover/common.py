"""Small source/dependency byte checks; no mathematical generator imports."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).absolute().parent

def require(ok,message):
    if not ok:raise ValueError(message)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def pins():
    data=json.loads((HERE/'SOURCE_PINS.json').read_text())
    for name,digest in data['relative_files'].items():
        require(sha(HERE.parent/name)==digest,'changed mathematical input: '+name)
    return data
