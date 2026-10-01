"""Two compact SHA-pinned exact helpers from the published triangle-majority source."""
from pathlib import Path
import hashlib,sys

BASE=Path(__file__).resolve().parent.parent/'triangle-majority'
SOURCE_COMMIT='99d63aa2f085127a670ae375b19a68b89e184074'
EXPECTED={
 'poly.py':'381e8635d3f1270e78175301c87bc8ffc1f1fc4699ba5cfbc20921b801cc3088',
 'exact.py':'e52c939bd67eabbcadea6e27c2cc5507fd1913189a63b8b5a3a79c1b8a89e6d0'}

def setup(base=BASE,expected=EXPECTED):
 for name,sha in expected.items():
  if hashlib.sha256((base/name).read_bytes()).hexdigest()!=sha:
   raise ValueError('Changed public helper: '+name)
 if str(base) not in sys.path:sys.path.insert(0,str(base))

setup()
