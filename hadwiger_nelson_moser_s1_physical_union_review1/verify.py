#!/usr/bin/env python3
"""Independent exact checker for all 70 physical S1-on-S1 unions."""
from argparse import ArgumentParser
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_moser_all_terminal_contacts" / "certificate.json"
TARGET_CERT = HERE.parent / "hadwiger_nelson_moser_reflection_s1_host_gate" / "certificate.json"
TARGET = (0, 10, 11, 17, 18)
EXCLUDED = "00112"
COMMON = "00001"
ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, b):
    q, r, s, t = a
    Q, R, S, T = b
    return (
        q*Q + 3*r*R + 11*s*S + 33*t*T,
        q*R + r*Q + 11*s*T + 11*t*S,
        q*S + s*Q + 3*r*T + 3*t*R,
        q*T + t*Q + r*S + s*R,
    )


def inv(a):
    """Invert a nonzero element of Q(sqrt(3),sqrt(11)) exactly."""
    columns = [mul(a, tuple(F(i == j) for i in range(4))) for j in range(4)]
    rows = [[columns[j][i] for j in range(4)] + [F(i == 0)] for i in range(4)]
    for col in range(4):
        try:
            pivot = next(i for i in range(col, 4) if rows[i][col])
        except StopIteration as exc:
            raise ValueError("division by zero") from exc
        rows[col], rows[pivot] = rows[pivot], rows[col]
        divisor = rows[col][col]
        rows[col] = [x / divisor for x in rows[col]]
        for i in range(4):
            if i != col and rows[i][col]:
                factor = rows[i][col]
                rows[i] = [x - factor*y for x, y in zip(rows[i], rows[col])]
    out = tuple(rows[i][4] for i in range(4))
    need(mul(a, out) == ONE, "field inverse")
    return out


def div(a, b):
    return mul(a, inv(b))


def norm2(p, q):
    dx, dy = sub(p[0], q[0]), sub(p[1], q[1])
    return add(mul(dx, dx), mul(dy, dy))


def cross(a, b, c):
    ux, uy = sub(b[0], a[0]), sub(b[1], a[1])
    vx, vy = sub(c[0], a[0]), sub(c[1], a[1])
    return sub(mul(ux, vy), mul(uy, vx))


def unit_edges(points):
    return [(a, b) for a, b in combinations(range(len(points)), 2)
            if norm2(points[a], points[b]) == ONE]


def reflect_close_once(points):
    es = unit_edges(points)
    adj = [[] for _ in points]
    for a, b in es:
        adj[a].append(b)
        adj[b].append(a)
    out = list(points)
    seen = set(out)
    for centre, neighbours in enumerate(adj):
        for a, b in combinations(neighbours, 2):
            q = (sub(add(points[a][0], points[b][0]), points[centre][0]),
                 sub(add(points[a][1], points[b][1]), points[centre][1]))
            need(norm2(q, points[a]) == norm2(q, points[b]) == ONE,
                 "reflection contact")
            if q not in seen:
                seen.add(q)
                out.append(q)
    return out


def decode_points(rows):
    return [(tuple(F(v, 12) for v in x), tuple(F(v, 12) for v in y))
            for x, y in rows]


def build_s1():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    need(data["scale"] == 12, "source scale")
    need(data["basis"] == ["1", "sqrt3", "sqrt11", "sqrt33"], "source basis")
    s0 = decode_points(data["C"])
    need(len(s0) == len(set(s0)) == 25, "source support")
    s1 = reflect_close_once(s0)
    need(len(s1) == len(set(s1)) == 115, "S1 support")
    es = unit_edges(s1)
    need(len(es) == 447, "S1 edge census")
    moser = decode_points(data["M"])
    need(len(moser) == len(set(moser)) == 7, "Moser support")
    mes = unit_edges(moser)
    need(len(mes) == 11, "Moser edge census")
    need(set(moser) <= set(s0), "Moser containment")
    return raw, s0, s1, es, moser, mes


