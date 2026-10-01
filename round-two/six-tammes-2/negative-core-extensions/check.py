"""Regenerate every witness, separately audit it and compare exact output."""
from pathlib import Path
import json
from generate import produce
HERE=Path(__file__).resolve().parent
def check():
    actual=produce(audit=True)
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    if actual!=expected:raise ValueError('complete audited output differs from EXPECTED.json')
    return actual
if __name__=='__main__':print(json.dumps(check(),sort_keys=True))
