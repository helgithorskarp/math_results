"""Verify four small published helpers before importing them."""
from pathlib import Path
import hashlib,sys

BASE=Path(__file__).resolve().parent.parent/'triangle-majority'
SOURCE_COMMIT='99d63aa2f085127a670ae375b19a68b89e184074'
PINS={'poly.py':'381e8635d3f1270e78175301c87bc8ffc1f1fc4699ba5cfbc20921b801cc3088',
      'model.py':'970b35506437ef7f5b7955d559f003376bb0ed74ef2d215d098472646ed19224',
      'exact.py':'e52c939bd67eabbcadea6e27c2cc5507fd1913189a63b8b5a3a79c1b8a89e6d0',
      'signs.py':'58d83c63335d728fb549f4a80b0c6b672d498306a52b2c82a7376544eec8b5fc'}

def setup(base=BASE,pins=PINS):
    for name,sha in pins.items():
        if hashlib.sha256((base/name).read_bytes()).hexdigest()!=sha:
            raise ValueError('Changed published helper: '+name)
    if str(base) not in sys.path:sys.path.insert(1,str(base))

setup()
