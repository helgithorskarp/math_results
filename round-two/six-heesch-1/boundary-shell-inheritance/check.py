"""Exact, standalone reader for a balanced shell-edit inheritance reduction.

The proof handles arbitrary edit cardinality. This reader checks its three
literal parent tilings and group hypotheses, and exercises the conclusion on
every one-cell shell edit and several multi-cell controls. No solver is used.
Affine motions act on integer lower-left cell indices, not polygon vertices.
"""
from collections import deque
from copy import deepcopy
from itertools import combinations, product
import json
from pathlib import Path
import sys

IDENTITY = (1, 0, 0, 1, 0, 0)
FOUR = ((1, 0), (-1, 0), (0, 1), (0, -1))
D4 = tuple((a, b, c, d) for a, b, c, d in product((-1, 0, 1), repeat=4)
           if a*a+b*b == c*c+d*d == 1 and a*c+b*d == 0)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def integer_tuple(raw, length, message):
    require(isinstance(raw, (list, tuple)) and len(raw) == length
            and all(type(x) is int for x in raw), message)
    return tuple(raw)


def cells(raw):
    require(isinstance(raw, (list, tuple)) and raw, 'empty/invalid cells')
    result = [integer_tuple(p, 2, 'invalid cell') for p in raw]
    require(len(result) == len(set(result)), 'duplicate cell')
    return frozenset(result)


def motion(raw):
    g = integer_tuple(raw, 6, 'invalid motion')
    require(g[:4] in D4, 'linear part is not a square-grid isometry')
    return g


def act(g, p):
    a, b, c, d, tx, ty = g
    x, y = p
    return a*x+b*y+tx, c*x+d*y+ty


def compose(g, h):
    a, b, c, d, tx, ty = g
    e, f, k, l, ux, uy = h
    return (a*e+b*k, a*f+b*l, c*e+d*k, c*f+d*l,
            a*ux+b*uy+tx, c*ux+d*uy+ty)


def inverse(g):
    a, b, c, d, tx, ty = g
    return a, c, b, d, -a*tx-c*ty, -b*tx-d*ty


def footprint(g, prototype):
    return frozenset(act(g, p) for p in prototype)


def normalized(prototype):
    xmin = min(x for x, y in prototype)
    ymin = min(y for x, y in prototype)
    return tuple(sorted((x-xmin, y-ymin) for x, y in prototype))


def halo(prototype):
    return {(x+dx, y+dy) for x, y in prototype
            for dx, dy in product((-1, 0, 1), repeat=2)} - set(prototype)


def flood(domain, start):
    visited = {start}
    todo = deque([start])
    while todo:
        x, y = todo.popleft()
        for dx, dy in FOUR:
            q = x+dx, y+dy
            if q in domain and q not in visited:
                visited.add(q)
                todo.append(q)
    return visited


def disc(prototype):
    if not prototype or flood(prototype, min(prototype)) != set(prototype):
        return False
    vertices = {(x+dx, y+dy) for x, y in prototype
                for dx, dy in product((0, 1), repeat=2)}
    for x, y in vertices:
        bits = [(x+dx, y+dy) in prototype
                for dx, dy in ((0, 0), (-1, 0), (-1, -1), (0, -1))]
        if sum(bits) == 2 and bits[0] == bits[2]:
            return False
    xmin, xmax = min(x for x, y in prototype)-1, max(x for x, y in prototype)+1
    ymin, ymax = min(y for x, y in prototype)-1, max(y for x, y in prototype)+1
    empty = {(x, y) for x in range(xmin, xmax+1)
             for y in range(ymin, ymax+1)} - set(prototype)
    return flood(empty, (xmin, ymin)) == empty


def packing(prototype, motions):
    occupied = set()
    for g in motions:
        image = footprint(g, prototype)
        if occupied & image:
            return False
        occupied.update(image)
    return True


class Quotient:
    def __init__(self, periods):
        require(isinstance(periods, (list, tuple)) and len(periods) == 2,
                'two lattice periods required')
        self.u, self.v = [integer_tuple(p, 2, 'invalid period') for p in periods]
        a, b = self.u
        c, d = self.v
        self.det = abs(a*d-b*c)
        require(0 < self.det <= 256, 'degenerate/oversized literal quotient')
        self.classes = {self.residue((x, y)) for x in range(self.det)
                        for y in range(self.det)}
        require(len(self.classes) == self.det, 'incorrect quotient index')

    def residue(self, p):
        a, b = self.u
        c, d = self.v
        x, y = p
        return (d*x-c*y) % self.det, (-b*x+a*y) % self.det

    def key(self, g):
        return g[:4] + self.residue(g[4:])

    def periodic(self, prototype, reps):
        owners = []
        for g in reps:
            owners.extend(self.residue(p) for p in footprint(g, prototype))
        require(len(owners) == self.det and len(set(owners)) == self.det
                and set(owners) == self.classes, 'periodic cell partition fails')
        return {'area': len(prototype), 'fundamental_copies': len(reps),
                'determinant': self.det, 'distinct_residues': len(set(owners))}

    def automorphism(self, g, reps):
        linear = g[:4] + (0, 0)
        require(all(self.residue(act(linear, p)) == (0, 0)
                    for p in (self.u, self.v)), 'motion does not normalize lattice')
        # Inclusion and equal covolume give M(L)=L, since det(M)=+/-1.
        expected = {self.key(h) for h in reps}
        actual = {self.key(compose(g, h)) for h in reps}
        require(actual == expected and len(actual) == len(reps),
                'motion does not permute fundamental motion classes')


