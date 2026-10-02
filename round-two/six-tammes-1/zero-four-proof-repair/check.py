"""Regenerate the source-proof repair certificate; Python standard library only."""
from pathlib import Path
from itertools import permutations, combinations, product
import hashlib
import json

ROOT = Path(__file__).resolve().parent
NAMES = ("U", "V", "F", "G", "X", "S", "B")


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(a, b):
    need(a != b, "self contact")
    return tuple(sorted((a, b)))


def boundary(face):
    need(len(face) in (3, 4) and len(set(face)) == len(face), "simple T/Q boundary")
    return {edge(a, b) for a, b in zip(face, face[1:] + face[:1])}


def graph(faces):
    return set().union(*(boundary(f) for f in faces)) if faces else set()


def common(edges, a, b):
    return sorted({v for u, v in edges if u == a} | {u for u, v in edges if v == a}) if a == b else sorted(
        ({v for u, v in edges if u == a} | {u for u, v in edges if v == a}) &
        ({v for u, v in edges if u == b} | {u for u, v in edges if v == b}))


def labels(indices):
    return [NAMES[i] for i in indices]


def orientations(face):
    return sorted({q[i:] + q[:i] for q in (face, face[::-1]) for i in range(len(face))})


def link_cover():
    # At B, indices mean U,V,X,S. Cycles are anchored at U, modulo reversal.
    cycles = sorted({min((0,) + p, (0,) + p[::-1]) for p in permutations((1, 2, 3))})
    required = {edge(0, 2), edge(1, 3)}
    good = [q for q in cycles if required <= boundary(q)]
    c5 = [q for q in good if edge(0, 1) in boundary(q)]
    c7 = [q for q in good if edge(0, 1) not in boundary(q)]
    need(len(cycles) == 3 and len(good) == 2 and len(c5) == len(c7) == 1, "complete four-link cover")
    names = ("U", "V", "X", "S")
    return {"all_undirected_cycles": len(cycles),
            "known_UX_VS_corner_cycles": [[names[i] for i in q] for q in good],
            "C5_shared_one_T_A_cycle": [names[i] for i in c5[0]],
            "C7_only_B_common_cycle": [names[i] for i in c7[0]],
            "XS_is_corner_in_C5": edge(2, 3) in boundary(c5[0]),
            "XS_is_corner_in_C7": edge(2, 3) in boundary(c7[0])}


def zero_control():
    vs = [(0, 0, 1), (0, 0, -1), (1, 0, 0), (0, 1, 0), (-1, 0, 0)]
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    need(len(set(vs)) == 5 and all(dot(v, v) == 1 for v in vs), "five distinct exact unit vectors")
    need(all(dot(vs[i], vs[j]) == 0 for i in (0, 1) for j in (2, 3, 4)), "zero-cosine exception")
    return {"vectors_F_B_U_X_S": vs, "common_zero_contacts": 3,
            "purpose": "the positive-c bound is not applied at c=0; no T/Q face template is asserted"}


def main():
    cert = json.loads((ROOT / "certificate.json").read_text())
    need(tuple(cert["roles"]) == NAMES and cert["cosine_scope"] == "0<c<1", "certificate domain/roles")
    faces = [tuple(NAMES.index(x) for x in f["vertices"]) for f in cert["faces"]]
    need(faces == [(2, 3, 5), (0, 2, 4, 6), (1, 3, 5, 6)], "three named source faces")
    pair = tuple(NAMES.index(x) for x in cert["witness"]["pair"])
    claimed = [NAMES.index(x) for x in cert["witness"]["distinct_common_contacts"]]
    edges = graph(faces)
    need(pair == (2, 6) and claimed == [0, 4, 5], "specified positive-common-contact witness")
    need(common(edges, *pair) == claimed and len(set(claimed)) == 3, "all six witness contacts and distinctness")
    all_pairs = {p: common(edges, *p) for p in combinations(range(7), 2)}
    need([p for p, ns in all_pairs.items() if len(ns) > 2] == [(2, 6)], "unique overfull common pair")
    stream = hashlib.sha256()
    count = 0
    for fs in product(*(orientations(f) for f in faces)):
        e = graph(fs)
        record = [list(map(list, fs)), list(map(list, sorted(e))), common(e, *pair)]
        stream.update((json.dumps(record, separators=(",", ":")) + "\n").encode())
        need(e == edges and common(e, *pair) == claimed, "orientation witness invariance")
        count += 1
    need(count == 384, "all 6*8*8 oriented face presentations")
    deletions = []
    for i, face in enumerate(cert["faces"]):
        remaining = graph(faces[:i] + faces[i+1:])
        need(all(len(common(remaining, *p)) <= 2 for p in combinations(range(7), 2)), "released-face necessary control")
        deletions.append([face["name"], labels(common(remaining, *pair))])
    edge_controls = []
    for w in claimed:
        for v in pair:
            deleted = edge(v, w)
            released = edges - {deleted}
            need(len(common(released, *pair)) == 2, "deleting one witness edge releases this certificate")
            edge_controls.append([labels(deleted), labels(common(released, *pair))])
    aliases = []
    for target in (0, 4):
        aliased = [tuple(target if v == 5 else v for v in f) for f in faces]
        ns = common(graph(aliased), *pair)
        need(len(ns) == 2, "coincident witness names are not counted three times")
        aliases.append(["S=" + NAMES[target], labels(ns)])
    return {"actual_author": "six-tammes-1", "role": "researcher",
            "claim_status": "explicit correction/reduction of a published source proof using a prior geometric fact",
            "known_contact_edges": [labels(e) for e in sorted(edges)],
            "witness_pair": labels(pair), "distinct_common_contacts": labels(claimed),
            "face_orientation_cases": count, "all_orientation_records_sha256": stream.hexdigest(),
            "face_deletion_controls": deletions, "single_witness_edge_deletion_controls": edge_controls,
            "coincident_name_controls": aliases, "zero_four_link_audit": link_cover(),
            "zero_cosine_control": zero_control(), "released_incidence_controls_are_not_packings": True,
            "complete_nine_Q_catalogue_proof": False, "global_Tammes15_bound": False}


if __name__ == "__main__":
    print(json.dumps(main(), sort_keys=True, indent=2))
