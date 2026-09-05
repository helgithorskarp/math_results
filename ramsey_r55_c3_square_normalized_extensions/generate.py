#!/usr/bin/env python3
"""Complete residual C3-square formulas with centralizer normalization."""
from pathlib import Path
from itertools import product
import importlib.util

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'ramsey_r55_c3_square_action_sweep'
PINS = {
    'model.py': 'b48a10a6e5ff285436d3d6f5d2ea874f4c87630d30e66cb5413387f5586cfacb',
    'check_formula.cpp': 'da84bab2dd928dad97c658125cbf0f2c4d1c86b752061eebe0eb76a7e3dd0aec',
    'inspect_graph.py': 'bd72c5d79400fbe66db0e0c56a13cde3d2b3efc350099c770c11bfb5c9fb5746',
}
BASE_HASHES = {
    9: '7846688b50408ebb6f9d6a9fc0a537d06186e9d732f5be9856edae6b7e88ca75',
    10: '6455b56f83001e09fd53f7fa8bdbd26270df013a32b3895569ddab3e5d18d929',
}


def load(name):
    import hashlib
    path = PARENT / (name+'.py')
    if hashlib.sha256(path.read_bytes()).hexdigest() != PINS[path.name]:
        raise ValueError('parent source changed: '+name)
    spec = importlib.util.spec_from_file_location('square_parent_'+name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load('model')
require, info = BASE.require, BASE.info


def case(index):
    require(index in (9, 10), 'not a residual action')
    return BASE.cases()[index]


def forbidden(variables, word):
    require(len(set(variables)) == len(variables), 'word repeats a primary variable')
    return tuple(sorted(-v if b else v for v, b in zip(variables, word, strict=True)))


def layer(index):
    ids = BASE.edge_orbits(case(index))
    edge = lambda u, v: ids[min(u, v), max(u, v)]
    regular = [list(range(s, s+9)) for s in (7, 16, 25, 34)]
    # Four unoriented F3^2 directions: (0,1), (1,0), (1,1), (1,2).
    profiles = [[edge(0, r[0])] + [edge(r[0], r[d]) for d in (1, 3, 4, 5)]
                for r in regular]
    order = set()
    words = list(product((0, 1), repeat=5))
    for a, b in zip(profiles, profiles[1:]):
        for x in words:
            for y in words:
                if x > y:
                    order.add(forbidden(a+b, x+y))
    phase = set()
    for r in regular[1:]:
        variables = [edge(7, v) for v in r]
        for word in product((0, 1), repeat=9):
            images = [tuple(word[3*((u+x) % 3)+(v+y) % 3]
                            for u, v in product(range(3), repeat=2))
                      for x, y in product(range(3), repeat=2)]
            if min(images) < word:
                phase.add(forbidden(variables, word))
    for r in (list(range(1, 4)), list(range(4, 7))):
        variables = [edge(7, v) for v in r]
        for word in product((0, 1), repeat=3):
            if min(word[s:]+word[:s] for s in range(3)) < word:
                phase.add(forbidden(variables, word))
    require(len(order) == 3*496 and len(phase) == 3*448+2*4, 'layer counts')
    require(not order.intersection(phase), 'layer overlap')
    return sorted(order | phase, key=lambda q: (len(q), q))


def generate(index, directory):
    directory.mkdir(parents=True, exist_ok=True)
    parent = directory / f'parent_{index:02}.cnf'
    full = directory / f'case_{index:02}.cnf'
    report = BASE.generate(case(index), parent)
    require(report['sha256'] == BASE_HASHES[index], 'parent formula changed')
    extra = layer(index)
    with parent.open() as src, full.open('w') as out:
        src.readline()
        out.write(f"p cnf {report['variables']} {report['clauses']+len(extra)}\n")
        for line in src:
            out.write(line)
        for clause in extra:
            out.write(' '.join(map(str, clause))+' 0\n')
    return dict(info(full), variables=report['variables'], clauses=report['clauses']+len(extra),
                parent=report, normalization_clauses=len(extra))


if __name__ == '__main__':
    import argparse
    import json
    p = argparse.ArgumentParser()
    p.add_argument('--case', type=int, choices=(9, 10), required=True)
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    require(not a.work.resolve().is_relative_to(ROOT.parent), 'generated data outside Git')
    print(json.dumps(generate(a.case, a.work), sort_keys=True))
