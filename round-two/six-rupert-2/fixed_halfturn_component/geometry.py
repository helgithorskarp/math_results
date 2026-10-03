"""Original J74 and exact receiving hexagon; small helpers credited to9918.

Only two compact public dependencies are imported. No old regional theorem,
local collar, source enumeration or floating discovery is a replay input.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib, importlib.util, json, sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PINS = {
    'model.py': 'cc0ce4358eea0139da13962b6abdf25a9710fb934e8e41ee3e6f3cbe3acb8cd7',
    'q5.py': 'cef1fe01c185fc5c63d729d8e27588b4efe56d8487c87a73f22a68297b18ed3c',
}
for name, pin in PINS.items():
    if hashlib.sha256((BASE/name).read_bytes()).hexdigest() != pin:
        raise ValueError('original dependency pin BEFORE import: '+name)
sys.path.insert(0, str(BASE))
import q5 as a
Q = a.Q
spec = importlib.util.spec_from_file_location('original_J74_fixed_G', BASE/'model.py')
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
V = model.VERTICES
S = Q(0, 1)
Z = (Q(),)*3
I = tuple(tuple(Q(int(i == j)) for j in range(3)) for i in range(3))
H = ((Q(-1), Q(), Q()), (Q(), Q(-1), Q()), (Q(), Q(), Q(1)))
MX = ((Q(-1), Q(), Q()), (Q(), Q(1), Q()), (Q(), Q(), Q(1)))
aa, bb, cc = (S-1)/4, (S+1)/4, Q(F(1, 2))
AXIS = (-bb, aa, cc)
G = ((aa, -cc, -bb), (-cc, -bb, aa), (-bb, aa, -cc))
t, ell = (3-S)/2, (5*S-9)/22
P = [(Q(1), Q()), ((S-1)/2, t), (ell, t), (ell, -t),
     ((5-S)/10, -t), ((3+S)/6, (S-3)/6)]
SIDES = [(Q(1), Q(-1), Q(-1)), (Q(1), Q(), -(3+S)/2),
         (Q(-1), (9+5*S)/2, Q()), (Q(1), Q(), (3+S)/2),
         (Q(1), (5-3*S)/2, Q(2)), (Q(1), Q(-1), Q(1))]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def enc(x):
    return [str(x.a), str(x.b)]

def vec(v):
    return [enc(x) for x in v]

def dec(v):
    return tuple(Q(F(x), F(y)) for x, y in v)

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()

def digest(x):
    return hashlib.sha256(canonical(x)).hexdigest()

def act(A, v):
    return tuple(a.dot(row, v) for row in A)

def mm(A, B):
    return tuple(tuple(a.dot(row, col) for col in zip(*B)) for row in A)

def proper(A):
    require(mm(A, tuple(zip(*A))) == I and
            a.dot(A[0], a.cross(A[1], A[2])) == 1, 'actual proper rotation')

def raw(p):
    return (p[0], Q(1), -p[1])

def value(w, p):
    return w[0]+w[1]*p[0]+w[2]*p[1]

def normalize(w):
    t0 = next((x for x in w if x != 0), None)
    if t0 is None:
        return None
    return tuple(x/(t0 if t0 > 0 else -t0) for x in w)

def clip(poly, w):
    out = []
    for v, u in zip(poly, poly[1:]+poly[:1]):
        fv, fu = value(w, v), value(w, u)
        if fv >= 0:
            out.append(v)
        if fv < 0 < fu or fu < 0 < fv:
            t0 = fv/(fv-fu)
            out.append(tuple(x+t0*(y-x) for x, y in zip(v, u)))
    result = []
    for v in out:
        if not result or v != result[-1]:
            result.append(v)
    if len(result) > 1 and result[0] == result[-1]:
        result.pop()
    return result

def area(poly):
    return sum((v[0]*u[1]-v[1]*u[0]
                for v, u in zip(poly, poly[1:]+poly[:1])), Q())

def projection(v, p):
    r = raw(p)
    return a.sub(v, a.scale(a.dot(r, v)/a.dot(r, r), r))

def facets():
    fs = []
    for face in model.FACES:
        N = a.cross(a.sub(V[face[1]], V[face[0]]), a.sub(V[face[2]], V[face[0]]))
        h = a.dot(N, V[face[0]])
        if h < 0:
            N, h = tuple(-v for v in N), -h
        require(h > 0 and all(a.dot(N, v) <= h for v in V), 'actual supporting plane')
        require({k for k, v in enumerate(V) if a.dot(N, v) == h} == set(face),
                'entire original coplanar facet')
        fs.append((N, h, face))
    return fs

def record():
    original, caps, gyrated, built, axes = model.cupola_construction()
    require(len(V) == len(set(V)) == 60 and built == set(V), 'original two-cupola J74')
    require(len(caps) == 2 and len(caps[0]) == len(caps[1]) == 5 and
            a.cross(axes[0], axes[1]) != Z, 'two nonopposite gyrated cupolas')
    R2 = (11+4*S)/4
    require(all(a.dot(v, v) == R2 for v in V), 'original common sphere')
    require(all(a.add(V[i], V[j]) == Z for i, j in ((0, 7), (1, 6), (2, 5))) and
            a.dot(V[0], a.cross(V[1], V[2])) != 0, 'origin interior without centrality')
    require({act(H, v) for v in V} == set(V) and {act(MX, v) for v in V} == set(V),
            'actual proper H and improper Mx body actions')
    require(a.dot(AXIS, AXIS) == 1 and G == tuple(tuple(2*AXIS[i]*AXIS[j]-int(i == j)
            for j in range(3)) for i in range(3)), 'literal unit-axis half-turn')
    proper(G)
    require(mm(G, G) == I and sum((G[i][i] for i in range(3)), Q()) == -1,
            'absolute original half-turn')
    require(0 < ell < 1 and 0 < t < 1, 'side bounds put the whole intersection in unit box')
    gaps = [value(w, p) for w in SIDES for p in P]
    require(min(gaps) >= 0 and area(P) == Q(F(63, 11), F(-349, 165)) > 0,
            'whole nondegenerate literal closed hexagon')
    for i, w in enumerate(SIDES):
        require(value(w, P[i]) == value(w, P[(i+1) % 6]) == 0 and
                all(value(w, P[j]) > 0 for j in range(6) if j not in (i, (i+1) % 6)),
                'strict convex cyclic sides and retained endpoints')
    poly = [(Q(-1), Q(-1)), (Q(1), Q(-1)), (Q(1), Q(1)), (Q(-1), Q(1))]
    for w in SIDES:
        poly = clip(poly, w)
    first = poly.index(P[0])
    require(poly[first:]+poly[:first] == P, 'entire intersection, not area-only cover')
    return {'original_vertices': 60, 'original_facets': len(facets()),
            'sphere_R2': enc(R2), 'halfturn_axis': vec(AXIS),
            'whole_component': list(map(vec, P)), 'six_side_controls': len(gaps),
            'component_double_area': enc(area(P))}
