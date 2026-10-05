"""Standalone CLOSED[29/40,3/4] exact verify kernels.
Own ab3798362ba9a701f68923aad5af2ed7dc608863 method provenance only.
No ancestor numerical exclusions, discovery records or peer/reviewer runtime inputs.
Ordinary/unformalized and independently unreviewed; full argument in PROOF.md.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
PINS=('.gitignore','COVER.json','ENTRY_COVER.json','EXPECTED.json','PROOF.md',
      'LITERATURE.md','README.md','core.py','origin.py','product.py','coupled.py',
      'literal.py','homothety.py','check_origin.py','certificate.py','verify.py','validate.py')

def require(ok,message):
    if not ok:raise ValueError(message)

def unique(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,'duplicate JSON key');out[key]=value
    return out

def read(path):return json.loads(path.read_text(),object_pairs_hook=unique)

def seal():
    manifest=read(HERE/'MANIFEST.json')
    require(type(manifest) is dict and set(manifest)=={'files'},'exact manifest schema')
    actual={name:dict(bytes=len((HERE/name).read_bytes()),
        sha256=sha256((HERE/name).read_bytes()).hexdigest()) for name in PINS}
    require(actual==manifest['files'],'manifest preimport whole local source bytes')
    return actual

# The documented author-only emit route is the sole source-generation bypass.
if '--emit' not in sys.argv:
    try:seal()
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)

def local(name):
    spec=importlib.util.spec_from_file_location('combined_twenty_nine_verify_'+name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module
    spec.loader.exec_module(module);return module

k=local('core');c=local('certificate');conditional=local('check_origin')
product=local('product');coupled=local('coupled');literal=local('literal');homothety=local('homothety')
CORE_POLAR=('last-polar-coefficient','drop-polar-series','radial-lower-cap','radial-coefficient','chord-slope')
CORE_ENCLOSURE=('wrong-T-lower','false-empty')
CORE_CENTERED=('centered-third-underpay','newton-eighth')
CORE_JOINT=('uncouple-T','energy-integral-coefficient','ET-last-bivariate-coefficient','ET-last-Bernstein-control')
CONTOUR=('contour-underpay-5','contour-underpay-6','contour-underpay-7')
DAMAGES=tuple(sorted(set(CORE_POLAR+CORE_ENCLOSURE+CORE_CENTERED+CORE_JOINT+CONTOUR)
    |set(conditional.DAMAGES)|set(product.DAMAGES)|set(dict(coupled.DAMAGES))
    |set(literal.DAMAGES)|set(homothety.DAMAGES)|{'omit-face-leaf'}))

def adverse(damage,cover_path,entry_path):
    """Inject one semantic defect into an actual used mathematical component.

    Helpers must reject at their specific gate. The validator disallows the
    final failed-to-reject guard as proof of an intended semantic rejection.
    """
    if damage in conditional.DAMAGES:conditional.compute(damage)
    elif damage in literal.DAMAGES:literal.compute(damage)
    elif damage in homothety.DAMAGES:homothety.compute(damage)
    elif damage in dict(coupled.DAMAGES):coupled.payment(damage)
    elif damage in product.DAMAGES:
        product.payment(k,conditional.WEAK[:10],conditional.WEAK[10:],damage)
    elif damage in CORE_POLAR:
        k.polar_payment(k.LOW,k.H,Q(0),Q(1,8),Q(8),(k.ENERGY-Q(1,8))/2,'first-entry',damage)
    elif damage in CORE_ENCLOSURE:
        k.enclose([k.LOW,k.H,Q(0),k.ENERGY,Q(8),Q(8),k.GAMMA,Q(1),Q(0),k.ENERGY/8],damage)
    elif damage in CORE_CENTERED:k.centered_constants(damage)
    elif damage in CONTOUR:k.origin.contour_cap_payment(damage)
    elif damage in CORE_JOINT:
        cover=read(cover_path);c.face_schema(cover)
        path=next(p for p,r in cover['leaves'].items() if r=='joint-energy-polar')
        box=list(map(Q,cover['root']))
        for i,bit in enumerate(path):
            cut=cover['splits'][path[:i]];axis=cut['axis'];box[2*axis+(bit=='0')]=Q(cut['cut'])
        enc=k.enclose(box[:4]+[Q(8),Q(8)]+box[4:],'')
        require(enc['status']=='nonempty-enclosure','joint adverse has a paid actual necessary enclosure')
        name={'ET-last-bivariate-coefficient':'last-bivariate-coefficient',
              'ET-last-Bernstein-control':'last-Bernstein-control'}.get(damage,damage)
        k.energy_payment(path,enc['tightened'],enc['T'],name)
    elif damage=='omit-face-leaf':
        cover=read(cover_path);cover['leaves'].pop(next(iter(cover['leaves'])))
        c.face_schema(cover)
    else:raise ValueError('unknown semantic damage')
    raise ValueError('semantic damage failed to reject')

def compute(cover_path,entry_path):
    # Full schema/coverage are checked before the expensive polynomial controls.
    c.face_schema(read(cover_path));c.entry_schema(read(entry_path))
    whole=c.run(cover_path=cover_path,entry_path=entry_path)
    raw=json.dumps(whole,sort_keys=True,separators=(',',':')).encode()
    origins=[x for x in whole['all_face_leaf_payments'] if x['role']=='retained-mean-product-origin']
    polars=[x for x in whole['all_face_leaf_payments'] if x['role']!='retained-mean-product-origin']
    least_o=min(origins,key=lambda x:Q(x['origin_margin']))
    least_j=min(polars,key=lambda x:Q(x['polar_margin']))
    expected=dict(agent='six-sendov-1',role='researcher',result='PASS',degree=9,
        marked_interval=['29/40','3/4'],annular_gap='1/10000',fixed_clipped_mass='8',
        full_checked_record_sha256=sha256(raw).hexdigest(),full_checked_record_bytes=len(raw),
        entry_initial_shells=83,entry_cuts=399,entry_leaves=482,entry_reachable_nodes=881,
        closed_face_leaves=368,internal_splits=367,reachable_closed_nodes=735,max_closed_depth=14,
        leaf_role_counts=whole['role_counts'],whole_product_payments=368,
        full_standard_polar_vectors=486,full_ET_matrices=107,ET_matrix_shape=[13,19],
        full_mean_channels=514,both_mean_leaf_pairs=257,full_mean_remainder_matrices=3598,
        mean_matrix_shape=[9,10],full_degree8_controls=514,full_degree9_controls=514,
        whole_cleared_mean_matrices=514,cleared_mean_matrix_shape=[10,10],
        centered_constants=whole['constants'][2:],origin_margin='1/3100',polar_margin='1/2200',
        J_Lipschitz_upper='2/3',O_Lipschitz_upper='5/4',
        least_origin=dict(path=least_o['path'],margin=least_o['origin_margin']),
        least_polar=dict(path=least_j['path'],margin=least_j['polar_margin']),
        full_coupled_payment_sha256=k.digest(whole['fresh_continuity']),
        conditional_controls_sha256=k.digest(whole['conditional_controls']),
        literal_endpoint_sha256={a:k.digest(v) for a,v in whole['both_endpoint_literal_controls'].items()},
        homothety_controls_sha256=k.digest(whole['homothety_controls']),
        all_full_coefficients_controls_and_closed_faces_checked=True,
        ordinary_continuum_proof_supplied=True,formalized=False,independently_reviewed=False,
        whole_lower_disk_numeric_gap_asserted=False,runtime_ancestor_private_or_reviewer_input=False,
        contour_coefficients_published_prior_art=True,
        mathematical_parent_scope='Standalone CLOSED[29/40,3/4]; no parent numeric/exclusion input. '
            'No older-band union theorem or whole lower-disk uniform numerical gap asserted.')
    return expected,raw

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true')
    parser.add_argument('--expected',type=Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--cover',type=Path,default=HERE/'COVER.json')
    parser.add_argument('--entry',type=Path,default=HERE/'ENTRY_COVER.json')
    parser.add_argument('--damage',choices=('',)+DAMAGES,default='')
    parser.add_argument('--record',type=Path);args=parser.parse_args()
    if args.record:require(HERE not in args.record.resolve().parents and args.record.resolve()!=HERE,
        'large regenerated record stays outside publication directory')
    if args.emit:require(not args.damage and args.cover==HERE/'COVER.json'
        and args.entry==HERE/'ENTRY_COVER.json' and args.expected==HERE/'EXPECTED.json',
        'explicit local author emit only')
    before=seal() if not args.emit else None
    # The immutable local EXPECTED bytes are already covered by the source
    # seal. Reject an altered alternate envelope before expensive arithmetic.
    # Every successful run still regenerates and compares the ENTIRE record.
    if not args.emit and args.expected.resolve()!=(HERE/'EXPECTED.json').resolve():
        k.typed_equal(read(args.expected),read(HERE/'EXPECTED.json'))
    if args.damage:adverse(args.damage,args.cover,args.entry)
    expected,raw=compute(args.cover,args.entry)
    if args.emit:args.expected.write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
    else:
        k.typed_equal(expected,read(args.expected))
        require(seal()==before,'whole local source unchanged during complete verification')
    if args.record:args.record.write_bytes(raw)
    print(json.dumps(dict(result='PASS',annular_gap=expected['annular_gap'],
        record_sha256=expected['full_checked_record_sha256'],whole_record_bytes=len(raw),
        entry_rectangles=482,closed_face_leaves=368,whole_coefficients_controls_and_coverage_checked=True,
        formalized=False,independently_reviewed=False)))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,ZeroDivisionError,json.JSONDecodeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
