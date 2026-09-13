"""Byte pins for imported mathematical source and corollary premises."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
def verify():
    pins=json.loads((HERE/'SOURCE_PINS.json').read_text())
    for name,expected in pins.items():
        if hashlib.sha256((HERE.parent/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('source pin mismatch: '+name)
    return len(pins)
if __name__=='__main__':print(json.dumps({'status':'PASS','pinned_files':verify()},sort_keys=True))
