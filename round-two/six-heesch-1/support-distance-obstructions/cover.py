"""Complete rooted grid-cover encoding; no solver dependency for reading."""
from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'linear-corona-bound'))
import sweep


def ball(cells, body, q):
    sweep.require(type(q) is int and q >= 0, 'invalid support distance')
    L = max(max(x, y) for x, y in cells) + 1
    r = q // L
    offsets = [(dx, dy) for dx in range(-r, r + 1)
               for dy in range(-r, r + 1)
               if sweep.support(body, (-dy, dx)) <= q]
    return sorted({(x + dx, y + dy) for x, y in cells for dx, dy in offsets})


def placements(cells, target):
    """All distinct integer D4 placements hitting a demanded nonroot cell."""
    root = set(cells)
    found = set()
    for orientation in sweep.variants(cells):
        translations = {(x - a, y - b) for x, y in target if (x, y) not in root
                        for a, b in orientation}
        for dx, dy in translations:
            physical = tuple(sorted((x + dx, y + dy) for x, y in orientation))
            if root.isdisjoint(physical):
                found.add(physical)
    return sorted(found)


def collision_cnf(candidates):
    """Sinz sequential at-most-one at EVERY footprint cell, including exterior."""
    owners = defaultdict(list)
    for i, physical in enumerate(candidates, 1):
        for p in physical:
            owners[p].append(i)
    clauses = []
    nv = len(candidates)
    for p in sorted(owners):
        xs = owners[p]
        if len(xs) < 2:
            continue
        if len(xs) == 2:
            clauses.append([-xs[0], -xs[1]])
            continue
        ss = list(range(nv + 1, nv + len(xs)))
        nv += len(xs) - 1
        clauses.append([-xs[0], ss[0]])
        for i in range(1, len(xs) - 1):
            clauses.extend(([-xs[i], ss[i]], [-ss[i - 1], ss[i]],
                            [-xs[i], -ss[i - 1]]))
        clauses.append([-xs[-1], -ss[-1]])
    return clauses, nv, owners


def compile_cover(cells, target):
    candidates = placements(cells, target)
    clauses, nv, owners = collision_cnf(candidates)
    clauses.extend(owners[p] for p in sorted(set(target) - set(cells)))
    return candidates, clauses, nv


def dimacs(clauses, nv):
    return ('p cnf %d %d\n' % (nv, len(clauses)) + ''.join(
            ' '.join(map(str, c)) + ' 0\n' for c in clauses)).encode()


def check_poses(cells, target, poses):
    orientations = sweep.variants(cells)
    occupied = set(cells)
    for pose in poses:
        sweep.require(isinstance(pose, list) and len(pose) == 3 and
                      all(type(z) is int for z in pose), 'malformed pose')
        o, dx, dy = pose
        sweep.require(0 <= o < len(orientations), 'invalid orientation')
        physical = {(x + dx, y + dy) for x, y in orientations[o]}
        sweep.require(occupied.isdisjoint(physical), 'witness overlap')
        occupied.update(physical)
    sweep.require(set(target) <= occupied, 'witness misses demanded cells')
    return len(poses)
