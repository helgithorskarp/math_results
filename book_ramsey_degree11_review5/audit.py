"""Independent Book Ramsey degree-eleven audit; six-reviewer-5.

CPython 3.11+, standard library. No researcher code or census input.
Written counting arguments, not finite identity controls, establish the
universal histogram exclusions. Explicit checks also run under python -O.
"""
from collections import Counter
from functools import cache
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent


def check(ok, message):
    if not ok:
        raise ValueError(message)


@cache
def labeled_count(degrees):
    """Degree-class recurrence; distinguished maximum-degree vertex.

    Sorting preserves the number of labeled realizations, not their labels.
    Binomial weights count which labels in each degree class are neighbors.
    This computes a count without generating any graph or edge mask.
    """
    if not degrees:
        return 1
    d, rest = degrees[-1], degrees[:-1]
    if d == 0:
        return 1
    if sum(degrees) % 2 or d >= len(degrees):
        return 0
    counts = Counter(rest)
    classes = sorted(h for h in counts if h)
    answer = 0
    for choices in product(*(range(min(d, counts[h]) + 1) for h in classes)):
        if sum(choices) != d:
            continue
        new = [0] * counts[0]
        weight = 1
        for h, k in zip(classes, choices):
            weight *= comb(counts[h], k)
            new.extend([h - 1] * k + [h] * (counts[h] - k))
        answer += weight * labeled_count(tuple(sorted(new)))
    return answer


def domain(n):
    """Adaptive residual-vertex deletion, independent of label order.

    Choose fewest possible neighbor subsets; ties prefer the largest label.
    Only parity and literal positive-degree availability prune branches.
    Each graph has one path because the chosen vertex is deterministic.
    """
    pairs = list(combinations(range(n), 2))
    bits = {edge: 1 << k for k, edge in enumerate(pairs)}
    need = [0, 2, 2, 2] + [3] * (n - 4)
    start = sum(bits[0, j] for j in (1, 2, 3))
    answers = []
    nodes = 0

    def visit(mask):
        nonlocal nodes
        nodes += 1
        active = [v for v in range(1, n) if need[v]]
        if not active:
            answers.append(mask)
            return
        k = len(active)
        if sum(need[v] for v in active) % 2 or any(need[v] >= k for v in active):
            return
        v = min(active, key=lambda w: (comb(k - 1, need[w]), -w))
        d = need[v]
        available = [w for w in active if w != v]
        need[v] = 0
        for chosen in combinations(available, d):
            nxt = mask
            for w in chosen:
                need[w] -= 1
                nxt |= bits[tuple(sorted((v, w)))]
            visit(nxt)
            for w in chosen:
                need[w] += 1
        need[v] = d

    visit(start)
    check(len(answers) == len(set(answers)), 'duplicate adaptive terminal')
    validate_domain(set(answers), n)
    return set(answers), nodes


def validate_domain(answers, n):
    check(len(answers) == labeled_count(tuple(sorted([2] * 3 + [3] * (n - 4)))),
          'independent degree-class count disagrees')
    for m in answers:
        rows = decode(m, n)
        check(all(len(row) == 3 for row in rows) and rows[0] == {1, 2, 3},
              'noncubic or nonnormalized terminal')


def decode(mask, n):
    check(type(mask) is int and 0 <= mask < (1 << comb(n, 2)), 'mask outside domain')
    rows = [set() for _ in range(n)]
    for k, (a, b) in enumerate(combinations(range(n), 2)):
        if mask & (1 << k):
            rows[a].add(b)
            rows[b].add(a)
    return rows


def core(mask):
    rows = decode(mask, 10) + [set(), set()]
    check(rows[0] == {1, 2, 3} and all(len(row) == 3 for row in rows[:10]),
          'invalid normalized cubic')
    rows[0].remove(1)
    rows[1].remove(0)
    rows[0].add(10)
    rows[10].add(0)
    for v in range(11):
        rows[v].add(11)
        rows[11].add(v)
    return rows


def spines(rows):
    full = set(range(len(rows)))
    check(all(v not in rows[v] for v in full) and
          all((b in rows[a]) == (a in rows[b]) for a, b in combinations(full, 2)),
          'graph is not simple symmetric')
    values = []
    for a, b in combinations(range(len(rows)), 2):
        red = b in rows[a]
        pages = len(rows[a] & rows[b]) if red else len(full - rows[a] - rows[b] - {a, b})
        values.append((a, b, red, pages))
    return values


