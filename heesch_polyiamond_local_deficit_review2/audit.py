"""six-reviewer-2: independent exact audit of the unmarked T214 claim.

No author modules, SAT libraries or floating arithmetic are imported.
Geometry uses centroid cells, rectangular translation inventories and
complement flood fills. Charge selectors use complete compatible-set search.
Glucose traces are checked as RUP by a separate literal-occurrence checker.
"""
import argparse
from collections import Counter, defaultdict, deque
from itertools import product, combinations
import hashlib
import json
from pathlib import Path
import time

TARGET_SHA = '35125be2f7a7d99faacbb1e9812817e83496f5ca'
SHAPE_SHA = '8d42c74f1e219ae37f34d5706f83ab4eb20e921ada66d70090c8a539f481335f'
DIR = 'heesch_polyiamond_local_deficit'
PRIOR = 'heesch_polyiamond_hexapillar'
RAYS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
IDENT = (1, 0, 0, 1, 0, 0)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canon(points):
    return tuple(sorted(points))


def up(x, y):
    return canon(((x, y), (x+1, y), (x, y+1)))


def down(x, y):
    return canon(((x+1, y+1), (x+1, y), (x, y+1)))


def norm(v):
    x, y = v
    return x*x+x*y+y*y


def metric_matrices():
    # Exhaust the integer unit vectors, rather than iterating rotations.
    out = []
    for a, b, c, d in product(range(-1, 2), repeat=4):
        if norm((a, c)) == norm((b, d)) == 1 and \
                2*a*b+a*d+b*c+2*c*d == 1 and abs(a*d-b*c) == 1:
            out.append((a, b, c, d))
    need(len(out) == 12, 'metric group')
    return out


def point(v, p):
    a, b, c, d, x, y = p
    return a*v[0]+b*v[1]+x, c*v[0]+d*v[1]+y


def move(shape, p):
    return {canon(point(v, p) for v in t) for t in shape}


def compose(p, q):
    a, b, c, d, _, _ = p
    e, f, g, h, x, y = q
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h, *point((x, y), p))


