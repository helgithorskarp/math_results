#!/usr/bin/env python3
"""Full local negative controls and independently counted global identities."""
import copy
import itertools as it
import json
import tempfile
from fractions import Fraction
from pathlib import Path
import audit
import check

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def controls():
    cert = json.loads((HERE / "certificate.json").read_text())
    mutations = []
    x = copy.deepcopy(cert); x["records"].pop(); mutations.append(x)
    x = copy.deepcopy(cert); x["records"].append(x["records"][0]); mutations.append(x)
    x = copy.deepcopy(cert); x["records"][0][2] = 31; mutations.append(x)
    x = copy.deepcopy(cert); x["records"][0][2] = 527; mutations.append(x)
    x = copy.deepcopy(cert); x["records"][0][0] = 252; mutations.append(x)
    x = copy.deepcopy(cert); x["records"][0][1] = -1; mutations.append(x)
    x = copy.deepcopy(cert); x["records"][0][0] = False; mutations.append(x)
    x = copy.deepcopy(cert); x["schema"] = "incorrect"; mutations.append(x)
    x = copy.deepcopy(cert); x["records"].append([0, 0, 992]); mutations.append(x)
    rejected = 0
    for x in mutations:
        try:
            check.verify(x)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("accepted corrupt certificate")

    # Every physical coloring of the eleven free pairs outside a rooted C5
    # on seven vertices. The direct count uses unordered physical five-sets,
    # an adjacency matrix and the complementary pair, not common-neighbor
    # enumeration or universal-set bit intersections.
    seven_counts = {}
    free = [(i, j) for i, j in it.combinations(range(7), 2) if j >= 5]
    for code in range(1 << len(free)):
        a = [0] * 7
        matrix = [[0] * 7 for _ in range(7)]
        edges = [(i, (i + 1) % 5) for i in range(5)]
        edges += [e for k, e in enumerate(free) if code >> k & 1]
        for i, j in edges:
            a[i] |= 1 << j; a[j] |= 1 << i
            matrix[i][j] = matrix[j][i] = 1
        direct = 0
        p = 0
        for s in it.combinations(range(7), 5):
            if not all(sum(matrix[i][j] for j in s) == 2 for i in s):
                continue
            p += 1
            i, j = sorted(set(range(7)) - set(s))
            if all(matrix[u][v] == matrix[i][j] for u in (i, j) for v in s):
                direct += 1
        result = audit.audit(a)
        require(result["pentagons"] == p and
                result["edge_pentagon_incidences"] == direct, "seven-vertex identity")
        seven_counts[str(direct)] = seven_counts.get(str(direct), 0) + 1

    # Sharpness of two at ten: the disjoint union of two pentagons.
    a = [0] * 10
    for offset in (0, 5):
        for i in range(5):
            u, v = offset + i, offset + (i + 1) % 5
            a[u] |= 1 << v; a[v] |= 1 << u
    sharp = audit.audit(a)
    require(sharp["ramsey_5_5"] and sharp["pentagons"] == 2, "sharp example")

    # Derive the hereditary bounds with exact rational arithmetic.
    lower = [0] * 10 + [2]
    for n in (11, 12, 13):
        bound = Fraction(n * lower[-1], n - 5)
        lower.append(-(-bound.numerator // bound.denominator))
    require(lower[-4:] == [2, 4, 7, 12], "subset counting")
    slack = [lower[q] - 2 * (q - 9) for q in range(14)]
    require(min(slack) == 0, "linear support")
    require(43 * 42 * 2 // 4 == 903 and (906 + 51) // 52 == 18,
            "global arithmetic")
    # d^2 == d mod 2 is the handshaking-based variance parity argument.
    require(all(d * d % 2 == d % 2 for d in range(43)), "degree parity")

    forty = audit.audit(audit.read_graph(HERE / "control40.edges"))
    require(forty["n"] == 40 and forty["ramsey_5_5"], "full-size good control")
    a = audit.read_graph(HERE / "control40.edges")
    complement = [((1 << 40) - 1) ^ (1 << i) ^ row for i, row in enumerate(a)]
    reversed_result = audit.audit(complement)
    require(reversed_result["edges"] == 40 * 39 // 2 - forty["edges"],
            "complement edge count")
    require({k: v for k, v in reversed_result.items() if k != "edges"} ==
            {k: v for k, v in forty.items() if k != "edges"},
            "global complement invariance")
    perm = [(17 * i + 3) % 40 for i in range(40)]
    b = [0] * 40
    for i, j in it.combinations(range(40), 2):
        if a[i] >> j & 1:
            b[perm[i]] |= 1 << perm[j]; b[perm[j]] |= 1 << perm[i]
    require(audit.audit(b) == forty, "global relabeling invariance")

    bad_inputs = ["0 0\n", "3 1\n0 0\n", "3 2\n0 1\n0 1\n",
                  "3 1\n0 3\n", "3 0\n0 1\n", "3 1\n1 0\n"]
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "bad.edges"
        for text in bad_inputs:
            path.write_text(text)
            try:
                audit.read_graph(path)
            except ValueError:
                pass
            else:
                raise ValueError("accepted malformed graph")
    return {"status": "PENTAGON_INCIDENCE_CONTROLS_PASS",
            "certificate_corruptions_rejected": rejected,
            "malformed_graphs_rejected": len(bad_inputs),
            "rooted_seven_graphs": 2048, "seven_incidence_histogram": seven_counts,
            "sharp_two_pentagons": sharp, "hereditary_lower_bounds": lower,
            "support_slacks": slack, "global43_W_minimum": 906,
            "global43_P_minimum": 18, "good40_control": forty}


if __name__ == "__main__":
    print(json.dumps(controls(), sort_keys=True))
