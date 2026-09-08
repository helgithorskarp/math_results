#!/usr/bin/env python3
"""Exact source audit and four-colouring certificate; Python standard library."""
import argparse
import ast
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
SPINDLE = [(0, 0, 0, 0), (12, 0, 0, 0), (6, 0, 6, 0),
           (18, 0, 6, 0), (10, 0, 0, 2), (5, -1, 5, 1), (15, -1, 5, 3)]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def validate_rows(rows):
    require(isinstance(rows, list) and bool(rows), "empty or malformed rows")
    require(all(isinstance(r, list) and len(r) == 4 and
                all(type(x) is int for x in r) for r in rows), "coordinate type")
    require(len({tuple(r) for r in rows}) == len(rows), "coincident vertices")


def fast_norm(row):
    # Row / 12 = ((a+b sqrt33)/12, (c sqrt3+d sqrt11)/12).
    a, b, c, d = row
    return a*a + 33*b*b + 3*c*c + 11*d*d, 2*(a*b + c*d)


def multiply(x, y):
    # Independent definition: Q[s,t]/(s^2-3,t^2-11), basis 1,s,t,st.
    answer = [0]*4
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            common = i & j
            answer[i ^ j] += a*b*(3 if common & 1 else 1)*(11 if common & 2 else 1)
    return answer


def generic_norm(row):
    a, b, c, d = row
    x = multiply((a, 0, 0, b), (a, 0, 0, b))
    y = multiply((0, c, d, 0), (0, c, d, 0))
    return tuple(u+v for u, v in zip(x, y))


def edges(rows):
    out = []
    for i, j in combinations(range(len(rows)), 2):
        delta = tuple(x-y for x, y in zip(rows[i], rows[j]))
        n, m = fast_norm(delta)
        require(generic_norm(delta) == (n, 0, 0, m), "independent norm mismatch")
        if (n, m) == (144, 0):
            out.append([i, j])
    return out


def moser_numerators(row):
    # row = (A+B*omega+C*u+D*omega*u)/3 in physical complex coordinates.
    a, b, c, d = row
    q = [Fraction(a-c-5*d-5*b, 4), Fraction(c+5*b, 2),
         Fraction(3*(d+b), 2), Fraction(-3*b)]
    require(all(x.denominator == 1 for x in q), "point outside (1/3) Moser lattice")
    A, B, C, D = map(int, q)
    # Reconstruct the original row with a separate forward expression.
    reconstructed = [Fraction(12*A+6*B+10*C+5*D, 3), Fraction(-D, 3),
                     Fraction(6*B+5*D, 3), Fraction(2*C+D, 3)]
    require(reconstructed == row, "Moser coordinate round trip")
    return A, B, C, D


def formula_words(rows):
    q = list(map(moser_numerators, rows))
    return ["".join(str((a+b+d) % 2 + 2*((a+c+d) % 2)) for a, b, c, d in q),
            "".join(str((a+d) % 2 + 2*((b+c+d) % 2)) for a, b, c, d in q)]


def check_word(word, n, edge_list):
    require(type(word) is str and len(word) == n and set(word) <= set("0123"),
            "invalid colouring alphabet/length")
    require(all(word[i] != word[j] for i, j in edge_list), "monochromatic unit edge")


def parse_data(data, name):
    # Deliberately do not run Sage/Python from the external archive.
    tree = ast.parse(data.decode())
    require(len(tree.body) == 1 and isinstance(tree.body[0], ast.Assign), "assignment")
    stmt = tree.body[0]
    require(len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name)
            and stmt.targets[0].id == name, "assignment name")

    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return Fraction(node.value)
        if isinstance(node, (ast.List, ast.Tuple)):
            return [visit(x) for x in node.elts]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            return visit(node.left)/visit(node.right)
        raise ValueError("unsupported external syntax")
    return visit(stmt.value)


def audit_archive(path, rows, edge_list, provenance):
    data = Path(path).read_bytes()
    require(hashlib.sha256(data).hexdigest() == provenance["archive_sha256"], "archive hash")
    with ZipFile(path) as archive:
        files = {}
        for name, sha in provenance["member_sha256"].items():
            b = archive.read(name)
            require(hashlib.sha256(b).hexdigest() == sha, "member hash: " + name)
            files[name] = b
    raw = parse_data(files["W_circles_607_vertices.sage"], "L")
    converted = []
    for x, y in raw:
        require(len(x) == len(y) == 4 and x[1] == x[2] == y[0] == y[3] == 0,
                "source field membership")
        scaled = [12*x[0], 12*x[3], 12*y[1], 12*y[2]]
        require(all(v.denominator == 1 for v in scaled), "source coordinate scale")
        converted.append(list(map(int, scaled)))
    require(converted == rows, "source rows, including order")
    supplied = parse_data(files["W_circles_607_edges.sage"], "Edges")
    require(all(len(e) == 2 and all(v.denominator == 1 for v in e) for e in supplied),
            "source edge types")
    supplied = [sorted([int(a)-1, int(b)-1]) for a, b in supplied]
    require(len(supplied) == len({tuple(e) for e in supplied}), "source repeated edge")
    require(sorted(supplied) == edge_list, "source exact edge equality")
    return {"source_rows_equal": True, "source_edges_equal": True,
            "source_members_hashed": len(files)}


