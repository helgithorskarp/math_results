"""Verify every credited runtime file before importing it."""
import hashlib
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent

def ensure_runtime(directory=None):
    directory=Path(directory) if directory is not None else HERE/'runtime'
    data=json.loads((HERE/'RUNTIME.json').read_text())
    for item in data:
        if hashlib.sha256((directory/item['path']).read_bytes()).hexdigest()!=item['sha256']:
            raise ValueError('changed runtime input: '+item['path'])
    if str(directory) not in sys.path:sys.path.insert(0,str(directory))
    return len(data)