def enumerate_embeddings(s0, s1):
    """Distance-index intersection search, independent of the target DFS."""
    wanted = [[norm2(s0[TARGET[i]], s0[TARGET[j]]) for j in range(5)]
              for i in range(5)]
    dist = [[norm2(a, b) for b in s1] for a in s1]
    out = []
    for a in range(len(s1)):
        for b in range(len(s1)):
            if b == a or dist[a][b] != wanted[0][1]:
                continue
            for c in range(len(s1)):
                if (c in (a, b) or dist[a][c] != wanted[0][2]
                        or dist[b][c] != wanted[1][2]):
                    continue
                ds = [d for d in range(len(s1)) if d not in (a, b, c)
                      and dist[a][d] == wanted[0][3]
                      and dist[b][d] == wanted[1][3]
                      and dist[c][d] == wanted[2][3]]
                for d in ds:
                    for e in range(len(s1)):
                        if e in (a, b, c, d):
                            continue
                        if (dist[a][e] == wanted[0][4]
                                and dist[b][e] == wanted[1][4]
                                and dist[c][e] == wanted[2][4]
                                and dist[d][e] == wanted[3][4]):
                            out.append((a, b, c, d, e))
    need(len(out) == len(set(out)) == 70, "embedding census")
    return out


def map_copy(host, ids, targets):
    """Construct the unique affine map on the first three anchor roles."""
    a, b, c = [host[i] for i in ids[:3]]
    A, B, C = targets[:3]
    ux, uy = sub(b[0], a[0]), sub(b[1], a[1])
    vx, vy = sub(c[0], a[0]), sub(c[1], a[1])
    det = sub(mul(ux, vy), mul(uy, vx))
    need(det != ZERO, "host anchors collinear")
    Ux, Uy = sub(B[0], A[0]), sub(B[1], A[1])
    Vx, Vy = sub(C[0], A[0]), sub(C[1], A[1])
    out = []
    for p in host:
        dx, dy = sub(p[0], a[0]), sub(p[1], a[1])
        alpha = div(sub(mul(dx, vy), mul(dy, vx)), det)
        beta = div(sub(mul(ux, dy), mul(uy, dx)), det)
        out.append((add(A[0], add(mul(alpha, Ux), mul(beta, Vx))),
                    add(A[1], add(mul(alpha, Uy), mul(beta, Vy)))))
    need(all(out[ids[i]] == targets[i] for i in range(5)), "five-role alignment")
    return out


def canonical_union(blocker, mapped):
    points, index = [], {}
    blocker_map, host_map = [], []
    for collection, indices in ((blocker, blocker_map), (mapped, host_map)):
        for point in collection:
            if point not in index:
                index[point] = len(points)
                points.append(point)
            indices.append(index[point])
    return points, blocker_map, host_map


def word(text, n):
    need(isinstance(text, str) and len(text) == n and set(text) <= set("0123"),
         "colour word")
    return tuple(map(int, text))


def proper(colours, edges):
    return all(colours[a] != colours[b] for a, b in edges)


def chromatic_lower_bound_four(moser_edges):
    return not any(proper(colours, moser_edges) for colours in product(range(3), repeat=7))


def row_hash(rows):
    blob = "".join(",".join(map(str, row)) + "\n" for row in rows).encode()
    return sha256(blob).hexdigest()


def point_key(point):
    return tuple(str(v) for coordinate in point for v in coordinate)


def audit_target(cert, found, s1_edges):
    need(cert["schema"] == "hn-moser-reflection-s1-host-gate-v1", "target schema")
    need(cert["target_terminals"] == list(TARGET), "target terminals")
    need(cert["excluded_pattern"] == EXCLUDED, "excluded pattern")
    need(cert["common_pattern"] == COMMON, "common pattern")
    entries = cert["host_witnesses"]
    need([tuple(x["embedding"]) for x in entries] == found, "target embeddings")
    blocker = word(cert["blocker_word"], 115)
    need(proper(blocker, s1_edges), "target blocker word")
    need("".join(str(blocker[v]) for v in TARGET) == COMMON, "blocker restriction")
    for ids, entry in zip(found, entries):
        colours = word(entry["word"], 115)
        need(proper(colours, s1_edges), "target host word")
        need("".join(str(colours[v]) for v in ids) == COMMON, "host restriction")
    edge_set = set(s1_edges)
    need(all(tuple(sorted((29, v))) in edge_set for v in (0, 11, 18)),
         "first forcing contacts")
    need(all(tuple(sorted((93, v))) in edge_set for v in (10, 17, 18, 29)),
         "second forcing contacts")
    need({int(EXCLUDED[TARGET.index(v)]) for v in (0, 11, 18)} == {0, 1, 2},
         "first forcing colours")
    need({int(EXCLUDED[TARGET.index(v)]) for v in (10, 17, 18)} == {0, 1, 2},
         "second forcing colours")


