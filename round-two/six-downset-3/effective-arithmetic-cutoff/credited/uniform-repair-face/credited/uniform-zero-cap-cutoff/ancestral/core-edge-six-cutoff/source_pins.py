"""Check both defining executable inputs in full before importing either."""
from pathlib import Path
from hashlib import sha256
import json

ROOT = Path(__file__).resolve().parent.parent


def check():
    data = json.loads(Path(__file__).with_name('INPUTS.json').read_text())
    if set(data['inputs']) != {'small-deletion-boundary/literal.py',
                              'triangle-majority/exact.py'}:
        raise ValueError('Changed complete executable input closure')
    for name, entry in data['inputs'].items():
        content = (ROOT/name).read_bytes()
        if len(content) != entry['bytes'] or sha256(content).hexdigest() != entry['sha256']:
            raise ValueError('Changed full defining input: '+name)
    return data
