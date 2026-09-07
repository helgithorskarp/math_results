"""Definition-level controls for the proof, plus malformed certificates.

These finite tests support the unformalized argument; they are not a proof
of the general lemmas. No solver, graph catalog, random data or third-party
package is used.
"""
from copy import deepcopy
from itertools import combinations
import check_cases
import check_branches
import nogood


def need(condition, message):
    if not condition:
        raise ValueError(message)


def adjacency(n, edges, word):
    rows = [0] * n
    for bit, (u, v) in enumerate(edges):
        if word >> bit & 1:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def homogeneous(rows, vertices, color):
    return all((rows[u] >> v & 1) == color for u, v in combinations(vertices, 2))


def no_independent_triple(rows, vertices):
    return not any(homogeneous(rows, triple, 0) for triple in combinations(vertices, 3))


def growth():
    graphs = checks = classes = 0
    for n in range(1, 7):
        edges = list(combinations(range(n), 2))
        for word in range(1 << len(edges)):
            rows = adjacency(n, edges, word)
            graphs += 1
            for c in range(1, n):
                core = list(range(c))
                if not no_independent_triple(rows, core):
                    continue
                contact = []
                for z in range(c, n):
                    nonneighbors = [u for u in core if not (rows[z] >> u & 1)]
                    if homogeneous(rows, nonneighbors, 1):
                        contact.append(z)
                classes += 1
                for mask in range(1 << len(contact)):
                    chosen = [z for k, z in enumerate(contact) if mask >> k & 1]
                    if homogeneous(rows, chosen, 1):
                        need(no_independent_triple(rows, core + chosen), "clique-growth lemma")
                        checks += 1
    return {"all_labeled_graphs_orders_1_to_6": graphs,
            "contact_classes": classes, "clique_extensions_checked": checks}


def contact_cover():
    graphs = uncovered = 0
    for a, b, s in ((2, 2, 2), (3, 3, 1)):
        n = a + b + s
        left, right = list(range(a)), list(range(a, a + b))
        free = [(u, v) for u, v in combinations(range(n), 2)
                if not (u < a <= v < a + b)]
        for word in range(1 << len(free)):
            rows = adjacency(n, free, word)
            graphs += 1
            for z in range(a + b, n):
                pairs = []
                for side in (left, right):
                    witness = next((p for p in combinations(side, 2)
                                    if homogeneous(rows, (z,) + p, 0)), None)
                    pairs.append(witness)
                if all(pairs):
                    need(homogeneous(rows, pairs[0] + pairs[1] + (z,), 0), "uncovered contact is not I5")
                    uncovered += 1
    return {"anticomplete_physical_graphs": graphs, "uncovered_contacts_with_literal_I5": uncovered}


def clique_attachments():
    graphs = good_k5 = singleton_pair_checks = 0
    # Exhaust every 3-vertex separator and every attachment to K2, K3, K4.
    for k in (2, 3, 4):
        sep = list(range(k, k + 3))
        free = list(combinations(sep, 2)) + [(u, z) for u in range(k) for z in sep]
        for word in range(1 << len(free)):
            rows = adjacency(k + 3, free, word)
            for u, v in combinations(range(k), 2):
                rows[u] |= 1 << v
                rows[v] |= 1 << u
            graphs += 1
            delta_side = min(rows[u].bit_count() for u in range(k))
            miss = [[u for u in range(k) if not (rows[z] >> u & 1)] for z in sep]
            population = [sum(len(m) == j for m in miss) for j in range(k + 1)]
            need(population[0] >= k * (delta_side - k + 1) - (k - 1) * 3, "common-neighbor bound")
            need(sum(j * population[j] for j in range(k + 1)) <= k * (3 - delta_side + k - 1), "contact upper bound")
            if any(homogeneous(rows, v, 1) for v in combinations(range(k + 3), 5)):
                continue
            good_k5 += 1
            common = [z for z, m in zip(sep, miss) if not m]
            need(not any(homogeneous(rows, v, 1) for v in combinations(common, 5 - k)), "forbidden common clique")
            if k == 4:
                need(population[0] == 0, "K4 all-red contact")
                for i in range(k):
                    group = [z for z, m in zip(sep, miss) if m == [i]]
                    need(homogeneous(rows, group, 0), "singleton-miss class is not independent")
                    singleton_pair_checks += len(list(combinations(group, 2)))
    return {"clique_attachment_graphs": graphs, "K5_free_attachment_graphs": good_k5,
            "independent_singleton_class_pairs": singleton_pair_checks}


