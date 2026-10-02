"""Regenerate whole-window scalar budgets and verify unchanged input bytes."""
from pathlib import Path
from hashlib import sha256
import argparse,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))

def dependencies():
    data=json.loads((HERE/'dependencies.json').read_text());root=HERE.parents[2]
    if data['schema']!='six-sendov-3-normalized-neighborhood-dependencies-v1' or len(data['files'])!=61:
        raise RuntimeError('input manifest metadata')
    for entry in data['files']:
        body=(root/entry['path']).read_bytes()
        if len(body)!=entry['bytes'] or sha256(body).hexdigest()!=entry['sha256']:
            raise RuntimeError('changed input '+entry['path'])

def same(a,b,path='record'):
    if type(a)is not type(b):raise RuntimeError('fixture type '+path)
    if isinstance(a,dict):
        if a.keys()!=b.keys():raise RuntimeError('fixture fields '+path)
        for key in a:same(a[key],b[key],path+'.'+key)
    elif isinstance(a,list):
        if len(a)!=len(b):raise RuntimeError('fixture length '+path)
        for j,(u,v) in enumerate(zip(a,b)):same(u,v,path+'.'+str(j))
    elif a!=b:raise RuntimeError('fixture value '+path)

def main():
    p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path,default=HERE/'expected.json');p.add_argument('--freeze',action='store_true');args=p.parse_args()
    expected=None if args.freeze else json.loads(args.fixture.read_text())
    dependencies()
    from bounds import build
    r=build()
    if args.freeze:args.fixture.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    else:same(r,expected)
    canonical=json.dumps(r,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({'status':'PASS','record_sha256':sha256(canonical).hexdigest(),'exact_predicates':len(r['checks']),
        'mathematical_damage_rejections':len(r['mathematical_damage_rejections']),'input_files':61,
        'parameter_radius':'delta*2^-322','coefficient_radius':'delta^6*2^-1999*eta^13',
        'quarter_coefficient_radius':'2^-2017*eta^13','complex_eta_radius':'1/1024','complex_raw_radius':'1/64',
        'eta_max':'1/65536','ordinary_analytic_bridges':'unformalized; new radius independently unreviewed'},sort_keys=True))

if __name__=='__main__':
    try:main()
    except (RuntimeError,ValueError,OSError,KeyError,TypeError) as exc:
        print('REJECT '+str(exc),file=sys.stderr);raise SystemExit(1)
