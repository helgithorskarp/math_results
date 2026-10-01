"""Replay pinned prerequisites and certify all new rational stability bounds.

Python >=3.11, standard library only. The geometric error propagation is
proved in PROOF.md; this checker is not a proof-assistant formalization.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
from models import Models, LO, HI, PIECES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EPSILON = Q(1, 10**13)
EXPECTED_EDGES = ((0,5),(0,6),(0,7),(0,11),(0,14),(1,2),(1,3),(1,4),
                  (1,10),(1,12),(2,4),(2,8),(2,10),(2,13),(3,4),(4,8),
                  (5,7),(5,9),(5,11),(6,8),(6,11),(6,14),(7,12),(8,13),
                  (9,10),(9,11),(9,13),(10,12))


def need(ok,message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def validate_config(c):
    need(c['format']==1, 'certificate format')
    need(c['epsilon']==[1,10**13], 'fixed contact tolerance')
    need(c['interval']==[[14,25],[593,1000]], 'fixed closed interval')
    need(c['bernstein_subintervals']==4, 'four complete closed subintervals')
    need(c['edges']==[list(e) for e in EXPECTED_EDGES], 'exact twenty-eight edges')
    need(c['bounds']=={
        'inverse_row_l1':5, 'reflection_inverse_column_l1':3,
        'A_coefficient_l1':3, 'model_coefficient_l1':3,
        'model_derivative_l1':18, 'parameter_error':30000,
        'ungauged_coordinate_error':2000000, 'gauge_growth':10,
    }, 'fixed quantitative certificate bounds')


def load_prerequisites(root,c):
    for name,sha in c['prerequisite_files_sha256'].items():
        p = Path(name)
        need(not p.is_absolute() and '..' not in p.parts, 'relative pinned prerequisite')
        need(hashlib.sha256((root/p).read_bytes()).hexdigest()==sha, 'pinned source '+name)
    parent = root/'tammes15_contact_pattern_obstruction'
    sys.path.insert(0,str(parent))
    # The published core module imports its sibling under the name "verify".
    sys.modules.pop('verify',None)
    import verify as base
    spec = importlib.util.spec_from_file_location('pinned_contact_core',parent/'verify_contact_core.py')
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    return base,core


def scalar_bridges(epsilon=EPSILON):
    need(0<=epsilon<=Q(1,10**13), 'contact tolerance range')
    need(epsilon<=Q(1,10000), 'anchor/reflection stability range')
    need(1-Q(3,5)**2>=Q(4,5)**2, 'anchor square-root lower bound')
    need(Q(3,5)**2<=1-Q(3,5)**2, 'square-root derivative at most one')
    need(Q(3,5)**2<=4*(1-Q(3,5)**2)**3, 'inverse-square-root derivative at most two')
    need(3*2+Q(1,4)*2<=7, 'anchor second-coordinate error seven')
    need(Q(5,16)+7*Q(1,10000)<Q(1,2), 'anchor transverse coordinate')
    need(1-Q(3,5)**2-Q(1,2)**2>Q(1,2)**2, 'anchor normal coordinate')
    need(Q(6,5)+7<9 and 1+7+9==17, 'anchor error seventeen')
    need(2+2*(LO-Q(1,10000))>=Q(8,5)**2, 'triangle reflection denominator')
    need(2*Q(3,5)/Q(8,5)<=Q(3,4), 'triangle axial coordinate')
    need(2-2*HI>=Q(4,5)**2, 'triangle transverse denominator')
    need(1-Q(3,4)**2-4*Q(1,10000)**2>Q(1,2)**2, 'triangle normal coordinate')
    need(3+16*Q(1,10000)<=4 and 10+4+4<=20, 'reflection error twenty')
    need(10*Q(1,10000)<Q(4,5) and 2*(1-HI)>Q(4,5)**2,
         'same triangle-reflection branch forbidden')
    delta = 161*epsilon
    need(Q(10,3)<4, 'projection error below twice delta')
    need(Q(51,100)<Q(3,4)**2, 'old common-neighbor projection below three quarters')
    need(Q(3,4)+2*delta<Q(4,5), 'new normal amplitude above three fifths')
    need(Q(7,10)+Q(3,5)>1, 'normal rationalization denominator')
    need(6*delta<=1000*epsilon, 'reflected V error one thousand')
    need(2*(1-HI)>Q(9,10)**2 and Q(9,10)-41*epsilon>Q(4,5)
         and 6*delta<Q(4,5), 'coincident common-neighbor branch forbidden')
    need(161+2*1000==2161 and 3*5*2161<40000,
         'linear-system Euclidean U error forty thousand')
    need(Q(3,2)*(40000+1000)<64000, 'W error sixty-four thousand')
    need(80+3*3*64000<600000, 'all-block error six hundred thousand')
    need(40000*epsilon<1 and 3*40000==120000, 'augmented determinant error')
    need(120000*epsilon<Q(1,10), 'negative orientation excluded')
    need(120000*Q(5,2)/10==30000, 'parameter error thirty thousand')
    # Exact B-anchor path has derivative norms at most six.
    need(Q(1,5)*Q(5,4)+Q(3,5)*Q(1,4)*Q(5,4)**3<1,
         'B-anchor beta derivative below one')
    need(2*(Q(3,5)+Q(5,16))<2 and 1+1+2<=6,
         'B-anchor gamma and full derivative bounds')
    need(600000+(18+6*3)*30000<2000000,
         'ungauged metric error below two million')
    need(2+4*Q(5,4)<=10, 'two rotations give gauge growth at most ten')
    need(10*2000000*epsilon<=Q(1,400000), 'entry into pinned local exclusion radius')
    need(4*LO**4-2*LO**3+3*LO**2-1<0 and (-6)**2-4*16*6<0,
         'published N14 comparison covers strict improvements')
    return {'cross_contact_error':161,'reflected_V_error':1000,
            'U_error':40000,'W_error':64000,'block_error':600000,
            'determinant_error':120000,'parameter_error':30000,
            'ungauged_coordinate_error':2000000,'gauge_growth':10}


def exact_identities(m):
    b,R = m.base,m.R
    one,t = m.one,m.t
    need(len(m.edges)==28 and m.edges==list(EXPECTED_EDGES), 'derived spanning contact graph')
    for group in (m.A,m.B):
        for v in group.values(): need(m.dot(v,v)==one, 'exact block unit norm')
    need(all(m.dot(m.A[i],m.A[j])==m.k for i,j in ((6,7),(6,9),(7,9))),
         'exact reflected equilateral triangle')
    need(m.dot(m.v,m.v)==one and m.dot(m.v,m.B[10])==t and m.dot(m.v,m.B[13])==t,
         'exact other common neighbor')
    need(m.mu**2==(one-t)**2*(one+2*t)*m.q2, 'both physical orientations exhaust signs')
    for branch in m.branches.values():
        need(branch['det']==branch['gramdet']*(one-m.dot(branch['u'],branch['u'])),
             'augmented determinant identity')
    a=R((-54,-12,140,-96,234),(4,))
    bb=R((-31,-38,136,-106,195),(4,))
    cc=R((81,42,-276,202,-429),(4,))
    target=((a,bb,cc),(cc,a,bb),(bb,cc,a))
    s=m.branches[1]['model']
    root_zero=lambda f: not b.prem(f.n,b.F)
    for i,ai in enumerate((0,5,11)):
        for j,bj in enumerate((1,2,4)):
            need(root_zero(m.dot(s[ai],s[bj])-target[i][j]), 'incumbent cross Gram at the root')
    for v in s.values(): need(root_zero(m.dot(v,v)-one), 'full comparison model unit at the root')
    for i,j in m.edges+[(3,7),(3,14)]:
        need(root_zero(m.dot(s[i],s[j])-t), 'all thirty incumbent contacts at the root')


def verify_bounds(m):
    funcs=m.functions()
    ranges={name:m.bound(f) for name,f in funcs.items()}
    def within(name,lo,hi):
        a,b=ranges[name]
        need(lo<=a<=b<=hi,'rational enclosure '+name)
    within('w',Q(1,3),Q(2,5))
    within('height2',Q(49,100),Q(3,5))
    within('kappa',Q(-3,10),Q(-1,5))
    within('gamma',Q(-1,2),Q(0))
    within('q2',Q(0),Q(1))
    within('Fprime',Q(10),Q(14))
    for tag in ('minus','plus'):
        within(tag+'_gramdet',Q(1,4),Q(1))
        need(max(sum(max(abs(x) for x in ranges[f'{tag}_xi_{i}_{j}']) for j in range(3))
                 for i in range(3))<=5,'inverse row l1 '+tag)
    need(ranges['minus_det'][0]>=Q(1,10), 'excluded orientation positive gap')
    need(ranges['plus_det_over_F'][1]<=Q(-2,5), 'remaining determinant factor magnitude')
    need(max(sum(max(abs(x) for x in ranges[f'ri_{j}_{i}']) for j in range(3))
             for i in range(3))<=3, 'reflection inverse column l1')
    need(max(sum(max(abs(x) for x in ranges[f'A_{label}_{i}']) for i in range(3))
             for label in m.A)<=3, 'A coefficient l1')
    need(max(sum(max(abs(x) for x in ranges[f's_{label}_{i}']) for i in range(3))
             for label in range(15))<=3, 'comparison coefficient l1')
    need(max(sum(max(abs(x) for x in m.bound(m.derivative(funcs[f's_{label}_{i}'])))
                 for i in range(3)) for label in range(15))<=18,
         'comparison derivative l1')
    return {'scalar_enclosures':8,'inverse_branches':2,
            'model_vectors':15,'closed_subintervals':PIECES,
            'rational_functions':len(funcs),'bound_manifest_sha256':digest(m.manifest())}


def verify(root,config=None,manifest=None):
    c=json.loads((HERE/'certificate.json').read_text()) if config is None else config
    validate_config(c)
    base,core=load_prerequisites(root,c)
    old=core.verify(json.loads((root/'tammes15_contact_pattern_obstruction/certificate_contact_core.json').read_text()))
    need(old['status']=='VERIFIED' and old['prescribed_edges']==24,'full pinned core replay')
    spec=importlib.util.spec_from_file_location('pinned_incumbent_local',root/'tammes15_exact_local_certificate/verify.py')
    local=importlib.util.module_from_spec(spec);spec.loader.exec_module(local)
    receipt=local.verify(json.loads((root/'tammes15_exact_local_certificate/certificate.json').read_text()),False)
    need(receipt['spherical_rigidity_rank']==42 and receipt['gauged_inverse_norm_upper']=='34',
         'full pinned local exclusion replay')
    m=Models(base,core)
    saved=json.loads((HERE/'model-functions.json').read_text()) if manifest is None else manifest
    need(m.manifest()==saved,'independently derived model-functions table')
    exact_identities(m)
    errors={}
    for roots,steps in (((0,5,11),m.ap),((1,2,4),m.bp)):
        for label,error in zip(roots,(0,2,17)): errors[label]=error
        for n,i,j,o in steps: errors[n]=20+errors[i]+errors[j]+errors[o]
    need(max(errors.values())==78 and max(errors.values())<80,'all block perturbation errors')
    result={'status':'VERIFIED','agent':'six-tammes-2','role':'researcher',
            'prescribed_edges':28,'epsilon':'1/10000000000000',
            'interval':['14/25','593/1000'],
            'block_errors':{str(k):errors[k] for k in sorted(errors)},
            'bridges':scalar_bridges(), 'rational_certificate':verify_bounds(m),
            'pinned_core_replayed':True,'pinned_local_stress_replayed':True,
            'strict_improvement_with_near_pattern_excluded':True,
            'incumbent_at_equality_classified':True,'global_bound_improved':False}
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prerequisite-root',type=Path,default=ROOT)
    args=parser.parse_args()
    print(json.dumps(verify(args.prerequisite_root.resolve()),sort_keys=True,indent=2))


if __name__=='__main__': main()
