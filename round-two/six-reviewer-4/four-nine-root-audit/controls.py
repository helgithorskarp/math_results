"""Definition-level controls and deliberately damaged certificate rejection."""
from itertools import combinations, product
from copy import deepcopy
import json, hashlib
from census import N, RED, BLUE, GROUND, MAPS, STARS, LOW, FULL, need


def geometry():
    need(len(RED) == 15 and len(BLUE) == 30 and all(x.bit_count() == 3 for x in N), "Petersen dimensions")
    need(all((N[i] & N[j]).bit_count() == (0 if (i, j) in RED else 1) for i, j in combinations(range(10), 2)), "Petersen codegrees")
    need({sum(1 << i for i in c) for c in combinations(range(10), 4) if not any((i, j) in RED for i, j in combinations(c, 2))} == set(STARS), "independent four-set inventory")
    need(len(LOW) == 582 and len(FULL[5]) == 30 and len(FULL[6]) == 80, "complete row pools")
    maps = 0
    for p, im in MAPS:
        need(len(set(im)) == 10 and all(((N[i] >> j) & 1) == ((N[im[i]] >> im[j]) & 1) for i, j in combinations(range(10), 2)), "ground map does not preserve actual graph")
        maps += 1
    # The short proof removing multiplicity three uses each complementary
    # matching and every admissible low row, not just selected census data.
    forcing = 0
    for s in STARS:
        outside = 1023 ^ s
        ed = [(i, j) for i, j in RED if outside >> i & outside >> j & 1]
        need(len(ed) == 3 and len({i for e in ed for i in e}) == 6, "ground-star complementary matching")
        for z in LOW:
            if (z & s).bit_count() <= 1:
                need(any(z >> i & z >> j & 1 for i, j in ed), "low row avoids complementary matching")
                forcing += 1
    # Exhaust every four-coordinate demand vector and admissible binary row.
    # This is a direct integer oracle for the unary bitplane update.
    updates = 0
    for r in product(range(5), repeat=4):
        planes = tuple(sum(1 << i for i, v in enumerate(r) if v >= t) for t in (1, 2, 3, 4))
        for z in range(16):
            if any((z >> i & 1) > r[i] for i in range(4)):
                continue
            new = tuple((planes[t] & ~z) | ((planes[t+1] if t < 3 else 0) & z) for t in range(4))
            actual = tuple(sum(v >> i & 1 for v in new) for i in range(4))
            need(actual == tuple(v-(z >> i & 1) for i, v in enumerate(r)), "unary subtraction oracle")
            updates += 1
    return {"ground_maps": maps, "matching_low_word_checks": forcing, "complete_unary_update_checks": updates, "low_words": len(LOW), "full_large_word_counts": [len(FULL[5]), len(FULL[6])]}


def primary(path):
    from check import Matrix
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == "3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55", "primary fixture bytes")
    m = json.loads(raw.decode().split("\n\n")[0])
    need(len(m) == 21 and all(len(row) == 21 for row in m), "primary dimensions")
    need(all(type(m[i][j]) is int and m[i][j] in (0, 1) and m[i][j] == m[j][i] and (i != j or m[i][i] == 0) for i in range(21) for j in range(21)), "primary matrix schema")
    r = [sum(1 << j for j in range(21) if j != i and m[i][j] == 0) for i in range(21)]
    q = [((1 << 21)-1) ^ r[i] ^ (1 << i) for i in range(21)]
    rc, qc = [], []
    for i, j in combinations(range(21), 2):
        (rc if r[i] >> j & 1 else qc).append(((r[i] & r[j]) if r[i] >> j & 1 else (q[i] & q[j])).bit_count())
    need((len(rc), len(qc), max(rc), max(qc)) == (93, 117, 3, 6), "primary page counts")
    roots = [i for i in range(21) if r[i].bit_count() == 10]
    need(len(roots) == 1, "primary degree-ten root")
    v = roots[0]
    a = [i for i in range(21) if r[v] >> i & 1]
    b = [i for i in range(21) if q[v] >> i & 1]
    local = tuple(sum(1 << j for j, w in enumerate(a) if r[u] >> w & 1) for u in a)
    misses = tuple(sum(1 << i for i, w in enumerate(a) if not r[u] >> w & 1) for u in b)
    deltas = tuple(10-r[u].bit_count() for u in b)
    actual = tuple(sum(1 << j for j, w in enumerate(b) if r[u] >> w & 1) for u in b)
    f = Matrix(local, misses, deltas)
    ds = f.domains()
    need(all(x in ds[i] for i, x in enumerate(actual)), "positive actual star rejected")
    need(all(f.compatible(i, actual[i], j, actual[j]) for i, j in combinations(range(10), 2)), "positive actual completion rejected")
    damages = 0
    for i in range(10):
        for j in range(10):
            for h in range(10):
                if len({i, j, h}) != 3 or not actual[i] >> j & 1 or actual[i] >> h & 1:
                    continue
                x = actual[i] ^ (1 << j) ^ (1 << h)
                # An asymmetric alteration changes only i's star. A direct
                # reciprocity check must reject it independently of page caps.
                need(any(((x >> c) ^ (actual[c] >> i)) & 1 for c in range(10) if c != i), "asymmetric star passed reciprocity")
                damages += 1
    return {"order": 21, "red_edges": len(rc), "blue_edges": len(qc), "red_cap": max(rc), "blue_cap": max(qc), "actual_stars": 10, "actual_pairs": 45, "asymmetric_star_damages": damages}


