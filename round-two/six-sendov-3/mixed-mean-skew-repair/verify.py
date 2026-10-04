"""Sealed standalone exact verifier; ordinary author evidence, not review."""
from pathlib import Path
from hashlib import sha256
import argparse,json,os,re,sys

HERE=Path(__file__).resolve().parent
SOURCE_FILES={'arithmetic.py','series.py','constants.py','family.py','calculation.py',
              'verify.py','validate.py','EXPECTED.json','README.md','PROOF.md',
              'DEPENDENCIES.json','LITERATURE.md','.gitignore'}
NATIVE=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
        'VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
for name in NATIVE:os.environ[name]='1'

def require(condition,message):
    if not condition:raise ValueError(message)

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,
                      allow_nan=False).encode('ascii')

def pairs(rows):
    out={}
    for key,value in rows:
        require(key not in out,'duplicate JSON member')
        out[key]=value
    return out

def invalid_number(value):raise ValueError('nonfinite JSON number')

def read_json(path):
    raw=Path(path).read_bytes()
    require(raw.endswith(b'\n'),'canonical JSON final newline')
    x=json.loads(raw,object_pairs_hook=pairs,parse_constant=invalid_number)
    require(raw==canonical(x)+b'\n','whole canonical JSON bytes')
    return x

def keys(x,required,label):
    require(type(x) is dict and set(x)==set(required),'exact '+label+' members')

def natural(x,label):require(type(x) is int and x>=0,'integer '+label)

def digest(x,label):require(type(x) is str and re.fullmatch('[0-9a-f]{64}',x),'SHA256 '+label)

def source_gate():
    x=read_json(HERE/'SOURCE.json')
    keys(x,('schema','files'),'source manifest')
    require(type(x['schema']) is int and x['schema']==1,'source schema version')
    keys(x['files'],SOURCE_FILES,'source files')
    for name in sorted(SOURCE_FILES):
        row=x['files'][name];keys(row,('bytes','sha256'),'source row')
        natural(row['bytes'],'source length');digest(row['sha256'],'source digest')
        raw=(HERE/name).read_bytes()
        require(len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256'],
                'whole pre-import source seal '+name)

def expected_gate(path):
    x=read_json(path)
    keys(x,('schema','agent','role','scope','records'),'expected')
    require(type(x['schema']) is int and x['schema']==1,'expected schema version')
    require(x['agent']=='six-sendov-3' and x['role']=='researcher','actual author role')
    require(x['scope']=='constructed mixed family only; ordinary unformalized author evidence',
            'constructed family expected scope')
    keys(x['records'],('forcing','unit'),'expected stages')
    for stage,row in x['records'].items():
        keys(row,('whole_bytes','whole_sha256','whole_identity_count','original_roots',
                  'critical_moments'),'expected stage')
        for name in ('whole_bytes','whole_identity_count','original_roots','critical_moments'):
            natural(row[name],name)
        digest(row['whole_sha256'],'whole exact record')
        require(row['original_roots']==9 and row['critical_moments']==8,
                'whole expected multiplicity census')
    return x

def same_whole(a,b):
    require(type(a) is type(b),'whole record exact nested type')
    if type(a) is dict:
        require(set(a)==set(b),'whole record exact nested keys')
        for key in a:same_whole(a[key],b[key])
    elif type(a) is list:
        require(len(a)==len(b),'whole record exact vector length')
        for x,y in zip(a,b):same_whole(x,y)
    else:require(a==b,'whole record exact coefficient value')

def summary(record):
    blob=canonical(record)
    return {'whole_bytes':len(blob),'whole_sha256':sha256(blob).hexdigest(),
            'whole_identity_count':record['whole_identity_count'],
            'original_roots':len(record['whole_all9_originals']),
            'critical_moments':len(record['whole_all8_moments'])}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage',choices=('forcing','unit'),default='unit')
    ap.add_argument('--expected',type=Path,default=HERE/'EXPECTED.json')
    ap.add_argument('--output',type=Path)
    ap.add_argument('--check',type=Path,help='compare every type and coefficient with a generated full record')
    ap.add_argument('--damage',choices=('keep_ninth','omit_fifth_binomial','omit_pair_variance',
        'reverse_skew_forcing','missing_ninth','outward_tenth','omit_seventh',
        'omit_ninth_center','omit_ninth_scale','wrong_cost_cross','wrong_motion_winner'),
        help=argparse.SUPPRESS)
    args=ap.parse_args()
    source_gate();expected=expected_gate(args.expected)
    if args.output:
        require(not args.output.resolve().is_relative_to(HERE),'generated record must be outside source')
    sys.path.insert(0,str(HERE))
    from calculation import build
    for name in ('arithmetic','series','constants','family','calculation'):
        require(Path(sys.modules[name].__file__).resolve()==HERE/(name+'.py'),
                'sealed local mathematical import '+name)
    record=build(args.stage,args.damage)
    require(type(record) is dict,'whole generated record')
    actual=summary(record)
    same_whole(actual,expected['records'][args.stage])
    if args.check:same_whole(record,read_json(args.check))
    if args.output:args.output.write_bytes(canonical(record)+b'\n')
    print(canonical({'agent':'six-sendov-3','role':'researcher','stage':args.stage,
                     'status':'all whole exact checks passed; ordinary analytic bridges unformalized',
                     **actual}).decode('ascii'),flush=True)

if __name__=='__main__':main()
