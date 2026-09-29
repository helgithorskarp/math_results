"""Small exact validation of the signed-state encoding and checked fixtures."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import sys

import hex_domain as hexes
import marked_corona as squares
from witness_contact_graph import analyze


def validate(Circuit):
    comparator_checks = 0
    for length in (4, 6):
        c = Circuit()
        signs = [(c.new(), c.new()) for _ in range(length)]
        squares.positive_charge_constraint(c, signs)
        for state in itertools.product((-1, 0, 1), repeat=length):
            values = {p: s == 1 for (p, q), s in zip(signs, state)}
            values.update({q: s == -1 for (p, q), s in zip(signs, state)})
            assert c.evaluate(values) == (state.count(1) > state.count(-1) > 0)
            comparator_checks += 1
    contact_checks = 0
    edge = ((0, 0), (1, 0))
    for fixed in (False, True):
        for a, b in itertools.product((-1, 0, 1), repeat=2):
            c = Circuit()
            if fixed:
                signs = [(1 if s == 1 else -1, 1 if s == -1 else -1) for s in (a, b)]
            else:
                signs = [(c.new(), c.new()) for _ in range(2)]
            actives = c.new(), c.new()
            globals_ = squares.edge_state_constraints(c, signs,
                [(actives[0], [(edge, 0)]), (actives[1], [(((2, 0), (3, 0)), 0), (edge, 1)])])
            for on_a, on_b in itertools.product((False, True), repeat=2):
                inputs = {actives[0]: on_a, actives[1]: on_b}
                if not fixed:
                    inputs.update({p: s == 1 for (p, q), s in zip(signs, (a, b))})
                    inputs.update({q: s == -1 for (p, q), s in zip(signs, (a, b))})
                variables = [v for pair in globals_.values() for v in pair]
                possible = any(c.evaluate({**inputs, **dict(zip(variables, bits))})
                               for bits in itertools.product((False, True), repeat=len(variables)))
                assert possible == (not (on_a and on_b) or a == -b)
                contact_checks += 1
    square_incidence = hex_incidence = 0
    for domain, dimensions, turns in ((squares, ((1, 1), (4, 1), (5, 1), (2, 3)), 4),
                                      (hexes, ((1, 1), (2, 1), (4, 1), (5, 1)), 6)):
        for width, height in dimensions:
            tile = [(x, y) for x in range(width) for y in range(height)]
            for reflect, t in itertools.product((False, True), range(turns)):
                cells, ports = domain.oriented(tile, reflect, t)
                assert len(cells) == len(tile)
                assert set(e for e, s in ports) == set(tuple(sorted(e)) for e in domain.boundary(cells))
                for ends, side in ports:
                    if domain is squares:
                        (x, y), (u, v) = ends
                        owners = ((x, y), (x, y - 1)) if y == v else ((x, y), (x - 1, y))
                        assert owners[side] in cells and owners[1 - side] not in cells
                        square_incidence += 1
                    else:
                        assert ends[side] in cells and ends[1 - side] not in cells
                        assert tuple(b - a for a, b in zip(*ends)) in hexes.NEIGHBORS
                        hex_incidence += 1
    coordinates = list(itertools.product(range(3), repeat=2))
    circuit = Circuit()
    occ = {p: circuit.new() for p in coordinates}
    hexes.topology_constraint(circuit, occ)
    for mask in range(1 << len(coordinates)):
        cells = {p for i, p in enumerate(coordinates) if mask >> i & 1}
        adj = sum((x + dx, y + dy) in cells for x, y in cells
                  for dx, dy in ((1, 0), (0, 1), (-1, 1)))
        full = sum(a in cells and b in cells for x, y in cells
                   for a, b in (((x + 1, y), (x, y + 1)), ((x + 1, y), (x + 1, y - 1))))
        bg = set(itertools.product(range(-1, 4), repeat=2)) - cells
        chi = squares.component_count(cells, hexes.NEIGHBORS) - squares.component_count(bg, hexes.NEIGHBORS) + 1
        assert len(cells) - adj + full == chi
        assert circuit.evaluate({v: bool(mask >> i & 1) for i, (p, v) in enumerate(occ.items())}) == (chi == 1)
    directory = Path(__file__).resolve().parent
    square = json.loads((directory / "signed_rect4_depth3.witness.json").read_text())
    hexa = json.loads((directory / "signed_hex4_depth5.witness.json").read_text())
    square_stats = squares.check_witness(square)
    hex_stats = squares.check_witness(hexa)
    graph = analyze(hexa)
    assert len(graph["components"]) == 2 and len(graph["contact_pairs"]) == 35
    assert graph["components"][0]["counts"] == [9, 8]
    assert graph["components"][1] == {"vertices": [17], "bipartite": False}
    assert len(graph["single_component_markings"]) == 1
    rejection_checks = 0
    for witness in (square, hexa):
        bads = []
        bad = copy.deepcopy(witness); bad["patch"].append(copy.deepcopy(bad["patch"][0])); bads.append(bad)
        bad = copy.deepcopy(witness); bad["signs"][0] = 0.0; bads.append(bad)
        bad = copy.deepcopy(witness); bad["tile"][0][0] = 0.0; bads.append(bad)
        bad = copy.deepcopy(witness); bad["depth"] = True; bads.append(bad)
        bad = copy.deepcopy(witness); bad["patch"][0]["turns"] = 1; bads.append(bad)
        for bad in bads:
            try:
                squares.check_witness(bad)
            except (ValueError, TypeError, KeyError):
                rejection_checks += 1
            else:
                raise AssertionError("invalid fixture was accepted")
    return {"status": "passed", "charge_comparator_checks": comparator_checks,
            "conditional_edge_state_checks": contact_checks, "square_D4_incidence_checks": square_incidence,
            "hex_D6_incidence_checks": hex_incidence, "hex_Euler_and_gate_projection_checks": 512,
            "malformed_witness_rejections": rejection_checks,
            "square_fixture_tiles": [p["tiles"] for p in square_stats["prefixes"]],
            "hex_fixture_tiles": [p["tiles"] for p in hex_stats["prefixes"]]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--unmarked-source", type=Path,
                        default=Path(__file__).resolve().parent.parent / "heesch_polyomino_euler_cnf")
    args = parser.parse_args()
    squares.check_encoding_dependencies(args.unmarked_source)
    sys.path.insert(0, str(args.unmarked_source))
    from circuit import Circuit
    print(json.dumps(validate(Circuit), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
