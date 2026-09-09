"""Pinned source interfaces; reconstruct the actual squared-distance factors."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
from arithmetic import need

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT/'hadwiger_nelson_three_wheel_architecture'
SYMMETRY = ROOT/'hadwiger_nelson_three_wheel_symmetry_frontier'
SOURCE_SHA = '7d3813350faffa9e6710cddc44d528a93ece7a1405db28c799974afd38c96e49'
SYMMETRY_SHA = '14e2a5e3fc00af36d4ef57b6a8fdd964450633b0ab76f0f2783094172ec69132'


def load():
    a = (SOURCE/'certificate.json').read_bytes()
    b = (SYMMETRY/'certificate.json').read_bytes()
    need(hashlib.sha256(a).hexdigest() == SOURCE_SHA, 'h4065 source hash')
    need(hashlib.sha256(b).hexdigest() == SYMMETRY_SHA, 'h4071 source hash')
    cert, sym = json.loads(a), json.loads(b)
    sys.path.insert(0, str(SOURCE))
    spec = importlib.util.spec_from_file_location('hn_closure_source', SOURCE/'verify.py')
    src = importlib.util.module_from_spec(spec); spec.loader.exec_module(src)
    displacements, polynomials = src.input_polynomials()
    factors, decomposition = src.factor_check(cert, polynomials)
    base, inventory = src.pair_inventory(displacements, decomposition)
    allowed = set(sym['nonalignment_factor_ids'])
    positive = {i for i, f in enumerate(factors) if f in (src.A.DX, src.A.DY)}
    # Reconstruct the finite alignment divisor set rather than trust its labels.
    align = set()
    def find(p):
        vector = src.A.primitive(p)
        return cert['factors'].index(list(vector))
    from fractions import Fraction as F
    for a in (F(0), F(1, 3), F(-1, 3), F(1), F(-1)):
        n, d = a.numerator, a.denominator
        align.add(find({(1, 0): d, (0, 0): -n}))
        align.add(find({(0, 1): d, (0, 0): -n}))
        align.add(find({(0, 1): d, (1, 0): -d, (0, 0): -n, (1, 1): -3*n}))
    align.add(find({(0, 0): 1, (1, 1): 3}))
    need(len(align) == 16 and len(positive) == 2, 'alignment and positive factors')
    need(allowed == set(range(len(factors)))-align-positive, 'nonalignment factor domain')
    pairs = sym['pair_orbit_representatives']
    need(len(pairs) == 800 and len(set(map(tuple, pairs))) == 800, 'complete 800-system interface')
    need(all(len(p) == 2 and p[0] < p[1] and set(p) <= allowed for p in pairs), 'valid factor pairs')
    return src, cert['factors'], pairs, allowed, base, inventory


def bad_factors(word, allowed, base, inventory):
    need(type(word) is str and len(word) == 343 and set(word) <= set('0123'), 'four-colour word')
    need(all(word[a] != word[b] for a, b in base), 'Cartesian edges properly coloured')
    bad = set()
    for a, b, ids in inventory:
        if word[a] == word[b]:
            bad.update(ids)
    return bad & allowed