def inverse(p):
    a, b, c, d, x, y = p
    det = a*d-b*c
    need(abs(det) == 1, 'nonunimodular pose')
    q = (d//det, -b//det, -c//det, a//det, 0, 0)
    return (*q[:4], *point((-x, -y), q))


def star(v):
    x, y = v
    return tuple(canon((v, (x+RAYS[j][0], y+RAYS[j][1]),
                       (x+RAYS[(j+1) % 6][0], y+RAYS[(j+1) % 6][1])))
                 for j in range(6))


def incidence(shape):
    out = Counter(v for t in shape for v in t)
    return out


def make_shape():
    # A grid-aligned hexagon contains a triangle iff its centroid is interior.
    hexagon = set()
    for x, y in product(range(-4, 4), repeat=2):
        for parity, t in ((1, up(x, y)), (2, down(x, y))):
            sx, sy = 3*x+parity, 3*y+parity
            if max(abs(sx), abs(sy), abs(sx+sy)) < 9:
                hexagon.add(t)
    need(len(hexagon) == 54, 'side-three centroid hexagon')
    shape = {canon((x+3*k, y+3*k) for x, y in t)
             for k in range(4) for t in hexagon}
    need(len(shape) == 216, 'four-hex strip')
    owners = {(k, 0) for k in range(4)}
    ports = sorted((c, (c[0]+dx, c[1]+dy)) for c in owners
                   for dx, dy in RAYS if (c[0]+dx, c[1]+dy) not in owners)
    signs = [1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0]
    feature = {up(0, 2), up(2, 0)}
    outside = {canon((3-y, 3-x) for x, y in t) for t in feature}
    for (c, n), sign in zip(ports, signs):
        if sign == 0:
            continue
        ray = (n[0]-c[0], n[1]-c[1])
        matrices = [m for m in metric_matrices()
                    if (m[0], m[2]) == ray and m[0]*m[3]-m[1]*m[2] == 1]
        need(len(matrices) == 1, 'directed macro rotation')
        p = (*matrices[0], 3*c[0], 3*c[0])
        f = move(feature if sign == 1 else outside, p)
        if sign == 1:
            need(f <= shape, 'nick location')
            shape -= f
        else:
            need(not f & shape, 'bump location')
            shape |= f
    raw = json.dumps({'triangles': sorted(shape)}, separators=(',', ':'))+'\n'
    need(len(shape) == 214 and hashlib.sha256(raw.encode()).hexdigest() == SHAPE_SHA,
         'explicit T214 geometry')
    return shape


def neighbors(t):
    return tuple(canon((u, v, (u[0]+v[0]-w[0], u[1]+v[1]-w[1])))
                 for w, u, v in ((t[0], t[1], t[2]),
                                 (t[1], t[0], t[2]), (t[2], t[0], t[1])))


def flood(region):
    unseen = set(region)
    need(bool(unseen), 'empty region')
    todo = [unseen.pop()]
    while todo:
        t = todo.pop()
        for u in neighbors(t):
            if u in unseen:
                unseen.remove(u)
                todo.append(u)
    return unseen


def disc(shape):
    need(not flood(shape), 'edge-disconnected shape')
    counts = incidence(shape)
    for v, count in counts.items():
        bits = [t in shape for t in star(v)]
        transitions = sum(bits[j] != bits[(j+1) % 6] for j in range(6))
        need(count == sum(bits) and transitions in (0, 2), 'pinched vertex star')
    xs = [x for x, _ in counts]; ys = [y for _, y in counts]
    rectangle = {t for x in range(min(xs)-2, max(xs)+2)
                 for y in range(min(ys)-2, max(ys)+2)
                 for t in (up(x, y), down(x, y))}
    need(shape <= rectangle, 'complement bounds')
    need(not flood(rectangle-shape), 'bounded complementary hole')
    edges = {tuple(sorted((u, v))) for t in shape for u, v in combinations(t, 2)}
    need(len(counts)-len(edges)+len(shape) == 1, 'Euler characteristic')
    return {'cells': len(shape), 'vertices': len(counts), 'edges': len(edges),
            'boundary_angles': dict(sorted(Counter(60*c for c in counts.values() if c < 6).items()))}


def lower(root, shape):
    data = json.loads((root/PRIOR/'coronas.json').read_text())
    need(data['depth'] == 5 and len(data['placements']) == 131, 'fixture scope')
    layers = [set() for _ in range(6)]
    counts = [0]*6
    occupied = set()
    copies = []
    for p in data['placements']:
        level = p['level']
        pose = (*p['matrix'], *p['translation'])
        need(type(level) is int and 0 <= level <= 5 and
             all(type(x) is int for x in pose) and pose[:4] in metric_matrices(), 'pose')
        f = move(shape, pose)
        need(not f & occupied, 'full-copy overlap')
        if level == 0:
            need(pose == IDENT, 'root pose')
        occupied |= f; layers[level] |= f; counts[level] += 1
        copies.append((level, f))
    need(counts == [1, 5, 11, 23, 39, 52], 'layer census')
    rows = []
    prefix = set()
    for level, layer in enumerate(layers):
        oldvertices = set(incidence(prefix))
        prefix |= layer
        stats = disc(prefix)
        need(all(set(star(v)) <= prefix for v in oldvertices), 'strict surrounding')
        rows.append({'level': level, 'copies': sum(counts[:level+1]), **stats})
    for level, f in copies:
        if level:
            need(set(incidence(f)) & set(incidence(layers[level-1])), 'preceding-layer contact')
    need(rows[0]['boundary_angles'] == {60: 11, 120: 25, 180: 3, 240: 25, 300: 8}, 'angles')
    return rows


def catalogue(shape):
    counts = incidence(shape)
    corners = sorted(v for v, count in counts.items() if count in (4, 5))
    pockets = sorted(v for v, count in counts.items() if count == 5)
    tips = sorted(v for v, count in counts.items() if count == 1)
    gapmasks = {v: sum(1 << j for j, t in enumerate(star(v)) if t not in shape) for v in corners}
    accepted = {}
    rectangles = 0
    for m in metric_matrices():
        rotated = move(shape, (*m, 0, 0))
        rc = incidence(rotated)
        convex = {v: sum(1 << j for j, t in enumerate(star(v)) if t in rotated)
                  for v, count in rc.items() if count in (1, 2)}
        lo = [min(v[j] for v in corners)-max(w[j] for w in convex) for j in (0, 1)]
        hi = [max(v[j] for v in corners)-min(w[j] for w in convex) for j in (0, 1)]
        for x in range(lo[0], hi[0]+1):
            for y in range(lo[1], hi[1]+1):
                rectangles += 1
                eligible = False
                for v in corners:
                    mask = convex.get((v[0]-x, v[1]-y), 0)
                    if mask and mask & gapmasks[v] == mask:
                        eligible = True
                        break
                if not eligible:
                    continue
                f = {canon((a+x, b+y) for a, b in t) for t in rotated}
                if not f & shape:
                    accepted[(*m, x, y)] = f
    wide = sorted(accepted)
    raw = [p for p in wide if any(len(set(star(v)) & accepted[p]) == 1
                                 for v in pockets)]
    need((len(pockets), len(tips), len(corners), len(raw), len(wide)) == (8, 11, 33, 59, 475),
         'complete corner inventories')
    return raw, wide, tips, corners, rectangles


def bitsets(feet):
    universe = {t: j for j, t in enumerate(sorted(set().union(*feet)))} if feet else {}
    return [sum(1 << universe[t] for t in f) for f in feet]


def geometric(shape, corners, wide, fixed):
    fixedfeet = [move(shape, p) for p in fixed]
    occupied = set()
    for f in fixedfeet:
        need(not occupied & f, 'overlapping fixed copies')
        occupied |= f
    pool = {compose(p, q) for p in fixed for q in wide}-set(fixed)
    poses = []; feet = []
    for p in sorted(pool):
        f = move(shape, p)
        if not f & occupied:
            poses.append(p); feet.append(f)
    required = set().union(*(set(star(point(v, p))) for p in fixed for v in corners))-occupied
    clauses = [[i+1 for i, f in enumerate(feet) if t in f] for t in sorted(required)]
    masks = bitsets(feet)
    for j, mask in enumerate(masks):
        clauses.extend([-(j+1), -(k+1)] for k in range(j) if mask & masks[k])
    return poses, clauses


def cnf(nv, clauses):
    return f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)


