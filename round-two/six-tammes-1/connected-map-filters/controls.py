"""Meaningful adverse inputs and valid representations for the exact auditor."""
from pathlib import Path
from copy import deepcopy
import hashlib, json
from fractions import Fraction as F
from audit import verify

ROOT=Path(__file__).resolve().parent


def row(obj,t,s):
    return next(x for x in obj['QQ_cases'] if (x['t'],x['s'])==(t,s))


def set_item(seq,index,value):seq[index]=value


def rescale_rf(obj):
    for r in obj['QQ_cases']:
        for name in ('B_t_over_A','B_s_over_A','S_over_A','P',
                     'discriminant','lower_gap_product','upper_gap_product'):
            for part in ('numerator','denominator'):
                r[name][part]=[str(3*F(x)) for x in r[name][part]]


def facet_cycles(obj):
    cal=obj['endpoint_calibration']
    cal['faces']=[f[1:]+f[:1] for f in reversed(cal['faces'])]
    cal['faces']=[list(reversed(f)) for f in cal['faces']]
    cal['supporting_planes'].reverse()
    for plane in cal['supporting_planes']:
        plane['normal']=[str(5*F(x)) for x in plane['normal']]
        plane['constant']=str(5*F(plane['constant']))


def component_order(obj):
    cal=obj['endpoint_calibration'];cal['triangle_components'].reverse()
    for comp in cal['triangle_components']:
        comp['triangles'].reverse();comp['vertices'].reverse()
        comp['triangles']=[list(reversed(t)) for t in comp['triangles']]
    cal['QQ_edges'].reverse()
    for r in cal['QQ_edges']:r['edge'].reverse()


def profile_order(obj):
    d=obj['triangle_forest_profiles'];d['rows'].reverse()
    for r in d['rows']:r['component_sizes'].reverse()
    d['motif_compatible_profiles'].reverse()
    for p in d['motif_compatible_profiles']:p.reverse()
    for block in d['triangles']:
        block.reverse()
        for t in block:t.reverse()
    d['prescribed_edges'].reverse()
    for e in d['prescribed_edges']:e.reverse()


def main():
    data=(ROOT/'CERTIFICATE.json').read_bytes();original=json.loads(data)
    damages=[
        ('omit endpoint type',lambda x:x['QQ_cases'].pop()),
        ('duplicate endpoint type',lambda x:x['QQ_cases'].append(deepcopy(x['QQ_cases'][0]))),
        ('invent wider upper endpoint',lambda x:x['algebraic_closed_band'].__setitem__(1,'3/4')),
        ('erase strict lower endpoint',lambda x:x.__setitem__('local_conclusion_lower_strict',False)),
        ('alter cotangent value',lambda x:row(x,2,3)['B_s_over_A']['numerator'].__setitem__(0,'1')),
        ('alter solved star sum',lambda x:row(x,2,2)['S_over_A']['numerator'].__setitem__(0,'2')),
        ('alter discriminant binding',lambda x:row(x,2,2)['discriminant']['numerator'].__setitem__(0,'2')),
        ('replace lower product by upper',lambda x:row(x,2,3)['obstruction'].__setitem__('rational',deepcopy(row(x,2,3)['upper_gap_product']))),
        ('use wrong cubic coefficient',lambda x:row(x,2,3)['obstruction']['numerator']['numerator'].__setitem__(3,'13')),
        ('lose upper endpoint negativity',lambda x:row(x,2,3)['obstruction']['Bernstein_numerator'].__setitem__(3,'4/49')),
        ('invent endpoint square value',lambda x:row(x,2,2)['obstruction'].__setitem__('exception_x_equals_y_squared','1/3')),
        ('wrong negative sum sign',lambda x:row(x,3,3)['S_over_A']['numerator'].__setitem__(0,'1')),
        ('change physical metric',lambda x:x['endpoint_calibration']['coordinate_metric'].__setitem__(2,5)),
        ('alter literal endpoint coordinate',lambda x:x['endpoint_calibration']['scaled_points'][0].__setitem__(0,'2')),
        ('alter a Gram entry',lambda x:x['endpoint_calibration']['Gram'][0].__setitem__(1,'0')),
        ('omit supporting facet',lambda x:x['endpoint_calibration']['supporting_planes'].pop()),
        ('flip supporting plane',lambda x:x['endpoint_calibration']['supporting_planes'][0]['normal'].__setitem__(0,'99')),
        ('omit actual face',lambda x:x['endpoint_calibration']['faces'].pop()),
        ('omit QQ endpoint counterexample',lambda x:x['endpoint_calibration']['QQ_edges'].pop()),
        ('invent mixed endpoint count',lambda x:x['endpoint_calibration']['QQ_edges'][0]['endpoint_face_sizes'][0].__setitem__(0,4)),
        ('omit calibration tree component',lambda x:x['endpoint_calibration']['triangle_components'].pop()),
        ('change component support',lambda x:x['endpoint_calibration']['triangle_components'][0]['vertices'].pop()),
        ('omit motif triangle',lambda x:x['triangle_forest_profiles']['triangles'][0].pop()),
        ('identify two motif labels',lambda x:x['triangle_forest_profiles']['triangles'][1][3].__setitem__(2,7)),
        ('omit a prescribed motif edge',lambda x:x['triangle_forest_profiles']['prescribed_edges'].pop()),
        ('omit a size profile',lambda x:x['triangle_forest_profiles']['rows'].pop()),
        ('duplicate size profile',lambda x:x['triangle_forest_profiles']['rows'].append(deepcopy(x['triangle_forest_profiles']['rows'][0]))),
        ('wrong Euler edge count',lambda x:x['triangle_forest_profiles']['rows'][0].__setitem__('NN_edges',99)),
        ('invent motif in small trees',lambda x:x['triangle_forest_profiles']['rows'][0].__setitem__('motif_size_condition',True)),
        ('claim size condition sufficient',lambda x:x['triangle_forest_profiles'].__setitem__('not_sufficient_for_occurrence',False)),
        ('confuse motif filter with packing exclusion',lambda x:x['triangle_forest_profiles'].__setitem__('no_profile_excludes_packings',False)),
    ]
    rejected=[]
    for name,mutate in damages:
        obj=deepcopy(original);mutate(obj)
        try:verify(obj)
        except (ValueError,KeyError,TypeError,IndexError,ZeroDivisionError):rejected.append(name)
        else:raise ValueError('damaged object accepted: '+name)
    valid=[('endpoint row order',lambda x:x['QQ_cases'].reverse()),
           ('positive rational rescaling',rescale_rf),
           ('facet cycles and positive planes',facet_cycles),
           ('component and seam representation',component_order),
           ('partition and motif representation',profile_order)]
    accepted=[]
    for name,mutate in valid:
        obj=deepcopy(original);mutate(obj);verify(obj);accepted.append(name)
    print(json.dumps({'verified':True,'rejected':rejected,'accepted':accepted,
        'certificate_sha256':hashlib.sha256(data).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
