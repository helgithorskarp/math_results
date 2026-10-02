"""Independent weighted complete census and literal physical AP refutations.

Imports only the independent cover checker, not the edge-branch producer,
rule generator, repaired CNF encoder, or any native solver.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
from check_cover import check, classify


def need(ok, message):
    if not ok:
        raise ValueError(message)


def check_unit(free, field, cell, demand):
    need(type(field) is int and field in free and type(cell) is int and 0 <= cell < 10,
         'actual free column and antipodal phase cell')
    need(type(demand['required_lower']) is int and demand['required_lower'] in [0, 1],
         'literal required lower bit')
    ap = demand['ap']
    need(type(ap) is list and len(ap) == 2 and all(type(x) is int for x in ap)
         and 0 <= ap[0] < 620 and 1 <= ap[1] < 620, 'actual start and all nonzero cyclic steps')
    positions = [(ap[0] + j * ap[1]) % 620 for j in range(7)]
    squares = {x * x % 31 for x in range(1, 31)}
    lower = [int(bool(72 & (2 ** s))) for s in range(10)]
    fixed_colors = []
    free_points = []
    for n in positions:
        r, s = n % 31, n % 20
        need(r != 0, 'actual regular AP, physical pole is not an input')
        if r in free:
            free_points.append((r, s))
        else:
            argument = (r + 1) % 31
            need(argument != 0, 'reference zero is not silently fixed or discarded')
            fixed_colors.append(int(argument not in squares) ^ lower[s % 10] ^ int(s >= 10))
    need(len(free_points) == 1 and len(fixed_colors) == 6,
         'exactly one physical free point and six actual fixed points')
    r, s = free_points[0]
    need(r == field and s % 10 == cell, 'demand names the actual free field/phase point')
    need(len(set(fixed_colors)) == 1, 'six actual fixed term colors agree')
    # With the claimed lower value the free point differs; its opposite gives
    # an actual seven-term monochromatic AP. This directly checks both bits.
    required = demand['required_lower']
    need((required ^ int(s >= 10)) != fixed_colors[0], 'claimed bit really avoids this AP')
    need(((1 - required) ^ int(s >= 10)) == fixed_colors[0], 'opposite bit really makes this AP monochromatic')
    return {'positions': positions, 'required_lower': required,
            'fixed_color': fixed_colors[0], 'free_phase': s}


def audit(hypergraph, positive, record):
    check(hypergraph, positive)  # Independently hash/validate all edges and scalar maps.
    need(record['schema'] == 'PHASE72_MINIMUM_MASK_UNIT_CONFLICT_PROPOSAL_V1'
         and record['edge_sha256'] == hypergraph['edge_sha256'] and record['mask'] == 72
         and record['reference_root'] == 30 and record['actual_pole'] == 0
         and record['fixed_reference_vertex'] == 1 and record['cover_size'] == 9
         and record['candidate_domain_size'] == math.comb(29, 8), 'exact two-hole normalized repaired family')
    census = classify(30, hypergraph['edges'], 9)
    entries = record['entries']
    seen = set()
    checked_aps = []
    for entry in entries:
        cover = entry['reference_cover']
        need(type(cover) is list and cover == sorted(set(cover)) and len(cover) == 9
             and 1 in cover and all(type(r) is int and 1 <= r <= 30 for r in cover), 'literal minimum cover')
        need(tuple(cover) not in seen, 'no duplicate certificate can substitute for another mask')
        seen.add(tuple(cover))
        need(all(set(edge) & set(cover) for edge in hypergraph['edges']), 'literal cover hits every actual bad edge')
        free = sorted([30] + [r - 1 for r in cover if r != 1])
        need(entry['actual_free_fields'] == free and len(free) == 9 and 0 not in free and 30 in free,
             'actual pole omitted, actual reference zero retained freely')
        conflict = entry['unit_conflict']
        need(type(conflict) is dict, 'every minimum mask has a physical contradiction')
        demands = conflict['opposite_actual_ap_demands']
        need(type(demands) is list and len(demands) == 2
             and {d['required_lower'] for d in demands} == {0, 1}, 'opposite bits for the same free point cell')
        for demand in demands:
            checked_aps.append(check_unit(free, conflict['field'], conflict['lower_phase_cell'], demand))
    need(len(seen) == census['positive_volume'],
         'every literal catalogue member is a distinct positive and matches the COMPLETE independent positive count')
    need(record['covers'] == len(seen) and record['masks_with_conflicts'] == len(seen), 'exact full counts')
    normalized = [list(c) for c in sorted(seen)]
    return {'author': 'six-vdw-1', 'role': 'researcher',
            'status': 'COMPLETE_INDEPENDENT_MINIMUM_MASK_PHYSICAL_CONFLICT_AUDIT',
            'mask': 72, 'minimum_cover_size': 9, 'normalized_minimum_covers': len(seen),
            'all_nine_cover_domain': census, 'physical_ap_witnesses': len(checked_aps),
            'actual_term_checks': 7 * len(checked_aps), 'opposite_input_bits_checked': len(checked_aps),
            'cover_catalogue_sha256': hashlib.sha256(json.dumps(normalized, separators=(',', ':')).encode()).hexdigest(),
            'literal_ap_checks_sha256': hashlib.sha256(json.dumps(checked_aps, separators=(',', ':'), sort_keys=True).encode()).hexdigest(),
            'scope': 'All normalized minimum masks refuted for cyclic regular620 shifted-character background, independently reconstructed actual AP terms; no numerical van der Waerden bound.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('proposal', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    print(json.dumps(audit(json.loads((here / 'hypergraph72.json').read_text()),
                           json.loads((here / 'cover9.json').read_text()),
                           json.loads(args.proposal.read_text())), sort_keys=True))
