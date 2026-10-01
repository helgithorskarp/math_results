"""Pin four compact previously published exact helpers before importing them."""
from pathlib import Path
import hashlib,sys
BASE=Path(__file__).resolve().parent.parent
SOURCE_COMMITS={'triangle-majority':'99d63aa2f085127a670ae375b19a68b89e184074','maximal-deletion':'abea9c6bff3924c42bbd7814f14845caffdcf7b8'}
PINS={'triangle-majority/poly.py': '381e8635d3f1270e78175301c87bc8ffc1f1fc4699ba5cfbc20921b801cc3088', 'triangle-majority/exact.py': 'e52c939bd67eabbcadea6e27c2cc5507fd1913189a63b8b5a3a79c1b8a89e6d0', 'maximal-deletion/symbolic.py': '59153617de2ea2f871aa03fa5802aeda82234d00b660cb0da46bc20c060a4aed', 'maximal-deletion/literal.py': '51333b999cb61038a858879f1b43df36c70f58e05322cf8c28210adf3ca381b7'}

def setup(base=BASE,pins=PINS):
 for path,sha in pins.items():
  if hashlib.sha256((base/path).read_bytes()).hexdigest()!=sha:raise ValueError('Changed public helper: '+path)
 for name in ['triangle-majority','maximal-deletion']:
  if str(base/name) not in sys.path:sys.path.insert(1,str(base/name))

setup()