def compare_formula(nv, clauses, expected, folder):
    text = cnf(nv, clauses)
    actual = {'variables': nv, 'clauses': len(clauses),
              'cnf_sha256': hashlib.sha256(text.encode()).hexdigest()}
    need(all(actual[k] == expected[k] for k in actual), 'independent geometric formula mismatch')
    need((folder/'instance.cnf').read_text() == text, 'native formula bytes changed')
    trace = (folder/'proof.drat').read_text()
    audit = rup(clauses, trace)
    return {**actual, 'rup': audit, 'trace_sha256': hashlib.sha256(trace.encode()).hexdigest()}


def rup(clauses, trace):
    """Check the monotone RUP skeleton; ignore native deletion hints.

    For each addition C, start afresh with ALL input and previously RUP-checked
    clauses and assumptions not-C. Retaining clauses is sound: by induction
    every retained clause follows from the original CNF. The trace's deletion
    multiset is syntax-checked separately and does not erase logical premises.
    Literal occurrences drive exact unit propagation. No RAT rule is used.
    """
    database = []
    active = []
    occurrences = defaultdict(list)
    indices = defaultdict(list)
    units = set()
    empties = set()

    def add(c):
        c = tuple(sorted(set(c)))
        i = len(database)
        database.append(c); active.append(True); indices[c].append(i)
        for lit in c:
            occurrences[lit].append(i)
        if len(c) == 1:
            units.add(i)
        if not c:
            empties.add(i)

    for c in clauses:
        add(c)

    def conflict(assumptions):
        if empties:
            return True
        assigned = set()
        queue = deque(assumptions)
        queue.extend(database[i][0] for i in units)
        while queue:
            lit = queue.popleft()
            if -lit in assigned:
                return True
            if lit in assigned:
                continue
            assigned.add(lit)
            for i in occurrences.get(-lit, ()):
                c = database[i]
                if any(x in assigned for x in c):
                    continue
                rest = [x for x in c if -x not in assigned]
                if not rest:
                    return True
                if len(rest) == 1:
                    queue.append(rest[0])
        return False

    additions = deletions = 0
    for line in trace.splitlines():
        if not line.strip() or line.startswith('c'):
            continue
        tokens = line.split()
        deleted = tokens[0] == 'd'
        if deleted:
            tokens = tokens[1:]
        values = list(map(int, tokens))
        need(values and values[-1] == 0 and 0 not in values[:-1], 'trace syntax')
        c = tuple(sorted(set(values[:-1])))
        if deleted:
            options = indices.get(c, [])
            while options and not active[options[-1]]:
                options.pop()
            need(bool(options), 'deletion of absent clause')
            active[options.pop()] = False
            deletions += 1
        else:
            need(conflict([-x for x in c]), 'non-RUP trace addition')
            add(c); additions += 1
    # Glucose may omit the explicit empty clause when input propagation already
    # conflicts. Check the terminal contradiction ourselves in every case.
    need(conflict([]), 'trace lacks a checked terminal contradiction')
    return {'additions': additions, 'deletions': deletions,
            'explicit_empty_clause': bool(empties),
            'deletion_hints_ignored_for_logic': True,
            'checked_terminal_conflict': True}


