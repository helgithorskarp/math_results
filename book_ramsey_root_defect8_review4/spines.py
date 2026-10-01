"""Literal 22-point spine domains and synchronous reciprocal-edge pruning."""
from functools import reduce
from itertools import combinations
from incidence import SUPPORTS, DELTA, need


def local_domain(spec, words, vertex, bounds=None, point_cap=False):
    """Compute pages from literal red/blue stars, with optional defect bounds."""
    root_neighbors = [sum(1 << i for i in row) | sum(1 << (6+v) for v, w in enumerate(words) if j in SUPPORTS[w])
                      for j, row in enumerate(spec['roots'])]
    root_blue = [((1 << 22)-1) ^ mask ^ (1 << j) for j, mask in enumerate(root_neighbors)]
    own_roots = words[vertex]
    degree = 9-own_roots.bit_count()
    neighbors = [v for v in range(16) if v != vertex]
    found = []
    for chosen in combinations(neighbors, degree):
        mask = sum(1 << v for v in chosen)
        red_star = own_roots | (mask << 6)
        blue_star = ((1 << 22)-1) ^ red_star ^ (1 << (6+vertex))
        defects = []
        for j in range(6):
            if own_roots >> j & 1:
                defect = 3-(red_star & root_neighbors[j]).bit_count()
            else:
                defect = 6-(blue_star & root_blue[j]).bit_count()
            if defect < 0 or (j in spec['saturated'] and defect != 0):
                break
            if bounds is not None and defect > bounds[j]:
                break
            defects.append(defect)
        else:
            if point_cap and sum(defects) > 1+2*DELTA[own_roots]:
                continue
            found.append((mask, tuple(defects[j] for j in spec['active'])))
    return found


def all_domains(spec, counts, mode='relaxed'):
    words = [w for w, n in enumerate(counts) for _ in range(n)]
    need(len(words) == 16, 'incidence size')
    bounds = None
    if mode != 'relaxed':
        bounds = [0]*6
        for j in spec['active']:
            bounds[j] = spec['f'][j]-(spec['w'] if len(spec['active']) == 2 else 0)
    by_word = {w: local_domain(spec, words, words.index(w), bounds, mode == 'point_cap') for w in sorted(set(words))}
    domains = []
    labeled = []
    for i, w in enumerate(words):
        rep = words.index(w)
        decoded = []
        for mask, defects in by_word[w]:
            if i != rep and bool(mask >> i & 1) != bool(mask >> rep & 1):
                mask ^= (1 << i) | (1 << rep)
            need(not (mask >> i & 1), 'local star excludes its own vertex')
            decoded.append((mask, defects))
        decoded.sort()
        labeled.append(decoded)
        domains.append([mask for mask, _ in decoded])
    return words, domains, labeled


def reciprocal(domains):
    """Batch rounds; each deletion follows an actual forced or forbidden edge."""
    domains = [list(row) for row in domains]
    n = len(domains)
    rounds = []
    while all(domains):
        forced = [reduce(int.__and__, row) for row in domains]
        possible = [reduce(int.__or__, row) for row in domains]
        next_domains = []
        for i, row in enumerate(domains):
            required = sum(1 << j for j in range(n) if forced[j] >> i & 1)
            forbidden = sum(1 << j for j in range(n) if not (possible[j] >> i & 1))
            next_domains.append([mask for mask in row if mask & required == required and not (mask & forbidden)])
        rounds.append({'before': list(map(len, domains)), 'after': list(map(len, next_domains))})
        if next_domains == domains:
            return {'excluded': False, 'rounds': rounds, 'surviving_domains': domains}
        domains = next_domains
    return {'excluded': True, 'rounds': rounds, 'empty_vertices': [i for i, row in enumerate(domains) if not row]}
