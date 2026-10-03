#!/usr/bin/env python3
"""Ten semantically false fixtures, checked without expected-output/hash gates."""
from pathlib import Path
import copy,json,argparse
import check as c
g=c.g
HERE=Path(__file__).resolve().parent
def fails(label,fn):
    try:fn()
    except (ValueError,IndexError,KeyError,TypeError):return {'fixture':label,'rejected':True}
    raise ValueError('false mathematical fixture accepted: '+label)
def record():
    data=json.loads((HERE/'certificate.json').read_text());tests=[]
    def changed(label,modify):
        d=copy.deepcopy(data);modify(d);tests.append(fails(label,lambda:c.record(d)))
    changed('negative actual stress weight',lambda d:d['positive_original_stress'][0].update(weight=['-1','0']))
    changed('wrong original source contact',lambda d:d['positive_original_stress'][0].update(source=1))
    changed('reverse actual receiving support',lambda d:d['positive_original_stress'][0]['edge'].reverse())
    changed('false centrally symmetric opposite height extension',lambda d:d['asymmetric_receiving_eta_height_coefficients'].__setitem__(1,['1/2','0']))
    changed('wrong original source antipode',lambda d:d['paired_source_triangle'][0].__setitem__(1,1))
    changed('false transverse bound1 instead of derived34',lambda d:d['constant_claims'].update(C0=1))
    changed('unproved physical radius1/8',lambda d:d.update(physical_Cayley_radius=['1/8','0']))
    changed('finite camera width1/1000 violates absorption',lambda d:d.update(receiver_wedge_delta=['1/1000','0']))
    def omit_translation(d):
        rows=d['full_stress_remainder_coefficients']
        k=next(i for i,row in enumerate(rows) if row[0][5] or row[0][6]);rows.pop(k)
    changed('omit a genuine original translation remainder',omit_translation)
    tests.append(fails('improper body reflection asserted as proper source motion',lambda:g.proper(g.MY)))
    return {'agent':'six-rupert-2','role':'researcher','false_mathematical_fixtures':tests,
            'rejected_count':len(tests),'no_expected_record_or_hash_rejection_used':True,
            'checks_explicit_under_optimized_python':True,'independent_review':False}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args();r=record()
    if args.output:Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'rejected_count':r['rejected_count'],'WHOLE_control_record_SHA256':g.digest(r)},indent=2))