def selector_data(shape, tips, raw, allowed, fixed):
    banned = set(raw)-{raw[i-1] for i in allowed}
    incoming = [inverse(raw[i-1]) for i in allowed]
    fixedfeet = [move(shape, p) for p in fixed]
    occupied = set().union(*fixedfeet)
    pool = {compose(p, q) for p in fixed for q in incoming}-set(fixed)

    def bad(p, q):
        return compose(inverse(p), q) in banned or compose(inverse(q), p) in banned

    need(all(not bad(p, q) for p, q in combinations(fixed, 2)), 'forbidden fixed pair')
    poses = []; feet = []
    for p in sorted(pool):
        f = move(shape, p)
        if not f & occupied:
            poses.append(p); feet.append(f)
    invalid = {j for j, p in enumerate(poses) if any(bad(p, q) for q in fixed)}
    incompatible = [0]*len(poses)
    for j in range(len(poses)):
        for k in range(j):
            if feet[j] & feet[k] or bad(poses[j], poses[k]):
                incompatible[j] |= 1 << k; incompatible[k] |= 1 << j
    automatic = []; charges = []
    for k, p in enumerate(fixed):
        vertices = [point(v, p) for v in tips]
        automatic.append(sum(1 << j for j, v in enumerate(vertices)
                             if any(len(set(star(v)) & f) == 5
                                    for l, f in enumerate(fixedfeet) if l != k)))
        charges.append([sum(1 << j for j, v in enumerate(vertices)
                            if len(set(star(v)) & f) == 5) for f in feet])
    return poses, feet, invalid, incompatible, automatic, charges


def all_compatible(incompatible, invalid):
    candidates = ((1 << len(incompatible))-1) & ~sum(1 << i for i in invalid)
    def visit(chosen, rest):
        yield chosen
        while rest:
            bit = rest & -rest; rest ^= bit
            j = bit.bit_length()-1
            yield from visit(chosen | bit, rest & ~incompatible[j])
    yield from visit(0, candidates)


def served(chosen, automatic, charges):
    values = list(automatic)
    while chosen:
        bit = chosen & -chosen; chosen ^= bit; j = bit.bit_length()-1
        for k in range(len(values)):
            values[k] |= charges[k][j]
    return [v.bit_count() for v in values]


def mask(indices):
    need(indices == sorted(set(indices)) and all(type(i) is int and i >= 1 for i in indices), 'index set')
    return sum(1 << (i-1) for i in indices)


