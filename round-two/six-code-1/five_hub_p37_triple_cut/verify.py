"""Full entrywise checks, compact output and semantic controls; six-code-1."""
from collections import Counter
import argparse
import copy
import hashlib
import json
from pathlib import Path
import producer
import oracle

HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise ValueError(message)

def enc(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def rejects(call):
    try:call()
    except (ValueError,KeyError,IndexError,TypeError):return True
    raise ValueError('semantic damage was accepted')

def run(first):
    a,diag_a=producer.build();b,diag_b=oracle.build()
    need(a==b,'every literal mark, scalar case, full vector, certificate and ordered allocation must agree')
    need(len(a['scalar_cases'])==92,'complete92-case T>=3 domain')
    allrows=[r for branch in a['branches'] for r in branch['rows']]
    need(all(r['certificate']['reason']!='OPEN' for r in allrows),'at least one necessary population remains')
    residual=[(br['case'],r) for br in a['branches'] for r in br['rows'] if r['certificate']['reason']=='DISJOINT_SINGLE_HUB_COLUMNS']
    need(len(residual)==2,'exact two actual single-hub residues')
    controls=[]
    K14=dict(N=(4,4,3,2,1),n=(1,1,3,0,0),D=(5,5,6,2,1))
    need(K14 in a['ordered_column_calibration'][14],'literal positive relaxed-column control')
    controls.append(dict(name='K14_RELAXED_POSITIVE_COLUMNS',record=K14,scope='necessary abstract allocation, not a packing'))
    c,r=residual[0];v=list(r['vector']);oldp=producer.frozen();oldo=oracle.frozen()
    bad=v.copy();bad[0]=-1
    damages=[('NEGATIVE_POPULATION',lambda:producer.check_vector(a['types'],c,bad)),
             ('SHORT_VECTOR',lambda:oracle.check_vector(a['types'],c,v[:-1])),
             ('WRONG_K',lambda:producer.check_vector(a['types'],dict(c,K=c['K']+1),v)),
             ('WRONG_X',lambda:oracle.check_vector(a['types'],dict(c,X=c['X']+1),v)),
             ('WRONG_Q',lambda:producer.check_vector(a['types'],dict(c,Q=c['Q']+1),v)),
             ('BOOLEAN_COUNT',lambda:oracle.check_vector(a['types'],c,[True]+v[1:]))]
    damage_records=[dict(name=n,rejected=rejects(f)) for n,f in damages]
    weakened=copy.deepcopy(r['certificate']);weakened['distinct_B_hubs']=False
    rejected=rejects(lambda:need(weakened==oracle.certificate(a['types'],c,v,oldo,a['ordered_column_calibration']),
                                'exact certificate lost the distinct-hub premise'))
    damage_records.append(dict(name='DROPPED_DISTINCT_HUB_PREMISE',rejected=rejected))
    cut_counts=Counter(r['certificate']['reason'] for r in allrows)
    record=dict(mathematical_core=a,controls=controls,semantic_damages=damage_records)
    summary=dict(actual_agent='six-code-1',role='researcher',status='COMPLETE_CONDITIONAL_P37_T_AT_MOST2',
                 raw_marks=len(a['actual_marks']),conservative_marks=len(a['conservative_marks']),types=len(a['types']),
                 scalar_cases=len(a['scalar_cases']),full_population_vectors=len(allrows),cut_counts=dict(cut_counts),
                 branch_records=[dict(case=br['case'],vectors=len(br['rows']),cuts=dict(Counter(r['certificate']['reason'] for r in br['rows']))) for br in a['branches']],
                 ordered_column_counts={str(k):len(v) for k,v in a['ordered_column_calibration'].items()},
                 literal_T3_residues=[dict(case=c,rows=[[a['types'][j],n] for j,n in enumerate(r['vector']) if n],certificate=r['certificate']) for c,r in residual],
                 semantic_damages=damage_records,mathematical_sha256=hashlib.sha256(enc(record)).hexdigest(),
                 ordinary_bridges_formalized=False,external_independent_review=False)
    target=HERE/'EXPECTED.json'
    if first:need(not target.exists(),'first output must precede EXPECTED')
    else:need(enc(summary)==enc(json.loads(target.read_text())),'complete canonical summary and whole-record checksum must match')
    print(json.dumps(dict(summary=summary,diagnostics=dict(producer=diag_a,oracle=diag_b)),sort_keys=True,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--first-run',action='store_true');run(p.parse_args().first_run)
