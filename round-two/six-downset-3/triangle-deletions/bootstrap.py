"""Validate the four SHA-pinned public helpers before making them importable."""
from pathlib import Path
import hashlib
import sys

BASE = Path(__file__).resolve().parent.parent/'triangle-majority'
EXPECTED = {'poly.py': '381e8635d3f1270e78175301c87bc8ffc1f1fc4699ba5cfbc20921b801cc3088', 'model.py': '970b35506437ef7f5b7955d559f003376bb0ed74ef2d215d098472646ed19224', 'exact.py': 'e52c939bd67eabbcadea6e27c2cc5507fd1913189a63b8b5a3a79c1b8a89e6d0', 'signs.py': '58d83c63335d728fb549f4a80b0c6b672d498306a52b2c82a7376544eec8b5fc'}
SOURCE_COMMIT = '99d63aa2f085127a670ae375b19a68b89e184074'


def setup(base=BASE, expected=EXPECTED):
    for name, sha in expected.items():
        if hashlib.sha256((base/name).read_bytes()).hexdigest() != sha:
            raise ValueError('Changed public dependency: '+name)
    parent = str(base)
    if parent not in sys.path:
        sys.path.insert(0, parent)


setup()
