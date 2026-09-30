"""Check independent decoding and universal-encoding boundaries on small cases."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile

import color_state as cs
import hex_domain as hd
import marked_corona


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--unmarked-source', type=Path,
                        default=Path(__file__).resolve().parent.parent / 'heesch_polyomino_euler_cnf')
    args = parser.parse_args()
    marked_corona.check_encoding_dependencies(args.unmarked_source)
    sys.path.insert(0, str(args.unmarked_source.resolve()))
    from circuit import Circuit
    from pysat.solvers import Solver
    out = {}

    cases = 0
    for colors in ([1,1], [1,2], [2,2], [1,4], [3,4], [4,4]):
        for left, right in itertools.product([False, True], repeat=2):
            c = Circuit()
            a, b = c.new(), c.new()
            cs.color_constraints(c, colors, [(a, [('e',0)]), (b,[('other',0),('e',1)])])
            with Solver(name='glucose4', bootstrap_with=c.clauses) as s:
                got = s.solve(assumptions=[a if left else -a, b if right else -b])
            assert got == (not (left and right) or colors[0] == colors[1])
            cases += 1
    out['conditional_color_cases'] = cases

    cases = 0
    for colors in itertools.product(range(4), repeat=2):
        for states in itertools.product([-1, 0, 1], repeat=2):
            c = Circuit()
            bits = [tuple(c.new() for _ in range(2)) for _ in range(2)]
            signs = [tuple(c.new() for _ in range(2)) for _ in range(2)]
            cs.exclude_periodic_pairs(c, bits, signs, [(0,1)])
            assumptions = []
            for color, xs in zip(colors, bits):
                assumptions.extend(x if (color >> k) & 1 else -x for k,x in enumerate(xs))
            for state, (a,b) in zip(states, signs):
                assumptions.extend((a if state == 1 else -a, b if state == -1 else -b))
            with Solver(name='glucose4', bootstrap_with=c.clauses) as s:
                got = s.solve(assumptions=assumptions)
            assert got == (colors[0] != colors[1] or states[0] != -states[1])
            cases += 1
    out['periodic_block_color_state_cases'] = cases

    c = Circuit()
    bits = [tuple(c.new() for _ in range(3)) for _ in range(5)]
    cs.canonical_partition_constraints(c, bits)
    models = cases = 0
    for values in itertools.product(range(8), repeat=5):
        inputs = {x: bool((value >> k) & 1)
                  for value, xs in zip(values, bits) for k,x in enumerate(xs)}
        got = c.evaluate(inputs)
        expected = all(values[i] == min(j for j in range(5) if values[j] == values[i]) for i in range(5))
        assert got == expected
        models += got
        cases += 1
    assert models == 52  # Bell(5), independently characterized by first indices.
    out['canonical_partition_cases'] = cases
    out['canonical_partition_models'] = models

    # Decode actual SAT models of both variable-label APIs, including states.
    out['variable_api_checks'] = {}
    for mode in ('cover', 'corona'):
        tile = [(0,0)]
        if mode == 'cover':
            circuit, candidates, bits, signs, _ = cs.build_cover_synthesis(tile,1,Circuit)
        else:
            circuit, candidates, bits, signs, _ = cs.build_synthesis(tile,1,Circuit)
        with Solver(name='glucose4', bootstrap_with=circuit.clauses) as solver:
            assert solver.solve()
            positive = {x for x in solver.get_model() if x > 0}
        colors = [1+sum(1 << k for k,x in enumerate(xs) if x in positive) for xs in bits]
        states = [1 if a in positive else -1 if b in positive else 0 for a,b in signs]
        patch = [{'level':0,'turns':0,'reflect':False,'translation':[0,0]}]
        for candidate in candidates:
            active = candidate['active'] if mode == 'cover' else candidate['z'][1]
            if active in positive:
                patch.append({'level':1,'turns':candidate['turns'],'reflect':False,
                              'translation':candidate['translation']})
        witness = {'grid':'hex','tile':tile,'colors':colors,'signs':states,'patch':patch}
        if mode == 'cover':
            witness.update(mode='rooted_cover',radius=1)
            checked = cs.check_cover(witness)
        else:
            witness['depth'] = 1
            checked = cs.check_corona(witness)['color_checks']
        assert checked['cells'] == 7 and checked['copies'] == 7
        out['variable_api_checks'][mode] = checked['matched_boundary_incidences']

    candidate_checks = 0
    tiles = [[(0,0)], [(0,0),(1,0),(2,0),(2,1)], [(0,0),(1,0),(1,1),(2,1)]]
    for tile in tiles:
        n = len(hd.boundary(tile))
        for radius in range(3):
            _, candidates, _ = cs.build_cover(tile, radius, [1]*n, [0]*n, Circuit)
            target, root = cs.region(tile, radius), set(tile)
            expected = set()
            for turns in range(6):
                raw = [cs.rotate(p, turns) for p in tile]
                ox, oy = min(x for x,y in raw), min(y for x,y in raw)
                shape = {(x-ox,y-oy) for x,y in raw}
                for tx in range(min(x for x,y in target)-max(x for x,y in shape), max(x for x,y in target)+1):
                    for ty in range(min(y for x,y in target)-max(y for x,y in shape), max(y for x,y in target)+1):
                        moved = {(x+tx,y+ty) for x,y in shape}
                        if moved & target and not moved & root:
                            expected.add((turns,tx,ty))
            actual = {(p['turns'],*p['translation']) for p in candidates}
            assert actual == expected
            candidate_checks += len(actual)
    out['complete_envelope_candidate_cases'] = candidate_checks

    # Distinct self-colors on a single hex force the half-turn at each of its
    # six neighbors; that sole whole surround has incompatible neighbor edges.
    tile = [(0,0)]
    root = {'level':0, 'turns':0, 'reflect':False, 'translation':[0,0]}
    forced = [root]
    for neighbor in hd.NEIGHBORS:
        allowed = []
        for turns in range(6):
            record = {'level':1, 'turns':turns, 'reflect':False, 'translation':neighbor}
            try:
                cs.check_patch(tile, list(range(1,7)), [0]*6, [root,record])
            except ValueError:
                continue
            allowed.append(turns)
        assert allowed == [3]
        forced.append({'level':1,'turns':3,'reflect':False,'translation':neighbor})
    try:
        cs.check_patch(tile,list(range(1,7)),[0]*6,forced)
    except ValueError:
        pass
    else:
        raise AssertionError('incompatible forced surround accepted')
    circuit, _, _ = cs.build_cover(tile,1,list(range(1,7)),[0]*6,Circuit)
    with Solver(name='glucose4',bootstrap_with=circuit.clauses) as solver:
        assert solver.solve() is False
    out['unique_color_single_hex'] = 'directly forced surround incompatible; CNF agrees'

    # Check wrapping to translates of the SAME motif copy, then cross-check
    # the older strip motif by its independently specialized owner function.
    out['one_hex_periodic'] = cs.check_periodic(tile,[1]*6,[0]*6,
                         [{'turns':0,'reflect':False,'translation':[0,0]}],1,0,1)
    strip = [(0,0),(1,0),(2,0),(3,0)]
    colors = [1]*17+[2]
    records = [{'turns':0,'reflect':False,'translation':[0,0]},
               {'turns':3,'reflect':False,'translation':[4,0]}]
    got = cs.check_periodic(strip,colors,[0]*18,records,8,0,1)
    from self_color_refinement import periodic_check
    assert got['boundary_incidences'] == periodic_check(strip,colors)['boundary_incidence_checks'] == 36
    out['strip_period_crosscheck'] = got
    try:
        cs.check_periodic([(0,0)],[2,1,1,1,1,1],[0]*6,
                          [{'turns':0,'reflect':False,'translation':[0,0]}],1,0,1)
    except ValueError:
        pass
    else:
        raise AssertionError('periodic mismatch accepted')

    circuit, *_ = marked_corona.build(tuple(strip),1,9,8,Circuit,hd.topology_constraint,domain=hd)
    with tempfile.TemporaryDirectory() as work:
        path = Path(work)/'previous-default.cnf'
        circuit.write_dimacs(path)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == '850b7d3664e2895bdc07ca24196a763170c849b30d8b4e17334dc51816ff43c4'
    out['previous_default_dimacs_sha256'] = digest
    print(json.dumps(out,sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
