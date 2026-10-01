"""Serial bounded proposals; only audited definitions plus strict RUP yield the lemma."""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
from common import BASE, HERE, pins, require, sha

THREAD_ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
                 MKL_NUM_THREADS='1', BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')


def stage(work, label, argv, seconds=30):
    result = subprocess.run(list(map(str, argv)), capture_output=True, text=True,
                            env=THREAD_ENV, timeout=seconds)
    (work / (label+'.stdout')).write_text(result.stdout)
    (work / (label+'.stderr')).write_text(result.stderr)
    require(result.returncode == 0, 'stage failed: '+label)
    return result.stdout


def reproduce(work, converter):
    began = time.monotonic()
    # Source-integrity guard; no manifest trust replaces definition/certificate checks.
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ')
        require(sha(HERE / name) == digest, 'changed published source: '+name)
    dependency = pins()
    require(sha(converter.parent / 'drat-trim.c') == dependency['converter']['sha256'],
            'converter source differs from pinned upstream source')
    require(not work.exists(), 'fresh external work directory required')
    # Keep this interpreter path: resolving a venv executable loses its environment.
    python = Path(sys.executable).absolute()
    generated = subprocess.run([str(python), str(HERE / 'generate.py'), '--work', str(work)],
        capture_output=True, text=True, timeout=55, env=THREAD_ENV)
    require(generated.returncode == 0, 'generator failed: '+generated.stderr[-1000:])
    (work / 'generate.stdout').write_text(generated.stdout)
    audits = [json.loads(stage(work, 'definitions-'+label,
        [python, *flags, HERE / 'audit.py', '--work', work], 55))
        for label, flags in [('normal', []), ('optimized', ['-O'])]]
    def semantic(data):
        return {k: v for k, v in data.items() if k not in ('seconds', 'maxrss_kib')}
    require(audits[0]['status'] == 'EXACT_ENDPOINT_DEFINITION_AUDIT'
            and semantic(audits[0]) == semantic(audits[1]), 'definition audits disagree')
    fixture = json.loads((HERE / 'EXPECTED.json').read_text())
    expected = fixture['cases']
    records = json.loads((work / 'models.json').read_text())['cases']
    require(len(records) == len(expected) == 18, 'incomplete proof cover')
    for actual, reference in zip(records, expected):
        require(all(actual[k] == reference[k] for k in
            ('stem', 'background', 'phase_K', 'variables', 'clauses', 'cnf_sha256')),
            'canonical CNF fixture differs')
    result = dict(agent='six-vdw-2', role='researcher', status='INCOMPLETE_NO_ENDPOINT_EXCLUSION',
                  cases=[], global_W_bound=False, whole_H7_exclusion=False)

    def save():
        result.update(seconds=time.monotonic()-began,
            maxrss_parent_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        (work / 'result.json').write_text(json.dumps(result, indent=2)+'\n')
    save()
    for index, (record, reference) in enumerate(zip(records, expected)):
        stem = record['stem']
        cnf, lrat = work / (stem+'.cnf'), work / (stem+'.lrat')
        item = dict(stem=stem, status='PENDING', mathematical_exclusion=False)
        result['cases'].append(item)
        save()
        try:
            proposal = json.loads(stage(work, stem+'-native',
                [python, BASE / 'solve.py', cnf, '--conflicts', 50000]))
            item.update(proposal=proposal, status=proposal['status'])
            save()
            if proposal['status'] != 'UNSAT_PENDING_CHECK':
                print(json.dumps(dict(stem=stem, status=item['status'])), flush=True)
                break  # UNKNOWN/SAT is no exclusion; no identical retry or larger cap.
            conversion = stage(work, stem+'-convert',
                [converter, cnf, cnf.with_suffix('.drat'), '-t', 25, '-L', lrat])
            require('s VERIFIED' in conversion, 'conversion did not complete')
            checks = [json.loads(stage(work, stem+'-RUP-'+label,
                [python, *flags, BASE / 'check_rup_lrat.py', cnf, lrat]))
                for label, flags in [('normal', []), ('optimized', ['-O'])]]
            require(checks[0]['status'] == 'EXACT_RUP_LRAT_VERIFIED'
                    and semantic(checks[0]) == semantic(checks[1]), 'strict RUP checks disagree')
            require(checks[0]['cnf_sha256'] == record['cnf_sha256'] == sha(cnf)
                    and checks[0]['proof_sha256'] == sha(lrat), 'changed certificate input')
            item.update(status='EXACT_ENDPOINT_CASE_REFUTATION', mathematical_exclusion=True,
                        RUP=checks[0], RUP_optimized=checks[1],
                        byte_reproduction=(sha(lrat) == reference['lrat_sha256']),
                        expected_count_reproduction=(checks[0]['checked_additions'] ==
                            reference['checked_additions'] and checks[0]['propagation_hints_checked']
                            == reference['hints']))
            save()
            print(json.dumps(dict(stem=stem, status=item['status'],
                conflicts=proposal['stats']['conflicts'], seconds=result['seconds'])), flush=True)
            if index == 7:
                require(all(r['mathematical_exclusion'] for r in result['cases']),
                        'packing cover not refuted before close branches')
        except subprocess.TimeoutExpired:
            item['status'] = 'BOUNDED_STAGE_TIMEOUT_NO_EXCLUSION'
            save()
            break
    if len(result['cases']) == 18 and all(r['mathematical_exclusion'] for r in result['cases']):
        result.update(status='EXACT_PHASE_ENDPOINTS_7_37_EXCLUDED',
            nonconstant_phase_band=[8, 36],
            total_checked_additions=sum(r['RUP']['checked_additions'] for r in result['cases']),
            total_hints=sum(r['RUP']['propagation_hints_checked'] for r in result['cases']),
            all_proof_bytes_reproduced=all(r['byte_reproduction'] for r in result['cases']))
        save()
    save()
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--converter', type=Path, required=True)
    args = parser.parse_args()
    reproduce(args.work.absolute(), args.converter.absolute())
