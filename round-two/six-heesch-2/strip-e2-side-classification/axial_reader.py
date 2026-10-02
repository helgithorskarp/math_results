"""Separate all-parameter replay using axial segments and determinants.

The coverage producer uses vertical UV columns. This reader solves axial
line intersections and eliminates array indices with a2x2 determinant.
It imports no producer geometry. The common mathematical six-segment model
and ordinary integer partition argument remain an unformalized trust boundary.
"""
import hashlib
import json

DIRS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
COLS = ((-2, (1, -1), (1, -1)), (-1, (1, 0), (1, 0)),
        (0, (0, 0), (1, 0)), (1, (0, 1), (1, 0)),
        (2, (0, 2), (1, 1)), (3, (0, 2), (1, 1)))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def freeze(x):
    return tuple(freeze(y) for y in x) if isinstance(x, (tuple, list)) else x


def sha(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def scale(n, a):
    return n*a[0], n*a[1]


def sub(a, b):
    return add(a, scale(-1, b))


def value(a, k):
    return a[0]*k+a[1]


def atom(kind, a, modulus=None):
    if kind == 'mod' and a[0] % modulus == 0:
        return a[1] % modulus == 0
    if a[0] == 0:
        return a[1] >= 0 if kind == 'ge' else a[1] == 0
    return (kind, *a) if modulus is None else (kind, *a, modulus)


def both(*rows):
    if False in rows:
        return False
    rest = tuple(x for x in rows if x is not True)
    return True if not rest else rest[0] if len(rest) == 1 else ('and', *rest)


def either(*rows):
    if True in rows:
        return True
    rest = tuple(x for x in rows if x is not False)
    return False if not rest else rest[0] if len(rest) == 1 else ('or', *rest)


def neg(x):
    return not x if type(x) is bool else ('not', x)


def evaluate(row, k):
    if type(row) is bool:
        return row
    if row[0] == 'and':
        return all(evaluate(x, k) for x in row[1:])
    if row[0] == 'or':
        return any(evaluate(x, k) for x in row[1:])
    if row[0] == 'not':
        return not evaluate(row[1], k)
    n = row[1]*k+row[2]
    return n >= 0 if row[0] == 'ge' else n == 0 if row[0] == 'eq' else n % row[3] == 0


def partition(rows, minimum):
    atoms = set()
    stack = list(rows)
    while stack:
        row = stack.pop()
        if type(row) is bool:
            continue
        if row[0] in ('and', 'or', 'not'):
            stack.extend(row[1:])
        else:
            atoms.add(row)
    breaks, period = {minimum}, 1
    for kind, A, B, *rest in atoms:
        if kind == 'mod':
            require(rest == [3], 'Unexpected axial partition modulus')
            period = 3
        elif kind == 'eq':
            root, remainder = divmod(-B, A)
            if remainder == 0 and root >= minimum:
                breaks.update((root, root+1))
        else:
            require(kind == 'ge', 'Unknown axial partition predicate')
            first = (-B+A-1)//A if A > 0 else B//(-A)+1
            if first > minimum:
                breaks.add(first)
    cuts = sorted(breaks)
    intervals, samples = [], []
    for j, lo in enumerate(cuts):
        hi = cuts[j+1]-1 if j+1 < len(cuts) else None
        reps = [lo+(r-lo)%period for r in range(period)]
        reps = [k for k in reps if hi is None or k <= hi]
        intervals.append({'lo': lo, 'hi': hi, 'representatives': reps})
        samples.extend(reps)
    return {'minimum': minimum, 'period': period, 'cuts': cuts, 'intervals': intervals,
            'representatives': samples, 'atomic_predicates': len(atoms)}


def possible(row, minimum, guard):
    if type(row) is bool:
        return row
    for k in partition([row], minimum)['representatives']:
        guard()
        if evaluate(row, k):
            return True
    return False


def matrices():
    return tuple((DIRS[r][0], DIRS[(r+s) % 6][0], DIRS[r][1], DIRS[(r+s) % 6][1])
                 for s in (1, -1) for r in range(6))


def axial(g):
    (a, b, c, d), U, V = freeze(g)
    m = a-2*c, 2*a+b-4*c-2*d, c, 2*c+d
    require(m in matrices(), 'Non-D6 positive-copy pose')
    require(all(type(x) is int for pair in (U, V) for x in pair), 'Noninteger affine translation')
    return m, sub(U, scale(2, V)), V


def col_base(g, column):
    (a, b, c, d), X, Y = g
    return (add(X, (0, a*column)), add(Y, (0, c*column))), (-2*a+b, -2*c+d)


def shifted(g, step):
    m, X, Y = g
    return m, add(X, (0, step[0])), add(Y, (0, step[1]))


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def cross_affine(a, b):
    return sub(scale(b[1], a[0]), scale(b[0], a[1]))


def line_intervals(anchor, column, copies, columns, minimum, guard):
    P, q = col_base(anchor, column)
    out = []
    for number, copy in enumerate(copies):
        for source, lo, hi in columns:
            guard()
            B, r = col_base(copy, source)
            diff = sub(B[0], P[0]), sub(B[1], P[1])
            determinant = cross(q, r)
            if determinant == 0:
                require(r == q or r == (-q[0], -q[1]), 'Nonunit parallel line parameter')
                component = next(i for i in (0, 1) if abs(q[i]) == 1)
                offset = scale(q[component], diff[component])
                sign = 1 if q == r else -1
                low, high = (lo, hi) if sign == 1 else (hi, lo)
                low, high = add(offset, scale(sign, low)), add(offset, scale(sign, high))
                active = atom('eq', cross_affine(diff, q))
                start, stop = scale(3, low), scale(3, add(high, (0, 1)))
            else:
                require(abs(determinant) == 3, 'Unexpected axial line determinant')
                sign = 1 if determinant > 0 else -1
                target = scale(sign, cross_affine(diff, r))
                source_height = scale(sign, cross_affine(diff, q))
                active = both(atom('mod', target, 3), atom('mod', source_height, 3),
                              atom('ge', sub(source_height, scale(3, lo))),
                              atom('ge', sub(scale(3, hi), source_height)))
                start, stop = target, add(target, (0, 3))
            if possible(active, minimum, guard):
                out.append({'copy': number, 'source_column': source,
                            'lo': start, 'hi': stop, 'active': active})
    return out


def overlap(first, second, columns, minimum, guard):
    rows = []
    for column, lo, hi in columns:
        bottom, stop = scale(3, lo), scale(3, add(hi, (0, 1)))
        for s in line_intervals(first, column, (second,), columns, minimum, guard):
            rows.append(both(s['active'], atom('ge', sub(sub(s['hi'], bottom), (0, 1))),
                             atom('ge', sub(sub(stop, s['lo']), (0, 1)))))
    return either(*rows)


def touching(first, second, columns, minimum, guard):
    return either(*(overlap(shifted(first, d), second, columns, minimum, guard) for d in DIRS))


def endpoint_rows(lines):
    rows = []
    for line in lines:
        ends = {line['lo'], line['hi']}
        for s in line['segments']:
            rows.append(s['active'])
            ends.update(s['lo'])
            ends.update(s['hi'])
        ends = sorted(ends)
        for j, a in enumerate(ends):
            for b in ends[:j]:
                rows.extend((atom('ge', sub(a, b)), atom('ge', sub(b, a))))
    return rows


def covered(line, k):
    low, high = value(line['lo'], k), value(line['hi'], k)
    intervals = [(max(value(x, k) for x in s['lo']), min(value(x, k) for x in s['hi']))
                 for s in line['segments'] if evaluate(s['active'], k)]
    # Sweep clipped endpoint events, separate from the producer cursor merge.
    events = {}
    for a, b in intervals:
        a, b = max(a, low), min(b, high)
        if a < b:
            events[a] = events.get(a, 0)+1
            events[b] = events.get(b, 0)-1
    events.setdefault(low, 0)
    events.setdefault(high, 0)
    level = 0
    ordered = sorted(events)
    for a, b in zip(ordered, ordered[1:]):
        level += events[a]
        if low <= a < b <= high and level <= 0:
            return False
    return True


def check_constant(fixed, surround, guard):
    fixed, surround = freeze(fixed), freeze(surround)
    require(len(set((*fixed, *surround))) == len(fixed)+len(surround), 'Duplicate constant affine copy')
    copies = tuple(axial(g) for g in (*fixed, *surround))
    packing = [neg(overlap(a, b, COLS, 6, guard))
               for j, b in enumerate(copies) for a in copies[:j]]
    lines = []
    for j, g in enumerate(copies[:len(fixed)]):
        for step in ((0, 0), *DIRS):
            for column, lo, hi in COLS:
                items = line_intervals(shifted(g, step), column, copies, COLS, 6, guard)
                lines.append({'fixed_copy': j, 'shift': step, 'column': column,
                    'lo': scale(3, lo), 'hi': scale(3, add(hi, (0, 1))),
                    'segments': [{'lo': [s['lo']], 'hi': [s['hi']], 'active': s['active']} for s in items]})
    part = partition([*packing, *endpoint_rows(lines)], 6)
    for k in part['representatives']:
        guard()
        require(all(evaluate(row, k) for row in packing), 'Axial constant pattern overlaps')
        require(all(covered(line, k) for line in lines), 'Axial constant pattern misses halo')
    return {'surround_copies': len(surround), 'traces': len(lines), 'partition': part,
            'trace_sha256': sha(lines), 'checked_all_k': True}


def substitute(x, residue):
    return 2*x[0], residue*x[0]+x[1]


def height_range(lo, hi, parity):
    require(lo[0] % 2 == hi[0] % 2 == 0, 'Axial height slope is not even')
    return (lo[0]//2, -((parity-lo[1])//2)), (hi[0]//2, (hi[1]-parity)//2+1)


def split_finite(segments, parity):
    out = []
    for s in segments:
        L, H = s['lo'], s['hi']
        require(L[0] % 6 == H[0] % 6 == 0 and L[1] % 3 == H[1] % 3 == 0,
                'Axial finite segment has fractional affine height')
        low, high = (L[0]//3, L[1]//3), (H[0]//3, H[1]//3-1)
        low, high = height_range(low, high, parity)
        out.append({'lo': [low], 'hi': [high], 'active': s['active']})
    return out


def constrained(A, B, coefficient, L, H):
    base = A, B
    if coefficient == 0:
        return [], [], both(atom('ge', sub(base, L)), atom('ge', sub(H, base)))
    if coefficient < 0:
        coefficient, base, L, H = -coefficient, scale(-1, base), scale(-1, H), scale(-1, L)
    low, high = sub(L, base), sub(H, base)
    require(low[0] % coefficient == high[0] % coefficient == 0, 'Nonaffine integer array bound')
    return [(low[0]//coefficient, -((-low[1])//coefficient))], \
           [(high[0]//coefficient, high[1]//coefficient+1)], True


def array_ranges(anchor, column, parity, residue, columns, guard):
    P, q = col_base(anchor, column)
    step, ray = (2, 2), (2, -1)
    require(cross(step, ray) == -6, 'Changed array determinant')
    out = []
    for source, lo, hi in columns:
        guard()
        B = (-4, -2*residue-source), (2, residue+6)
        diff = sub(P[0], B[0]), sub(P[1], B[1])
        index = scale(-1, cross_affine(diff, ray))
        height = cross_affine(diff, step)
        index_t, height_t = -cross(q, ray), -cross(step, q)
        require(index[0] % 6 == height[0] % 6 == 0 and index_t % 3 == height_t % 3 == 0,
                'Array determinant elimination has nonaffine residue slopes')
        if (index[1]+index_t*parity) % 6 or (height[1]+height_t*parity) % 6:
            continue
        JA, JB, JC = index[0]//6, (index[1]+index_t*parity)//6, index_t//3
        SA, SB, SC = height[0]//6, (height[1]+height_t*parity)//6, height_t//3
        jlo, jhi, jactive = constrained(JA, JB, JC, (0, 0), (1, residue-2))
        slo, shi, sactive = constrained(SA, SB, SC, lo, hi)
        active = both(jactive, sactive)
        if possible(active, 3, guard):
            require(jlo or slo, 'Unbounded axial array interval')
            require(jhi or shi, 'Unbounded axial array interval')
            out.append({'lo': [*jlo, *slo], 'hi': [*jhi, *shi], 'active': active})
    return out


def check_array(record, guard):
    results = []
    for residue in (0, 1):
        fixed_uv = freeze(record['fixed'])
        caps_uv = freeze(record['even_caps' if residue == 0 else 'odd_caps'])
        columns = tuple((c, substitute(lo, residue), substitute(hi, residue)) for c, lo, hi in COLS)
        uv = [(m, substitute(U, residue), substitute(V, residue)) for m, U, V in (*fixed_uv, *caps_uv)]
        copies = tuple(axial(g) for g in uv)
        packing = [neg(overlap(a, b, columns, 3, guard))
                   for j, b in enumerate(copies) for a in copies[:j]]
        for g in copies:
            for column, lo, hi in columns:
                for parity in (0, 1):
                    L, H = height_range(lo, hi, parity)
                    for s in array_ranges(g, column, parity, residue, columns, guard):
                        lower, upper = [L, *s['lo']], [H, *s['hi']]
                        packing.append(neg(both(s['active'], *(atom('ge', sub(sub(h, l), (0, 1)))
                                                              for l in lower for h in upper))))
        # Array u-extent is12+6j+[-3,2], hence distinct indices do not overlap.
        require(max(-c for c, _, _ in columns)-min(-c for c, _, _ in columns) < 6,
                'Array transverse extents do not separate')
        lines = []
        for j, g in enumerate(copies[:len(fixed_uv)]):
            for step in ((0, 0), *DIRS):
                anchor = shifted(g, step)
                for column, lo, hi in columns:
                    finite = line_intervals(anchor, column, copies, columns, 3, guard)
                    for parity in (0, 1):
                        L, H = height_range(lo, hi, parity)
                        items = split_finite(finite, parity)+array_ranges(anchor, column, parity, residue, columns, guard)
                        lines.append({'fixed_copy': j, 'shift': step, 'column': column, 'parity': parity,
                                      'lo': L, 'hi': H, 'segments': items})
        part = partition([*packing, *endpoint_rows(lines)], 3)
        for n in part['representatives']:
            guard()
            require(all(evaluate(row, n) for row in packing), 'Axial repeated cover overlaps')
            require(all(covered(line, n) for line in lines), 'Axial repeated cover misses halo')
        results.append({'k_residue': residue, 'caps': len(caps_uv), 'traces': len(lines),
                        'partition': part, 'trace_sha256': sha(lines)})
    return {'checked_all_k': True, 'parity_classes': results}


def inverse(g):
    (a, b, c, d), U, V = freeze(g)
    det = a*d-b*c
    require(det in (-1, 1), 'Nonrigid inverse')
    m = d*det, -b*det, -c*det, a*det
    return m, scale(-1, add(scale(m[0], U), scale(m[1], V))), \
           scale(-1, add(scale(m[2], U), scale(m[3], V)))


def compose(g, h):
    (a, b, c, d), U, V = freeze(g)
    (e, f, j, l), X, Y = freeze(h)
    return (a*e+b*j, a*f+b*l, c*e+d*j, c*f+d*l), \
           add(U, add(scale(a, X), scale(b, Y))), add(V, add(scale(c, X), scale(d, Y)))


def contact_types(fixed, surround, expected_types, guard):
    uv = freeze((*fixed, *surround))
    copies = tuple(axial(g) for g in uv)
    rows = {(i, j): touching(a, b, COLS, 6, guard)
            for j, b in enumerate(copies) for i, a in enumerate(copies[:j])}
    part = partition(list(rows.values()), 6)
    expected_types = set(freeze(expected_types))
    actual, pairs = set(), set()
    for k in part['representatives']:
        guard()
        for (i, j), row in rows.items():
            if evaluate(row, k):
                rel = compose(inverse(uv[i]), uv[j])
                canonical = min(rel, inverse(rel))
                require(canonical in expected_types, 'Unproved touching E1 type in E2 pattern')
                actual.add(canonical)
                pairs.add((i, j))
    require(actual == expected_types, 'Changed E1 contact inventory')
    return {'touching_pairs': sorted(pairs), 'types': sorted(actual), 'partition': part}
