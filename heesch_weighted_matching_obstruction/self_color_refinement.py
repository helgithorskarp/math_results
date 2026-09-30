#!/usr/bin/env python3
"""Canonical port refinement of the published five-corona strip patch.

The independent periodic matching check below decodes cell owners and
inverse motions directly; it uses no SAT circuit or solver.
"""

import hashlib
import json
from pathlib import Path

import hex_domain
import marked_corona
from witness_contact_graph import analyze


FIXTURE = Path(__file__).resolve().parent / "signed_hex4_depth5.witness.json"
FIXTURE_SHA256 = "d857774a28daa5e8f28e45a4ce711cc45ebc11cb759904fa98309122892aed0a"


def periodic_check(tile, colors):
    tile = set(map(tuple, tile))
    assert tile == {(0, 0), (1, 0), (2, 0), (3, 0)}
    original = {tuple(sorted(edge)): i for i, edge in enumerate(hex_domain.boundary(tile))}

    def owner(cell):
        x, y = cell
        block, residue = divmod(x, 8)
        return (8*block, y, 0) if residue < 4 else (8*block+4, y, 3)

    def inverse(cell, placement):
        tx, ty, turns = placement
        x, y = cell
        if turns == 0:
            return x-tx, y-ty
        # R^3=-I; the transformed four-cell strip was normalized by +(3,0).
        assert turns == 3
        return tx+3-x, ty-y

    footprint0 = {(x, 0) for x in range(4)}
    footprint1 = {(7-x, 0) for x in range(4)}
    assert not footprint0 & footprint1
    assert footprint0 | footprint1 == {(x, 0) for x in range(8)}
    interface_checks = private_incidences = 0
    for cell in sorted(footprint0 | footprint1):
        placement = owner(cell)
        assert inverse(cell, placement) in tile
        for dx, dy in hex_domain.NEIGHBORS:
            adjacent = (cell[0]+dx, cell[1]+dy)
            other = owner(adjacent)
            if other == placement:
                assert inverse(adjacent, placement) in tile
                continue
            first = tuple(sorted((inverse(cell, placement), inverse(adjacent, placement))))
            second = tuple(sorted((inverse(cell, other), inverse(adjacent, other))))
            a, b = original[first], original[second]
            assert colors[a] == colors[b]
            interface_checks += 1
            private_incidences += colors[a] == 2
    assert interface_checks == 36 and private_incidences == 2
    return {"periods": [[8, 0], [0, 1]], "determinant": 8,
            "copies": [{"turns": 0, "translation": [0, 0]},
                       {"turns": 3, "translation": [4, 0]}],
            "cell_classes": 8, "boundary_incidence_checks": interface_checks,
            "private_color_incidences": private_incidences,
            "inverse_motion_and_cell_owner_check": True}


def main():
    raw = FIXTURE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256
    witness = json.loads(raw)
    assert witness["grid"] == "hex" and witness["depth"] == 5
    tile = witness["tile"]
    old = marked_corona.check_witness(witness)
    changed = 0
    for record in witness["patch"]:
        if record["reflect"]:
            before, _ = hex_domain.oriented(tile, True, record["turns"])
            after, _ = hex_domain.oriented(tile, False, record["turns"])
            assert before == after  # Valid for this mirror-symmetric strip.
            record["reflect"] = False
            changed += 1
    witness["signs"] = [0] * len(witness["signs"])
    result = analyze(witness)
    assert result["witness_checks"]["prefixes"] == old["prefixes"]
    components = result["components"]
    assert [c["vertices"] for c in components] == [list(range(17)), [17]]
    assert all(not c["bipartite"] for c in components)
    loops = [i for i, j in result["contact_pairs"] if i == j]
    assert all(set(c["vertices"]) & set(loops) for c in components)
    colors = [1]*17 + [2]
    assert all(colors[i] == colors[j] for i, j in result["contact_pairs"])
    assert len(result["contact_pairs"]) == 51
    pair_cells = hex_domain.boundary(tile)[17]
    center_sum = tuple(pair_cells[0][i]+pair_cells[1][i] for i in (0, 1))
    partner = {(center_sum[0]-x, center_sum[1]-y) for x, y in tile}
    assert not partner & set(map(tuple, tile))
    dimer = partner | set(map(tuple, tile))
    assert dimer == {(x, 0) for x in range(8)}
    out = {"agent": "six-heesch-3", "role": "researcher",
           "input_witness_sha256": FIXTURE_SHA256,
           "uniform_rotational_reinterpretation": {
               "changed_reflection_records": changed,
               "layers": [s["tiles"] for s in old["prefixes"]],
               "footprints_and_prefix_topology_preserved": True},
           "port_graph": {"ports": 18, "contact_pairs": 51,
                          "components": [c["vertices"] for c in components],
                          "self_loops": loops, "nonbipartite_components": 2},
           "strongest_compatible_colors": colors,
           "compatible_directed_states": "all zero; each connected component has a self-loop",
           "private_port": 17, "private_port_cell_pair": [list(p) for p in pair_cells],
           "forced_dimer": sorted(map(list, dimer)),
           "periodic_tiling": periodic_check(tile, colors),
           "conclusion": "Every color/state marking compatible with this uniform five-corona patch tiles the plane in the quintic realization; this patch cannot yield a finite record through that refinement.",
           "scope": "This fixed reinterpreted patch only; other patches and mixed-handed quartic models remain unclassified."}
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
