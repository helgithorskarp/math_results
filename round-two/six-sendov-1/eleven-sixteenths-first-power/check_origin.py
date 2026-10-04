"""Local exact conditional and literal Gaussian controls.

Openly adapted from the same author's 10300 check_origin.py; its fixture
marked intervals are transported here and all payments freshly computed.
No ancestor runtime input or independent-review claim.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import resource
import sys
import time
import importlib.util
HERE=Path(__file__).resolve().parent
_spec=importlib.util.spec_from_file_location('eleven_sixteenths_control_origin',HERE/'origin.py')
m=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

WEAK=list(map(Q,['2/3','27/40','23/10','23/8','77/10','157/20',
                  '553/640','291/320','0','3543/16384','17/40','81/40']))
L=Q(51,80);TM=Q(6776,729)
UPPER=[Q(2,3),Q(27,40),Q(0),Q(23,5),Q(37,5),Q(8),L,Q(1),
       Q(0),1-L**2,Q(0),TM]
LOWER=[Q(2,3),Q(27,40),Q(0),Q(23,5),Q(4),Q(8),Q(1,2),Q(1),
       Q(0),Q(1),Q(0),TM]
PRODUCT=list(map(Q,['2/3','27/40','161/40','69/16','157/20','8',
                    '291/320','1193/1280','0','17719/204800','103/40','141/40']))

# Fresh marked-coordinate fixture transport; energy/mean tests remain fixed.
for _fixture in (WEAK,UPPER,LOWER,PRODUCT):
    _fixture[0],_fixture[1]=Q(27,40),Q(11,16)

DENOMINATOR=WEAK.copy();DENOMINATOR[9]=Q(1,40)

def cmul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def cadd(a,b):return (a[0]+b[0],a[1]+b[1])
def cnorm(a):return a[0]**2+a[1]**2
def cscale(a,x):return (a[0]*x,a[1]*x)

def quartic_control(q):
    mu=(sum(z[0] for z in q)/8,sum(z[1] for z in q)/8)
    z=[cadd(x,cscale(mu,-1)) for x in q]
    m.require(sum(x[0] for x in z)==sum(x[1] for x in z)==0,
              'literal eight complex centered deviations')
    # Literal product coefficients provide e4 without Newton or payment().
    e=[(Q(1),Q(0))]
    for x in z:
        next=[(Q(0),Q(0))]*(len(e)+1)
        for i,y in enumerate(e):
            next[i]=cadd(next[i],y);next[i+1]=cadd(next[i+1],cmul(y,x))
        e=next
    squares=[cmul(x,x) for x in z]
    p2=(sum(x[0] for x in squares),sum(x[1] for x in squares))
    p4s=[cmul(x,x) for x in squares]
    p4=(sum(x[0] for x in p4s),sum(x[1] for x in p4s))
    X=[cadd(x,cscale(p2,-Q(1,8))) for x in squares]
    variance=(sum(cmul(x,x)[0] for x in X),sum(cmul(x,x)[1] for x in X))
    M4=sum(cnorm(x) for x in squares);S=sum(cnorm(x) for x in z)
    m.require(variance==cadd(p4,cscale(cmul(p2,p2),-Q(1,8))),
              'literal whole complex square-centered variance')
    m.require(sum(cnorm(x) for x in X)==M4-cnorm(p2)/8,
              'literal whole squared norm compensation')
    m.require(e[4]==cadd(cscale(cmul(p2,p2),Q(3,32)),cscale(variance,-Q(1,4))),
              'literal e4 versus whole compensated Newton identity')
    m.require(M4<=Q(25,32)*S**2 and cnorm(p2)<=S**2,
              'literal paid centered absolute moment bounds')
    upper=m.hilbert_quartic_payment()*S**2
    m.require(cnorm(e[4])<=upper**2,'literal full complex e4 norm below improved cap')
    return dict(q=q,deviations=z,all9_product_coefficients=e,p2=p2,p4=p4,
                square_variance=variance,S=S,M4=M4,quartic_upper=upper,
                original_feasibility_asserted=False)
def direct_origin(q,a):
    # Literal eight Gaussian factors, no centered polynomial engine.
    pol=[(Q(1),Q(0))]
    for z in q:
        factor=(-a*z[0],-a*z[1]);out=[(Q(0),Q(0))]*(len(pol)+1)
        for i,x in enumerate(pol):
            out[i]=cadd(out[i],x);out[i+1]=cadd(out[i+1],cmul(x,factor))
        pol=out
    m.require(len(pol)==9,'all eight literal tuple factors')
    value=(Q(0),Q(0))
    for j,x in enumerate(pol):value=cadd(value,(9*x[0]/(j+1),9*x[1]/(j+1)))
    return pol,value

def physical(q,a):
    m.require(len(q)==8 and all(cnorm(z)>0 for z in q),'eight nonzero Gaussian tuple members')
    u=sum(z[0] for z in q)/8;v=sum(z[1] for z in q)/8;w=v*v
    Fhi=sum(m.ceiling(cnorm(z)) for z in q)
    # These four controls have |q_j|<=1, so (1-r)^2 decreases in r.
    floors=[]
    for z in q:
        n=m.ceiling(cnorm(z));r=n if n*n==cnorm(z) else n-Q(1,4096)
        m.require(0<=r*r<=cnorm(z)<=1,'paid lower radius and unit upper controls')
        floors.append(r)
    Th=sum((1-r)**2 for r in floors)
    E=sum((z[0]-1)**2+z[1]**2 for z in q)
    box=[a,a,Q(0),E,Q(0),Fhi,u,u,w,w,Q(0),Th]
    polynomial,actual=direct_origin(q,a)
    rows=[]
    for channel in ('energy','joint'):
        paid=m.payment(box,channel)
        m.require(paid['status']=='bounded','direct tuple channel available')
        lower=paid['score']
        if lower>0:m.require(cnorm(actual)>=lower**2,'actual literal origin modulus versus full polynomial lower bound')
        rows.append(dict(channel=channel,payment=paid))
    return dict(q=q,a=a,box=box,all9_literal_coefficients=polynomial,
                actual_origin=actual,actual_origin_squared_norm=cnorm(actual),rows=rows,
                actual_original_polynomial_feasibility_asserted=False)

DAMAGES={'drop-upper-anchor':UPPER,'drop-lower-anchor':LOWER,
         'quartic-variance-coefficient':WEAK,
         'quartic-real-norm-underpay':WEAK,
         'quartic-cross-coefficient':WEAK,
         'quartic-Hilbert-factor':WEAK,
         'linear-norm-root-underpay':WEAK,
         'last-cleared-coefficient':WEAK,
         'tenth-Bernstein-control':WEAK,
         'anchor-above-marked':WEAK,'centered-energy-decouple':WEAK,
         'odd-root-underpay':WEAK,'synchronized-denominator':DENOMINATOR,
         'diagonal-last-coefficient':WEAK,'last-bivariate-coefficient':WEAK,
         'drop-eighth':WEAK,'last-Bernstein-control':WEAK}

def compute(damage=''):
    if damage:
        m.require(damage in DAMAGES,'explicit mathematical damage')
        m.payment(DAMAGES[damage],'energy',damage)
        raise ValueError('mathematical damage failed to reject')
    rows=[]
    for label,box in [('retained-mean-control',WEAK),('upper-anchor',UPPER),
                      ('lower-anchor',LOWER),('new-product-mean-leaf',PRODUCT),
                      ('separate-actual-mean-norm',DENOMINATOR)]:
        for channel in ('energy','joint'):
            row=m.payment(box,channel)
            m.require(row['status']=='bounded','all conditional fixtures available')
            rows.append(dict(label=label,box=box,payment=row))
    m.require(rows[-2]['payment']['actual_mean_norm_bound']>DENOMINATOR[6]**2+DENOMINATOR[9],
              'fresh fixture genuinely separates actual norm and beta envelope')
    # This transported formal control tests the complete positive lower bound;
    # it is not asserted to be one of the new successful face leaves. The
    # actual defining leaf inequalities are all paid separately by verify.py.
    m.require(rows[0]['payment']['score']>0,'positive transported retained mean control')
    fixtures=[[(Q(9,10),Q(0))]*8,
              [(Q(19,20),Q(1 if j%2 else -1,50)) for j in range(8)],
              [(Q(9,10)+Q(j,1000),Q(j*j,2000)) for j in range(8)],
              [(Q(9,10),Q(0))]*7+[(Q(1,10),Q(0))]]
    controls=[physical(q,a) for q in fixtures for a in (Q(27,40),Q(11,16))]
    # Whole gate controls retain an unavailable status; no negative centered
    # operand is interpreted as a successful bound or original nonexistence.
    bad=WEAK.copy();bad[3]=Q(1,100)
    rejected_gate=m.payment(bad,'energy')
    m.require(rejected_gate['status']=='unavailable-negative-whole-energy-envelope',
              'negative whole centered envelope is unavailable')
    m.require(m.payment(UPPER,'energy')['anchor']<UPPER[0],
              'upper endpoint supplies a genuinely needed anchor')
    m.require(m.payment(LOWER,'energy')['anchor']<LOWER[0],
              'lower endpoint supplies a genuinely needed anchor')
    return m.clean(dict(agent='six-sendov-1',role='researcher',
        status='COMPLETE_CONDITIONAL_POLYNOMIAL_CHECKS',
        conditional_boxes=rows,gaussian_tuple_controls=controls,
        quartic_identity_controls=[quartic_control(q) for q in fixtures+
            [[(Q(1),Q(0))]*4+[(Q(-1),Q(0))]*4]],
        direct_variance_quartic_cap=m.quartic_cap_payment(),
        improved_quartic_cap=m.hilbert_quartic_payment(),
        external_ordinary_input='Banach real-Hilbert norm identity,1810.09373 equation(2)',
        unavailable_gate=rejected_gate,
        all_seven_orders_and_all_nine_controls=True,whole_coefficients_compared=True,
        ordinary_trust='PROOF.md sections5/6a/6b; unformalized SAME-AUTHOR conditional proof',
        actual_polynomial_theorem_established_by_this_conditional_control=False,independent_review=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--damage',default='',choices=['']+list(DAMAGES))
    parser.add_argument('--record',type=Path);args=parser.parse_args();start=time.monotonic()
    try:
        record=compute(args.damage);blob=json.dumps(record,sort_keys=True,separators=(',',':')).encode()
        if args.record:args.record.write_bytes(blob)
        print(json.dumps(dict(status='PASS',record_sha256=sha256(blob).hexdigest(),
            conditional_boxes=len(record['conditional_boxes']),
            gaussian_tuple_controls=len(record['gaussian_tuple_controls']),
            full_bivariate_vectors=7*(len(record['conditional_boxes'])+2*len(record['gaussian_tuple_controls'])),
            full_Bernstein_vectors=len(record['conditional_boxes'])+2*len(record['gaussian_tuple_controls']),
            new_mean_leaf_score=record['conditional_boxes'][0]['payment']['score'],
            seconds=time.monotonic()-start,peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))
    except (ValueError,KeyError,TypeError,ZeroDivisionError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);raise SystemExit(1)
