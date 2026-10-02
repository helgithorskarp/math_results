"""Serial exact regeneration and independent checking, standard-library Python.

Each child has an unchanged55-second operational limit. A failed/incomplete
stage is not a mathematical exclusion. All large arrays stay in ignored work/.
The scalar mathematical checks run with and without Python optimization.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def need(test,message):
    if not test:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()


def finite(obj):
    return {k:v for k,v in obj.items() if k not in ('seconds','maximum_rss_kib')}


def stage(name,args=(),optimized=False,receipt=None):
    argv = [sys.executable]+(['-O'] if optimized else [])+[str(ROOT/name),*map(str,args)]
    result = subprocess.run(argv,capture_output=True,text=True,timeout=55,check=False)
    need(result.returncode == 0, 'Failed stage '+name+': '+result.stderr[-2500:])
    data = json.loads(result.stdout)
    if receipt:
        (ROOT/'work'/receipt).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'stage':name,'args':list(args),'optimized':optimized,
                      'status':data.get('status','EXACT_STAGE_COMPLETED')},sort_keys=True),flush=True)
    return data


def both(name,args=(),normal_receipt=None,optimized_receipt=None):
    a = stage(name,args,receipt=normal_receipt)
    b = stage(name,args,True,optimized_receipt)
    need(finite(a) == finite(b), 'Mathematical records differ under -O: '+name)
    return finite(a)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record-certificate',action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        os.environ[name] = '1'
    work = ROOT/'work'
    work.mkdir(exist_ok=True)
    manifest = json.loads((ROOT/'source-manifest.json').read_text())
    for row in manifest['files']:
        need(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest() == row['sha256'],
             'Source pin differs: '+row['path'])
    stage('base.py')
    base = both('verify_base.py')
    stage('preparations.py',('--partner',4))
    prep = both('verify_preparations.py')
    need(prep['partners'][0]['complete_functions'] == 762, 'Complete preparation census differs')
    stage('minimum.py')
    minimum = both('verify_minimum.py')
    stage('fronts.py')
    cover = both('verify_fronts.py',normal_receipt='partner4-one-prior-fronts-independent-normal.json',
                 optimized_receipt='partner4-one-prior-fronts-independent-optimized.json')
    cases = []
    for branch in range(10):
        stage('select_constant.py',('--branch',branch))
        stage('select_full.py',('--branch',branch))
        replay = both('verify_nested.py',('--branch',branch))
        cases.append({k:replay[k] for k in ('branch_id','census','selected_occurrences','selected_B7_counts',
                                           'minimum_selected_mass','replay_sha256','root_masses_sha256')})
    certificate = {'schema':'thirteen-L4-one-prior-HIGH-summary-v1','agent':'six-sorting-1','role':'researcher',
                   'fixture_sha256':hashlib.sha256((ROOT/'fixture.json').read_bytes()).hexdigest(),
                   'scope':'Standard completions of literalB23;L4 with exactly one prior equal HIGH merge before the first strict HIGH singleton. Arbitrary suffix depth; not universal S13 exclusion.',
                   'total_budget':44,'imported_lower_bounds':{'S5':9,'S6':12,'S7':16,'S11':35},
                   'core_image_sha256':base['core_image_sha256'],
                   'complete_LOW_records_sha256':base['complete_LOW_records_sha256'],
                   'complete_HIGH_records_sha256':base['complete_HIGH_records_sha256'],
                   'preparation_functions':762,'per_gate_function_counts':[r['full_preparation_functions'] for r in prep['partners'][0]['branches']],
                   'minimum_census':minimum['census'],'minimum_records_sha256':minimum['records_sha256'],
                   'front_census':cover['census'],'front_records_sha256':cover['producer_records_sha256'],
                   'verified_nested_fronts':sum(r['census']['verified_fronts'] for r in cases),
                   'selected_original_outer_witnesses':sum(r['selected_occurrences'] for r in cases),
                   'minimum_selected_mass':min(r['minimum_selected_mass'] for r in cases),
                   'size44_ceiling':1<<44,'branch_certificates':cases,
                   'normal_optimized_checker_finite_records_equal':True,
                   'same_author_algorithmic_independence':True,'external_person_review_claimed':False,
                   'written_bridges_formalized':False,'large_Harder_corpus_replayed':False}
    need(certificate['verified_nested_fronts'] == 5613 and certificate['selected_original_outer_witnesses'] == 25630 and
         certificate['minimum_selected_mass'] > 1<<44, 'Full strict nested summary differs')
    path = ROOT/'certificate.json'
    if args.record_certificate:
        need(not path.exists(), 'Refusing to overwrite recorded certificate')
        path.write_text(json.dumps(certificate,separators=(',',':'))+'\n')
    else:
        need(certificate == json.loads(path.read_text()), 'Reproduced finite certificate differs')
    (work/'verified-summary.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps({'agent':'six-sorting-1','role':'researcher','status':'ALL_ONE_PRIOR_HIGH_PREMISES_AND5613_NESTED_EXCLUSIONS_VERIFIED_NORMAL_AND_O',
                      'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                      'certificate_bytes':path.stat().st_size,'fronts':5613,'selected_outer_witnesses':25630,
                      'minimum_selected_mass':certificate['minimum_selected_mass'],
                      'seconds':time.monotonic()-start},sort_keys=True),flush=True)


if __name__ == '__main__':
    main()
