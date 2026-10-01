"""Solver-free whole-square reproduction of the partial-cell corner criterion.

Standard library only.  No import of a generator, SAT encoding, inventory,
center map, or earlier geometric checker.  Affine maps are derived from the
four vertices of each closed unit square.
"""
from collections import Counter, deque
from copy import deepcopy
from pathlib import Path
import hashlib
import itertools
import json

BASE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def point(raw):
    need(isinstance(raw, (list, tuple)) and len(raw) == 2
         and all(type(a) is int for a in raw), 'nonintegral point')
    return tuple(raw)


def cells(raw):
    result = set(map(point, raw))
    need(len(result) == len(raw), 'duplicate cell')
    return result


def frame(raw):
    need(isinstance(raw, (list, tuple)) and len(raw) == 2, 'invalid frame')
    m, t = raw
    need(len(m) == 2, 'invalid matrix')
    m = tuple(map(point, m))
    need(all(a in (-1, 0, 1) for row in m for a in row)
         and all(sum(abs(a) for a in row) == 1 for row in m)
         and all(sum(abs(m[i][j]) for i in range(2)) == 1 for j in range(2)),
         'matrix is not D4')
    return m, point(t)


def square(p, g):
    """Lower-left corner of the image, computed by all four vertex images."""
    m, t = g
    corners = [(p[0]+a, p[1]+b) for a, b in itertools.product((0, 1), repeat=2)]
    moved = [tuple(sum(m[i][j]*z[j] for j in range(2))+t[i]
                   for i in range(2)) for z in corners]
    return min(z[0] for z in moved), min(z[1] for z in moved)


def d4():
    result = []
    for perm in itertools.permutations(range(2)):
        for signs in itertools.product((-1, 1), repeat=2):
            result.append(tuple(tuple(signs[i] if j == perm[i] else 0
                                      for j in range(2)) for i in range(2)))
    return sorted(result)


IDENTITY = (((1, 0), (0, 1)), (0, 0))


def reference():
    rows = [[2, 3], [1, 2, 3, 4], [0, 1, 2, 3, 4], [2, 3, 4, 5], [3, 4]]
    base = {(2*x+a, 2*y+b) for y, row in enumerate(rows) for x in row
            for a, b in itertools.product((0, 1), repeat=2)}
    near = lambda s: {(x+a, y+b) for x, y in s
                      for a, b in itertools.product((-1, 0, 1), repeat=2)}
    return base, near(base), {p for p in base if near({p}) <= base}


def flood(s, start):
    seen, todo = {start} & s, deque({start} & s)
    while todo:
        x, y = todo.popleft()
        for p in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if p in s and p not in seen:
                seen.add(p)
                todo.append(p)
    return seen


