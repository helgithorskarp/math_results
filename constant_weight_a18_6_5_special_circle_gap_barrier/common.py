"""Exact shared inputs, authenticated reuse; six-code-2, researcher.

The imported programs are the previously published implementations by
this same researcher. Distinct algorithms here are not peer review.
"""
from hashlib import sha256
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
DEPENDENCY = ROOT.parent / 'constant_weight_a18_6_5_steiner_extension_barrier'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return sha256(canonical_bytes(value)).hexdigest()


def check_dependencies():
    pins = json.loads((ROOT / 'DEPENDENCIES.json').read_text())
    for name, wanted in pins['files_sha256'].items():
        require(sha256((DEPENDENCY / name).read_bytes()).hexdigest() == wanted,
                'dependency bytes changed: ' + name)
    return pins


PINS = check_dependencies()
sys.path.insert(0, str(DEPENDENCY))
from geometry import classical_design, mask, move, points
from verify_four_gap import close_group
from generate_fixed_word_gap import enumerate_fixed_words
from verify_fixed_word_gap import enumerate_sets, clique_census
from generate_five_gap_projection import project
from verify_five_gap_projection import pair_projection
from generate_three_gap import find_clique


def source_fingerprint():
    files = sorted(ROOT.glob('*.py'))
    files += [ROOT / name for name in ['DEPENDENCIES.json', 'expected.json', 'fixtures.json']]
    hashes = [(p.name, sha256(p.read_bytes()).hexdigest()) for p in files]
    return digest(hashes)


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)
