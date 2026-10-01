"""Independent exact audit by six-reviewer-2; no author code is imported."""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import json
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def encode(points):
    return sum(1 << p for p in points)


def points(word, size=17):
    require(type(word) is int and 0 <= word < 1 << size, 'invalid mask')
    return tuple(p for p in range(size) if word & (1 << p))


def field_product(a, b):
    # Polynomial convolution, followed by long division by X^4+X+1.
    coefficients = [0] * 7
    for i, j in product(range(4), repeat=2):
        coefficients[i + j] ^= ((a >> i) & 1) & ((b >> j) & 1)
    for degree in range(6, 3, -1):
        if coefficients[degree]:
            for offset in (0, 1, 4):
                coefficients[degree - 4 + offset] ^= 1
    return sum(coefficients[i] << i for i in range(4))


def classical_circles():
    multiplication = [[field_product(a, b) for b in range(16)] for a in range(16)]
    def power(a, n):
        result = 1
        for _ in range(n):
            result = multiplication[result][a]
        return result
    subfield = tuple(a for a in range(16) if power(a, 4) == a)
    require(len(subfield) == 4, 'subfield size')
    # Twenty affine subfield lines, with the point at infinity appended.
    lines = {encode([16] + [c ^ multiplication[b][t] for t in subfield])
             for c in range(16) for b in range(1, 16)}
    # Forty-eight norm circles: N(x-c)=(x-c)^5 in GF(4)^*.
    norm = [power(a, 5) for a in range(16)]
    finite = {encode(x for x in range(16) if norm[x ^ c] == r)
              for c in range(16) for r in subfield if r}
    require(len(lines) == 20 and len(finite) == 48 and not lines & finite,
            'classical circle inventory')
    return sorted(lines | finite)


def prepare(given):
    raw = given['design_circles']
    require(type(raw) is list and len(raw) == 68 and raw == sorted(set(raw)),
            'invalid circle inventory')
    circles = [frozenset(points(c)) for c in raw]
    require(all(len(c) == 5 for c in circles), 'wrong circle weight')
    require(raw == classical_circles(), 'norm construction differs from input')
    triple_owner = {}
    for i, circle in enumerate(circles):
        for t in combinations(sorted(circle), 3):
            require(t not in triple_owner, 'repeated triple')
            triple_owner[t] = i
    require(set(triple_owner) == set(combinations(range(17), 3)), 'missing triple')
    words = sorted(encode(q) for q in combinations(range(17), 4)
                   if not any(set(q) <= c for c in circles))
    require(len(words) == 2040, 'wrong noncontained inventory')
    owners = {}
    for q in words:
        indices = {triple_owner[t] for t in combinations(points(q), 3)}
        require(len(indices) == 4, 'owner count is not four')
        direct = {i for i, c in enumerate(raw) if (q & c).bit_count() >= 3}
        require(indices == direct, 'triple-owner/direct-circle mismatch')
        owners[q] = sum(1 << i for i in indices)
    root = given['root_word']
    require(root in owners, 'root is not noncontained')
    maps = given['actual_transport_generators']
    require(type(maps) is list and len(maps) == 4, 'wrong map count')
    for permutation in maps:
        require(sorted(permutation) == list(range(17)), 'map is not a permutation')
        moved = {encode(permutation[x] for x in c) for c in circles}
        require(moved == set(raw), 'map does not preserve circles')
    orbit, queue = {root}, [root]
    for q in queue:
        for permutation in maps:
            moved = encode(permutation[x] for x in points(q))
            if moved not in orbit:
                orbit.add(moved)
                queue.append(moved)
    require(orbit == set(words), 'incomplete root transport orbit')
    return raw, words, owners, root, orbit


