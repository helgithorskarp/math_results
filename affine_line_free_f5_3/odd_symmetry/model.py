"""Exact finite model for the order-three symmetry theorem."""
from itertools import product


def build():
    points = list(product(range(5), repeat=2))
    index = {p: i for i, p in enumerate(points)}
    rotation = [index[(-z % 5, (y-z) % 5)] for y, z in points]
    seen, orbits = {0}, []
    for p in range(1, 25):
        if p in seen:
            continue
        orbit, q = [], p
        while q not in orbit:
            orbit.append(q)
            seen.add(q)
            q = rotation[q]
        if q != p or len(orbit) != 3:
            raise ValueError("incorrect rotation orbit")
        orbits.append(orbit)
    if len(orbits) != 8:
        raise ValueError("incorrect orbit count")
    orbit_of = {p: i for i, orbit in enumerate(orbits) for p in orbit}
    orbit_of[0] = 8
    lines = sorted({
        sum(1 << index[((y+t*a) % 5, (z+t*b) % 5)] for t in range(5))
        for y, z, a, b in product(range(5), repeat=4) if a or b
    })
    if len(lines) != 30:
        raise ValueError("incorrect planar line count")
    menus = []
    for center in range(2):
        menu = []
        for mask in range(256):
            lifted = center
            for i, orbit in enumerate(orbits):
                if mask >> i & 1:
                    lifted |= sum(1 << p for p in orbit)
            if all(lifted & line != line for line in lines):
                menu.append(mask)
        menus.append(menu)
    constraints = sorted({
        tuple(orbit_of[index[((y+x*a) % 5, (z+x*b) % 5)]] for x in range(5))
        for y, z, a, b in product(range(5), repeat=4)
    })
    if len(constraints) != 209 or any(m.bit_count() > 5 for menu in menus for m in menu):
        raise ValueError("unexpected finite model")
    return {"orbits": orbits, "menus": menus, "constraints": constraints}


def write_instance(path, model):
    with path.open("w") as output:
        for menu in model["menus"]:
            output.write(str(len(menu)) + " " + " ".join(map(str, menu)) + "\n")
        output.write(str(len(model["constraints"])) + "\n")
        for row in model["constraints"]:
            output.write(" ".join(map(str, row)) + "\n")


def decode(center_mask, masks, model):
    points = set()
    if len(masks) != 5 or any(not 0 <= m < 256 for m in masks):
        raise ValueError("invalid layer masks")
    for x, mask in enumerate(masks):
        if center_mask >> x & 1:
            points.add(25*x)
        for i, orbit in enumerate(model["orbits"]):
            if mask >> i & 1:
                points.update(25*x + p for p in orbit)
    return sorted(points)
