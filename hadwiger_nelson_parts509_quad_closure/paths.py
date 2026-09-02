"""Sibling-directory layout used by the all-anchored delete-5-add-4 closure tools (repository version).

CRIT   : hadwiger_nelson_parts509_criticality   (parts509.py, parts509.vtx: exact vertex coordinates)
SWAP   : hadwiger_nelson_parts509_swap_closure   (kfield.py, completion_points.json = Q3, swap_certificate.json)
PAIR   : hadwiger_nelson_parts509_pair_closure   (pair_closure.py, pair_certificate.json, ambient_w3_edges.json)
TRIPLE : hadwiger_nelson_parts509_triple_closure (cluster_U.py, two_neighbour_points.py, nonk_exact.py, triple_certificate.json;
          q2k_extra.json and nonk_exact.json must be regenerated there:
          python two_neighbour_points.py; python nonk_exact.py q2k_extra.json nonk_exact.json)
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
_CAND = [HERE.parent, Path.home() / 'math_results']


def sibling(name, probe):
    for p in _CAND:
        if (p / name / probe).exists():
            return p / name
    raise FileNotFoundError(f'sibling directory {name} (probe {probe}) not found next to {HERE} or under ~/math_results')


CRIT = sibling('hadwiger_nelson_parts509_criticality', 'parts509.py')
SWAP = sibling('hadwiger_nelson_parts509_swap_closure', 'kfield.py')
PAIR = sibling('hadwiger_nelson_parts509_pair_closure', 'pair_closure.py')
TRIPLE = sibling('hadwiger_nelson_parts509_triple_closure', 'two_neighbour_points.py')
for p in (SWAP, TRIPLE, HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
COMPLETION = SWAP / 'completion_points.json'
SWAP_CERT = SWAP / 'swap_certificate.json'
PAIR_CERT = PAIR / 'pair_certificate.json'
AMBIENT = PAIR / 'ambient_w3_edges.json'
TRIPLE_CERT = TRIPLE / 'triple_certificate.json'
Q2K_EXTRA = TRIPLE / 'q2k_extra.json'
NONK_EXACT = TRIPLE / 'nonk_exact.json'
N, K = 509, 4
