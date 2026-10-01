#!/usr/bin/env python3
"""Explicit reproduction bridge to hash-pinned author source, separate from audit.

Run with assertions enabled. The author source is checked before importing
it in a fresh process. Our independent checker does not import this module.
"""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from exact import need


def run(author_dir):
    here=Path(__file__).resolve().parent
    prov=json.loads((here/'PROVENANCE.json').read_text())
    for name,record in prov['pinned_author_files'].items():
        raw=(author_dir/name).read_bytes()
        need(len(raw)==record['bytes'] and sha256(raw).hexdigest()==record['sha256'],
             'pinned author input mismatch: '+name)
    own=json.loads((here/'expected.json').read_text())
    script=r"""
import json,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from dense_row_lambda import centered_certificate,maximal_certificate,cap_bound,cap_gap
from verify import matrix_hash
from dense_row_identities import run
from verify_dense_row_lambda import run as source_default
request=json.load(sys.stdin)
items=[]
for x in request['inputs']:
 D,s,Q=centered_certificate(x['v'],x['lambda'],x['blocks'])
 _,_,Qm,eta=maximal_certificate(x['v'],x['lambda'],x['blocks'],(D,s,Q))
 assert len(D)==x['N'] and s==x['s'] and str(eta)==x['eta']
 centered,repaired=matrix_hash(Q),matrix_hash(Qm)
 assert centered==x['centered_sha256'] and repaired==x['repaired_sha256']
 assert str(cap_bound(x['v'],x['lambda']))==x['upper_certificate']['caps']['original']['cap']
 assert str(cap_gap(x['v'],x['lambda']))==x['upper_certificate']['caps']['original']['delta']
 items.append({'v':x['v'],'lambda':x['lambda'],'N':len(D),'centered_sha256':centered,'repaired_sha256':repaired})
scalar=run()
assert scalar['repair_margin_shifted_polynomials']==request['coefficients']
default=source_default()
assert default==json.loads((Path(sys.argv[1])/'dense_row_expected.json').read_text())
default_summary={'default_exact_expected_match':True,'principal_forms':default['independent_principal_Fraction_forms'],
 'whole_dense_eliminations':default['default_direct_full_Schur_forms'],'rejection_controls':default['rejection_controls'],
 'upper_transfer':default['inputs'][0]['upper_transfer']}
print(json.dumps({'matrices':items,'author_zero_identities':scalar['zero_identities'],
 'author_strict_certificates':scalar['strict_certificate_count'],
 'original_repair_tables_matched':sum(len(t) for z in scalar['repair_margin_shifted_polynomials'].values() for t in z.values()),
 'author_default_cohort':default_summary},sort_keys=True))
"""
    request={'inputs':own['finite_inputs'],'coefficients':own['scalar']['repair_margin_shifted_polynomials']}
    env=os.environ.copy()
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        env[name]='1'
    r=subprocess.run([sys.executable,'-B','-c',script,str(author_dir.resolve())],
                     input=json.dumps(request),text=True,capture_output=True,env=env,timeout=30)
    need(r.returncode==0,'author bridge failure: '+r.stderr)
    result=json.loads(r.stdout)
    result.update(author_source_commit=prov['reviewed_target']['source_commit'],
                  pinned_files_verified=len(prov['pinned_author_files']),
                  trust='explicit author replay; independent audit imports none of this source; source default four principal forms and full transfer replayed; optional three full Schur forms not replayed')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--author-dir',type=Path,required=True)
    g=p.add_mutually_exclusive_group();g.add_argument('--write',type=Path);g.add_argument('--check',type=Path)
    args=p.parse_args();need(__debug__,'author bridge requires assertions enabled')
    result=run(args.author_dir)
    if args.write:args.write.write_text(json.dumps(result,indent=2)+'\n')
    if args.check:need(result==json.loads(args.check.read_text()),'bridge expected output mismatch')
    print(json.dumps({'status':'passed','pinned_files':result['pinned_files_verified'],
                      'matched_matrices':2*len(result['matrices']),
                      'canonical_sha256':sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()}))
