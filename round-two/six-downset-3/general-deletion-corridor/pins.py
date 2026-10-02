"""One credited standalone original-entry input; no copied matrix corpus."""
from hashlib import sha256
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
PINS = {'small-deletion-boundary/literal.py':
        '46218af58a0654279231ade1bc40106d9eb390b6c0b2ceee5f3c4c5b7bedbf39'}
SOURCE_COMMIT = '41a580c695e0b0d38858af543a8fabcf880631ae'


def setup(pins=PINS):
    for name, expected in pins.items():
        if sha256((ROOT/name).read_bytes()).hexdigest() != expected:
            raise ValueError('Changed credited original-entry input: '+name)
    path = str(ROOT/'small-deletion-boundary')
    if path not in sys.path:
        sys.path.insert(1, path)


setup()