def orbit_table(labeled):
    pairs = list(combinations(range(10), 2))
    index = {edge: k for k, edge in enumerate(pairs)}
    maps = [(0, 1) + low + high for low in ((2, 3), (3, 2))
            for high in permutations(range(4, 10))]
    check(len(set(maps)) == 1440, 'wrong action group')
    maps = [[1 << index[tuple(sorted((p[a], p[b])))] for a, b in pairs] for p in maps]
    remaining = set(labeled)
    records = []
    core_checks = 0
    while remaining:
        representative = min(remaining)
        edges = [k for k in range(45) if representative & (1 << k)]
        orbit = {sum(action[k] for k in edges) for action in maps}
        check(orbit <= remaining, 'orbit overlaps another orbit or exits exact domain')
        check(min(orbit) == representative, 'representative not minimal')
        remaining -= orbit
        rows = core(representative)
        values = spines(rows)
        check(all(p <= (3 if red else 6) for _, _, red, p in values), 'invalid core')
        check(sum(len(row) for row in rows) // 2 == 26, 'wrong core edge count')
        check(sorted(len(rows[v] - {11}) for v in range(11)) == [1, 2] + [3] * 9,
              'wrong local histogram')
        check([v for v in range(12) if len(rows[v]) == 11] == [11],
              'root is not recoverable without marking')
        core_checks += len(values)
        records.append({'mask': representative, 'orbit_size': len(orbit)})
    check(sum(r['orbit_size'] for r in records) == len(labeled), 'incomplete orbit cover')
    return records, core_checks


def phi(z):
    return (z - 3) * (z - 4) // 2


def identity_control(jrows, sizes, salt, offset=0):
    """Literal full-graph pages vs derived residual and general row identities.

    Deliberately invalid controls are allowed; slack may be negative.
    Arbitrary J is allowed: the total-degree correction is mandatory.
    """
    rows = [set(row) for row in jrows] + [{*range(11)}] + [set() for _ in range(10)]
    for a in range(11):
        rows[a].add(11)
    zsets = []
    for b, size in enumerate(sizes, 12):
        order = sorted(range(11), key=lambda a: hashlib.sha256(f'{salt}:{b}:{a}'.encode()).digest())
        z = set(order[:size])
        zsets.append(z)
        for a in set(range(11)) - z:
            rows[a].add(b)
            rows[b].add(a)
    for b, c in combinations(range(12, 22), 2):
        if (b * c + salt + b + c) % 3 == 0:
            rows[b].add(c)
            rows[c].add(b)
    h = list(map(len, jrows))
    t = [sum(a in z for z in zsets) for a in range(11)]
    slack = [[0] * 11 for _ in range(11)]
    unused = 0
    for a, b, red, pages in spines(rows):
        if b < 11:
            s = (3 if red else 6) - pages
            slack[a][b] = slack[b][a] = s
            unused += s
    for a, b in combinations(range(11), 2):
        common = len(jrows[a] & jrows[b])
        base = t[a] + t[b] - 8 if b in jrows[a] else h[a] + h[b] - 3
        check(sum(a in z and b in z for z in zsets) == base - common - slack[a][b],
              'mixed spine identity')
    for a in range(11):
        pt = sum(t[b] for b in jrows[a])
        ph = sum(h[b] for b in jrows[a])
        u = sum(len(z) - 4 for z in zsets if a in z)
        lhs = (3 - h[a]) * t[a] - pt
        rhs = 5 * h[a] - h[a] ** 2 + sum(h) - 30 - 2 * ph - sum(slack[a]) - u + offset
        check(lhs == rhs, 'general row identity')
    # Works for any eleven-vertex local graph, not just the three histograms.
    twice_d = sum(16 * x - 3 * x * x for x in h) - 210
    mandatory = sum((3 - x) * x for x in h)
    residual = unused + sum(phi(len(z)) for z in zsets) + sum(
        (3 - h[a]) * (11 - len(rows[a])) for a in range(11))
    check(2 * residual == twice_d - 2 * mandatory, 'column residual identity')
    return {'mixed': 55, 'rows': 11, 'residual': 1, 'total_h': sum(h)}


def controls(records):
    total = Counter()
    for k, record in enumerate(records):
        rows = [r - {11} for r in core(record['mask'])[:11]]
        for sizes in ([4] * 10, [4, 5] * 5, list(range(1, 11))):
            x = identity_control(rows, sizes, 9001 + k)
            total.update({name: x[name] for name in ('mixed', 'rows', 'residual')})
    # Surviving histogram: start with the hexagonal prism, remove vertex0,
    # then link its former neighbors1,5; its third neighbor retains degree two.
    cubic12 = [set() for _ in range(12)]
    for a in range(6):
        for b, c in ((a, (a + 1) % 6), (a + 6, (a + 1) % 6 + 6), (a, a + 6)):
            cubic12[b].add(c); cubic12[c].add(b)
    j32 = [set(b - 1 for b in cubic12[a] if b) for a in range(1, 12)]
    j32[0].add(4); j32[4].add(0)
    check(sorted(map(len, j32)) == [2] + [3] * 10, 'bad surviving-histogram control')
    for salt in range(6):
        x = identity_control(j32, [(b + salt) % 12 for b in range(10)], 10001 + salt)
        total.update({name: x[name] for name in ('mixed', 'rows', 'residual')})
    for density in range(7):
        arbitrary = [set() for _ in range(11)]
        for a, b in combinations(range(11), 2):
            if (a * 7 + b * 11 + a * b) % 6 < density:
                arbitrary[a].add(b); arbitrary[b].add(a)
        x = identity_control(arbitrary, [(b + density) % 12 for b in range(10)],
                             11001 + density)
        total.update({name: x[name] for name in ('mixed', 'rows', 'residual')})
    failed = False
    try:
        identity_control(j32, [4] * 10, 123, offset=-2)
    except ValueError:
        failed = True
    check(failed, 'missing total-degree correction was not rejected')
    total['missing_plus_two_rejected'] = 1
    return dict(total)


def scalar_audit():
    degree_bounds = {}
    for r, s, start in ((3, 6, 12), (6, 3, 15)):
        degree_bounds[f'{r},{s}'] = []
        for d in range(start, 22):
            q = 21 - d
            upper = d * max((3 * d + r - s - 4 - q) * h - 3 * h * h
                            for h in range(r + 1)) + 2 * (s - d + 2) * comb(d, 2) + q * r * (r + 1)
            check(upper < 0, 'degree upper bound does not exclude case')
            degree_bounds[f'{r},{s}'].append([d, upper])
    histograms = []
    for n1, n2 in product((0, 1), (1, 3, 5, 7)):
        hs = [1] * n1 + [2] * n2 + [3] * (11 - n1 - n2)
        twice_d = sum(16 * h - 3 * h * h for h in hs) - 210
        e = twice_d // 2 - sum((3 - h) * h for h in hs)
        check(2 * e == 21 - 12 * n1 - 5 * n2, 'histogram residual')
        histograms.append({'n1': n1, 'n2': n2, 'E': e})
    check([(x['n1'], x['n2']) for x in histograms if x['E'] >= 0] == [(0, 1), (0, 3), (1, 1)],
          'wrong residual survivors')
    direct = []
    scalar_vectors = 0
    for n0 in range(12):
        for n1 in range(12 - n0):
            for n2 in range(12 - n0 - n1):
                n3 = 11 - n0 - n1 - n2
                scalar_vectors += 1
                hs = [0] * n0 + [1] * n1 + [2] * n2 + [3] * n3
                twice_e = sum(16 * h - 3 * h * h - 2 * (3 - h) * h for h in hs) - 210
                check(twice_e == 21 - 21 * n0 - 12 * n1 - 5 * n2,
                      'direct residual formula')
                if twice_e >= 0 and sum(hs) % 2 == 0:
                    direct.append([n0, n1, n2, n3, twice_e // 2])
    check(scalar_vectors == 364 and direct ==
          [[0, 0, 1, 10, 8], [0, 0, 3, 8, 3], [0, 1, 1, 9, 2], [1, 0, 0, 10, 0]],
          'direct four-case coverage')
    # Verify the all-size inequalities used for u_i, not only z=4/5.
    penalties = []
    for z in range(12):
        check(phi(z) >= 0 and z - 4 <= phi(z), 'miss-size penalty fails')
        penalties.append([z, phi(z), phi(z) - (z - 4)])
    # Only bounding arithmetic is computational; the proof uses actual graphs.
    for triple in product(range(1, 4), repeat=3):
        check(2 * sum(triple) - 6 <= 12 < 15, 'saturated cubic contradiction')
    # Necessary localized budget in the remaining unique-degree-two case.
    # t ranges2..6 by the already established full degree bounds7..11.
    cuts = []
    for t, triangle in product(range(2, 7), (0, 1)):
        lower = 12 - 3 * t + 2 * triangle
        upper = 10 - t
        check(lower <= upper, 'unexpected scalar contradiction in surviving class')
        cuts.append({'t': t, 'triangle_at_degree_two_vertex': bool(triangle),
                     'blue_incident_slack_plus_u_lower': lower, 'U_plus_F': upper})
    return {'degree_bounds': degree_bounds, 'old_histogram_residuals': histograms,
            'all_scalar_vectors': scalar_vectors, 'direct_residual_survivors': direct,
            'surviving_localized_cuts': cuts,
            'size_penalties': penalties, 'cubic_neighbor_triples': 27}


def baseline():
    data = (HERE / 'primary21.txt').read_bytes()
    check(hashlib.sha256(data).hexdigest() ==
          '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
          'primary matrix bytes changed')
    # The data file's search metadata is never executed.
    literal = data.decode().split('\n\n', 1)[0]
    matrix = ast.literal_eval(literal)
    check(type(matrix) is list and len(matrix) == 21 and
          all(type(r) is list and len(r) == 21 and all(type(x) is int and x in (0, 1) for x in r)
              for r in matrix), 'bad primary matrix')
    check(all(matrix[i][i] == 0 for i in range(21)) and
          all(matrix[i][j] == matrix[j][i] for i, j in combinations(range(21), 2)),
          'nonsimple primary matrix')
    rows = [{j for j in range(21) if j != i and matrix[i][j] == 0} for i in range(21)]
    values = spines(rows)
    caps = [max(p for _, _, red, p in values if red),
            max(p for _, _, red, p in values if not red)]
    check(caps == [3, 6], 'primary matrix color orientation')
    return {'edges': sum(map(len, rows)) // 2,
            'degrees': dict(sorted(Counter(map(len, rows)).items())), 'caps': caps,
            'input_sha256': hashlib.sha256(data).hexdigest()}


def corruption_controls(labeled, records):
    cases = []
    for name, bad in [('omitted_terminal', set(labeled) - {min(labeled)}),
                      ('noncubic_terminal', (set(labeled) - {min(labeled)}) | {0})]:
        rejected = False
        try:
            validate_domain(bad, 10)
        except ValueError:
            rejected = True
        check(rejected, 'wrong domain size not rejected')
        cases.append(name)
    bad = [dict(r) for r in records]
    bad[0]['orbit_size'] += 1
    check(sum(r['orbit_size'] for r in bad) != len(labeled), 'altered orbit size not rejected')
    cases.append('altered_orbit_size')
    return cases


def audit():
    counts, nodes = {}, {}
    labeled = None
    for n in (4, 6, 8, 10):
        d, visited = domain(n)
        counts[str(n)] = len(d)
        nodes[str(n)] = visited
        if n == 10:
            labeled = d
    check(counts == {'4': 1, '6': 7, '8': 553, '10': 133105}, 'complete domain counts')
    records, core_checks = orbit_table(labeled)
    check(len(records) == 148, 'wrong number of unmarked core types')
    digest = hashlib.sha256(''.join(f'{x}\n' for x in sorted(labeled)).encode()).hexdigest()
    return {'agent': 'six-reviewer-5', 'role': 'independent mathematical reviewer',
            'complete': True, 'schema': 'book-degree11-independent-review-v1',
            'normalized_counts': counts, 'adaptive_nodes': nodes,
            'degree_class_recurrence_states': labeled_count.cache_info().currsize,
            'domain_sha256': digest, 'core_types': len(records), 'group_order': 1440,
            'core_spines_checked': core_checks,
            'orbit_size_histogram': dict(sorted(Counter(r['orbit_size'] for r in records).items())),
            'records': records, 'identity_controls': controls(records),
            'scalar_audit': scalar_audit(), 'baseline': baseline(),
            'negative_controls': corruption_controls(labeled, records)}


if __name__ == '__main__':
    result = audit()
    serialized = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if (HERE / 'expected.json').exists():
        check(serialized == (HERE / 'expected.json').read_text(), 'expected summary mismatch')
    print(serialized, end='')