def audit(cert, target_cert):
    source_raw, s0, s1, s1_edges, moser, moser_edges = build_s1()
    need(cert["schema"] == "hn-moser-s1-physical-unions-review-v1", "schema")
    need(cert["source_sha256"] == sha256(source_raw).hexdigest(), "source hash")
    need(cert["target_certificate_sha256"] == sha256(TARGET_CERT.read_bytes()).hexdigest(),
         "target hash")
    need(cert["target_terminals"] == list(TARGET), "certificate terminals")
    need(cert["s1_points"] == 115 and cert["s1_edges"] == 447, "certificate S1 census")
    found = enumerate_embeddings(s0, s1)
    need(cert["embedding_count"] == len(found), "certificate embedding count")
    need(cross(*(s0[v] for v in TARGET[:3])) != ZERO, "target anchors collinear")
    audit_target(target_cert, found, s1_edges)
    need(chromatic_lower_bound_four(moser_edges), "Moser graph is three-colourable")

    rows = cert["unions"]
    need(len(rows) == len(found), "union count")
    point_counts, edge_counts, incidental_counts = [], [], []
    for serial, (entry, ids) in enumerate(zip(rows, found)):
        need(entry["embedding"] == list(ids), f"embedding {serial}")
        mapped = map_copy(s1, ids, [s0[v] for v in TARGET])
        points, blocker_map, host_map = canonical_union(s1, mapped)
        need(len(points) == len(set(points)), f"union collision merge {serial}")
        edges = unit_edges(points)
        edge_set = set(edges)
        blocker_edges = {tuple(sorted((blocker_map[a], blocker_map[b])))
                         for a, b in s1_edges}
        host_edges = {tuple(sorted((host_map[a], host_map[b])))
                      for a, b in s1_edges}
        need(blocker_edges <= edge_set and host_edges <= edge_set,
             f"isometric copy edges {serial}")
        incidental = edge_set - blocker_edges - host_edges
        need(entry["points"] == len(points), f"point count {serial}")
        need(entry["overlap"] == 230-len(points), f"overlap count {serial}")
        need(entry["edges"] == len(edges), f"edge count {serial}")
        need(entry["incidental_edges"] == len(incidental), f"incidental count {serial}")
        need(entry["point_sha256"] == row_hash([point_key(p) for p in points]),
             f"point hash {serial}")
        need(entry["edge_sha256"] == row_hash(edges), f"edge hash {serial}")
        colours = word(entry["four_colour_word"], len(points))
        need(proper(colours, edges), f"four-colour word {serial}")
        point_counts.append(len(points))
        edge_counts.append(len(edges))
        incidental_counts.append(len(incidental))

    result = {
        "source_points": len(s0),
        "s1_points": len(s1),
        "s1_edges": len(s1_edges),
        "moser_points": len(moser),
        "moser_edges": len(moser_edges),
        "moser_chromatic_number": 4,
        "target_terminals": list(TARGET),
        "target_anchors_noncollinear": True,
        "excluded_pattern": EXCLUDED,
        "common_isolated_pattern": COMMON,
        "labeled_metric_embeddings": len(found),
        "target_positive_words_checked": 1 + len(found),
        "physical_unions": len(rows),
        "physical_point_range": [min(point_counts), max(point_counts)],
        "complete_edge_range": [min(edge_counts), max(edge_counts)],
        "incidental_edge_range": [min(incidental_counts), max(incidental_counts)],
        "unions_with_incidental_edges": sum(x > 0 for x in incidental_counts),
        "four_colour_words_checked": len(rows),
        "all_physical_unions_chromatic_number": 4,
        "record_candidate": False,
        "verdict": "ACCEPT_AND_STRENGTHEN",
        "status": "ALL_70_COMPLETE_PHYSICAL_UNIONS_EXACTLY_FOUR_CHROMATIC",
    }
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(result == expected, "EXPECTED mismatch")
    return result


def controls(cert, target_cert):
    rejected = []
    for kind in ("embedding", "colour", "point_count", "target_colour"):
        bad, bad_target = deepcopy(cert), deepcopy(target_cert)
        if kind == "embedding":
            bad["unions"][0]["embedding"][0] = 114
        elif kind == "colour":
            bad["unions"][0]["four_colour_word"] = "0" * bad["unions"][0]["points"]
        elif kind == "point_count":
            bad["unions"][0]["points"] += 1
        else:
            bad_target["blocker_word"] = "0" * 115
        try:
            audit(bad, bad_target)
        except ValueError:
            rejected.append(kind)
        else:
            raise ValueError("corruption accepted: " + kind)
    return rejected


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    certificate = json.loads((HERE / "certificate.json").read_text())
    target_certificate = json.loads(TARGET_CERT.read_text())
    output = audit(certificate, target_certificate)
    if args.controls:
        output["corruptions_rejected"] = controls(certificate, target_certificate)
    print(json.dumps(output, indent=2, sort_keys=True))
