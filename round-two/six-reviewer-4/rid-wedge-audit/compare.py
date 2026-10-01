"""Compare all common exact numerical claims with the author record.

Reads JSON only; does not execute author code. Own expected.json is regenerated
by check.py, not inferred from these comparisons. All shared entries are compared
as field elements, with different sqrt5 and phi encodings.
"""
import argparse
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import re
from field import S, need

HERE=Path(__file__).resolve().parent

def surd(x):
    m=re.fullmatch(r'\(([^()]*)\)\+\(([^()]*)\)sqrt5',x)
    need(m is not None,'literal sqrt5 encoding')
    a,b=map(F,m.groups());d=a.denominator*b.denominator
    return S(a.numerator*(d//a.denominator),b.numerator*(d//b.denominator),d)

def phi(x):
    need(isinstance(x,list) and len(x)==2 and all(isinstance(a,str) for a in x),'literal phi pair')
    a,b=map(F,x);A=a+b/2;B=b/2;d=A.denominator*B.denominator
    return S(A.numerator*(d//A.denominator),B.numerator*(d//B.denominator),d)

def compare(native,own):
    need(native['original_vertices']==60 and native['proper_group_order']==own['proper_group_size']==60,'body/group counts')
    need(native['supporting_triples']==own['hull']['supporting_triples']==260,'all supporting triples')
    fields={'major_coefficient':'H','wedge_corner_squared_area':'squared_corner_area',
            'minimum_nonzero_facet_sign_corner_margin':'minimum_nonzero_area_sign_margin',
            'maximum_squared_directional_width':'max_squared_directional_width',
            'filter_squared_width_margin':'width_filter_margin',
            'source_minor_face_strict_margin':'target_support_face_margin',
            'paired_radius_ratio':'rho','strict_area_domination_margin':'strict_area_domination_margin'}
    need(len(native['families'])==len(own['wedge_gates'])==2,'both families exactly')
    count=0
    for j,(a,b) in enumerate(zip(native['families'],own['wedge_gates'])):
        need(a['major_axis']==['x','y'][j] and b['major_axis']==j,'family order')
        for u,v in fields.items():need(phi(a[u])==surd(b[v]),'family entry '+u);count+=1
    a=native['example'];b=own['off_mirror_example']
    need(a['original_shadow_hull_size']==b['corners']==18,'actual hull corner count')
    for u,v in [('physical_squared_area','squared_area'),('complete_mirror_maximum_squared_cosine','mirror_cosine_squared'),
                ('minimum_original_height_squared','minimum_original_height_squared')]:
        need(phi(a[u])==surd(b[v]),'physical example entry '+u);count+=1
    for name in ['twofold','fivefold','endpoint']:
        need(phi(a['outside_specified_old_caps'][name]['maximum_positive_squared_cosine'])==
             surd(b['specified_prior_caps'][name]['max_positive_cosine_squared']),'prior cover entry '+name);count+=1
    E={tuple(phi(x) for x in v) for v in native['original_geometry']['equatorial_originals']}
    p=phi(['0','1']);need(E=={(i*p*p,j*(2+p),S()) for i in [-1,1] for j in [-1,1]},'every actual equatorial label');count+=4
    need(native['damaged_controls_rejected']==6,'all six native controls')
    return {'common_exact_field_entries':count,'both_families_compared':True,'every_example_and_named_cover_field_compared':True,
            'trust':'JSON comparison only; independent checker verifies its whole record separately'}

def controls(native,own):
    rejected=[]
    for name in ['missing_family','duplicate_family','wrong_area','wrong_support_face','wrong_cosine','wrong_original']:
        x=copy.deepcopy(native)
        if name=='missing_family':x['families'].pop()
        elif name=='duplicate_family':x['families'][1]=copy.deepcopy(x['families'][0])
        elif name=='wrong_area':x['families'][0]['wedge_corner_squared_area']=['1','0']
        elif name=='wrong_support_face':x['families'][1]['source_minor_face_strict_margin']=['-99/100','158/160']
        elif name=='wrong_cosine':x['example']['complete_mirror_maximum_squared_cosine']=['1','0']
        else:x['original_geometry']['equatorial_originals'][0][0]=['0','0']
        try:compare(x,own)
        except ValueError:rejected.append(name)
        else:raise ValueError('damaged comparison accepted:'+name)
    return rejected

def main():
    p=argparse.ArgumentParser();p.add_argument('native_json');p.add_argument('--controls',action='store_true');a=p.parse_args()
    native=json.loads(Path(a.native_json).read_text());own=json.loads((HERE/'expected.json').read_text())
    result=compare(native,own)
    if a.controls:result['damaged_records_rejected']=controls(native,own)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
