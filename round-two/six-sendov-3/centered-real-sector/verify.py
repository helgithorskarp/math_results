"""Regenerate and compare every finite certificate field, including under -O."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import argparse,json
from hashlib import sha256
from interval import require
from centered import exact,certify
from audit import audit
from reference import recompute


def same(a,b,path='root'):
    require(type(a) is type(b),'fixture type '+path)
    if isinstance(a,dict):
        require(a.keys()==b.keys(),'fixture keys '+path)
        for k in a:same(a[k],b[k],path+'.'+k)
    elif isinstance(a,list):
        require(len(a)==len(b),'fixture length '+path)
        for j,(x,y) in enumerate(zip(a,b)):same(x,y,path+'.'+str(j))
    else:require(a==b,'fixture value '+path)


def build():
    kernel=audit();v,Y,w0,w1,initial=exact();bounds=certify(v,Y,w0,w1)
    alternate=recompute(v,Y,w0,w1);same(bounds,alternate,'Fraction-endpoint-reference')
    tests=[('rounding',lambda:audit('rounding')),
        ('first-mixed',lambda:audit('mixed-jet')),('second-mixed',lambda:audit('second-mixed')),
        ('marked-anchor',lambda:audit('anchor')),('split-factor',lambda:audit('split-factor')),
        ('split-anchor',lambda:audit('split-anchor')),
        ('lost-second-mixed',lambda:certify(v,Y,w0,w1,'lost-second-mixed')),
        ('curvature-sign',lambda:certify(v,Y,w0,w1,'curvature-sign'))]
    rejected=[]
    for name,operation in tests:
        try:operation()
        except (RuntimeError,ValueError):rejected.append(name)
    require(rejected==[name for name,_ in tests],'all mathematical damages reject')
    return {'schema':'six-sendov-3-centered-real-sector-v1','kernel_audit':kernel,
        'initial':initial,'interval':bounds,'Fraction_reference_every_field_equal':True,
        'mathematical_damage_rejections':rejected}


def fixture_controls(record):
    rejected=[]
    for name in ('missing-entry','altered-bound','changed-domain','wrong-type'):
        bad=json.loads(json.dumps(record))
        if name=='missing-entry':bad['interval']['five_block_enclosure'][0].pop()
        elif name=='altered-bound':bad['interval']['relative_curvature_difference_quotient'][0]='-4'
        elif name=='changed-domain':bad['interval']['eta_interval'][1]='1/32768'
        else:bad['Fraction_reference_every_field_equal']=1
        try:same(record,bad)
        except RuntimeError:rejected.append(name)
    require(len(rejected)==4,'full-fixture controls reject')
    return rejected


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture',type=Path,
        default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--freeze',action='store_true');args=parser.parse_args()
    r=build();controls=fixture_controls(r)
    if args.freeze:args.fixture.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    else:same(r,json.loads(args.fixture.read_text()))
    canonical=json.dumps(r,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({'status':'PASS','eta_max':'1/65536','parameter_radius':'1/1024',
        'kernel_checks':r['kernel_audit']['exact_kernel_checks'],
        'derivative_monomials':r['kernel_audit']['derivative_monomials'],'jet_components':21,
        'full_split_controls':len(r['kernel_audit']['full_split_controls']),
        'centered_eigenvalue_window':'eta^2(1-5eta)<lambda_W<eta^2(1-3eta)',
        'Fraction_reference_every_field_equal':True,'mathematical_damage_rejections':len(r['mathematical_damage_rejections']),
        'full_fixture_damage_rejections':controls,'record_sha256':sha256(canonical).hexdigest()},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (RuntimeError,ValueError,OSError,KeyError,TypeError) as exc:
        print('REJECT '+str(exc),file=sys.stderr);raise SystemExit(1)
