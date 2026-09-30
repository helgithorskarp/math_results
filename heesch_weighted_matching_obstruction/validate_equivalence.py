"""Definition-level tests before using direct equality variables in research."""
from itertools import combinations, product
import argparse
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--unmarked-source', type=Path, default=HERE.parent/'heesch_polyomino_euler_cnf')
args = parser.parse_args()
import marked_corona
marked_corona.check_encoding_dependencies(args.unmarked_source)
sys.path.insert(0, str(args.unmarked_source.resolve()))
from circuit import Circuit
from pysat.solvers import Solver
import color_state as cs
import equivalence_state as es
import hex_domain as hd

evidence = {}
counts = []
for n in range(1, 7):
    c = Circuit(); pairs = es.partition_variables(c, n)
    valid = 0
    for bits in product([False, True], repeat=len(pairs)):
        inputs = dict(zip(pairs.values(), bits))
        positive = {x for x, value in inputs.items() if value}
        try:
            labels = es.decode_partition(pairs, n, positive)
            direct = all((labels[i] == labels[j]) == value for (i, j), value in zip(pairs, bits))
        except ValueError:
            direct = False
        encoded = c.evaluate(inputs)
        assert encoded == direct, (n, bits)
        valid += direct
    counts.append(valid)
assert counts == [1, 2, 5, 15, 52, 203]
evidence['partition_assignment_cases'] = sum(2**(n*(n-1)//2) for n in range(1, 7))
evidence['partition_models'] = counts

# Includes the illegal (+,-)=(1,1) assignment; direct checks must reject it.
c = Circuit(); pairs = es.partition_variables(c, 3)
signs = [(c.new(), c.new()) for _ in range(3)]
for p, m in signs: c.clause([-p, -m])
compat = es.compatibility_literals(c, pairs, signs)
compat_cases = 0
for bits in product([False, True], repeat=3):
    for signs_bits in product([False, True], repeat=6):
        inputs = dict(zip(pairs.values(), bits))
        inputs.update(zip([x for row in signs for x in row], signs_bits))
        positive = {x for x, value in inputs.items() if value}
        try: labels = es.decode_partition(pairs, 3, positive); partition_valid = True
        except ValueError: partition_valid = False; labels = [0]*3
        states = [int(inputs[p])-int(inputs[m]) for p, m in signs]
        valid = partition_valid and all(not(inputs[p] and inputs[m]) for p, m in signs)
        assert c.evaluate(inputs) == valid
        for (i, j), literal in compat.items():
            good = labels[i] == labels[j] and states[i] == -states[j]
            c.clause([literal if good else -literal])
            assert c.evaluate(inputs) == valid, (bits, signs_bits, i, j)
            c.clauses.pop(); compat_cases += 1
evidence['compatibility_truth_cases_including_invalid_states'] = compat_cases

motif_block_cases = 0
for bits in product([False, True], repeat=3):
    for ternary_states in product([-1, 0, 1], repeat=3):
        inputs = dict(zip(pairs.values(), bits))
        for (p, m), state in zip(signs, ternary_states):
            inputs[p] = state == 1; inputs[m] = state == -1
        positive = {x for x, value in inputs.items() if value}
        try: labels = es.decode_partition(pairs, 3, positive)
        except ValueError: continue
        for selected in product([False, True], repeat=len(compat)):
            edges = [edge for edge, present in zip(compat, selected) if present]
            forbidden = all(labels[i] == labels[j] and ternary_states[i] == -ternary_states[j]
                            for i, j in edges)
            es.exclude_motif(c, compat, edges)
            assert c.evaluate(inputs) == (not forbidden)
            c.clauses.pop(); motif_block_cases += 1
evidence['motif_exclusion_truth_cases'] = motif_block_cases

contact_cases = 0
geometry = []
for tile in [[(0, 0)], [(0, 0), (1, 0)], [(0, 0), (1, 0), (2, 0), (2, 1)]]:
    for radius in ([0, 1, 5] if len(tile) == 4 else [0, 1]):
        c, candidates, incidences, stats = cs.cover_geometry(tile, radius, Circuit)
        actual, omitted = es.contact_inventory(tile, candidates, incidences)
        records = [{'turns': 0, 'translation': [0, 0]}] + candidates
        footprints = [cs.placement(tile, r) for r in records]
        ports = {edge: i for i, edge in enumerate(hd.boundary(tile))}
        expected = set()
        for a, b in combinations(range(len(records)), 2):
            ac, ai = footprints[a]; bc, bi = footprints[b]
            contact_cases += 1
            if ac & bc: continue
            for u in ac:
                for dx, dy in hd.NEIGHBORS:
                    v = (u[0]+dx, u[1]+dy)
                    if v in bc:
                        i = ports[ai(u), ai(v)]; j = ports[bi(v), bi(u)]
                        expected.add((a, b, min(i, j), max(i, j)))
        assert actual == sorted(expected), (tile, radius)
        geometry.append({'tile': tile, 'radius': radius, 'candidates': len(candidates),
                         'contacts': len(actual), 'overlapping_contact_pairs_omitted': omitted})
evidence['candidate_pair_cases_independently_decoded'] = contact_cases
evidence['geometry'] = geometry

def sign_assumptions(signs, states):
    return [literal if ((s == 1) if k == 0 else (s == -1)) else -literal
            for (p, m), s in zip(signs, states) for k, literal in enumerate([p, m])]

# All contact equations must be sufficient and necessary after choosing labels.
random_source = random.Random(61305)
fixed_cases = 0
decoded_covers = 0
for tile in [[(0, 0)], [(0, 0), (1, 0)], [(0, 0), (1, 0), (2, 0), (2, 1)]]:
    n = len(hd.boundary(tile))
    for radius in [1, 2]:
        c, candidates, pairs, signs, compat, stats = es.build_cover(tile, radius, Circuit)
        with Solver(name='glucose4', bootstrap_with=c.clauses) as solver:
            for k in range(4):
                colors = [1]*n if k == 0 else [random_source.randrange(1, 4) for _ in range(n)]
                states = [0]*n if k < 2 else [random_source.randrange(-1, 2) for _ in range(n)]
                assumptions = [v if colors[i] == colors[j] else -v for (i, j), v in pairs.items()]
                assumptions += sign_assumptions(signs, states)
                result = solver.solve(assumptions=assumptions)
                other, oc, os = cs.build_cover(tile, radius, colors, states, Circuit)
                with Solver(name='glucose4', bootstrap_with=other.clauses) as old:
                    reference = old.solve()
                assert result == reference, (tile, radius, colors, states)
                if result:
                    positive = {x for x in solver.get_model() if x > 0}
                    witness = es.decode_cover(tile, radius, candidates, pairs, signs, positive)
                    assert witness['signs'] == states
                    assert all((witness['colors'][i] == witness['colors'][j]) == (colors[i] == colors[j])
                               for i, j in combinations(range(n), 2))
                    decoded_covers += 1
                fixed_cases += 1
evidence['fixed_table_cover_comparisons'] = fixed_cases
evidence['independently_decoded_SAT_covers'] = decoded_covers

motifs = json.loads((HERE/'bend4_directed_cover_tiling.json').read_text())['motifs']
tile = [(0, 0), (1, 0), (2, 0), (2, 1)]
for motif in motifs:
    checks = cs.check_periodic(tile, [1]*18, [0]*18, motif['patch'], *motif['period'])
    assert checks == motif['checks']
evidence['rechecked_periodic_motifs'] = len(motifs)
print(json.dumps(evidence, indent=2), flush=True)
expected_path = HERE/'equivalence_validation_expected.json'
if expected_path.exists() and evidence != json.loads(expected_path.read_text()):
    raise AssertionError('validation output differs from frozen expected data')
