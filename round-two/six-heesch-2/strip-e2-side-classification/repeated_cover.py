"""Exact parity-separated E1 cover with a variable number of array copies.

For k=2n+r, n>=3, 0<=r<=1, the array is (-I;12+6j,k+6+2j),
0<=j<=n-2+r. On each prototype line, source-column alignment eliminates j.
Splitting the line height into its two parity classes yields affine interval
bounds in n. Thus packing and coverage require only exact 1D order cuts.
"""
import deps
import strip_contact_reader as R
import strip_parametric_geometry as G
from strip_columns import require
import uv_cover as P


def substitute(x, residue):
    return 2*x[0], residue*x[0]+x[1]


def pose_substitute(g, residue):
    return g[0], substitute(g[1], residue), substitute(g[2], residue)


def columns_substitute(residue):
    return tuple((c, substitute(lo, residue), substitute(hi, residue)) for c, lo, hi in G.COLS)


def splitter(rows, minimum=3):
    atoms = set()
    todo = list(rows)
    while todo:
        row = todo.pop()
        if type(row) is bool:
            continue
        if row[0] in ('and', 'or', 'not'):
            todo.extend(row[1:])
        else:
            atoms.add(row)
    cuts = {minimum}
    period = 1
    for kind, A, B, *rest in atoms:
        if kind == 'mod':
            require(rest == [3], 'Unexpected partition modulus')
            period = 3
        elif kind == 'ge':
            cut = (-B+A-1)//A if A > 0 else B//(-A)+1
            if cut > minimum:
                cuts.add(cut)
        elif kind == 'eq':
            root, remainder = divmod(-B, A)
            if remainder == 0 and root >= minimum:
                cuts.update((root, root+1))
        else:
            raise ValueError('Unknown partition atom')
    intervals = []
    representatives = []
    cuts = sorted(cuts)
    for j, lo in enumerate(cuts):
        hi = cuts[j+1]-1 if j+1 < len(cuts) else None
        samples = [lo+(r-lo)%period for r in range(period)]
        samples = [n for n in samples if hi is None or n <= hi]
        intervals.append({'lo': lo, 'hi': hi, 'representatives': samples})
        representatives.extend(samples)
    return {'minimum': minimum, 'period': period, 'cuts': cuts, 'intervals': intervals,
            'representatives': representatives, 'atomic_predicates': len(atoms)}


