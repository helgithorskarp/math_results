"""six-reviewer-3: fresh exact finite evidence for the ordinary G20 proof.

No author module, certificate, coordinate fixture, solver, or float is imported.
This corroborates the stated finite reductions; PROOF.md supplies geometry.
"""
from fractions import Fraction as F
from itertools import combinations, product
from collections import Counter
import hashlib
import json
from pathlib import Path

A = ((0, 5, 11), (0, 6, 11), (0, 5, 7), (5, 9, 11))
B = ((1, 2, 4), (2, 4, 8), (1, 2, 10), (1, 10, 12))
P = (5, 7, 12, 10, 9)
R = (7, 0, 6, 11, 9, 10, 2, 8, 4, 1, 12)
CORE = tuple(sorted(set(sum(A + B, ()))))
LO, HI = F(7, 15), F(8, 13)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a, b):
    require(a != b, 'loop')
    return tuple(sorted((a, b)))


def darts(cycle):
    require(len(cycle) >= 3 and len(set(cycle)) == len(cycle), 'simple cycle')
    return list(zip(cycle, cycle[1:] + cycle[:1]))


def edges(cycle):
    return {edge(*p) for p in darts(tuple(cycle))}


def canon(cycle):
    t = tuple(cycle)
    return min(t[i:] + t[:i] for i in range(len(t)))


def unoriented(cycle):
    return min(canon(cycle), canon(tuple(reversed(cycle))))


G20 = set().union(*(edges(t) for t in A + B)) | {edge(7, 12), edge(9, 10)}


def residual_cycle(graph, chosen_faces):
    """Subtract oriented facial darts; reconstruct the complete remaining cycle."""
    full = {(a, b) for a, b in graph} | {(b, a) for a, b in graph}
    used = [d for face in chosen_faces for d in darts(tuple(face))]
    require(len(used) == len(set(used)), 'same side used twice')
    require(set(used) <= full, 'face uses absent contact')
    left = full - set(used)
    nxt = {}
    for a, b in left:
        require(a not in nxt, 'residual pinched/outdegree')
        nxt[a] = b
    require(set(nxt) == set(nxt.values()), 'residual indegree')
    start = min(nxt)
    result = [start]
    while nxt[result[-1]] != start:
        require(nxt[result[-1]] not in result, 'residual multiple cycle')
        result.append(nxt[result[-1]])
    require(len(result) == len(left), 'residual missing cycle')
    return tuple(result)


def sphere_map(graph, faces):
    """Check every dart and every complete vertex link, then Euler."""
    ds = [d for face in faces for d in darts(tuple(face))]
    all_darts = {(a, b) for a, b in graph} | {(b, a) for a, b in graph}
    require(Counter(ds) == Counter(all_darts), 'whole dart coverage')
    vertices = sorted({v for e in graph for v in e})
    links = {v: {} for v in vertices}
    for face in faces:
        for i, v in enumerate(face):
            before, after = face[i-1], face[(i+1) % len(face)]
            require(before not in links[v], 'duplicate vertex corner')
            links[v][before] = after
    for v, link in links.items():
        require(set(link) == set(link.values()), 'incomplete link')
        seen = set()
        u = min(link)
        while u not in seen:
            seen.add(u)
            u = link[u]
        require(u == min(link) and seen == set(link), 'multiple vertex link')
    require(len(vertices)-len(graph)+len(faces) == 2, 'sphere Euler')
    return {'vertices': vertices, 'edges': [list(e) for e in sorted(graph)],
            'faces': [list(f) for f in sorted(canon(t) for t in faces)],
            'degrees': [[v, len(links[v])] for v in vertices]}


def coherent_faces(graph, triangles, fixed):
    choices = []
    for bits in product((0, 1), repeat=len(triangles)):
        ts = [t if b == 0 else tuple(reversed(t)) for t, b in zip(triangles, bits)]
        try:
            rem = residual_cycle(graph, ts + list(fixed))
            sphere_map(graph, ts + list(fixed) + [rem])
        except ValueError:
            continue
        choices.append((ts, rem))
    require(len(choices) == 1, 'unique oriented map with fixed small face')
    return choices[0]


def partition_polygon(cycle, chords):
    """A boundary chord cuts a topological disk into two disks; recurse literally."""
    if not chords:
        return [tuple(cycle)]
    a, b = min(chords)
    i, j = sorted((cycle.index(a), cycle.index(b)))
    q1 = tuple(cycle[i:j+1])
    q2 = tuple(cycle[j:] + cycle[:i+1])
    rest = chords - {edge(a, b)}
    c1 = {e for e in rest if set(e) <= set(q1)}
    c2 = {e for e in rest if set(e) <= set(q2)}
    require(c1.isdisjoint(c2) and c1 | c2 == rest, 'noncrossing split coverage')
    return partition_polygon(q1, c1) + partition_polygon(q2, c2)


def alternating(e, f):
    if set(e) & set(f):
        return False
    a, b = sorted(P.index(v) for v in e)
    x, y = (P.index(v) for v in f)
    return (a < x < b) != (a < y < b)


