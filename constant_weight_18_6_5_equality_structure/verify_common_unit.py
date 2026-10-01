"""Separate point-by-point carrier and literal-set common-unit leaf checker.

Author: six-code-1, researcher. Extends this author's common-mixed checker;
this is a separate implementation, not an independent peer review.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import argparse
import importlib.util
import json
import resource
import time

HERE = Path(__file__).resolve().parent


class Incomplete(RuntimeError):
    pass


def require(ok, message):
    if not ok:
        raise ValueError(message)


def vertices(mask):
    require(type(mask) is int and 0 <= mask < 1 << 18, 'invalid point mask')
    return frozenset(i for i in range(18) if mask & (1 << i))


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def template(words):
    blocks = tuple(vertices(w) for w in words)
    require(len(blocks) == len(set(blocks)) == 20 and all(len(q) == 4 and 17 not in q for q in blocks),
            'invalid template blocks')
    require(all(len(q & r) <= 1 for q, r in combinations(blocks, 2)), 'template repeats a pair')
    require([sum(i in q for q in blocks) for i in range(17)] == [4] * 5 + [5] * 12,
            'template profile differs')
    covered = {frozenset(e) for q in blocks for e in combinations(q, 2)}
    require({frozenset(e) for e in combinations(range(5), 2)} - covered
            == {frozenset((1, 3)), frozenset((1, 4)), frozenset((2, 3)), frozenset((2, 4))},
            'template marked hub is not isolated in its high core')
    return blocks


def provenance(expected):
    original = expected['classification_source_canonical']
    require(sha256(encoded(original)).hexdigest()
            == expected['classification_source_canonical_sha256']
            == 'fd7129751da4c53d9fbf4387d255d1075e9c30f118188849ed97d3567c801fcc',
            'classification representative hash differs')
    mapping = expected['classification_source_point_map']
    require(sorted(mapping) == list(range(17)) and mapping[14] == 0,
            'classification relabeling is not a marked bijection')
    moved = sorted(sum(1 << mapping[x] for x in q) for q in original)
    require(moved == expected['template'], 'classification relabeling differs')
    require(expected['classification_source_commit']
            == '43dc0a95a2232b6b9ff1e85d18a1a34fe5705bbc'
            and expected['classification_source_expected_sha256']
            == '6c29da7306ce0cf874c5f60ba58ac07dd28deacd264dbd2f1a2b66c536c4b0d0',
            'classification provenance differs')


def structure(cert):
    labels = [(a, b) for a in (1, 2, 3, 4) for b in (1, 2, 3, 4)]
    require(type(cert) is dict and cert.get('schema') == 1
            and type(cert.get('cases')) is list,
            'invalid certificate structure')
    require([(r['a'], r['b']) for r in cert['cases']] == labels,
            'certificate cases missing, repeated or out of order')
    require(all(type(r['proof']) is list and len(r['proof']) == 2592
                for r in cert['cases']), 'certificate leaf coverage differs')


def point_maps(blocks, a, b, node_limit=200000, seconds=10):
    """Assign points individually; target block choice arises at its first point."""
    source = tuple(sorted((q - {b} for q in blocks if b in q), key=lambda q: tuple(sorted(q))))
    target = tuple(sorted((q - {a} for q in blocks if a in q), key=lambda q: tuple(sorted(q))))
    require(len(source) == len(target) == 4 and all(len(q) == 3 for q in source + target),
            'wrong common-tail domain')
    require(all(len(set().union(*parts)) == 12 for parts in (source, target)), 'tails not disjoint')
    source_hub = next(i for i, q in enumerate(source) if 0 in q)
    target_hub = next(i for i, q in enumerate(target) if 0 in q)
    order = sorted(source[source_hub] - {0})
    for i, q in enumerate(source):
        if i != source_hub:
            order.extend(sorted(q))
    owner = {x: i for i, q in enumerate(source) for x in q}
    current = {0: 0, b: 17}
    block_map = {source_hub: target_hub}
    used_blocks = {target_hub}
    used_points = {0, 17}
    found = []
    began = time.monotonic()
    nodes = 0

    def visit(depth):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit or time.monotonic() - began > seconds:
            raise Incomplete('INCOMPLETE literal point-map guard; no exclusion')
        if depth == len(order):
            found.append(tuple(current.get(i, -1) for i in range(17)))
            return
        x = order[depth]
        i = owner[x]
        choices = (block_map[i],) if i in block_map else tuple(j for j in range(4) if j not in used_blocks)
        for j in choices:
            fresh = i not in block_map
            if fresh:
                block_map[i] = j
                used_blocks.add(j)
            for y in sorted(target[j] - used_points):
                current[x] = y
                used_points.add(y)
                visit(depth + 1)
                used_points.remove(y)
                del current[x]
            if fresh:
                used_blocks.remove(j)
                del block_map[i]

    visit(0)
    require(len(found) == len(set(found)) == 2592, 'point-map carrier incomplete or repeated')
    require(all(p[0] == 0 and p[b] == 17 and sum(y >= 0 for y in p) == 13
                and len({y for y in p if y >= 0}) == 13 for p in found), 'invalid generated point map')
    return tuple(sorted(found)), nodes


def literal_problem(blocks, a, b):
    first = tuple(q | {17} for q in blocks if a not in q)
    second = tuple(q for q in blocks if b not in q)
    common_targets = set().union(*(q - {a} for q in blocks if a in q))
    extra = frozenset(range(18)) - common_targets - {17, a}
    require(len(extra) == 4, 'wrong unmatched target points')
    return first, second, extra


def allowed_images(mapping, first, second, extra):
    unknown = tuple(i for i in range(17) if mapping[i] < 0)
    require(len(unknown) == 4, 'wrong unmatched sources')
    current = {i: y for i, y in enumerate(mapping) if y >= 0}
    domains = []
    for x in unknown:
        permitted = set()
        for y in extra:
            current[x] = y
            collision = False
            for q in second:
                known = {current[z] for z in q if z in current}
                if any(len(known & f) >= 3 for f in first):
                    collision = True
                    break
            del current[x]
            if not collision:
                permitted.add(y)
        domains.append(frozenset(permitted))
    return unknown, tuple(domains)


def check_collision(mask, mapping, first, second):
    witness = vertices(mask)
    require(len(witness) == 3 and any(witness <= q for q in second), 'invalid source collision triple')
    require(all(x < 17 and mapping[x] >= 0 for x in witness), 'collision uses an unmapped point')
    image = {mapping[x] for x in witness}
    require(len(image) == 3 and any(image <= f for f in first), 'claimed covered triple is absent')


def check_leaf(proof, mapping, first, second, extra):
    require(type(proof) is list and len(proof) == 2 and all(type(x) is int for x in proof),
            'malformed leaf')
    kind, witness = proof
    if kind == 0:
        check_collision(witness, mapping, first, second)
        return
    require(kind in (1, 2), 'unknown leaf kind')
    unknown, domains = allowed_images(mapping, first, second, extra)
    if kind == 1:
        subset = vertices(witness)
        require(subset and subset <= set(unknown), 'invalid Hall subset')
        images = set().union(*(domains[unknown.index(x)] for x in subset))
        require(len(images) < len(subset), 'Hall inequality does not fail')
    else:
        matches = tuple(p for p in permutations(sorted(extra))
                        if all(p[i] in domains[i] for i in range(4)))
        require(len(matches) == 1, 'completion matching is not unique')
        moved = list(mapping)
        for x, y in zip(unknown, matches[0]):
            moved[x] = y
        require(len(set(moved)) == 17 and -1 not in moved, 'invalid sole matching')
        check_collision(witness, moved, first, second)


def packing_fixture(words):
    blocks = tuple(vertices(w) for w in words)
    require(len(blocks) == len(set(blocks)) == 35 and all(len(q) == 5 for q in blocks),
            'bad positive fixture size/distinctness/weight')
    require(all(len(q & r) <= 2 for q, r in combinations(blocks, 2)), 'bad positive fixture intersection')
    require(all(sum(x in q for q in blocks) == 20 for x in (0, 17))
            and sum({0, 17} <= q for q in blocks) == 5
            and sum(16 in q for q in blocks) == 3, 'positive fixture centers or marker differ')
    return blocks


def controls(first_map, first_case, blocks, fixture, cert):
    first, second, extra = literal_problem(blocks, first_case['a'], first_case['b'])
    rejected = 0
    for bad in ([0, 0], [1, 0], [2, 0], [3, 1], [0], ['0', 1]):
        try:
            check_leaf(bad, first_map, first, second, extra)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('corrupted or malformed leaf accepted')
    packing_fixture(fixture)
    bad = list(fixture)
    bad[1] = bad[0]
    try:
        packing_fixture(bad)
    except ValueError:
        rejected += 1
    else:
        raise ValueError('corrupted positive fixture accepted')
    try:
        point_maps(blocks, 1, 1, node_limit=0)
    except Incomplete:
        pass
    else:
        raise ValueError('zero guard did not report incomplete')
    # Hall cannot reject an unrestricted bijection, and a sole matching
    # is a positive assignment until an actual covered triple is exhibited.
    current = [-1] * 17
    current[4:] = list(range(4, 17))
    try:
        check_leaf([1, 15], current, (), (), frozenset(range(4)))
    except ValueError:
        rejected += 1
    else:
        raise ValueError('false Hall exclusion of a positive bijection accepted')
    # The necessary domains have the sole completion 0->0,...,3->3.
    # It is compatible, so uniqueness alone must never prove exclusion.
    first = tuple(frozenset((y, 4+2*x, 5+2*x, 13, 14))
                  for x in range(4) for y in range(4) if y != x)
    second = tuple(frozenset((x, 4+2*x, 5+2*x, 12)) for x in range(4))
    unknown, permitted = allowed_images(current, first, second, frozenset(range(4)))
    require(unknown == (0, 1, 2, 3)
            and permitted == tuple(frozenset((x,)) for x in range(4)),
            'positive unique-matching fixture differs')
    try:
        check_leaf([2, (1 << 0) | (1 << 4) | (1 << 5)], current,
                   first, second, frozenset(range(4)))
    except ValueError:
        rejected += 1
    else:
        raise ValueError('compatible unique matching falsely excluded')
    # Tampering with the finite carrier must be visible independently of hashes.
    for mode in ('missing-case', 'repeated-case', 'missing-leaf'):
        bad = json.loads(json.dumps(cert))
        if mode == 'missing-case':
            bad['cases'].pop()
        elif mode == 'repeated-case':
            bad['cases'][-1] = bad['cases'][0]
        else:
            bad['cases'][0]['proof'].pop()
        try:
            structure(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('damaged carrier coverage accepted')
    return {'invalid_controls_rejected': rejected, 'positive_joint_words': 35,
            'compatible_unique_matching_control': True,
            'coverage_damage_controls': 3, 'zero_guard_incomplete': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare-primary', action='store_true')
    args = parser.parse_args()
    began = time.monotonic()
    expected = json.loads((HERE / 'common_unit_expected.json').read_text())
    raw = (HERE / 'common_unit_certificate.json').read_bytes()
    require(len(raw) == expected['certificate_bytes'] and sha256(raw).hexdigest() == expected['certificate_sha256'],
            'certificate bytes differ')
    cert = json.loads(raw)
    provenance(expected)
    blocks = template(expected['template'])
    structure(cert)
    primary = None
    if args.compare_primary:
        spec = importlib.util.spec_from_file_location('common_unit_primary', HERE / 'check_common_unit.py')
        primary = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(primary)
        require(tuple(expected['template']) == primary.TEMPLATE, 'input fixtures differ')
    rows = []
    stream = sha256()
    total_nodes = 0
    saved = None
    for case in cert['cases']:
        a, b = case['a'], case['b']
        started = time.monotonic()
        domain, nodes = point_maps(blocks, a, b)
        total_nodes += nodes
        if primary is not None:
            require(domain == primary.partial_maps(a, b), 'entrywise point-map carrier mismatch')
        require(type(case['proof']) is list and len(case['proof']) == len(domain), 'proof leaves missing or repeated')
        first, second, extra = literal_problem(blocks, a, b)
        counts = Counter()
        for mapping, proof in zip(domain, case['proof']):
            if time.monotonic() - started > 10:
                raise Incomplete('INCOMPLETE literal case guard; no exclusion')
            stream.update(encoded((a, b, mapping)))
            check_leaf(proof, mapping, first, second, extra)
            counts[proof[0]] += 1
        rows.append({'a': a, 'b': b, 'partial_maps': len(domain),
                     'full_bijections_represented': 24 * len(domain),
                     'direct_triple': counts[0], 'hall': counts[1],
                     'unique_matching_triple': counts[2]})
        if saved is None:
            saved = domain[0], case
    require(rows == expected['cases'] and stream.hexdigest() == expected['partial_input_sha256'],
            'reconstructed coverage or manifest differs')
    positive = json.loads((HERE / 'common_mixed_positive.json').read_text())['word_masks']
    tested = controls(*saved, blocks, positive, cert)
    result = {'agent': 'six-code-1', 'role': 'researcher',
              'status': 'COMPLETE_SEPARATE_CARRIER_AND_LITERAL_REPLAY',
              'cases': len(rows), 'partial_maps': sum(r['partial_maps'] for r in rows),
              'point_dfs_nodes': total_nodes, 'entrywise_primary_comparison': args.compare_primary,
              'controls': tested, 'seconds': round(time.monotonic() - began, 6),
              'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
