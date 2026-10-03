#!/usr/bin/env python3
"""Whole exact coefficient record and genuine mathematical damage checks.

Actual six-sendov-3 / researcher. Same-author corroboration, not review.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arithmetic import CertificateError,need,canonical,sha256
from jets import build
import json

HERE=Path(__file__).resolve().parent
DAMAGES={
 'wrong_cubic_mean':'entire third root jet 1',
 'wrong_mean_column':'complete actual anchored polynomial fourth jet',
 'missing_critical_multiplicity':'all eight centered criticals sum zero',
 'wrong_primitive_cubic_sign':'entire third root jet 0',
 'missing_ninth_root':'all nine entire root and normal maps',
 'missing_modulus_curvature':'whole fourth residuals in real cubic field',
 'wrong_fourth_residual':'whole fourth residuals in real cubic field',
 'wrong_closing_M':'active root strictly inward at fourth order 3',
 'quadratic_instead_of_first_power':'actual first-power exact C slope',
 'false_objective_upper_cut':'strict second objective coefficient bounds 9<K<10',
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
    need({'arithmetic.py','jets.py','verify.py','validate.py','EXPECTED.json','PROOF.md','README.md','LITERATURE.md','dependencies.json'}<=set(names),'complete required source manifest')

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
      'all_original_root_jets':len(record['all_nine_parameter_root_jets']),
      'all_individual_half_normals':len(record['all_nine_parameter_half_normals']),
      'all_critical_multiplicities':8,'active_fourth_order_inward_roots':4,
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
