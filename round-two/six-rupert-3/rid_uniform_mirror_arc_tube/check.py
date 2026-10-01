#!/usr/bin/env python3
"""Exact polynomial hypotheses for a uniform receiving tube about RID mirror arcs.

PROOF.md proves the continuum reduction. Bernstein coefficients certify
whole parameter intervals; no sampled search is a proof input.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from importlib.util import module_from_spec,spec_from_file_location
from math import comb
import argparse
import copy
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
S_MIN=Q(1,300)
S_MAX=Q(1,12)
DELTA=Q(1,2000000)


def require(condition,message):
    if not condition:raise ValueError(message)


def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==Z:p.pop()
    return tuple(p)

def pcoerce(p):
    return p if isinstance(p, tuple) else (F.coerce(p),)

def add(p,q):
    p,q=pcoerce(p),pcoerce(q)
    return trim([(p[i] if i<len(p) else Z)+(q[i] if i<len(q) else Z) for i in range(max(len(p),len(q)))])

def neg(p):return tuple(-x for x in pcoerce(p))
def sub(p,q):return add(p,neg(q))
def mul(p,q):
    p,q=pcoerce(p),pcoerce(q);out=[Z]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return trim(out)

def scale(a,p):return mul(a,p)
def dot(v,w):return sum_poly(mul(a,b) for a,b in zip(v,w))
def sum_poly(seq):
    result=(Z,)
    for p in seq:result=add(result,p)
    return result

def cross(v,w):
    return (sub(mul(v[1],w[2]),mul(v[2],w[1])),sub(mul(v[2],w[0]),mul(v[0],w[2])),sub(mul(v[0],w[1]),mul(v[1],w[0])))

def vsub(v,w):return tuple(sub(a,b) for a,b in zip(v,w))
def ev(p,s):
    result=Z
    for a in reversed(p):result=result*s+a
    return result

def encode(p):return [x.encode() for x in p]

def bernstein(p,lo,hi):
    # p(lo+(hi-lo)t) power coefficients, then fixed degree Bernstein.
    n=len(p)-1;d=F(hi-lo);a=[Z]*(n+1)
    for j,c in enumerate(p):
        for k in range(j+1):a[k]+=c*comb(j,k)*F(lo)**(j-k)*d**k
    return tuple(sum((a[k]*Q(comb(i,k),comb(n,k)) for k in range(i+1)),Z) for i in range(n+1))


def positive_certificate(p,lo=Q(0),hi=S_MAX):
    coefficients=bernstein(p,lo,hi)
    require(min(coefficients)>Z,'whole-interval Bernstein positivity fails')
    return {'domain':[str(lo),str(hi)],'degree':len(p)-1,
            'power_coefficients':encode(p),'bernstein_coefficients':encode(coefficients)}


def replay():
    pins=json.loads((HERE/'DEPENDENCIES.json').read_text())
    require(set(pins)=={'endpoint','twofold_caps'},'prerequisite inventory differs')
    paths={}
    for label,pin in pins.items():
        directory=(HERE/pin['directory']).resolve();paths[label]=directory
        needed={'check.py','PROOF.md','expected.json','DEPENDENCIES.json'}|({'PROBES.json'} if label=='endpoint' else set())
        require(set(pin['sha256'])==needed,'prerequisite file list differs')
        for name,sha in pin['sha256'].items():
            require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==sha,'published prerequisite changed:'+label+'/'+name)
    # A separate sequential child respects each old verifier's arithmetic
    # isolation. The parent waits; there are never two active CPU jobs.
    flags=['-O'] if sys.flags.optimize else []
    run=subprocess.run([sys.executable,*flags,'-B',str(paths['twofold_caps']/'check.py')],
                       stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
    require(run.returncode==0,'whole twofold check failed:'+run.stderr.decode()[:500])
    require(run.stdout==(paths['twofold_caps']/'expected.json').read_bytes(),'whole twofold expected output differs')
    require('field' not in sys.modules,'unverified arithmetic preloaded')
    spec=spec_from_file_location('uniform_tube_endpoint_dependency',paths['endpoint']/'check.py')
    e=module_from_spec(spec);spec.loader.exec_module(e)
    result=e.verify();output=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    require(output==(paths['endpoint']/'expected.json').read_bytes(),'whole endpoint expected output differs')
    # Independently locate the original field and geometry using the pinned
    # twofold manifest, and require the already verified endpoint field to
    # be exactly this source before using it for the new polynomial gates.
    bp=json.loads((paths['twofold_caps']/'DEPENDENCIES.json').read_text())
    base=(paths['twofold_caps']/bp['directory']).resolve()
    for name,sha in bp['sha256'].items():
        require(hashlib.sha256((base/name).read_bytes()).hexdigest()==sha,'original geometry prerequisite differs:'+name)
    require(Path(sys.modules['field'].__file__).resolve()==base/'field.py','original arithmetic location differs')
    spec=spec_from_file_location('uniform_tube_original_geometry',base/'verify.py')
    b=module_from_spec(spec);spec.loader.exec_module(b)
    return b,{'endpoint_whole_expected_bytes':len(output),'endpoint_whole_expected_sha256':hashlib.sha256(output).hexdigest(),
              'twofold_whole_expected_bytes':len(run.stdout),'twofold_whole_expected_sha256':hashlib.sha256(run.stdout).hexdigest(),
              'inherited_old_local_expected_sha256':result['inherited_local_expected_sha256']}


def read_poly(encoded):
    require(isinstance(encoded,list) and 1<=len(encoded)<=2 and all(isinstance(x,list) and len(x)==2 for x in encoded),'malformed affine polynomial')
    return trim([F(*x) for x in encoded])


def family(record,radius_multiple=Q(1)):
    require(record['axis'] in ['x','y'] and len(record['probes'])==4 and len(record['positive_stress_weight_polynomials'])==4,'both four-probe families required')
    j=0 if record['axis']=='x' else 1;s=(Z,O);V=b.vertices();T=[];records=[]
    weights=[read_poly(p) for p in record['positive_stress_weight_polynomials']]
    for item in record['probes']:
        require(len(item['vertex'])==3 and all(len(x)==2 for x in item['vertex']),'malformed actual original')
        v=tuple(F(*x) for x in item['vertex'])
        require(len(item['probe_polynomial'])==3,'malformed physical spatial probe')
        m=tuple(read_poly(p) for p in item['probe_polynomial'])
        require(v in V and len(m[0])==len(m[1])==1,'probe must use an actual original and fixed x/y components')
        require(add(mul(s,m[j]),m[2])==(Z,),'probe not in the actual parameter plane')
        norm=dot(m,m)
        require(max(ev(norm,Q(0)),ev(norm,S_MAX))<F(16),'physical probe norm4 fails')
        gaps=[]
        for w in V:
            if w==v:continue
            gap=dot(m,tuple((x,) for x in b.sub(v,w)));g=sub(gap,s)
            require(len(g)<=2 and ev(g,Q(0))>=Z and ev(g,S_MAX)>Z,'unique original gap>s fails on the full interval')
            gaps.append(g)
        require(len(gaps)==59,'actual-original support comparison omitted')
        t=cross(tuple((x,) for x in v),m);T.append(t)
        records.append({'vertex':b.encode(v),'probe_polynomial':[encode(p) for p in m],
                        'torque_polynomial':[encode(p) for p in t],
                        'squared_probe_norm_endpoint_max':max(ev(norm,Q(0)),ev(norm,S_MAX)).encode(),
                        'minimum_gap_minus_s_at_zero':min(ev(g,Q(0)) for g in gaps).encode(),
                        'minimum_gap_minus_s_at_upper_endpoint':min(ev(g,S_MAX) for g in gaps).encode(),
                        'all_original_support_comparisons':59})
    require(all(ev(w,Q(0))>=Z and ev(w,S_MAX)>Z for w in weights),'stress not positive for all positive tilts')
    require(all(sum_poly(mul(w,t[k]) for w,t in zip(weights,T))==(Z,) for k in range(3)),'polynomial torque balance fails')
    determinant=dot(vsub(T[1],T[0]),cross(vsub(T[2],T[0]),vsub(T[3],T[0])))
    if ev(determinant,S_MAX)<Z:determinant=neg(determinant)
    determinant_record=positive_certificate(determinant)
    facets=[]
    for ids in combinations(range(4),3):
        a,c,d=[T[i] for i in ids];N=cross(vsub(c,a),vsub(d,a));h=dot(N,a)
        p=sub(mul(h,h),scale(radius_multiple**2,mul(mul(s,s),dot(N,N))))
        factor=0
        while len(p)>1 and p[0]==Z:p=p[1:];factor+=1
        facets.append({'indices':list(ids),'removed_positive_s_power':factor,
                       'distance_minus_radius_squared_certificate':positive_certificate(p)})
    return {'axis':record['axis'],'positive_parameter_domain':'0<s<=1/12',
            'probe_norm_upper':'4','unique_support_gap_lower':'s','torque_ball_radius_lower':'s',
            'probes':records,'positive_stress_weight_polynomials':[encode(w) for w in weights],
            'oriented_affine_torque_determinant_certificate':determinant_record,'four_facet_certificates':facets}


def geometry_gates(C,delta=DELTA,s_min=S_MIN,local_receiver=Q(1,24000),local_angle=Q(1,12000)):
    require(len(C)==31 and len(set(C))==31,'complete physical Cauchy inventory required')
    require(s_min==Q(1,300) and 0<delta<=Q(1,1000000),'unsupported positive tilt/receiving domain')
    A0=12+28*phi;B=3*phi**2;S=phi+2;D=[c for c in C if c[2]==Z]
    require(len(D)==6 and A0<F(58) and 7+8*phi<F(20),'physical body constants differ')
    require(all(c[2]**2/b.dot(c,c)>F(Q(1,16)) for c in C if c[2]!=Z),'physical nonzero-z sign threshold lost')
    require(940+1520*phi>F(Q(583,10)**2),'all-source polar level bound lost')
    require(250*delta<Q(1,50) and 180*delta+100*delta**2<Q(1,50),'full-source area/width margins lost')
    endpoint_values=[((F(28048)+44032*phi)/29,(F(2371108)+3159652*phi)/104401),
                     (F(Q(138704,145))+Q(43792,29)*phi,(F(2292772)+3127108*phi)/104401)]
    width_limit=(20+32*phi)*(1-Q(10,11664));records=[]
    for j in [0,1]:
        k=1-j;H=sum((abs(c[j]) for c in D),Z)
        require(H==(4+8*phi if j==0 else 8+4*phi) and F(14)<H<F(17),'mirror physical area coefficient differs')
        kj,ell=(phi**2,phi**2) if j==0 else (phi,O)
        require(H-A0*S_MAX>Z and kj*S-ell*B*S_MAX>Z,'area/physical directional width not increasing over the whole reference interval')
        area2,width2=endpoint_values[j]
        require(area2<F((Q(1171,20)-Q(1,50))**2) and width_limit-width2>F(Q(1,50)) and width2<F(81),'whole-arc strengthened filter margins fail')
        signed=tuple(sum((c[i]*c[j].sign() for c in D if c[j]!=Z),Z) for i in range(3))
        require(signed==tuple(H if i==j else Z for i in range(3)) and sum((abs(c[k]) for c in D if c[j]==Z),Z)==F(4),'actual target equatorial sign sum differs')
        require(all(abs(c[j])*F(Q(1,301)-delta)>abs(c[k])*F(delta) for c in D if c[j]!=Z),'positive-tilt actual target signs fail')
        require(all(tuple(-x if i==k else x for i,x in enumerate(c)) in D or b.neg(tuple(-x if i==k else x for i,x in enumerate(c))) in D for c in D),'physical equatorial area not reflection-even')
        gamma,other=(phi**2,2+phi) if j==0 else (2+phi,phi**2)
        require(gamma**2>F(6) and other**2<F(20),'summed radial coefficients differ')
        records.append({'axis':'x' if j==0 else 'y','physical_H':H.encode(),
                        'area_derivative_numerator_at_upper_endpoint':(H-A0*S_MAX).encode(),
                        'width_derivative_sign_at_upper_endpoint':(kj*S-ell*B*S_MAX).encode(),
                        'squared_width_filter_margin':(width_limit-width2).encode()})
    require(s_min**2/(1+s_min**2)>Q(1,301)**2 and Q(1,301)-delta>Q(1,302),'positive normalized tilt lower bound lost')
    require(Q(1473,5632)+Q(25,22)*delta<Q(4,15),'arbitrary full-roll starting bound lost')
    require(Q(45,116)>Q(3,5)**2 and (Q(3,5)-5*delta)**2>Q(1,3)>Q(36,125),'actual-original radial support separation lost')
    require(Q(144,145)>Q(99,100)**2 and Q(99,100)-delta>Q(24,25),'receiving singular value lower bound lost')
    require(Q(3,25)+16*delta<Q(123,1000) and Q(1,8)+16*delta<Q(1,4),'corrected source leaves physical sign domain')
    require(Q(4,15)+16*delta<Q(1,3) and S_MAX+delta<Q(123,1000),'source row or actual target leaves the locked mirror domain')
    require(1-Q(123,1000)**2>Q(24,25)**2 and 14-58*Q(123,1000)/Q(24,25)>6,'mirror derivative lower six lost')
    require(Q(10,9)*14<16 and Q(16*14)/Q(19,10)<120,'proper row/quadratic retained correction lost')
    require(Q(20,6)*16**2+240<1100 and 1100*302==332200 and 1+332200*delta<2,'uniform radial lower tilt error2delta fails')
    require((58+17)*120==9000 and (21+9000*delta)/6<4,'uniform upper tilt error4delta fails')
    require(2*4+16+1==25 and 150*delta<=local_angle and delta<=local_receiver,'all-source pose misses the uniform contact box')
    require(0<local_receiver<=s_min/80 and 0<local_angle<=s_min/40,'uniform contact parameters exceed the proved parameter-scaled box')
    require(40*local_receiver<s_min and 20*(local_receiver+local_angle/2)<s_min,'closed contact support/torque budgets fail')
    require(s_min+delta<Q(1,270),'nearzero portion misses the published strict twofold cap')
    return {'all_source_positive_arc_closed_radius':str(delta),'whole_mirror_union_strict_exclusion_radius':str(delta),
            'positive_reference_parameter_interval':[str(s_min),str(S_MAX)],
            'uniform_contact_receiver_chord_radius':str(local_receiver),'uniform_contact_full_angle_radians':str(local_angle),
            'parameter_scaled_contact_receiver_radius':'s/80','parameter_scaled_contact_full_angle_radians':'s/40',
            'retained_normal_coordinate_correction':'120delta^2','summed_radial_squared_error':'1100delta^2',
            'lower_tilt_error':'2delta','upper_tilt_error':'4delta','full_two_row_operator_pose_error':'25delta',
            'actual_shadow_preserving_proper_relative_angle_upper':'150delta','whole_arc_physical_gates':records,
            'nearzero_receiving_conclusion':'strict exclusion only; no closed-fit classification transferred from the twofold cap'}


def negative_controls(C,records):
    reverse=copy.deepcopy(records[0]);reverse['probes'][0]['probe_polynomial']=[[[str(-Q(a)),str(-Q(b))] for a,b in p] for p in reverse['probes'][0]['probe_polynomial']]
    stress=copy.deepcopy(records[0]);stress['positive_stress_weight_polynomials'][0][0]=['1','0']
    plane=copy.deepcopy(records[0]);plane['probes'][0]['probe_polynomial'][2][1]=['0','0']
    short=copy.deepcopy(records[0]);short['probes']=short['probes'][:-1]
    cases=[lambda:family(reverse),lambda:family(stress),lambda:family(plane),lambda:family(short),
           lambda:family(records[0],radius_multiple=Q(4)),lambda:geometry_gates(C,delta=Q(1,1000)),
           lambda:geometry_gates(C,local_angle=Q(1,100)),lambda:geometry_gates(C,s_min=Q(0)),lambda:geometry_gates(C[:-1])]
    for case in cases:
        try:case()
        except ValueError:continue
        raise ValueError('damaged parameter or continuum premise accepted')
    return len(cases)


def verify():
    global b,F,Z,O,phi
    b,prior=replay();F,Z,O,phi=b.F,b.ZERO,b.ONE,b.PHI
    V=b.vertices();planes,_=b.complete_facets(V);C,_,_=b.area_generators(V,planes)
    records=json.loads((HERE/'PARAMETERS.json').read_text())
    require([r['axis'] for r in records]==['x','y'],'both mirror families required')
    families=[family(r) for r in records];gates=geometry_gates(C)
    return {'agent':'six-rupert-3','role':'researcher','arithmetic':'ordered exact Q(phi), Fraction, exact polynomial and Bernstein coefficients',
            'proof_status':'written uniform positive-arc closed-rigidity and complete mirror-union strict tube with exact polynomial hypotheses',
            'global_RID_Rupert_status':'unresolved','actual_original_vertices':len(V),
            'new_actual_original_support_comparisons':472,'new_parameter_torque_families':families,
            'damaged_controls_rejected':negative_controls(C,records),**prior,**gates}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');args=parser.parse_args()
    output=json.dumps(verify(),indent=2,sort_keys=True)+'\n'
    if not args.emit:require(output==(HERE/'expected.json').read_text(),'whole uniform-tube expected output differs')
    print(output,end='')


if __name__=='__main__':main()
