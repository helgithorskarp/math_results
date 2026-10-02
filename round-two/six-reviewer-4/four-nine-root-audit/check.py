#!/usr/bin/env python3
"""Independent complete incidence and physical-bitmatrix certificate audit."""
import argparse, json
import hashlib
from pathlib import Path
from collections import Counter
from itertools import combinations
from census import N, STARS, RED, BLUE, LOW, FULL, census, key_orbit, need, digest

HERE = Path(__file__).resolve().parent
DELTAS = (1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0)


def integer(x, lo, hi, name):
    need(type(x) is int and lo <= x <= hi, "invalid " + name)


def fields(x, names, name):
    need(type(x) is dict and set(x) == set(names), "invalid " + name + " fields")


def decode(raw):
    need(type(raw) is list and len(raw) == 3, "invalid key")
    lo, hi, mu = raw
    need(type(lo) is list and len(lo) == 4 and type(hi) is list and len(hi) <= 2 and type(mu) is list and len(mu) == 5, "invalid key shape")
    for z in lo:
        integer(z, 0, 1023, "low word")
        need(z in LOW, "invalid low size")
    for z in hi:
        integer(z, 0, 1023, "full word")
        need(z in FULL.get(z.bit_count(), ()), "invalid full word")
    for x in mu:
        integer(x, 0, 2, "star multiplicity")
    need(lo == sorted(lo) and hi == sorted(hi) and sum(mu) + len(hi) == 7, "invalid key order or full count")
    return tuple(lo), tuple(hi), tuple(mu)


def rows(key):
    lo, hi, mu = key
    return lo + hi + tuple(s for s, n in zip(STARS, mu) for _ in range(n))


class Matrix:
    """Construct actual physical red/complement adjacency bit rows.

    Root 0, local vertices 1..10, outside vertices 11..(10+m).
    An outside star is an m-bit row in that final block. No decomposed page
    formula is used in the proof checker.
    """
    def __init__(self, local, misses, deltas):
        self.local, self.misses, self.deltas = tuple(local), tuple(misses), tuple(deltas)
        self.m = len(misses)
        need(len(deltas) == self.m and len(local) == 10, "matrix dimensions")
        self.all = (1 << (11 + self.m)) - 1
        self.ar = tuple(1 | (local[i] << 1) | sum(1 << (11+b) for b, z in enumerate(misses) if not z >> i & 1) for i in range(10))
        self.ab = tuple(self.all ^ self.ar[i] ^ (1 << (1+i)) for i in range(10))
        self.red = [dict() for b in misses]
        self.blue = [dict() for b in misses]

    def physical(self, b, x):
        r = ((1023 ^ self.misses[b]) << 1) | (x << 11)
        return r, self.all ^ r ^ (1 << (11+b))

    def domains(self):
        result = []
        for b, (z, delta) in enumerate(zip(self.misses, self.deltas)):
            degree = z.bit_count() - delta
            need(0 <= degree < self.m, "outside degree")
            domain = []
            # Every degree-correct star is literally an outside edge subset.
            for picked in combinations(tuple(c for c in range(self.m) if c != b), degree):
                x = sum(1 << c for c in picked)
                r, q = self.physical(b, x)
                if all((q & self.ab[i]).bit_count() <= 6 if z >> i & 1 else (r & self.ar[i]).bit_count() <= 3 for i in range(10)):
                    domain.append(x)
                    self.red[b][x], self.blue[b][x] = r, q
            result.append(sorted(domain))
        return result

    def compatible(self, b, x, c, y, mode="full"):
        if ((x >> c) ^ (y >> b)) & 1:
            return False
        if x >> c & 1:
            return mode in ("reciprocal", "blue_only") or (self.red[b][x] & self.red[c][y]).bit_count() <= 3
        return mode in ("reciprocal", "red_only") or (self.blue[b][x] & self.blue[c][y]).bit_count() <= 6


def exclusion(frame, domains, exc):
    need(type(exc) is dict, "exclusion object")
    b = exc.get("point")
    integer(b, 0, 10, "target point")
    if exc.get("type") == "empty_star":
        fields(exc, ("type", "point"), "empty exclusion")
        need(not domains[b], "claimed domain is nonempty")
        return 0, 0
    fields(exc, ("type", "point", "covers"), "cover exclusion")
    need(exc["type"] == "star_pair_cover" and all(domains), "invalid static cover type")
    need(type(exc["covers"]) is list and exc["covers"], "missing covers")
    covered, support_points = set(), []
    for group in exc["covers"]:
        fields(group, ("against", "stars"), "cover group")
        c = group["against"]
        integer(c, 0, 10, "support point")
        need(c != b, "self support")
        xs = group["stars"]
        need(type(xs) is list and xs and xs == sorted(set(xs)), "cover values")
        for x in xs:
            integer(x, 0, 2047, "star")
            need(x in domains[b] and x not in covered, "absent or repeated cover star")
            need(all(not frame.compatible(b, x, c, y) for y in domains[c]), "actual supported star excluded")
        support_points.append(c)
        covered.update(xs)
    need(support_points == sorted(set(support_points)), "support point order")
    need(covered == set(domains[b]), "cover incomplete")
    return len(exc["covers"]), len(covered)


def static_mode(frame, domains, mode):
    for b, domain in enumerate(domains):
        if all(any(all(not frame.compatible(b, x, c, y, mode) for y in domains[c]) for c in range(11) if c != b) for x in domain):
            return b
    return None