def disc(s):
    need(s and flood(s, min(s)) == s, 'disconnected witness')
    x0, x1 = min(x for x, y in s)-1, max(x for x, y in s)+1
    y0, y1 = min(y for x, y in s)-1, max(y for x, y in s)+1
    empty = set(itertools.product(range(x0, x1+1), range(y0, y1+1)))-s
    need(flood(empty, (x0, y0)) == empty, 'witness hole')
    vertices = {(x+a, y+b) for x, y in s for a, b in itertools.product((0, 1), repeat=2)}
    for x, y in vertices:
        local = {(x-a, y-b) for a, b in itertools.product((0, 1), repeat=2)} & s
        need(not (len(local) == 2 and len({p[0] for p in local}) == 2
                  and len({p[1] for p in local}) == 2), 'witness diagonal pinch')
    return sum((x+a, y+b) not in s for x, y in s
               for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def normalized(s):
    a, b = min(x for x, y in s), min(y for x, y in s)
    return tuple(sorted((x-a, y-b) for x, y in s))


def positive_check(data, q, f, implied, old_frames):
    selected = cells(data['prototype_selected_cells'])
    literal = cells(data['cells'])
    need(data['candidate_id'] == 2101 and data['candidate_name'] == 'Q50'
         and len(selected) == len(literal) == data['area'] == 50, 'wrong positive identity')
    base, pool, core = reference()
    need(core <= selected <= pool and q <= selected and not selected & (f | implied),
         'positive fails the partial hypotheses')
    need(normalized(selected) == tuple(sorted(literal)), 'positive normalization differs')
    variants = sorted({normalized({square(p, (m, (0, 0))) for p in selected}) for m in d4()})
    need(normalized(base) not in variants, 'positive is congruent to the reference')
    old = [{square(p, g) for p in selected} for g in old_frames]
    need(not any(a & b for a, b in itertools.combinations(old, 2)), 'positive old copies overlap')
    offset = min(x for x, y in selected), min(y for x, y in selected)
    need(list(map(len, data['integral_prefix_layers'])) == [1, 6], 'wrong positive layer sizes')
    prefix, all_copies, areas, perimeters = set(), [], [], []
    for k, row in enumerate(data['integral_prefix_layers']):
        layer = []
        for code in row:
            need(len(code) == 3 and all(type(a) is int for a in code), 'bad positive pose')
            i, x, y = code
            need(0 <= i < len(variants), 'bad positive image')
            layer.append({(a+x, b+y) for a, b in variants[i]})
        need(not any(s & prefix for s in layer)
             and not any(a & b for a, b in itertools.combinations(layer, 2)), 'positive copies overlap')
        added = set().union(*layer)
        if not k:
            need(layer[0] == literal, 'positive root is not the stated prototype')
        if k:
            halo = {(x+a, y+b) for x, y in prefix
                    for a, b in itertools.product((-1, 0, 1), repeat=2)}-prefix
            need(halo <= added, 'positive first surround incomplete')
            old_vertices = {(x+a, y+b) for x, y in prefix
                            for a, b in itertools.product((0, 1), repeat=2)}
            need(all({(x+a, y+b) for x, y in s
                      for a, b in itertools.product((0, 1), repeat=2)} & old_vertices
                     for s in layer), 'positive copy misses preceding prefix')
        prefix |= added
        all_copies.extend(layer)
        areas.append(len(prefix))
        perimeters.append(disc(prefix))
    need(areas == data['prefix_cells'] == [50, 350], 'positive area differs')
    need(all({(x-offset[0], y-offset[1]) for x, y in s} in all_copies for s in old),
         'old pattern is absent from the positive first prefix')
    return {'areas': areas, 'perimeters': perimeters, 'D4_images': len(variants)}


def certify(data, root_context):
    need(data['reference_rows'] == [[2, 3], [1, 2, 3, 4], [0, 1, 2, 3, 4],
                                    [2, 3, 4, 5], [3, 4]], 'changed reference')
    base, pool, core = reference()
    extra = cells(data['additional_selected'])
    need(extra <= pool-core, 'invalid extra selected cells')
    q = core | extra
    f = cells(data['required_empty_root_context' if root_context else 'required_empty_two_copy'])
    need(f <= pool-q, 'invalid empty hypotheses')
    all_frames = list(map(frame, data['old_frames']))
    need(len(all_frames) == 3 and all_frames[0] == IDENTITY, 'missing compulsory identity root')
    old_frames = all_frames if root_context else all_frames[1:]
    old_maps = [{square(p, g): p for p in pool} for g in old_frames]
    old_required = [{square(p, g): p for p in q} for g in old_frames]
    need(not any(a.keys() & b.keys() for a, b in itertools.combinations(old_required, 2)),
         'mandatory old squares overlap')
    # Each derived absent cell has a whole-square collision with a compulsory
    # cell in another old copy, or a same-source collision between old copies.
    implied, packing_witnesses = set(), []
    if root_context:
        for p in sorted(pool):
            witnesses = []
            for i, j in itertools.permutations(range(len(old_frames)), 2):
                physical = square(p, old_frames[i])
                other = old_maps[j].get(physical)
                if other in q or other == p:
                    witnesses.append((i, j, other, physical))
            if witnesses:
                implied.add(p)
                packing_witnesses.append((p, min(witnesses)))
    need(not q & implied, 'mandatory selected cell is forced absent')
    vertex, gap = point(data['vertex']), point(data['gap_cell'])
    star = {(vertex[0]-a, vertex[1]-b) for a, b in itertools.product((0, 1), repeat=2)}
    need(gap in star and star & set().union(*(set(s) for s in old_required)) == star-{gap},
         'not three compulsory occupied quadrants')
    need(all(gap not in inv or inv[gap] in f | implied for inv in old_maps),
         'old copies can occupy the missing quadrant')
    counts, envelope, rejection_witnesses = Counter(), set(), []
    for matrix in d4():
        for source in sorted(pool):
            a, b = square(source, (matrix, (0, 0)))
            g = matrix, (gap[0]-a, gap[1]-b)
            need(square(source, g) == gap, 'wrong owner translation')
            record = (g, source)
            need(record not in envelope, 'duplicate owner pose')
            envelope.add(record)
            if source in f:
                rule, witness = 'explicit_empty_source', None
            elif source in implied:
                rule, witness = 'packing_implied_empty_source', None
            else:
                owner_required = {square(p, g): p for p in q}
                overlaps = [(physical, i, owner_required[physical], old[physical])
                            for i, old in enumerate(old_required)
                            for physical in owner_required.keys() & old.keys()]
                need(overlaps, 'owner not excluded by partial hypotheses')
                rule, witness = 'mandatory_new_old_collision', min(overlaps)
            counts[rule] += 1
            rejection_witnesses.append((g, source, rule, witness))
    need(len(envelope) == 8*len(pool), 'owner envelope incomplete')
    positive = positive_check(data['positive'], q, f, implied, old_frames)
    encode = lambda obj: json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()
    return {'root_context': root_context, 'reference_cells': len(base), 'pool': len(pool),
            'mandatory_core': len(core), 'extra_selected': len(extra), 'explicit_empty': len(f),
            'packing_implied_empty': len(implied), 'old_copies': len(old_frames),
            'vertex': vertex, 'gap_cell': gap, 'complete_D4_owner_envelope': len(envelope),
            'rejection_rules': dict(counts),
            'packing_witness_sha256': hashlib.sha256(encode(packing_witnesses)).hexdigest(),
            'owner_rejection_witness_sha256': hashlib.sha256(encode(rejection_witnesses)).hexdigest(),
            'unspecified_cell_bits': len(pool)-len(q)-len(f),
            'unspecified_after_packing': len(pool)-len(q)-len(f | implied),
            'constructor_cut_literals': len(extra)+len(f)+2,
            'nonvacuous_Q50_first_disc': positive}


def main():
    path = BASE/'data.json'
    data = json.loads(path.read_text())
    results = [certify(data, root_context=False), certify(data, root_context=True)]
    edits = [
        ('lose required selected cell', lambda d: d['additional_selected'].pop(0)),
        ('lose required empty cell', lambda d: d['required_empty_root_context'].pop(0)),
        ('wrong gap', lambda d: d.__setitem__('gap_cell', [1000, 1000])),
        ('missing identity root', lambda d: d['old_frames'].pop(0)),
        ('fractional frame', lambda d: d['old_frames'][1][1].__setitem__(0, -9.5)),
        ('changed reference', lambda d: d['reference_rows'][0].pop()),
        ('changed Q50 prototype', lambda d: d['positive']['prototype_selected_cells'].pop()),
        ('lost whole first copy', lambda d: d['positive']['integral_prefix_layers'][1].pop()),
        ('moved first copy', lambda d: d['positive']['integral_prefix_layers'][1][0].__setitem__(1, 1000)),
    ]
    controls = []
    for label, edit in edits:
        bad = deepcopy(data)
        edit(bad)
        try:
            certify(bad, root_context=True)
        except ValueError as e:
            controls.append({'control': label, 'status': 'rejected', 'reason': str(e)})
        else:
            raise ValueError('damaged instance accepted: '+label)
    benign = deepcopy(data)
    benign['additional_selected'].reverse()
    benign['required_empty_root_context'].reverse()
    benign['positive']['prototype_selected_cells'].reverse()
    need(certify(benign, root_context=True) == results[1], 'benign ordering changed the result')
    controls.append({'control': 'benign cell-order reversal', 'status': 'accepted'})
    print(json.dumps({'agent': 'six-heesch-1', 'role': 'researcher',
                      'data_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'results': results, 'controls': controls,
                      'conclusion': 'conditional all-real pattern obstruction; no global Heesch height or valid-prototype census',
                      'status': 'written geometric bridge plus exact author checks; unformalized/independently unreviewed'},
                     sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
