#!/usr/bin/env python3
"""Reconstruct all4 models and the complete input cover, then check all traces."""
import argparse
import hashlib
import json
import os
import platform
import resource
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_SHA256 = '79df26ebf2ed2066aceb60ecac24f6aa3353fba1e38cb636c5136b0ab2564afa'
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, record):
    path.write_text(json.dumps(record, indent=2) + '\n')


def run(command, seconds):
    r = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                       env=ENV, timeout=seconds)
    need(r.returncode == 0, 'Child failed: ' + r.stdout + r.stderr)
    return r.stdout


def pin(path, spec):
    need(sha(path) == spec['sha256'], 'Byte-pinned imported source changed')


def sources(work, specs):
    work.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name, spec in specs.items():
        path = work / spec['filename']
        if not path.exists():
            with urllib.request.urlopen(spec['url'], timeout=20) as response:
                path.write_bytes(response.read())
        pin(path, spec)
        paths[name] = path
    converter = work / 'drat-trim'
    if not converter.exists():
        run(['cc', '-O2', '-std=c99', paths['drat_converter'], '-o', converter], 20)
    # Conversion is untrusted, including an executable reused through --tools.
    paths['converter_executable'] = converter
    return paths


def main(args):
    started = time.monotonic()
    need(platform.python_version() == '3.11.2', 'Validated runtime is Python3.11.2')
    manifest = ROOT / 'expected.json'
    need(sha(manifest) == EXPECTED_SHA256, 'Frozen expectations changed')
    expected = json.loads(manifest.read_text())
    need(sha(ROOT / 'cover.json') == expected['cover_sha256'], 'Input cover changed')
    need(args.fresh_case is None or args.resume_dir is not None,
         '--fresh-case supplements --resume-dir; without resume all cases are fresh')
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    paths = sources((args.tools or work / 'tools').resolve(), expected['sources'])
    common, checker = paths['common_checker'], paths['RUP_checker']
    try:
        pin(checker, dict(expected['sources']['RUP_checker'], sha256='0' * 64))
    except ValueError:
        pass
    else:
        raise ValueError('Changed RUP checker pin accepted')

    # Both fresh child processes reconstruct the common actual cyclic relation
    # once, then compare every distinct signed word. No old literal frontend.
    families, smalls, guards = [], [], []
    for name, flags in (('normal', []), ('optimized', ['-O'])):
        directory = work / name
        run([sys.executable, *flags, ROOT / 'audit_family.py', '--cover', ROOT / 'cover.json',
             '--helper', common, '--work', directory], 35)
        family = json.loads((directory / 'family-audit.json').read_text())
        family.pop('seconds', None)
        need(family['coverage'] == expected['coverage'], 'Incomplete input cover')
        need(len(family['cases']) == len(expected['cases']) == 4, 'Incomplete model family')
        for actual, wanted in zip(family['cases'], expected['cases']):
            need(actual['number'] == wanted['number'] and actual['model'] == wanted['model'],
                 'Frozen field/signed-word model changed')
            need(actual['audit'] == {**wanted['model'],
                                    **expected['common_actual_cyclic_audit_details']},
                 'Independent actual-cyclic model differs')
        need(family['literal_unit_inputs_checked'] == expected['literal_unit_inputs_checked'] and
             family['positive_literal_unit_words'] == expected['positive_literal_unit_words'] and
             family['common_actual_cyclic_pairs_checked'] == 381306 and
             family['all_models_free_bits'] == [88,88,86,86] and family['production_damages_rejected'] == 20, 'Incomplete signed-unit domain')
        tiny = json.loads(run([sys.executable, *flags, ROOT / 'controls.py', '--helper', common,
                              '--work', work / ('controls-' + name)], 35))
        need(tiny == expected['controls'], 'Complete small controls changed')
        source = json.loads(run([sys.executable, *flags, ROOT / 'source_controls.py',
                                '--cover', ROOT / 'cover.json'], 25))
        need(source == expected['source_controls'], 'Source damage guards changed')
        save(work / ('small-' + name + '.json'), tiny)
        save(work / ('source-controls-' + name + '.json'), source)
        families.append(family)
        smalls.append(tiny)
        guards.append(source)
        print(json.dumps({'stage': name + '_all_models_cover_and_controls_checked'}), flush=True)
    need(families[0] == families[1] and smalls[0] == smalls[1] and guards[0] == guards[1],
         'Source differs under Python -O')
    for case in expected['cases']:
        name = 'case-' + str(case['number']) + '.cnf'
        need((work / 'normal' / name).read_bytes() == (work / 'optimized' / name).read_bytes(),
             'CNF bytes differ under -O')

    verified = []
    proof_controls = None
    for case in expected['cases']:
        number = case['number']
        cnf = work / 'normal' / ('case-' + str(number) + '.cnf')
        lrat = cnf.with_suffix('.lrat')
        cached = args.resume_dir is not None and number != args.fresh_case
        native = None
        if cached:
            candidate = args.resume_dir / lrat.name
            need(candidate.is_file(), 'Missing untrusted cached candidate')
            shutil.copyfile(candidate, lrat)
        else:
            native = json.loads(run([sys.executable, paths['native_driver'], '--solve', cnf], 35))
            save(work / ('case-' + str(number) + '-native.json'), native)
            need(native['status'] == 'UNSAT_PENDING_CHECK',
                 'Incomplete native proposal: stop, no exclusion or retry')
            need(sha(cnf.with_suffix('.drat')) == case['drat_sha256'], 'Fresh DRAT bytes differ')
            conversion = run([paths['converter_executable'], cnf, cnf.with_suffix('.drat'),
                              '-t', '25', '-L', lrat], 30)
            (work / ('case-' + str(number) + '-conversion.log')).write_text(conversion)
        need(sha(lrat) == case['proof']['proof_sha256'], 'Candidate LRAT bytes differ')
        proofs, damages = [], []
        for name, flags in (('normal', []), ('optimized', ['-O'])):
            proof = json.loads(run([sys.executable, *flags, checker, cnf, lrat], 50))
            save(work / ('case-' + str(number) + '-proof-' + name + '.json'), proof)
            proof.pop('seconds', None)
            need(proof == case['proof'] and proof['mathematical_exclusion'],
                 'Missing strict positive-RUP checked refutation')
            proofs.append(proof)
            if number == 1:
                damage = json.loads(run([sys.executable, *flags, paths['proof_controls'],
                                         '--checker', checker, '--cnf', cnf, '--lrat', lrat], 50))
                need(damage == expected['proof_controls'], 'Strict proof guards changed')
                damages.append(damage)
        need(proofs[0] == proofs[1], 'Strict proof differs under -O')
        if number == 1:
            need(damages[0] == damages[1], 'Strict proof controls differ under -O')
            proof_controls = damages[0]
        verified.append({'number': number, 'strict_proof_per_mode': proofs[0],
                         'cached_candidate_untrusted': cached, 'native_proposal': native})
        save(work / 'progress.json', {'complete_negative_family': False,
                                     'strictly_refuted_classes': len(verified), 'cases': verified})
        print(json.dumps({'stage': 'strict_normal_and_optimized_refutations_checked',
                          'case': number, 'cached_candidate_untrusted': cached}), flush=True)
    need(len(verified) == 4, 'Incomplete refutation family')
    additions = sum(x['strict_proof_per_mode']['checked_additions'] for x in verified)
    hints = sum(x['strict_proof_per_mode']['propagation_hints_checked'] for x in verified)
    need((additions, hints) == (97664, 2486245), 'Complete strict proof totals changed')
    result = {'agent': 'six-vdw-3', 'role': 'researcher',
              'status': 'MATCHED_FIVE_SEED_THREE_SATELLITE_RULE_AUTHOR_CHECKED',
              'complete_negative_family': True, 'refuted_classes': 4,
              'complete_four_head_local_inputs_excluded_both_palettes': 20,
              'first_residual_profile_excluded': True,
              'mono_five_forces_opposite_at52_54_or55_with_cited_dependencies': True,
              'mathematical_dependencies': json.loads((ROOT / 'cover.json').read_text())['mathematical_dependencies'],
              'expected_sha256': EXPECTED_SHA256, 'cover_sha256': expected['cover_sha256'],
              'checked_additions_per_mode': additions, 'propagation_hints_per_mode': hints,
              'actual_cyclic_pairs_audited_per_mode': 381306, 'other_regular_bits_free_each': [88,88,86,86],
              'literal_unit_inputs_per_mode': 20480, 'positive_literal_unit_words_per_mode': 4,
              'small_anchored_inputs_per_mode': smalls[0]['anchored_orientation_inputs'],
              'small_positive_words_per_mode': smalls[0]['positive_partial_words'],
              'model_damages_rejected_per_mode': smalls[0]['model_damages_rejected'],
              'complete_q7_pair_inputs_per_mode': 128, 'q7_consistent_fixed_inputs_per_mode': 2,
              'source_controls_per_mode': guards[0], 'production_model_damages_per_mode':20, 'proof_controls_per_mode': proof_controls,
              'changed_checker_pin_rejected': True,
              'cached_candidates_strictly_checked': sum(x['cached_candidate_untrusted'] for x in verified),
              'fresh_native_proposals': sum(x['native_proposal'] is not None for x in verified),
              'fresh_native_case_numbers': [x['number'] for x in verified if x['native_proposal'] is not None],
              'global_colorings_counted': False, 'full_deleted_robustness_proved': False,
              'length3704_coloring_found': False, 'W_bound_improved': False,
              'earlier_UNKNOWN_instances_not_retried': True, 'existing_resource_caps_unchanged': True,
              'all_threads': 1, 'max_CPU_intensive_jobs': 1, 'native_external_seconds': 35,
              'native_conflict_budget': 100000, 'converter_internal_seconds': 25,
              'converter_external_seconds': 30, 'strict_replay_external_seconds': 50,
              'child_peak_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'pipeline_seconds': time.monotonic() - started}
    save(work / 'verification.json', result)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--tools', type=Path)
    p.add_argument('--resume-dir', type=Path)
    p.add_argument('--fresh-case', type=int, choices=range(1, 5))
    main(p.parse_args())
