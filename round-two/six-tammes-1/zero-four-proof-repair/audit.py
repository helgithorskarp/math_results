"""Separate same-author bit-incidence audit; imports no primary checker code."""
from pathlib import Path
from itertools import combinations, permutations, product
import hashlib
import json

ROOT = Path(__file__).resolve().parent
NAMES = ("U", "V", "F", "G", "X", "S", "B")
PAIRS = list(combinations(range(7), 2))


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def mask(face):
    need(len(face) in (3, 4) and len(set(face)) == len(face), "simple face")
    code = 0
    for i, v in enumerate(face):
        code |= 1 << PAIRS.index(tuple(sorted((v, face[(i+1) % len(face)]))))
    return code


def neighbors(code, v):
    ns = 0
    for k, (a, b) in enumerate(PAIRS):
        if code >> k & 1:
            if a == v:
                ns |= 1 << b
            if b == v:
                ns |= 1 << a
    return ns


def common(code, a, b):
    return [v for v in range(7) if (neighbors(code, a) & neighbors(code, b)) >> v & 1]


def union(fs):
    code = 0
    for f in fs:
        code |= mask(f)
    return code


def labelled(indices):
    return [NAMES[i] for i in indices]


def links():
    pairs = list(combinations(range(4), 2))
    cycles = []
    for chosen in combinations(range(6), 4):
        ns = [0] * 4
        for k in chosen:
            a, b = pairs[k]
            ns[a] |= 1 << b
            ns[b] |= 1 << a
        if any(m.bit_count() != 2 for m in ns):
            continue
        first = min(i for i in range(4) if ns[0] >> i & 1)
        path = [0, first]
        while len(path) < 4:
            nxt = [i for i in range(4) if ns[path[-1]] >> i & 1 and i != path[-2]]
            need(len(nxt) == 1 and nxt[0] not in path, "four-cycle connected traversal")
            path.append(nxt[0])
        need(ns[path[-1]] & 1, "closed four-cycle")
        cycles.append((tuple(path), ns))
    need(len(cycles) == 3, "all degree-two four-vertex edge sets")
    good = sorted((p, ns) for p, ns in cycles if ns[0] >> 2 & 1 and ns[1] >> 3 & 1)
    c5 = [r for r in good if r[1][0] >> 1 & 1]
    c7 = [r for r in good if not r[1][0] >> 1 & 1]
    need(len(good) == 2 and len(c5) == len(c7) == 1, "all known-corner link alternatives")
    names = ("U", "V", "X", "S")
    return {"all_undirected_cycles": 3,
            "known_UX_VS_corner_cycles": [[names[i] for i in p] for p, ns in good],
            "C5_shared_one_T_A_cycle": [names[i] for i in c5[0][0]],
            "C7_only_B_common_cycle": [names[i] for i in c7[0][0]],
            "XS_is_corner_in_C5": bool(c5[0][1][2] >> 3 & 1),
            "XS_is_corner_in_C7": bool(c7[0][1][2] >> 3 & 1)}


def main():
    cert = json.loads((ROOT / "certificate.json").read_text())
    need(cert["roles"] == list(NAMES) and cert["cosine_scope"] == "0<c<1", "role/domain certificate")
    fs = [tuple(NAMES.index(v) for v in row["vertices"]) for row in cert["faces"]]
    need(fs == [(2, 3, 5), (0, 2, 4, 6), (1, 3, 5, 6)], "literal source face incidence")
    need(cert["witness"] == {"pair": ["F", "B"], "distinct_common_contacts": ["U", "X", "S"]}, "literal certificate witness")
    full = union(fs)
    need(common(full, 2, 6) == [0, 4, 5], "three different original contacts")
    need([p for p in PAIRS if len(common(full, *p)) > 2] == [(2, 6)], "unique common-contact capacity violation")
    variants = [sorted(p for p in permutations(f) if mask(p) == mask(f)) for f in fs]
    need([len(v) for v in variants] == [6, 8, 8], "all boundary-preserving label permutations")
    stream = hashlib.sha256()
    count = 0
    for triple in product(*variants):
        code = union(triple)
        edges = [list(p) for k, p in enumerate(PAIRS) if code >> k & 1]
        record = [list(map(list, triple)), edges, common(code, 2, 6)]
        stream.update((json.dumps(record, separators=(",", ":")) + "\n").encode())
        need(code == full, "every incidence mask is identical")
        count += 1
    deletions = []
    for i, row in enumerate(cert["faces"]):
        code = union(fs[:i] + fs[i+1:])
        need(all(len(common(code, *p)) <= 2 for p in PAIRS), "released-face necessary assignments")
        deletions.append([row["name"], labelled(common(code, 2, 6))])
    controls = []
    for w in (0, 4, 5):
        for v in (2, 6):
            pair = tuple(sorted((v, w)))
            code = full & ~(1 << PAIRS.index(pair))
            need(len(common(code, 2, 6)) == 2, "single-edge damage cannot certify three commons")
            controls.append([labelled(pair), labelled(common(code, 2, 6))])
    aliases = []
    for w in (0, 4):
        code = union([tuple(w if v == 5 else v for v in f) for f in fs])
        need(len(common(code, 2, 6)) == 2, "distinct original witness requirement")
        aliases.append(["S=" + NAMES[w], labelled(common(code, 2, 6))])
    vectors = [(0, 0, 1), (0, 0, -1), (1, 0, 0), (0, 1, 0), (-1, 0, 0)]
    need(len(set(vectors)) == 5, "five distinct c=0 vectors")
    for i in range(5):
        need(sum(v*v for v in vectors[i]) == 1, "unit c=0 control")
    for i in (0, 1):
        for j in (2, 3, 4):
            need(sum(vectors[i][k]*vectors[j][k] for k in range(3)) == 0, "antipodal zero contact planes")
    return {"actual_author": "six-tammes-1", "role": "researcher",
            "claim_status": "explicit correction/reduction of a published source proof using a prior geometric fact",
            "known_contact_edges": [labelled(p) for k, p in enumerate(PAIRS) if full >> k & 1],
            "witness_pair": ["F", "B"], "distinct_common_contacts": ["U", "X", "S"],
            "face_orientation_cases": count, "all_orientation_records_sha256": stream.hexdigest(),
            "face_deletion_controls": deletions, "single_witness_edge_deletion_controls": controls,
            "coincident_name_controls": aliases, "zero_four_link_audit": links(),
            "zero_cosine_control": {"vectors_F_B_U_X_S": vectors, "common_zero_contacts": 3,
                "purpose": "the positive-c bound is not applied at c=0; no T/Q face template is asserted"},
            "released_incidence_controls_are_not_packings": True,
            "complete_nine_Q_catalogue_proof": False, "global_Tammes15_bound": False}


if __name__ == "__main__":
    print(json.dumps(main(), sort_keys=True, indent=2))
