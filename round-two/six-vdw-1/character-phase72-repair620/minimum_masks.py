"""Untrusted edge-branch catalogue and actual-AP unit-conflict producer.

The catalogue enumerates all size-nine covers containing1 by selecting the
first chosen vertex of a currently unmet edge. The independent binary
classifier is not imported here.
"""
import hashlib
import json
import math
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def catalogue(edges, size=9):
    supports = [sum(1 << (r - 1) for r in edge) for edge in edges]
    found = []
    stats = {'nodes': 0, 'unavailable_edge': 0, 'too_small': 0}
    all_vertices = (1 << 30) - 1

    def visit(chosen, available, unmet):
        stats['nodes'] += 1
        need(stats['nodes'] <= 2000000, 'fixed two-million-node bound; incomplete on failure')
        left = size - chosen.bit_count()
        if left < 0 or available.bit_count() < left:
            stats['too_small'] += 1
            return
        if not unmet:
            need(left == 0, 'a smaller cover contradicts the separately audited minimum')
            found.append([r for r in range(1, 31) if chosen & (1 << (r - 1))])
            return
        if left == 0:
            return
        edge = min((edge & available for edge in unmet), key=lambda x: (x.bit_count(), x))
        if edge == 0:
            stats['unavailable_edge'] += 1
            return
        # Every completion has a unique first selected vertex in this edge.
        # Earlier vertices are excluded from later branches; the edge must be hit.
        candidates = edge
        remaining = available
        while candidates:
            vertex = candidates & -candidates
            candidates ^= vertex
            remaining ^= vertex
            visit(chosen | vertex, remaining, [e for e in unmet if not (e & vertex)])

    visit(1, all_vertices ^ 1, [edge for edge in supports if not (edge & 1)])
    found.sort()
    need(len(found) == len({tuple(e) for e in found}), 'producer catalogue has no duplicates')
    return found, stats


def unit_rules():
    """Actual cyclic APs with one point omitted, six fixed equal colors."""
    phase = [((72 >> (s % 10)) & 1) ^ (s // 10) for s in range(20)]
    colors = [None if n % 31 in (0, 30)
              else int(pow((n % 31 + 1) % 31, 15, 31) != 1) ^ phase[n % 20]
              for n in range(620)]
    rules = {}
    regular = pole = repeated_fields = 0
    for a in range(620):
        for d in range(1, 620):
            points = [(a + j * d) % 620 for j in range(7)]
            fields = [n % 31 for n in points]
            if 0 in fields:
                pole += 1
                continue
            regular += 1
            if len(set(fields)) != 7:
                # Constant field APs cannot leave exactly one field point free.
                repeated_fields += 1
                continue
            support = sum(1 << (r - 1) for r in fields)
            for j, point in enumerate(points):
                fixed = [colors[points[k]] for k in range(7) if k != j]
                if fixed[0] is None or any(x != fixed[0] for x in fixed):
                    continue
                r, s = fields[j], point % 20
                required_lower = (1 - fixed[0]) ^ (s // 10)
                key = (support, r, s % 10, required_lower)
                rules.setdefault(key, [a, d])
    need((regular, pole) == (299400, 84380), 'whole actual cyclic start/step domain')
    return rules, {'original_pairs': 383780, 'regular_pairs': regular,
                   'pole_pairs': pole, 'constant_field_pairs': repeated_fields,
                   'distinct_unit_rules': len(rules)}


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    output = here / 'minimum-mask-proposal.json'
    need(not output.exists(), 'fresh proposal, preserve old evidence')
    hypergraph = json.loads((here / 'hypergraph72.json').read_text())
    need(hashlib.sha256(json.dumps(hypergraph['edges'], separators=(',', ':'), sort_keys=True).encode()).hexdigest()
         == 'b44cf8af4cbb78425f5bfc3c4b82c9e050fe57bb82e691200c6756b5241d4846', 'whole frozen actual hypergraph')
    covers, enumeration = catalogue(hypergraph['edges'])
    rules, rule_stats = unit_rules()
    entries = []
    for cover in covers:
        free = sorted([30] + [r - 1 for r in cover if r != 1])
        free_mask = sum(1 << (r - 1) for r in free)
        demands = {}
        conflict = None
        for (support, r, cell, bit), ap in rules.items():
            if support & free_mask != 1 << (r - 1):
                continue
            key = (r, cell)
            if key in demands and bit != demands[key][0]:
                first = {'required_lower': demands[key][0], 'ap': demands[key][1]}
                second = {'required_lower': bit, 'ap': ap}
                conflict = {'field': r, 'lower_phase_cell': cell,
                            'opposite_actual_ap_demands': [first, second]}
                break
            demands[key] = (bit, ap)
        entries.append({'reference_cover': cover, 'actual_free_fields': free,
                        'unit_conflict': conflict})
    result = {'author': 'six-vdw-1', 'role': 'researcher',
              'schema': 'PHASE72_MINIMUM_MASK_UNIT_CONFLICT_PROPOSAL_V1',
              'edge_sha256': hypergraph['edge_sha256'], 'mask': 72,
              'reference_root': 30, 'actual_pole': 0, 'fixed_reference_vertex': 1,
              'cover_size': 9, 'candidate_domain_size': math.comb(29, 8),
              'catalogue_statistics': enumeration, 'rule_statistics': rule_stats,
              'covers': len(covers), 'masks_with_conflicts': sum(e['unit_conflict'] is not None for e in entries),
              'entries': entries,
              'scope': 'Candidate complete normalized minimum-cover catalogue with physical AP unit refutations where found; independent checks required.'}
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'entries'}, sort_keys=True))
