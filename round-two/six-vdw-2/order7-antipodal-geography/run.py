"""Regenerate, independently audit, propose and strictly replay all 46 models."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'order7-geometric-cut'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_seconds(result):
    return {k:v for k,v in result.items() if k != 'seconds'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--audit-only', action='store_true')
    args = parser.parse_args()
    work = args.work.absolute()
    require(not work.exists() or args.resume, 'fresh work directory or --resume required')
    work.mkdir(parents=True, exist_ok=True)
    prior = json.loads((work/'progress.json').read_text()) if (work/'progress.json').exists() else None
    pins = json.loads((HERE/'SOURCE_PINS.json').read_text())
    for name,digest in pins['files'].items():
        require(sha(BASE/name) == digest, 'changed committed helper: '+name)
    if prior is not None:
        require(prior['dependency_pins'] == pins['files'], 'changed resume dependencies')
    # Import the log generator only after checking every committed dependency.
    import encode
    began = time.monotonic()
    records = encode.prepare(work)
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    def run(cmd, timeout=30):
        p = subprocess.run([str(v) for v in cmd],capture_output=True,text=True,
                           env=env,timeout=timeout)
        require(p.returncode == 0, p.stderr[-1800:] or p.stdout[-1800:])
        return p.stdout
    # No solver call precedes both complete independent semantic audits.
    audits = [json.loads(run([sys.executable]+flags+[HERE/'audit.py',work],timeout=55))
              for flags in ([],['-O'])]
    require(without_seconds(audits[0]) == without_seconds(audits[1]), 'audit modes differ')
    require(audits[0]['status'] == 'ALL_46_MODELS_EXACTLY_DEFINITION_AUDITED', 'incomplete semantic audit')
    fixtures = json.loads((HERE/'expected.json').read_text())['records']
    require(len(records) == len(fixtures) == len(audits[0]['records']) == 46, 'case cover incomplete')
    for rec, aud, fixture in zip(records, audits[0]['records'], fixtures):
        require(rec == {k:v for k,v in aud.items() if k != 'cnf_sha256'}, 'generator/auditor case mismatch')
        rec['cnf_sha256'] = aud['cnf_sha256']
        require(all(rec[k] == fixture[k] for k in ('stem','variables','clauses','cnf_sha256')),
                'reference instance changed')
        rec.update(status='EXACTLY_AUDITED_NOT_PROPOSED',mathematical_exclusion=False)
    meta = {'agent':'six-vdw-2', 'role':'researcher', 'status':'ALL_46_MODELS_EXACTLY_AUDITED',
            'dependency_pins':pins['files'], 'records':records, 'audit':audits[0],
            'audit_optimized_seconds':audits[1]['seconds'], 'whole_H7_exclusion':False,
            'global_W_bound':False}
    progress = work/'progress.json'
    progress.write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps({'stage':meta['status'],'seconds':time.monotonic()-began}),flush=True)
    if args.audit_only:
        return
    converter_source = work/'drat-trim.c'
    if not converter_source.exists():
        converter_source.write_bytes(urlopen(pins['converter']['url'],timeout=20).read())
    require(sha(converter_source) == pins['converter']['sha256'], 'changed converter source')
    run(['gcc','-O2','-std=gnu99',converter_source,'-o',work/'drat-trim'])
    for rec,fixture in zip(records,fixtures):
        # Boundary coverage uses the arc theorem. Do not claim the combined
        # band from unchecked native messages or a forged progress record.
        if rec['kind'] == 'boundary' and not all(r['mathematical_exclusion'] for r in records[:2]):
            break
        cnf = work/(rec['stem']+'.cnf')
        drat = cnf.with_suffix('.drat'); lrat = cnf.with_suffix('.lrat')
        try:
            proposal_file = cnf.with_suffix('.solve.json')
            if args.resume and proposal_file.exists():
                prop = json.loads(proposal_file.read_text())
                require(prop['cnf_sha256'] == sha(cnf), 'changed resume proposal input')
                if prop['status'] == 'UNSAT_PENDING_CHECK':
                    require(drat.exists() and sha(drat) == prop['drat_sha256'], 'changed resume trace')
            else:
                prop = json.loads(run([sys.executable,BASE/'solve.py',cnf,'--conflicts',50000]))
            rec['proposal'] = prop
            rec['status'] = prop['status']
            if prop['status'] == 'UNSAT_PENDING_CHECK':
                completion = cnf.with_suffix('.conversion.complete.json')
                if args.resume and completion.exists():
                    marker = json.loads(completion.read_text())
                    require(lrat.exists() and marker == {'drat_sha256':sha(drat),'lrat_sha256':sha(lrat)},
                            'changed completed conversion')
                else:
                    require(not lrat.exists(), 'unmarked converted trace')
                    output = run([work/'drat-trim',cnf,drat,'-t',25,'-L',lrat])
                    require('s VERIFIED' in output, 'conversion incomplete')
                    completion.write_text(json.dumps({'drat_sha256':sha(drat),'lrat_sha256':sha(lrat)},indent=2)+'\n')
                checked = [json.loads(run([sys.executable]+flags+[BASE/'check_rup_lrat.py',cnf,lrat]))
                           for flags in ([],['-O'])]
                require(without_seconds(checked[0]) == without_seconds(checked[1]), 'RUP modes differ')
                require(checked[0]['status'] == 'EXACT_RUP_LRAT_VERIFIED', 'no checked refutation')
                rec.update(RUP=checked[0], RUP_optimized=checked[1],
                           mathematical_exclusion=True, status='EXACT_PHASE_MODEL_REFUTATION',
                           reference_proof_byte_match=fixture['proof_sha256'] == sha(lrat))
            elif prop['status'] == 'SAT_PENDING_INDEPENDENT_CHECK':
                import audit
                witness = audit.check_candidate(rec,prop['candidate_bits'])
                cnf.with_suffix('.field-colors.json').write_text(json.dumps(witness,indent=2)+'\n')
                rec['status'] = witness['status']
            elif prop['status'] != 'UNKNOWN':
                raise ValueError('unsupported proposal status')
        except subprocess.TimeoutExpired:
            rec.update(status='BOUNDED_STAGE_TIMEOUT_NO_EXCLUSION',mathematical_exclusion=False)
        meta['seconds'] = time.monotonic()-began
        progress.write_text(json.dumps(meta,indent=2)+'\n')
        print(json.dumps({'stem':rec['stem'],'status':rec['status'],
                          'conflicts':rec.get('proposal',{}).get('stats',{}).get('conflicts'),
                          'seconds':meta['seconds']}),flush=True)
        if rec['status'] == 'INDEPENDENT_LITERAL_NONQR_H7_FIELD_WITNESS_VERIFIED':
            break
    complete = all(r['mathematical_exclusion'] for r in records)
    meta.update(status='EXACT_PHASE_SEVEN_RUN_AND_BOUNDARY_EXCLUSIONS' if complete else
                'INCOMPLETE_NO_COMBINED_PHASE_BAND',
                all_46_exact_refutations=complete,
                phase_run_bound=7 if all(r['mathematical_exclusion'] for r in records[:2]) else None,
                nonconstant_phase_weight_band=[7,37] if complete else None,
                counts=dict(Counter(r['status'] for r in records)),
                maxrss_parent_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                all_reference_proof_bytes_match=all(r.get('reference_proof_byte_match',False) for r in records))
    progress.write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps({k:meta[k] for k in ('status','all_46_exact_refutations','phase_run_bound',
                    'nonconstant_phase_weight_band','seconds','maxrss_parent_kib','maxrss_child_kib')}),flush=True)
    if not complete:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
