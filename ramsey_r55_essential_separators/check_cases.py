"""Check coverage using compositions and integer attachment populations.

Does not import the producer. Human proof supplies the Ramsey implications;
this checker verifies the finite domain, populations and certificate fields.
"""
from itertools import product


def need(value, message):
    if not value:
        raise ValueError(message)


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, length - 1):
                yield (first,) + tail


def check(document):
    need(set(document) == {"n", "maximum_separator", "external_bound", "cases"}, "schema")
    need(document["n"] == 43 and document["maximum_separator"] == 20, "dimensions")
    need(document["external_bound"] == "R(4,5)<=25", "import")
    domain = set()
    for a, b, s in compositions(43, 3):
        if 2 <= a <= b and s <= 20:
            for p, q in product((1, 2, 3), repeat=2):
                if p + q <= 4 and a < (5, 14, 25)[p - 1] and b < (5, 14, 25)[q - 1]:
                    domain.add((s, a, b, p, q))
    actual = [(r["s"], r["a"], r["b"], r["alpha_a"], r["alpha_b"]) for r in document["cases"]]
    need(len(actual) == len(set(actual)) and set(actual) == domain, "incomplete/duplicate coverage")
    populations = 0
    residual = []
    for r in document["cases"]:
        s, a, b, p, q = (r[k] for k in ("s", "a", "b", "alpha_a", "alpha_b"))
        fields = {"s", "a", "b", "alpha_a", "alpha_b", "status", "rule"}
        if 1 in (p, q):
            k = a if p == 1 else b
            feasible = 0
            # n[j] counts separator vertices with exactly j blue contacts to K_k.
            for n in compositions(s, k + 1):
                populations += 1
                if n[0] > (13, 4, 0)[k - 2]:
                    continue
                if k == 4 and n[1] > 4 * 4:
                    continue
                if sum(j * n[j] for j in range(k + 1)) > k * (s - 18 + k - 1):
                    continue
                feasible += 1
            need(feasible == 0 and r["status"] == "EXCLUDED", "clique populations survive")
            if k == 4:
                need(r["rule"] == "K4_contact_types" and r["required_separator"] == 22, "K4 certificate")
                fields |= {"required_separator"}
            else:
                need(r["rule"] == "common_neighbors", "clique rule")
                need(r["lower"] == s - k * (s - 18 + k - 1), "common lower")
                need(r["upper"] == (13 if k == 2 else 4), "common upper")
                fields |= {"lower", "upper"}
        else:
            def limit(c):
                # No clique of order 14-c in T_C; no independent five.
                return (1, 5, 14, 25)[13 - c] - 1
            capacity = limit(a) + limit(b)
            need(r["capacity"] == capacity, "contact capacity")
            feasible = any(x + y >= s for x in range(min(s, limit(a)) + 1)
                           for y in range(min(s, limit(b)) + 1))
            fields |= {"capacity"}
            if not feasible:
                need(r["status"] == "EXCLUDED" and r["rule"] == "contact_cover", "cover exclusion")
            else:
                need(r["status"] == "NECESSARY_RESIDUAL_ONLY", "residual status")
                need(r["rule"] == "contact_cover_and_degree", "residual rule")
                allowed = [d for d in range(18, 25) if 13 * d <= 13 * 8 + 8 * s]
                need(r["maximum_minimum_degree"] == max(allowed) == 20, "degree boundary")
                fields |= {"maximum_minimum_degree"}
                residual.append([s, a, b, p, q])
        need(set(r) == fields, "row schema")
    need(residual == [[20, 10, 13, 2, 2]], "residual list")
    return {"status": "PASS", "covered_cases": len(domain),
            "cases_through_19": sum(k[0] <= 19 for k in domain),
            "excluded_cases": len(domain) - len(residual),
            "clique_population_vectors": populations, "necessary_residuals": residual}
