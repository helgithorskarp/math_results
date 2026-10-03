"""Regenerate the entire selected inventory from 23 compact literal stars.

No prior owner list, prior colored key, graph, expected result, or private
checkpoint is an input. The two owner readers, two root-partition readers and
two colored readers use separate representations and decompositions.
"""
import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
from pathlib import Path
import resource
import time
from common import Budget, Guard, digest, encode, freeze, need, put, source_pins
import owner_bits
import owner_sets
import mate_bits
import mate_sets
import colored_bits
import colored_sets
import colored_verify


def child_guard(start):
    if time.monotonic() - start > 60:
        raise Guard('original60s inventory child')


def damage_controls(words, old, row):
    accepted = colored_verify.record(words, old, row)
    need(accepted, 'whole literal point-map positive control')
    rejected = []
    for label in ('missing_free_tail', 'Hub_role_swap', 'false_incidence_key'):
        bad = list(copy.deepcopy(row))
        if label == 'missing_free_tail':
            bad[3] = bad[3][1:]
        elif label == 'Hub_role_swap':
            values = list(bad[8])
            a, b = row[0][3][:2]
            values[a], values[b] = values[b], values[a]
            bad[8] = tuple(values)
        else:
            deficit, colors, rows = bad[7]
            hubmask, cells = rows[0]
            changed = list(cells)
            changed[0] = (changed[0][0], changed[0][1] + 1)
            bad[7] = (deficit, colors, ((hubmask, tuple(changed)),) + rows[1:])
        try:
            colored_verify.record(words, old, tuple(bad))
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('semantic original-row damage accepted: ' + label)
    return {'positive_full_point_map': True, 'rejected': rejected}


def fixture(index, out, start, progress):
    root, manifest = source_pins()
    raw = (root / 'fixtures.json').read_bytes()
    stars = json.loads(raw)['stars']
    need(len(stars) == 23 and isinstance(index, int) and 0 <= index < 23,
         'entire declared 23-star domain and one predetermined fixture')
    words = stars[index]
    progress['active_phase'] = 'all physical five-Hub placements'
    put(out / 'progress.json', progress)
    # One reader scans all C(17,5) Hub sets. The other scans every owned block,
    # mate point and two additional Hub points, without importing the first.
    A, counts, cap, marks = owner_bits.compile_fixture(words, index)
    B, other_cap, other_marks, other_coordinates = owner_sets.compile_fixture(words, index)
    need(encode(A) == encode(B), 'every original physical owner differs')
    need(cap == other_cap and encode(sorted(marks)) == encode(sorted(other_coordinates)),
         'entire physical propagation domain and coordinates differ')
    # JSON conversion reproduces the original record schema, including lists.
    owners = json.loads(encode(A))
    selected = [r for r in owners if r['delta'] == [0] * 5 and r['z'] == 0]
    put(out / 'selected-physical-owners.json', selected)
    child_guard(start)
    progress['active_phase'] = 'every selected named mate/free partition'
    put(out / 'progress.json', progress)
    P, n, ps = mate_bits.decode(words, owners, index)
    Q, m, qs = mate_sets.decode(words, owners, index)
    need(encode(P) == encode(Q) and n == m == len(selected) and ps == qs == 12 * n,
         'entire selected mate/free records and all 12 original role assignments')
    by_owner = defaultdict(list)
    for row in P:
        fi, hubs, mate, roles = row[0]
        by_owner[fi, tuple(hubs), mate].append(row)
    need(len(by_owner) == n and all(len(rows) == 12 for rows in by_owner.values()),
         'exactly every selected physical owner with all original named roles')
    progress['active_phase'] = 'complete original 12-field colored rows'
    put(out / 'progress.json', progress)
    branches, controls, all_rows = [], [], []
    with (out / 'complete-owner-records.jsonl').open('xb') as stream:
        for identity, source in sorted(by_owner.items()):
            child_guard(start)
            budget = Budget('entire selected original owner ' + str(identity))
            progress['active_original_owner'] = list(identity)
            progress['active_case_receipt'] = budget.receipt()
            put(out / 'progress.json', progress)
            X, xs = colored_bits.physical(words, source)
            Y, ys = colored_sets.physical(words, source)
            budget.tick(xs + ys)
            need(encode(X) == encode(Y), 'every complete colored row and original17-point map differs')
            role_source = {tuple(row[0][3]): row for row in source}
            for row in X:
                budget.tick()
                colored_verify.record(words, role_source[row[0][3]], row)
            if not controls:
                controls.append(damage_controls(words, role_source[X[0][0][3]], X[0]))
            branches.append({'original_owner': list(identity), 'all12_records_sha256': digest(X),
                             'producer_states': xs, 'oracle_states': ys,
                             'whole_validation_states': budget.states})
            all_rows.extend(X)
            stream.write(encode(X) + b'\n')
            stream.flush()
            progress['completed_physical_owners'] = len(branches)
            progress['completed_original_named_rows'] = len(all_rows)
            progress.pop('active_original_owner', None)
            progress.pop('active_case_receipt', None)
            put(out / 'progress.json', progress)
    mathematical = {
        'actual_agent': 'six-code-1', 'role': 'researcher', 'complete': True,
        'action': 'source_only_fixture_inventory', 'fixture': index,
        'literal23_input_sha256': hashlib.sha256(raw).hexdigest(),
        'all_physical_owners': len(owners), 'all_physical_owner_records_sha256': digest(owners),
        'selected_zero_Hub_z0_owners': n, 'all_original_named_rows': len(all_rows),
        'all_selected_physical_owner_records_sha256': digest(selected),
        'all_complete_colored_records_sha256': digest(all_rows),
        'all_original_owner_branches': branches, 'semantic_controls': controls,
        'original_named_role_count_per_physical_owner': 12,
        'source_only_input': True, 'prior_private_owner_or_key_input': False,
        'global_endpoint_change': False, 'reproduction_is_not_new_discovery': True,
    }
    child_guard(start)
    return mathematical


