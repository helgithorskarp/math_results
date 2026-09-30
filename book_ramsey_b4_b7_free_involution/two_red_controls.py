"""Exact row contradictions and literal controls for the two-red extension.
Author: six-books-2, role researcher. Standard library, integer arithmetic.
The deterministic lifted graphs test identities, not Ramsey witnesses.
"""
from itertools import combinations, product
import json
import random
import time


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def linear(*terms):
    return tuple(sum(c * v[i] for c, v in terms) for i in range(6))


def vector_controls():
    balanced = [v for v in product([-1, 1], repeat=6) if sum(v) == 0]
    require(len(balanced) == 20, "balanced universe")
    parity_pairs = 0
    for a, b in product(balanced, repeat=2):
        require(dot(a, b) % 4 == 2 and dot(a, b) != 0,
                "shape C balanced-row parity")
        parity_pairs += 1
    rank_one = 0
    for values in product([-1, 1], repeat=4):
        p = [values[:2], values[2:]]
        if dot(p[0], p[1]) == 0:
            continue
        require(values[0] * values[3] == values[1] * values[2], "rank-one block")
        switched = [[p[i][j] * p[i][0] * p[0][j] * p[0][0]
                     for j in range(2)] for i in range(2)]
        require(switched == [[1, 1], [1, 1]], "positive switched block")
        rank_one += 1
    a_cases = 0
    for p1, p2 in product(balanced, repeat=2):
        if dot(p1, p2) != -2:
            continue
        candidates = [v for v in balanced if dot(v, p1) == dot(v, p2) == -2]
        for q1, q2 in product(candidates, repeat=2):
            if dot(q1, q2) != -2:
                continue
            p = linear((1, p1), (1, p2))
            q = linear((1, q1), (1, q2))
            require(linear((1, p), (1, q)) == (0,) * 6, "A opposite row sums")
            require(dot(p, p) == 8, "A nonzero row sum")
            p_image = linear((-3, p), (-2, q))
            q_image = linear((-1, q), (-2, p))
            require(p_image == linear((-1, p)) and q_image == q,
                    "A required images")
            require(q_image != linear((-1, p_image)), "A linearity contradiction")
            a_cases += 1
    a = (1,) * 6
    two_plus = [v for v in product([-1, 1], repeat=6) if sum(v) == -2]
    b_cases = 0
    for r1, r2 in product(two_plus, repeat=2):
        if dot(r1, r2) != -2:
            continue
        rows = [v for v in balanced if dot(v, r1) == dot(v, r2) == 0]
        for r0, r3 in product(rows, repeat=2):
            if dot(r0, r3) != -2:
                continue
            a_image = linear((-1, a), (-1, r1), (-1, r2))
            r1_image = linear((-1, a), (-3, r1), (-1, r2))
            require(dot(a_image, r1) == -2, "B first bilinear value")
            require(dot(a, r1_image) == 2, "B second bilinear value")
            require(dot(a_image, r1) != dot(a, r1_image), "B symmetry contradiction")
            b_cases += 1
    require((rank_one, a_cases, b_cases, parity_pairs) == (8, 720, 2160, 400),
            "complete vector counts")
    return {"rank_one_sign_blocks": rank_one,
            "shape_A_normalized_row_tuples": a_cases,
            "shape_B_normalized_row_tuples": b_cases,
            "shape_B_bilinear_values": [-2, 2],
            "shape_C_balanced_row_pairs": parity_pairs}


def lift(w, s, inside):
    red = [set() for _ in range(22)]
    for i, bit in enumerate(inside):
        if bit:
            red[2 * i].add(2 * i + 1)
            red[2 * i + 1].add(2 * i)
    for i, j in combinations(range(11), 2):
        for b, c in product([0, 1], repeat=2):
            if w[i][j] == 1 or (w[i][j] == 0 and (b == c) == (s[i][j] == 1)):
                red[2 * i + b].add(2 * j + c)
                red[2 * j + c].add(2 * i + b)
    blue = [set(range(22)) - {i} - red[i] for i in range(22)]
    return red, blue


