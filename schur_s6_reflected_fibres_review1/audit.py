"""Rebuild reflected-fibre fixtures from their product-group classes."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "additive_combinatorics/schur6_reflected_fibres/fixtures.json"


def sum_free(points, a, m):
    for x in points:
        for y in points:
            if ((x[0] + y[0]) % a, (x[1] + y[1]) % m) in points:
                return False
    return True


def axis_sum_free(values, a):
    return all((x + y) % a not in values for x in values for y in values)


def differences(values, a):
    return {(x - y) % a for x in values for y in values}


def check_fixture(fixture):
    a = fixture["axis_factor"]
    n = fixture["modulus"]
    word = fixture["word"]
    assert n == 5 * a and len(word) == n - 1
    assert set(word) <= set(range(6)) and all(type(c) is int for c in word)
    positions = {(t % a, t % 5): t for t in range(1, n)}
    assert len(positions) == n - 1
    label = {point: word[t - 1] for point, t in positions.items()}
    axis = [{r for r in range(1, a) if label[(r, 0)] == c} for c in range(6)]
    q = {r: label[(r, 1)] for r in range(a)}
    assert set(q.values()) <= {0, 2, 3, 4, 5} and q[0] == 0
    residual = {r for r in range(a) if q[r] == 0}
    common = {c: {r for r in range(a) if q[r] == c} for c in range(2, 6)}
    assert set().union(*axis) == set(range(1, a))
    assert sum(map(len, axis)) == a - 1
    assert residual | set().union(*common.values()) == set(range(a))
    assert len(residual) + sum(map(len, common.values())) == a
    assert all({-r % a for r in colour} == colour for colour in axis)

    classes = []
    classes.append({(r, 0) for r in axis[0]} |
                   {(r, 1) for r in residual} |
                   {(-r % a, 4) for r in residual})
    classes.append({(r, 0) for r in axis[1]} |
                   {(r, 2) for r in residual} |
                   {(-r % a, 3) for r in residual})
    for c in range(2, 6):
        C = common[c]
        classes.append({(r, 0) for r in axis[c]} |
                       {(r, b) for r in C for b in (1, 2)} |
                       {(-r % a, b) for r in C for b in (3, 4)})
    assert sum(map(len, classes)) == n - 1
    assert set().union(*classes) == set(positions)
    assert all(label[point] == c for c, points in enumerate(classes) for point in points)
    assert all(sum_free(points, a, 5) for points in classes)
    assert all(word[t - 1] == word[n - t - 1] for t in range(1, n))

    criterion = all(axis_sum_free(colour, a) for colour in axis)
    criterion &= all(axis_sum_free(common[c] | {-r % a for r in common[c]}, a)
                     for c in range(2, 6))
    criterion &= not (axis[0] | axis[1]) & differences(residual, a)
    criterion &= all(not axis[c] & differences(common[c], a) for c in range(2, 6))
    assert criterion

    projection = [{(r, 0) for r in axis[0] | axis[1]} |
                  {(r, 1) for r in residual}]
    for c in range(2, 6):
        projection.append({(r, 0) for r in axis[c]} |
                          {(r, 1) for r in common[c]})
    assert sum(map(len, projection)) == 2 * a - 1
    project_label = {(t % a, t % 2): c for c, points in enumerate(projection)
                     for t in range(1, 2 * a) if (t % a, t % 2) in points}
    assert len(project_label) == 2 * a - 1
    pword = [project_label[(t % a, t % 2)] for t in range(1, 2 * a)]
    defects = [(x, y, (x + y) % (2 * a))
               for x in range(1, 2 * a) for y in range(x, 2 * a)
               if (x + y) % (2 * a) and
               pword[x - 1] == pword[y - 1] == pword[(x + y) % (2 * a) - 1]]
    witness = next(r for r in range(1, a) if q[r] == 0 and q[-r % a] != 0)
    assert q[0] == q[witness] == 0 and q[-witness % a] != 0
    return {
        "endpoint": n - 1,
        "sizes": [len(points) for points in classes],
        "reflection_witness": [witness, q[-witness % a]],
        "old_projection_defects": len(defects),
        "first_projection_defect": list(defects[0]),
        "mergeable_special_axis": axis_sum_free(axis[0] | axis[1], a),
    }


def main():
    fixtures = json.loads(FIXTURES.read_text())
    reports = [check_fixture(fixture) for fixture in fixtures]
    assert reports[0] == {
        "endpoint": 34, "sizes": [6, 6, 10, 8, 4, 0],
        "reflection_witness": [3, 4], "old_projection_defects": 5,
        "first_projection_defect": [2, 6, 8], "mergeable_special_axis": False,
    }
    assert reports[1] == {
        "endpoint": 234, "sizes": [38, 36, 34, 42, 30, 54],
        "reflection_witness": [4, 2], "old_projection_defects": 19,
        "first_projection_defect": [1, 7, 8], "mergeable_special_axis": True,
    }
    print("PASS endpoints=34,234 modular_sum_free=yes reflected_fibres=yes "
          "nonuniform_reflection=yes projection_defects=5,19")


if __name__ == "__main__":
    main()
