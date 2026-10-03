#!/usr/bin/env python3
"""Whole exact coefficient record and genuine mathematical damage checks.

Actual six-sendov-3 / researcher. Same-author corroboration, not review.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arithmetic import CertificateError,need,canonical,sha256
from maps import build
import json

HERE=Path(__file__).resolve().parent
DAMAGES={
 'missing_critical_factor':'whole generic literal derivative',
 'wrong_cubic_sign':'whole individual third half-normal 1',
 'missing_ninth_root':'all nine whole root maps',
 'missing_curvature':'whole attained least-profile fourth objective cost',
 'wrong_cubic_closure':'all four generic active cubic cancellations 3',
 'singular_odd_block':'whole odd two-by-two determinant',
 'wrong_even_closure':'all four generic normals vanish through fourth order 3',
 'wrong_first_power':'complete first-power objective and exact C slope',
 'wrong_profile_cost':'whole attained least-profile fourth objective cost',
 'missing_stationary_multiplicity':'all seven stationary multiplicity cases',
}


def check_source(directory=HERE):
    rows=(directory/'SHA256SUMS').read_text().splitlines()
    need(bool(rows),'source manifest nonempty')
    names=[]
    for row in rows:
        digest,name=row.split('  ',1)
        need('/' not in name and name not in names,'unique local manifest paths')
        names.append(name)
        need(sha256((directory/name).read_bytes()).hexdigest()==digest,'source-byte mismatch '+name)
    need({'arithmetic.py','maps.py','literal.py','verify.py','validate.py','EXPECTED.json','PROOF.md','README.md','LITERATURE.md','dependencies.json'}<=set(names),'complete required source manifest')

def no_duplicates(pairs):
    out={}
    for key,value in pairs:
        need(key not in out,'duplicate JSON key')
        out[key]=value
    return out

def no_nonfinite(value):raise CertificateError('nonfinite JSON constant')

def typed_equal(x,y):
    if type(x) is not type(y):return False
    if isinstance(x,dict):return set(x)==set(y) and all(typed_equal(x[k],y[k]) for k in x)
    if isinstance(x,list):return len(x)==len(y) and all(typed_equal(a,b) for a,b in zip(x,y))
    return x==y

def check_fixture(record,path):
    need(path.stat().st_size<300000,'compact external record size')
    other=json.loads(path.read_text(),object_pairs_hook=no_duplicates,parse_constant=no_nonfinite)
    need(typed_equal(record,other),'complete typed record mismatch')

def damage_checks():
    rows=[]
    for damage,reason in DAMAGES.items():
        try:build(damage)
        except CertificateError as e:
            need(str(e)==reason,'wrong mathematical damage rejection '+damage)
            rows.append({'damage':damage,'expected_reason':reason,'observed':str(e)})
        else:raise CertificateError('mathematical damage accepted '+damage)
    return rows

def summary(record,damages):
    return {'agent':'six-sendov-3','role':'researcher','status':'PASS',
      'all_original_root_jets':len(record['all_nine_control_root_jets']),
      'all_individual_half_normals':len(record['all_nine_control_half_normals']),
      'all_critical_multiplicities':8,'active_normals_closed_through_fourth':4,'full_control_Jacobian_blocks':2,
      'whole_record_sha256':sha256(canonical(record)).hexdigest(),
      'mathematical_damage_rejections':len(damages),
      'source_integrity':'PASS','analytic_collars':'existential ordinary proof',
      'independent_review':False,'formalized':False}

def main():
    check_source();record=build()
    path=Path(sys.argv[1]) if len(sys.argv)==2 else HERE/'EXPECTED.json'
    need(len(sys.argv)<=2,'usage: verify.py [whole-external-record.json]')
    check_fixture(record,path);damages=damage_checks()
    print(json.dumps(summary(record,damages),sort_keys=True))

if __name__=='__main__':main()
