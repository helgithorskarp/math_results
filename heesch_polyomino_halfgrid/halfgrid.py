"""Exact half-phase collapse and the first-corona doubled-tile bridge.

Universal correctness is the written proof, not this finite diagnostic module.
The imported covering formula and arrangement checker are hash-pinned sources.
"""
from dataclasses import replace
from fractions import Fraction
import hashlib
import importlib
from pathlib import Path
import sys


PINS = {
    'prior': {
        'cover.py': '67155ec7fd3f6997acf9857b938b1cc51eb9d1f4f8511b3f2e39f8e74c7dc0ae',
        'corona.py': 'd207a5f8a5b025392a0941427f6cf760386d87194a329e8be36a2033a12d99ec',
        'circuit.py': 'be6a80950052bb3b5b09874b3ecd16a22fb5caa1cec55b0734891e591a00c975',
        'topology.py': '65f914feed3f60a63304b36651e3b5fc99c35847ffa4a5ccc27bdec7bc361f54',
    },
    'motion': {
        'motion.py': 'fa3be9050a10a28675abc92122543b145306091828d984d187e74c10529de5dd',
    },
}


def load_dependencies(prior, motion):
    directories = {}
    for name, directory in (('prior', prior), ('motion', motion)):
        directory = Path(directory).resolve()
        directories[name] = directory
        for file, expected in PINS[name].items():
            actual = hashlib.sha256((directory/file).read_bytes()).hexdigest()
            if actual != expected:
                raise ValueError(file+' dependency hash mismatch')
        sys.path.insert(0, str(directory))
    cover = importlib.import_module('cover')
    motion = importlib.import_module('motion')
    for group, directory in directories.items():
        for file in PINS[group]:
            module = importlib.import_module(file[:-3])
            if Path(module.__file__).resolve() != directory/file:
                raise ValueError(file+' imported from an unexpected path')
    return cover, motion


def half_phase(t):
    """Nondecreasing, unit-periodic rounding; integers stay fixed."""
    t = Fraction(t)
    return Fraction(t // 1) + (Fraction(1, 2) if t % 1 else 0)


def collapse(poses):
    return [replace(p, tx=half_phase(p.tx), ty=half_phase(p.ty)) for p in poses]


def normalize(cells):
    raw = [tuple(p) for p in cells]
    if not raw or len(raw) != len(set(raw)):
        raise ValueError('nonempty distinct cells required')
    if any(len(p) != 2 or any(type(x) is not int for x in p) for p in raw):
        raise ValueError('integer cell pairs required')
    x0, y0 = min(x for x, y in raw), min(y for x, y in raw)
    return tuple(sorted((x-x0, y-y0) for x, y in raw))


def double_cells(tile):
    return tuple(sorted((2*x+dx, 2*y+dy) for x, y in normalize(tile)
                        for dx in (0, 1) for dy in (0, 1)))


def vertex_quadrant(square, vertex, signs):
    """Whether a closed unit square fills this infinitesimal quadrant."""
    return all(a <= v < a+1 if sign == 1 else a < v <= a+1
               for a, v, sign in zip(square, vertex, signs))


def decode_cover(tile, patch, motion):
    """Decode doubled-grid copies, then check definitions with rational geometry."""
    tile = normalize(tile)
    doubled = double_cells(tile)
    shapes = {double_cells(s): s for s in motion.variants(tile)}
    poses = []
    for raw in patch:
        cells = tuple(tuple(p) for p in raw)
        shape = normalize(cells)
        if shape not in shapes:
            raise ValueError('noncongruent doubled-grid copy')
        x, y = min(a for a, b in cells), min(b for a, b in cells)
        root = set(cells) == set(doubled)
        poses.append(motion.Pose(0 if root else 1, shapes[shape], Fraction(x, 2), Fraction(y, 2)))
    statistics = motion.check_corona(tile, 1, poses, holes_last=True)
    if any(p.level and p.tx % 1 and p.ty % 1 for p in poses):
        raise ValueError('copy contacting integer root cannot have two nonzero phases')
    return poses, statistics


def encode_poses(poses):
    return [{'level': p.level, 'shape': p.shape,
             'translation': [str(p.tx), str(p.ty)]} for p in poses]