def height_range(lo, hi, parity):
    require(lo[0] % 2 == hi[0] % 2 == 0, 'Nonintegral height residue endpoints')
    return (lo[0]//2, (lo[1]-parity+1)//2), (hi[0]//2, (hi[1]-parity)//2+1)


def finite_ranges(segments, parity):
    out = []
    for s in segments:
        lo, stop = s['lo'], s['hi']
        require(lo[0] % 6 == stop[0] % 6 == 0 and lo[1] % 3 == stop[1] % 3 == 0,
                'Finite line intersection is not an integer affine height')
        low = lo[0]//3, lo[1]//3
        high = stop[0]//3, stop[1]//3-1
        L, H = height_range(low, high, parity)
        out.append({'lo': [L], 'hi': [H], 'active': s['active']})
    return out


def array_ranges(anchor, column, parity, residue, guard):
    (a, b, c, d), U, V = anchor
    require(U[0] % 6 == 0 and V[0] % 2 == 0 and b in (0, -3, 3),
            'Array elimination assumptions fail')
    out = []
    for z, source_lo, source_hi in columns_substitute(residue):
        guard()
        Q = a*column+U[1]+z-12
        YA = 6+U[0]-3*V[0]
        YB = 3*residue+(a-3*c)*column+U[1]-3*V[1]+z+6
        if Q % 3 or YB % 3:
            continue
        require(YA % 6 == 0, 'Odd array source-height slope')
        Y = YA//3, YB//3
        coefficient = b//3-d
        require(coefficient in (-1, 0, 1), 'Unexpected array source-height direction')
        lower, upper = [], []
        active = True
        if b == 0:
            if Q % 6:
                continue
            J = U[0]//6, Q//6
            active = G.both(G.atom('ge', J), G.atom('ge', G.sub((1, -2+residue), J)))
        else:
            if (b*parity+Q) % 6:
                continue
            if b > 0:
                lower.append((-U[0]//3, -Q//3))
                upper.append(((6-U[0])//3, (-12+6*residue-Q)//3))
            else:
                lower.append(((U[0]-6)//3, (Q+12-6*residue)//3))
                upper.append((U[0]//3, Q//3))
        if coefficient == 0:
            active = G.both(active, G.atom('ge', G.sub(Y, source_lo)),
                            G.atom('ge', G.sub(source_hi, Y)))
        elif coefficient > 0:
            lower.append(G.sub(source_lo, Y))
            upper.append(G.sub(source_hi, Y))
        else:
            lower.append(G.sub(Y, source_hi))
            upper.append(G.sub(Y, source_lo))
        require(lower and upper, 'Unbounded array trace')
        if not P.globally_possible(active, guard, 3):
            continue
        lows = [height_range(x, x, parity)[0] for x in lower]
        highs = [height_range(x, x, parity)[1] for x in upper]
        out.append({'lo': lows, 'hi': highs, 'active': active})
    return out


def endpoint_formulas(lines):
    rows = []
    for line in lines:
        ends = {line['lo'], line['hi']}
        for s in line['segments']:
            rows.append(s['active'])
            ends.update(s['lo'])
            ends.update(s['hi'])
        ends = sorted(ends)
        for j, x in enumerate(ends):
            for y in ends[:j]:
                rows.extend((G.atom('ge', G.sub(x, y)), G.atom('ge', G.sub(y, x))))
    return rows


def segments_at(segments, n):
    return [(max(G.value(x, n) for x in s['lo']), min(G.value(x, n) for x in s['hi']))
            for s in segments if G.evaluate(s['active'], n)]


def covered(line, n):
    cursor, stop = G.value(line['lo'], n), G.value(line['hi'], n)
    for lo, hi in sorted(segments_at(line['segments'], n)):
        if lo >= hi or hi <= cursor:
            continue
        if lo > cursor:
            break
        cursor = max(cursor, hi)
        if cursor >= stop:
            return True
    return cursor >= stop


def intersection(g, columns):
    (a, b, c, d), U, V = g
    rows = []
    for x, lo, hi in columns:
        for z, L, H in columns:
            if b == 0:
                low, high = (lo, hi) if d == 1 else (hi, lo)
                low = G.add(G.add(G.constant(c*x), V), G.scale(d, low))
                high = G.add(G.add(G.constant(c*x), V), G.scale(d, high))
                rows.append(G.both(G.atom('eq', G.add(U, G.constant(a*x-z))),
                                   G.atom('ge', G.sub(H, low)), G.atom('ge', G.sub(high, L))))
            else:
                numerator = G.scale(1 if b > 0 else -1, G.sub(G.constant(z-a*x), U))
                height = G.add(G.scale(3, G.add(G.constant(c*x), V)), G.scale(d, numerator))
                rows.append(G.both(G.atom('mod', numerator, 3), G.atom('ge', G.sub(numerator, G.scale(3, lo))),
                    G.atom('ge', G.sub(G.scale(3, hi), numerator)), G.atom('ge', G.sub(height, G.scale(3, L))),
                    G.atom('ge', G.sub(G.scale(3, H), height))))
    return G.either(*rows)


def check(record, guard, material=True):
    fixed_original = R.freeze(record['fixed'])
    require(fixed_original == (((1, 0, 0, 1), (0, 0), (0, 0)),
                               ((-2, 3, -1, 1), (0, 5), (0, 3))), 'Wrong repeated-cover fixed pair')
    results = []
    for residue in (0, 1):
        caps_original = R.freeze(record['even_caps' if residue == 0 else 'odd_caps'])
        fixed = tuple(pose_substitute(g, residue) for g in fixed_original)
        copies = (*fixed, *(pose_substitute(g, residue) for g in caps_original))
        columns = columns_substitute(residue)
        packing = [G.neg(intersection(G.relative(a, b), columns))
                   for j, b in enumerate(copies) for a in copies[:j]]
        physical_traces = 0
        for g in copies:
            for column, lo, hi in columns:
                for parity in (0, 1):
                    guard()
                    L, H = height_range(lo, hi, parity)
                    for s in array_ranges(g, column, parity, residue, guard):
                        lows, highs = [L, *s['lo']], [H, *s['hi']]
                        nonempty = G.both(s['active'],
                            *(G.atom('ge', G.sub(G.sub(h, l), G.constant(1))) for l in lows for h in highs))
                        packing.append(G.neg(nonempty))
                    physical_traces += 1
        lines = []
        for j, (m, U, V) in enumerate(fixed):
            for du, dv in ((0, 0), *G.UV_DIRS):
                anchor = m, G.add(U, G.constant(du)), G.add(V, G.constant(dv))
                for column, lo, hi in columns:
                    finite = P.line_intervals(anchor, column, copies, guard, columns, 3)
                    for parity in (0, 1):
                        L, H = height_range(lo, hi, parity)
                        pieces = finite_ranges(finite, parity) + array_ranges(anchor, column, parity, residue, guard)
                        lines.append({'fixed_copy': j, 'halo_shift': (du, dv), 'column': column,
                                      'height_parity': parity, 'lo': L, 'hi': H, 'segments': pieces})
        formulas = [*packing, *endpoint_formulas(lines)]
        part = G.partition(formulas, minimum=3)
        require(part == splitter(formulas), 'Separate repeated-cover parameter partitions disagree')
        audits = []
        for n in part['representatives']:
            guard()
            require(all(G.evaluate(row, n) for row in packing), f'Repeated cover overlaps at n={n}, r={residue}')
            for number, line in enumerate(lines):
                require(covered(line, n), f'Repeated cover misses trace {number} at n={n}, r={residue}')
            if material:
                k = 2*n+residue
                tile = R.literal(k)
                feet = [set(R.E.affine(tile, R.axial(g, k))) for g in (*fixed_original, *caps_original)]
                array = [((-1, 0, 0, -1), (0, 12+6*j), (1, 6+2*j)) for j in range(n-1+residue)]
                feet += [set(R.E.affine(tile, R.axial(g, k))) for g in array]
                occupied = set()
                for foot in feet:
                    require(occupied.isdisjoint(foot), 'Material repeated cover overlaps')
                    occupied.update(foot)
                old = feet[0] | feet[1]
                require(R.E.halo(old) <= occupied, 'Material repeated cover misses halo')
                audits.append({'k': k, 'surround_copies': len(feet)-2, 'halo_cells': len(R.E.halo(old))})
        results.append({'k_residue': residue, 'minimum_n': 3, 'array_index_lo': (0, 0),
                        'array_index_hi': (1, -2+residue), 'caps': len(caps_original),
                        'array_packing_traces': physical_traces, 'halo_parity_traces': len(lines),
                        'segments': sum(len(x['segments']) for x in lines), 'partition': part,
                        'trace_sha256': R.sha(lines), 'material_audits': audits})
    return {'checked_all_k_E1': True, 'fixed': fixed_original, 'parity_classes': results,
            'array_mutual_packing': 'UV u-ranges12+6j+[-3,2] are disjoint for distinct indices',
            'scope': 'Complete original fixed-pair halo packing; local holes and arbitrary E0 contacts allowed'}