def ring_paths(ring, start, stop):
    paths = []
    for step in (1,-1):
        i = ring.index(start)
        path = [start]
        while path[-1] != stop:
            i = (i+step) % len(ring)
            path.append(ring[i])
        paths.append(path)
    return sorted(paths,key=len)


def annulus_pairings(oriented_triangles):
    ga = set().union(*(edges(t) for t in A))
    gb = set().union(*(edges(t) for t in B))
    ra = residual_cycle(ga,oriented_triangles[:4])
    rb = residual_cycle(gb,oriented_triangles[4:8])
    require(unoriented(ra) == unoriented((0,6,11,9,5,7)), 'A boundary')
    require(unoriented(rb) == unoriented((1,4,8,2,10,12)), 'B boundary')
    pa, pb = ring_paths(ra,7,9),ring_paths(rb,10,12)
    cycles = {(i,j):pa[i]+pb[j] for i in range(2) for j in range(2)}
    require(all(edges(tuple(x)) <= G20 and len(set(x)) == len(x)
                for x in cycles.values()), 'annulus complete cycles')
    result = [[cycles[(0,0)],cycles[(1,1)]], [cycles[(0,1)],cycles[(1,0)]]]
    require(sorted(map(len,result[0])) == [5,11] and
            sorted(map(len,result[1])) == [7,9], 'both annulus pairings')
    require(unoriented(result[0][0]) == unoriented(P) and
            unoriented(result[0][1]) == unoriented(R), 'selected annulus disks')
    return result


def pentagon_cases():
    diagonals = sorted({edge(a, b) for a, b in combinations(P, 2)} - edges(P))
    out = []
    for mask in range(1 << len(diagonals)):
        chosen = {e for i, e in enumerate(diagonals) if mask >> i & 1}
        row = {'chords': [list(e) for e in sorted(chosen)]}
        if edge(7, 9) in chosen:
            row['reason'] = 'strict7-9'
        elif any(alternating(e, f) for e, f in combinations(chosen, 2)):
            row['reason'] = 'crossing'
        else:
            fs = partition_polygon(P, chosen)
            row['faces'] = [list(unoriented(f)) for f in sorted(fs)]
            deg5 = len({b if a == 5 else a for a, b in G20 | chosen if 5 in (a,b)})
            if deg5 > 5:
                row['reason'] = 'degree6at5'
            elif sum(len(f) == 3 and 5 in f for f in fs) == 2:
                row['reason'] = 'five-triangle-star-at5'
            elif edge(7, 10) in chosen or edge(9, 12) in chosen:
                row['reason'] = 'gamma-rhombus'
            elif edge(5, 10) in chosen:
                row['reason'] = 'a-b-rhombus-at10'
            else:
                row['reason'] = 'necessary-survivor'
        out.append(row)
    require(len(out) == 32, 'all five diagonals')
    survivors = [r['chords'] for r in out if r['reason'] == 'necessary-survivor']
    require(survivors == [[], [[5, 12]]], 'two complete necessary subdivisions')
    return out


