"""Scope, coverage, factor, endpoint and radical-sign controls."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
import copy,json,signal
from schema import validate,require
from generate import generate
from check import replay
from algebra import derive
from signs import strict
from polynomials import P,dot
from frame import make,CORE,CONTACTS
from audit import identity_audit,taylor
HERE=Path(__file__).resolve().parent

def rejected(function,message,expected_error=None):
    try:function()
    except (ValueError,TypeError,KeyError) as error:
        if expected_error is not None:require(str(error)==expected_error,'wrong rejection mechanism')
        return message
    raise ValueError('damaged certificate accepted: '+message)

def guard(A,B,R,positive_root=True):
    if positive_root is not True or R<=0:return False
    H=A*A-B*B*R
    return (A>0 and H>0) or (B>0 and H<0) or (A>0 and B>0)

def controls(system,factors,certificate):
    rejected_packets=[]
    mutations=[
        ('dropped cover box',lambda s:s['closed_cover'].pop()),
        ('wrong lower-corner packing pair',lambda s:s['closed_cover'][0].update(contradicting_pair=[0,1])),
        ('missing closed seam',lambda s:s['closed_cover'][1]['box'].__setitem__(0,'283/500')),
        ('discarded lower outer band',lambda s:s.update(excluded_z_interval=['71/50','5/2'])),
        ('discarded lower t endpoint',lambda s:s.update(t_interval=['561/1000','593/1000'])),
        ('missing required contact',lambda s:s['required_contacts'].pop()),
        ('extra 5-12 premise',lambda s:s['required_contacts'].append([5,12])),
        ('synthetic point13 premise',lambda s:s['core_labels'].append(13)),
        ('arbitrary additions removed',lambda s:s.update(other_points_arbitrary=False)),
        ('extra contacts forbidden',lambda s:s.update(additional_contacts_allowed=False)),
        ('negative radical branch',lambda s:s.update(root_sign='w<0')),
        ('unproved formal sheet',lambda s:s.update(imported_complete_branch=[1,1])),
        ('weak regularity substituted',lambda s:s.update(necessary_core_regularity='2*G>=(1+t)^4*C^2')),
        ('hidden face or cohort condition',lambda s:s.update(cohort='A5/B6')),
        ('unconditional conclusion',lambda s:s.update(conclusion_is_global_Tammes_bound=True))]
    for name,change in mutations:
        damaged=copy.deepcopy(system);change(damaged);rejected_packets.append(rejected(lambda:validate(damaged),name))
    for name,change in [
        ('missing sign obligation',lambda c:c['strict_sign_obligations'].pop()),
        ('wrong whole coefficient hash',lambda c:c['strict_sign_obligations'][0].update(whole_coefficient_array_sha256='0'*64)),
        ('deleted chart-equality branch',lambda c:c.update(chart_equality_branch='omitted'))]:
        damaged=copy.deepcopy(certificate);change(damaged);rejected_packets.append(rejected(lambda:replay(system,factors,damaged),name))
    for name,change in [
        ('corrupted L5 coefficient',lambda f:f['rows']['L5'][0].__setitem__(3,str(int(f['rows']['L5'][0][3])+2))),
        ('reversed M6 sign',lambda f:[r.__setitem__(3,str(-int(r[3]))) for r in f['rows']['M6']]),
        ('reversed H10 sign',lambda f:[r.__setitem__(3,str(-int(r[3]))) for r in f['rows']['H10']]),
        ('duplicate polynomial row',lambda f:f['rows']['H12'].append(f['rows']['H12'][0]))]:
        damaged=copy.deepcopy(factors);change(damaged);rejected_packets.append(rejected(lambda:derive(damaged),name))
    damaged=copy.deepcopy(factors);damaged['rows']['L5'][0][3]=str(int(damaged['rows']['L5'][0][3])+2)
    interpolation_rejection=rejected(lambda:identity_audit(damaged),'alternate interpolation detects corrupted L5','nonzero full-grid exact residual')
    ta,tb=map(Q,system['t_interval']);za,zb=map(Q,system['excluded_z_interval']);box=(ta,tb,za,zb)
    endpoint_rejections=[rejected(lambda:strict(25*P.var(0)-14,box,1),'Bernstein rejects closed endpoint zero'),rejected(lambda:taylor([(1,0,25),(0,0,-14)],box,1),'Taylor rejects closed endpoint zero')]
    require(guard(Q(3),Q(-2),Q(1)) and guard(Q(-2),Q(3),Q(1)) and guard(Q(1),Q(1),Q(1)),'three valid radical guards')
    require(not guard(Q(-3),Q(2),Q(1)),'unsigned positive-square counterexample')
    require(not guard(Q(-2),Q(-3),Q(1)),'unsigned negative-square counterexample')
    require(not guard(Q(-2),Q(3),Q(1),False),'reversed-root counterexample')
    # A credited prior rational G21 family member. All twelve points and
    # all66 products are decoded exactly; it lies outside the new target.
    t=Q(29,50);z=(1+2*t)/(t*(3*t+1));m0=make(t,z,Q(0));R=m0['root_squared']
    n,d=isqrt(R.numerator),isqrt(R.denominator);require(n*n==R.numerator and d*d==R.denominator and n>0,'positive rational radical control')
    w=Q(n,d);m=make(t,z,w);points={i:[x/m['Omega'] for x in m['points'][i]] for i in CORE}
    require(z<Q(7,5) and (1-t)**2*z*z<=1 and 2*m['G']>(1+t)**4*m['C']**2,'feasible control domain and retained lower band')
    for i in CORE:require(dot(points[i],points[i],t)==1,'exact control unit')
    for i,j in combinations(CORE,2):require(dot(points[i],points[j],t)<=t,'exact control packing pair')
    for i,j in CONTACTS:require(dot(points[i],points[j],t)==t,'exact control required contact')
    require(dot(points[5],points[12],t)==t,'prior rational boundary curve control')
    zboundary=1/(1-t);Mboundary=1+2*t-t*t-2*t*(1-t)*(1+2*t)*zboundary
    require(Mboundary==1-5*t*t<0,'exceptional closed chart equality is handled separately')
    return {'actual_agent':'six-tammes-2','role':'researcher','status':'ALL_SCOPE_COVER_FACTOR_AND_SIGN_CONTROLS_PASSED','damaged_packet_rejections':rejected_packets,'damaged_packet_rejection_count':len(rejected_packets),'alternate_interpolation_rejection':interpolation_rejection,'closed_endpoint_zero_rejections':endpoint_rejections,'valid_radical_sign_controls':3,'unsigned_or_reversed_root_counterexamples_rejected':3,'exact_prior_core_control':{'credited_source':'LEMMA10012 and prior REVIEW9984 rational family, not a new construction','t':str(t),'z':str(z),'positive_w':str(w),'unit_checks':12,'all_packing_pair_checks':66,'required_contact_checks':20,'additional_5_12_contact_checked':True,'outside_excluded_target':True},'exceptional_chart_equality_checked':True,'independent_new_result_review':'pending','new_global_bound':False}

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('20s scope and arithmetic controls guard')));signal.alarm(20)
    s=json.loads((HERE/'SYSTEM.json').read_text());f=json.loads((HERE/'FACTORS.json').read_text());c=json.loads((HERE/'CERTIFICATE.json').read_text());print(json.dumps(controls(s,f,c),indent=2))
