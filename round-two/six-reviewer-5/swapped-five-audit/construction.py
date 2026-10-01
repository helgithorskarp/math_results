"""Independent matrix construction and complete ordinary one-cap census.

No researcher generator, field arithmetic or witness checker is imported.
"""
from collections import Counter
from itertools import combinations, product
import json
from core import HERE, G, code_check, digest, image, mask, pin_inputs, points, require

def multiply(a, b):
    polynomial = 0
    for i in range(4):
        for j in range(4):
            if a >> i & 1 and b >> j & 1:
                polynomial ^= 1 << (i + j)
    for k in range(6, 3, -1):
        if polynomial >> k & 1:
            polynomial ^= 19 << (k - 4)
    return polynomial

M = tuple(tuple(multiply(a, b) for b in range(16)) for a in range(16))
INV = {a: next(b for b in range(1, 16) if M[a][b] == 1) for a in range(1, 16)}

def power(a, n):
    r = 1
    for _ in range(n):
        r = M[r][a]
    return r

SUB = (0, 1, 6, 7)
FIELD = tuple(SUB[x] ^ M[2][SUB[y]] for y in range(4) for x in range(4))
COORD = {a: i for i, a in enumerate(FIELD)}

def plane():
    require(len(COORD) == 16, 'coordinate basis')
    require({a for a in range(16) if power(a, 4) == a} == set(SUB), 'subfield')
    require(all(M[a][M[b][c]] == M[M[a][b]][c] for a, b, c in product(range(16), repeat=3)),
            'field associativity')
    matrices = set()
    for row in product(range(16), repeat=4):
        a, b, c, d = row
        if M[a][d] == M[b][c]:
            continue
        scale = INV[next(x for x in row if x)]
        matrices.add(tuple(M[scale][x] for x in row))
    require(len(matrices) == 4080, 'projective matrix count')
    base = (16,) + tuple(COORD[a] for a in SUB)
    permutations, blocks = set(), set()
    for a, b, c, d in sorted(matrices):
        q = []
        for z in FIELD:
            denominator = M[c][z] ^ d
            q.append(16 if denominator == 0 else COORD[M[M[a][z] ^ b][INV[denominator]]])
        q.append(16 if c == 0 else COORD[M[a][INV[c]]])
        require(sorted(q) == list(range(17)), 'projective permutation')
        permutations.add(tuple(q))
        blocks.add(mask(q[v] for v in base))
    require(len(permutations) == 4080 and len(blocks) == 68, 'literal projective action')
    blocks = tuple(sorted(blocks))
    code_check(blocks, G)
    owners = Counter(t for w in blocks for t in combinations(points(w), 3))
    require(set(owners) == set(combinations(range(17), 3)) and set(owners.values()) == {1},
            'complete Steiner triple ownership')
    return blocks

def matchings(cap):
    """Every inclusion-perfect matching from cap triples to cap pairs."""
    triples, pairs = tuple(combinations(cap, 3)), tuple(combinations(cap, 2))
    index = {p: i for i, p in enumerate(pairs)}
    output = []
    def visit(k, used, omissions):
        if k == len(triples):
            require(used == (1 << len(pairs)) - 1, 'matching not surjective')
            output.append(omissions)
            return
        for a in triples[k]:
            p = tuple(v for v in triples[k] if v != a)
            bit = 1 << index[p]
            if not used & bit:
                visit(k + 1, used | bit, omissions + (a,))
    visit(0, 0, ())
    require(len(output) == len(set(output)) == 60, 'Petersen permanent')
    return triples, tuple(output)

def transfer(blocks, cap, omissions):
    old = set(blocks)
    require(len(cap) == 5 and all(0 <= v < 17 for v in cap), 'old five-cap domain')
    cap = frozenset(cap)
    require(max(len(cap & frozenset(points(w))) for w in blocks) <= 3, 'cap meets block in four')
    parents = {w for w in blocks if len(cap & frozenset(points(w))) == 3}
    require(len(parents) == 10 and set(omissions) == parents, 'ten parent omissions required')
    require(all(a in cap and w >> a & 1 for w, a in omissions.items()), 'omission outside triple')
    tails = tuple(w & ~(1 << omissions[w]) for w in sorted(parents))
    require(all((a & b).bit_count() <= 1 for a, b in combinations(tails, 2)), 'incompatible tails')
    words = tuple(sorted((old - parents) | {mask(cap)} | {w | (1 << 17) for w in tails}))
    require(len(words) == 69, 'trade size')
    code_check(words)
    return words

def check_witness(data, blocks):
    words, g, centers = data['words'], data['involution'], data['centers']
    require(len(words) == 69 and len(g) == 18 and sorted(g) == list(range(18)), 'witness size/map')
    require(all(g[g[v]] == v for v in range(18)) and sum(g[v] == v for v in range(18)) == 2,
            'witness involution cycle type')
    require(len(centers) == 2 and len(set(centers)) == 2 and
            all(type(v) is int and 0 <= v < 18 for v in centers), 'witness centers')
    x, y = centers
    require(g[x] == y, 'centers not exchanged')
    degrees = code_check(words, g)
    require(degrees[x] == degrees[y] == 20 and sum(w >> x & 1 and w >> y & 1 for w in words) == 5,
            'witness replications/pair multiplicity')
    require(tuple(data['replications']) == degrees, 'witness degree readout')
    omissions = data['construction']['omissions']
    require(len(omissions) == len({w for w, a in omissions}) == 10, 'duplicate parent record')
    recreated = transfer(blocks, points(data['construction']['cap']), dict(omissions))
    require(tuple(sorted(words)) == recreated, 'trade does not decode to witness')
    return {'words': 69, 'pairs_checked': 2346, 'degrees': degrees,
            'degree_profile': sorted(Counter(degrees).items()),
            'fixed_words': sum(image(w, g) == w for w in words), 'pair_multiplicity': 5}

