"""Fresh source reconstruction and every independently checked longest-six five-run certificate."""
import argparse
import csv
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time
from common import BASE, HERE, pins, require, sha
import hashlib

ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
           BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
JOURNAL = None

def semantic(data):
    return {k:v for k,v in data.items() if k not in ('seconds', 'maxrss_kib')}

def journal_save():
    path = JOURNAL['path']; temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps({k:v for k,v in JOURNAL.items() if k != 'path'}, indent=2)+'\n'); temporary.replace(path)

def stage(work, label, arguments, seconds):
    pins()
    require(all(item['label'] != label for item in JOURNAL['stages']), 'identical stage already exists')
    item = dict(label=label, status='RUNNING_INCOMPLETE', wall_limit_seconds=seconds, started=time.time())
    JOURNAL['stages'].append(item); journal_save(); print(json.dumps(item), flush=True)
    try:
        child = subprocess.run(list(map(str, arguments)), capture_output=True, text=True, env=ENV, timeout=seconds)
    except subprocess.TimeoutExpired as error:
        for suffix, data in [('stdout', error.stdout), ('stderr', error.stderr)]:
            (work/(label+'.'+suffix)).write_text(data.decode(errors='replace') if isinstance(data, bytes) else data or '')
        item.update(status='TIMEOUT_INCOMPLETE', finished=time.time()); journal_save(); raise
    (work/(label+'.stdout')).write_text(child.stdout); (work/(label+'.stderr')).write_text(child.stderr)
    item.update(status='COMPLETE' if child.returncode == 0 else 'FAILED_INCOMPLETE', returncode=child.returncode, finished=time.time())
    journal_save(); require(child.returncode == 0, 'bounded source stage failed: '+label+' '+child.stderr[-700:])
    print(json.dumps(dict(label=label, status=item['status'])), flush=True)
    return child.stdout

