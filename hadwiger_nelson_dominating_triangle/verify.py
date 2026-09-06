"""Definition-level exact audit; imports no producer or previous research code."""
import argparse
import copy
import hashlib
import json
import math
import time
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


# Sparse squarefree radical arithmetic. Keys are squarefree radicands.
def clean(x):
    return {r:F(v) for r,v in x.items() if v}


def plus(x, y):
    z = dict(x)
    for r,v in y.items():
        z[r] = z.get(r,F(0))+v
    return clean(z)


def neg(x):
    return {r:-v for r,v in x.items()}


def times(x, y):
    z = {}
    for r,a in x.items():
        for s,b in y.items():
            g = math.gcd(r,s)
            t = r*s//(g*g)
            z[t] = z.get(t,F(0))+g*a*b
    return clean(z)


def cadd(z, w):
    return (plus(z[0],w[0]),plus(z[1],w[1]))


def csub(z, w):
    return (plus(z[0],neg(w[0])),plus(z[1],neg(w[1])))


def cmul(z, w):
    return (plus(times(z[0],w[0]),neg(times(z[1],w[1]))),
            plus(times(z[0],w[1]),times(z[1],w[0])))


def squared(z, w):
    a,b = csub(z,w)
    return plus(times(a,a),times(b,b))


def point(a=0,b=0,c=0,d=0):
    return (clean({1:a,3:b}),clean({1:c,3:d}))


def key(z):
    return tuple(tuple(sorted(v.items())) for v in z)


def encode(z):
    q = [z[0].get(1,F(0)),z[0].get(3,F(0)),z[1].get(1,F(0)),z[1].get(3,F(0))]
    require(all((10*v).denominator == 1 for v in q),'integral transcription')
    return [int(10*v) for v in q]


