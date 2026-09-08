"""Exact geometry and CNF generator for the global EI interface reduction."""
import hashlib
import importlib.util
import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
EI = REPO / 'hadwiger_nelson_ei_interface_minima'
T375 = REPO / 'hadwiger_nelson_small_triangle_forcer375'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def load(name):
    spec = importlib.util.spec_from_file_location('global_ei_' + name, T375 / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


for filename, expected in read(ROOT / 'dependency_hashes.json').items():
    require(hashlib.sha256((REPO / filename).read_bytes()).hexdigest() == expected,
            'changed dependency: ' + filename)
A = load('radicals')


def half_layer():
    g40 = list(map(A.point, read(EI / 'g40.json')))
    g49 = list(map(A.point, read(EI / 'g49.json')))
    cert = read(EI / 'certificate.json')
    pairs = [p for p in combinations(range(40), 2)
             if A.distance(*(g40[v] for v in p)) == A.scalar(4752)]
    triangles = [t for t in combinations(range(49), 3)
                 if all(A.distance(g49[i], g49[j]) == A.scalar(432)
                        for i, j in combinations(t, 2))]
    selected = sorted(set(cert['g40']['essential']) |
                      {v for k, v in enumerate(cert['g40']['optional']) if 1682 >> k & 1})
    require(len(selected) == 53 and len(pairs) == 59 and len(triangles) == 18,
            'wrong source incidence')
    union = set(g40)
    targets = set()
    for k in selected:
        i, j = pairs[k]
        f = A.frame(g49[0], g49[1], g40[i], g40[j], 4752)
        placed = [A.apply(f, p) for p in g49]
        union.update(placed)
        for t in cert['g49']['essential']:
            targets.add(tuple(sorted(placed[v] for v in triangles[t])))
    points = sorted(union)
    lookup = {p: i for i, p in enumerate(points)}
    return points, sorted(tuple(lookup[p] for p in t) for t in targets), [lookup[p] for p in g40[:2]]


def edges(points):
    """Complete edge enumeration, with an exact necessary modular filter."""
    prime = 1021
    roots = [next(x for x in range(prime) if x*x % prime == d) for d in (3, 11, 247)]
    basis = [1] * 8
    for mask in range(8):
        for k in range(3):
            if mask >> k & 1:
                basis[mask] = basis[mask] * roots[k] % prime
    def residue(axis):
        return sum(x.numerator * pow(x.denominator, -1, prime) * basis[k]
                   for k, x in enumerate(axis)) % prime
    residues = [(residue(x), residue(y)) for x, y in points]
    result = []
    for i, (x, y) in enumerate(residues):
        for j in range(i + 1, len(points)):
            u, v = residues[j]
            if ((x-u)**2 + (y-v)**2 - 1296) % prime == 0:
                if A.distance(points[i], points[j]) == A.scalar(1296):
                    result.append((i, j))
    return result


def cnf(n, unit_edges, triangles, pins):
    clauses = []
    for v in range(n):
        clauses.append([4*v+c+1 for c in range(4)])
        clauses.extend([-(4*v+c+1), -(4*v+d+1)] for c, d in combinations(range(4), 2))
    for u, v in unit_edges:
        clauses.extend([-(4*u+c+1), -(4*v+c+1)] for c in range(4))
    clauses.extend([[4*pins[0]+1], [4*pins[1]+2]])
    for triangle in triangles:
        clauses.extend([-(4*v+c+1) for v in triangle] for c in range(4))
    return clauses


def dimacs(n, clauses):
    return f'p cnf {4*n} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)


def forcer_points():
    reference = load('geometry').reference()
    return [A.point(reference[i]) for i in read(T375 / 'certificate.json')['retained_reference_indices']]


def completed_half(points, triangles):
    forcer = forcer_points()
    require(len(forcer) == 375, 'wrong terminal gadget')
    union = set(points)
    frames = []
    for triangle in triangles:
        targets = [points[v] for v in triangle]
        f = A.frame(forcer[0], forcer[1], targets[0], targets[1], 432)
        if A.apply(f, forcer[2]) != targets[2]:
            f = A.frame(forcer[0], forcer[1], targets[0], targets[1], 432, True)
        require(all(A.apply(f, p) == q for p, q in zip(forcer, targets)), 'terminal frame')
        frames.append(f)
        union.update(A.apply(f, p) for p in forcer)
    return sorted(union), frames


def digest(points):
    h = hashlib.sha256()
    for p in sorted(points):
        encoded = [[[v.numerator, v.denominator] for v in axis] for axis in p]
        h.update(json.dumps(encoded, separators=(',', ':')).encode() + b'\n')
    return h.hexdigest()
