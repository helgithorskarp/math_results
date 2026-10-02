"""Reconstruct actual literal interfaces and all residual words from definitions.

No producer, domain helper, previous census or solver is imported.
Carrier completeness is established separately by the full point-DFS replay.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

BRIDGE_PIN = '802b7938a70812de37eed2ab37a830858350718923177d0eb3009d4856c7ae50'
FIXTURE_PIN = 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'

def need(test, message):
    if not test:
        raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def role_and_domain(row, fixtures):
    x = 17
    fi, mark = row['first']
    si, source_mark = row['second']
    need(type(fi) is int and type(si) is int and 0 <= fi < 23 and 0 <= si < 23, 'invalid fixture index')
    need(type(mark) is list and len(mark) == 3, 'invalid first mark')
    u, v, y = mark
    need(all(type(p) is int and 0 <= p < 17 for p in mark) and len({x, y, u, v}) == 4,
         'invalid distinguished first points')
    need(type(source_mark) is list and len(source_mark) == 3 and len(set(source_mark)) == 3, 'invalid second mark')
    su, sv, sx = source_mark
    need(all(type(p) is int and 0 <= p < 17 for p in source_mark), 'invalid distinguished source points')
    phi = row['point_map']
    need(type(phi) is list and len(phi) == 17 and all(type(p) is int for p in phi)
         and set(phi) == set(range(18))-{y}, 'relative point map is not a bijection')
    need((phi[su], phi[sv], phi[sx]) == (u, v, x), 'distinguished images differ')
    first_blocks = [frozenset(q) for q in fixtures['stars'][fi]]
    second_blocks = [frozenset(q) for q in fixtures['stars'][si]]
    need(all(len(q) == 4 and q <= set(range(17)) for q in first_blocks+second_blocks), 'invalid literal quadruple')
    source_pairs = {frozenset(t) for q in second_blocks for t in itertools.combinations(q, 2)}
    missing_u = set(range(17))-{su}-{p for p in range(17) if frozenset((p, su)) in source_pairs}
    need(len(missing_u) == 4 and sx not in missing_u, 'deficient second u leave/covered x-u differs')
    words = set(q | {x} for q in first_blocks) | set(frozenset(phi[p] for p in q) | {y} for q in second_blocks)
    need(len(words) == 36 and all(len(q) == 5 for q in words), 'wrong distinct36-word union')
    need(all(len(a & b) <= 2 for a, b in itertools.combinations(words, 2)), 'literal union collision')
    ordered_masks = sorted(sum(1 << p for p in q) for q in words)
    need(type(row['word_masks']) is list and all(type(m) is int for m in row['word_masks'])
         and row['word_masks'] == ordered_masks, 'stored words differ from actual point-map images')
    replication = {p: sum(p in q for q in words) for p in range(18)}
    need(replication[x] == replication[y] == 20, 'centers are not complete degree20 stars')
    lam = lambda p, q: sum({p, q} <= word for word in words)
    covered = lambda p, q, t: any({p, q, t} <= word for word in words)
    need(lam(x, y) == 4 and lam(x, v) == 5 and not covered(x, y, v), 'common pair/low-v condition fails')
    need(lam(x, u) < 5, 'first u must be deficient')
    high = {p for p in range(18) if p != x and lam(x, p) < 5}
    need(all(covered(x, u, p) for p in high-{u}), 'u not isolated in deficient x-star leave')
    need(lam(y, u) == 4 and all(lam(y, p) in (4, 5) for p in range(18) if p != y),
         'unit second-row condition fails')
    source_uv = sum({su, sv} <= q for q in second_blocks)
    need(source_uv in (0, 1) and lam(u, v) == 1 + source_uv,
         'actual source u-v coverage differs from observed union multiplicity')
    owned = [tuple(t) for q in words for t in itertools.combinations(sorted(q), 3)]
    need(len(owned) == len(set(owned)) == 360, 'triple ownership differs')
    used = set(owned)
    candidates = [frozenset(q) for q in itertools.combinations(sorted(set(range(18))-{x, y}), 5)
                  if all(t not in used for t in itertools.combinations(q, 3))]
    masks = [sum(1 << p for p in q) for q in candidates]
    triangles = [p for p in range(18) if p not in (x, y, u, v) and lam(x, p) == lam(y, p) == 4
                 and not covered(x, y, p)]
    need(row['triangle_points'] == triangles, 'diagnostic triangle readout differs')
    deficits = sorted((5-lam(x, p) for p in high), reverse=True)
    need(deficits in ([2, 1, 1, 1], [1, 1, 1, 1, 1]), 'isolated deficient first-row pattern differs')
    return candidates, masks, dict(lambda_xu=lam(x, u), lambda_yv=lam(y, v), observed_uv=lam(u, v),
        first_deficit_pattern=''.join(str(d) for d in deficits), triangle_count=len(triangles))

def check(bridge, certificate, fixtures):
    need(len(fixtures['stars']) == 23, 'wrong fixture population')
    rows = bridge['raw_positive_maps']
    need(type(rows) is list and len(rows) == 3, 'wrong full positive population')
    keys = [(r['product_index'], tuple(r['point_map'])) for r in rows]
    need(len(set(keys)) == 3, 'duplicate positive point map')
    entries = certificate['entries']
    need(type(entries) is list and len(entries) == 3, 'wrong certificate population')
    need(all(type(e['index']) is int for e in entries) and {e['index'] for e in entries} == set(range(3)),
         'certificate index gap or duplicate')
    by_index = {e['index']: e for e in entries}
    records, universes = [], []
    for index, row in enumerate(rows):
        entry = by_index[index]
        candidates, masks, role = role_and_domain(row, fixtures)
        need(entry['product_index'] == row['product_index'] and entry['first_fixture'] == row['first'][0],
             'product/fixture attribution differs')
        need(entry['candidate_count'] == len(candidates) and entry['candidate_sha256'] == digest(masks),
             'actual residual domain differs')
        need(entry['triangle_count'] == role['triangle_count'], 'diagnostic triangle statistic differs')
        colors, capacity = entry['colors'], entry['capacity']
        need(type(capacity) is int and 1 <= capacity <= len(candidates), 'invalid color capacity')
        need(type(colors) is list and len(colors) == len(candidates), 'invalid color population')
        need(all(type(c) is int and 0 <= c < capacity for c in colors) and set(colors) == set(range(capacity)),
             'invalid or unused color class')
        edges = 0
        for i, j in itertools.combinations(range(len(candidates)), 2):
            if len(candidates[i] & candidates[j]) <= 2:
                need(colors[i] != colors[j], 'compatible candidates share a color')
                edges += 1
        need(entry['edges'] == edges and entry['upper_bound'] == 36+capacity, 'edge or bound record differs')
        records.append(dict(index=index, product_index=row['product_index'], candidate_count=len(candidates),
                            candidate_sha256=digest(masks), edges=edges, capacity=capacity,
                            upper_bound=36+capacity, **role))
        universes.append(masks)
    maximum = max(r['upper_bound'] for r in records)
    need(maximum <= 62, 'uniform upper62 certificate fails')
    need(all(r['lambda_xu'] == 4 and r['lambda_yv'] == 5 and r['observed_uv'] == 2 and
             r['first_deficit_pattern'] == '11111' for r in records),
         'literal structural conclusions of complete three-core census differ')
    subscopes = {}
    for field in ('lambda_xu', 'lambda_yv', 'observed_uv', 'first_deficit_pattern'):
        subscopes[field] = {str(d): dict(interfaces=sum(r[field] == d for r in records),
            maximum_upper_bound=max(r['upper_bound'] for r in records if r[field] == d))
            for d in sorted({r[field] for r in records})}
    return dict(status='PASS_ALL3_UNIT_SECOND_U_FOUR_LITERAL_COLOR_CERTIFICATES', interfaces=3,
                universe_per_interface=4368, total_residual_candidates=sum(r['candidate_count'] for r in records),
                total_compatible_edges=sum(r['edges'] for r in records), maximum_upper_bound=maximum,
                color_range=[min(r['capacity'] for r in records), max(r['capacity'] for r in records)],
                upper_bound_census={str(k): sum(r['upper_bound'] == k for r in records)
                                   for k in sorted({r['upper_bound'] for r in records})},
                subscopes=subscopes, records=records,
                candidate_domains_sha256=digest(universes), records_sha256=digest(records))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bridge', required=True)
    parser.add_argument('--certificate', required=True)
    parser.add_argument('--fixtures', required=True)
    args = parser.parse_args()
    raw = Path(args.bridge).read_bytes()
    fixture_raw = Path(args.fixtures).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == BRIDGE_PIN, 'frozen bridge pin differs')
    need(hashlib.sha256(fixture_raw).hexdigest() == FIXTURE_PIN, 'credited fixture pin differs')
    result = check(json.loads(raw), json.loads(Path(args.certificate).read_text()), json.loads(fixture_raw))
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
