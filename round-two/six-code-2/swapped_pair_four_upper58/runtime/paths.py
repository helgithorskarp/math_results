"""Offline, hash-pinned inputs and local generated-data destination."""
import hashlib
import json
import os
from pathlib import Path
HERE = Path(__file__).resolve().parent
INPUTS = HERE/'inputs'
WORK = Path(os.environ.get('SWAPPED69_WORK', str(HERE/'work'))).resolve()

def verify_inputs(directory=INPUTS):
    manifest=json.loads((HERE/'INPUTS.json').read_text())
    for item in manifest:
        data=(directory/item['path']).read_bytes()
        if hashlib.sha256(data).hexdigest()!=item['sha256']:
            raise ValueError('changed pinned input: '+item['path'])
    return len(manifest)

verify_inputs()