def audit(cert, keys, include_modes=True, cache=None):
    fields(cert, ("schema", "order", "red_page_cap", "blue_page_cap", "outside_deficits", "local_graph", "incidence_records", "entries"), "certificate")
    for k, v in (("schema", 1), ("order", 22), ("red_page_cap", 3), ("blue_page_cap", 6), ("incidence_records", len(keys))):
        integer(cert[k], v, v, k)
    need(cert["outside_deficits"] == list(DELTAS) and all(type(x) is int for x in cert["outside_deficits"]), "deficiency tags")
    need(cert["local_graph"] == "KG(5,2)" and type(cert["entries"]) is list and cert["entries"], "local graph or entries")
    seen, ordered, records = set(), [], []
    hist, weighted, kinds, modes = Counter(), Counter(), Counter(), Counter()
    groups = targets = 0
    for e in cert["entries"]:
        fields(e, ("key", "orbit_size", "domain_sizes", "domains_sha256", "exclusion"), "entry")
        key = decode(e["key"])
        if cache is not None and key in cache:
            orb, frame, domains = cache[key]
        else:
            orb = key_orbit(key)
            frame = Matrix(N, rows(key), DELTAS)
            domains = frame.domains()
            if cache is not None:
                cache[key] = orb, frame, domains
        need(key == min(orb) and orb <= keys and not seen & orb, "orbit coverage or representative")
        integer(e["orbit_size"], len(orb), len(orb), "orbit size")
        seen.update(orb)
        ordered.append(key)
        need(e["domain_sizes"] == list(map(len, domains)) and all(type(x) is int for x in e["domain_sizes"]), "domain sizes")
        need(e["domains_sha256"] == digest(domains), "domain entry mismatch")
        g, t = exclusion(frame, domains, e["exclusion"])
        groups += g
        targets += t
        kind = e["exclusion"]["type"]
        hist[len(orb)] += 1
        kinds[kind] += 1
        weighted[kind] += len(orb)
        record = {"key": key, "orbit": len(orb), "domains_sha256": digest(domains), "domain_sizes": list(map(len, domains)), "original_static_cover_verified": True}
        if include_modes and all(domains):
            record["relaxed_static_targets"] = {m: static_mode(frame, domains, m) for m in ("reciprocal", "red_only", "blue_only", "full")}
            for m, b in record["relaxed_static_targets"].items():
                modes[m] += b is not None
        records.append(record)
    need(ordered == sorted(set(ordered)) and seen == keys, "full entrywise census coverage")
    return {"records": len(keys), "incidence_sha256": digest(sorted(keys)), "templates": len(records), "orbit_histogram": dict(sorted(hist.items())), "exclusions": dict(kinds), "weighted_exclusions": dict(weighted), "original_cover_groups": groups, "original_target_stars": targets, "certificate_sha256": digest(cert), "entrywise_domain_and_obstruction_record_sha256": digest(records), "relaxed_static_template_counts": dict(modes)}, records


def main():
    p = argparse.ArgumentParser()
    p.add_argument("certificate", type=Path)
    p.add_argument("--emit", action="store_true")
    p.add_argument("--refinement-output", type=Path)
    p.add_argument("--primary", type=Path, required=True)
    args = p.parse_args()
    keys, cohorts = census(3)
    need(all(max(mu) <= 2 for lo, hi, mu in keys), "broader multiplicity-three incidence survives")
    raw = args.certificate.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == "1eb55ea5963ecbba0deaa1414bcbdb4aa500e9fa0ce9e2a81f6bb77684428330", "original certificate byte provenance")
    cert = json.loads(raw)
    cache = {}
    result, records = audit(cert, keys, cache=cache)
    result["broader_multiplicity_cap"] = 3
    result["broader_keys_all_have_original_cap_two"] = True
    refined = []
    for record in records:
        if "relaxed_static_targets" not in record:
            continue
        key = record["key"]
        orb, frame, domains = cache[key]
        b = record["relaxed_static_targets"]["red_only"]
        need(b is not None, "refinement has no red-only static target")
        groups = {}
        for x in domains[b]:
            c = next(c for c in range(11) if c != b and all(not frame.compatible(b, x, c, y, "red_only") for y in domains[c]))
            groups.setdefault(c, []).append(x)
        refined.append({"key": key, "point": b, "covers": [{"against": c, "stars": xs} for c, xs in sorted(groups.items())]})
    result["red_only_static_certificate_sha256"] = digest(refined)
    result["red_only_static_groups"] = sum(len(e["covers"]) for e in refined)
    result["red_only_static_target_stars"] = sum(len(g["stars"]) for e in refined for g in e["covers"])
    refined = json.loads(json.dumps(refined))
    if not args.emit:
        need(refined == json.loads((HERE/"red-only-certificate.json").read_text()), "complete red-only certificate mismatch")
    if args.refinement_output:
        args.refinement_output.write_text(json.dumps(refined, sort_keys=True, indent=2)+"\n")
    result["cohorts"] = cohorts
    result["size_patterns"] = [{"low": a, "high": b, "count": n} for (a, b), n in sorted(Counter((tuple(sorted(z.bit_count() for z in lo)), tuple(z.bit_count() for z in hi)) for lo, hi, mu in keys).items())]
    from controls import geometry, primary, corruptions
    result["controls"] = {"geometry": geometry(), "primary": primary(args.primary), "damaged_certificates_rejected": corruptions(cert, keys, cache)}
    if not args.emit:
        need(json.loads(json.dumps(result)) == json.loads((HERE/"expected.json").read_text()), "complete expected record mismatch")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
