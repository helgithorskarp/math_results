"""Search and independently check small lattice-periodic grid tilings.

Failure to find a periodic pattern proves no nontiling or Heesch bound.
"""
from corona import normalize, orientations


def check_periodic(tile, certificate):
    tile = normalize(tile)
    a, b, c = certificate['a'], certificate['b'], certificate['c']
    if any(type(x) is not int for x in (a, b, c)) or a <= 0 or c <= 0 or not 0 <= b < a:
        raise ValueError('invalid lattice basis')
    copies = certificate['copies']
    variants = set(orientations(tile))
    cells = []
    roots = 0
    for raw in copies:
        copy = set(map(tuple, raw))
        if len(copy) != len(raw) or len(copy) != len(tile) or normalize(copy) not in variants:
            raise ValueError('invalid congruent copy')
        roots += copy == set(tile)
        cells.extend(sorted(copy))
    if roots != 1 or len(cells) != a * c:
        raise ValueError('wrong prescribed root or lattice determinant')
    # Independent difference-vector membership; the search uses residue masks.
    for i, (x, y) in enumerate(cells):
        for u, v in cells[:i]:
            dy = y - v
            if dy % c == 0 and (x - u - b * (dy // c)) % a == 0:
                raise ValueError('copies overlap modulo lattice')
    return {'copies': len(copies), 'determinant': a * c,
            'basis': [[a, 0], [b, c]], 'checked': 'periodic plane tiling'}


def find_periodic(tile, count=2, node_budget=10000):
    """Complete two-copy search, or budgeted backtracking for larger counts.

Lattices are integer lattices of index count*area, in Hermite normal form.
For count>2 a budget exhaustion only skips this lattice, never proves a negative.
"""
    tile = normalize(tile)
    if type(count) is not int or count < 1:
        raise ValueError('copy count must be positive')
    area = len(tile)
    determinant = count * area
    variants = orientations(tile)
    exhausted = 0
    for a in range(1, determinant + 1):
        if determinant % a:
            continue
        c = determinant // a
        for b in range(a):
            def residues(cells):
                return {(x - b * (y // c)) % a + a * (y % c) for x, y in cells}

            root_residues = residues(tile)
            if len(root_residues) != area:
                continue
            root_mask = sum(1 << r for r in root_residues)
            remaining = ((1 << determinant) - 1) ^ root_mask
            if not remaining:
                cert = {'a': a, 'b': b, 'c': c, 'copies': [tile]}
                check_periodic(tile, cert)
                return cert, exhausted
            placements = {}
            for shape in variants:
                for tx in range(a):
                    for ty in range(c):
                        moved = tuple((x + tx, y + ty) for x, y in shape)
                        rs = residues(moved)
                        if len(rs) != area:
                            continue
                        mask = sum(1 << r for r in rs)
                        if mask & root_mask:
                            continue
                        if mask == remaining:
                            cert = {'a': a, 'b': b, 'c': c, 'copies': [tile, moved]}
                            check_periodic(tile, cert)
                            return cert, exhausted
                        if count > 2:
                            placements.setdefault(mask, moved)
            if count <= 2:
                continue
            coverers = {}
            for mask in placements:
                bits = mask
                while bits:
                    low = bits & -bits
                    coverers.setdefault(low, []).append(mask)
                    bits -= low
            nodes = 0
            failed = set()

            def search(wanted):
                nonlocal nodes
                nodes += 1
                if nodes > node_budget:
                    raise TimeoutError('periodic-search node budget exhausted')
                if not wanted:
                    return []
                if wanted.bit_count() == area:
                    return [wanted] if wanted in placements else None
                if wanted.bit_count() == 2 * area:
                    for mask in placements:
                        if mask & wanted == mask and wanted ^ mask in placements:
                            return [mask, wanted ^ mask]
                    return None
                if wanted in failed:
                    return None
                pivot = None
                bits = wanted
                while bits:
                    low = bits & -bits
                    options = [mask for mask in coverers.get(low, ()) if mask & wanted == mask]
                    if not options:
                        failed.add(wanted)
                        return None
                    if pivot is None or len(options) < len(pivot):
                        pivot = options
                    bits -= low
                for mask in pivot:
                    result = search(wanted ^ mask)
                    if result is not None:
                        return [mask] + result
                failed.add(wanted)
                return None

            try:
                masks = search(remaining)
            except TimeoutError:
                exhausted += 1
                continue
            if masks is not None:
                cert = {'a': a, 'b': b, 'c': c,
                        'copies': [tile] + [placements[mask] for mask in masks]}
                check_periodic(tile, cert)
                return cert, exhausted
    return None, exhausted
