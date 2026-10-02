"""SHA-check the credited entry table and exact arithmetic before import."""
from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parent.parent
PINS={'small-deletion-boundary/literal.py':'46218af58a0654279231ade1bc40106d9eb390b6c0b2ceee5f3c4c5b7bedbf39',
      'triangle-majority/exact.py':'e52c939bd67eabbcadea6e27c2cc5507fd1913189a63b8b5a3a79c1b8a89e6d0'}
SOURCE_COMMITS={'small-deletion-boundary':'41a580c695e0b0d38858af543a8fabcf880631ae',
                'triangle-majority':'99d63aa2f085127a670ae375b19a68b89e184074'}
def setup(pins=PINS):
    for name,sha in pins.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:
            raise ValueError('Changed published input '+name)
    for d in ('small-deletion-boundary','triangle-majority'):
        if str(ROOT/d) not in sys.path:sys.path.insert(1,str(ROOT/d))
setup()
