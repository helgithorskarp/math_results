#!/usr/bin/env python3
"""Finite exact algebra for global low-sublevel polar routing, Python3.10+.

Default reads, reconstructs and fully compares EXPECTED.json. No assertion,
floating-point evidence, solver, source import, phase grid or root enumeration.
--emit is an explicit fixture-generation action. Written analytic bridges and
the scoped8656/7244/9620 dependencies remain outside this checker.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import comb
from pathlib import Path
from copy import deepcopy
import argparse
import json

class CheckError(Exception):
    pass

def require(ok, message):
    if not ok:
        raise CheckError(message)

def tidy(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p

def add(*ps):
    r = [Q(0)] * max(map(len, ps))
    for p in ps:
        for k, c in enumerate(p):
            r[k] += c
    return tidy(r)

def scale(p, s):
    return tidy([c*s for c in p])

def mul(p, q):
    r = [Q(0)] * (len(p)+len(q)-1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i+j] += x*y
    return tidy(r)

def power(p, n):
    r = [Q(1)]
    for _ in range(n):
        r = mul(r, p)
    return r

def value(p, x):
    r = Q(0)
    for c in reversed(p):
        r = r*x+c
    return r

def smul(p, q):
    r = {}
    for (i,t), c in p.items():
        for (j,u), d in q.items():
            key = i+j,t+u
            r[key] = r.get(key,Q(0))+c*d
    return {k:v for k,v in r.items() if v}

def s_integral(p):
    r = [Q(0)]*(max(i for i,t in p)+1)
    for (i,t),c in p.items():
        r[i] += c/(t+1)
    return tidy(r)

def gadd(x, y):
    return x[0]+y[0], x[1]+y[1]

def gmul(x, y):
    return x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0]

def gscale(x,s):
    return x[0]*s,x[1]*s

def gnorm2(x):
    return x[0]*x[0]+x[1]*x[1]

def gp_product(qs, c, d):
    """Complete Gaussian-rational polynomial product of c+d*t*q_j."""
    p = [(Q(1),Q(0))]
    for q in qs:
        out = [(Q(0),Q(0))]*(len(p)+1)
        for k,x in enumerate(p):
            out[k] = gadd(out[k],gscale(x,c))
            out[k+1] = gadd(out[k+1],gscale(gmul(x,q),d))
        p = out
    return p

def gp_integral(p):
    r = Q(0),Q(0)
    for k,c in enumerate(p):
        r = gadd(r,gscale(c,Q(1,k+1)))
    return r

def e_gauss(qs):
    out = [(Q(1),Q(0))]+[(Q(0),Q(0))]*len(qs)
    for used,q in enumerate(qs):
        for k in range(used+1,0,-1):
            out[k] = gadd(out[k],gmul(q,out[k-1]))
    return out

def e_real(rs):
    out = [Q(1)]+[Q(0)]*len(rs)
    for used,r in enumerate(rs):
        for k in range(used+1,0,-1):
            out[k] += r*out[k-1]
    return out

def exact_record():
    eta = [Q(0),Q(1)]
    a = [Q(1),Q(-1)]
    b = add([Q(1)],scale(power(a,2),-1))
    L = [Q(8),Q(3)]
    d = scale(mul(power(a,7),b),Q(1,2))
    T = [Q(0)]
    for k in range(2,9):
        term = mul(mul(power(a,8-k),power(b,k)),power(scale(L,Q(1,8)),k))
        T = add(T,scale(term,Q(comb(8,k),k+1)))
    B = add(power(a,8),mul(d,L),T)
    D = mul(power(a,15),b)
    N_mean = add([Q(1)],scale(power(a,16),-1),
                 scale(mul(power(d,2),power(L,2)),-1),
                 scale(mul(add(power(a,8),mul(d,L)),T),-2),
                 scale(power(T,2),-1),scale(mul([Q(8),Q(-6)],D),-1))
    N_mod = add([Q(1),Q(0),Q(9)],scale(B,-1))
    N_var = add(scale(mul(power(a,6),power(b,2)),13),scale(add(B,[Q(-1)]),-6))

    # Separate construction: multiply all eight eta,t factors first, then
    # integrate the entire product. No elementary-symmetric coefficient list.
    mu = scale(L,Q(1,8))
    factor = {(i,0):c for i,c in enumerate(a) if c}
    for i,c in enumerate(mul(b,mu)):
        if c: factor[(i,1)] = c
    raw = {(0,0):Q(1)}
    for _ in range(8):
        raw = smul(raw,factor)
    B_direct = s_integral(raw)
    require(B_direct == B,'full balanced-product polynomial')
    T_direct = add(B_direct,scale(power(a,8),-1),scale(mul(d,L),-1))
    require(T_direct == T,'full integrated higher tail')

    e = Q(1,2**16)
    margins = {}
    certs = {}
    for name, p, head, threshold in [('mean',N_mean,Q(4,3),Q(1)),
                                      ('modulus',N_mod,Q(2,3),Q(1,2)),
                                      ('variance',N_var,Q(2),Q(1))]:
        require(p[:2] == [0,0] and p[2] == head,'entire cancellation '+name)
        loss = sum(abs(c)*e**(k-2) for k,c in enumerate(p) if k>=3)
        lower = head-loss
        require(lower > threshold,'full interval positive '+name)
        certs[name] = {'polynomial':p,'head':head,'absolute_tail_at_endpoint':loss,
                       'uniform_lower_bound_after_eta_squared':lower,'threshold':threshold}
        margins['scalar_'+name] = lower-threshold

    K1 = 9*sum(Q(comb(7,k),k+2)*Q(8,7)**k for k in range(8))
    K2 = 9*sum(Q(comb(6,k),k+3)*Q(4,3)**k for k in range(7))
    K9 = 9*sum(Q(comb(7,k),k+2)*Q(9,7)**k for k in range(8))
    P9 = Q(9,7)**7
    require(K1 == Q(570801247,1647086) and K2 == Q(1199851,5103),'credited full derivatives')
    amin = 1-e
    margins.update({
        'derivative350':350-K1,
        'hessian_ordered_pairs':2*K1-K2,
        'origin_lipschitz600':600-K9,
        'product_lipschitz6':6-P9,
        'radial_normalization_phase10':10-9*(1+Q(3,2)*e),
        'normalized_second_symmetric_7over4':28*amin**2-26-Q(7,4),
        'variance_transfer65over64':Q(65,64)-Q(256,255)**2,
        'mean_modulus_positive':8-6*e,
        'individual_left_of_mark':1-165*e,
        'weighted_original_radial10':2-10*e-81*e**2,
        'origin_radial_gap60000':60000-(350*160+600*6+6*6),
        'energy_carrier2pow28':2**28-(199680144+52*e),
        'routed_positive_eta_collar':Q(1,512)-2**28*Q(1,2**37),
        'linear13over5':Q(8,3)-Q(13,5)-Q(4,3)*e,
    })
    # The routed energy endpoint is equal, legitimately; strict H<2^28*eta
    # supplies strict entry. No manufactured positive margin for equality.
    require(margins.pop('routed_positive_eta_collar') == 0,'exact routed endpoint equality')
    for name,m in margins.items():
        require(m>0,'strict rational window margin '+name)
    normalized_variance = Q(8*256*60000,5)
    transferred_variance = normalized_variance*Q(65,64)
    require(normalized_variance == 24576000 and transferred_variance == 24960000,'full variance budget')

    controls = []
    phases = [(Q(1),Q(0)),(Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13)),
              (Q(0),Q(-1)),(Q(-1),Q(0))]
    for sample in range(10):
        aa = Q(3+sample,16)
        bb = 1-aa*aa
        radii = [Q(5+(j+sample)%4,10) for j in range(8)]
        qs = [gscale(phases[(j+sample)%len(phases)],radii[j]) for j in range(8)]
        for r,q in zip(radii,qs):
            require(gnorm2(q) == r*r,'Gaussian rational radius')
            diff = q[0]-r,q[1]
            require(gnorm2(diff) == 2*r*(r-q[0]),'complete phase identity')
        es = e_gauss(qs)
        polar = gp_integral(gp_product(qs,aa,bb))
        polar_es = Q(0),Q(0)
        origin_es = Q(0),Q(0)
        for k,z in enumerate(es):
            polar_es = gadd(polar_es,gscale(z,Q(aa**(8-k)*bb**k,k+1)))
            origin_es = gadd(origin_es,gscale(z,Q(9*(-aa)**k,k+1)))
        origin = gscale(gp_integral(gp_product(qs,1,-aa)),9)
        require(polar == polar_es and origin == origin_es,'whole Gaussian polar/origin product')
        ff = sum(radii);v = sum((r-ff/8)**2 for r in radii)
        require(e_real(radii)[2] == Q(7,16)*ff*ff-v/2,'whole radial variance identity')
        delta = sum(r-q[0] for r,q in zip(radii,qs))
        require(sum(gnorm2((q[0]-1,q[1])) for q in qs)
                == v+8*(ff/8-1)**2+2*delta,'whole reciprocal-to-energy identity')
        controls.append({'a':aa,'radii':radii,'reciprocals':qs,'polar':polar,'origin':origin,
                         'variance':v,'angular_defect':delta})

    # Actual disk-rooted controls with all multiplicities retained. This
    # family is OUTSIDE the low-sum cut; it checks identities, not existence
    # of a near minimizer. Other originals are all -1.
    actual = []
    for ee in [Q(1,2**16),Q(1,2**37),Q(1,128)]:
        aa = 1-ee
        rs = [1/(aa+1)]*7+[9/(aa+1)]
        qs = [(r,Q(0)) for r in rs]
        polar = gp_integral(gp_product(qs,aa,1-aa*aa))
        origin = gscale(gp_integral(gp_product(qs,1,-aa)),9)
        require(polar == (Q(1),Q(0)),'actual collapsed polar identity')
        require(origin == (Q(9)/(aa+1)**8,Q(0)),'actual collapsed origin identity')
        require(sum(rs) == Q(16)/(aa+1),'actual collapsed reciprocal sum')
        actual.append({'eta':ee,'F':sum(rs),'polar':polar,'origin':origin,'critical_multiplicities':[7,1]})

    return {'schema':'global-polar-routing-exact-v1','agent':'six-sendov-1','role':'researcher',
            'eta_endpoint':e,'complete_tail':T,'complete_balanced_integral':B,
            'scalar_certificates':certs,'strict_margins':margins,
            'derivatives':{'K1':K1,'K2':K2,'K9':K9,'P9':P9},
            'variance_budgets':{'normalized':normalized_variance,'transferred':transferred_variance},
            'routed_eta_endpoint':Q(1,2**37),'routed_energy_endpoint':Q(1,512),
            'gaussian_controls':controls,'actual_controls':actual}

def encode(x):
    if isinstance(x,Q): return {'numerator':x.numerator,'denominator':x.denominator}
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()

def check_manifest():
    root=Path(__file__).resolve().parent
    manifest=strict_load(root/'MANIFEST.json')
    names={'.gitignore','PROOF.md','README.md','LITERATURE.md','verify.py','validate.py','EXPECTED.json'}
    require(manifest.get('schema')=='global-polar-routing-source-v1'
            and set(manifest.get('files',{}))==names,'source manifest census')
    for name in sorted(names):
        path=root/name
        require(manifest['files'][name]=={'bytes':path.stat().st_size,
                'sha256':sha256(path.read_bytes()).hexdigest()},'source manifest bytes '+name)

def strict_load(path):
    def pairs(items):
        out={}
        for k,v in items:
            require(k not in out,'duplicate JSON key')
            out[k]=v
        return out
    def badconstant(value):
        raise CheckError('nonfinite JSON constant '+value)
    return json.loads(path.read_text(),object_pairs_hook=pairs,parse_constant=badconstant)

def validate(actual, expected):
    # Canonical serialization compares complete types and records, including
    # zero/nonzero entries. Boolean/int substitution and fractional spelling
    # changes are rejected; expected values never generate the mathematics.
    require(canonical(actual) == canonical(expected),'entire typed expected record differs')

def record_damage(record):
    damages=[]
    for label, mutate in [
        ('mean_head',lambda x:x['scalar_certificates']['mean']['head'].__setitem__('numerator',5)),
        ('full_tail_last',lambda x:x['complete_tail'][-1].__setitem__('numerator',730)),
        ('modulus_tail_omitted',lambda x:x['scalar_certificates']['modulus']['polynomial'].pop()),
        ('variance_factor',lambda x:x['variance_budgets'].__setitem__('normalized',24576001)),
        ('hessian_ordering',lambda x:x['derivatives']['K2'].__setitem__('denominator',5104)),
        ('routing_endpoint',lambda x:x['routed_eta_endpoint'].__setitem__('denominator',2**36)),
        ('complex_phase',lambda x:x['gaussian_controls'][1]['reciprocals'][0][1].__setitem__('numerator',17)),
        ('actual_multiplicity',lambda x:x['actual_controls'][0].__setitem__('critical_multiplicities',[6,2])),
    ]:
        bad=deepcopy(record);mutate(bad)
        try: validate(record,bad)
        except CheckError: damages.append(label)
        else: raise CheckError('damage unexpectedly accepted '+label)
    return damages

def mathematical_damage():
    """Reject broken sufficient constants before fixture comparison.

    Certificate failures are not refutations of stronger mathematical claims.
    """
    rejected=[]
    e=Q(1,2**16)
    K1=Q(570801247,1647086)
    K2=Q(1199851,5103)
    for label, condition in [
        ('mean_constant5_leading_margin',Q(2)*(5-Q(16,3))>0),
        ('modulus_constant8_leading_margin',8-Q(25,3)>0),
        ('variance_constant12_leading_margin',4*12-50>0),
        ('tripled_mixed_hessian',3*K2<2*K1),
        ('phase_allowance9',9-9*(1+Q(3,2)*e)>0),
        ('energy_carrier2pow27',2**27-(199680144+52*e)>0),
    ]:
        try: require(condition,'deliberately broken math budget '+label)
        except CheckError: rejected.append(label)
        else: raise CheckError('math damage unexpectedly accepted '+label)
    return rejected

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--emit',action='store_true')
    parser.add_argument('--fixture',type=Path)
    args=parser.parse_args()
    path=args.fixture or Path(__file__).with_name('EXPECTED.json')
    if not args.emit:check_manifest()
    record=encode(exact_record())
    damaged_records=record_damage(record)
    damaged_math=mathematical_damage()
    if args.emit:
        require(args.fixture is None,'emit cannot replace an external fixture')
        path.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    expected=strict_load(path)
    validate(record,expected)
    print(json.dumps({'status':'PASS','whole_record_sha256':sha256(canonical(record)).hexdigest(),
                     'full_polynomial_degrees':{k:len(v['polynomial'])-1 for k,v in record['scalar_certificates'].items()},
                     'strict_window_margins':len(record['strict_margins']),
                     'complete_gaussian_controls':len(record['gaussian_controls']),
                     'actual_multiplicity_controls':len(record['actual_controls']),
                     'rejected_record_damages':damaged_records,
                     'rejected_mathematical_damages':damaged_math},sort_keys=True))

if __name__=='__main__':
    main()
