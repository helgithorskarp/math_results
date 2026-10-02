"""Complete ten-file imported executable closure, checked before import."""
from pathlib import Path
from hashlib import sha256
ROOT=Path(__file__).resolve().parent.parent
PINS={'remaining-deletion-orders/dependencies.py': 'f44adf04fdf5d64680c63ea3b28d83d7d8b42034766d158ea4859e3cb27179ca', 'remaining-deletion-orders/dual.py': '42f395caa99d10cc5b66f8c805ac700bfd68b612113194148bc1a15986678528', 'remaining-deletion-orders/orbits.py': '53c1b07e519d297d1836869c132a0fd87a5ab39bb8dc6871f3a263e93165493a', 'remaining-deletion-orders/three_vectors.py': 'a42d741151aaa3b888a7944c16e125478f386f87e6828e76bea27ee676a348aa', 'small-deletion-boundary/literal.py': '46218af58a0654279231ade1bc40106d9eb390b6c0b2ceee5f3c4c5b7bedbf39', 'triangle-majority/exact.py': 'e52c939bd67eabbcadea6e27c2cc5507fd1913189a63b8b5a3a79c1b8a89e6d0', 'variance-deletion-frontier/algebra.py': '0e1d92ffc3341823351cbfb90fdbe2fbb3b955e76034de087b0878cbcac5ce02', 'variance-deletion-frontier/pins.py': '5800784f4d233cd5a2eb955eba5aaecb39fe50e8e96f5329cc29a29450f1f7f2', 'variance-deletion-frontier/point.py': '2a0748f98043bbf20e8bb7a7a6d37153fe5aad192bc532be23e9bcdf8c257fa6', 'variance-deletion-frontier/variance.py': 'ac4622bd4e93d81db870e38bdfec8adceb62a470abb4224865d8f80182a388b7'}
def check():
    for name,expected in PINS.items():
        if sha256((ROOT/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('Changed credited executable input: '+name)
