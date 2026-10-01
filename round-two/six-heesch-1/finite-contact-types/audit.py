"""Independent bounded unit-rectangle audit of finite mesh candidate pools."""
from contact import require


def audit_pool(tile, fixed, scale, pool, domain=None):
    fixed_rects = [(int(x*scale), int(y*scale))
                   for p in fixed for x, y in tile.anchors(p)]
    xmin, ymin = min(x for x, y in fixed_rects), min(y for x, y in fixed_rects)
    xmax, ymax = max(x for x, y in fixed_rects)+scale, max(y for x, y in fixed_rects)+scale
    found = set()
    for o, shape in enumerate(tile.orientations):
        width, height = max(x for x, y in shape)+1, max(y for x, y in shape)+1
        op = [(a*scale, b*scale) for a, b in shape]
        for x in range(xmin-width*scale, xmax+1):
            for y in range(ymin-height*scale, ymax+1):
                overlaps, touches = False, False
                for a, b in op:
                    for u, v in fixed_rects:
                        dx, dy = abs(x+a-u), abs(y+b-v)
                        if dx < scale and dy < scale:
                            overlaps = True
                            break
                        if dx <= scale and dy <= scale:
                            touches = True
                    if overlaps:
                        break
                if overlaps or not touches:
                    continue
                if domain is not None:
                    from fractions import Fraction
                    p = (o, Fraction(x, scale), Fraction(y, scale))
                    if any(tile.relation(p, A) == 'contact' and
                           tile.relative_type(p, A) not in domain for A in fixed):
                        continue
                found.add((o, x, y))
    actual = set()
    for p, physical in pool:
        o, x, y = p
        key = (o, int(x*scale), int(y*scale))
        require(key not in actual, 'duplicate candidate')
        actual.add(key)
        footprint = {(key[1]+a*scale+i, key[2]+b*scale+j)
                     for a, b in tile.orientations[o]
                     for i in range(scale) for j in range(scale)}
        require(footprint == physical, 'candidate footprint mismatch')
    require(found == actual, 'incomplete or extra candidate pool')
    return len(actual)