def audit():
    pin_inputs()
    blocks = plane()
    data = json.loads((HERE / 'WITNESS69.json').read_text())
    witness = check_witness(data, blocks)
    caps = []
    for pair in combinations(range(8), 2):
        cap = tuple(sorted((16,) + tuple(v for i in pair for v in (2 * i, 2 * i + 1))))
        if mask(cap) not in blocks:
            caps.append(cap)
    require(len(caps) == 24, 'complete fixed-cap carrier')
    records, all_codes, fixed_codes, g_patterns = [], set(), set(), 0
    for cap in caps:
        triples, patterns = matchings(cap)
        parent = {t: next(w for w in blocks if all(w >> v & 1 for v in t)) for t in triples}
        ordinary, invariant, paired = 0, 0, 0
        for omitted in patterns:
            assignments = dict(zip((parent[t] for t in triples), omitted))
            equivariant = all(assignments[image(w, G)] == G[a] for w, a in assignments.items())
            paired += equivariant
            tails = [w & ~(1 << a) for w, a in assignments.items()]
            if any((a & b).bit_count() > 1 for a, b in combinations(tails, 2)):
                continue
            words = transfer(blocks, cap, assignments)
            ordinary += 1
            all_codes.add(words)
            closed = {image(w, G) for w in words} == set(words)
            require(closed == equivariant, 'equivariance versus literal closure')
            if closed:
                invariant += 1
                fixed_codes.add(words)
        g_patterns += paired
        records.append({'cap': cap, 'pair_matchings': len(patterns),
                        'equivariant_pair_matchings': paired, 'ordinary_trades': ordinary,
                        'invariant_trades': invariant})
    maps, images, stabilizer = [], set(), []
    base = tuple(sorted(data['words']))
    for e in range(4):
        for b in range(16):
            q = tuple(COORD[power(z, 1 << e) ^ b] for z in FIELD) + (16, 17)
            require(sorted(q) == list(range(18)) and all(q[G[v]] == G[q[v]] for v in range(18)),
                    'commuting affine Frobenius permutation')
            require({image(w, q) for w in blocks} == set(blocks), 'plane not preserved')
            transformed = tuple(sorted(image(w, q) for w in base))
            images.add(transformed)
            maps.append(q)
            if transformed == base:
                stabilizer.append(q)
    require(len(set(maps)) == 64 and images == fixed_codes, 'complete field orbit equality')
    group = set(maps)
    require(all(tuple(a[b[v]] for v in range(18)) in group for a, b in product(maps, repeat=2)),
            'field-map closure')
    h = tuple(COORD[power(z, 4) ^ 2] for z in FIELD) + (16, 17)
    require(power(2, 4) ^ 2 == 1 and tuple(h[h[v]] for v in range(18)) == G, 'order-four square')
    require(h in stabilizer and len(stabilizer) == 4 and h != G, 'cyclic stabilizer')
    remaining, ordinary_orbits = set(all_codes), []
    while remaining:
        root = min(remaining)
        orbit = {tuple(sorted(image(w, q) for w in root)) for q in maps}
        require(orbit <= remaining, 'ordinary cap-family orbit escaped or overlapped')
        fixing = [q for q in maps if tuple(sorted(image(w, q) for w in root)) == root]
        require(len(orbit) * len(fixing) == 64, 'ordinary orbit-stabilizer')
        invariant = sum(words in fixed_codes for words in orbit)
        require(invariant in (0, len(orbit)), 'commuting maps changed invariant status')
        ordinary_orbits.append({'labelled_codes': len(orbit), 'invariant_codes': invariant,
                                'stabilizer_order': len(fixing), 'root_sha256': digest(root)})
        remaining -= orbit
    acl = [int(line.strip(), 2) for line in (HERE / 'inputs/acl69.txt').read_text().splitlines()
           if len(line.strip()) == 18 and set(line.strip()) <= {'0', '1'}]
    require(len(acl) == 69, 'ACL baseline decoding')
    acl_degrees = code_check(acl)
    return {'status': 'PASS_INDEPENDENT_CONSTRUCTION_AND_ORDINARY_CAP_CENSUS',
            'steiner_blocks': len(blocks), 'triple_owners': 680, 'projective_maps': 4080,
            'plane_sha256': digest(blocks), 'witness': witness,
            'caps': len(caps), 'ordinary_pair_matchings_per_cap': 60,
            'ordinary_pair_matchings': sum(r['pair_matchings'] for r in records),
            'equivariant_pair_matchings': g_patterns,
            'ordinary_trades': sum(r['ordinary_trades'] for r in records),
            'distinct_ordinary_codes': len(all_codes), 'invariant_trades': len(fixed_codes),
            'ordinary_codes_sha256': digest(sorted(all_codes)), 'invariant_codes_sha256': digest(sorted(fixed_codes)),
            'per_cap': records, 'actual_field_maps': 64, 'stabilizer_order': len(stabilizer),
            'ordinary_field_orbits': ordinary_orbits,
            'order_four_generator': h, 'acl_degree_profile': sorted(Counter(acl_degrees).items())}

if __name__ == '__main__':
    print(json.dumps(audit(), sort_keys=True))
