#!/usr/bin/env python3
"""Complete fixed one-pair Kempe family, exact selector projection."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'hadwiger_nelson_heule632_pair_pilot'))
import build as geometric
spec = importlib.util.spec_from_file_location('fixed_interface_producer', ROOT / 'hadwiger_nelson_heule560_interface/build.py')
interface = importlib.util.module_from_spec(spec)
spec.loader.exec_module(interface)


def load():
    plan = json.loads((HERE / 'plan.json').read_text())
    for name, digest in plan['input_files'].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError('input hash: ' + name)
    boundary = json.loads((ROOT / 'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    mandatory, optional = boundary['mandatory_vertices'], boundary['optional_vertices']
    c = json.loads((ROOT / 'hadwiger_nelson_heule560_degree_family/certificate.json').read_text())['cover_colouring']
    _, edges, _ = geometric.geometry()
    return plan, mandatory, optional, c, edges


def normalize(c, mandatory):
    names = {}
    result = ['.'] * 632
    for v in mandatory:
        names.setdefault(c[v], str(len(names)))
        result[v] = names[c[v]]
    return ''.join(result)


def templates(mandatory, c, edges):
    adj = {v: set() for v in mandatory}
    for u, v in edges:
        if u in adj and v in adj:
            adj[u].add(v)
            adj[v].add(u)
    result = {}
    component_rows = []
    slots = 0
    for a, b in itertools.combinations('0123', 2):
        remaining = {v for v in mandatory if c[v] in (a, b)}
        components = []
        while remaining:
            stack = [min(remaining)]
            remaining.remove(stack[0])
            component = []
            while stack:
                u = stack.pop()
                component.append(u)
                reached = sorted(adj[u] & remaining)
                remaining.difference_update(reached)
                stack.extend(reached)
            components.append(sorted(component))
        component_rows.append({'pair': [int(a), int(b)], 'components': components})
        for mask in range(1 << (len(components) - 1)):
            slots += 1
            new = list(c)
            for i, component in enumerate(components[1:]):
                if mask >> i & 1:
                    for v in component:
                        new[v] = b if c[v] == a else a
            text = normalize(new, mandatory)
            result.setdefault(text, []).append({'pair': [int(a), int(b)], 'mask': mask})
    return component_rows, slots, result


def antichain(rows):
    result = []
    for row in sorted(set(rows), key=lambda r: (r.bit_count(), r)):
        if not any(old & row == old for old in result):
            result.append(row)
    return result


def compact_boundary(allrows, combined, mandatory, optional, edges, limits):
    """A small semantic certificate, independent of the projection trace."""
    transversals = [frozenset()]
    start = time.monotonic()
    for forbidden in combined:
        candidates = set()
        for old in transversals:
            if old & set(forbidden):
                candidates.add(old)
            else:
                candidates.update(old | {v} for v in forbidden)
        transversals = []
        for t in sorted(candidates, key=lambda t: (len(t), sorted(t))):
            if not any(old <= t for old in transversals):
                transversals.append(t)
        if len(transversals) > limits['max_boundary_cases']:
            raise RuntimeError('boundary size cap')
    adj = {v: set() for v in mandatory + optional}
    for u, v in edges:
        if u in adj and v in adj:
            adj[u].add(v)
            adj[v].add(u)
    witnesses = []
    for omitted in transversals:
        selected = set(optional) - omitted
        row = next(row for row in allrows if not any(set(f) <= selected for f in row['minimal_nonextending_sets']))
        colour = row['colouring']
        domains = {v: set(range(4)) - {int(colour[n]) for n in adj[v] & set(mandatory)} for v in selected}
        assigned = {}

        def search():
            if time.monotonic() - start > limits['seconds_per_stage']:
                raise RuntimeError('boundary colouring cap')
            if len(assigned) == len(selected):
                return True
            choices = {v: domains[v] - {assigned[n] for n in adj[v] if n in assigned}
                       for v in selected if v not in assigned}
            v = min(choices, key=lambda v: (len(choices[v]), -len(adj[v]), v))
            for c in sorted(choices[v]):
                assigned[v] = c
                if search():
                    return True
            assigned.pop(v, None)
            return False

        if not search():
            raise ValueError('projected boundary has no positive witness')
        text = list(colour)
        for v, c in assigned.items():
            text[v] = str(c)
        witnesses.append({'omitted_optional': sorted(omitted), 'colouring': ''.join(text)})
    counts, unions = interface.counts_by_union(combined, 68)
    template_stream = ''.join(row['colouring'] + '\n' for row in allrows).encode('ascii')
    return {'quotient_slots': 123, 'distinct_templates': len(allrows),
            'canonical_template_stream_sha256': hashlib.sha256(template_stream).hexdigest(),
            'combined_minimal_nonextending_sets': combined, 'maximal_extending_cover_colourings': witnesses,
            'extending_counts_by_optional_size': counts, 'inclusion_exclusion_union_count': unions}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    plan, mandatory, optional, c, edges = load()
    components, slots, colours = templates(mandatory, c, edges)
    if [len(r['components']) for r in components] != plan['expected_component_counts'] or slots != plan['expected_quotient_slots']:
        raise ValueError('template family differs from frozen protocol')
    medges = [(u, v) for u, v in edges if u in set(mandatory) and v in set(mandatory)]
    oe = [(u, v) for u, v in edges if u in set(optional) and v in set(optional)]
    neighbours = {v: [] for v in optional}
    for u, v in edges:
        if u in neighbours and v in set(mandatory):
            neighbours[u].append(v)
        if v in neighbours and u in set(mandatory):
            neighbours[v].append(u)
    bit = {v: 1 << i for i, v in enumerate(optional)}
    allrows = []
    failures = [0]
    for index, (colour, recipes) in enumerate(sorted(colours.items())):
        if time.monotonic() - start > plan['limits']['seconds_per_stage']:
            raise RuntimeError('complete production time boundary')
        if any(colour[u] == colour[v] for u, v in medges):
            raise ValueError('improper Kempe template')
        lists = {v: set(range(4)) - {int(colour[n]) for n in neighbours[v]} for v in optional}
        forbidden, trace = interface.project(optional, lists, oe, plan['limits'])
        masks = [sum(bit[v] for v in row) for row in forbidden]
        if len(failures) * len(masks) > plan['limits']['max_products_per_step']:
            raise RuntimeError('combined product boundary')
        failures = antichain([x | y for x in failures for y in masks])
        if len(failures) > plan['limits']['max_antichain']:
            raise RuntimeError('combined antichain boundary')
        allrows.append({'colouring': colour, 'recipes': recipes, 'minimal_nonextending_sets': forbidden,
                        'projection_colour_variables': trace['colour_variables'], 'projection_initial_clauses': trace['initial_clauses'],
                        'projection_peak_clauses': trace['peak_live_clauses']})
        progress = {'completed_templates': index + 1, 'total_templates': len(colours), 'combined_obstructions': len(failures),
                    'minimum_obstruction_size': min(map(int.bit_count, failures), default=None)}
        (args.out / 'progress.json').write_text(json.dumps(progress, indent=2) + '\n')
        if (index + 1) % 20 == 0:
            print(json.dumps(progress), flush=True)
    combined = [sorted(v for v in optional if mask & bit[v]) for mask in failures]
    certificate = {'components': components, 'quotient_slots': slots, 'templates': allrows,
                   'combined_minimal_nonextending_sets': combined}
    (args.out / 'certificate.json').write_text(json.dumps(certificate, separators=(',', ':'), sort_keys=True) + '\n')
    compact = compact_boundary(allrows, combined, mandatory, optional, edges, plan['limits'])
    (args.out / 'compact_certificate.json').write_text(json.dumps(compact, separators=(',', ':'), sort_keys=True) + '\n')
    report = {'quotient_slots': slots, 'distinct_templates': len(colours), 'combined_obstructions': len(combined),
              'combined_obstruction_sizes': sorted(map(len, combined)), 'combined_minimal_nonextending_sets': combined,
              'positive_covers': len(compact['maximal_extending_cover_colourings']),
              'extending_16': compact['extending_counts_by_optional_size'][16],
              'elapsed_seconds': time.monotonic() - start}
    (args.out / 'report.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
