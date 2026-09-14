"""Positive collision control and independent radical distance arithmetic."""
from itertools import combinations, product
import copy
import json
import verify as v


def norm(p, q):
    # Prime-mask basis 1,sqrt3,sqrt11,sqrt33 on each coordinate.
    a, b, c, d = (x-y for x, y in zip(p, q))
    axes = [(0, a, b, 0), (c, 0, 0, d)]
    radicals = (1, 3, 11, 33)
    out = [0]*4
    for axis in axes:
        for i, x in enumerate(axis):
            for j, y in enumerate(axis):
                out[i ^ j] += x*y*radicals[i & j]
    return tuple(out)


def run():
    p, _ = v.source()
    for a, b in combinations(p, 2):
        rational, radical = v.sq(a, b)
        v.need(norm(a, b) == (rational, 0, 0, radical), 'independent distance')
    cert = json.loads((v.HERE/'certificate.json').read_text())
    path = [tuple(row) for row in cert['path_points']]
    for flags in product((0, 1), repeat=4):
        q = [v.reflect(a) if f else a for a, f in zip(path, flags)]
        want = all(norm(a, b) == (1296, 0, 0, 0) for a, b in zip(q, q[1:]))
        v.need(v.preserves_path(path, flags)[0] == want, 'fold norm control')
    # A unit two-edge path whose middle point lies on the actual bisector
    # DOES admit an edge-preserving fold identifying the endpoints.
    positive = [(0, 0, 0, 0), (6, 0, 0, 6), (0, 0, 0, 12)]
    v.need(all(v.sq(a, b) == (1296, 0) for a, b in zip(positive, positive[1:])), 'positive unit path')
    v.need(v.difference(positive[1], positive[0], positive[2]) == (0, 0), 'positive on-axis middle')
    v.need(v.preserves_path(positive, (1, 0, 0)) == (True, True), 'positive collision')
    trials = []
    q = copy.deepcopy(cert); q['off_axis_unit_path'][1] = 2; trials.append(q)
    q = copy.deepcopy(cert); q['path_points'][1][0] += 1; trials.append(q)
    q = copy.deepcopy(cert); q['path_squared_distance_differences'][1] = [0, 0]; trials.append(q)
    q = copy.deepcopy(cert); q['source_sha256'] = '0'*64; trials.append(q)
    for q in trials:
        try:
            v.verify(q)
        except ValueError:
            continue
        raise ValueError('accepted corrupt evidence')
    return {'status': 'CONTROLS_PASS', 'independent_norm_vectors': 101025,
            'independent_fold_assignments': 16, 'positive_collision_control': True,
            'rejected_corruptions': len(trials)}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
