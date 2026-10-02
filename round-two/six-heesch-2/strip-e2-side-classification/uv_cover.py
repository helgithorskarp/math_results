"""Exact whole-halo coverage for a proposed finite affine strip pattern.

Coverage is reduced to 84 integer line segments for a two-copy fixed pair.
Nonparallel intersections are singletons with denominator3, made active only
when integral. Half-open endpoints are scaled by3. Exact order and activation
partitions include the infinite tail; finite materialized checks are audits.
"""
import deps
import strip_parametric_geometry as G
import strip_contact_reader as R
from strip_columns import require


def globally_possible(predicate, guard, minimum=6):
    if type(predicate) is bool:
        return predicate
    part = G.partition([predicate], minimum=minimum)
    for k in part['representatives']:
        guard()
        if G.evaluate(predicate, k):
            return True
    return False


def line_intervals(anchor, column, copies, guard, columns=None, minimum=6):
    """In anchor coordinates, intersect all copies with u=column."""
    segments = []
    columns = G.COLS if columns is None else columns
    for number, copy in enumerate(copies):
        (a, b, c, d), U, V = G.relative(anchor, copy)
        for source, lo, hi in columns:
            guard()
            if b == 0:
                active = G.atom('eq', G.add(U, G.constant(a*source-column)))
                left, right = (lo, hi) if d == 1 else (hi, lo)
                bottom = G.add(G.add(G.constant(c*source), V), G.scale(d, left))
                top = G.add(G.add(G.constant(c*source), V), G.scale(d, right))
                start = G.scale(3, bottom)
                stop = G.scale(3, G.add(top, G.constant(1)))
            else:
                require(abs(b) == 3, 'Unexpected strip direction')
                n = G.scale(1 if b > 0 else -1,
                            G.sub(G.constant(column-a*source), U))
                active = G.both(G.atom('mod', n, 3),
                                G.atom('ge', G.sub(n, G.scale(3, lo))),
                                G.atom('ge', G.sub(G.scale(3, hi), n)))
                start = G.add(G.scale(3, G.add(G.constant(c*source), V)), G.scale(d, n))
                stop = G.add(start, G.constant(3))
            if globally_possible(active, guard, minimum):
                segments.append({'copy': number, 'source_column': source,
                                 'lo': start, 'hi': stop, 'active': active})
    return segments


def traces(fixed, copies, guard):
    out = []
    for j, (m, U, V) in enumerate(fixed):
        for du, dv in ((0, 0), *G.UV_DIRS):
            anchor = m, G.add(U, G.constant(du)), G.add(V, G.constant(dv))
            for column, lo, hi in G.COLS:
                guard()
                out.append({'fixed_copy': j, 'halo_shift': (du, dv), 'column': column,
                            'lo': G.scale(3, lo), 'hi': G.scale(3, G.add(hi, G.constant(1))),
                            'segments': line_intervals(anchor, column, copies, guard)})
    return out


def order_formulas(lines):
    rows = []
    for line in lines:
        ends = {line['lo'], line['hi']}
        for s in line['segments']:
            rows.append(s['active'])
            ends.update((s['lo'], s['hi']))
        ordered = sorted(ends)
        for j, x in enumerate(ordered):
            for y in ordered[:j]:
                # Both weak comparisons distinguish equality from strict order.
                rows.extend((G.atom('ge', G.sub(x, y)), G.atom('ge', G.sub(y, x))))
    return rows


def covered(line, k):
    cursor, target_end = G.value(line['lo'], k), G.value(line['hi'], k)
    ranges = sorted((G.value(s['lo'], k), G.value(s['hi'], k))
                    for s in line['segments'] if G.evaluate(s['active'], k))
    for lo, hi in ranges:
        require(lo % 3 == hi % 3 == 0 and lo < hi, 'Nonintegral/empty active line intersection')
        if lo > cursor:
            break
        cursor = max(cursor, hi)
        if cursor >= target_end:
            return True
    return False


def check(fixed, surround, guard, material=True):
    fixed, surround = R.freeze(fixed), R.freeze(surround)
    require(len(fixed) > 0, 'No fixed centers')
    copies = (*fixed, *surround)
    require(len(set(copies)) == len(copies), 'Repeated affine copy')
    packing = [G.neg(G.intersection(G.relative(a, b)))
               for j, b in enumerate(copies) for a in copies[:j]]
    lines = traces(fixed, copies, guard)
    formulas = [*packing, *order_formulas(lines)]
    part = G.partition(formulas)
    require(part == R.splitter(formulas), 'Separate whole-halo partitions differ')
    audits = []
    for k in part['representatives']:
        guard()
        require(all(G.evaluate(row, k) for row in packing), f'Pattern overlaps at k={k}')
        for number, line in enumerate(lines):
            require(covered(line, k), f'Pattern misses whole-halo trace {number} at k={k}')
        if material:
            tile = R.literal(k)
            feet = [set(R.E.affine(tile, R.axial(g, k))) for g in copies]
            occupied = set()
            for foot in feet:
                require(occupied.isdisjoint(foot), 'Material pattern overlaps')
                occupied.update(foot)
            old = set().union(*feet[:len(fixed)])
            needed = R.E.halo(old)
            require(needed <= set().union(*feet[len(fixed):]), 'Material original halo is missed')
            audits.append({'k': k, 'halo_cells': len(needed)})
    return {'fixed_copies': len(fixed), 'surround_copies': len(surround),
            'traces': len(lines), 'segments': sum(len(x['segments']) for x in lines),
            'partition': part, 'trace_sha256': R.sha(lines),
            'material_audits': audits, 'complete_all_k_cover': True}
