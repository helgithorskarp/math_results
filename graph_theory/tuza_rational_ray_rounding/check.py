"""Exact certificate checker. Python standard library; independent of solvers.

Literal pair checks, rational primal/dual inequalities and packet degree
identities are the trust boundary. Finite tests do not prove Keevash's theorem.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import json
import sys

from packet import compile_packet, latin_lift, label_substitute


class InvalidCertificate(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def unpack(profile, optimal=True):
    d = profile['d']
    require(isinstance(d, int) and d >= 1, 'invalid type count')
    edges = [tuple(e) for e in profile['edges']]
    require(all(len(e) == 2 and 0 <= e[0] < e[1] < d for e in edges), 'invalid cross edge')
    require(len(edges) == len(set(edges)), 'duplicate cross edge')
    loops = profile['loops']
    require(len(set(loops)) == len(loops) and all(0 <= i < d for i in loops), 'invalid clique types')
    edges = sorted(edges + [(i, i) for i in loops])
    cap = {e: Q(1, 2) if e[0] == e[1] else Q(1) for e in edges}
    triangles = [t for t in combinations_with_replacement(range(d), 3)
                 if all(e in cap for e in combinations(t, 2))]
    primal = {}
    for row in profile['primal']:
        t, w = tuple(row['types']), Q(row['weight'])
        require(t in triangles and t not in primal and w > 0, 'invalid primal term')
        primal[t] = w
    loads = {e: Q(0) for e in edges}
    for t, w in primal.items():
        for e in combinations(t, 2):
            loads[e] += w
    require(all(loads[e] <= cap[e] for e in edges), 'primal capacity exceeded')
    value = sum(primal.values(), Q(0))
    if optimal:
        dual = {e: Q(0) for e in edges}
        seen = set()
        for row in profile['dual']:
            e, w = tuple(row['types']), Q(row['weight'])
            require(e in dual and e not in seen and w > 0, 'invalid dual term')
            seen.add(e)
            dual[e] = w
        require(all(sum(dual[e] for e in combinations(t, 2)) >= 1 for t in triangles),
                'dual triangle inequality failed')
        require(value == sum(cap[e] * dual[e] for e in edges) == Q(profile['optimum']),
                'primal/dual value mismatch')
    return edges, cap, triangles, primal, value


def check_packet(profile, packet):
    edges, cap, _, primal, _ = unpack(profile, optimal=False)
    D, types, parts = packet['denominator'], packet['types'], packet['components']
    require(isinstance(D, int) and D > 0, 'invalid denominator')
    require(all(0 <= i < profile['d'] for i in types), 'invalid packet type')
    used_vertices, used_edges = set(), set()
    edge_counts, triangle_counts, single_counts = Counter(), Counter(), Counter()
    degree_sum = [Counter() for _ in range(profile['d'])]
    for component in parts:
        require(len(component) in (2, 3), 'invalid component size')
        require(len(set(component)) == len(component), 'repeated packet vertex')
        require(all(0 <= v < len(types) and v not in used_vertices for v in component),
                'components must be vertex disjoint')
        used_vertices.update(component)
        roles = tuple(sorted(types[v] for v in component))
        (triangle_counts if len(component) == 3 else single_counts)[roles] += 1
        for u, v in combinations(component, 2):
            pair = tuple(sorted((u, v)))
            kind = tuple(sorted((types[u], types[v])))
            require(kind in cap and pair not in used_edges, 'invalid packet edge')
            used_edges.add(pair)
            edge_counts[kind] += 1
            degree_sum[types[u]][kind] += 1
            degree_sum[types[v]][kind] += 1
    require(used_vertices == set(range(len(types))), 'unused packet vertices')
    require(all(edge_counts[e] == D * cap[e] for e in edges), 'packet edge counts failed')
    require(dict(triangle_counts) == {t: D * w for t, w in primal.items()},
            'packet triangle counts failed')
    for i in range(profile['d']):
        require(all(degree_sum[i][e] == (D if i in e else 0) for e in edges),
                'type degree-vector identity failed')
    for t in (D + 1, 2 * D + 1, 5 * D + 1):
        require(t * (t - 1) % D == 0 and (t - 1) % D == 0, 'nonintegral multiplier')
        require(all((t * (t - 1) // D) * edge_counts[e] == t * (t - 1) * cap[e]
                    for e in edges), 'zero-level divisibility failed')
        for i in range(profile['d']):
            require(all(((t - 1) // D) * degree_sum[i][e] == (t - 1 if i in e else 0)
                        for e in edges), 'one-level divisibility failed')
    return {'D': D, 'vertices': len(types), 'edges': len(used_edges),
            'triangles': sum(triangle_counts.values()), 'spare_edges': sum(single_counts.values())}


def graph_edges(profile, t, diagonal_deleted):
    _, cap, _, _, _ = unpack(profile, optimal=False)
    return {e for e in combinations(range(profile['d'] * t), 2)
            if (e[0] // t, e[1] // t) in cap
            and (not diagonal_deleted or e[0] % t != e[1] % t)}


def check_fractional_host(profile, t):
    _, cap, _, primal, value = unpack(profile)
    edges = graph_edges(profile, t, True)
    actual = [tr for tr in combinations(range(profile['d'] * t), 3)
              if all(e in edges for e in combinations(tr, 2))]
    counts = Counter(tuple(v // t for v in tr) for tr in actual)
    require(all(counts[tr] > 0 for tr in primal), 'missing lifted type')
    loads, total = Counter(), Q(0)
    for triangle in actual:
        roles = tuple(v // t for v in triangle)
        weight = Q(t * (t - 1)) * primal.get(roles, 0) / counts[roles]
        total += weight
        for edge in combinations(triangle, 2):
            loads[edge] += weight
    require(total == t * (t - 1) * value, 'fractional value failed')
    for edge in edges:
        kind = (edge[0] // t, edge[1] // t)
        expected = sum(sum(pair == kind for pair in combinations(tr, 2)) * w
                       for tr, w in primal.items()) / cap[kind]
        require(loads[edge] == expected and loads[edge] <= 1, 'literal fractional edge load failed')
    return {'t': t, 'edges': len(edges), 'triangles': len(actual), 'value': str(total)}


def check_typicality(profile, t=7, max_inputs=2):
    _, cap, _, _, _ = unpack(profile, optimal=False)
    vertices = list(range(profile['d'] * t))
    edges = graph_edges(profile, t, True)
    neighborhoods = {v: set() for v in vertices}
    for a, b in edges:
        neighborhoods[a].add(b)
        neighborhoods[b].add(a)
    checked = 0
    for a in range(max_inputs + 1):
        for inputs in combinations(vertices, a):
            for j in range(profile['d']):
                intersection = set(range(j * t, (j + 1) * t))
                for v in inputs:
                    intersection.intersection_update(neighborhoods[v])
                supported = all(tuple(sorted((v // t, j))) in cap for v in inputs)
                z = sum(v // t != j for v in inputs)
                target = t * Q(t - 1, t) ** z if supported else Q(0)
                exact = t - len({v % t for v in inputs}) if supported else 0
                require(len(intersection) == exact, 'common-neighbor formula failed')
                require(abs(len(intersection) - target) <= Q(2 * a, t) * target,
                        'typicality estimate failed')
                checked += 1
    return checked


def check_packing(profile, scale, packing):
    allowed = {tuple(e) for e in profile['edges']}
    require(not profile['loops'], 'independent lift requires loopless template')
    used = set()
    for triangle in packing:
        require(len(triangle) == 3 and len(set(triangle)) == 3, 'invalid triangle vertices')
        require(all(isinstance(v, int) and 0 <= v < profile['d'] * scale for v in triangle),
                'triangle vertex out of range')
        for a, b in combinations(triangle, 2):
            e = tuple(sorted((a, b)))
            parent = tuple(sorted((a // scale, b // scale)))
            require(parent in allowed, 'packing contains nonedge')
            require(e not in used, 'packing repeats edge')
            used.add(e)
    _, _, _, _, optimum = unpack(profile)
    require(len(packing) == scale * scale * optimum, 'packing does not attain dual bound')
    return len(used)


def expect_rejection(label, operation):
    try:
        operation()
    except (InvalidCertificate, ValueError):
        return label
    raise RuntimeError('negative control was accepted: ' + label)


def check_diagonal_decomposition(profile, order, packing):
    edges = graph_edges(profile, order, True)
    used = set()
    for triangle in packing:
        require(len(triangle) == 3 and len(set(triangle)) == 3, 'invalid diagonal triangle')
        for pair in combinations(triangle, 2):
            edge = tuple(sorted(pair))
            require(edge in edges and edge not in used, 'invalid diagonal packing edge')
            used.add(edge)
    require(used == edges, 'diagonal decomposition misses edges')
    return {'order': order, 'vertices': profile['d'] * order,
            'edges': len(edges), 'triangles': len(packing)}


def audit(certificate):
    require(certificate['format'] == 1, 'unsupported format')
    summaries = []
    for p in certificate['profiles']:
        edges, _, triangles, _, value = unpack(p)
        summaries.append({'name': p['name'], 'edge_types': len(edges),
                          'triangle_types': len(triangles), 'P': str(value),
                          'packet': check_packet(p, compile_packet(p)),
                          'fractional_hosts': [check_fractional_host(p, t) for t in (3, 4, 7)],
                          'typicality_checks': check_typicality(p)})
    template_count = 0
    for d in (1, 2, 3):
        possibilities = list(combinations_with_replacement(range(d), 2))
        for mask in range(1 << len(possibilities)):
            supported = [e for k, e in enumerate(possibilities) if (mask >> k) & 1]
            triangles = [tr for tr in combinations_with_replacement(range(d), 3)
                         if all(e in supported for e in combinations(tr, 2))]
            incidence = Counter(e for tr in triangles for e in combinations(tr, 2))
            weight = min((Q(1, 2) if a == b else Q(1)) / incidence[(a, b)]
                         for a, b in incidence) if incidence else Q(0)
            p = {'d': d, 'loops': [a for a, b in supported if a == b],
                 'edges': [list(e) for e in supported if e[0] != e[1]],
                 'primal': [{'types': list(tr), 'weight': str(weight)} for tr in triangles]}
            check_packet(p, compile_packet(p))
            template_count += 1
    lift = certificate['independent_lift']
    seed = next(p for p in certificate['profiles'] if p['name'] == lift['profile'])
    scale, packing = lift['scale'], lift['packing']
    check_packing(seed, scale, packing)
    lifts = []
    for u in (1, 2, 3, 5, 8, 15):
        lifted = latin_lift(packing, u)
        edges_used = check_packing(seed, scale * u, lifted)
        lifts.append({'factor': u, 'scale': scale * u, 'triangles': len(lifted), 'edges_used': edges_used})
    diagonal = certificate['diagonal_decomposition']
    cube = next(p for p in certificate['profiles'] if p['name'] == diagonal['profile'])
    require(diagonal['scale'] == 3, 'expected order-three certificate')
    check_diagonal_decomposition(cube, 3, diagonal['packing'])
    substitutions = []
    for order in (3, 7, 9, 15, 31):
        if order == 9:
            blocks = [tr for tr in combinations(range(9), 3)
                      if all(sum((v // (3 ** k)) % 3 for v in tr) % 3 == 0 for k in (0, 1))]
        else:
            blocks = [tr for tr in combinations(range(order), 3)
                      if (tr[0] + 1) ^ (tr[1] + 1) ^ (tr[2] + 1) == 0]
        pairs = [e for tr in blocks for e in combinations(tr, 2)]
        require(len(pairs) == len(set(pairs)) and set(pairs) == set(combinations(range(order), 2)),
                'label blocks are not a Steiner triple system')
        lifted = label_substitute(diagonal['packing'], 3, order, blocks)
        substitutions.append(check_diagonal_decomposition(cube, order, lifted))
    bad_primal = deepcopy(seed)
    bad_primal['primal'][0]['weight'] = '3'
    bad_dual = deepcopy(seed)
    bad_dual['dual'] = []
    bad_packet = compile_packet(seed)
    bad_packet['components'].pop()
    bad_lift = [[a * 2 + i, b * 2 + j, c * 2 + i]
                for a, b, c in packing for i in range(2) for j in range(2)]
    negative = [expect_rejection('overloaded primal', lambda: unpack(bad_primal)),
                expect_rejection('deficient dual', lambda: unpack(bad_dual)),
                expect_rejection('missing spare-edge component', lambda: check_packet(seed, bad_packet)),
                expect_rejection('repeated packing edge', lambda: check_packing(seed, scale, packing + [packing[0]])),
                expect_rejection('packing nonedge', lambda: check_packing(seed, scale, [[8, 10, 12]])),
                expect_rejection('broken Latin rule', lambda: check_packing(seed, scale * 2, bad_lift)),
                expect_rejection('missing diagonal triangle', lambda: check_diagonal_decomposition(cube, 3, diagonal['packing'][:-1]))]
    return {'status': 'PASS', 'profiles': summaries, 'small_templates': template_count,
            'independent_lifts': lifts, 'label_substitutions': substitutions, 'negative_controls': negative,
            'scope': 'Exact finite certificate audit; universal existence imports Keevash Theorems 3.2 and 3.3.'}


if __name__ == '__main__':
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('CERTIFICATES.json')
    print(json.dumps(audit(json.loads(path.read_text())), indent=2, sort_keys=True))
