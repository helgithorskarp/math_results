"""Whole-source/preimport input seal and strict entire-record comparison."""
from pathlib import Path
from hashlib import sha256
import argparse,json,sys
HERE=Path(__file__).resolve().parent
NAMES={'.gitignore','DEPENDENCIES.json','EXPECTED.json','LITERATURE.md','PROOF.md',
       'README.md','SHA256SUMS','VALIDATION.json','arithmetic.py','means.py',
       'provenance.json','series.py','validate.py','verify.py'}
BASELINE_SHA256='d00486db2576f1be9de39483d374b68c4223a8193bf0f7374bd37b3c9d14cccd'
def unique(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError('duplicate JSON key '+k)
        out[k]=v
    return out
def parsed(raw):
    return json.loads(raw,object_pairs_hook=unique,
        parse_constant=lambda token:(_ for _ in ()).throw(ValueError('nonfinite JSON '+token)))
def same(a,b,path='record'):
    if type(a) is not type(b):raise ValueError('WHOLE CANONICAL strict type '+path)
    if isinstance(a,dict):
        if set(a)!=set(b):raise ValueError('WHOLE CANONICAL keys '+path)
        for k in a:same(a[k],b[k],path+'/'+k)
    elif isinstance(a,list):
        if len(a)!=len(b):raise ValueError('WHOLE CANONICAL length '+path)
        for i,(x,y) in enumerate(zip(a,b)):same(x,y,path+'/'+str(i))
    elif a!=b:raise ValueError('WHOLE CANONICAL value '+path)
def seals(baseline):
    if {p.name for p in HERE.iterdir()}!=NAMES:raise ValueError('SOURCE exact file set')
    manifest={}
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if name in manifest:raise ValueError('SOURCE duplicate manifest')
        manifest[name]=digest
    if set(manifest)!=NAMES-{'SHA256SUMS'}:raise ValueError('SOURCE complete manifest')
    for name,digest in manifest.items():
        if sha256((HERE/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('SOURCE SHA256 '+name)
    raw=baseline.read_bytes()
    if len(raw)!=150740 or sha256(raw).hexdigest()!=BASELINE_SHA256:
        raise ValueError('PREIMPORT whole public10212 fixture')
    parsed(raw)
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--baseline',type=Path,default=HERE.parent/'optimal-cap-construction/EXPECTED.json')
    parser.add_argument('--damage',choices=('unbalanced_mean','freeze_third','omit_pair_compensation',
        'drop_quadratic_pair','wrong_cost_linear','wrong_dual','outward_ninth','wrong_positivity'))
    args=parser.parse_args()
    seals(args.baseline)
    expected=parsed((HERE/'EXPECTED.json').read_bytes())
    sys.path.insert(0,str(HERE))
    import means
    actual=means.build(args.baseline,args.damage)
    same(actual,expected)
    blob=means.canonical(actual)
    print(json.dumps({'agent':'six-sendov-3','role':'researcher','complete':True,
        'whole_identities':len(actual['whole_identities']),
        'positive_rational_signs':len(actual['positive_rational_signs']),
        'whole_record_bytes':len(blob),'whole_record_sha256':sha256(blob).hexdigest(),
        'whole_baseline_sha256':BASELINE_SHA256,
        'analytic_bridges_unformalized':True,'independent_review':False},sort_keys=True))
if __name__=='__main__':main()
