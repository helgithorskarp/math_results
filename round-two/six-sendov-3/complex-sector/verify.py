"""Regenerate the complete certificate; missing/changed source or evidence rejects."""
from pathlib import Path
from hashlib import sha256
import argparse,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))


def check_dependencies():
    data=json.loads((HERE/'dependencies.json').read_text());root=HERE.parents[2]
    if data['source_commit']!='8a29091f0c1fdf3b310c3788987b3441a13fc1d6' or len(data['files'])!=16:
        raise RuntimeError('dependency manifest metadata')
    for entry in data['files']:
        body=(root/entry['path']).read_bytes()
        if len(body)!=entry['bytes'] or sha256(body).hexdigest()!=entry['sha256']:
            raise RuntimeError('dependency bytes '+entry['path'])
    return data['source_commit']


def same(a,b,path='root'):
    if type(a)is not type(b):raise RuntimeError('fixture type '+path)
    if isinstance(a,dict):
        if a.keys()!=b.keys():raise RuntimeError('fixture keys '+path)
        for key in a:same(a[key],b[key],path+'.'+key)
    elif isinstance(a,list):
        if len(a)!=len(b):raise RuntimeError('fixture length '+path)
        for j,(v,w) in enumerate(zip(a,b)):same(v,w,path+'.'+str(j))
    elif a!=b:raise RuntimeError('fixture value '+path)


def build():
    commit=check_dependencies()
    from sector import certificate,require
    from controls import audit
    from audit import audit as kernel
    from alternate import recompute
    kernel_record=kernel();controls=audit();r=certificate()
    same(r,recompute(),'Fraction-endpoint-reference')
    rejected=[]
    controls_damage=('odd-primitive','common-second-primitive','root-radial-acceleration',
                     'heavy-distance-variance','paired-forcing','paired-anchor')
    interval_damage=('lost-second-mixed','odd-normal-sign','heavy-variance-bound')
    for name in controls_damage+interval_damage:
        try:
            if name in controls_damage:audit(name)
            else:certificate(name)
        except (RuntimeError,ValueError):rejected.append(name)
    require(rejected==list(controls_damage+interval_damage),'all nine mathematical damages reject')
    return {'schema':'six-sendov-3-complex-sector-v1','dependency_commit':commit,
            'kernel_audit':kernel_record,'complex_identity_controls':controls,
            'certificate':r,'Fraction_reference_every_field_equal':True,
            'mathematical_damage_rejections':rejected}


def fixture_controls(r):
    rejected=[]
    for label in ('missing-entry','changed-eta','changed-curvature','wrong-type'):
        bad=json.loads(json.dumps(r))
        if label=='missing-entry':bad['certificate']['odd_matrix'][0].pop()
        elif label=='changed-eta':bad['certificate']['eta_max']='1/32768'
        elif label=='changed-curvature':bad['certificate']['common_sigma_cost_div_eta2'][0]='401'
        else:bad['Fraction_reference_every_field_equal']=1
        try:same(r,bad)
        except RuntimeError:rejected.append(label)
    if len(rejected)!=4:raise RuntimeError('full fixture controls')
    return rejected


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture',type=Path,default=HERE/'expected.json')
    parser.add_argument('--freeze',action='store_true');args=parser.parse_args()
    expected=None if args.freeze else json.loads(args.fixture.read_text())
    r=build();tests=fixture_controls(r)
    if args.freeze:args.fixture.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    else:same(r,expected)
    canonical=json.dumps(r,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({'status':'PASS','record_sha256':sha256(canonical).hexdigest(),
                     'dependency_files':16,'kernel_checks':r['kernel_audit']['exact_kernel_checks'],
                     'new_identity_controls':r['complex_identity_controls']['exact_identity_controls'],
                     'whole_positive_eta_records':len(r['complex_identity_controls']['positive_eta_whole_records']),
                     'mathematical_damage_rejections':len(r['mathematical_damage_rejections']),
                     'full_fixture_damage_rejections':tests,'Fraction_reference_every_field_equal':True,
                     'eta_max':'1/65536','centered_imaginary_eigenvalue':'(3,6)eta^2',
                     'common_imaginary_eigenvalue':'(400/3,650/3)eta^2',
                     'least_full12_eigenvalue':'the9164 centered-real eigenvalue',
                     'nonlinear_displacement_radius':'existential at each fixed positive eta'},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (RuntimeError,ValueError,OSError,KeyError,TypeError) as exc:
        print('REJECT '+str(exc),file=sys.stderr);raise SystemExit(1)