def controls(rows, edge_list, word):
    bad_words = [word[:-1], "4"+word[1:]]
    i, j = edge_list[0]
    bad = list(word)
    bad[j] = bad[i]
    bad_words.append("".join(bad))
    for bad in bad_words:
        try:
            check_word(bad, len(rows), edge_list)
        except ValueError:
            pass
        else:
            raise ValueError("bad colouring accepted")
    malformed = [[], [[True, 0, 0, 0]], [[0, 0, 0]], [[0, 0, 0, 0]]*2]
    for bad in malformed:
        try:
            validate_rows(bad)
        except ValueError:
            pass
        else:
            raise ValueError("bad coordinates accepted")
    for bad in [b"L = __import__('os')", b"X = []", b"L = []; X = 1"]:
        try:
            parse_data(bad, "L")
        except ValueError:
            pass
        else:
            raise ValueError("unsafe source syntax accepted")
    require(parse_data(b"L = [(1/3, -2/5, 0)]", "L") ==
            [[Fraction(1, 3), Fraction(-2, 5), 0]], "rational parse")
    # The mod-four identity in Ducz's first colouring, every residue tuple.
    for a, b, c, d in product(range(4), repeat=4):
        N = 6*(a*a+a*b+b*b+c*c+c*d+d*d)+10*a*c+5*a*d+5*b*c+10*b*d
        M = b*c-a*d
        l1, l2 = (a+b+d) % 2, (a+c+d) % 2
        require((N+M) % 2 == 0 and ((N+M)//2) % 2 == (l1+l2+l1*l2) % 2,
                "parity identity")
    return {"bad_words_rejected": 3, "bad_coordinates_rejected": 4,
            "unsafe_source_syntax_rejected": 3, "parity_residue_tuples": 256}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author-archive", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    rows = json.loads((HERE/"coordinates.json").read_text())
    cert = json.loads((HERE/"certificate.json").read_text())
    validate_rows(rows)
    require(len(rows) == 607, "source order")
    edge_list = edges(rows)
    require(len(edge_list) == 3390, "strict size")
    words = formula_words(rows)
    require(words == cert["formula_words"], "arithmetic word mismatch")
    for word in words + [cert["discovery_word"]]:
        check_word(word, len(rows), edge_list)
    ids = cert["spindle_labels"]
    require(len(ids) == 7 and len(set(ids)) == 7 and
            all(type(i) is int and 0 <= i < len(rows) for i in ids), "spindle labels")
    base = rows[ids[0]]
    require([tuple(x-y for x, y in zip(rows[i], base)) for i in ids] == SPINDLE,
            "translated spindle coordinates")
    small_edges = edges(SPINDLE)
    require(len(small_edges) == 11, "spindle size")
    proper3 = sum(all(c[i] != c[j] for i, j in small_edges)
                  for c in product(range(3), repeat=7))
    require(proper3 == 0, "spindle three-colourability")
    result = {"verified": True, "vertices": len(rows), "strict_edges": len(edge_list),
              "all_point_pairs_checked_by_two_norms": len(rows)*(len(rows)-1)//2,
              "coordinates_sha256": digest(rows), "edges_sha256": digest(edge_list),
              "moser_lattice_divided_by_three_members": len(rows),
              "proper_four_colour_words": 3, "formula_words_sha256": digest(words),
              "spindle_labels": ids, "spindle_three_colour_assignments": 3**7,
              "spindle_proper_three_colourings": proper3, "chromatic_number": 4,
              "non_four_colourability_gate_passed": False, "record_improvement": False,
              "controls": controls(rows, edge_list, words[0])}
    if args.check_expected:
        require(result == json.loads((HERE/"expected.json").read_text()), "expected output")
    if args.author_archive:
        result["source_audit"] = audit_archive(args.author_archive, rows, edge_list,
                                              json.loads((HERE/"provenance.json").read_text()))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