def stretch(base, parameters):
    axis, band, extra = integer_tuple(parameters, 3, 'invalid stretch')
    require(axis in (0, 1) and extra > 0, 'invalid stretch parameters')
    result = set()
    for p in base:
        q = list(p)
        if p[axis] > band:
            q[axis] += extra
            result.add(tuple(q))
        elif p[axis] == band:
            for offset in range(extra+1):
                q[axis] = band+offset
                result.add(tuple(q))
        else:
            result.add(p)
    return frozenset(normalized(result))


def validate_parent(record, base):
    prototype = cells(record['cells'])
    require(prototype == stretch(base, record['stretch']), 'parent provenance mismatch')
    require(disc(prototype), 'parent is not a topological disc')
    require(len({normalized(footprint(m+(0, 0), prototype)) for m in D4}) == 8,
            'parent is not asymmetric')
    reps = [motion(g) for g in record['fundamental_motions']]
    neighbors = [motion(g) for g in record['neighbor_motions']]
    quotient = Quotient(record['periods'])
    require(IDENTITY in reps and len(set(reps)) == len(reps),
            'identity/unique representatives required')
    require(len({quotient.key(g) for g in reps}) == len(reps),
            'duplicate fundamental motion class')
    audit = quotient.periodic(prototype, reps)
    # These finite permutations certify that H={translation_l o r} is a group.
    for g in reps:
        quotient.automorphism(g, reps)
    require(IDENTITY not in neighbors and len(set(neighbors)) == len(neighbors),
            'invalid neighbor inventory')
    require({inverse(g) for g in neighbors} == set(neighbors),
            'neighbor inventory is not inverse closed')
    all_motions = [IDENTITY] + neighbors
    require(packing(prototype, all_motions), 'old star overlaps')
    occupied = set(prototype)
    for g in neighbors:
        require(quotient.key(g) in {quotient.key(h) for h in reps},
                'neighbor does not belong to the certified group')
        quotient.automorphism(g, reps)
        image = footprint(g, prototype)
        require(image & halo(prototype), 'listed tile is not a neighbor')
        occupied.update(image)
    require(halo(prototype) <= occupied, 'incomplete old neighbor inventory')
    return prototype, reps, neighbors, quotient, audit


def inherited_edit(prototype, reps, neighbors, quotient, removed, added):
    removed, added = frozenset(removed), frozenset(added)
    require(removed <= prototype and added <= halo(prototype)
            and len(removed) == len(added), 'not a balanced shell edit')
    changed = (prototype-removed) | added
    if not packing(changed, [IDENTITY]+neighbors):
        return None
    preimages = []
    for v in sorted(added):
        owners = [g for g in neighbors if v in footprint(g, prototype)]
        require(len(owners) == 1, 'added cell does not have a unique old owner')
        w = act(inverse(owners[0]), v)
        require(w in removed, 'removed-cell necessity fails')
        preimages.append(w)
    require(len(set(preimages)) == len(removed), 'injection/bijection fails')
    # Independent finite quotient check, in addition to replaying the bijection.
    quotient.periodic(changed, reps)
    return changed


def reject(call, name):
    try:
        call()
    except ValueError:
        return name
    raise ValueError('negative control accepted: '+name)


