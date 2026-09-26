"""Exact planar menus and GL(2,5) orbits for a line reflection."""
from itertools import product


def build():
    points = list(product(range(5), repeat=2))
    index = {p: i for i, p in enumerate(points)}
    neg = [index[(-y % 5, -z % 5)] for y, z in points]
    orbits = [(p, neg[p]) for p in range(1, 25) if p < neg[p]]
    owner = {p: i for i, orbit in enumerate(orbits) for p in orbit}
    owner[0] = 12
    lines = sorted({
        sum(1 << index[((y+t*a) % 5, (z+t*b) % 5)] for t in range(5))
        for y, z, a, b in product(range(5), repeat=4) if a or b
    })
    if len(orbits) != 12 or len(lines) != 30:
        raise ValueError("invalid planar geometry")
    lifted = [sum(1 << p for i, orbit in enumerate(orbits)
                  if mask >> i & 1 for p in orbit) for mask in range(4096)]
    menus = [[m for m, subset in enumerate(lifted)
              if all((subset | center) & line != line for line in lines)]
             for center in range(2)]
    matrices = [(a,b,c,d) for a,b,c,d in product(range(5), repeat=4)
                if (a*d-b*c) % 5]
    permutations = [
        [owner[index[((a*y+b*z) % 5, (c*y+d*z) % 5)]]
         for y,z in (points[orbit[0]] for orbit in orbits)]
        for a,b,c,d in matrices
    ]
    def images(mask):
        return {sum(1 << perm[i] for i in range(12) if mask >> i & 1)
                for perm in permutations}
    classes = []
    for center, menu in enumerate(menus):
        unseen = set(menu)
        records = []
        while unseen:
            rep = min(unseen)
            orbit = images(rep)
            if not orbit <= unseen:
                raise ValueError("GL2 orbit partition failure")
            unseen -= orbit
            records.append({"representative": rep, "weight": rep.bit_count(),
                            "multiplicity": len(orbit)})
        classes.append(records)
    constraints = sorted({
        tuple(owner[index[((u+x*a)%5, (v+x*b)%5)]] for x in range(5))
        for u,v,a,b in product(range(5), repeat=4)
    })
    return {"orbits": orbits, "menus": menus, "classes": classes,
            "constraints": constraints, "permutations": permutations}


def decode(center, masks, model):
    return sorted([25*x for x in range(5) if center >> x & 1] + [
        25*x+p for x,m in enumerate(masks)
        for j,o in enumerate(model["orbits"]) if m >> j & 1 for p in o
    ])


def normalizations(model):
    """Second-layer orbit representatives under the first-layer stabilizer."""
    def image(mask, permutation):
        return sum(1 << permutation[j] for j in range(12) if mask >> j & 1)
    result = []
    maximal = [r for r in model["classes"][0] if r["weight"] == 8]
    for first in maximal:
        representative = first["representative"]
        stabilizer = [p for p in model["permutations"] if image(representative,p) == representative]
        unseen = {m for m in model["menus"][0] if m.bit_count() >= 7}
        classes = []
        while unseen:
            rep = min(unseen)
            orbit = {image(rep,p) for p in stabilizer}
            if not orbit <= unseen:
                raise ValueError("incomplete stabilizer orbit partition")
            unseen -= orbit
            classes.append({"representative":rep,"weight":rep.bit_count(),"multiplicity":len(orbit)})
        result.append({"first":representative,"stabilizer_order":len(stabilizer),"classes":classes})
    return result


def write_instance(path, model, cube=False):
    with path.open("w") as output:
        for i, menu in enumerate(model["menus"]):
            if cube and i == 0:
                menu = [0,943]
            output.write(str(len(menu))+" "+" ".join(map(str,menu))+"\n")
        output.write(str(len(model["constraints"]))+"\n")
        for row in model["constraints"]:
            output.write(" ".join(map(str,row))+"\n")
