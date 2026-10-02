"""Whole radial certificate, dependency-byte and damaged-evidence checker."""
from pathlib import Path
from hashlib import sha256
import argparse,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))


def check_dependencies():
    data=json.loads((HERE/'dependencies.json').read_text());root=HERE.parents[2]
    if data['schema']!='six-sendov-3-radial-dependencies-v1' or len(data['sources'])!=2 or len(data['files'])!=29:
        raise RuntimeError('dependency manifest metadata')
    if data['sources']!=[
            {'commit':'9f8293764732c302d0225150ea018951b14a96db','directory':'round-two/six-sendov-3/complex-sector','files':13},
            {'commit':'8a29091f0c1fdf3b310c3788987b3441a13fc1d6','directory':'round-two/six-sendov-3/centered-real-sector','files':16}]:
        raise RuntimeError('dependency source versions')
    for entry in data['files']:
        body=(root/entry['path']).read_bytes()
        if len(body)!=entry['bytes'] or sha256(body).hexdigest()!=entry['sha256']:
            raise RuntimeError('dependency bytes '+entry['path'])
    return data['sources']


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
    sources=check_dependencies()
    from radial import certificate,require
    from metric_controls import audit
    from arithmetic_check import recompute
    r=certificate();same(r,recompute(),'Fraction-endpoint-reference')
    controls=audit();rejected=[]
    control_damage=('even-primitive','marked-anchor','odd-primitive','heavy-objective-pair',
                    'odd-conjugation-sign','half-squared-modulus','full-radial-factor-four','individual-dual-factor-two')
    interval_damage=('even-normal-sign','odd-normal-sign','objective-pair-factor')
    for name in control_damage+interval_damage:
        try:
            if name in control_damage:audit(name)
            else:certificate(name)
        except (RuntimeError,ValueError):rejected.append(name)
    require(rejected==list(control_damage+interval_damage),'all eleven mathematical damages reject')
    return {'schema':'six-sendov-3-radial-slack-v1','dependency_sources':sources,
            'radial_certificate':r,'literal_metric_controls':controls,
            'Fraction_reference_every_field_equal':True,'mathematical_damage_rejections':rejected}


def fixture_controls(r):
    rejected=[]
    for label in ('missing-normal-entry','changed-slack-weight','changed-window','wrong-type'):
        bad=json.loads(json.dumps(r))
        if label=='missing-normal-entry':bad['radial_certificate']['even_radial_div_eta'][0].pop()
        elif label=='changed-slack-weight':bad['radial_certificate']['individual_root_multipliers'][0][0]='1/4'
        elif label=='changed-window':bad['radial_certificate']['eta_max']='1/32768'
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
                     'dependency_files':29,'new_identity_controls':r['literal_metric_controls']['exact_identity_controls'],
                     'positive_eta_whole_records':len(r['literal_metric_controls']['positive_eta_whole_records']),
                     'mathematical_damage_rejections':len(r['mathematical_damage_rejections']),
                     'full_fixture_damage_rejections':tests,'Fraction_reference_every_field_equal':True,
                     'eta_max':'1/65536','even_radial_det':'>1/16','odd_radial_det':'<-1/100',
                     'signed_four_radial_det_div_eta5':'<-1/6400','individual_root_multipliers':'(1/4,3)',
                     'root_slack_coefficient':'1/4','nonlinear_displacement_radius':'existential at each fixed positive eta'},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (RuntimeError,ValueError,OSError,KeyError,TypeError) as exc:
        print('REJECT '+str(exc),file=sys.stderr);raise SystemExit(1)
