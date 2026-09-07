#!/usr/bin/env python3
"""Affine-basis reference census, exhaustive tiny fixtures, and corrupt words."""
import copy
import itertools
import json
from collections import Counter
from pathlib import Path
import geometry as producer
import verify as audit


def require(test, message):
    if not test:
        raise RuntimeError(message)


def affine_hyperplanes(dimension):
    """Reference: affine spans of every possible affine basis, no normal vectors."""
    ambient = list(itertools.product(range(3), repeat=dimension))
    labels = {v: i for i, v in enumerate(ambient)}
    hyperplanes = set()
    for basis in itertools.combinations(ambient, dimension):
        origin = basis[0]
        directions = [tuple((x-y) % 3 for x, y in zip(v, origin)) for v in basis[1:]]
        span = {tuple((origin[i]+sum(t*d[i] for t, d in zip(coefficients, directions))) % 3
                      for i in range(dimension))
                for coefficients in itertools.product(range(3), repeat=dimension-1)}
        if len(span) == 3**(dimension-1):
            hyperplanes.add(sum(1 << labels[v] for v in span))
    return ambient, sorted(hyperplanes)


def run():
    basis_products = 0
    for i, d in enumerate(audit.RAD):
        for j, e in enumerate(audit.RAD):
            basis = tuple(int(k == i) for k in range(16))
            expected = {r: v for r, v in zip(audit.RAD, producer.rootmul(basis, j)) if v}
            require(audit.mul({d: 1}, {e: 1}) == expected, 'basis multiplication')
            basis_products += 1
    hyperplane_counts = []
    for dimension in (1, 2, 3):
        ambient, expected = affine_hyperplanes(dimension)
        records, _ = audit.family_census(ambient, len(ambient), dimension)
        require(sorted(mask for a, b, mask in records) == expected, 'affine basis versus normal-vector census')
        hyperplane_counts.append(len(expected))
    ambient, lines = affine_hyperplanes(2)
    fixtures = 0
    for subset in range(1 << len(ambient)):
        vertices = [v for v in range(len(ambient)) if subset >> v & 1]
        values = [ambient[v] for v in vertices]
        expected = [sum(1 << i for i, v in enumerate(vertices) if line >> v & 1) for line in lines]
        if values:
            generated, _ = producer.section_family(values, len(values))
            require(Counter({mask: len(eq) for mask, eq in generated.items()}) == Counter(expected), 'producer small intersections')
        for limit in range(len(vertices)+1):
            records, admitted = audit.family_census(values, limit, 2)
            require(Counter(m for a, b, m in records) == Counter(expected), 'fixture multiplicity')
            require(Counter(m for a, b, m in admitted) == Counter(m for m in expected if m.bit_count() <= limit), 'fixture cardinality')
            fixtures += 1
    points = audit.reconstruct()
    edges, _ = audit.edge_census(points)
    ppoints, _ = producer.construction()
    pedges, _ = producer.exact_edges(ppoints)
    require(points == ppoints and edges == pedges, 'independent complete geometry')
    columns, divisors, values = audit.projection(points)
    pcolumns, pdivisors, pvalues = producer.residues(ppoints)
    require((columns, divisors, values) == (pcolumns, pdivisors, pvalues), 'primitive residue projection')
    records, admitted = audit.family_census(values, 508)
    family, _ = producer.section_family(values)
    require(Counter({mask: len(eq) for mask, eq in family.items()}) == Counter(m for a, b, m in admitted), 'independent complete candidate family')
    certificate = json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())
    changes = []
    def change(name, function):
        c = copy.deepcopy(certificate)
        function(c)
        changes.append((name, c))
    change('version', lambda c: c.update(version='bad'))
    change('target', lambda c: c.update(target=507))
    change('boolean target', lambda c: c.update(target=True))
    change('deleted label range', lambda c: c.update(deleted=len(points)))
    change('boolean deleted label', lambda c: c.update(deleted=True))
    change('wrong endpoint', lambda c: c.update(deleted=0))
    change('short base word', lambda c: c.update(base_word=c['base_word'][:-1]))
    change('missing base colour', lambda c: c.update(base_word='-'+c['base_word'][1:]))
    change('colour on omitted endpoint', lambda c: c.update(base_word=c['base_word'][:-1]+'0'))
    def base_mono(c):
        w = list(c['base_word'])
        u, v = next((u, v) for u, v in edges if u != c['deleted'] and v != c['deleted'])
        w[v] = w[u]
        c['base_word'] = ''.join(w)
    change('base monochromatic edge', base_mono)
    change('zero normal', lambda c: c['exceptions'][0].update(normal='00000000'))
    change('unnormalized normal', lambda c: c['exceptions'][0].update(normal=''.join(str(2*int(x)%3) for x in c['exceptions'][0]['normal'])))
    change('normal digit', lambda c: c['exceptions'][0].update(normal='3'+c['exceptions'][0]['normal'][1:]))
    change('short exception word', lambda c: c['exceptions'][0].update(word=c['exceptions'][0]['word'][:-1]))
    change('exception colour', lambda c: c['exceptions'][0].update(word='4'+c['exceptions'][0]['word'][1:]))
    change('missing exception', lambda c: c['exceptions'].pop())
    # Distinct equations can cut the same finite support; duplicates must be
    # rejected by support, not merely by equation text.
    by_mask = {}
    for normal, b, mask in admitted:
        if b == 0:
            by_mask.setdefault(mask, []).append(''.join(map(str, normal)))
    alternatives = next(names for names in by_mask.values() if len(names) > 1)
    existing = next(e for e in certificate['exceptions'] if e['normal'] in alternatives)
    duplicate = copy.deepcopy(existing)
    duplicate['normal'] = next(name for name in alternatives if name != existing['normal'])
    change('duplicate support via another equation', lambda c: c['exceptions'].append(duplicate))
    rejected = []
    for name, c in changes:
        try:
            audit.check_certificate(points, edges, values, admitted, c)
        except ValueError:
            rejected.append(name)
        else:
            raise RuntimeError('accepted invalid certificate: '+name)
    old = audit.ROOTS[3]
    audit.ROOTS[3] = old+1
    try:
        try:
            audit.edge_census(points[:2])
        except ValueError:
            rejected.append('invalid modular square root')
        else:
            raise RuntimeError('invalid sieve root accepted')
    finally:
        audit.ROOTS[3] = old
    return dict(all_checks_passed=True, basis_products=basis_products,
                reference_affine_hyperplane_counts=hyperplane_counts,
                exhaustive_small_subset_threshold_cases=fixtures,
                full_geometry_and_family_equal=True,
                malformed_inputs_rejected=len(rejected), rejections=rejected)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
