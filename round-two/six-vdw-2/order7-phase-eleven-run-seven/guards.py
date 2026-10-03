"""Whole physical/cover/provenance and strict RUP rejection probes before native work."""
import argparse
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from common import BASE, PUBLIC, ROOT, pins, require, sha
import audit

ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
           BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')

def main(work, output):
    began = time.monotonic(); dependency = pins(); pins()
    require(not output.exists(), 'fresh damage-output workspace required'); output.mkdir(parents=True)
    models = json.loads((work / 'models.json').read_text()); audit.validate_cover(models)
    slots, supports = audit.literal_field(); tests = []; references = {}
    for original in models['records'][:2]:
        cnf = work / (original['stem']+'.cnf')
        audit.audit_case(original, cnf, slots, supports)
        references[original['stem']] = copy.deepcopy(original), cnf.read_text(), audit.Counter(audit.read_cnf(cnf))
    def reject(label, function):
        try:
            function()
        except (ValueError, KeyError, IndexError, TypeError):
            tests.append(label); return
        raise ValueError('damage accepted: '+label)
    def check_cached(record, cnf):
        require(record['stem'] in references, 'unknown independently audited case')
        expected, text, whole_rows = references[record['stem']]
        expected = copy.deepcopy(expected); expected['cnf_sha256'] = sha(cnf)
        require(record == expected, 'changed independently audited whole metadata')
        require(audit.Counter(audit.read_cnf(cnf)) == whole_rows, 'changed independently audited ENTIRE signed CNF')
    def rejected(label, record, text):
        path = output / 'damaged.cnf'; path.write_text(text); record['cnf_sha256'] = sha(path)
        reject(label, lambda: check_cached(record, path))
    def change(label, function, index=0):
        record = copy.deepcopy(models['records'][index]); function(record)
        rejected(label, record, (work / (models['records'][index]['stem']+'.cnf')).read_text())
    changes = [
        ('wrong-gap-index', lambda r:r.update(gap_index=1)),
        ('wrong-gap-order', lambda r:r['background_gaps'].reverse()),
        ('wrong-gap-sum', lambda r:r['background_gaps'].__setitem__(0, 6)),
        ('wrong-b0', lambda r:r.update(background=1)),
        ('wrong-phase-K', lambda r:r.update(phase_K=10)),
        ('wrong-minority-count', lambda r:r.update(minority_count=10)),
        ('wrong-fixed-phase', lambda r:r['phase'].__setitem__(0, 0)),
        ('missing-fixed-phase', lambda r:r['phase'].pop()),
        ('wrong-normalized-run', lambda r:r.update(normalized_minority_run=list(range(1, 8)))),
        ('wrong-run-profile', lambda r:r.update(minority_run_lengths=[7, 2, 1, 1])),
        ('wrong-background-runs', lambda r:r.update(background_run_count=4)),
        ('nonunique-longest', lambda r:r.update(unique_longest_minority_run=False)),
        ('wrong-longest', lambda r:r.update(maximum_minority_run=6)),
        ('isolated-background-max4', lambda r:r.update(maximum_background_run=4)),
        ('introduced-phase-variable', lambda r:r.update(phase_variables=1)),
        ('identified-lower-colors', lambda r:r.update(lower_orientation_variables=11)),
        ('less-than44-independent-lower', lambda r:r.update(independent_lower_colors_before_palette_gauge=43)),
        ('wrong-field-count', lambda r:r.update(physical_field_clauses=r['physical_field_clauses']-1)),
        ('wrong-color-count', lambda r:r.update(universal_color_clauses=r['universal_color_clauses']-1)),
        ('wrong-new-color-count', lambda r:r.update(new_universal_color_clauses=r['new_universal_color_clauses']+1)),
        ('wrong-palette-gauge', lambda r:r.update(gauge_clauses=[[1]])),
        ('extra-lower-gauge', lambda r:r.update(gauge_clauses=[[-1], [-2]])),
        ('false-only-global-gauge', lambda r:r.update(only_global_y0_zero=False)),
        ('missing-root3', lambda r:r.update(root3_color_cut=False)),
        ('missing-root57', lambda r:r.update(root57_color_cut=False)),
        ('missing-phase8', lambda r:r.update(nonconstant_phase8_checked=False)),
        ('unjustified-phase8-row', lambda r:r.update(phase8_residual_clauses=1)),
        ('transferred-isolated-gap4', lambda r:r.update(isolated_eleven_gap4_rule_used=True)),
        ('transferred-TEN', lambda r:r.update(exact_TEN_rules_used=True)),
        ('numerical-adjacency-cut', lambda r:r.update(prior_adjacent_rule_used_as_numerical_cut=True)),
        ('circular-run7-cut', lambda r:r.update(proposed_run7_exclusion_used=True)),
        ('foreign-family-cut', lambda r:r.update(unrelated_family_cut=True)),
        ('unpublished-cut', lambda r:r.update(unpublished_exclusion_used_as_input=True)),
        ('wrong-parent-ref', lambda r:r.update(prior_adjacent_ref='changed')),
        ('wrong-source-commit', lambda r:r.update(source_commit='changed')),
        ('unsupported-negative-flag', lambda r:r.update(mathematical_exclusion=True)),
    ]
    for label, function in changes:
        change(label, function)
    change('wrong-b1', lambda r:r.update(background=0), 1)
    for index in (0, 1):
        original = models['records'][index]; lines = (work / (original['stem']+'.cnf')).read_text().splitlines()
        field, color = audit.semantic_rows(slots, supports, original['phase'])
        parsed = [tuple(sorted(map(int, row.split()[:-1]))) for row in lines[1:]]
        field_index = next(j for j, row in enumerate(parsed, 1) if row in field and len(row) >= 4)
        color_index = next(j for j, row in enumerate(parsed, 1) if row in color-field)
        for label, position in [('remove-field', field_index), ('remove-universal-color', color_index), ('remove-gauge', len(lines)-1)]:
            record = copy.deepcopy(original); bad = lines[:position]+lines[position+1:]; record['clauses'] -= 1
            bad[0] = f'p cnf 44 {record["clauses"]}'
            rejected(label+'-b'+str(index), record, '\n'.join(bad)+'\n')
        for label, position in [('wrong-physical-sign', field_index), ('wrong-root-window-sign', color_index), ('reverse-gauge', len(lines)-1)]:
            record = copy.deepcopy(original); bad = lines.copy(); values = list(map(int, bad[position].split()))
            values[0] = -values[0]; bad[position] = ' '.join(map(str, values))
            rejected(label+'-b'+str(index), record, '\n'.join(bad)+'\n')
        for label, row in [('extra-empty', '0'), ('extra-lower-unit', '2 0'),
                           ('lower-identification', '1 -5 0'), ('duplicate-field', lines[field_index])]:
            record = copy.deepcopy(original); bad = lines+[row]; record['clauses'] += 1
            bad[0] = f'p cnf 44 {record["clauses"]}'
            rejected(label+'-b'+str(index), record, '\n'.join(bad)+'\n')
    for label, modify in [
        ('missing-background-head', lambda d:d['records'].pop(1)),
        ('missing-gap-head', lambda d:d['records'].__delitem__(slice(6, 8))),
        ('repeated-gap-head', lambda d:d['records'].__setitem__(2, copy.deepcopy(d['records'][0]))),
        ('wrong-whole-producer', lambda d:d.update(producer_sha256='changed')),
        ('false-producer-status', lambda d:d.update(status='EXACT')),
        ('wrong-whole-head-count', lambda d:d.update(total_heads=29)),
        ('extra-producer-field', lambda d:d.update(foreign_cut=True)),
    ]:
        damaged = copy.deepcopy(models); modify(damaged)
        reject(label, lambda d=damaged:audit.validate_cover(d))
    isolated = output/'isolated'/'round-two/six-vdw-2'/ROOT.name
    isolated.mkdir(parents=True)
    for path in ROOT.iterdir():
        if path.is_file():
            shutil.copyfile(path, isolated/path.name)
    for name in dependency['relative_files']:
        target = isolated.parent/name; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PUBLIC/name, target)
    python = Path(sys.executable).absolute(); flags = [] if __debug__ else ['-O']
    for label, path in [('changed-common-before-import', isolated/'common.py'),
                        ('changed-producer-before-import', isolated/'generate.py'),
                        ('changed-independent-audit-before-import', isolated/'audit.py'),
                        ('changed-physical-helper-before-import', isolated.parent/'order7-geometric-cut/encode.py'),
                        ('changed-fixture-before-import', isolated/'EXPECTED.csv'),
                        ('changed-whole-phase8-proof-before-import', isolated.parent/'order7-antipodal-geography/PROOF.md')]:
        pins(); original = path.read_bytes(); path.write_bytes(original+b'# changed\n')
        try:
            child = subprocess.run([python, *flags, isolated/'common.py'], capture_output=True, text=True, env=ENV, timeout=10)
            require(child.returncode != 0 and 'ValueError' in child.stderr, 'whole pre-import source damage accepted: '+label)
            tests.append(label)
        finally:
            path.write_bytes(original)
    cnf = output/'control.cnf'; cnf.write_text('p cnf 1 2\n1 0\n-1 0\n')
    proof = output/'control.lrat'; positives = []
    for label, text, wanted in [('valid', '3 0 1 2 0\n', True), ('unknown-hint', '3 0 1 8 0\n', False),
                               ('deleted-hint', '3 d 1 0\n4 0 1 2 0\n', False), ('no-conflict', '3 0 1 0\n', False),
                               ('no-empty', '3 1 0 1 0\n', False), ('RAT-hint', '3 0 -1 2 0\n', False),
                               ('stale-addition-id', '2 0 1 2 0\n', False)]:
        pins(); pins(); proof.write_text(text)
        child = subprocess.run([python, *flags, BASE/'check_rup_lrat.py', cnf, proof], capture_output=True, text=True, env=ENV, timeout=10)
        require((child.returncode == 0) == wanted, 'strict RUP control differs: '+label)
        if wanted:
            result = json.loads(child.stdout)
            require(result['status'] == 'EXACT_RUP_LRAT_VERIFIED' and result['checked_additions'] == 1
                    and result['propagation_hints_checked'] == 2, 'valid strict RUP control counts differ')
            positives.append('RUP-'+label)
        else:
            require(json.loads(child.stdout)['status'] == 'REJECTED', 'strict RUP rejection not explicit')
            tests.append('RUP-'+label)
    result = dict(agent='six-vdw-2', role='researcher', status='ALL_RUN7_PRE_NATIVE_DAMAGES_REJECTED',
                  tests=tests, positive_controls=positives, seconds=time.monotonic()-began)
    (output/'result.json').write_text(json.dumps(result, indent=2)+'\n'); print(json.dumps(result), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True); args = parser.parse_args()
    main(args.work.absolute(), args.output.absolute())
