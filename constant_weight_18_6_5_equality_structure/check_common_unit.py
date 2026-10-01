"""Exact small certificates for two unit stars sharing their isolated hub.

Each of sixteen markings has 2592 common-tail partial maps. A leaf is an
already covered triple, a Hall obstruction on the four remaining points,
or a covered triple in their unique necessary perfect matching.

Author: six-code-1, researcher. The carrier/leaf methods extend this
author's common-mixed certificate; the marked template is credited to
six-code-3. No ambient code automorphism is used.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import resource
import time

HERE = Path(__file__).resolve().parent
TEMPLATE = (1376, 2193, 4617, 8259, 9732, 10280, 12672, 16645, 17538, 19008, 20528, 32806, 32968, 33552, 39936, 66208, 66584, 67842, 69700, 122880)
SOURCE_COMMIT = '43dc0a95a2232b6b9ff1e85d18a1a34fe5705bbc'
SOURCE_CANONICAL = ((0, 1, 2, 15), (0, 4, 12, 14), (0, 5, 9, 13), (0, 7, 10, 16), (1, 4, 11, 16), (1, 7, 13, 14), (1, 8, 9, 12), (2, 3, 10, 12), (2, 4, 7, 9), (2, 5, 8, 16), (2, 6, 11, 13), (3, 4, 5, 15), (3, 6, 9, 16), (3, 8, 11, 14), (4, 8, 10, 13), (5, 6, 10, 14), (5, 7, 11, 12), (6, 7, 8, 15), (9, 10, 11, 15), (12, 13, 15, 16))
SOURCE_POINT_MAP = (1, 2, 5, 3, 6, 7, 4, 8, 9, 10, 11, 12, 13, 14, 0, 15, 16)



class Incomplete(RuntimeError):
    pass


def require(ok, message):
    if not ok:
        raise ValueError(message)


def points(word):
    return tuple(i for i in range(18) if word >> i & 1)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def validate_template():
    require(len(TEMPLATE) == len(set(TEMPLATE)) == 20
            and all(0 <= w < 1 << 17 and w.bit_count() == 4 for w in TEMPLATE),
            'invalid shortened word list')
    covered = Counter(e for w in TEMPLATE for e in combinations(points(w), 2))
    require(len(covered) == 120 and set(covered.values()) == {1}, 'repeated shortened pair')
    reps = [sum(w >> i & 1 for w in TEMPLATE) for i in range(17)]
    require(reps == [4] * 5 + [5] * 12, 'wrong unit replication profile')
    require(set(combinations(range(5), 2)) - set(covered) == {(1, 3), (1, 4), (2, 3), (2, 4)},
            'wrong isolated-hub unit leave')
    require(sorted(SOURCE_POINT_MAP) == list(range(17)), 'invalid source relabeling')
    require(sha256(encoded(SOURCE_CANONICAL)).hexdigest()
            == 'fd7129751da4c53d9fbf4387d255d1075e9c30f118188849ed97d3567c801fcc',
            'source canonical list digest differs')
    require(tuple(sorted(sum(1 << SOURCE_POINT_MAP[x] for x in q)
                         for q in SOURCE_CANONICAL)) == TEMPLATE, 'source relabeling differs')
    return {'replications': reps, 'covered_pairs': len(covered),
            'template_sha256': sha256(encoded(TEMPLATE)).hexdigest()}


def partial_maps(a, b, node_limit=200000, seconds=10):
    """Every map of the four common tails, fixing their shared hub 0."""
    began = time.monotonic()
    target = tuple(tuple(x for x in points(w) if x != a) for w in TEMPLATE if w >> a & 1)
    source = tuple(tuple(x for x in points(w) if x != b) for w in TEMPLATE if w >> b & 1)
    require(len(source) == len(target) == 4, 'four common tails required')
    require(all(len(set().union(*map(set, tails))) == 12 for tails in (source, target)),
            'common tails not disjoint')
    ti = next(i for i, q in enumerate(target) if 0 in q)
    si = next(i for i, q in enumerate(source) if 0 in q)
    require(sum(0 in q for q in source) == sum(0 in q for q in target) == 1,
            'wrong hub occurrence in common tails')
    other = tuple(i for i in range(4) if i != si)
    domain = []
    for order in permutations(i for i in range(4) if i != ti):
        indices = dict(zip(other, order))
        indices[si] = ti
        choices = [tuple(q for q in permutations(target[indices[i]])
                         if 0 not in source[i] or q[source[i].index(0)] == 0)
                   for i in range(4)]
        require(sorted(map(len, choices)) == [2, 6, 6, 6], 'wrong tail choices')
        for images in product(*choices):
            if len(domain) >= node_limit or time.monotonic() - began > seconds:
                raise Incomplete('INCOMPLETE common-tail guard; no exclusion')
            mapping = [-1] * 17
            mapping[b] = 17
            for q, mapped in zip(source, images):
                for x, y in zip(q, mapped):
                    mapping[x] = y
            require(mapping[0] == 0 and len({x for x in mapping if x >= 0}) == 13,
                    'noninjective partial map')
            domain.append(tuple(mapping))
    require(len(domain) == len(set(domain)) == 2592, 'incomplete or repeated partial maps')
    return tuple(sorted(domain))


def problem(a, b):
    first = tuple(w | 1 << 17 for w in TEMPLATE if not (w >> a & 1))
    first_triples = {sum(1 << x for x in t) for w in first for t in combinations(points(w), 3)}
    private = tuple(w for w in TEMPLATE if not (w >> b & 1))
    source_triples = tuple(sorted({sum(1 << x for x in t)
                                   for w in private for t in combinations(points(w), 3)}))
    require(len(first_triples) == 160 and len(source_triples) == 64, 'triple count mismatch')
    targets = tuple(tuple(x for x in points(w) if x != a) for w in TEMPLATE if w >> a & 1)
    target_extra = tuple(sorted(set(range(18)) - {17, a} - set().union(*map(set, targets))))
    require(len(target_extra) == 4, 'wrong remaining target set')
    return first_triples, source_triples, target_extra


def collision(mapping, triples, forbidden):
    for t in triples:
        vertices = points(t)
        if all(mapping[x] >= 0 for x in vertices):
            image = sum(1 << mapping[x] for x in vertices)
            if image in forbidden:
                return t
    return None


def domains(mapping, triples, forbidden, target_extra):
    unknown = tuple(i for i in range(17) if mapping[i] < 0)
    require(len(unknown) == 4, 'four remaining sources required')
    allowed = []
    for x in unknown:
        options = []
        for y in target_extra:
            moved = list(mapping)
            moved[x] = y
            if collision(moved, triples, forbidden) is None:
                options.append(y)
        allowed.append(tuple(options))
    return unknown, tuple(allowed)


def leaf(mapping, triples, forbidden, target_extra):
    witness = collision(mapping, triples, forbidden)
    if witness is not None:
        return [0, witness]
    unknown, allowed = domains(mapping, triples, forbidden, target_extra)
    for size in range(1, 5):
        for ids in combinations(range(4), size):
            if len(set().union(*(set(allowed[i]) for i in ids))) < size:
                return [1, sum(1 << unknown[i] for i in ids)]
    matches = tuple(p for p in permutations(target_extra)
                    if all(p[i] in allowed[i] for i in range(4)))
    require(len(matches) == 1, 'input requires a broader completion certificate')
    moved = list(mapping)
    for x, y in zip(unknown, matches[0]):
        moved[x] = y
    witness = collision(moved, triples, forbidden)
    require(witness is not None, 'compatible relative star or incomplete proof')
    return [2, witness]


def produce():
    template = validate_template()
    certificate = {'schema': 1, 'cases': []}
    rows = []
    stream = sha256()
    for a in (1, 2, 3, 4):
        for b in (1, 2, 3, 4):
            began = time.monotonic()
            domain = partial_maps(a, b)
            forbidden, triples, extra = problem(a, b)
            proof = []
            for mapping in domain:
                if time.monotonic() - began > 10:
                    raise Incomplete('INCOMPLETE case guard; no exclusion')
                stream.update(encoded((a, b, mapping)))
                proof.append(leaf(mapping, triples, forbidden, extra))
            counts = Counter(p[0] for p in proof)
            certificate['cases'].append({'a': a, 'b': b, 'proof': proof})
            rows.append({'a': a, 'b': b, 'partial_maps': len(domain),
                         'full_bijections_represented': 24 * len(domain),
                         'direct_triple': counts[0], 'hall': counts[1],
                         'unique_matching_triple': counts[2]})
    raw = encoded(certificate)
    result = {'schema': 1, 'agent': 'six-code-1', 'role': 'researcher',
              'claim': 'No two isolated-hub unit saturated stars share that hub and join at multiplicity four.',
              'status': 'COMPLETE_EXACT_FINITE_CERTIFICATE', 'template': list(TEMPLATE),
              'template_validation': template, 'classification_source_commit': SOURCE_COMMIT,
              'classification_source_expected_sha256': '6c29da7306ce0cf874c5f60ba58ac07dd28deacd264dbd2f1a2b66c536c4b0d0',
              'classification_source_canonical': SOURCE_CANONICAL,
              'classification_source_canonical_sha256': 'fd7129751da4c53d9fbf4387d255d1075e9c30f118188849ed97d3567c801fcc',
              'classification_source_point_map': SOURCE_POINT_MAP,
              'cases': rows, 'partial_input_sha256': stream.hexdigest(),
              'certificate_bytes': len(raw), 'certificate_sha256': sha256(raw).hexdigest(),
              'independent_peer_reviewed': False, 'ordinary_bridges_formalized': False,
              'guards': {'node_limit': 200000, 'seconds_per_case': 10}}
    return json.loads(json.dumps(result)), raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='regenerate compact source evidence')
    parser.add_argument('--source-expected', type=Path,
                        help='also check the unchanged cited classification manifest')
    args = parser.parse_args()
    began = time.monotonic()
    result, raw = produce()
    if args.source_expected is not None:
        source = args.source_expected.read_bytes()
        require(sha256(source).hexdigest() == result['classification_source_expected_sha256'],
                'cited classification manifest differs')
        source = json.loads(source)
        require(source['isolated_canonical'] == result['classification_source_canonical']
                and source['canonical_sha256'] == result['classification_source_canonical_sha256']
                and source['marked_isomorphism_classes'] == 1,
                'cited classification input differs')
    cert = HERE / 'common_unit_certificate.json'
    expected = HERE / 'common_unit_expected.json'
    if args.write:
        cert.write_bytes(raw)
        expected.write_text(json.dumps(result, indent=2) + '\n')
    else:
        require(cert.read_bytes() == raw, 'certificate regeneration differs')
        require(json.loads(expected.read_text()) == result, 'expected manifest differs')
    print(json.dumps({'status': result['status'], 'cases': len(result['cases']),
                      'partial_maps': sum(r['partial_maps'] for r in result['cases']),
                      'represented_full_bijections': sum(r['full_bijections_represented'] for r in result['cases']),
                      'leaf_totals': {k: sum(r[k] for r in result['cases'])
                                      for k in ('direct_triple', 'hall', 'unique_matching_triple')},
                      'seconds': round(time.monotonic() - began, 6),
                      'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, indent=2))


if __name__ == '__main__':
    main()
