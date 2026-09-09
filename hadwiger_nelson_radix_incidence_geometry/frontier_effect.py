#!/usr/bin/env python3
"""Apply only certified whole-pair exclusions to the global h4117 quotient."""
import argparse
import hashlib
import json
from pathlib import Path
import produce

HERE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def run(quotient_path, interface_path, export=None):
    quotient = json.loads(Path(quotient_path).read_text())
    interface = json.loads(Path(interface_path).read_text())
    certificate = json.loads((HERE / 'certificate.json').read_text())
    if digest(interface) != certificate['interface_sha256']:
        raise ValueError('verified geometry interface')
    pairs = quotient['pair_system_representatives']
    if len(pairs) != 132130 or digest(pairs) != 'ab9d291e1b59a234712eb9ef95aaeb70654921351542b825afeee887b118ccd6':
        raise ValueError('global h4117 pair interface')
    factors, circle, rows = produce.inventory()
    if digest(factors) != certificate['curve_inventory_sha256']:
        raise ValueError('curve degree/ID inventory')
    degrees = [max(i + j for i, j, c in f) for f in factors]
    offset_pairs = {tuple(p) for p in interface['monic_degree_four_excluded_pairs']}
    collision_pairs = {tuple(p) for p in interface['injectivity_excluded_sets'] if len(p) == 2}
    before = [p for p in pairs if circle not in p]
    excluded_pairs = collision_pairs | offset_pairs
    removed = [p for p in before if tuple(p) in excluded_pairs]
    if not all(tuple(p) in collision_pairs for p in removed):
        raise ValueError('the removed global pairs already force collisions')
    retained = [p for p in before if tuple(p) not in excluded_pairs]
    allowance = lambda ps: sum(degrees[a] * degrees[b] for a, b in ps)
    if export is not None:
        with Path(export).open('x') as f:
            json.dump(retained, f, separators=(',', ':'))
            f.write('\n')
    return {
        'verified': True, 'source_global_systems': len(pairs),
        'source_global_parameter_allowance': allowance(pairs),
        'after_accepted_circle_exclusion_systems': len(before),
        'after_accepted_circle_exclusion_allowance': allowance(before),
        'new_whole_pair_systems_excluded': len(removed),
        'new_parameter_allowance_removed': allowance(removed),
        'removed_pairs_sha256': digest(removed),
        'remaining_global_pair_systems': len(retained),
        'remaining_parameter_allowance': allowance(retained),
        'remaining_pairs_sha256': digest(retained),
        'all_removed_pairs_force_label_collision': True,
        'injectivity_excluded_conjunctions': certificate['injectivity_excluded_sets'],
        'combined_nonfour_excluded_conjunctions': certificate['combined_nonfour_excluded_sets'],
        'eight_active_gate_closed': False, 'record_improvement': False,
        'scope': 'Global pair representatives are used without a simultaneous chamber restriction. Counts are conservative Bezout allowances, not distinct-root counts. Triple exclusions remain usable at all higher incidences but do not individually remove a whole pair system.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--quotient', type=Path, required=True)
    parser.add_argument('--interface', type=Path, required=True)
    parser.add_argument('--export-remaining', type=Path)
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args()
    result = run(args.quotient, args.interface, args.export_remaining)
    if args.check_expected and result != json.loads((HERE / 'FRONTIER_EFFECT.json').read_text()):
        raise ValueError('expected frontier effect')
    print(json.dumps(result, indent=2, sort_keys=True))
