"""Sibling-directory layout used by the one-anchor closure tools (repository version).

CRIT   : hadwiger_nelson_parts509_criticality   (parts509.py, parts509.vtx: exact vertex coordinates)
SWAP   : hadwiger_nelson_parts509_swap_closure   (kfield.py, enumerate_completion_points.py, completion_points.json = Q3)
PAIR   : hadwiger_nelson_parts509_pair_closure   (pair_closure.py, pair_certificate.json, ambient_w3_edges.json)
TRIPLE : hadwiger_nelson_parts509_triple_closure (two_neighbour_points.py, nonk_exact.py, cluster_U.py, triple_certificate.json;
          q2k_extra.json and nonk_exact.json must be regenerated there: python two_neighbour_points.py; python nonk_exact.py q2k_extra.json nonk_exact.json)
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
_CAND = [HERE.parent, Path.home() / 'math_results']


def sibling(name, probe):
    return next(p / name for p in _CAND if (p / name / probe).exists())


CRIT = sibling('hadwiger_nelson_parts509_criticality', 'parts509.py')
SWAP = sibling('hadwiger_nelson_parts509_swap_closure', 'kfield.py')
PAIR = sibling('hadwiger_nelson_parts509_pair_closure', 'pair_closure.py')
TRIPLE = sibling('hadwiger_nelson_parts509_triple_closure', 'two_neighbour_points.py')
for p in (SWAP, TRIPLE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
COMPLETION = SWAP / 'completion_points.json'
Q2K_EXTRA = TRIPLE / 'q2k_extra.json'
NONK_EXACT = TRIPLE / 'nonk_exact.json'
N, K = 509, 4
