"""Fail-closed regeneration of all moment-entry budgets and inherited inputs."""
from pathlib import Path
from hashlib import sha256
import argparse, json, sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))

def dependencies():
    manifest = json.loads((HERE/'dependencies.json').read_text())
    root = HERE.parents[2]
    if manifest['schema'] != 'six-sendov-3-moment-entry-dependencies-v1' or len(manifest['files']) != 72:
        raise RuntimeError('dependency metadata')
    if len({item['path'] for item in manifest['files']}) != 72:
        raise RuntimeError('duplicate dependency')
    for item in manifest['files']:
        value = (root/item['path']).read_bytes()
        if len(value) != item['bytes'] or sha256(value).hexdigest() != item['sha256']:
            raise RuntimeError('changed input '+item['path'])

def same(actual, expected, path='record'):
    if type(actual) is not type(expected):
        raise RuntimeError('fixture type '+path)
    if isinstance(actual,dict):
        if actual.keys() != expected.keys():
            raise RuntimeError('fixture fields '+path)
        for key in actual:
            same(actual[key],expected[key],path+'.'+key)
    elif isinstance(actual,list):
        if len(actual) != len(expected):
            raise RuntimeError('fixture length '+path)
        for i,(x,y) in enumerate(zip(actual,expected)):
            same(x,y,path+'.'+str(i))
    elif actual != expected:
        raise RuntimeError('fixture value '+path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture',type=Path,default=HERE/'expected.json')
    parser.add_argument('--freeze',action='store_true')
    args = parser.parse_args()
    expected = None if args.freeze else json.loads(args.fixture.read_text())
    dependencies()
    from checks import build
    result = build()
    if args.freeze:
        args.fixture.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        same(result,expected)
    canonical = json.dumps(result,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({'status':'PASS','record_sha256':sha256(canonical).hexdigest(),
        'new_exact_predicates':len(result['checks']),'credited_baseline_predicates':80,
        'mathematical_damage_rejections':len(result['mathematical_damage_rejections']),
        'input_files':72,'coefficient_radius':'delta^6*2^-1999*eta^7',
        'critical_energy_radius':'delta^2*2^-664*eta^3',
        'sharp_critical_energy_exponent':3,'ordinary_analytic_bridges':'unformalized; independently unreviewed'},sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError,ValueError,OSError,KeyError,TypeError) as error:
        print('REJECT '+str(error),file=sys.stderr)
        raise SystemExit(1)