def aggregate(dirs, out, start, progress):
    root, manifest = source_pins()
    need(len(dirs) == 23 and len(set(dirs)) == 23, '23 distinct predetermined completed fixture directories')
    classes = defaultdict(list)
    witnesses = {}
    all_digest = hashlib.sha256(b'[')
    prior_identity = None
    named_count = physical_count = full_owner_count = 0
    free_deficits = Counter()
    branch_hashes = []
    source_fixture_hashes = []
    first = True
    for fi, directory in enumerate(dirs):
        child_guard(start)
        p = json.loads((directory / 'progress.json').read_bytes())
        math = json.loads((directory / 'mathematical-record.json').read_bytes())
        need(p['complete'] and math['complete'] and math['fixture'] == fi and
             digest(math) == p['mathematical_sha256'], 'entire completed original fixture binding')
        physical_count += math['selected_zero_Hub_z0_owners']
        full_owner_count += math['all_physical_owners']
        source_fixture_hashes.append(digest(math))
        per_fixture_rows = 0
        for line in (directory / 'complete-owner-records.jsonl').open('rb'):
            budget = Budget('entire original aggregate owner ' + str(fi) + '/' + str(per_fixture_rows))
            rows = json.loads(line)
            need(len(rows) == 12, 'whole original physical-owner group')
            identity = freeze(rows[0][0][:3])
            need(identity[0] == fi and (prior_identity is None or prior_identity < identity),
                 'all original physical owners in strict global order')
            prior_identity = identity
            branch_hashes.append(digest(rows))
            for row in rows:
                budget.tick()
                need(len(row) == 12 and freeze(row[0][:3]) == identity,
                     'entire original 12-field row and physical identity')
                k = freeze(row[7])
                free_deficits[k[0]] += 1
                if not classes[k]:
                    witnesses[k] = row[0]
                classes[k].append(named_count)
                if not first:
                    all_digest.update(b',')
                all_digest.update(encode(row))
                first = False
                named_count += 1
                per_fixture_rows += 1
        need(per_fixture_rows == math['all_original_named_rows'], 'entire original fixture-row coverage')
        progress['completed_fixture_indices'].append(fi)
        progress['completed_original_named_rows'] = named_count
        put(out / 'progress.json', progress)
    all_digest.update(b']')
    catalogue = [[k, len(classes[k]), witnesses[k], classes[k]] for k in sorted(classes)]
    put(out / 'decorated-classes.json', catalogue)
    mathematical = {
        'actual_agent': 'six-code-1', 'role': 'researcher', 'complete': True,
        'action': 'source_only_aggregate_inventory', 'original23_fixtures': len(dirs),
        'all_physical_T1_owners': full_owner_count,
        'selected_zero_Hub_z0_physical_owners': physical_count,
        'all_original_named_rows': named_count,
        'all_original_colored_classes': len(catalogue),
        'free_deficit_frequencies': sorted(free_deficits.items()),
        'D2_original_type_ids': [i for i, row in enumerate(catalogue) if row[0][0] == 2],
        'entire_original_named_record_list_sha256': all_digest.hexdigest(),
        'entire_original_decorated_classes_sha256': digest(catalogue),
        'all_original_physical_group_hashes_sha256': digest(branch_hashes),
        'all_source_fixture_mathematical_hashes': source_fixture_hashes,
        'literal_input_only': True, 'prior_private_owner_or_key_input': False,
        'normalization_and_selected_domain_bridges': 'ordinary unformalized',
        'independent_person_review': 'pending', 'global_endpoint_change': False,
        'reproduction_is_not_new_discovery': True,
    }
    child_guard(start)
    return mathematical


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=['fixture', 'aggregate'])
    ap.add_argument('--index', type=int)
    ap.add_argument('--fixtures', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    progress = {'actual_agent': 'six-code-1', 'role': 'researcher', 'complete': False,
                'status': 'INCOMPLETE_NOT_ABSENCE', 'completed_physical_owners': 0,
                'completed_original_named_rows': 0, 'completed_fixture_indices': []}
    put(args.out / 'progress.json', progress)
    try:
        if args.action == 'fixture':
            need(args.index is not None, 'fixed whole source fixture required')
            mathematical = fixture(args.index, args.out, start, progress)
        else:
            need(args.fixtures is not None, 'fixed whole fixture directory list required')
            dirs = [Path(p) for p in json.loads(args.fixtures.read_bytes())]
            mathematical = aggregate(dirs, args.out, start, progress)
        put(args.out / 'mathematical-record.json', mathematical)
        progress.update(complete=True, status='COMPLETE_SOURCE_ONLY_DECLARED_INVENTORY',
                        mathematical_sha256=digest(mathematical))
        put(args.out / 'progress.json', progress)
        summary = {'mathematical_record': mathematical, 'mathematical_sha256': digest(mathematical),
                   'elapsed_seconds': time.monotonic() - start,
                   'peak_rss_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        put(args.out / 'summary.json', summary)
        print(json.dumps({'complete': True, 'action': mathematical['action'],
                          'fixture': mathematical.get('fixture'),
                          'named_rows': mathematical['all_original_named_rows'],
                          'seconds': summary['elapsed_seconds'], 'peak_rss_KiB': summary['peak_rss_KiB'],
                          'mathematical_sha256': digest(mathematical)}))
    except BaseException as exc:
        progress.update(complete=False, status='INCOMPLETE_GUARD_OR_DISCREPANCY_NOT_ABSENCE',
                        error_type=type(exc).__name__, error=str(exc))
        put(args.out / 'progress.json', progress)
        raise


if __name__ == '__main__':
    main()
