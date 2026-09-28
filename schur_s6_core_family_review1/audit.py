"""Independent arithmetic and C++ hypergraph audit of the fixed-core claim."""
import hashlib
import json
from itertools import combinations
from itertools import product
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'schur_s6_three_colour_trades'


def triples(n):
    for z in range(2, n + 1):
        for x in range(1, z // 2 + 1):
            yield x, z - x, z


def main():
    cert_path = SOURCE / 'core_family.json'
    cert = json.loads(cert_path.read_text())
    kernels = json.loads((SOURCE / 'class_splitting.json').read_text())
    fixtures = json.loads((SOURCE / 'fixtures.json').read_text())
    assert hashlib.sha256(cert_path.read_bytes()).hexdigest() == '6933d5d6c4aad46152fbd671a38ac73daf5bba5e7f61edd1d0d7446225ed128a'
    assert hashlib.sha256((SOURCE / 'class_splitting.json').read_bytes()).hexdigest() == cert['kernel_certificate_sha256']
    assert hashlib.sha256((SOURCE / 'fixtures.json').read_bytes()).hexdigest() == cert['fixtures_sha256']

    base = fixtures['baseline']['colours']
    assert len(base) == 536 and set(base) == set('123456')
    assert hashlib.sha256((base + '\n').encode()).hexdigest() == fixtures['baseline']['sha256']
    old = [0] + [int(c) for c in base]
    T536 = list(triples(536))
    T537 = list(triples(537))
    assert len(T536) == 71824
    assert all(len({old[x], old[y], old[z]}) > 1 for x, y, z in T536)

    cores = {int(label): set(values) for label, values in cert['cores'].items()}
    assert set(cores) == set(range(1, 7))
    assert [len(cores[i]) for i in range(1, 7)] == [34, 38, 35, 39, 37, 42]
    assert all(len(cores[i]) == len(cert['cores'][str(i)]) for i in cores)
    assert all(cores[i] <= set(range(1, 537)) for i in cores)
    assert len(set.union(*cores.values())) == 225
    assert all(all(not {x, y, z} <= cores[i] for x, y, z in T536) for i in cores)
    assert all(all(old[v] == i for v in cores[i]) for i in cores)

    # Rebuild the pair witnesses without using the 15 printed triples.
    pair_witnesses = set()
    for x, y, z in T536:
        for i, j in combinations(range(1, 7), 2):
            if {x, y, z} <= cores[i] | cores[j] and ({x, y, z} & cores[i]) and ({x, y, z} & cores[j]):
                pair_witnesses.add((i, j))
    assert len(pair_witnesses) == 15
    assert len(cert['nonmerge']) == 15
    for row in cert['nonmerge']:
        x, y, z = row['triple']
        i, j = row['palette']
        assert x <= y and x + y == z and (i, j) in pair_witnesses
        assert {x, y, z} <= cores[i] | cores[j]
        assert ({x, y, z} & cores[i]) and ({x, y, z} & cores[j])

    # D_i is rebuilt from the three defining arithmetic operations.
    forbidden = {}
    for i, B in cores.items():
        sums = {a + b for a in B for b in B}
        differences = {a - b for a in B for b in B if a > b}
        halves = {b // 2 for b in B if b % 2 == 0}
        forbidden[i] = (sums | differences | halves) & set(range(1, 538))
    rows = [row for row in kernels['cases'] if row['input'] == 'baseline']
    assert len(rows) == 20
    assert {tuple(row['palette']) for row in rows} == set(combinations(range(1, 7), 3))
    inputs = [str(len(rows))]
    incidence = 0
    max_size = 0
    for row in rows:
        W = row['vertices']
        assert W == sorted(set(W)) and W and 1 <= W[0] and W[-1] <= 537
        frozen = set(range(1, 7)) - set(row['palette'])
        assert set(W) <= set.intersection(*(forbidden[i] for i in frozen))
        incidence += len(W) * 3
        max_size = max(max_size, len(W))
        index = {v: j for j, v in enumerate(W)}
        edges = sorted({tuple(sorted({index[x], index[y], index[z]}))
                        for x, y, z in T537 if x in index and y in index and z in index})
        inputs.append(f'{len(W)} {len(edges)} {index[row["root"]]}')
        inputs.extend(str(len(edge)) + ' ' + ' '.join(map(str, edge)) for edge in edges)
    assert incidence == 3189 and max_size == 80

    # A Cartesian product family is valid iff every Schur triple has empty
    # intersection of its independently offered colour domains.
    choices = [{old[v]} for v in range(537)]
    switched = set()
    for row in cert['product_switches']:
        v, a, b = row['vertex'], row['old'], row['alternative']
        assert 1 <= v <= 536 and v not in switched and v not in set.union(*cores.values())
        assert a == old[v] and b in range(1, 7) and b != a
        switched.add(v)
        choices[v].add(b)
    assert len(switched) == 53
    assert all(not (choices[x] & choices[y] & choices[z]) for x, y, z in T536)

    with tempfile.TemporaryDirectory() as tmp:
        executable = Path(tmp) / 'kernel_solver'
        subprocess.run(['g++', '-O2', '-std=c++17', '-Wall', '-Wextra',
                        str(HERE / 'kernel_solver.cpp'), '-o', str(executable)], check=True)
        run = subprocess.run([str(executable)], input='\n'.join(inputs) + '\n',
                             text=True, capture_output=True, check=True)
        # Compare the solver with literal exhaustive assignments on every
        # four-vertex hypergraph with edges of sizes two and three.
        small_edges = list(combinations(range(4), 2)) + list(combinations(range(4), 3))
        checks = [str(1 << len(small_edges))]
        expected = []
        for mask in range(1 << len(small_edges)):
            selected = [edge for j, edge in enumerate(small_edges) if mask & (1 << j)]
            checks.append(f'4 {len(selected)} 0')
            checks.extend(str(len(edge)) + ' ' + ' '.join(map(str, edge)) for edge in selected)
            expected.append(any(all(len({assignment[v] for v in edge}) > 1 for edge in selected)
                                for assignment in product(range(3), repeat=4)))
        small = subprocess.run([str(executable)], input='\n'.join(checks) + '\n',
                               text=True, capture_output=True, check=True)
        actual = [line.split()[1] == 'SAT' for line in small.stdout.splitlines()]
        assert actual == expected
    results = [line.split() for line in run.stdout.splitlines()]
    assert len(results) == 20 and all(int(row[0]) == j and row[1] == 'UNSAT'
                                     for j, row in enumerate(results))
    print('PASS cores=225 pairs=15 kernels=20 blocked_incidences=3189 '
          'product_dimension=53 product_triples=71824 toy_hypergraphs=1024')
    print('independent_solver_nodes=' + str(sum(int(row[2]) for row in results)))
    print('per_kernel_nodes=' + ','.join(row[2] for row in results))


if __name__ == '__main__':
    main()
