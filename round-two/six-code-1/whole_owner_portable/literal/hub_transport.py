"""Literal hub relabeling, full inventory closure, and every original row."""
import argparse
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
import resource
import time
from model import Budget, Guard, digest, encode, need
from partitions import key
from inventory_gate import prototype


GROUP = tuple(tuple(a) + tuple(b) for a in permutations(range(3))
              for b in permutations(range(3, 5)))


def mask_image(mask, perm):
    need(isinstance(mask, int) and 0 <= mask < 32, 'entire original Hub mask')
    return sum(1 << perm[a] for a in range(5) if (mask >> a) & 1)


def descriptor_image(k, perm, budget):
    deficit, colors, rows = k
    need(deficit == 2 and len(colors) == 4 and len(rows) == 5, 'whole original D2 key')
    candidates = []
    for p in permutations(range(3)):
        budget.tick()
        p = tuple(p) + (3,)
        candidates.append([2, [mask_image(colors[j], perm) for j in p],
                           sorted([mask_image(mask, perm),
                                   [[mask_image(cells[j][0], perm), cells[j][1]] for j in p]]
                                  for mask, cells in rows)])
    return min(candidates)


def image_cells(cells, rho):
    return sorted(sorted(rho[a] for a in cell) for cell in cells)


def normalized_star(quads, values, budget):
    need(len(quads) == len({tuple(q) for q in quads}) == 20 and
         len(values) == 17 and sorted(values) == list(range(16)) + [17], 'entire original owner source')
    star = image_cells(quads, values)
    star = sorted(sorted([16] + w) for w in star)
    need(len({tuple(w) for w in star}) == 20 and all(len(set(w)) == 5 for w in star), 'whole literal owner20')
    for a, b in combinations(star, 2):
        budget.tick()
        need(len(set(a) & set(b)) <= 2, 'all190 literal target owner pairs')
    return star


def source_identity(record):
    fixture, hubs, mate, roles = record[0]
    return fixture, tuple(sorted(hubs)), record[1], mate


def verify_rho(rho, base_star, target_star, base_M, target_M, base_F, target_F, perm, budget):
    budget.tick()
    need(len(rho) == 18 and sorted(rho) == list(range(18)), 'entire18 point bijection')
    need([rho[a] for a in range(5)] == list(perm) and
         [rho[a] for a in [15, 16, 17]] == [15, 16, 17], 'all named Hub and original center images')
    need(perm in GROUP, 'covered Hub triple and other two Hub labels preserved')
    need(image_cells(base_star, rho) == target_star and
         image_cells(base_M, rho) == sorted(target_M) and
         image_cells(base_F, rho) == sorted(target_F), 'entire actual owner/M/F images')
    return True


