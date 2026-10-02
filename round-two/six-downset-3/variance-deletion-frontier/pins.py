"""Complete imported executable closure; written premises linked in PROOF."""
from pathlib import Path
from hashlib import sha256
import sys
ROOT=Path(__file__).resolve().parent.parent
PINS={'small-deletion-boundary/literal.py': '46218af58a0654279231ade1bc40106d9eb390b6c0b2ceee5f3c4c5b7bedbf39', 'triangle-majority/exact.py': 'e52c939bd67eabbcadea6e27c2cc5507fd1913189a63b8b5a3a79c1b8a89e6d0'}
SOURCE_COMMITS={'small-deletion-boundary/literal.py':'41a580c695e0b0d38858af543a8fabcf880631ae',
                'triangle-majority/exact.py':'99d63aa2f085127a670ae375b19a68b89e184074'}
def setup(pins=PINS):
    for name,expected in pins.items():
        if sha256((ROOT/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('Changed credited executable input: '+name)
    for name in ('small-deletion-boundary','triangle-majority'):
        path=str(ROOT/name)
        if path not in sys.path:sys.path.append(path)
setup()
