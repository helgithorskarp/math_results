#!/usr/bin/env python3
"""Direct closed mass-eight cover and complete coupled annular gap checks.

Exact Fraction arithmetic; same author, ordinary unformalized analytic bridges.
Every full coefficient/control representation is checked before extrema/hash.
Default runtime uses only compact LOCAL files; large regenerated records are outputs.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from math import comb
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
PINS=('.gitignore','COVER.json','EXPECTED.json','PROOF.md','LITERATURE.md','README.md',
      'core.py','origin.py','check_origin.py','product.py','coupled.py','literal.py',
      'verify.py','validate.py')

def require(ok,message):
    if not ok:raise ValueError(message)

def unique_object(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,'duplicate JSON object key')
        out[key]=value
    return out

def load_json(path):
    return json.loads(path.read_text(),object_pairs_hook=unique_object)

def source_seal():
    manifest=load_json(HERE/'MANIFEST.json')
    require(type(manifest) is dict and set(manifest)=={'files'},'exact manifest schema')
    actual={name:dict(bytes=len((HERE/name).read_bytes()),
        sha256=sha256((HERE/name).read_bytes()).hexdigest()) for name in PINS}
    require(actual==manifest['files'],'manifest preimport whole local source bytes')
    return actual

# Source is checked before ANY mathematical helper import. --emit is the
# explicitly documented author's generation path, not production verification.
if '--emit' not in sys.argv:
    try:source_seal()
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)

def local_module(name):
    spec=importlib.util.spec_from_file_location('mass_eight_'+name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module
    spec.loader.exec_module(module);return module

k=local_module('core');product=local_module('product');coupled=local_module('coupled')
literal=local_module('literal');conditional=local_module('check_origin')
ROOT4=(k.LOW,k.H,Q(0),k.ENERGY,k.GAMMA,Q(1),Q(0),k.ENERGY/8)
ROLES={'scalar-product-origin','retained-mean-product-origin',
       'standard-polar','joint-energy-polar'}
ORIGIN_MARGIN=Q(1,100);POLAR_MARGIN=Q(1,600);ENTRY_TARGET=Q(49,50)

def entry(damage):
    require(k.BM==1-k.H**2 and k.BX==1-k.LOW**2 and
        k.AB==min(k.LOW*(1-k.LOW**2),k.H*(1-k.H**2)),
        'whole marked endpoint budgets')
    require(k.C==k.LOW+1-k.LOW**2-k.H and k.GAMMA==k.MASS/8-k.ENERGY/16,
        'whole chord and conservative mean budgets')
    require(k.TM==56*(1-1/(1+k.H))**2,'whole global radial budget')
    mass=k.power([k.H,k.C*k.MASS/8],8)
    require(mass==[comb(8,i)*k.H**(8-i)*(k.C*k.MASS/8)**i for i in range(9)],
        'ALL9 scalar mass coefficients')
    ma=k.integral(mass);slope=k.C*k.MASS/8
    require(ma==((k.H+slope)**9-k.H**9)/(9*slope)<ENTRY_TARGET,
        'whole antiderivative and conservative mass floor')
    shells=[]
    for index in range(73):
        tl=Q(index,8);th=min(k.TM,Q(index+1,8));phase=max(Q(0),(k.ENERGY-th)/2)
        paid=k.polar_payment(k.LOW,k.H,tl,th,Q(8),phase,'energy-'+str(index),damage)
        require(Q(paid['integral'])<ENTRY_TARGET,'whole strict energy-shell exclusion '+str(index))
        shells.append(paid)
    require(Q(shells[0]['T'][0])==0 and Q(shells[-1]['T'][1])==k.TM
        and all(a['T'][1]==b['T'][0] for a,b in zip(shells,shells[1:])),
        'all73 complete closed energy shells')
    return dict(mass_coefficients=mass,mass_integral=ma,energy_shell=shells)

def cover_schema(cover):
    require(type(cover) is dict and set(cover)=={'root','splits','leaves'},'exact face cover schema')
    k.typed_equal(cover['root'],k.strings(ROOT4),'face-root')
    splits,leaves=cover['splits'],cover['leaves']
    require(type(splits) is dict and type(leaves) is dict,'face dictionary types')
    require(all(type(path) is str and set(path)<={'0','1'} and len(path)<=13
        and type(obj) is dict and set(obj)=={'axis','cut'}
        and type(obj['axis']) is int and 0<=obj['axis']<4
        and type(obj['cut']) is str for path,obj in splits.items()),
        'exact face cut path/axis/rational types')
    require(all(type(path) is str and set(path)<={'0','1'} and len(path)<=13
        and type(role) is str and role in ROLES for path,role in leaves.items()),
        'exact face leaf path/role types')
    require(set(splits).isdisjoint(leaves),'face internal/leaf disjointness')
    return splits,leaves

def compute(damage='',cover_path=None):
    # Conditional fixtures make anchor/norm defects meaningful even if an
    # active endpoint is absent in a particular fixed face cell.
    if damage in conditional.DAMAGES:conditional.compute(damage)
    if damage in literal.DAMAGES:literal.compute(damage)
    if damage in dict(coupled.DAMAGES):coupled.payment(damage)
    if damage in product.DAMAGES:
        product.payment(k,conditional.WEAK[:10],conditional.WEAK[10:],damage)
    entered=entry(damage)
    constants,derivations=k.centered_constants(damage)
    cover=load_json(cover_path or HERE/'COVER.json');splits,leaves=cover_schema(cover)
    if damage=='omit-face-leaf':
        leaves=leaves.copy();leaves.pop(next(iter(leaves)))
    visited=set();rows=[];cuts=[]
    def walk(path,box):
        require(path not in visited and len(path)<=13,'unique bounded reachable face path')
        visited.add(path)
        require(all(ROOT4[2*j]<=box[2*j]<box[2*j+1]<=ROOT4[2*j+1] for j in range(4)),
            'whole closed face containment '+path)
        if path in splits:
            axis=splits[path]['axis'];text=splits[path]['cut'];cut=Q(text)
            require(str(cut)==text and box[2*axis]<cut<box[2*axis+1],
                'strict canonical rational face parent cut '+path)
            low,high=list(box),list(box);low[2*axis+1]=cut;high[2*axis]=cut
            require(low[2*axis]==box[2*axis] and low[2*axis+1]==high[2*axis]
                and high[2*axis+1]==box[2*axis+1]
                and all(low[j]==high[j]==box[j] for j in range(8) if j not in (2*axis,2*axis+1)),
                'both whole closed face children retain all other axes')
            cuts.append(dict(path=path,box=k.strings(box),axis=axis,cut=text))
            walk(path+'0',tuple(low));walk(path+'1',tuple(high));return
        require(path in leaves,'missing closed face leaf '+path)
        face=tuple(box[:4])+(Q(8),Q(8))+tuple(box[4:])
        enc=k.enclose(face,damage)
        require(enc['status']=='nonempty-enclosure','complete usable necessary face enclosure '+path)
        tight,radial=enc['tightened'],enc['T']
        ori=k.origin_payment(path,tight,radial,constants,damage)
        require(ori['status']=='bounded','whole bounded scalar origin on EVERY face leaf '+path)
        paid_product=product.payment(k,tight,radial,damage)
        cap=Q(paid_product['actual_origin_product_upper'])
        require(0<cap<=1,'whole positive face product cap')
        role=leaves[path]
        row=dict(path=path,compact_box=k.strings(box),face_box=k.strings(face),
            role=role,enclosure=enc,origin=ori,product=paid_product)
        if role in ('scalar-product-origin','retained-mean-product-origin'):
            score=Q(ori['score'])
            if role=='retained-mean-product-origin':
                attempts=[k.origin.payment(tight+radial,mode,damage) for mode in ('energy','joint')]
                require(len(attempts)==2 and all(a['status']=='bounded' for a in attempts),
                    'BOTH whole retained mean channels bounded '+path)
                row['both_mean_origin_channels']=k.clean(attempts)
                selected=max(attempts,key=lambda a:a['score'])
                row['selected_mean_origin']=k.clean(selected);score=Q(selected['score'])
            require(score-cap>ORIGIN_MARGIN and
                100*(score.numerator*cap.denominator-cap.numerator*score.denominator)>
                    score.denominator*cap.denominator,
                'whole strict origin margin by rational and integer signs '+path)
            row.update(status='origin-product-face',score=str(score),product_margin=str(score-cap))
        else:
            al,ah,el,eh,fl,fh,ul,uh,wl,wh=map(Q,tight);tl,th=map(Q,radial)
            polar=k.polar_payment(al,ah,tl,th,fh,max(Q(0),fl-8*uh),path,damage)
            row['standard_polar']=polar
            if role=='joint-energy-polar':
                et_damage={'ET-last-bivariate-coefficient':'last-bivariate-coefficient',
                    'ET-last-Bernstein-control':'last-Bernstein-control'}.get(damage,damage)
                energy=k.energy_payment(path,tight,radial,et_damage);row['energy_polar']=energy
                upper=Q(energy['integral_upper'])
            else:upper=Q(polar['integral'])
            require(1-upper>POLAR_MARGIN and 600*upper.numerator<599*upper.denominator,
                'whole strict polar margin by rational and integer signs '+path)
            row.update(status='polar-face',upper=str(upper),polar_margin=str(1-upper))
        rows.append(row)
    walk('',ROOT4)
    require(visited==set(splits)|set(leaves),'all face entries reached without missing nodes')
    require(len(visited)==277 and len(splits)==138 and len(leaves)==139,'whole fixed face census')
    counts={role:sum(row['role']==role for row in rows) for role in sorted(ROLES)}
    require(counts=={'scalar-product-origin':79,'retained-mean-product-origin':9,
        'standard-polar':2,'joint-energy-polar':49},'complete defining face role census')
    gap=coupled.payment(damage)
    require(gap['epsilon']==Q(1,350) and gap['origin_margin']==ORIGIN_MARGIN
        and gap['polar_margin']==POLAR_MARGIN and gap['entry_target']==ENTRY_TARGET,
        'coupled continuity pays exactly the new complete face targets')
    controls=conditional.compute()
    literal_records={str(a):literal.compute(endpoint=a) for a in (k.LOW,k.H)}
    whole=k.clean(dict(entry=entered,centered_constants=constants,constant_derivations=derivations,
        cover=cover,all_cut_payments=cuts,coupled_leaves=rows,coupled_continuity=gap,
        conditional_origin_controls=controls,both_endpoint_literal_controls=literal_records,
        ordinary_trust='Communication, Gauss--Lucas, Hermite, centered/mean/Bernstein/clipping '
          'bridges and REAL Hilbert Banach are ordinary unformalized premises. '
          'Published10274 excludesF<=8; this direct local face certificate pays the stronger gap.'))
    origins=[row for row in rows if row['status']=='origin-product-face']
    polars=[row for row in rows if row['status']=='polar-face']
    least_o=min(origins,key=lambda row:Q(row['product_margin']))
    least_j=min(polars,key=lambda row:Q(row['polar_margin']))
    expected=dict(agent='six-sendov-1',role='researcher',result='PASS',
        degree=9,marked_interval=k.strings([k.LOW,k.H]),annular_gap='1/350',fixed_clipped_mass='8',
        full_checked_record_sha256=k.digest(whole),energy_shell_cells=73,
        closed_face_leaves=139,internal_splits=138,reachable_closed_nodes=277,
        max_closed_depth=max(map(len,leaves)),leaf_role_counts=counts,
        full_scalar_origin_vectors=7*len(rows),whole_product_payments=len(rows),
        full_standard_polar_vectors=73+51,full_ET_matrices=49,ET_matrix_shape=[13,19],
        full_mean_channels=18,both_mean_leaf_pairs=9,full_mean_remainder_matrices=126,
        mean_matrix_shape=[9,10],full_degree8_controls=18,full_degree9_controls=18,
        whole_cleared_mean_matrices=18,cleared_mean_matrix_shape=[10,10],
        origin_margin='1/100',polar_margin='1/600',J_Lipschitz_upper='7/12',O_Lipschitz_upper='6/5',
        least_origin=dict(path=least_o['path'],margin=least_o['product_margin']),
        least_polar=dict(path=least_j['path'],margin=least_j['polar_margin']),
        full_coupled_payment_sha256=k.digest(whole['coupled_continuity']),
        conditional_controls_sha256=k.digest(controls),
        literal_endpoint_sha256={a:k.digest(v) for a,v in literal_records.items()},
        literal_fixtures=12,literal_points=36,literal_slot_gradients=576,
        literal_primitive_coefficients=360,literal_critical_slots=288,
        literal_affine_derivative_coefficients=648,wrong_normalization_controls=24,
        all_full_coefficients_controls_and_closed_faces_checked=True,
        formalized=False,independently_reviewed=False,whole_lower_disk_numeric_gap_asserted=False,
        runtime_ancestor_private_or_reviewer_input=False,
        mathematical_parent_scope='10274 ordinary exclusionF<=8 on sameclosedannulus; no parent numerical constant input')
    return expected,whole

CORE_DAMAGES=('last-polar-coefficient','drop-polar-series','radial-lower-cap',
    'radial-coefficient','chord-slope','wrong-T-lower','uncouple-energy',
    'centered-third-underpay','newton-eighth','origin-odd-root','origin-drop-eighth',
    'false-empty','unsafe-anchor','last-bivariate-coefficient','uncouple-T',
    'energy-integral-coefficient','last-Bernstein-control','omit-face-leaf',
    'ET-last-bivariate-coefficient','ET-last-Bernstein-control')
DAMAGES=tuple(sorted(set(CORE_DAMAGES)|set(conditional.DAMAGES)|set(product.DAMAGES)
    |set(dict(coupled.DAMAGES))|set(literal.DAMAGES)))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true')
    parser.add_argument('--expected',type=Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--cover',type=Path,default=HERE/'COVER.json')
    parser.add_argument('--damage',default='',choices=('',)+DAMAGES)
    parser.add_argument('--record',type=Path,help='Optional large PRIVATE output outside source directory')
    args=parser.parse_args()
    if args.record:require(HERE not in args.record.resolve().parents and args.record.resolve()!=HERE,
        'large regenerated record stays outside publication directory')
    if args.emit:require(not args.damage and args.expected==HERE/'EXPECTED.json'
        and args.cover==HERE/'COVER.json','explicit local author emit only')
    before=source_seal() if not args.emit else None
    expected,whole=compute(args.damage,args.cover)
    if args.emit:args.expected.write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
    else:
        k.typed_equal(expected,load_json(args.expected))
        require(source_seal()==before,'whole local source unchanged during complete verification')
    if args.record:args.record.write_bytes(k.canonical(whole)+b'\n')
    print(json.dumps(dict(result='PASS',annular_gap=expected['annular_gap'],
        record_sha256=expected['full_checked_record_sha256'],closed_face_leaves=139,
        whole_coefficients_controls_and_coverage_checked=True,formalized=False,independently_reviewed=False)))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,ZeroDivisionError,json.JSONDecodeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