def no_saturation(incompatible, invalid, automatic, charges, cuts, threshold=8):
    candidates = ((1 << len(incompatible))-1) & ~sum(1 << i for i in invalid)
    nodes = 0

    def search(chosen, rest, values):
        nonlocal nodes
        nodes += 1
        if any(chosen & c == c for c in cuts):
            return None
        if all(v.bit_count() >= threshold for v in values):
            return chosen
        possible = list(values)
        left = rest
        while left:
            bit = left & -left; left ^= bit; j = bit.bit_length()-1
            for k in range(len(values)):
                possible[k] |= charges[k][j]
        if any(v.bit_count() < threshold for v in possible) or not rest:
            return None
        bit = rest & -rest; j = bit.bit_length()-1; tail = rest ^ bit
        val = [v | charges[k][j] for k, v in enumerate(values)]
        answer = search(chosen | bit, tail & ~incompatible[j], val)
        if answer is not None:
            return answer
        return search(chosen, tail, values)

    answer = search(0, candidates, automatic)
    need(answer is None, 'uncovered saturated selector model: '+str(answer))
    return nodes


def selectors(shape, raw, tips, expected):
    allowed = expected['retained_indices']
    excluded = [r['attachment'] for r in expected['pair_negatives']]
    need(allowed == sorted(set(allowed)) and excluded == sorted(set(excluded)) and
         set(allowed).isdisjoint(excluded) and set(allowed) | set(excluded) == set(range(1, 60)),
         'incomplete attachment partition')
    outer = selector_data(shape, tips, raw, allowed, [IDENT])
    poses, feet, invalid, incompatible, automatic, charges = outer
    need(len(poses) == 21, 'inverse provider inventory')
    cuts = [mask(c['providers']) for c in expected['saturation_cases']]
    total = maximum = saturated = 0
    saturated_sets = []
    for chosen in all_compatible(incompatible, invalid):
        total += 1
        n, = served(chosen, automatic, charges)
        maximum = max(maximum, n)
        if n >= 8:
            saturated += 1
            need(any(chosen & c == c for c in cuts), 'uncovered outer provider configuration')
            saturated_sets.append([j+1 for j in range(len(poses)) if chosen & (1 << j)])
    need(maximum == 8 and saturated > 0, 'charge capacity')
    cases = []
    for case in expected['saturation_cases']:
        fixed = [IDENT]+[poses[i-1] for i in case['providers']]
        inner = selector_data(shape, tips, raw, allowed, fixed)
        ps, fs, bad, clashes, auto, covers = inner
        for row in case['deep_negatives']:
            chosen = mask(row['selected_providers'])
            need(chosen < 1 << len(ps), 'deep index outside inventory')
            need(not chosen & sum(1 << i for i in bad), 'deep forbidden fixed pair')
            need(all(not chosen & clashes[j] for j in range(len(ps)) if chosen & (1 << j)),
                 'deep overlapping/forbidden pair')
            need(min(served(chosen, auto, covers)) >= 8, 'deep cut premise not saturated')
        nodes = no_saturation(clashes, bad, auto, covers,
                              [mask(r['selected_providers']) for r in case['deep_negatives']])
        cases.append({'providers': case['providers'], 'inner_poses': len(ps),
                      'cuts': len(case['deep_negatives']), 'search_nodes': nodes})
    # A provider's charge recipients use the direct, not inverse, attachment pool.
    receivers = [raw[i-1] for i in allowed]
    receiverfeet = [move(shape, p) for p in receivers]
    banned = set(raw)-set(receivers)
    invalid_receivers = {j for j, p in enumerate(receivers) if inverse(p) in banned}
    clashes = [0]*len(receivers)
    for j in range(len(receivers)):
        for k in range(j):
            if receiverfeet[j] & receiverfeet[k] or \
                    compose(inverse(receivers[j]), receivers[k]) in banned or \
                    compose(inverse(receivers[k]), receivers[j]) in banned:
                clashes[j] |= 1 << k; clashes[k] |= 1 << j
    receiver_sets = list(all_compatible(clashes, invalid_receivers))
    maximum_receivers = max(c.bit_count() for c in receiver_sets)
    largest = [[allowed[j] for j in range(len(receivers)) if c & (1 << j)]
               for c in receiver_sets if c.bit_count() == maximum_receivers]
    return {'root_compatible_sets': total, 'root_capacity': maximum,
            'root_saturated_sets': saturated_sets, 'saturation_cases': cases,
            'outgoing_compatible_sets': len(receiver_sets),
            'maximum_distinct_interior_recipients': maximum_receivers,
            'largest_recipient_sets': largest}


