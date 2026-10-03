"""Bind the locally regenerated whole second-route cover.

This is a final coverage/binding audit of completed independent mathematical
replays, not a replacement for those replays. No external cached array,
historical negative corpus or previously classified negative front is read.
Head/tail and selected-witness bookkeeping is credited to the author's prior
private freeze_complete.py; packed/scalar mathematics is separate.
"""
from collections import Counter
import hashlib
import json
import sys
from pathlib import Path
import time

from controls import operations_allow
from inputs import bound_path, checked_finite, digest, load, need, static_sources

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'
CEILING = 1 << 44
EVIDENCE = {}


def record(path):
    need(path.resolve().is_relative_to(ROOT), 'No external generated evidence allowed')
    raw = path.read_bytes()
    relative = str(path.relative_to(ROOT))
    EVIDENCE[relative] = {'path': relative, 'bytes': len(raw),
                          'sha256': hashlib.sha256(raw).hexdigest()}
    return json.loads(raw)


def read(name):
    return record(WORK / name)


def paired(base):
    n, o = (checked_finite(read(base + suffix + '.json')) for suffix in ('', '-O'))
    need(n['finite'] == o['finite'] and n['finite_sha256'] == o['finite_sha256'],
         'Entire normal/O finite records differ: ' + base)
    return n


def witness_partition(case, front):
    """Audit selected-domain bookkeeping, not a second scalar replay."""
    need(case['constant16_exceeds44'], 'An unresolved sufficient miss is not a negative')
    need(case['prefix_sha256'] == front['prefix_sha256'] and
         case['nine_core_sha256'] == front['nine_core_sha256'], 'Actual front binding differs')
    tags = set()
    mass = 0
    for witness in case['selected_witnesses']:
        low, high = witness['original_LOW_mask'], witness['original_HIGH_mask']
        original = witness['outer_record']
        need(low.bit_count() == high.bit_count() == 3 and low & high == 0 and
             low | high < 8192 and original[:2] == [low, high], 'Invalid immutable original clamp')
        need(witness['B7'] == 16 and witness['label'] == original[4] + original[5] + 16,
             'Unjustified seven-input floor or label')
        tag = tuple(original[2:4])
        need(tag not in tags, 'Duplicate selected current class')
        tags.add(tag)
        mass += 1 << witness['label']
    need(mass == case['selected_mass'] and mass > CEILING, 'Mass must be strictly above size44')
    return len(tags), mass


def controls(name, labels, key, preserved):
    result = checked_finite(read(name))
    rows = result['finite'][key]
    need(len(rows) == 6 and {(r['label'], r['optimized']) for r in rows} ==
         {(label, mode) for label in labels for mode in (False, True)} and
         all(r['rejected'] for r in rows) and result['finite'][preserved],
         'Incomplete intended semantic controls: ' + name)
    return result['finite_sha256']