def negative(case_doc, branch_doc):
    rejected = 0
    mutations = []
    d = deepcopy(case_doc); d["cases"].pop(); mutations.append(d)
    d = deepcopy(case_doc); d["cases"].append(d["cases"][0]); mutations.append(d)
    d = deepcopy(case_doc); d["external_bound"] = "none"; mutations.append(d)
    for field, value, rule in (("capacity", 19, "contact_cover"),
                               ("required_separator", 20, "K4_contact_types"),
                               ("maximum_minimum_degree", 21, "contact_cover_and_degree"),
                               ("lower", 0, "common_neighbors")):
        d = deepcopy(case_doc)
        next(r for r in d["cases"] if r["rule"] == rule)[field] = value
        mutations.append(d)
    d = deepcopy(case_doc)
    next(r for r in d["cases"] if r["status"] == "NECESSARY_RESIDUAL_ONLY")["status"] = "EXCLUDED"
    mutations.append(d)
    for d in mutations:
        try:
            check_cases.check(d)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("accepted corrupt arithmetic certificate")
    mutations = []
    d = deepcopy(branch_doc); d["n"] = 42; mutations.append(d)
    d = deepcopy(branch_doc); d["frame_pins"][0][2] ^= 1; mutations.append(d)
    d = deepcopy(branch_doc); d["a"][0] = d["b"][0]; mutations.append(d)
    d = deepcopy(branch_doc); d["branches"] = d["branches"][:1]; mutations.append(d)
    for d in mutations:
        try:
            check_branches.check(d)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("accepted corrupt branch certificate")
    # Literal signs: the homogeneous branch falsifies its cut clause, while
    # flipping any one of its 144 bits satisfies it. All other bits are absent.
    truth_checks = 0
    for row in branch_doc["branches"]:
        clause = row["cut_nogood_in_F27_variables"]
        c = row["cross_color"]
        for flipped in [None] + [abs(v) for v in clause]:
            value = any((c ^ int(abs(v) == flipped)) == int(v > 0) for v in clause)
            need(value == (flipped is not None), "cut-clause truth basis")
            truth_checks += 1
    physical = list(combinations(range(43), 2))
    frame = {tuple(e[:2]) for e in branch_doc["frame_pins"]}
    frame_variables = [e for e in physical if e not in frame]
    for row in branch_doc["branches"]:
        actual = nogood.clause(branch_doc["a"], branch_doc["b"], row["cross_color"])
        expected = [(1 if v > 0 else -1) * (physical.index(frame_variables[abs(v) - 1]) + 1)
                    for v in row["cut_nogood_in_F27_variables"]]
        need(actual == expected, "physical-to-F27 cut clause transport")
    invalid = [([0], list(range(1, 25)), 0), (list(range(12)), list(range(11, 24)), 0),
               (list(range(12)), list(range(12, 23)), 0),
               (list(range(12)), list(range(12, 24)), 2),
               (list(range(12)), list(range(12, 23)) + [43], 0)]
    for a, b, c in invalid:
        try:
            nogood.clause(a, b, c)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("accepted out-of-scope cut")
    return {"malformed_certificates_rejected": rejected, "cut_clause_truth_checks": truth_checks,
            "physical_to_frame_literal_transports": 288}


def run(case_doc, branch_doc):
    return {"growth": growth(), "cover": contact_cover(),
            "attachments": clique_attachments(), "negative": negative(case_doc, branch_doc)}