def reproduce(work, converter, cache):
    global JOURNAL
    began = time.monotonic(); dependency = pins(); python = Path(sys.executable).absolute()
    require(not work.exists(), 'fresh source-replay workspace required; incomplete inputs stay frozen')
    require(sha(converter.parent/'drat-trim.c') == dependency['converter']['sha256'], 'converter source differs')
    work.mkdir(parents=True); models = work/'models'
    JOURNAL = dict(path=work/'stage-ledger.json', status='INCOMPLETE', source_sha256=sha(HERE/'reproduce.py'), stages=[])
    journal_save()
    fixture = list(csv.DictReader((HERE/'EXPECTED.csv').open(newline='')))
    expected = json.loads((HERE/'VERIFICATION.json').read_text())
    require(len(fixture) == 120 and [(int(r['pair_run_slot']), int(r['gap_index']), int(r['background'])) for r in fixture]
            == [(slot, i, b) for slot in range(1,5) for i in range(15) for b in (0,1)], 'incomplete all120 canonical fixtures')
    for batch in range(20):
        stage(work, 'generate-'+str(batch), [python, HERE/'generate.py', '--work', models, '--batch', batch], 55)
    stage(work, 'merge-generation', [python, HERE/'generate.py', '--work', models, '--merge'], 55)
    audits = []
    for mode, flags in [('normal', []), ('optimized', ['-O'])]:
        batches = []
        for batch in range(20):
            stage(work, 'definitions-'+mode+'-'+str(batch), [python, *flags, HERE/'audit.py', '--work', models, '--batch', batch], 55)
            batches.append(json.loads((models/f'audit-{mode}-batch-{batch}.json').read_text()))
        stage(work, 'cover-'+mode, [python, *flags, HERE/'audit.py', '--work', models, '--controls'], 55)
        controls = json.loads((models/f'audit-{mode}-controls.json').read_text())
        census = lambda d:{k:v for k,v in d.items() if k not in ('records', 'ordinary_cover_controls', 'bounded_batch', 'seconds', 'maxrss_kib')}
        require(all(census(batch) == census(controls) for batch in batches), 'entire actual-field census differs')
        records = [record for batch in batches for record in batch['records']]
        require(records == json.loads((models/'models.json').read_text())['records'], 'incomplete whole120 signed definitions')
        merged = dict(controls, records=records, bounded_batch=None, bounded_batches=20,
                      seconds=sum(batch['seconds'] for batch in batches)+controls['seconds'],
                      maxrss_kib=max(child['maxrss_kib'] for child in [*batches, controls]))
        (models/f'audit-{mode}.json').write_text(json.dumps(merged, indent=2)+'\n'); audits.append(merged)
    require(semantic(audits[0]) == semantic(audits[1])
            and hashlib.sha256(json.dumps(semantic(audits[0]),sort_keys=True,separators=(',',':')).encode()).hexdigest() == expected['expected_complete_definition_sha256'],
            'ENTIRE normal/O actual definitions/ordinary coverage/metadata differ')
    guards = []
    for mode, flags in [('normal', []), ('optimized', ['-O'])]:
        output = work/('guards-'+mode)
        stage(work, 'guards-'+mode, [python, *flags, HERE/'guards.py', '--work', models, '--output', output], 55)
        guards.append(json.loads((output/'result.json').read_text()))
    require(semantic(guards[0]) == semantic(guards[1]) and len(guards[0]['tests']) == 83
            and guards[0]['positive_controls'] == ['RUP-valid'], 'ENTIRE source/physical/cover/RUP damage records differ')
    produced = json.loads((models/'models.json').read_text())
    require(produced['producer_sha256'] == sha(HERE/'generate.py') and len(produced['records']) == 120, 'changed whole producer/source binding')
    require(len({r['cnf_sha256'] for r in produced['records']}) == 120
            and not {r['cnf_sha256'] for r in produced['records']}.intersection(dependency['frozen_prior_cnfs']), 'duplicate/frozen native inputs')
    for record, row in zip(produced['records'], fixture):
        require(all(str(record[k]) == row[k] for k in ('stem', 'pair_run_slot', 'gap_index', 'background', 'phase_K', 'variables', 'clauses', 'cnf_sha256')),
                'whole canonical model fixture differs')
    result = dict(agent='six-vdw-2', role='researcher', status='INCOMPLETE_LONGEST_SIX_FIVE_RUNS_SOURCE_REPLAY', cases=[],
                  fixture_sha256=sha(HERE/'EXPECTED.csv'), definition_audit=semantic(audits[0]), damage_controls=semantic(guards[0]),
                  global_W_bound=False, whole_H7_exclusion=False, phase_endpoint_exclusion=False, longest_minority_run6_exclusion=False, longest_minority_run6_five_runs_exclusion=False)
    def save():
        result.update(seconds=time.monotonic()-began, maxrss_parent_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        temporary = work/'result.json.tmp'; temporary.write_text(json.dumps(result, indent=2)+'\n'); temporary.replace(work/'result.json')
    save()
    for record, row in zip(produced['records'], fixture):
        stem = record['stem']; cnf = models/(stem+'.cnf'); lrat = cnf.with_suffix('.lrat')
        item = dict(stem=stem, status='PENDING_INCOMPLETE', mathematical_exclusion=False); result['cases'].append(item); save()
        try:
            pins(); require(sha(cnf) == record['cnf_sha256'], 'independently audited input changed')
            if cache is not None:
                candidate = cache/(stem+'.lrat'); require(sha(candidate) == row['lrat_sha256'], 'untrusted candidate bytes differ')
                shutil.copyfile(candidate, lrat); item['proposal_source'] = 'cached_candidate_not_trusted'
            else:
                item.update(proposal=json.loads(stage(work, stem+'-native', [python, BASE/'solve.py', cnf, '--conflicts', 50000], 30)))
                item['status'] = item['proposal']['status']; save()
                require(item['proposal']['cnf_sha256'] == record['cnf_sha256'], 'fresh native input binding differs')
                if item['proposal']['status'] == 'SAT_PENDING_INDEPENDENT_CHECK':
                    for mode, flags in [('normal', []), ('optimized', ['-O'])]:
                        stage(work, stem+'-witness-'+mode, [python, *flags, HERE/'audit.py', '--work', models, '--witness', stem], 55)
                    item['status'] = 'INDEPENDENT_ACTUAL_FIELD_WITNESS'; save(); break
                if item['proposal']['status'] != 'UNSAT_PENDING_CHECK':
                    break
                require('s VERIFIED' in stage(work, stem+'-convert', [converter, cnf, cnf.with_suffix('.drat'), '-t', 25, '-L', lrat], 30), 'incomplete conversion')
                item['proposal_source'] = 'fresh_bounded_native_and_conversion'
            checks = [json.loads(stage(work, stem+'-RUP-'+mode, [python, *flags, BASE/'check_rup_lrat.py', cnf, lrat], 30))
                      for mode, flags in [('normal', []), ('optimized', ['-O'])]]
            require(semantic(checks[0]) == semantic(checks[1]) and checks[0]['status'] == 'EXACT_RUP_LRAT_VERIFIED'
                    and checks[0]['cnf_sha256'] == record['cnf_sha256'] == sha(cnf)
                    and checks[0]['proof_sha256'] == sha(lrat), 'whole strict RUP normal/O bindings/counts differ')
            require(sha(lrat) == row['lrat_sha256'] and all(str(checks[0][k]) == row[c] for k,c in
                    [('checked_additions', 'additions'), ('deleted_clauses', 'deletions'), ('propagation_hints_checked', 'hints')]),
                    'exact expected certificate bytes/counts differ')
            item.update(status='EXACT_CASE_REFUTATION', mathematical_exclusion=True, RUP=checks[0], RUP_optimized=checks[1])
        except BaseException as error:
            item.update(status='FAILED_OR_TIMEOUT_INCOMPLETE_NO_EXCLUSION', failure=type(error).__name__); save(); raise
        save()
    if len(result['cases']) == 120 and all(item['mathematical_exclusion'] for item in result['cases']):
        result.update(status='EXACT_H7_ELEVEN_LONGEST_SIX_FORCES_SIX_RUNS', longest_minority_run6_five_runs_exclusion=True,
                      phase_weights=[11,33],conditional_longest_minority_run=6,conditional_minority_run_count=6,
                      remaining_necessary_normalized_phases_per_background=1876,
                      total_additions=sum(item['RUP']['checked_additions'] for item in result['cases']),
                      total_deletions=sum(item['RUP']['deleted_clauses'] for item in result['cases']),
                      total_hints=sum(item['RUP']['propagation_hints_checked'] for item in result['cases']))
        require(all(item['status'] == 'COMPLETE' for item in JOURNAL['stages']), 'incomplete source journal stage')
        JOURNAL['status'] = 'ALL_SOURCE_STAGES_COMPLETED'; journal_save()
    save(); print(json.dumps({k:v for k,v in result.items() if k not in ('cases', 'definition_audit', 'damage_controls')}), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--converter', type=Path, required=True); parser.add_argument('--certificate-cache', type=Path)
    args = parser.parse_args()
    reproduce(args.work.absolute(), args.converter.absolute(), args.certificate_cache.absolute() if args.certificate_cache else None)
