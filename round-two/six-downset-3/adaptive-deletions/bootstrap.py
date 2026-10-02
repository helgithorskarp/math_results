"""SHA-pin compact published inputs before importing them.

The table is credited9145; its complete sector mechanism is credited8757.
No matrices, private data, or large certificate corpus are imported.
"""
from pathlib import Path
import hashlib, sys

ROOT=Path(__file__).resolve().parent.parent
SOURCE_COMMITS={
    'triangle-majority':'99d63aa2f085127a670ae375b19a68b89e184074',
    'two-deletion-kappa':'21bd374fef20b19b8a07f12e0bfc0e43d4f2d3e7'}
PINS={
    'triangle-majority/poly.py':'381e8635d3f1270e78175301c87bc8ffc1f1fc4699ba5cfbc20921b801cc3088',
    'triangle-majority/model.py':'970b35506437ef7f5b7955d559f003376bb0ed74ef2d215d098472646ed19224',
    'triangle-majority/exact.py':'e52c939bd67eabbcadea6e27c2cc5507fd1913189a63b8b5a3a79c1b8a89e6d0',
    'triangle-majority/signs.py':'58d83c63335d728fb549f4a80b0c6b672d498306a52b2c82a7376544eec8b5fc',
    'two-deletion-kappa/weights.py':'a0db7aeace187a373efe8121388e7984e6ec3c7160e7fd9e36c434d2a4f4e457',
    'two-deletion-kappa/bootstrap.py':'7e116ff284977314887c4018ea3f1df84f9d92bea25371515efc29b3134b2246'}

def setup(root=ROOT,pins=PINS):
    for name,sha in pins.items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=sha:
            raise ValueError('Changed published input: '+name)
    for directory in ('triangle-majority','two-deletion-kappa'):
        path=str(root/directory)
        if path not in sys.path:sys.path.insert(1,path)

setup()
