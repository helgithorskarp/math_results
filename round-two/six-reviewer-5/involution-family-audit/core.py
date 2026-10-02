"""Small explicit guards and literal operations; six-reviewer-5."""
import hashlib
import json
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()

def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()

def pin_inputs(base=HERE):
    rows = json.loads((base / 'INPUTS.json').read_text())
    require(len({r['path'] for r in rows}) == len(rows), 'duplicate input pin')
    for row in rows:
        require(hashlib.sha256((base / row['path']).read_bytes()).hexdigest() == row['sha256'],
                'changed input: ' + row['path'])

def mask(points):
    return sum(1 << v for v in points)

def points(word):
    return tuple(i for i in range(18) if word >> i & 1)

def image(word, permutation):
    return mask(permutation[v] for v in points(word))

def code_check(words, permutation=None):
    require(len(words) == len(set(words)), 'duplicate words')
    require(all(type(w) is int and 0 <= w < 1 << 18 and w.bit_count() == 5 for w in words),
            'five-subset domain')
    literal = [frozenset(points(w)) for w in words]
    require(all(len(a & b) <= 2 for a, b in combinations(literal, 2)), 'repeated triple')
    if permutation is not None:
        require(len(permutation) == 18 and sorted(permutation) == list(range(18)),
                'permutation domain')
        require({image(w, permutation) for w in words} == set(words), 'closure failure')
    return tuple(sum(v in w for w in literal) for v in range(18))

G = tuple(v ^ 1 if v < 16 else v for v in range(18))