def main(output_dir=None):
    operations_allow()
    started = time.monotonic()
    pins = static_sources()
    transport = read('transport-inputs.json')
    need(transport['all_inputs_regenerated_locally_from_static_source'], 'Locally generated input phase required')
    for key in transport['inputs']:
        record(bound_path(key))
    preparation, cuts = load('preparations'), load('cuts')
    prep_scalar, cut_scalar = paired('checked02'), paired('free-cut-independent-02-03')
    base, original = paired('base-checked'), paired('original-checked')
    seed, reserve = paired('reserve-seed-checked'), paired('reserve-preparations-checked')
    first_phase = checked_finite(read('phase-original-reserve-complete.json'))
    final_phase = checked_finite(read('phase-fronts-complete.json'))
    public_certificate = checked_finite(load('public_universal_certificate'))
    public_fixture = load('public_universal_fixture')
    public_ref = pins['public_universal_graph_ref']
    need(public_certificate['finite_sha256'] ==
         'a2faef8075c751886b467a5c2095ad79552e712b3b7ca29256715dd86fe6ed4e' and
         public_certificate['finite']['cold_source_only_complete'] and
         public_certificate['finite']['all8_semantic_damages_reject'], 'Cold public conditional-maximum replay differs')
    need(preparation['complete'] and preparation['queue_unexpanded'] == 0 and
         len(preparation['functions']) == 8351 and len(cuts['retained_function_ids']) == 5295,
         'Preparation closure incomplete')
    need(first_phase['finite']['cold_all_sources_and_original_inputs'] and
         first_phase['finite']['external_cached_arrays_used'] is False and
         first_phase['finite']['old_negative_corpus_used'] is False and
         first_phase['finite']['whole_preparation_scalar_finite_sha256'] == prep_scalar['finite_sha256'] and
         first_phase['finite']['whole_freecut_scalar_finite_sha256'] == cut_scalar['finite_sha256'] and
         first_phase['finite']['whole_original_HIGH_reserve_finite_sha256'] == seed['finite_sha256'] and
         first_phase['finite']['reserve_preparation_scalar_finite_sha256'] == reserve['finite_sha256'] and
         first_phase['finite']['original_scalar_cache_sha256'] == original['finite']['scalar_cache_sha256'] and
         final_phase['finite']['cold_input_phase_finite_sha256'] == first_phase['finite_sha256'] and
         final_phase['finite']['remaining_open_functions'] == 0,
         'Whole source-only original/preparation/front phase bindings differ')
    ids = cuts['retained_function_ids']
    classification = checked_finite(load('reserve_classifications'))
    rows = classification['classifications']
    need([row['retained_offset'] for row in rows] == list(range(5295)) and
         [row['function_id'] for row in rows] == ids and
         digest(rows) == classification['finite']['classification_sha256'] ==
         reserve['finite']['complete_classification_sha256'], 'Full immutable retained-domain partition differs')
    open_offsets = [row['retained_offset'] for row in rows if row['witness'] is None]
    closed_offsets = [row['retained_offset'] for row in rows if row['witness'] is not None]
    need(len(open_offsets) == 3197 and len(closed_offsets) == 2098 and
         digest(open_offsets) == reserve['finite']['remaining_retained_offsets_sha256'] and
         digest(closed_offsets) == reserve['finite']['excluded_retained_offsets_sha256'] and
         sorted(open_offsets + closed_offsets) == list(range(5295)), 'Full2098/3197 reserve partition differs')
    intervals = []
    processed = []
    counts, front_metrics, constant_metrics, extended_metrics = Counter(), Counter(), Counter(), Counter()
    negative_fronts = selected_originals = 0
    masses = []
    prefix = public_fixture['B23'] + public_fixture['LOW_suffix'] + public_fixture['prior_HIGH_merges']
    dead = preparation['dead_preparation_ports']
    canonical_tails = [[[6, 9], [10, 11], [9, 11]],
                       [[6, 10], [9, 11], [10, 11]],
                       [[6, 11], [9, 10], [10, 11]]]
    for first in range(0, 5295, 128):
        operations_allow()
        need(time.monotonic() - started < 45, 'Incomplete45s coverage audit: no new certificate')
        last = min(first + 128, 5295)
        stem = f'02-{first:05}-{last:05}'
        result = checked_finite(read('slice-complete' + stem + '.json'))
        finite = result['finite']
        offsets = [x for x in open_offsets if first <= x < last]
        selected_ids = [ids[x] for x in offsets]
        need(finite['retained_interval'] == [first, last] and
             finite['processed_previous_open_offsets'] == offsets and
             finite['HIGH_word'] == [[5, 6], [7, 10]] and
             finite['public_universal_graph_ref'] == public_ref and finite['imported_negative_count'] == 0,
             'Complete interval/route/dependency binding differs')
        front = read('fronts' + stem + '.json')
        front_finite = {k: v for k, v in front.items() if k not in
                        ('agent', 'role', 'status', 'survivors', 'rejections', 'finite_sha256',
                         'seconds', 'maximum_rss_kib', 'scope')}
        need(digest(front_finite) == front['finite_sha256'] == finite['producer_front_finite_sha256'] and
             digest(front['survivors']) == front['survivors_sha256'] and
             digest(front['rejections']) == front['rejections_sha256'] and
             front['retained_function_ids'] == selected_ids and
             digest(selected_ids) == finite['retained_function_ids_sha256'] and
             front['preparation_functions_sha256'] == preparation['full_functions_sha256'] and
             front['preparation_cut_classification_sha256'] == cuts['classification_sha256'],
             'Whole actual front/cut/function arrays differ')
        checked = paired('check' + stem)
        need(checked['finite_sha256'] == finite['scalar_front_finite_sha256'] and
             checked['finite']['producer_front_sha256'] == front['finite_sha256'] and
             checked['finite']['retained_function_ids'] == selected_ids and
             checked['finite']['processed_previous_open_offsets'] == offsets and
             checked['finite']['census'] == front['census'] == finite['front_census'] and
             checked['finite']['remaining_gate_budgets'] == front['remaining_gate_budgets'] ==
             finite['remaining_gate_budgets'], 'Scalar full-front replay binding differs')
        head_rejects, tail_records = {}, {}
        for row in front['rejections']:
            key = (row['function_id'], tuple(row['singleton']))
            need(row['function_id'] in selected_ids and row['singleton'] in [[p, 9] for p in dead],
                 'Extraneous rejected head')
            if row['stage'] == 'HEAD':
                need(key not in head_rejects, 'Duplicate rejected head')
                head_rejects[key] = row
            else:
                tail_key = key + (row['tail_id'],)
                need(row['stage'] == 'TAIL' and 0 <= row['tail_id'] < 3 and
                     tail_key not in tail_records and row['HIGH_tail'] == canonical_tails[row['tail_id']],
                     'Duplicate or wrong necessary tail rejection')
                if row['kind'] == 'PUBLIC_CONDITIONAL_MAXIMUM_OBSTRUCTION':
                    columns = preparation['functions'][row['function_id']]['full_six_variable_columns']
                    value = sum(((col >> 24) & 1) << j for j, col in enumerate(columns))
                    chosen = next(p for p in public_fixture['candidate_head_ports']
                                  if not (value >> dead.index(p) & 1))
                    need(row['F24'] == value and row['chosen_head_port'] == chosen == row['singleton'][0] and
                         row['public_universal_graph_ref'] == public_ref and
                         row['HIGH_tail'] == public_fixture['canonical_tail'],
                         'Public one-head lemma is not applicable')
                tail_records[tail_key] = row
        for row in front['survivors']:
            key = (row['function_id'], tuple(row['singleton']), row['tail_id'])
            need(key not in tail_records and row['function_id'] in selected_ids and
                 row['singleton'] in [[p, 9] for p in dead] and 0 <= row['tail_id'] < 3 and
                 row['HIGH_tail'] == canonical_tails[row['tail_id']], 'Duplicate or extraneous actual front')
            word = preparation['functions'][row['function_id']]['shortest_word']
            literal = prefix + word + [row['singleton']] + row['HIGH_tail']
            need(row['preparation_word'] == word and row['prefix'] == literal and
                 row['prefix_length'] == len(literal) and row['remaining_gate_budget'] == 44 - len(literal) and
                 row['prefix_sha256'] == digest(literal) and
                 row['nine_core_sha256'] == digest(row['nine_core_states']), 'Actual front word/image/budget differs')
            tail_records[key] = row
        audited_counts = Counter(eligible_preparation_functions=len(selected_ids),
                                  candidate_singleton_heads=6 * len(selected_ids))
        for fid in selected_ids:
            for p in dead:
                key = (fid, (p, 9))
                if key in head_rejects:
                    need(all(key + (t,) not in tail_records for t in range(3)), 'Rejected head also has a tail')
                    audited_counts['head_' + head_rejects[key]['kind']] += 1
                else:
                    audited_counts['active_uncut_singleton_heads'] += 1
                    for t in range(3):
                        need(key + (t,) in tail_records, 'One necessary full tail function is missing')
                        audited_counts['candidate_complete_tail_functions'] += 1
                        row = tail_records[key + (t,)]
                        if row.get('stage') == 'TAIL':
                            audited_counts['tail_' + row['kind']] += 1
                        else:
                            audited_counts['surviving_complete_fronts'] += 1
        need(audited_counts == Counter(front['census']), 'Complete head/tail census differs')
        kernel = read('kernels' + stem + '.json')
        expected_kernel = [{'front_index': i, 'prefix_sha256': row['prefix_sha256'],
                            'status': 'NO_IMPORTED_NEGATIVE_ASSUMED_DIRECT_CONSTANT_FIRST'}
                           for i, row in enumerate(front['survivors'])]
        need(kernel['classifications'] == expected_kernel and kernel['finite'] == {
            'producer_front_sha256': front['finite_sha256'], 'classifications_sha256': digest(expected_kernel),
            'imported_negative_count': 0}, 'Unjustified imported negative in new residual cover')
        proposal = checked_finite(read('constant' + stem + '.json'))
        cases = proposal['cases']
        need(digest(cases) == proposal['cases_sha256'] == finite['complete_constant_cases_sha256'] ==
             proposal['finite']['cases_sha256'] and
             proposal['finite']['producer_front_sha256'] == front['finite_sha256'] and
             proposal['finite']['kernel_classifications_sha256'] == digest(expected_kernel) and
             [r['front_index'] for r in cases] == list(range(len(front['survivors']))),
             'Full constant case partition differs')
        positive, misses = [], []
        for i, case in enumerate(cases):
            need(case['prefix_sha256'] == front['survivors'][i]['prefix_sha256'] and
                 case['nine_core_sha256'] == front['survivors'][i]['nine_core_sha256'],
                 'Preserved positive/miss case is assigned to a different front')
            if case['constant16_exceeds44']:
                positive.append(i)
                selected, mass = witness_partition(case, front['survivors'][i])
                selected_originals += selected
                masses.append(mass)
            else:
                misses.append(i)
        need(misses == finite['unresolved_front_indices'] == proposal['finite']['inconclusive_front_indices'] and
             len(positive) == finite['actual_negatives'] and len(misses) == finite['unresolved_sufficient_misses'] and
             digest(positive) == finite['negative_front_indices_sha256'], 'Positive/miss partition differs')
        scalar_census, scalar_metrics = Counter(), Counter()
        expected_slices = [[i, min(i + 1000, len(cases))] for i in range(0, len(cases), 1000)]
        need([r['case_interval'] for r in finite['constant_scalar_slices']] == expected_slices,
             'Incomplete scalar case interval cover')
        for meta, (lo, hi) in zip(finite['constant_scalar_slices'], expected_slices):
            checked_cases = paired(f'constant-check{stem}-{lo:05}-{hi:05}')
            sf = checked_cases['finite']
            slice_positive = [[i, cases[i]['selected_mass']] for i in positive if lo <= i < hi]
            slice_occurrences = sum(len(cases[i]['selected_witnesses']) for i, _ in slice_positive)
            need(checked_cases['finite_sha256'] == meta['finite_sha256'] and sf['case_slice'] == [lo, hi] and
                 sf['complete_case_certificate_sha256'] == proposal['cases_sha256'] and
                 sf['complete_front_cover_sha256'] == front['finite_sha256'] and
                 sf['root_masses_sha256'] == digest(slice_positive) and
                 sf['census'].get('independently_constant16_excluded_cases', 0) == len(slice_positive) and
                 sf['census'].get('selected_outer_occurrences', 0) == slice_occurrences and
                 sf['census'].get('inconclusive_preserved_open', 0) == sum(lo <= i < hi for i in misses) and
                 sf['metrics']['outer_free_assignments'] == 128 * slice_occurrences,
                 'Whole scalar original-domain replay or mass binding differs')
            scalar_census.update(sf['census'])
            scalar_metrics.update(sf['metrics'])
        need(scalar_census == Counter(finite['constant_scalar_census']) and
             scalar_metrics == Counter(finite['constant_scalar_metrics_normal']), 'Constant cumulative metrics differ')
        extension = None
        if misses:
            extended = checked_finite(read(f'extended-{first:05}-{last:05}.json'))
            ef = extended['finite']
            need(ef['actual_genuine_miss_front_indices'] == misses and
                 ef['actual_complete_front_sha256'] == front['finite_sha256'] and
                 ef['old_constant_cases_sha256'] == proposal['cases_sha256'] and
                 ef['extended_cases_sha256'] == digest(extended['cases']) and
                 [r['front_index'] for r in extended['cases']] == misses and
                 ef['remaining_open_indices'] == [] and ef['imported_negative_corpus_count'] == 0,
                 'Extended-original repairs do not cover all actual sufficient misses')
            checked_extended = paired(f'extended-check-{first:05}-{last:05}')
            sf = checked_extended['finite']
            root_masses = []
            occurrences = 0
            for case in extended['cases']:
                index = case['front_index']
                need(case['original99_class_mass'] == cases[index]['whole99_class_mass'] and
                     case['function_id'] == front['survivors'][index]['function_id'],
                     'Extension is not for the same genuine original-pool miss')
                selected, mass = witness_partition(case, front['survivors'][index])
                occurrences += selected
                masses.append(mass)
                root_masses.append([index, mass])
            need(sf['entire_case_front_indices'] == misses and sf['extended_cases_sha256'] == digest(extended['cases']) and
                 sf['actual_complete_front_sha256'] == front['finite_sha256'] and sf['remaining_open_indices'] == [] and
                 sf['independently_positive_cases'] == len(misses) == ef['positive_count'] and
                 sf['selected_original_occurrences'] == occurrences and sf['root_masses_sha256'] == digest(root_masses) and
                 sf['metrics']['outer_free_assignments'] == 128 * occurrences,
                 'Full extended scalar replay/mass partition differs')
            extended_metrics.update(sf['metrics'])
            selected_originals += occurrences
            extension = {'actual_miss_indices': misses, 'proposal_finite_sha256': extended['finite_sha256'],
                         'scalar_finite_sha256': checked_extended['finite_sha256'],
                         'selected_original_occurrences': occurrences,
                         'minimum_selected_mass': sf['minimum_selected_mass'],
                         'actual_tested_original_pair_counts': [r['tested_original_pairs'] for r in extended['cases']]}
        negative_fronts += len(cases)
        counts.update(audited_counts)
        constant_metrics.update(scalar_metrics)
        front_metrics.update(checked['finite']['metrics'])
        processed.extend(offsets)
        intervals.append({'retained_interval': [first, last], 'previous_open_functions': len(offsets),
                          'slice_finite_sha256': result['finite_sha256'],
                          'front_finite_sha256': front['finite_sha256'],
                          'scalar_front_finite_sha256': checked['finite_sha256'],
                          'constant_positive_fronts': len(positive), 'extended_positive_fronts': len(misses),
                          'complete_residual_fronts': len(cases), 'extension': extension})
    need(processed == open_offsets and len(intervals) == 42 and
         counts['tail_PUBLIC_CONDITIONAL_MAXIMUM_OBSTRUCTION'] == len(open_offsets),
         'Complete3197-function coverage is missing or duplicated')
    phase_intervals = final_phase['finite']['complete_front_intervals']
    need([r['retained_interval'] for r in phase_intervals] == [r['retained_interval'] for r in intervals] and
         [r['slice_finite_sha256'] for r in phase_intervals] == [r['slice_finite_sha256'] for r in intervals] and
         [r['functions'] for r in phase_intervals] == [r['previous_open_functions'] for r in intervals],
         'Final serial phase differs from entire actual front cover')
    for row, meta in zip(intervals, phase_intervals):
        if row['extension'] is None:
            need(meta['extension'] is None, 'Extraneous extended-front phase')
        else:
            need(meta['extension']['actual_indices'] == row['extension']['actual_miss_indices'] and
                 meta['extension']['scalar_finite_sha256'] == row['extension']['scalar_finite_sha256'],
                 'Actual extended-front phase differs')
    base_controls = controls('controls-00000-00128.json',
                             ('actual_nonzero_head', 'omitted_actual_tail_front', 'unjustified_larger_constant'),
                             'semantic_rejections', 'valid_original_proposals_unchanged')
    extended_controls = controls('extended-controls-05120-05248.json',
                                 ('false_original_deletion', 'duplicate_actual_current_class', 'genuine_equal_mass_not_strict'),
                                 'records', 'valid_original_proposal_bytes_preserved')
    need(read('extended-controls-05120-05248.json')['finite']['genuine_equality_mass'] == CEILING,
         'Strict boundary control is not a genuine equality fixture')
    reserve_controls = read('reserve-controls.json')
    control_rows = reserve_controls['controls']
    need(len(control_rows) == 4 and {(r['damage'], r['optimized']) for r in control_rows} ==
         {(label, mode) for label in ('false-future-depth', 'actual-active-original') for mode in (False, True)} and
         all(r['returncode'] != 0 and r['superficial_bindings_repaired'] for r in control_rows) and
         reserve_controls['positive_scalar_finite_sha256'] == reserve['finite_sha256'] and
         reserve_controls['original_classification_bytes_unchanged'], 'Incomplete actual reserve controls')
    control_finite = {k: v for k, v in reserve_controls.items() if k not in ('seconds', 'controls')}
    control_finite['controls'] = [{k: v for k, v in row.items() if k != 'seconds'} for row in control_rows]
    dependency_record = record(ROOT / 'DEPENDENCIES.json')
    stages = read('run-stages.json')
    need(stages and all(row['returncode'] == 0 for row in stages), 'One preserved serial phase is incomplete')
    finite = {'HIGH_word': [[5, 6], [7, 10]], 'literal_LOW_suffix': public_fixture['LOW_suffix'],
              'full_preparation_functions': 8351, 'absorbing_minimum_locks': 2143,
              'further_original_pivot3_cuts': 913, 'retained_preparation_functions': 5295,
              'preparation_functions_sha256': preparation['full_functions_sha256'],
              'preparation_cut_classification_sha256': cuts['classification_sha256'],
              'base_scalar_finite_sha256': base['finite_sha256'],
              'original_scalar_finite_sha256': original['finite_sha256'],
              'preparation_scalar_finite_sha256': prep_scalar['finite_sha256'],
              'whole_original_cut_scalar_finite_sha256': cut_scalar['finite_sha256'],
              'original_HIGH_seed_scalar_finite_sha256': seed['finite_sha256'],
              'original_HIGH_reserve_scalar_finite_sha256': reserve['finite_sha256'],
              'cold_seed_phase_finite_sha256': first_phase['finite_sha256'],
              'cold_front_phase_finite_sha256': final_phase['finite_sha256'],
              'original_HIGH_reserve_excluded_functions': 2098,
              'complete_front_covered_preparation_functions': len(processed),
              'all_retained_preparation_functions_excluded': 5295, 'remaining_open_preparation_functions': 0,
              'complete_front_processed_retained_offsets_sha256': digest(processed),
              'all_excluded_retained_offsets_sha256': digest(list(range(5295))),
              'complete_front_intervals': intervals, 'front_census': dict(counts),
              'front_scalar_metrics_normal': dict(front_metrics),
              'complete_residual_front_negatives': negative_fronts,
              'original99_constant16_front_negatives': sum(r['constant_positive_fronts'] for r in intervals),
              'extended_original_constant16_front_negatives': sum(r['extended_positive_fronts'] for r in intervals),
              'selected_original_occurrences': selected_originals,
              'constant_scalar_metrics_normal': dict(constant_metrics),
              'extended_scalar_metrics_normal': dict(extended_metrics),
              'minimum_positive_mass': min(masses), 'size44_mass_ceiling': CEILING,
              'public_primitive_code_origin_commit': pins['public_primitive_source_commit'],
              'public_universal_source_commit': pins['public_universal_source_commit'],
              'public_universal_graph_ref': public_ref, 'mathematical_dependencies': dependency_record,
              'normal_O_entire_records_equal': True, 'imported_negative_corpus_count': 0,
              'base_controls_finite_sha256': base_controls, 'extended_controls_finite_sha256': extended_controls,
              'reserve_control_finite_sha256': digest(control_finite),
              'all24_semantic_rejections': True,
              'actual_preparation_word_length_bound_assumed': False, 'suffix_depth_bound_assumed': False,
              'whole_scoped_branch_exclusion_author_checked': True,
              'cold_source_only_whole_route_mathematical_reproduction_complete': True,
              'external_cached_arrays_used': False, 'external_person_review_complete': False,
              'formalized': False, 'unrestricted_size44_exclusion_claimed': False,
              'remaining_other_disjoint_two_prior_routes': 13}
    source_files = sorted(p for p in ROOT.rglob('*') if p.is_file() and
                          'work' not in p.relative_to(ROOT).parts and
                          '__pycache__' not in p.relative_to(ROOT).parts and
                          p not in (ROOT/'WORK_IN_PROGRESS.json', ROOT/'source-manifest.json', ROOT/'certificate.json', ROOT/'universal/source-manifest.json', ROOT/'universal/certificate.json'))
    source_rows = [{'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
                    'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in source_files]
    evidence_rows = sorted(EVIDENCE.values(), key=lambda row: row['path'])
    manifest = {'agent': 'six-sorting-1', 'role': 'researcher', 'files': source_rows,
                'files_sha256': digest(source_rows), 'generated_evidence': evidence_rows,
                'generated_evidence_sha256': digest(evidence_rows), 'source_commit': None, 'graph_ref': None,
                'scope': 'All mathematical work locally regenerated; generated arrays/logs remain private.'}
    certificate = {'agent': 'six-sorting-1', 'role': 'researcher',
                   'status': 'COMPLETE_COLD_WHOLE_SECOND_SCOPED_ROUTE_AUTHOR_CERTIFICATE',
                   'finite': finite, 'finite_sha256': digest(finite),
                   'source_manifest_files_sha256': manifest['files_sha256'],
                   'generated_evidence_sha256': manifest['generated_evidence_sha256'],
                   'remaining_open_retained_offsets': [], 'cached_verified_external_inputs_used': False,
                   'source_commit': None, 'graph_ref': None,
                   'scope': 'First strict ordinary two-HIGH mass increase SINGLETON, preceded by exactly equal disjoint(5,6)/(7,10) at literal P26; either order, arbitrary preparations/suffix depth.'}
    destination = ROOT if output_dir is None else ROOT / output_dir
    need(destination.resolve().is_relative_to(ROOT), 'Audit output outside standalone directory')
    destination.mkdir(parents=True, exist_ok=True)
    for name, value in (('source-manifest.json', manifest), ('certificate.json', certificate)):
        path = destination / name
        payload = json.dumps(value, indent=2) + '\n'
        need(not path.exists() or path.read_text() == payload, 'Refusing to overwrite changed frozen artifact: ' + name)
        path.write_text(payload)
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher', 'status': certificate['status'],
                      'finite_sha256': certificate['finite_sha256'], 'all_retained_functions_excluded': 5295,
                      'complete_residual_front_negatives': negative_fronts,
                      'original99_constant16_front_negatives': finite['original99_constant16_front_negatives'],
                      'extended_original_constant16_front_negatives': finite['extended_original_constant16_front_negatives'],
                      'minimum_positive_mass': min(masses), 'source_files': len(source_rows),
                      'source_bytes': sum(r['bytes'] for r in source_rows), 'evidence_files': len(evidence_rows),
                      'seconds': time.monotonic() - started}, indent=2))


if __name__ == '__main__':
    need(len(sys.argv) in (1, 3) and (len(sys.argv) == 1 or sys.argv[1] == '--output-dir'), 'Use optional --output-dir local/path')
    main(sys.argv[2] if len(sys.argv) == 3 else None)