def integer_partitions(n):
    """Coin-multiplicity representation, no sorted-part recursion or cut mask."""
    states = [((), 0)]
    for value in range(1, n+1):
        states = [(p+(value,)*k, s+value*k)
                  for p,s in states for k in range((n-s)//value+1)]
    return sorted(p for p,s in states if s == n)


def route_profiles():
    all_parts = integer_partitions(11)
    cohort = [p for p in all_parts if len(p) <= 8]
    selected = [p for p in cohort if sum(x >= 4 for x in p) >= 2]
    rows = []
    for p in selected:
        assignments = sorted({(p[i],p[j]) for i in range(len(p)) for j in range(len(p))
                              if i != j and min(p[i],p[j]) >= 4})
        for a,b in assignments:
            left = list(p)
            left.remove(a)
            left.remove(b)
            rows.append({'profile': list(p), 'A': a, 'B': b, 'others': left,
                         'eNN': 8-len(p), 'V_possible': a >= 5,
                         'V_and_degree10five_possible': a == 5 and b == 6})
    require(len(all_parts) == 56 and len(cohort) == 52 and len(selected) == 9, 'partition scope')
    require(len(rows) == 14 and sum(x['V_possible'] for x in rows) == 7, 'oriented assignments')
    require(sum(x['V_and_degree10five_possible'] for x in rows) == 1, 'forced5+6 assignment')
    return {'all_partitions': [list(p) for p in all_parts],
            'cohort_partitions': [list(p) for p in cohort], 'assignments': rows}


def budgets(lo=LO, hi=HI):
    require(F(0) < lo <= hi < 1, 'positive closed interval')
    tlo, thi = lo/(1+lo), hi/(1+hi)
    upper_root = 2 - 4*thi**2  # thi < cos(3pi/8), via sqrt2 < upper_root
    five_root = 1+4*tlo        # cos(2pi/5) < tlo, via sqrt5 < five_root
    margins = {
        'lo-square-minus-one-fifth': lo**2-F(1,5),
        'upper-root-minus-zero': upper_root,
        'upper-root-square-minus-two': upper_root**2-2,
        'five-root-minus-zero': five_root,
        'five-root-square-minus-five': five_root**2-5,
        'sqrt-five-lower-control': 5-F(11,5)**2,
        '9lo-square-2lo-1': 9*lo**2-2*lo-1,
        'derivative9c-square-2c-1': 18*lo-2,
        'hi-less-one': 1-hi,
        'extension-left': F(1,2)-lo,
        'extension-right': hi-F(3,5),
    }
    require(all(v > 0 for v in margins.values()), 'whole strict angle/rhombus budget')
    return {k: str(v) for k,v in sorted(margins.items())}


def whole_record():
    require(len(CORE) == 12 and len(G20) == 20, 'literal12/20')
    ts, rem = coherent_faces(G20, A+B, (P,))
    require(unoriented(rem) == unoriented(R), 'full11-boundary')
    bare = sphere_map(G20, ts+[P,rem])
    V = G20 | {edge(5,12)}
    quad = (5,12,10,9)
    tv, rv = coherent_faces(V, A+B+((5,7,12),), (quad,))
    split = sphere_map(V, tv+[quad,rv])
    require(unoriented(rv) == unoriented(R), 'same residual region')
    fresh = 3
    G24 = V | {edge(2,fresh),edge(9,fresh),edge(10,fresh)}
    tt, rr = coherent_faces(G24, A+B+((5,7,12),(2,10,fresh),(9,10,fresh)), (quad,))
    forced = sphere_map(G24, tt+[quad,rr])
    expectedR24 = tuple(fresh if v == 10 else v for v in R)
    require(unoriented(rr) == unoriented(expectedR24), 'G24 residual11-boundary')
    triangles = [frozenset(t) for t in tt]
    adjacency = [(i,j) for i,j in combinations(range(11),2) if len(triangles[i]&triangles[j]) == 2]
    components = []
    unseen = set(range(11))
    while unseen:
        stack = [min(unseen)]; comp = set()
        while stack:
            i = stack.pop()
            if i in comp: continue
            comp.add(i)
            stack.extend(j if i == k else k for k,j in adjacency if i in (k,j))
        unseen -= comp
        components.append(sorted(comp))
    require(sorted(map(len,components)) == [5,6] and len(adjacency) == 9, 'full triangle dual')
    slots = []
    for x in CORE:
        if x == 10: why = 'self'
        elif x in (1,2,9,12): why = 'existing10neighbor'
        elif x in (0,11):
            new = V | {edge(x,k) for k in (2,9,10)}
            deg = len({b if a == x else a for a,b in new if x in (a,b)})
            require(deg > 5, 'fresh-corner degree obstruction')
            why = 'degree'+str(deg)
        else:
            why = {5:'forbiddenU',7:'forbiddenW',4:'2alpha-at1',
                   6:'gamma-at11',8:'gamma-at2'}[x]
        slots.append([x,why])
    qcounts = []
    for label, n, e, triangles_out, q_out, p_out in [('P',12,20,8,0,1),
                                                 ('V',12,21,9,1,0),
                                                 ('G24',13,24,11,1,0)]:
        ti,qi,pi = 11-triangles_out,3-q_out,3-p_out
        inner_edges, inner_vertices = 30-e,15-n
        face_count = ti+qi+pi
        require(3*ti+4*qi+5*pi == 11+2*inner_edges, 'complete residual side incidence')
        require(inner_vertices-inner_edges+face_count == 1, 'residual disk Euler')
        qcounts.append({'branch':label, 'interior_points':inner_vertices,
                        'inner_contacts':inner_edges,'faces':face_count,'TQP':[ti,qi,pi]})
    return {'agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'ordinary_geometry_unformalized':True,'target_native_used':False,
            'local_band':[str(LO),str(HI)],'physical_corollary_band':[str(LO),'19/31'],
            'profile_screen_band':['7/13','3/5'],
            'strict_margins':budgets(),'G20':bare,'V':split,'G24':forced,
            'pentagon_cases':pentagon_cases(), 'profiles':route_profiles(),
            'fresh_core_candidates':slots,'G24_triangle_dual_edges':[list(e) for e in adjacency],
            'G24_triangle_components':components,'residual_budgets':qcounts,
            'annulus_pairings':annulus_pairings(ts)}


def canonical(record):
    return json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()


def verify(record):
    require(canonical(record) == canonical(whole_record()), 'complete typed record mismatch')


if __name__ == '__main__':
    result = whole_record()
    text = json.dumps(result,sort_keys=True,indent=2)+'\n'
    print(json.dumps({'status':'PASS','record_bytes':len(text.encode()),
                      'whole_record_sha256':hashlib.sha256(text.encode()).hexdigest(),
                      'pentagon_cases':32,'oriented_profile_assignments':14,
                      'strict_margins':len(result['strict_margins'])},sort_keys=True))
