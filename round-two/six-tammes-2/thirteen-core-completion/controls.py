"""Reject six corruptions of geometric data, hypotheses or scalar bridges."""
import copy,json
from fractions import Fraction as Q
from pathlib import Path
import check,audit

def controls():
    original=json.loads(Path(__file__).with_name('certificate.json').read_text());cases=[]
    d=copy.deepcopy(original);d['cap_bound']='14/5';cases.append(('cap_cut_with_exterior_vertex',d))
    d=copy.deepcopy(original);d['short_squared_norm_upper']='1';cases.append(('lost_strict_norm_gap',d))
    d=copy.deepcopy(original);d['relaxed_isolated_distance_constant']=801;cases.append(('insufficient_distance_constant',d))
    d=copy.deepcopy(original);d['core_edges'].remove([6,8]);cases.append(('missing_orientation_contact',d))
    d=copy.deepcopy(original);d['exterior_vertices'][0]['vector'][0][0]=str(Q(d['exterior_vertices'][0]['vector'][0][0])+Q(1,1000))
    cases.append(('false_exterior_intersection',d))
    d=copy.deepcopy(original);d['incumbent_vectors'][3][0][0]=str(Q(d['incumbent_vectors'][3][0][0])+Q(1,1000))
    cases.append(('changed_isolated_unit_point',d))
    rejected=[]
    for name,data in cases:
        for label,verify in (('primary',check.verify),('audit',audit.verify)):
            try:verify(data)
            except ValueError:pass
            else:raise ValueError(label+' accepted '+name)
        rejected.append(name)
    return {'status':'VERIFIED','negative_controls':len(rejected),'rejected_by_both':rejected}

if __name__=='__main__':print(json.dumps(controls(),sort_keys=True))
