"""Seal source before imports, then independently regenerate the entire exact record."""
import argparse,hashlib,json,pathlib,sys,time
NAMES=['.gitignore', 'BASE-DATA.json', 'COMPARISON.json', 'DEPENDENCIES.json', 'FRESH-BASE.json', 'GEOMETRY.json', 'PROOF.md', 'PROVENANCE.json', 'README.md', 'REVIEW.md', 'SHA256SUMS', 'VALIDATION.json', 'geometry.py', 'interior.py', 'validate.py', 'verify.py']
DAMAGE=('none', 'coefficient', 'parent-coefficient', 'dependency', 'incidence', 'dimension', 'degree', 'norm', 'loop', 'empty', 'margin', 'spectral', 'float', 'boolean', 'key')

def require(ok,msg):
    if not ok:raise ValueError(msg)


def seal(root):
    require(sorted(p.name for p in root.iterdir() if p.is_file())==NAMES,'preimport exact source census')
    lines=(root/'SHA256SUMS').read_text().splitlines();rows=[r.split('  ') for r in lines]
    require(all(len(r)==2 for r in rows),'preimport manifest format')
    require([r[1] for r in rows]==sorted(set(NAMES)-{'SHA256SUMS'}),'preimport full manifest census')
    for sha,name in rows:
        raw=(root/name).read_bytes();require(hashlib.sha256(raw).hexdigest()==sha,'preimport source digest: '+name)
    return hashlib.sha256((root/'SHA256SUMS').read_bytes()).hexdigest()


def equal_tree(actual,expected,where='record'):
    require(type(actual) is type(expected),'whole fixture type: '+where)
    if type(actual) is dict:
        require(actual.keys()==expected.keys(),'whole fixture keys: '+where)
        for k in actual:equal_tree(actual[k],expected[k],where+'.'+k)
    elif type(actual) is list:
        require(len(actual)==len(expected),'whole fixture length: '+where)
        for i,(a,e) in enumerate(zip(actual,expected)):equal_tree(a,e,where+'.'+str(i))
    else:require(actual==expected,'whole fixture value: '+where)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out');p.add_argument('--damage',choices=DAMAGE,default='none');a=p.parse_args();root=pathlib.Path(__file__).resolve().parent
    if a.out:require(root not in pathlib.Path(a.out).resolve().parents,'generated record must be outside source')
    manifest=seal(root);sys.path.insert(0,str(root));from interior import make;from geometry import canon
    start=time.monotonic();r=make(json.loads((root/'BASE-DATA.json').read_text()),json.loads((root/'COMPARISON.json').read_text()),json.loads((root/'GEOMETRY.json').read_text()),a.damage)
    expected_bytes=(root/'FRESH-BASE.json').read_bytes();expected=json.loads(expected_bytes)
    require(canon(expected)+b'\n'==expected_bytes,'whole fixture canonical encoding');equal_tree(json.loads(canon(r)),expected)
    b=canon(r);require(b+b'\n'==expected_bytes,'whole regenerated record bytes')
    if a.out:pathlib.Path(a.out).write_bytes(b+b'\n')
    print(json.dumps(dict(status='PASS',complete=True,whole_record_bytes=len(b),whole_record_sha256=hashlib.sha256(b).hexdigest(),source_manifest_sha256=manifest,seconds=time.monotonic()-start,python=sys.version.split()[0],optimized=bool(sys.flags.optimize))))

if __name__=='__main__':main()
