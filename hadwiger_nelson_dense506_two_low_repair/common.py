"""Pinned finite census and exact real-field pair arithmetic."""
from fractions import Fraction
from hashlib import sha256
from math import lcm
from pathlib import Path
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / 'hadwiger_nelson_dense506_one_low_repair/engine.py'
if sha256(SOURCE.read_bytes()).hexdigest() != '41b8461ef9ba14b37fdf045b5511efabe4a2e4b93a95f328077aa951a8db4c00':
    raise ValueError('prior engine pin')
spec = importlib.util.spec_from_file_location('prior_engine', SOURCE)
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)
G, S = E.G, E.S
PINS = {
    'points': '28b46f5eae9a537d8a189d03284e32d9012fbccde35f05bd72e19ee1f1699f43',
    'host_pairs': 'df22d5b218106b24ee0651fd6b7c8e79038765a75a90a923de507efa8299c8f0',
    'eligible_candidate_neighbors': '3e622b2e34c439bce776300c06890141458f568927e5e476c6dd19d865a13d39',
}


def load(candidate_work, centre_work):
    table = json.loads((centre_work / 'centres.json').read_text())
    for field, pin in PINS.items():
        S.require(G.digest(table[field]) == pin, 'centre table pin: ' + field)
    data, colors = S.load(candidate_work)
    masks = [15 ^ ((1 << colors[i]) | (1 << colors[j])) for i, j in table['host_pairs']]
    S.require(all(m.bit_count() == 2 for m in masks), 'outside palette size')
    for mask, neighbors in zip(masks, table['eligible_candidate_neighbors']):
        S.require(all(0 < data['available_masks'][c] < 16 and
                      not (data['available_masks'][c] & ~mask) for c in neighbors), 'eligibility')
    return table, data, masks


def squared_distance(a, b):
    d, e = a[0], b[0]
    dx = tuple(a[i] * e - b[i] * d for i in range(1, 5))
    dy = tuple(a[i] * e - b[i] * d for i in range(5, 9))
    norm = G.norm(dx, dy)
    coefficients = tuple(Fraction(x, (d * e) ** 2) for x in norm)
    denominator = lcm(*(x.denominator for x in coefficients))
    return (denominator,) + tuple(int(x * denominator) for x in coefficients)


def read_certificate():
    rows = []
    for line in (HERE / 'squared_distances.tsv').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        row = tuple(map(int, line.split()))
        S.require(len(row) == 6 and row[0] > 0 and row[-1] > 0, 'distance row')
        rows.append(row)
    S.require(len(rows) == len(set(r[:5] for r in rows)), 'duplicate squared distance')
    S.require(all(r[:5] != (1, 1, 0, 0, 0) for r in rows), 'unit distance in certificate')
    return [(r[:5], r[5]) for r in rows]


def triangle_obstruction(a, b, c, edge_mask):
    """For |a|,|b|>=2 and c nonempty, this is the complete failure criterion."""
    return bool(edge_mask == 7 and a == b and a.bit_count() == 2 and not (c & ~a))
