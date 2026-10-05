"""Source before mathematical data; exact reader with no result-file writes.

The manifest is compact integrity evidence, not an adversarial trust root.
The independently inspectable engine digest is also pinned in this reader.
Only the standard library is used. No parent or peer executable is loaded.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import types

ROOT=Path(__file__).resolve().parent
ENGINE_SHA256='48b32422ba2bfbbe6e1bcbd028c424676995b31f36b8c356ba2227c977c24b1e'
CODE=('verify.py','damage.py','check.py')
TEXT=('.gitignore','README.md','PROOF.md','DEPENDENCIES.json','VALIDATION.json','EDITORIAL.json')
DATA=('CANDIDATE.json','COMPARISON.json','CLAIM.json','EXACT-RESULT.json')


def require(ok,message):
    if not ok:raise ValueError(message)


def sealed_bytes(root,name,manifest):
    path=root/name
    require(path.is_file() and not path.is_symlink(),'missing or linked sealed file: '+name)
    raw=path.read_bytes();item=manifest[name]
    require(len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['SHA256'],
            'whole sealed file changed: '+name)
    return raw


def source_gate(root=ROOT):
    root=Path(root)
    raw=(root/'MANIFEST.json').read_bytes()
    require(len(raw)<=12000,'bounded integrity manifest')
    manifest=json.loads(raw)['files']
    require(set(manifest)==set(CODE+TEXT+DATA),'exact coherent manifest inventory')
    require(all(type(x['bytes']) is int and 0<=x['bytes']<=60000 for x in manifest.values())
            and sum(x['bytes'] for x in manifest.values())<=150000,'bounded compact source')
    require(manifest['check.py']['SHA256']==ENGINE_SHA256,'pinned exact engine digest')
    sources={name:sealed_bytes(root,name,manifest) for name in CODE}
    for name in TEXT:sealed_bytes(root,name,manifest)
    # No candidate, comparison, scalar claim or EXPECTED data read before here.
    engine=types.ModuleType('q18_exact_engine')
    engine.__file__=str(root/'check.py')
    exec(compile(sources['check.py'],engine.__file__,'exec'),engine.__dict__)
    return engine,manifest


def read_inputs(root,manifest):
    return {name:json.loads(sealed_bytes(Path(root),name,manifest)) for name in DATA}


def validate_claim(claim,result):
    require(claim['tau_min']=='0' and 0<F(claim['tau_max'])<=F(1,128),
            'stated real interval lies inside paid sharp-attainment premise')
    require(F(claim['tau_max'])/220<=F(result['actual_min_entry_C_units'])/220
            and F(claim['original_entry_floor'])<=F(result['actual_min_entry_C_units'])/220,
            'uniform actual floor including the empty loop')
    require(0<F(claim['proper_C_floor'])<=F(result['proper_C_starperp_floor']),
            'new full proper floor is paid by the weighted factors')
    require([F(x) for x in claim['weights']]==[F(result['weight_ZZ_WW'])]*2+[F(result['weight_bcW'])],
            'all81 literal weights match the claimed NS aggregate')
    alpha=F(result['maximum_original_E2_weight_product'])
    require(F(claim['alpha'])==alpha and alpha>0,'literal maximum E2 product in the Schur budget')
    Q=F(result['Q']);cap=F(result['old_BB_cap']);gap=Q-cap
    require(F(claim['weighted_gap_lower'])<gap,'strict original weighted Schur crossing')
    require(F(claim['fiber_Delta_lower'])<gap/(2*alpha),
            'all-real fiber gap uses the original dual half factor')
    qlo=F(claim['witness_norm_lower']);caphigh=F(claim['optimizer_norm_upper'])
    require(qlo>0 and caphigh>0 and qlo*qlo<58*Q and caphigh*caphigh>58*cap,
            'exact rational separators for both NS vector norms')
    distance=F(claim['NS_vector_distance_lower'])
    require(0<distance<=qlo-caphigh,'strict vector distance follows from the two norm separators')
    delta=F(claim['original_NS_entry_distance_lower'])
    require(delta>0 and 58*(220*F(result['weight_l1'])*delta)**2<distance**2,
            'original NS movement pays all58 coordinates and the220 normalization')
    require(claim['quantification']=='ALL original individual-real feasible competitors'
            and claim['independent_review_claimed'] is False,
            'ordinary real quantifiers and independent-review boundary')


def verify(root=ROOT):
    engine,manifest=source_gate(root);inputs=read_inputs(root,manifest)
    result=engine.check(inputs['CANDIDATE.json'],inputs['COMPARISON.json'])
    require(result==inputs['EXACT-RESULT.json'],'ENTIRE exact computed record including ALL pivots and58 coordinates')
    validate_claim(inputs['CLAIM.json'],result)
    return json.dumps(result,indent=2)+'\n'


if __name__=='__main__':
    require(len(sys.argv)==1,'reader takes no input overrides')
    sys.stdout.write(verify())