def corruptions(cert, keys, cache):
    from check import audit
    cases = []
    def add(name, change):
        c = deepcopy(cert)
        change(c)
        cases.append((name, c))
    add("missing_template", lambda c: c["entries"].pop())
    add("duplicate_template", lambda c: c["entries"].append(deepcopy(c["entries"][0])))
    add("wrong_deficit", lambda c: c["outside_deficits"].__setitem__(0, 0))
    add("boolean_deficit", lambda c: c["outside_deficits"].__setitem__(0, True))
    add("boolean_order", lambda c: c.__setitem__("order", True))
    add("wrong_orbit_size", lambda c: c["entries"][0].__setitem__("orbit_size", 119))
    add("wrong_domain_hash", lambda c: c["entries"][0].__setitem__("domains_sha256", "0"*64))
    add("wrong_domain_size", lambda c: c["entries"][0]["domain_sizes"].__setitem__(0, 11))
    add("unsorted_low_words", lambda c: c["entries"][0]["key"][0].reverse())
    add("changed_incidence", lambda c: c["entries"][0]["key"][0].__setitem__(0, 30))
    add("boolean_word", lambda c: c["entries"][0]["key"][0].__setitem__(0, True))
    add("wrong_multiplicity", lambda c: c["entries"][0]["key"][2].__setitem__(0, 1))
    add("false_empty_domain", lambda c: c["entries"][0]["exclusion"].__setitem__("point", 0))
    add("propagation_in_static_schema", lambda c: c["entries"][0]["exclusion"].__setitem__("type", "propagation"))
    pos = next(i for i, e in enumerate(cert["entries"]) if e["exclusion"]["type"] == "star_pair_cover")
    add("missing_cover_star", lambda c: c["entries"][pos]["exclusion"]["covers"][0]["stars"].pop())
    add("duplicate_cover_star", lambda c: c["entries"][pos]["exclusion"]["covers"][0]["stars"].append(c["entries"][pos]["exclusion"]["covers"][0]["stars"][0]))
    add("self_support", lambda c: c["entries"][pos]["exclusion"]["covers"][0].__setitem__("against", c["entries"][pos]["exclusion"]["point"]))
    add("empty_cover_groups", lambda c: c["entries"][pos]["exclusion"].__setitem__("covers", []))
    supported = None
    for i, e in enumerate(cert["entries"]):
        if e["exclusion"]["type"] != "star_pair_cover":
            continue
        key = tuple(tuple(x) for x in e["key"])
        orb, f, ds = cache[key]
        b = e["exclusion"]["point"]
        for c in range(11):
            if c != b:
                for x in ds[b]:
                    if any(f.compatible(b, x, c, y) for y in ds[c]):
                        supported = i, b, c, x
                        break
            if supported:
                break
        if supported:
            break
    need(supported is not None, "no actual support corruption control")
    i, b, c, x = supported
    add("actual_supported_star_claimed_unsupported", lambda z: z["entries"][i].__setitem__("exclusion", {"type":"star_pair_cover", "point":b, "covers":[{"against":c, "stars":[x]}]}))
    rejected = []
    for name, broken in cases:
        try:
            audit(broken, keys, include_modes=False, cache=cache)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("damaged certificate passed: " + name)
    return rejected
