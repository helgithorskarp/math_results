"""Verify the four-class splitting obstruction without a SAT solver.

Unary blocked colours are regenerated directly from integer Schur triples,
independently of the sum/difference/halving formula used for discovery.
"""
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from check import colourable, require, violations


def blocked_colours(old):
    """For each v, find colours forced off v by old vertices of that colour.

    Colour 0 denotes an unassigned vertex and supplies no premise. For a
    colour d used by a frozen old class, every premise of a d-blocking
    triple remains fixed, so its target cannot receive d.
    """
    blocked = [set() for _ in old]
    for z in range(2, len(old)):
        for x in range(1, z//2+1):
            edge = {x,z-x,z}
            for target in edge:
                colours = {old[v] for v in edge if v != target}
                if len(colours) == 1:
                    colour = next(iter(colours))
                    if colour:
                        blocked[target].add(colour)
    return blocked


def verify(fixtures, certificate):
    names = {'baseline','near537','team_near_190','team_near_359'}
    require(set(fixtures) == names, 'fixture coverage')
    require(certificate.get('format') == 1, 'unsupported certificate format')
    require(set(certificate['nonmerge']) == names, 'nonmerge fixture coverage')
    original = {}
    blocked = {}
    wanted = set()
    pair_count = 0
    for name, fixture in fixtures.items():
        text = fixture['colours']
        n = 536 if name == 'baseline' else 537
        require(type(text) is str and len(text) == n and set(text) == set('123456'),
                'wrong fixture colouring')
        require(sha256((text+'\n').encode()).hexdigest() == fixture['sha256'],
                'fixture hash mismatch')
        old = [0]+list(map(int,text))
        bad = violations(old[1:])
        require(bad == fixture['expected_violations'], 'wrong original violations')
        bad_colours = {r[3] for r in bad}
        require(not bad if name == 'baseline' else len(bad_colours) == 1,
                'unexpected defective classes')
        wanted.update((name,p) for p in combinations(range(1,7),3)
                      if bad_colours <= set(p))
        pairs = set()
        for row in certificate['nonmerge'][name]:
            pair = tuple(row['palette'])
            require(pair in set(combinations(range(1,7),2)) and pair not in pairs,
                    'invalid nonmerge pair')
            triple = row['triple']
            require(len(triple) == 3 and all(type(v) is int and 1 <= v <= n for v in triple),
                    'nonmerge triple outside old assignment')
            x,y,z = triple
            require(x <= y and x+y == z, 'nonmerge triple is not additive')
            require({old[x],old[y],old[z]} == set(pair),
                    'nonmerge triple has wrong old colours')
            pairs.add(pair)
        require(pairs == set(combinations(range(1,7),2)), 'missing nonmerge pair')
        pair_count += len(pairs)
        if name == 'baseline':
            old.append(0)
        original[name] = old
        blocked[name] = blocked_colours(old)
    rows = certificate['cases']
    keys = [(row['input'],tuple(row['palette'])) for row in rows]
    require(len(keys) == len(set(keys)) and set(keys) == wanted, 'kernel case coverage')
    result = []
    for row in rows:
        name = row['input']
        palette = set(row['palette'])
        frozen = set(range(1,7))-palette
        old = original[name]
        vertices = row['vertices']
        require(all(type(v) is int and 1 <= v <= 537 for v in vertices), 'invalid kernel vertices')
        require(all(old[v] in palette or (name == 'baseline' and v == 537)
                    for v in vertices), 'kernel outside free old classes')
        require(all(frozen <= blocked[name][v] for v in vertices),
                'kernel vertex can enter a frozen colour')
        answer,nodes,edges = colourable(vertices,3,row['root'])
        require(answer is None, 'kernel is three-colourable')
        result.append({'input':name,'palette':row['palette'],
                       'vertices':len(vertices),'edges':edges,'nodes':nodes})
    return {'status':'VERIFIED_FOUR_CLASS_SPLITTING', 'fixtures':len(fixtures),
            'nonmerge_pairs':pair_count, 'kernel_cases':len(rows),
            'blocked_domain_checks':3*sum(r['vertices'] for r in result),
            'total_nodes':sum(r['nodes'] for r in result),
            'maximum_kernel_vertices':max(r['vertices'] for r in result),
            'cases':result}


def main():
    directory = Path(__file__).resolve().parent
    fixture_bytes = (directory/'fixtures.json').read_bytes()
    certificate = json.loads((directory/'class_splitting.json').read_text())
    require(sha256(fixture_bytes).hexdigest() == certificate['fixtures_sha256'],
            'wrong fixture file')
    result = verify(json.loads(fixture_bytes),certificate)
    require(result == json.loads((directory/'splitting_expected.json').read_text()),
            'verification differs from splitting_expected.json')
    print('PASS four_class_splitting fixtures={} pairs={} kernels={} nodes={} max_vertices={}'.format(
        result['fixtures'], result['nonmerge_pairs'], result['kernel_cases'],
        result['total_nodes'], result['maximum_kernel_vertices']))
    print('class_splitting_sha256='+sha256((directory/'class_splitting.json').read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
