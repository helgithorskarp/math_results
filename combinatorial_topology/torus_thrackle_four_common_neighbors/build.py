"""Emit the cyclic K_{2,4} rotation certificate; Python 3.11, standard library."""
import json


def build():
    paths = {}
    for i in range(4):
        paths[f"e{i}"] = (
            ["u"] + [f"x{i}{(i+s)%4}" for s in (2, 3, 1)] + [f"w{i}"]
        )
        paths[f"f{i}"] = (
            ["v"] + [f"x{(i+s)%4}{i}" for s in (1, 3, 2)] + [f"w{i}"]
        )
    rotations = {
        "u": [paths[f"e{i}"][1] for i in range(4)],
        "v": [paths[f"f{i}"][1] for i in range(4)],
    }
    for i in range(4):
        rotations[f"w{i}"] = [paths[f"e{i}"][-2], paths[f"f{i}"][-2]]
        for j in range(4):
            if i == j:
                continue
            x = f"x{i}{j}"
            e, f = paths[f"e{i}"], paths[f"f{j}"]
            p, q = e.index(x), f.index(x)
            a, b, c, d = e[p-1], e[p+1], f[q-1], f[q+1]
            rotations[x] = [a, d, b, c] if (j-i) % 4 == 1 else [a, c, b, d]
    return {
        "schema": "oriented-ribbon-thrackle-v1",
        "paths": paths,
        "rotations": rotations,
        "face_orbits": [
            {"size": 4, "representative": ["u", "x02", "x12", "w1", "x31"]},
            {"size": 4, "representative": ["x02", "x03", "v", "x10", "x12"]},
            {"size": 4, "representative": ["x03", "x02", "w2", "x23"]},
            {"size": 2, "representative": ["x01", "x03", "x23", "x21"]},
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, indent=2))
