#!/usr/bin/env python3
"""Transport a certified physical cut; no graph search or solver is run."""
import argparse
import itertools as it
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def instantiate(vertices, color, package=HERE):
    if (len(vertices) != 19 or len(set(vertices)) != 19 or
            any(type(v) is not int or not 0 <= v < 43 for v in vertices)):
        raise ValueError("vertices must be 19 distinct integers in [0,42]")
    if type(color) is not int or color not in (0, 1):
        raise ValueError("color must be 0 (blue) or 1 (red)")
    data = json.loads((package / "TEMPLATE.json").read_text())
    pairs = list(it.combinations(range(43), 2))
    ids = {p: i + 1 for i, p in enumerate(pairs)}
    pair = lambda u, v: tuple(sorted((vertices[u], vertices[v])))
    # The physical cut is a disjunction of the displayed signed pair literals.
    physical = [[*pair(u, v), 1 - (c if color else 1 - c)]
                for u, v, c in data["fixed"]]
    guard = [(2 * truth - 1) * ids[u, v] for u, v, truth in physical]
    local_map = [(2 * color - 1) * ids[pair(u, v)]
                 for u, v in data["local_pairs"]]
    premises = []
    for p in data["premises"]:
        subset = sorted(vertices[v] for v in p["vertices"])
        forbidden = p["color"] if color else 1 - p["color"]
        premises.append({"vertices": subset, "color": forbidden,
                         "clause": [(1 - 2 * forbidden) * ids[e]
                                    for e in it.combinations(subset, 2)]})
    proof = []
    for line in (package / "proof.rup").read_text().splitlines():
        xs = list(map(int, line.split()))
        if not xs or xs[-1] != 0 or 0 in xs[:-1]:
            raise ValueError("invalid proof line")
        proof.append(guard + [(1 if x > 0 else -1) * local_map[abs(x) - 1]
                              for x in xs[:-1]])
    return {"n": 43, "vertices": vertices, "color": color,
            "physical_clause": physical, "canonical_clause": guard,
            "canonical_premises": premises, "canonical_rup": proof}


def receive(cut, mapping):
    """Substitute an explicit complete physical edge map, with constants.

    Edge entries are [u,v,"var",positive_id] or [u,v,"fixed",red_bit].
    A positive SAT variable must mean RED. A receiver with opposite polarity
    must normalize its map before calling. No compact-CNF numbering is assumed.
    """
    table, used = {}, set()
    for entry in mapping["edges"]:
        if len(entry) != 4:
            raise ValueError("invalid mapping entry")
        u, v, kind, value = entry
        if (type(u) is not int or type(v) is not int or
                not 0 <= u < v < 43 or (u, v) in table):
            raise ValueError("invalid or duplicate physical pair")
        if type(value) is not int:
            raise ValueError("map values must be integers")
        if kind == "var":
            if value <= 0 or value in used:
                raise ValueError("variables must be positive and injective")
            used.add(value)
        elif kind != "fixed" or value not in (0, 1):
            raise ValueError("invalid map type or fixed bit")
        table[u, v] = kind, value
    if len(table) != 903:
        raise ValueError("supply all 903 physical pairs")
    clause = []
    for u, v, truth in cut["physical_clause"]:
        kind, value = table[u, v]
        if kind == "fixed":
            if value == truth:
                return {"status": "TAUTOLOGY", "clause": []}
        else:
            clause.append((2 * truth - 1) * value)
    result = {"status": "CLAUSE" if clause else "CONFLICT", "clause": clause}
    if not clause and all(kind == "fixed" for kind, value in table.values()):
        for premise in cut["canonical_premises"]:
            vertices, color = premise["vertices"], premise["color"]
            if all(table[e][1] == color for e in it.combinations(vertices, 2)):
                result["monochromatic_five"] = {"vertices": vertices, "color": color}
                break
        else:
            raise ValueError("complete rejected graph has no certified physical witness")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", required=True,
                        help="19 comma-separated labels: root then five modules")
    parser.add_argument("--color", type=int, choices=(0, 1), required=True)
    parser.add_argument("--map", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    cut = instantiate(list(map(int, args.vertices.split(","))), args.color)
    if args.map:
        cut["receiver"] = receive(cut, json.loads(args.map.read_text()))
    args.out.write_text(json.dumps(cut, separators=(",", ":")) + "\n")
    print(json.dumps({"guard_literals": len(cut["physical_clause"]),
                      "proof_additions": len(cut["canonical_rup"]),
                      "receiver_status": cut.get("receiver", {}).get("status")}))


if __name__ == "__main__":
    main()
