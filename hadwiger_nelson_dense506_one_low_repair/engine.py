"""Exact eligible host-host-candidate circle census for one outside point."""
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / 'hadwiger_nelson_dense506_completion_closure/construct.py'
if sha256(SOURCE.read_bytes()).hexdigest() != 'f734b6e6bcf00eb7cb4084140588b1257b8d12589a2e1f9d93e5c2ae131bf5bd':
    raise ValueError('source input-loader pin')
spec = importlib.util.spec_from_file_location('prior_loader', SOURCE)
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
G = S.pinned_import('prior_geometry', S.PRIOR / 'geometry.py', S.GEOMETRY_PIN)
digest = G.digest


def obstructed(mask, a, b, xc, xd, cd):
    """Requires a,b nonempty and not equal singletons on a cd edge."""
    return bool(xc and xd and not (a & ~mask) and not (b & ~mask)
                and (cd or (a != b and a.bit_count() == b.bit_count() == 1)))


def colour_triple(mask, a, b, cd):
    return next(((x, y, z) for x in range(4) for y in range(4) for z in range(4)
                 if (mask >> x) & 1 and (a >> y) & 1 and (b >> z) & 1
                 and x != y and x != z and (not cd or y != z)), None)


class Census:
    def __init__(self, candidate_work):
        self.data, self.colors = S.load(candidate_work)
        self.P = G.host()
        for h in self.data['points']:
            S.require(G.D % h[0] == 0, 'candidate denominator')
            self.P.append((G.scale(h[1:5], G.D // h[0]), G.scale(h[5:], G.D // h[0])))
        hedges = G.distances(self.P[:506])[2]
        S.check_colors(self.colors, [15] * 506, hedges)
        masks = self.data['available_masks']
        rebuilt = [sum(1 << c for c in range(4) if all(self.colors[v] != c for v in nn))
                   for nn in self.data['neighbors']]
        S.require(rebuilt == masks and all(masks), 'host lists')
        S.require(all(not (masks[i] == masks[j] and masks[i].bit_count() == 1)
                      for i, j in self.data['candidate_edges']), 'candidate singleton edge')
        edges = hedges + [(v, 506 + i) for i, nn in enumerate(self.data['neighbors']) for v in nn]
        edges += [(506 + i, 506 + j) for i, j in self.data['candidate_edges']]
        S.require(len(edges) == 12074, 'known graph edges')
        self.adj = [0] * len(self.P)
        for i, j in edges:
            self.adj[i] |= 1 << j
            self.adj[j] |= 1 << i
        self.actual = {G.canonical(x, y, G.D) for x, y in self.P}
        S.require(len(self.actual) == 1926, 'known graph vertices')

    def screen(self, limit=506):
        p, z, r = 10007, 283, 6718
        S.require(z * z % p == 33 and r * r % p == (-408 + 72 * z) % p, 'modular roots')
        invD = pow(G.D, -1, p)
        mp = [(G.embedding(p, z, r, x) * invD % p, G.embedding(p, z, r, y) * invD % p)
              for x, y in self.P]
        ds = [[((x - X) ** 2 + 3 * (y - Y) ** 2) % p for X, Y in mp] for x, y in mp[:limit]]
        eligible = {m: [506 + i for i, a in enumerate(self.data['available_masks']) if a & ~m == 0]
                    for m in range(1, 16) if m.bit_count() == 2}
        rows = []
        known = total = pairs = 0
        for i in range(limit):
            for j in range(i + 1, limit):
                if self.colors[i] == self.colors[j]:
                    continue
                pairs += 1
                mask = 15 ^ ((1 << self.colors[i]) | (1 << self.colors[j]))
                choices = eligible[mask]
                total += len(choices)
                a = ds[i][j]
                aa = a * a
                common = self.adj[i] & self.adj[j]
                di, dj = ds[i], ds[j]
                for k in choices:
                    if common & self.adj[k]:
                        known += 1
                        continue
                    b, c = di[k], dj[k]
                    if (a * b * c - 2 * (a * b + a * c + b * c) + aa + b * b + c * c) % p == 0:
                        rows.append((i, j, k - 506))
        return rows, {'prime': p, 'z': z, 'r': r, 'host_limit': limit,
                      'differently_coloured_host_pairs': pairs, 'eligible_triples': total,
                      'known_U_centres': known, 'modular_survivors': len(rows),
                      'survivor_sha256': digest(rows)}

    def exact(self, rows):
        P = self.P
        @lru_cache(None)
        def distance(i, j):
            return G.norm(G.sub(P[i][0], P[j][0]), G.sub(P[i][1], P[j][1]))
        centres = defaultdict(list)
        positive = []
        for i, j, ci in rows:
            k = 506 + ci
            a, b, c = distance(i, j), distance(i, k), distance(j, k)
            heron = G.sub(G.scale(G.add(G.add(G.mul(a, b), G.mul(a, c)), G.mul(b, c)), 2),
                          G.add(G.add(G.mul(a, a), G.mul(b, b)), G.mul(c, c)))
            if G.mul(G.mul(a, b), c) != G.scale(heron, G.D ** 2):
                continue
            dx, dy = G.sub(P[j][0], P[i][0]), G.sub(P[j][1], P[i][1])
            ex, ey = G.sub(P[k][0], P[i][0]), G.sub(P[k][1], P[i][1])
            det = G.sub(G.mul(dx, ey), G.mul(ex, dy))
            S.require(det != G.ZERO, 'collinear unit-circle triple')
            v = G.inv(G.scale(det, 6))
            xx = G.mul(G.scale(G.sub(G.mul(a, ey), G.mul(b, dy)), 3), v)
            yy = G.mul(G.sub(G.mul(dx, b), G.mul(ex, a)), v)
            h = G.canonical(G.add(P[i][0], xx), G.add(P[i][1], yy), G.D)
            S.require(h not in self.actual, 'known-centre removal failed')
            centres[h].append((i, j, ci))
            positive.append((i, j, ci))
        return centres, positive

    def check_pairs(self, centres, positive):
        points = sorted(centres)
        pairs, cn = [], []
        tested = 0
        stream = sha256()
        cedges = {tuple(e) for e in self.data['candidate_edges']}
        masks = self.data['available_masks']
        for ix, h in enumerate(points):
            triples = centres[h]
            hp = {t[:2] for t in triples}
            S.require(len(hp) == 1, 'more than two host neighbours')
            pair = next(iter(hp))
            pairs.append(pair)
            cs = sorted(t[2] for t in triples)
            S.require(len(cs) == len(set(cs)), 'duplicate incidence')
            cn.append(cs)
            mask = 15 ^ ((1 << self.colors[pair[0]]) | (1 << self.colors[pair[1]]))
            for a, b in combinations(cs, 2):
                tested += 1
                cd = (a, b) in cedges
                S.require(not obstructed(mask, masks[a], masks[b], True, True, cd), 'list obstruction')
                witness = colour_triple(mask, masks[a], masks[b], cd)
                S.require(witness is not None, 'missing direct colouring')
                stream.update(json.dumps([ix, a, b, *witness], separators=(',', ':')).encode() + b'\n')
        table = {'points': points, 'host_pairs': pairs, 'eligible_candidate_neighbors': cn,
                 'positive_triples': positive, 'obstructions': []}
        result = {'positive_triples': len(positive), 'positive_triple_sha256': digest(positive),
                  'external_centres': len(points), 'point_sha256': digest(points),
                  'host_pair_sha256': digest(pairs), 'eligible_candidate_neighbor_sha256': digest(cn),
                  'eligible_candidate_neighbor_histogram': dict(sorted(Counter(map(len, cn)).items())),
                  'centres_at_least_two_eligible': sum(len(x) >= 2 for x in cn),
                  'candidate_pairs_tested': tested, 'pair_colouring_stream_sha256': stream.hexdigest(),
                  'fixed_host_list_obstructions': 0}
        return table, result
