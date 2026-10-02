"""Verify the self-contained runtime inputs before importing exact code."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent

def verify_pins():
    data=json.loads((HERE/'DEPENDENCIES.json').read_text())
    for name,pin in data['before_import_source_pins'].items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=pin:
            raise ValueError('runtime source or compact certificate changed: '+name)
    return data['before_import_source_pins']