def run(given, max_products=1200000, max_seconds=45):
    start = time.monotonic()
    def guard(count=0):
        if count > max_products or time.monotonic() - start > max_seconds:
            raise RuntimeError('INCOMPLETE: no negative mathematical verdict')
    require(max_products >= 0 and max_seconds >= 0, 'invalid resource guard')
    raw, words, owners, root, orbit = prepare(given)
    guard()
    compatible = lambda a, b: (a & b).bit_count() <= 1
    shares = lambda a, b: bool(owners[a] & owners[b])
    partners, opposites = [], []
    # The global pair bridge is checked on every compatible pair.
    compatible_pair_count = 0
    for a, b in combinations(words, 2):
        if compatible(a, b):
            compatible_pair_count += 1
            require((owners[a] & owners[b]).bit_count() <= 1,
                    'compatible pair shares more than one circle')
    for q in words:
        if compatible(q, root):
            (partners if shares(q, root) else opposites).append(q)
    root_indices = [i for i in range(68) if owners[root] & (1 << i)]
    groups = [[q for q in partners if owners[q] & owners[root] == 1 << i]
              for i in root_indices]
    require(list(map(len, groups)) == [33] * 4 and len(partners) == 132
            and len(opposites) == 1461, 'root carriers')
    edges = [tuple((a, b)) for a, b in combinations(partners, 2)
             if compatible(a, b) and shares(a, b)]
    frames, boundary_frames = [], []
    histogram, gap_histogram = Counter(), Counter()
    products_examined = 0
    # All 33^4 products are visited. No graph-pattern or connected-growth search.
    for neighbor_tuple in product(*groups):
        products_examined += 1
        if products_examined % 1024 == 0:
            guard(products_examined)
        pairs = tuple(combinations(neighbor_tuple, 2))
        if not all(compatible(a, b) for a, b in pairs):
            continue
        edge_count = sum(shares(a, b) for a, b in pairs)
        if edge_count < 2:
            continue
        frame = tuple(sorted(neighbor_tuple))
        boundary_frames.append(frame)
        if edge_count >= 3:
            frames.append(frame)
            degrees = sorted(sum(shares(a, b) for b in frame if a != b) for a in frame)
            histogram[','.join(map(str, degrees))] += 1
            union = owners[root]
            for q in frame:
                union |= owners[q]
            gap_histogram[str(union.bit_count())] += 1
    guard(products_examined)
    frames.sort()
    boundary_frames.sort()
    require(len(frames) == len(set(frames)) and
            len(boundary_frames) == len(set(boundary_frames)), 'duplicate frame')
    failures, equalities = [], []
    equality_degrees = Counter()
    negative_tests = boundary_tests = 0
    # Equality needs >=2 neighbor edges; a putative union <=13 needs >=3.
    for frame in boundary_frames:
        union = owners[root]
        for q in frame:
            union |= owners[q]
        is_negative_frame = union.bit_count() <= 13
        for z in opposites:
            boundary_tests += 1
            if is_negative_frame:
                negative_tests += 1
            size = (union | owners[z]).bit_count()
            if size > 14 or not all(compatible(z, q) for q in frame):
                continue
            family = tuple(sorted((root, *frame, z)))
            if size <= 13:
                failures.append(family)
            if size == 14:
                equalities.append(family)
                degree_tuple = tuple(sorted(sum(shares(a, b) for b in family if a != b)
                                            for a in family))
                equality_degrees[','.join(map(str, degree_tuple))] += 1
        guard(products_examined)
    require(not failures, 'counterexample: union at most thirteen')
    require(len(equalities) == len(set(equalities)), 'duplicate equality key')
    # Any seven-word family of cost <=15 has a six-word subfamily of cost14.
    # Normalize a degree-four root of that subfamily, then exhaust all words.
    seven_tests, seven_failures = 0, []
    for family in equalities:
        union = 0
        for q in family:
            union |= owners[q]
        for q in words:
            seven_tests += 1
            if q not in family and (union | owners[q]).bit_count() <= 15 \
                    and all(compatible(q, a) for a in family):
                seven_failures.append(tuple(sorted((*family, q))))
        guard(products_examined)
    require(not seven_failures, 'seven-word family has cost at most fifteen')
    seven_sharp = [15, 240, 6161, 9249, 16964, 33156, 74048]
    require(len(set(seven_sharp)) == 7 and all(q in owners for q in seven_sharp)
            and all(compatible(a, b) for a, b in combinations(seven_sharp, 2)),
            'invalid seven-word sharp family')
    seven_removed = 0
    for q in seven_sharp:
        seven_removed |= owners[q]
    seven_code = sorted([c for i, c in enumerate(raw) if not seven_removed & (1 << i)]
                        + [q | (1 << 17) for q in seven_sharp])
    require(seven_removed.bit_count() == 16 and len(seven_code) == len(set(seven_code)) == 59
            and all(q.bit_count() == 5 for q in seven_code)
            and all((a & b).bit_count() <= 2 for a, b in combinations(seven_code, 2)),
            'invalid seven-word sharp code')
    sharp = given['sharp_four_parts']
    require(type(sharp) is list and len(sharp) == len(set(sharp)) == 6
            and all(q in owners for q in sharp)
            and all(compatible(a, b) for a, b in combinations(sharp, 2)), 'invalid sharp parts')
    removed = 0
    for q in sharp:
        removed |= owners[q]
    removed_circles = [c for i, c in enumerate(raw) if removed & (1 << i)]
    code = sorted([c for i, c in enumerate(raw) if not removed & (1 << i)]
                  + [q | (1 << 17) for q in sharp])
    require(len(removed_circles) == 14 and len(code) == len(set(code)) == 60
            and all(q.bit_count() == 5 for q in code)
            and all((a & b).bit_count() <= 2 for a, b in combinations(code, 2)), 'invalid sharp code')
    require(tuple(sorted(sharp)) in equalities, 'sharp example missing from census')
    result = {
        'reviewer': 'six-reviewer-2', 'role': 'independent mathematical reviewer',
        'status': 'COMPLETE', 'classical_circles': 68, 'triple_count': 680,
        'noncontained_words': len(words), 'noncontained_sha256': digest(words),
        'root_transport_orbit': len(orbit), 'root_transport_sha256': digest(sorted(orbit)),
        'compatible_noncontained_pairs': compatible_pair_count,
        'root_partners': len(partners), 'root_partners_sha256': digest(partners),
        'root_partner_edges': len(edges), 'root_edges_sha256': digest(edges),
        'cartesian_products_examined': products_examined,
        'root_degree_four_frames': len(frames), 'root_frames_sha256': digest(frames),
        'frame_degree_histogram': dict(sorted(histogram.items())),
        'frame_gap_histogram': dict(sorted(gap_histogram.items())),
        'negative_last_stage_tests': negative_tests, 'union_at_most13': len(failures),
        'equality_boundary_frames': len(boundary_frames),
        'equality_boundary_tests': boundary_tests,
        'root_normalized_equality_families': len(equalities),
        'equality_degree_histogram': dict(sorted(equality_degrees.items())),
        'equality_families_sha256': digest(sorted(equalities)),
        'seven_word_extension_tests': seven_tests,
        'seven_word_union_at_most15': len(seven_failures),
        'seven_word_sharp_parts': seven_sharp,
        'seven_word_sharp_gap_cost': seven_removed.bit_count(),
        'seven_word_sharp_code_size': len(seven_code),
        'seven_word_sharp_code_sha256': digest(seven_code),
        'sharp_gap_cost': len(removed_circles), 'sharp_gaps': removed_circles,
        'sharp_code_size': len(code), 'sharp_code_sha256': digest(code),
    }
    arrays = {'noncontained': words, 'orbit': sorted(orbit), 'partners': partners,
              'edges': edges, 'frames': frames, 'equalities': sorted(equalities),
              'sharp_code': code, 'sharp_gaps': removed_circles, 'seven_sharp_code': seven_code}
    return result, arrays


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('INPUT.json'))
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--dump', type=Path)
    parser.add_argument('--max-products', type=int, default=1200000)
    parser.add_argument('--max-seconds', type=float, default=45)
    args = parser.parse_args()
    given = json.loads(args.input.read_text())
    try:
        result, arrays = run(given, args.max_products, args.max_seconds)
    except RuntimeError as error:
        print(str(error))
        return 2
    if args.expected:
        require(result == json.loads(args.expected.read_text()), 'expected result mismatch')
    if args.dump:
        args.dump.write_text(json.dumps(arrays, separators=(',', ':')) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