def audit(data):
    require(data['coordinate_scale'] == 10,'scale')
    require(data['coordinate_map'] == '(a,b,c,d)/10 -> ((a+b*sqrt3)/10,(c+d*sqrt3)/10)','coordinate map')
    D = [point(),point(a=1),point(a=F(1,2),d=F(1,2))]
    # Reconstruct the patch as all lattice points in a small box at unit
    # distance from a centre, not by importing the producer's rim list.
    lattice = []
    P = []
    for a,b in product(range(-2,4),repeat=2):
        z = point(a=F(a)+F(b,2),d=F(b,2))
        if any(squared(z,d) == {1:F(1)} for d in D):
            lattice.append([a,b])
            P.append(z)
    require(len(P) == 12 and lattice == data['patch_lattice'],'patch reconstruction')
    # Closed sine/cosine table, unlike the producer's iterated rotation.
    trig = [(2,0),(1,1),(-1,1),(-2,0),(-1,-1),(1,-1)]
    roots = [point(a=F(c,2),d=F(s,2)) for c,s in trig]
    u = point(a=F(3,5),c=F(4,5))
    require(squared(u,point()) == {1:F(1)} and u not in roots,'generic unit seed')
    Q = [cadd(d,cmul(u,r)) for d in D for r in roots]
    V = P+Q
    require(len({key(z) for z in V}) == 30,'distinct embedding')
    require([encode(z) for z in V] == data['vertices'],'exact coordinate transcription')
    centres = [P.index(d) for d in D]
    require(centres == data['centres'],'centre indices')
    require(data['generic_labels'] == [[i,j] for i in range(3) for j in range(6)],'generic labels')
    E = [list(e) for e in combinations(range(30),2) if squared(V[e[0]],V[e[1]]) == {1:F(1)}]
    require(E == data['edges'],'all435 pair norms/edge list')
    patch_edges = [e for e in E if e[1]<12]
    generic_edges = [e for e in E if e[0]>=12]
    spokes = [e for e in E if e[0] in centres and e[1]>=12]
    require(len(patch_edges) == 24 and len(generic_edges) == 36 and len(spokes) == 18,'edge partition')
    require(len(E) == 78,'no additional patch/generic edges')
    predicted = set()
    for i,j in product(range(3),range(6)):
        x = 12+6*i+j
        predicted.add(tuple(sorted((x,12+6*i+(j+1)%6))))
        for k in range(i+1,3):
            predicted.add((x,12+6*k+j))
    require(set(map(tuple,generic_edges)) == predicted,'Cartesian K3 x C6')
    rim = set(range(12))-set(centres)
    rim_edges = [e for e in patch_edges if set(e)<=rim]
    require(len(rim) == len(rim_edges) == 9,'exceptional rim size')
    require(all(sum(v in e for e in rim_edges)==2 for v in rim),'exceptional rim degrees')
    reached = {min(rim)}
    while True:
        more = reached | {v for e in rim_edges if reached.intersection(e) for v in e}
        if more == reached:
            break
        reached = more
    require(reached == rim,'exceptional C9 connectivity')
    membership = [[squared(z,d) == {1:F(1)} for d in D] for z in V]
    require(all(sum(row) == 1 for row in membership[12:]),'generic circle uniqueness')
    cross = 0
    for x,y in ((a,b) for e in E for a,b in (e,e[::-1])):
        if x in centres or y in centres:
            continue
        for i,k in permutations(range(3),2):
            if membership[x][i] and membership[y][k]:
                require(csub(V[x],D[i]) == csub(V[y],D[k]),'rhombus translation')
                cross += 1
    chords = []
    for r in roots:
        value = squared(r,roots[0])
        require(set(value)<={1},'rational orbit chord')
        chords.append(int(value.get(1,F(0))))
    require(chords == data['rotation_chord_squared'] == [0,1,3,4,3,1],'six orbit chords')
    derangements = [list(p) for p in permutations(range(3)) if all(p[i]!=i for i in range(3))]
    require(derangements == data['generic_column_derangements'],'column states')
    # Read and directly verify both colour rows before the exhaustive checks.
    rows = data['pinned_colourings']
    require(len(rows) == 2 and all(len(row)==30 for row in rows),'row dimensions')
    for row in rows:
        require(all(type(c) is int and c in range(3) for c in row),'colour domain')
        require([row[v] for v in centres] == [0,1,2],'centre pinning')
        require(all(row[a]!=row[b] for a,b in E),'positive colour row')
    # Exhaust all3^9 assignments of the exceptional rim, with centres pinned.
    outside = sorted(rim)
    patch_solutions = []
    patch_rows = 0
    for assignment in product(range(3),repeat=9):
        row = [None]*12
        for c,v in enumerate(centres):
            row[v] = c
        for v,c in zip(outside,assignment):
            row[v] = c
        patch_rows += 1
        if all(row[a]!=row[b] for a,b in patch_edges):
            patch_solutions.append(row)
    require(len(patch_solutions) == 1,'unique pinned exceptional colouring')
    # Independently exhaust every 2^18 generic assignment allowed by spokes.
    # This checks the two-state structural derivation without relying on it.
    lists = [[c for c in range(3) if c!=i] for i in range(3) for _ in range(6)]
    local_edges = [(a-12,b-12) for a,b in generic_edges]
    generic_solutions = []
    generic_rows = 0
    for row in product(*lists):
        generic_rows += 1
        if all(row[a]!=row[b] for a,b in local_edges):
            generic_solutions.append(list(row))
    require(len(generic_solutions) == 2,'exactly two pinned generic colourings')
    combined = [patch_solutions[0]+row for row in generic_solutions]
    require(sorted(combined) == sorted(rows),'all pinned colourings match entrywise')
    column_rows = 0
    valid_columns = []
    for word in product(range(2),repeat=6):
        column_rows += 1
        if all(all(derangements[word[j]][i]!=derangements[word[(j+1)%6]][i] for i in range(3)) for j in range(6)):
            valid_columns.append(word)
    require(valid_columns == [(0,1,0,1,0,1),(1,0,1,0,1,0)],'alternating column classification')
    precolourings = set()
    for perm in permutations(range(3)):
        for row in rows:
            c = [perm[v] for v in row]
            require(all(c[a]!=c[b] for a,b in E),'permuted edge test')
            precolourings.add(tuple(c[v] for v in centres))
    require(len(precolourings) == 6,'all centre prescriptions')
    return {'status':'PASS','vertices':30,'pair_norms':435,'unit_edges':78,
            'patch_vertices':12,'patch_edges':24,'exceptional_residual_cycle':9,
            'generic_vertices':18,'generic_edges':36,'generic_spokes':18,
            'circle_membership_checks':90,'directed_noncentre_rhombus_checks':cross,
            'orbit_chord_cases':6,'column_permutations_examined':6,'allowed_column_states':2,
            'column_state_words_examined':column_rows,'valid_column_state_words':2,
            'pinned_patch_assignments_examined':patch_rows,'pinned_patch_colourings':1,
            'pinned_generic_assignments_examined':generic_rows,'pinned_generic_colourings':2,
            'prescribed_centre_permutations':len(precolourings),
            'permuted_positive_edge_checks':12*len(E),'native_solver_calls':0}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work',required=True)
    p.add_argument('--discover',action='store_true')
    args = p.parse_args()
    work = Path(args.work)
    raw = (work/'certificate.json').read_bytes()
    require(raw == (HERE/'certificate.json').read_bytes(),'published certificate bytes')
    data = json.loads(raw)
    start = time.monotonic()
    result = audit(data)
    mutants = []
    bad = copy.deepcopy(data); bad['vertices'][12][0] += 1; mutants.append(bad)
    bad = copy.deepcopy(data); bad['edges'].pop(); mutants.append(bad)
    bad = copy.deepcopy(data); bad['pinned_colourings'][0][12] = 0; mutants.append(bad)
    bad = copy.deepcopy(data); bad['rotation_chord_squared'][1] = 3; mutants.append(bad)
    bad = copy.deepcopy(data); bad['generic_column_derangements'][0][0] = 0; mutants.append(bad)
    rejected = 0
    for bad in mutants:
        try:
            audit(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('malformed certificate accepted')
    result.update(malformed_certificate_rejections=rejected,certificate_bytes=len(raw),
                  certificate_sha256=hashlib.sha256(raw).hexdigest())
    if not args.discover:
        require(result == json.loads((HERE/'expected.json').read_text()),'expected report')
    (work/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    (work/'timing.json').write_text(json.dumps({'seconds':time.monotonic()-start},indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