def arithmetic(shape, selectors_result):
    vertices = sorted(incidence(shape))
    d2 = max(norm((x[0]-y[0], x[1]-y[1])) for x, y in combinations(vertices, 2))
    witnesses = [(x, y) for x, y in combinations(vertices, 2)
                 if norm((x[0]-y[0], x[1]-y[1])) == d2]
    q = selectors_result['maximum_distinct_interior_recipients']
    denominator = 8*(q+1)
    numerator = denominator+1
    # A > 214*12/(4*7) from sqrt(3)>12/7; enclosing square area <=4D^2(K+1)^2.
    failed = lambda k: 214*3*numerator**k > 28*d2*(k+1)**2*denominator**k
    k = 0
    while not failed(k):
        k += 1
        need(k < 2000, 'arithmetic guard')
    need(failed(k) and not failed(k-1), 'first area contradiction')
    original_first = next(j for j in range(2000)
                          if 214*73**j > 16*24**2*(j+1)**2*72**j)
    need(original_first == 1315, 'original upper arithmetic')
    # Concurrent reviewer1's published385 refinement: integer ceiling growth
    # and a regular circumscribed hexagon. Independently check its arithmetic.
    lower_count = 1
    integer_rows = []
    depth = 0
    while 214*lower_count <= 8*d2*(depth+1)**2:
        if depth >= 383:
            integer_rows.append([depth, lower_count, 214*lower_count, 8*d2*(depth+1)**2])
        lower_count = (numerator*lower_count+denominator-1)//denominator
        depth += 1
        need(depth < 2000, 'integer-growth guard')
    integer_rows.append([depth, lower_count, 214*lower_count, 8*d2*(depth+1)**2])
    need(depth == 384 and lower_count == 2517671, 'concurrent385 arithmetic mismatch')
    return {'exact_diameter_squared': d2, 'diameter_vertex_pairs': witnesses,
            'deficient_assignment_multiplicity': q+1,
            'growth_ratio': [numerator, denominator],
            'area_rational_sqrt3_lower': [12, 7],
            'first_area_contradiction': k, 'square_finite_upper': k+1,
            'finite_upper': depth+1,
            'original_first_area_contradiction': original_first,
            'original_finite_upper': 1316,
            'credited_review1_integer_area_rows': integer_rows,
            'credited_review1_integer_first_contradiction': depth,
            'credited_review1_finite_upper': depth+1}


