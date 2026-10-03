"""Semantic damage controls for the new chart/normal/derivative bridge.

Same-author checking, not independent researcher review. No assertions,
floats, solver calls or private runtime files. Python3.11 standard library.
"""
from copy import deepcopy
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json,signal
import check as c
from interval import A,I,S
from exact import E
import field as f

HERE=Path(__file__).resolve().parent
def rejected(name,thunk,out):
    try:thunk()
    except (ValueError,ArithmeticError):out.append(name);return
    raise RuntimeError('damaged certificate accepted: '+name)
def change(plan,key,value):
    p=deepcopy(plan);p[key]=value;return p
def run():
    data=json.loads((HERE/'INPUT.json').read_text());plan=json.loads((HERE/'PLAN.json').read_text())
    H,V,B,z0,specialized,units=c.calibrate(data,plan);bad=[]
    for key,value in (('no_actual_thirteenth_point',False),('all_three_added_points_arbitrary',False),('fixed_reference_labels',list(c.CORE[:-1])),('basis_new',[1,2,5]),('sharp_delta_max','1/10000000'),('sharp_three_stability_constant','1330'),('subcritical_parameter_gate','1/1000000')):
        rejected(key,lambda key=key,value=value:c.layout(data,change(plan,key,value)),bad)
    rejected('missing_cross_contact',lambda:c.layout(data,change(plan,'original_twenty_contacts',plan['original_twenty_contacts'][:-1])),bad)
    altered=deepcopy(plan);altered['z0_coefficients'][0]='-114/16'
    rejected('wrong_exact_chart_value',lambda:c.calibrate(data,altered),bad)
    altered=deepcopy(plan);altered['z0_rational_bracket']=['1/2','501/1000']
    rejected('wrong_chart_bracket',lambda:c.calibrate(data,altered),bad)
    altered=deepcopy(data);altered['vectors'][3][0][0]='1'
    rejected('nonunit_reference',lambda:c.calibrate(altered,plan),bad)
    rejected('false_positive_weight_bound',lambda:c.normal_case(H,V,units['p3'],(1,4,7),lambda_lower=Q(1,5)),bad)
    rejected('false_inverse_cube_norm_bound',lambda:c.normal_case(H,V,units['p3'],(1,4,7),cube_norm_upper=Q(8)),bad)
    rejected('wrong_reference_normal',lambda:c.normal_case(H,V,units['p3'],(1,2,7)),bad)
    root=E.positive_root;E.positive_root=f.scale(root,-1)
    try:rejected('negative_exact_radical_branch',lambda:c.points(E(f.T,1,0),E(z0,0,1)),bad)
    finally:E.positive_root=root
    for name,method,broken in (
        ('omitted_product_chain_term','__mul__',lambda a,b:A(a.v*A.cv(b).v,a.dt*A.cv(b).v,a.dz*A.cv(b).v)),
        ('omitted_quotient_chain_term','__truediv__',lambda a,b:A(a.v/A.cv(b).v,a.dt/A.cv(b).v,a.dz/A.cv(b).v)),
        ('omitted_radical_derivative','sqrt',lambda a:A(a.v.sqrt(),0,0))):
        original=getattr(A,method);setattr(A,method,broken)
        try:rejected(name,lambda:c.derivative_box(plan,specialized),bad)
        finally:setattr(A,method,original)
    rejected('zero_straddling_denominator',lambda:I(1)/I(-Q(1,10),Q(1,10)),bad)
    rejected('negative_radical_argument',lambda:I(-1,-Q(1,2)).sqrt(),bad)
    good=[]
    reordered={k:deepcopy(plan[k]) for k in reversed(list(plan))};reordered['nonbinding_comment']='harmless metadata'
    if c.run(data,reordered)['status']!='CHECKED_EXACT_CHART_NORMAL_AND_DERIVATIVE_LOCAL_GATE':raise ValueError('valid reordered plan rejected')
    good.append('reordered_keys_and_metadata')
    if c.normal_case(H,V,units['p3'],(7,4,1))['cube_corners_actually_checked']!=8:raise ValueError('valid normal permutation rejected')
    good.append('consistently_permuted_normal_columns')
    # Closed interval arithmetic encloses both endpoint products and exact root.
    x=I(-Q(3,7),Q(2,3));square=x**2
    if not (Q(square.l,S)<=0 and Q(square.h,S)>=Q(4,9)):raise ValueError('closed square enclosure')
    r=I(2).sqrt()
    if not Q(r.l,S)**2<=2<=Q(r.h,S)**2:raise ValueError('closed radical enclosure')
    good.append('closed_arithmetic_endpoints')
    return {'actual_agent':'six-tammes-2','role':'researcher','status':'SEMANTIC_CONTROLS_PASSED','rejected_count':len(bad),'rejected':bad,'valid_count':len(good),'valid':good,'source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in c.FROZEN+('controls.py',)}}
if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second semantic-control guard')));signal.alarm(50)
    print(json.dumps(run(),sort_keys=True))
