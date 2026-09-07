#!/usr/bin/env python3
"""Independent small exhaustive coverage controls and corrupt-witness rejection."""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import native
import verify as audit


def require(test, message):
    if not test:
        raise RuntimeError(message)


def run(inputs):
    arithmetic = 0
    for i, d in enumerate(audit.RADICALS):
        for j, e in enumerate(audit.RADICALS):
            a = tuple(int(k == i) for k in range(8))
            b = tuple(int(k == j) for k in range(8))
            expected = {r: v for r, v in zip(audit.RADICALS, native.mul(a, b)) if v}
            require(audit.times({d: 1}, {e: 1}) == expected, 'field product')
            arithmetic += 1
    fixtures = [
        '{0,0}', '{1,0}', '{-1/2,Sqrt[3]/2}',
        '{Sqrt[11/3],-(1/Sqrt[3])}',
        '{(Sqrt[55]-Sqrt[15])/16,(Sqrt[5]+Sqrt[165])/48}',
        '{-Sqrt[5/3],(1-Sqrt[33])/12}',
    ]
    for row in fixtures:
        require(native.parse(row) == audit.read_points(row), 'parser fixture')
    coverage_cases = 0
    for k in range(4):
        all_masks = list(range(1 << k))
        for selector in range(1 << len(all_masks)):
            masks = [m for m in all_masks if selector >> m & 1]
            brute_covered = [any(m & ~c == 0 for c in masks) for m in all_masks]
            for weights in itertools.product((1, 2), repeat=k):
                orders = [sum(w for i, w in enumerate(weights) if m >> i & 1) for m in all_masks]
                for limit in range(sum(weights) + 1):
                    good = [m for m in all_masks if orders[m] <= limit]
                    complete = all(brute_covered[m] for m in good)
                    try:
                        report = audit.complete_family(weights, masks, limit)
                    except ValueError as error:
                        require(not complete and str(error).startswith('uncovered assignment'), 'false rejection')
                    else:
                        require(complete, 'false coverage acceptance')
                        expected_maximal = sum(not any(m != other and m & ~other == 0 for other in good) for m in good)
                        require(report['admissible'] == len(good), 'admissible count')
                        require(report['exact_target'] == sum(orders[m] == limit for m in good), 'exact count')
                        require(report['maximal_admissible'] == expected_maximal, 'maximal count')
                        require(report['downward_coverage_sha256'] == hashlib.sha256(bytes(brute_covered)).hexdigest(), 'coverage array')
                    coverage_cases += 1
    graph = native.build(inputs)
    points, atoms, edges, keys = audit.geometry(inputs)
    require(points == graph['points'], 'independent point reconstruction')
    require(edges == graph['edges'], 'independent complete edge census')
    require(atoms == [a['vertices'] for a in graph['atoms']], 'independent partition')
    cert = json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())
    mutations = []
    def add(name, function):
        c = copy.deepcopy(cert)
        function(c)
        mutations.append((name, c))
    add('wrong version', lambda c: c.update(version='bad'))
    add('wrong target', lambda c: c.update(target=507))
    add('boolean target', lambda c: c.update(target=True))
    add('negative mask', lambda c: c['covers'][0].update(mask=-1))
    add('oversize mask', lambda c: c['covers'][0].update(mask=2**len(atoms)))
    add('boolean mask', lambda c: c['covers'][0].update(mask=True))
    add('short word', lambda c: c['covers'][0].update(word=c['covers'][0]['word'][:-1]))
    add('invalid colour', lambda c: c['covers'][0].update(word='9'+c['covers'][0]['word'][1:]))
    add('empty covers', lambda c: c.update(covers=[]))
    add('duplicate cover', lambda c: c['covers'].append(copy.deepcopy(c['covers'][0])))
    def uncolour(c):
        word = list(c['covers'][0]['word'])
        i = next(i for i, w in enumerate(word) if w != '-')
        word[i] = '-'
        c['covers'][0]['word'] = ''.join(word)
    add('missing selected colour', uncolour)
    def colour_absent(c):
        word = list(c['covers'][0]['word'])
        i = word.index('-')
        word[i] = '0'
        c['covers'][0]['word'] = ''.join(word)
    add('colour on absent vertex', colour_absent)
    def make_mono(c):
        word = list(c['covers'][0]['word'])
        u, v = next((u, v) for u, v in edges if word[u] != '-' and word[v] != '-')
        word[v] = word[u]
        c['covers'][0]['word'] = ''.join(word)
    add('monochromatic edge', make_mono)
    rejected = []
    for name, c in mutations:
        try:
            audit.colour_checks(atoms, edges, c)
        except ValueError:
            rejected.append(name)
        else:
            raise RuntimeError('accepted corruption: '+name)
    # The final discovered word covers a maximal member missed by every prior
    # word. Removing it tests the full-family condition, not just syntax.
    partial = copy.deepcopy(cert)
    partial['covers'].pop()
    masks, _ = audit.colour_checks(atoms, edges, partial)
    try:
        audit.complete_family(list(map(len, atoms)), masks, 508)
    except ValueError as error:
        require(str(error).startswith('uncovered assignment'), 'wrong coverage failure')
        rejected.append('missing essential cover')
    else:
        raise RuntimeError('accepted incomplete family')
    return dict(all_checks_passed=True, field_basis_products=arithmetic,
                parser_fixtures=len(fixtures), exhaustive_weighted_coverage_cases=coverage_cases,
                independent_geometry_equal=True, malformed_inputs_rejected=len(rejected), rejections=rejected)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--inputs', type=Path, required=True)
    args = ap.parse_args()
    print(json.dumps(run(args.inputs), indent=2, sort_keys=True))
