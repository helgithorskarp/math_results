"""Standalone regeneration of every finite field; no theorem checker is imported."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import argparse
import json
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from interval import require
from audit import audit
from initial import exact_initial
from bounds import certify
from reference import recompute


def same(left,right,path='root'):
    require(type(left) is type(right),'fixture type '+path)
    if isinstance(left,dict):
        require(left.keys()==right.keys(),'fixture keys '+path)
        for key in left:
            same(left[key],right[key],path+'.'+key)
    elif isinstance(left,list):
        require(len(left)==len(right),'fixture length '+path)
        for i,(a,b) in enumerate(zip(left,right)):
            same(a,b,path+'.'+str(i))
    else:
        require(left==right,'fixture value '+path)


def comparison():
    e=F(1,65536);a=1-e;kappa=(1+a)*(a-F(5,8));width=F(1,10000)
    require(a>F(7,8) and kappa>F(7,10),'uniform radius and collapsed energy coefficient')
    require(width<kappa/5000,'effective original-root width inherited from7290')
    # (2-eta)[16/(2-eta)-8-4eta] is identically4eta^2.
    product=[0]*3
    for i,u in enumerate((2,-1)):
        for j,v in enumerate((8,4)):
            product[i+j]+=u*v
    cleared=[16-product[0],-product[1],-product[2]]
    require(cleared==[0,0,4],'complete cleared baseline-surplus identity')
    return {'eta_max':str(e),'a_min':str(a),'kappa_lower':str(kappa),
            'known_7290_root_width':'kappa/5000','uniform_root_width':str(width),
            'energy_coefficient_lower':'7/20','global_infimum_gap_lower':'eta+(7/20)E',
            'cleared_baseline_minus_8_plus_4eta_coefficients':list(map(str,cleared))}


def build():
    a=audit();v,j,Y,B,initial=exact_initial();bounds=certify(v,j,Y,B)
    reference=recompute(v,j,Y,B);same(bounds,reference,'fraction-reference')
    rejected=[]
    tests=[('rounding',lambda:audit('rounding')),('mixed-jet',lambda:audit('mixed-jet')),
           ('anchor',lambda:audit('anchor')),('initial-phase',lambda:exact_initial('initial-phase')),
           ('scaled-partial',lambda:exact_initial('scaled-partial')),
           ('initial-jacobian',lambda:exact_initial('initial-jacobian')),
           ('rouche',lambda:certify(v,j,Y,B,'rouche')),
           ('inward-sign',lambda:certify(v,j,Y,B,'inward-sign'))]
    for name,test in tests:
        try:
            test()
        except (RuntimeError,ValueError):
            rejected.append(name)
    require(rejected==[name for name,_ in tests],'every damaged mathematical calculation rejects')
    return {'schema':'six-sendov-3-fixed-box-v1','kernel_audit':a,'exact_initial':initial,
            'interval':bounds,'fraction_reference_every_field_equal':True,
            'collapse_comparison':comparison(),'mathematical_damage_rejections':rejected}


def fixture_controls(record):
    controls=[]
    for name in ('missing-field','altered-curvature','omitted-jacobian-entry','wrong-type'):
        bad=json.loads(json.dumps(record))
        if name=='missing-field':
            del bad['interval']['rouche_margin']
        elif name=='altered-curvature':
            bad['interval']['symmetric_curvature_lower']='23'
        elif name=='omitted-jacobian-entry':
            bad['exact_initial']['jacobian'][0].pop()
        else:
            bad['fraction_reference_every_field_equal']=1
        try:
            same(record,bad)
        except RuntimeError:
            controls.append(name)
    require(len(controls)==4,'every full-fixture damage rejects')
    return controls


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixture',type=Path,default=HERE/'expected.json')
    parser.add_argument('--freeze',action='store_true',help='regenerate the compact exact fixture')
    args=parser.parse_args()
    record=build();controls=fixture_controls(record)
    if args.freeze:
        args.fixture.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    else:
        same(record,json.loads(args.fixture.read_text()))
    canonical=json.dumps(record,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({'status':'PASS','eta_max':'1/65536','parameter_radius':'1/1024',
        'kernel_checks':record['kernel_audit']['exact_kernel_checks'],
        'derivative_monomials':record['kernel_audit']['derivative_monomials'],
        'initial_jacobian_entries':36,'fraction_reference_every_field_equal':True,
        'mathematical_damage_rejections':len(record['mathematical_damage_rejections']),
        'full_fixture_damage_rejections':controls,'record_sha256':sha256(canonical).hexdigest()},sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except (RuntimeError,ValueError,OSError,KeyError,TypeError) as exc:
        print('REJECT '+str(exc),file=sys.stderr)
        raise SystemExit(1)