def put(path, obj):
    path.write_bytes(encode(obj) + b'\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    spec = json.loads(args.spec.read_bytes())
    for pin in spec['input_pins']:
        b = Path(pin['path']).read_bytes()
        need(len(b) == pin['bytes'] and hashlib.sha256(b).hexdigest() == pin['sha256'], 'whole source pin')
    types = json.loads(Path(spec['all697_spec']).read_bytes())['all_original697_D2_types']
    fine = json.loads(Path(spec['whole_original_fine_inventory']).read_bytes())
    fixtures = json.loads(Path(spec['whole23_source_fixtures']).read_bytes())['stars']
    need(len(fine) == 2117 and len(types) == len({encode(t['canonical_key']) for t in types}) == 697,
         'entire original fine dictionary and disjoint selected697 inventory')
    by_key = {encode(t['canonical_key']): t['original_type_id'] for t in types}
    need(all(fine[t['original_type_id']][0] == t['canonical_key'] for t in types), 'whole original fine type keys')
    progress = {'complete': False, 'status': 'INCOMPLETE_NOT_ABSENCE', 'completed_closure_pairs': 0,
                'completed_original_owner_rows': 0}
    put(args.out / 'progress.json', progress)
    active = None
    closure = []
    row_receipts = []
    max_states = 0
    try:
        for pi, perm in enumerate(GROUP):
            maps = []
            for t in types:
                if time.monotonic() - start > 60:
                    raise Guard('original60s hub-transport child')
                active = Budget('whole inventory action ' + str(pi) + '/' + str(t['original_type_id']))
                k = descriptor_image(t['canonical_key'], perm, active)
                M, F = prototype(t['canonical_key'], active)
                rho = list(perm) + list(range(5, 15))
                literal = key(image_cells(M, rho), image_cells(F, rho), active)
                need(k == literal, 'whole mask action matches independent literal point-partition action')
                maps.append([t['original_type_id'], by_key.get(encode(k))])
                max_states = max(max_states, active.states)
                progress['completed_closure_pairs'] += 1
            closed = all(target is not None for source, target in maps)
            if closed:
                need(len({target for source, target in maps}) == 697, 'whole inventory action bijective')
            closure.append({'Hub_permutation': list(perm), 'closed': closed, 'all697_type_images': maps})
            put(args.out / 'progress.json', progress)
            active = None
        all_closed = all(x['closed'] for x in closure)
        base_specs = spec['completed_base_owner37_exclusions']
        base_data = {}
        target_ids = set()
        orbits = []
        for item in base_specs:
            gate = json.loads(Path(item['complete697_gate_record']).read_bytes())
            need(gate['complete'] and gate['original_D2_type_count'] == 697 and
                 gate['realized_D2_pairs'] == 0, 'pinned completed base owner37 exclusion')
            base_id = item['original_type_id']
            data = json.loads(Path(item['whole_direct_owner_input']).read_bytes())
            base_data[base_id] = data
            active = Budget('complete base key orbit ' + str(base_id))
            images = [by_key.get(encode(descriptor_image(fine[base_id][0], p, active))) for p in GROUP]
            ids = sorted({i for i in images if i is not None})
            target_ids.update(ids)
            orbits.append({'base_type_id': base_id, 'type_orbit': ids, 'all12_Hub_action_images': images,
                           'base_original_rows': data['owner_row_indices']})
            max_states = max(max_states, active.states)
        needed = {i for t in target_ids for i in fine[t][3]}
        records = {}
        flat = 0
        for line in Path(spec['whole_original_owner_record_file']).open():
            for record in json.loads(line):
                if flat in needed:
                    records[flat] = record
                flat += 1
        need(flat == 56292 and set(records) == needed,
             'every original named target row recovered from the entire pinned record file without grouped-line aliasing')
        all_type_checks = []
        for orbit in orbits:
            base_id = orbit['base_type_id']
            data = base_data[base_id]
            source_field = 'all_original_owner_rows' if 'all_original_owner_rows' in data else 'all_four_original_owner_rows'
            base_rows = {r['original_named_record_index']: r for r in data[source_field]}
            need(set(base_rows) == set(fine[base_id][3]), 'all original base rows retained')
            for target_id in orbit['type_orbit']:
                need(len(fine[target_id][3]) == fine[target_id][1] and
                     len(set(fine[target_id][3])) == fine[target_id][1], 'entire original target-row frequency')
                covered = []
                for row_id in fine[target_id][3]:
                    if time.monotonic() - start > 60:
                        raise Guard('original60s whole owner-row transport child')
                    active = Budget('whole original owner-row image ' + str(base_id) + '/' + str(row_id))
                    record = records[row_id]
                    need(record[7] == fine[target_id][0] and len(record) == 12, 'entire original target row and key')
                    choices = [b for b in base_rows if source_identity(records[b]) == source_identity(record)]
                    if not choices:
                        row_receipts.append({'base_type_id': base_id, 'target_type_id': target_id,
                                             'original_target_row': row_id, 'covered': False,
                                             'reason': 'no identical physical original source/Hubset/free/mate in base rows'})
                        continue
                    base_row_id = min(choices)
                    source = base_rows[base_row_id]
                    base_record = records[base_row_id]
                    fixture = record[0][0]
                    quads = fixtures[fixture]
                    need(quads == source['whole_original20_quadruples'] and
                         source['original17_point_map'] == base_record[8], 'whole original source identity and point map')
                    base_star = normalized_star(quads, source['original17_point_map'], active)
                    target_star = normalized_star(quads, record[8], active)
                    pairs = {source['original17_point_map'][a]: record[8][a] for a in range(17)}
                    pairs[16] = 16
                    rho = [pairs[a] for a in range(18)]
                    perm = tuple(rho[:5])
                    base_M, base_F = base_record[9], base_record[10]
                    target_M, target_F = record[9], record[10]
                    for star, record_M, record_F in [(base_star, base_M, base_F),
                                                     (target_star, target_M, target_F)]:
                        need(sorted(sorted(set(w) - {16, 17}) for w in star if 17 in w) == sorted(record_M) and
                             sorted(sorted(set(w) - {15, 16}) for w in star if 15 in w) == sorted(record_F),
                             'whole owner words bind every original mate/free partition')
                    need(sorted(base_M) == sorted(data['target_mate_triples']) and
                         sorted(base_F) == sorted(data['target_free_triples']), 'entire imported base owner37 interface')
                    verify_rho(rho, base_star, target_star, base_M, target_M, base_F, target_F, perm, active)
                    need(descriptor_image(fine[base_id][0], perm, active) == fine[target_id][0] and
                         key(target_M, target_F, active) == fine[target_id][0], 'entire actual target colored type binding')
                    receipt = {'base_type_id': base_id, 'target_type_id': target_id,
                               'original_base_row': base_row_id, 'original_target_row': row_id,
                               'source_fixture': fixture, 'Hub_permutation': list(perm), 'entire18_point_bijection': rho,
                               'whole_original20_target_quadruples': quads, 'whole_original17_target_point_map': record[8],
                               'whole_literal20_target_owner': target_star, 'covered': True,
                               'whole_case_states': active.states}
                    row_receipts.append(receipt)
                    covered.append(row_id)
                    progress['completed_original_owner_rows'] += 1
                    max_states = max(max_states, active.states)
                    active = None
                all_type_checks.append({'base_type_id': base_id, 'target_type_id': target_id,
                                        'all_original_rows': fine[target_id][3], 'covered_original_rows': covered,
                                        'all_original_rows_covered': sorted(covered) == sorted(fine[target_id][3]),
                                        'selected_inventory49_exclusion_transferred': all_closed and sorted(covered) == sorted(fine[target_id][3])})
                put(args.out / 'progress.json', progress)
        controls = []
        first = next((r for r in row_receipts if r['covered']), None)
        if first:
            b = records[first['original_base_row']]
            t = records[first['original_target_row']]
            active = Budget('whole original semantic damages')
            bs = normalized_star(fixtures[b[0][0]], b[8], active)
            ts = first['whole_literal20_target_owner']
            for name in ['nonbijective original image', 'moved original center', 'missing target owner word']:
                rho = first['entire18_point_bijection'].copy()
                target = ts
                if name == 'nonbijective original image':
                    rho[5] = rho[6]
                elif name == 'moved original center':
                    rho[15], rho[16] = rho[16], rho[15]
                else:
                    target = ts[:-1]
                try:
                    verify_rho(rho, bs, target, b[9], t[9], b[10], t[10], tuple(first['Hub_permutation']), active)
                except ValueError:
                    controls.append(name)
                else:
                    raise ValueError('semantic original-image damage accepted: ' + name)
        result = {'actual_agent': 'six-code-1', 'role': 'researcher', 'complete': True,
                  'whole_S3_times_S2_Hub_group_order': len(GROUP), 'original_D2_inventory_size': 697,
                  'complete_inventory_action_pairs': sum(len(x['all697_type_images']) for x in closure),
                  'all12_inventory_actions_closed_bijections': all_closed,
                  'all_inventory_closure_records': closure, 'all_base_type_orbits': orbits,
                  'all_original_target_type_checks': all_type_checks, 'all_original_row_image_certificates': row_receipts,
                  'complete_original_owner_rows': len(needed),
                  'all_original_owner_rows_covered': all(r['covered'] for r in row_receipts),
                  'conditionally_excluded_types': sorted({c['target_type_id'] for c in all_type_checks if c['selected_inventory49_exclusion_transferred']}),
                  'semantic_damages_rejected': controls, 'max_whole_case_states': max_states,
                  'normalization_inventory_and_label_action_bridges': 'ordinary unformalized',
                  'independent_person_review': 'pending', 'global_endpoint_change': False,
                  'other38072_physical_owner_rows_uncovered': True}
        put(args.out / 'mathematical-record.json', result)
        progress.update(complete=True, status='COMPLETE_QUALIFIED_LABEL_ACTION', mathematical_sha256=digest(result))
        put(args.out / 'progress.json', progress)
        summary = {'mathematical_record': result, 'mathematical_sha256': digest(result),
                   'elapsed_seconds': time.monotonic() - start,
                   'peak_rss_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        put(args.out / 'summary.json', summary)
        print(json.dumps({'complete': True, 'all12_inventory_actions_closed': all_closed,
                          'type_orbits': [o['type_orbit'] for o in orbits],
                          'all_original_rows': len(needed), 'all_original_rows_covered': result['all_original_owner_rows_covered'],
                          'conditionally_excluded_types': result['conditionally_excluded_types'],
                          'max_states': max_states, 'seconds': summary['elapsed_seconds'], 'mathematical_sha256': digest(result)}))
    except BaseException as exc:
        progress.update(error_type=type(exc).__name__, error=str(exc), active_case=active.receipt() if active else None)
        put(args.out / 'progress.json', progress)
        put(args.out / 'complete-closure-prefix.json', closure)
        put(args.out / 'complete-owner-row-prefix.json', row_receipts)
        raise


if __name__ == '__main__':
    main()
