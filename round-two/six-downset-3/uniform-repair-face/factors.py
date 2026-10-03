"""Small exact divisor proposals, never an assumed sign or trusted quotient."""
from functools import lru_cache
import json
from pathlib import Path
import input as inputs
z, require = inputs.ipoly, inputs.require
BASE = Path(__file__).resolve().parent

def decode(rows):
    out = {}
    for power, value in rows:
        require(len(power)==2 and all(type(t) is int and t>=0 for t in power),
                'nonnegative integer factor monomial')
        key = tuple(power)
        require(key not in out and isinstance(value,str), 'unique exact factor encoding')
        coefficient = int(value)
        require(coefficient!=0, 'explicit zero factor coefficient')
        out[key] = coefficient
    require(bool(out), 'nonzero factor polynomial')
    return out

@lru_cache(maxsize=None)
def factor(name):
    data = json.loads((BASE/'FACTORS.json').read_text())['factors'][name]
    out = {(0,0):int(data['unit'])}
    require(bool(out[(0,0)]), 'nonzero factor unit')
    for entry in data['factors']:
        exponent = entry['power']
        require(type(exponent) is int and exponent>=1, 'positive factor power')
        polynomial = decode(entry['polynomial'])
        for _ in range(exponent): out = z.mul(out,polynomial)
    return out
