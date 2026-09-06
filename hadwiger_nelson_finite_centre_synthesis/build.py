"""Replay the compact construction using exact pair-circle intersections."""
import hashlib
import json
from itertools import combinations
from pathlib import Path

from geometry import c, centres, dist, seed

ROOT = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def main():
    points = seed()
    known = set(points)
    triples = json.loads((ROOT / 'construction.json').read_text())
    for triple in triples:
        if (len(triple) != 3 or len(set(triple)) != 3 or
                any(type(i) is not int or not 0 <= i < len(points) for i in triple)):
            raise ValueError('Invalid parent triple')
        a, b, k = triple
        choices = [p for p in centres(points[a], points[b])
                   if dist(p, points[k]) == c(1296)]
        if len(choices) != 1 or choices[0] in known:
            raise ValueError('Triple must determine one new point')
        points.append(choices[0])
        known.add(choices[0])
    rows = []
    for p in points:
        row = [v for coordinate in p for v in coordinate]
        if any(v.denominator != 1 for v in row):
            raise ValueError('This fixture should have integral scaled coefficients')
        rows.append([int(v) for v in row])
    edges = [[i, j] for i, j in combinations(range(len(points)), 2)
             if dist(points[i], points[j]) == c(1296)]
    cert = json.loads((ROOT / 'certificate.json').read_text())
    result = {'vertices': len(points), 'edges': len(edges),
              'point_sha256': digest(rows), 'edge_sha256': digest(edges)}
    if any(cert[k] != v for k, v in result.items()):
        raise ValueError('Replay disagrees with certificate')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