def run(data):
    base = cells(data['base_cells'])
    require(len(data['parents']) == 3 and {r['case'] for r in data['parents']} == {2, 9, 22},
            'wrong parent set')
    summaries = []
    two_cell_controls = []
    many_cell_controls = []
    validated = {}
    for record in data['parents']:
        prototype, reps, neighbors, quotient, audit = validate_parent(record, base)
        validated[record['case']] = prototype, reps, neighbors, quotient
        require(inherited_edit(prototype, reps, neighbors, quotient, [], []) == prototype,
                'empty edit control failed')
        moves = []
        rejected = 0
        accepted_disc = 0
        for u in sorted(prototype):
            for v in sorted(halo(prototype)):
                changed = inherited_edit(prototype, reps, neighbors, quotient, [u], [v])
                if changed is None:
                    rejected += 1
                else:
                    moves.append((u, v))
                    accepted_disc += bool(disc(changed))
        # Deterministic positive multi-cell control, not a multi-cell census.
        example = None
        for (u, v), (w, z) in combinations(moves, 2):
            if u == w or v == z:
                continue
            changed = inherited_edit(prototype, reps, neighbors, quotient, [u, w], [v, z])
            if changed is not None and disc(changed):
                example = {'case': record['case'], 'removed': [u, w], 'added': [v, z]}
                break
        require(example is not None, 'missing two-cell positive control')
        two_cell_controls.append(example)
        by_preimage = {}
        for v in sorted(halo(prototype)):
            owner = next(g for g in neighbors if v in footprint(g, prototype))
            by_preimage.setdefault(act(inverse(owner), v), []).append(v)
        many_removed = sorted(by_preimage)
        many_added = [by_preimage[w][0] for w in many_removed]
        many = inherited_edit(prototype, reps, neighbors, quotient, many_removed, many_added)
        require(many is not None and len(many_removed) > 2, 'many-cell control failed')
        many_cell_controls.append({'case': record['case'], 'cardinality': len(many_removed),
                                   'disc': disc(many)})
        summaries.append(dict(case=record['case'], **audit,
                              neighbors=len(neighbors), shell_cells=len(halo(prototype)),
                              single_edits_checked=len(prototype)*len(halo(prototype)),
                              single_edits_packing=len(moves), single_edits_disc=accepted_disc,
                              single_edits_rejected=rejected))

    example = data['changed_motion_example']
    prototype, reps, neighbors, quotient = validated[example['parent_case']]
    removed, added = cells(example['removed']), cells(example['added'])
    require(removed <= prototype and added <= halo(prototype) and len(removed) == len(added),
            'scope control is not a balanced shell edit')
    changed = (prototype-removed) | added
    require(normalized(changed) == normalized(cells(example['cells'])),
            'changed-motion example does not match edit')
    require(disc(changed) and not packing(changed, [IDENTITY]+neighbors),
            'scope control should break the old star while remaining a disc')
    separate = Quotient(example['periods'])
    different_tiling = separate.periodic(cells(example['cells']),
                                        [motion(g) for g in example['fundamental_motions']])

    controls = []
    original = data['parents'][0]
    bad = deepcopy(original)
    missing = motion(bad['neighbor_motions'][0])
    bad['neighbor_motions'] = [g for g in bad['neighbor_motions']
                               if motion(g) not in {missing, inverse(missing)}]
    controls.append(reject(lambda: validate_parent(bad, base), 'missing_neighbor'))
    bad = deepcopy(original)
    bad['fundamental_motions'].append(bad['fundamental_motions'][0])
    controls.append(reject(lambda: validate_parent(bad, base), 'duplicate_fundamental_copy'))
    bad = deepcopy(original)
    bad['periods'][0][0] += 1
    controls.append(reject(lambda: validate_parent(bad, base), 'wrong_lattice_period'))
    controls.append(reject(lambda: motion([1, 1, 0, 1, 0, 0]), 'nonisometric_shear'))
    controls.append(reject(lambda: cells([[0, 0], [0, 0]]), 'duplicate_cell'))
    p, rs, ns, q = validated[2]
    controls.append(reject(lambda: inherited_edit(p, rs, ns, q, [min(p)], []),
                           'unbalanced_edit'))
    controls.append(reject(lambda: inherited_edit(p, rs, ns, q, [min(p)], [(100, 100)]),
                           'outside_shell_edit'))
    # Exercise the inverse-neighbor part of the argument with two additions
    # having the same preimage in the prototype, and a balanced removal set.
    by_preimage = {}
    for v in sorted(halo(p)):
        owner = next(g for g in ns if v in footprint(g, p))
        by_preimage.setdefault(act(inverse(owner), v), []).append(v)
    duplicate = next((w, vs[:2]) for w, vs in sorted(by_preimage.items()) if len(vs) >= 2)
    w, vs = duplicate
    second = min(p-{w})
    require(inherited_edit(p, rs, ns, q, [w, second], vs) is None,
            'duplicate-preimage edit should fail star packing')
    controls.append('duplicate_preimage_overlap')
    return {'agent': 'six-heesch-1', 'role': 'researcher',
            'parents': summaries, 'two_cell_disc_controls': two_cell_controls,
            'many_cell_partition_controls': many_cell_controls,
            'changed_motion_scope_control': different_tiling,
            'negative_controls': controls,
            'proof_scope': 'Arbitrary-cardinality balanced shell edits preserving the old star packing tile by the same certified group; no finite Heesch record.'}


if __name__ == '__main__':
    require(len(sys.argv) <= 2, 'usage: python3 check.py [input.json]')
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).with_name('input.json')
    print(json.dumps(run(json.loads(path.read_text())), indent=2, sort_keys=True))
