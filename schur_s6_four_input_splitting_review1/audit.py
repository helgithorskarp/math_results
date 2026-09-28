"""Independent exact audit of the four-input splitting certificate."""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'schur_s6_three_colour_trades'
SOLVER = HERE.parent / 'schur_s6_core_family_review1' / 'kernel_solver.cpp'
NAMES = ('baseline', 'near537', 'team_near_190', 'team_near_359')


def triples(n):
    for z in range(2, n + 1):
        for x in range(1, z // 2 + 1):
            yield x, z - x, z


def forbidden_vertices(class_set, endpoint=537):
    sums = {a + b for a in class_set for b in class_set}
    differences = {a - b for a in class_set for b in class_set if a > b}
    halves = {a // 2 for a in class_set if a % 2 == 0}
    return (sums | differences | halves) & set(range(1, endpoint + 1))


def main():
    fixture_file = SOURCE / 'fixtures.json'
    certificate_file = SOURCE / 'class_splitting.json'
    fixtures = json.loads(fixture_file.read_text())
    certificate = json.loads(certificate_file.read_text())
    assert sha256(fixture_file.read_bytes()).hexdigest() == 'be1de027a09a08e6d78785a6af6ee126f7bc3f49bfa59f6061359566406d1a5a'
    assert sha256(certificate_file.read_bytes()).hexdigest() == '027b1c25df0ed2c21cbf25f653a8abb6e13bbc8dc2e0dfb868bc6da7a4812a81'
    assert sha256(fixture_file.read_bytes()).hexdigest() == certificate['fixtures_sha256']
    assert set(fixtures) == set(NAMES)

    words, classes, bad_colours = {}, {}, {}
    total_pairs = 0
    for name in NAMES:
        entry = fixtures[name]
        word = entry['colours']
        n = 536 if name == 'baseline' else 537
        assert len(word) == n and set(word) == set('123456')
        assert sha256((word + '\n').encode()).hexdigest() == entry['sha256']
        colours = [0] + [int(c) for c in word]
        violations = [[x, y, z, colours[z]] for x, y, z in triples(n)
                      if colours[x] == colours[y] == colours[z]]
        assert violations == entry['expected_violations']
        assert len(violations) == (0 if name == 'baseline' else (2 if name == 'near537' else 1))
        words[name] = colours
        classes[name] = {i: {v for v in range(1, n + 1) if colours[v] == i}
                         for i in range(1, 7)}
        bad_colours[name] = {row[3] for row in violations}
        assert len(bad_colours[name]) == (0 if name == 'baseline' else 1)

        # Search the complete word for mixed-class pair witnesses, then
        # separately validate the printed witnesses.
        found = set()
        for x, y, z in triples(n):
            old_labels = {colours[x], colours[y], colours[z]}
            if len(old_labels) == 2:
                found.add(tuple(sorted(old_labels)))
        assert found == set(combinations(range(1, 7), 2))
        printed = certificate['nonmerge'][name]
        assert len(printed) == 15
        seen = set()
        for row in printed:
            pair = tuple(row['palette'])
            x, y, z = row['triple']
            assert pair in found and pair not in seen
            assert 1 <= x <= y < z <= n and x + y == z
            assert {colours[x], colours[y], colours[z]} == set(pair)
            seen.add(pair)
        total_pairs += len(seen)

    all_triples = list(triples(537))
    assert len(all_triples) == 72092
    cases = certificate['cases']
    expected_keys = {(name, palette) for name in NAMES
                     for palette in combinations(range(1, 7), 3)
                     if bad_colours[name] <= set(palette)}
    actual_keys = [(row['input'], tuple(row['palette'])) for row in cases]
    assert len(cases) == 50 and len(set(actual_keys)) == 50
    assert set(actual_keys) == expected_keys

    forbidden = {name: {i: forbidden_vertices(classes[name][i])
                        for i in range(1, 7)} for name in NAMES}
    text = [str(len(cases))]
    incidence = 0
    sizes = defaultdict(list)
    for row in cases:
        name = row['input']
        palette = set(row['palette'])
        frozen = set(range(1, 7)) - palette
        assert not bad_colours[name] & frozen
        for i in frozen:
            B = classes[name][i]
            assert all(not {x, y, z} <= B for x, y, z in all_triples)
        allowed = set.union(*(classes[name][i] for i in palette))
        if name == 'baseline':
            allowed.add(537)
        W = row['vertices']
        assert W and W == sorted(set(W)) and row['root'] in W
        assert set(W) <= allowed
        assert all(set(W) <= forbidden[name][i] for i in frozen)
        incidence += 3 * len(W)
        sizes[name].append(len(W))
        index = {v: j for j, v in enumerate(W)}
        edges = sorted({tuple(sorted({index[x], index[y], index[z]}))
                        for x, y, z in all_triples
                        if x in index and y in index and z in index})
        text.append(f'{len(W)} {len(edges)} {index[row["root"]]}')
        text.extend(str(len(edge)) + ' ' + ' '.join(map(str, edge)) for edge in edges)
    assert incidence == 7047
    assert {name: (len(sizes[name]), min(sizes[name]), max(sizes[name])) for name in NAMES} == {
        'baseline': (20, 33, 80), 'near537': (10, 14, 48),
        'team_near_190': (10, 21, 74), 'team_near_359': (10, 25, 96)}

    with tempfile.TemporaryDirectory() as temp:
        binary = Path(temp) / 'solver'
        subprocess.run(['g++', '-O2', '-std=c++17', '-Wall', '-Wextra',
                        str(SOLVER), '-o', str(binary)], check=True)
        output = subprocess.run([str(binary)], input='\n'.join(text) + '\n',
                                text=True, capture_output=True, check=True)
    results = [line.split() for line in output.stdout.splitlines()]
    assert len(results) == 50
    assert all(int(row[0]) == i and row[1] == 'UNSAT'
               for i, row in enumerate(results))
    nodes = defaultdict(int)
    for row, result in zip(cases, results):
        nodes[row['input']] += int(result[2])
    print('PASS fixtures=4 pairs={} kernels={} blocked_incidences={}'.format(
        total_pairs, len(cases), incidence))
    print('violations=' + ','.join(f'{name}:{len(fixtures[name]["expected_violations"])}'
                                for name in NAMES))
    print('independent_solver_nodes=' + str(sum(nodes.values())))
    print('nodes_by_input=' + ','.join(f'{name}:{nodes[name]}' for name in NAMES))


if __name__ == '__main__':
    main()