def mutation_controls():
    tests = [([[1], [-1]], '0\n', True), ([[1, 2], [-1], [-2]], '0\n', True),
             ([[1], [-1]], '', True), ([[1, 2]], '', False),
             ([[1, 2]], '0\n', False), ([[1]], '-1 0\n0\n', False),
             ([[1], [-1]], 'd 1 0\n0\n', True),
             ([[1, 2], [-1]], 'd -1 0\n0\n', False),
             ([[1], [-1]], 'd 2 0\n0\n', False),
             ([[1], [-1]], '0 1\n', False)]
    for clauses, trace, valid in tests:
        try:
            rup(clauses, trace)
        except ValueError:
            need(not valid, 'valid RUP control rejected')
        else:
            need(valid, 'invalid RUP control accepted')
    return len(tests)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--phase', choices=('geometry', 'selectors', 'pairs', 'deep'), required=True)
    ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--stop', type=int)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    started = time.monotonic()
    root = a.root.resolve(); expected = json.loads((root/DIR/'expected.json').read_text())
    manifest_path = Path(__file__).resolve().parent/'INPUT.json'
    manifest = json.loads(manifest_path.read_text())
    need(manifest['commit'] == TARGET_SHA and len(manifest['files']) == 12 and
         len({r['path'] for r in manifest['files']}) == 12, 'input commit/manifest')
    for row in manifest['files']:
        need(hashlib.sha256((root/row['path']).read_bytes()).hexdigest() == row['sha256'],
             'input bytes changed: '+row['path'])
    shape = make_shape()
    raw, wide, tips, corners, rectangles = catalogue(shape)
    pose_sha = lambda poses: hashlib.sha256(json.dumps(poses, separators=(',', ':')).encode()).hexdigest()
    exported = a.work/'native-inventory.json'
    if exported.exists():
        inventory = json.loads(exported.read_text())
        need(inventory['raw'] == [list(p) for p in raw] and
             inventory['wide'] == [list(p) for p in wide], 'entry-level native inventory mismatch')
    base = {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer',
            'source_commit': TARGET_SHA, 'shape_sha256': SHAPE_SHA, 'phase': a.phase,
            'translation_rectangle_cases': rectangles, 'narrow_poses': len(raw), 'wide_poses': len(wide),
            'narrow_pose_sha256': pose_sha(raw), 'wide_pose_sha256': pose_sha(wide)}
    if a.phase == 'geometry':
        result = {'lower_prefixes': lower(root, shape), 'rup_controls': mutation_controls()}
    elif a.phase == 'selectors':
        selected = selectors(shape, raw, tips, expected)
        result = {'selectors': selected, 'arithmetic': arithmetic(shape, selected)}
    elif a.phase == 'pairs':
        end = a.stop if a.stop is not None else len(expected['pair_negatives'])
        need(0 <= a.start < end <= len(expected['pair_negatives']), 'pair range')
        rows = []
        for row in expected['pair_negatives'][a.start:end]:
            i = row['attachment']
            ps, clauses = geometric(shape, corners, wide, [IDENT, raw[i-1]])
            verified = compare_formula(len(ps), clauses, row, a.work/f'pair-{i:02d}')
            rows.append({'attachment': i, **verified})
            print('independent pair', i, 'RUP additions', verified['rup']['additions'], flush=True)
        result = {'pair_negatives': rows}
    else:
        outerposes, *_ = selector_data(shape, tips, raw, expected['retained_indices'], [IDENT])
        rows = []
        for case in expected['saturation_cases']:
            fixed = [IDENT]+[outerposes[i-1] for i in case['providers']]
            innerposes, *_ = selector_data(shape, tips, raw, expected['retained_indices'], fixed)
            label = '-'.join(map(str, case['providers']))
            for j, row in enumerate(case['deep_negatives']):
                allfixed = fixed+[innerposes[i-1] for i in row['selected_providers']]
                ps, clauses = geometric(shape, corners, wide, allfixed)
                folder = a.work/('saturation-'+label)/f'deep-{j:02d}'
                verified = compare_formula(len(ps), clauses, row, folder)
                rows.append({'providers': case['providers'], 'deep_case': j, **verified})
                print('independent deep', label, j, 'RUP additions', verified['rup']['additions'], flush=True)
        # The remaining five formulas are audited by the same RUP implementation;
        # selector soundness/completeness is independently closed without auxiliaries.
        selector_rows = []
        for label, row in [('capacity-nine', expected['capacity_nine']),
                           ('forced-deficit-final', expected['forced_deficit_final'])]+[
                ('saturation-'+'-'.join(map(str, c['providers']))+'/final', c['final'])
                for c in expected['saturation_cases']]:
            folder = a.work/label
            text = (folder/'instance.cnf').read_text()
            need(hashlib.sha256(text.encode()).hexdigest() == row['cnf_sha256'], 'selector CNF hash')
            clauses = [list(map(int, line.split()))[:-1] for line in text.splitlines()
                       if not line.startswith(('c', 'p'))]
            proof = (folder/'proof.drat').read_text()
            selector_rows.append({'label': label, 'cnf_sha256': row['cnf_sha256'],
                                  'rup': rup(clauses, proof),
                                  'trace_sha256': hashlib.sha256(proof.encode()).hexdigest()})
        result = {'deep_negatives': rows, 'selector_traces': selector_rows}
    a.output.write_text(json.dumps({**base, **result}, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'phase': a.phase, 'seconds': round(time.monotonic()-started, 6),
                      'output': str(a.output)}), flush=True)


if __name__ == '__main__':
    main()