def literal_controls():
    # Every integer partition of six into blocks of size at most three.
    partitions = [(1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 2), (1, 1, 2, 2),
                  (2, 2, 2), (1, 1, 1, 3), (1, 2, 3), (3, 3)]
    forms = {"A": ([(0, 1), (0, 2)], [(0, 3), (0, 4), (1, 2), (3, 4)], [0, 0, 0, 1, 1]),
             "B": ([(0, 1), (2, 3)], [(0, 2), (1, 3), (0, 4), (3, 4)], [0, 0, 0, 0, 1]),
             "C": ([(0, 1), (2, 3)], [(0, 2), (1, 3), (0, 4), (3, 4), (1, 2)], [0, 0, 0, 0, 1])}
    graphs = matching = uniform = shifts = 0
    for form, (red_pairs, blue_pairs, fixed_inside) in forms.items():
        for sizes in partitions:
            blocks = []
            start = 5
            for size in sizes:
                blocks.append(tuple(range(start, start + size)))
                start += size
            require(start == 11, "six outside orbits")
            low_blue = [e for block in blocks for e in combinations(block, 2)]
            for seed in range(8):
                rng = random.Random(seed)
                w = [[0] * 11 for _ in range(11)]
                s = [[0] * 11 for _ in range(11)]
                for i, j in red_pairs:
                    w[i][j] = w[j][i] = 1
                for i, j in blue_pairs + low_blue:
                    w[i][j] = w[j][i] = -1
                for i, j in combinations(range(11), 2):
                    if w[i][j] == 0:
                        s[i][j] = s[j][i] = rng.choice([-1, 1])
                u = [sum(row) for row in w]
                w2 = [[dot(row, col) for col in w] for row in w]
                s2 = [[dot(row, col) for col in s] for row in s]
                t = [[s[h][k] + (u[h] if h == k else 0)
                      for k in range(5, 11)] for h in range(5, 11)]
                for outside_bit in [0, 1]:
                    inside = fixed_inside + [outside_bit] * 6
                    red, blue = lift(w, s, inside)
                    for i, j in combinations(range(11), 2):
                        if w[i][j] == 0:
                            rn = 9 + u[i] + u[j] + w2[i][j] + s[i][j] * s2[i][j]
                            bn = 9 - u[i] - u[j] + w2[i][j] - s[i][j] * s2[i][j]
                            require(rn % 2 == bn % 2 == 0, "integral matching pages")
                            for b, c in product([0, 1], repeat=2):
                                v, z = 2 * i + b, 2 * j + c
                                color = red if z in red[v] else blue
                                require(len(color[v] & color[z]) == (rn if color is red else bn) // 2,
                                        "literal matching pages")
                                matching += 1
                        else:
                            color = red if w[i][j] == 1 else blue
                            outside = sum((1 + w[i][k]) * (1 + w[j][k]) if color is red
                                          else (1 - w[i][k]) * (1 - w[j][k])
                                          for k in range(11) if k not in (i, j))
                            predicted = outside + 2 * (inside[i] + inside[j] if color is red
                                                       else 2 - inside[i] - inside[j])
                            for b in [0, 1]:
                                observed = [len(color[2 * i + b] & color[2 * j + c]) for c in [0, 1]]
                                require(sum(observed) == predicted, "literal uniform sum")
                                require(observed[0] - observed[1] == (1 if b == 0 else -1) * s2[i][j],
                                        "literal uniform difference")
                                uniform += 1
                    for i in range(5):
                        for h in range(5, 11):
                            require(w2[i][h] == 0 and abs(s[i][h]) == 1,
                                    "active/outside matching hypothesis")
                            shifted = sum(s[i][k] * t[k - 5][h - 5] for k in range(5, 11))
                            shifted += sum(s[i][j] * s[j][h] for j in range(5))
                            shifted += (3 + u[i]) * s[i][h]
                            general = s2[i][h] + (3 + u[i] + u[h]) * s[i][h]
                            c = 0 if s[i][h] == 1 else 1
                            actual = 2 * s[i][h] * (len(red[2 * i] & red[2 * h + c]) - 3)
                            require(shifted == general == actual, "literal diagonal-shift residual")
                            shifts += 1
                    graphs += 1
    return {"deterministic_lifted_graphs": graphs,
            "literal_matching_spine_checks": matching,
            "literal_uniform_sum_difference_checks": uniform,
            "literal_diagonal_shift_checks": shifts,
            "outside_clique_partitions": len(partitions),
            "matching_sign_seeds_per_shape_partition": 8,
            "outside_inside_patterns_per_seed": 2,
            "full_matching_sign_enumeration": False}


def main():
    start = time.monotonic()
    result = {"agent": "six-books-2", "role": "researcher", "complete": True,
              "vector_controls": vector_controls(), "literal_controls": literal_controls(),
              "validation_not_theorem_premise": True,
              "wall_seconds": time.monotonic() - start}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
