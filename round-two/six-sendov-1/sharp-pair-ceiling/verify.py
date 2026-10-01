"""Exact finite algebra for the sharp degree-nine normalized pair ceiling.

Actual author six-sendov-1, role researcher. Standard library, CPython3.10+.
Complete minimizer/equality/Schur/transfer arguments remain in PROOF.md.
Arithmetic kernels adapted from the author's8814 checker and rederived here.
No external research implementation, CAS, solver or numerical root is imported.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import argparse
import copy
import hashlib
import sys


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def add(p, q):
    z = [F(0)] * max(len(p), len(q))
    for i, a in enumerate(p): z[i] += a
    for i, a in enumerate(q): z[i] += a
    return trim(z)


def scale(p, a): return trim([a*x for x in p])


def mul(p, q):
    z = [F(0)] * (len(p)+len(q)-1)
    for i, a in enumerate(p):
        for j, b in enumerate(q): z[i+j] += a*b
    return trim(z)


def power(p, n):
    z = [F(1)]
    for _ in range(n): z = mul(z, p)
    return z


def value(p, x):
    z = F(0)
    for a in reversed(p): z = z*x+a
    return z


def affine(p, a, b):
    z = [F(0)]*len(p)
    for i, c in enumerate(p):
        for j in range(i+1): z[j] += c*comb(i,j)*a**(i-j)*(b-a)**j
    return trim(z)


def bernstein(p, d):
    return [sum(p[j]*F(comb(i,j),comb(d,j))
                for j in range(min(i,len(p)-1)+1)) for i in range(d+1)]


def sparse_mul(p,q):
    z={}
    for key,a in p.items():
        for other,b in q.items():
            k=tuple(x+y for x,y in zip(key,other))
            z[k]=z.get(k,F(0))+a*b
    return {k:a for k,a in z.items() if a}


def profile_power(k,j,L,H):
    """Integrate the complete (S,B,t) power polynomial, then compose S."""
    m=6-k-j
    p={(0,0,0):F(1),(1,0,1):F(-1)}
    for _ in range(k): p=sparse_mul(p,{(0,0,0):F(1),(0,0,1):F(-1,2)})
    for _ in range(j): p=sparse_mul(p,{(0,0,0):F(1),(0,1,1):F(-1)})
    for _ in range(m):
        p=sparse_mul(p,{(0,0,0):F(1),(0,0,1):-(8-F(k,2))/m,
                        (0,1,1):F(j,m),(1,0,1):F(1,m)})
    integral={}
    for (s,b,t),a in p.items(): integral[s,b]=integral.get((s,b),F(0))+9*a/(t+1)
    d=m+1
    W=add(H,scale(L,-1))
    xpower=[[F(0)] for _ in range(d+1)]
    for (s,b),a in integral.items():
        for i in range(s+1):
            q=scale(mul(power(L,s-i),power(W,i)),a*comb(s,i))
            q=[F(0)]*b+q
            xpower[i]=add(xpower[i],q)
    controls=[[F(0)] for _ in range(d+1)]
    for i in range(d+1):
        for h in range(i+1):
            controls[i]=add(controls[i],scale(xpower[h],F(comb(i,h),comb(d,h))))
    return xpower,controls


def tensor_mul(p,dp,q,dq):
    """Bernstein multiplication over the coefficient ring Q[B]."""
    z={}
    for (i,j),a in p.items():
        for (k,l),b in q.items():
            w=F(comb(dp[0],i)*comb(dq[0],k),comb(dp[0]+dq[0],i+k))
            w*=F(comb(dp[1],j)*comb(dq[1],l),comb(dp[1]+dq[1],j+l))
            z[i+k,j+l]=add(z.get((i+k,j+l),[F(0)]),scale(mul(a,b),w))
    return z,(dp[0]+dq[0],dp[1]+dq[1])


def profile_tensor(k,j,L,H,integration=F(9,8)):
    """Direct tensor Bernstein in (x,t), then integrate every t layer."""
    one=[F(1)];m=6-k-j
    p={(0,0):one,(1,0):one,(0,1):add(one,scale(L,-1)),
       (1,1):add(one,scale(H,-1))};d=(1,1)
    for r in [[F(1,2)]]*k+[[F(0),F(1)]]*j:
        p,d=tensor_mul(p,d,{(0,0):one,(0,1):add(one,scale(r,-1))},(0,1))
    C=[8-F(k,2),F(-j)]
    r0=scale(add(C,scale(L,-1)),F(1,m))
    r1=scale(add(C,scale(H,-1)),F(1,m))
    factor={(0,0):one,(1,0):one,(0,1):add(one,scale(r0,-1)),
            (1,1):add(one,scale(r1,-1))}
    for _ in range(m): p,d=tensor_mul(p,d,factor,(1,1))
    if d!=(m+1,7):raise ValueError('unexpected complete tensor degree')
    out=[]
    for i in range(m+2):
        q=[F(0)]
        for h in range(8):q=add(q,scale(p[i,h],integration))
        out.append(q)
    return out


def bounds(k,j):
    L=[F(1)] if k<=3 else ([F(6),F(-2)] if k==4 else [F(11,2),F(-1)])
    H=([F(0),F(2)] if j==0 else [F(11,2),F(-1)] if j==1 else [F(6),F(-2)])
    return L,H


P=[F(x) for x in [2188,128,-36,-110,68,-72,28,-7]]
WIDE=(F(9,4),F(23,10))
COARSE=(F(2296776,10**6),F(2296777,10**6))
FINE=(F(22967760069,10**10),F(22967760070,10**10))


class VerificationError(Exception):
    pass


def require(condition,message):
    if not condition: raise VerificationError(message)


def canonical(obj):
    """Rationals are strings; no floating-point proof input exists."""
    return json.loads(json.dumps(obj,default=str,sort_keys=True))


def encoded(obj):
    return json.dumps(canonical(obj),sort_keys=True,separators=(',',':')).encode()


def affine_positive(p):
    return all(value(p,b)>0 for b in WIDE)


def topology():
    """Enumerate every floor/ceiling/free count before pruning feasibility."""
    accepted=[];rejected=[];endpoint=[];excluded_endpoint=[]
    for k in range(7):
        for j in range(7-k):
            m=6-k-j
            if m==0:
                S=[8-F(k,2),F(-j)]
                if affine_positive(add(S,[F(-1)])) and affine_positive(add([F(0),F(2)],scale(S,-1))):
                    endpoint.append({'k':k,'j':j,'S_B_power':S})
                else:
                    require(affine_positive(add([F(1)],scale(S,-1)))
                            or affine_positive(add(S,[F(0),F(-2)])),
                            'endpoint feasibility crosses the wide interval')
                    excluded_endpoint.append([k,j])
                continue
            rawL=[8-F(k,2),F(-(6-k))]
            one=[F(1)]
            if affine_positive(add(rawL,scale(one,-1))): L=rawL
            else:
                require(affine_positive(add(one,scale(rawL,-1))),
                        'lower max branch crosses the wide interval')
                L=one
            rawH=[5+F(j,2),F(-j)]
            paired=[F(0),F(2)]
            if affine_positive(add(paired,scale(rawH,-1))): H=rawH
            else:
                require(affine_positive(add(rawH,scale(paired,-1))),
                        'upper min branch crosses the wide interval')
                H=paired
            margin=add(H,scale(L,-1))
            if affine_positive(margin):
                require((L,H)==bounds(k,j),'independently derived chart bounds mismatch')
                accepted.append([k,j,m])
            else:
                require(affine_positive(scale(margin,-1)),'feasibility crosses the wide interval')
                rejected.append([k,j,m])
    desired=[[k,j,6-k-j] for k in range(6) for j in range(min(2,5-k)+1)]
    require(accepted==desired,'complete chart enumeration mismatch')
    require([[r['k'],r['j']] for r in endpoint]==[[4,2],[5,1]],
            'all-endpoint coverage mismatch')
    return {'all_positive_free_candidates':accepted+rejected,
            'accepted':accepted,'rejected':rejected,'endpoints':endpoint,
            'excluded_endpoints':excluded_endpoint}


def inverse_controls(controls):
    """Expand every x-Bernstein basis polynomial back into powers of x."""
    d=len(controls)-1
    out=[[F(0)] for _ in range(d+1)]
    for i,p in enumerate(controls):
        for j in range(d-i+1):
            out[i+j]=add(out[i+j],scale(p,F(comb(d,i)*comb(d-i,j)*(-1)**j)))
    return out


def endpoint_polynomial(k,j):
    """Direct t-power integration with S=8-k/2-jB and no free radii."""
    p={(0,0):F(1),(0,1):-(8-F(k,2)),(1,1):F(j)}
    for _ in range(k):p=sparse_mul(p,{(0,0):F(1),(0,1):F(-1,2)})
    for _ in range(j):p=sparse_mul(p,{(0,0):F(1),(1,1):F(-1)})
    out=[F(0)]*8
    for (b,t),a in p.items():out[b]+=9*a/(t+1)
    return trim(out)


def monomial(n,indices):
    e=[0]*n
    for i in indices:e[i]+=1
    return tuple(e)


def algebraic_bridges():
    # Complete pair derivative numerator, treating A and B as formal variables.
    x={monomial(4,[0]):F(1)};y={monomial(4,[1]):F(1)}
    difference={**x,monomial(4,[1]):F(-1)}
    factor={monomial(4,[2]):F(1),monomial(4,[0,3]):F(-1),
            monomial(4,[1,3]):F(-1)}
    rhs=sparse_mul(difference,factor)
    lhs={monomial(4,[0,2]):F(1),monomial(4,[1,2]):F(-1),
         monomial(4,[1,1,3]):F(1),monomial(4,[0,0,3]):F(-1)}
    require(lhs==rhs,'full pair derivative numerator identity fails')
    # Full projection identity, before imposing sum(u)=0.
    pair={}
    for i in range(8):
        for j in range(i+1,8):
            for a,b,c in [(i,i+8,1),(j,j+8,1),(i,j+8,-1),(j,i+8,-1)]:
                e=monomial(16,[a,b]);pair[e]=pair.get(e,F(0))+c
    centered={monomial(16,[i,j+8]):F(7 if i==j else -1)
              for i in range(8) for j in range(8)}
    require(pair==centered,'complete centering/projection identity fails')
    return {'pair_numerator_monomials':len(lhs),'centering_monomials':len(pair)}


def direct_radii(r):
    require(len(r)==8 and sum(r)==8 and min(r)>=F(1,2),'invalid rational test radii')
    factors=[F(1)]
    for z in r:factors=mul(factors,[1/z,F(-1)])
    phi=9*sum(a/(i+1) for i,a in enumerate(factors))
    other=[F(1)]
    for z in r[2:]:other=mul(other,[F(1),-z])
    J=9*sum(a/(i+1) for i,a in enumerate(mul(other,[F(1),-(r[0]+r[1])])) )
    prod=F(1)
    for z in r[2:]:prod*=z
    gamma=J/(r[0]**2*r[1]**2*prod)
    gradients=[]
    for j in range(2):
        product=[F(1)]
        for k,z in enumerate(r):
            if k!=j:product=mul(product,[1/z,F(-1)])
        gradients.append(-9*sum(a/(i+1) for i,a in enumerate(product))/r[j]**2)
    require(gradients[0]-gradients[1]==(r[0]-r[1])*gamma,
            'direct full derivative and kernel disagree')
    return {'radii':r,'Phi':phi,'J':J,'Gamma_12':gamma,
            'gradient_difference':gradients[0]-gradients[1]}


def certificate():
    t=topology()
    bridges=algebraic_bridges()
    require(WIDE[0]<COARSE[0]<FINE[0]<FINE[1]<COARSE[1]<WIDE[1],
            'root brackets not nested')
    derivative=[i*P[i] for i in range(1,len(P))]
    db=bernstein(affine(derivative,*WIDE),6)
    require(all(x<0 for x in db),'boundary derivative certificate fails')
    sign_rows=[]
    for I in [WIDE,COARSE,FINE]:
        values=[value(P,b) for b in I]
        require(values[0]>0>values[1],'root sign bracket fails')
        sign_rows.append({'interval':I,'values':values})
    rows=[];positive=[];lookup={}
    for k,j,m in t['accepted']:
        L,H=bounds(k,j)
        xp,bp=profile_power(k,j,L,H)
        bt=profile_tensor(k,j,L,H)
        require(bp==bt,'complete power and direct tensor routes disagree')
        require(inverse_controls(bp)==xp,'complete x-Bernstein inverse fails')
        cells=[]
        for i,p in enumerate(bp):
            if k==j==0 and i==7:
                require(p==scale(P,F(1,2268)),'critical coefficient is not P/2268')
                cells.append({'i':i,'B_power':p,'at_beta':'zero by P(beta)=0'})
            else:
                controls=bernstein(affine(p,*COARSE),7)
                require(all(x>0 for x in controls),'strict positive B-controls fail')
                positive+=controls
                cells.append({'i':i,'B_power':p,'full_B_Bernstein':controls})
        rows.append({'k':k,'j':j,'m':m,'L_B_power':L,'H_B_power':H,
                     'full_x_power_B_power':xp,'full_x_Bernstein':cells})
        lookup[k,j]=bp
    endpoints=[]
    for k,j in [(4,2),(5,1)]:
        ep=endpoint_polynomial(k,j)
        require(ep==lookup[k-1,j][-1],'all-endpoint reclassification fails')
        controls=bernstein(affine(ep,*COARSE),7)
        require(all(x>0 for x in controls),'all-endpoint sign fails')
        endpoints.append({'k':k,'j':j,'B_power':ep,'full_B_Bernstein':controls})
    tests=[direct_radii([F(1)]*8),
           direct_radii([F(9,4),F(2249,1000)]+[F(3501,6000)]*6),
           direct_radii([F(23,10)]*2+[F(17,30)]*6),
           direct_radii([F(23,10),F(2299,1000)]+[F(3401,6000)]*6)]
    require(tests[0]['Phi']==1 and tests[0]['Gamma_12']==F(27,28),'uniform normalization fails')
    require(tests[1]['Gamma_12']>0,'inside-domain direct control fails')
    require(tests[2]['J']==F(-160310809,22680000000),'boundary negative control fails')
    require(tests[3]['Gamma_12']<0 and tests[3]['gradient_difference']<0
            and tests[3]['Phi']>1,'unequal-pair obstruction scope fails')
    kappa=F(492694,984375)
    transfer=F(25,338)*kappa
    require(transfer>F(1,28),'inherited transfer coefficient fails')
    require(len(rows)==15 and sum(len(x['full_x_Bernstein']) for x in rows)==76
            and len(positive)==600,'complete certificate census fails')
    return {'scope':'exact finite certificate; written analytic bridges and inherited8814 corollary separate',
            'P':P,'wide':WIDE,'coarse':COARSE,'fine':FINE,
            'root_sign_brackets':sign_rows,'derivative_Bernstein':db,
            'topology':t,'profiles':rows,'all_endpoints':endpoints,
            'profile_controls':76,'zero_at_beta':1,'positive_profile_controls':75,
            'positive_B_controls':600,'minimum_positive_B_control':min(positive),
            'algebraic_bridges':bridges,'direct_rational_controls':tests,
            'inherited8814_kappa':kappa,'transfer_step':F(5,13),
            'transfer_coefficient':transfer,'claimed_uniform_coefficient':F(1,28)}


def fixture_matches(fixture,record):
    require(fixture==canonical(record),'full regenerated fixture mismatch')


def rejection_controls(record):
    rejected=0
    L,H=bounds(0,0)
    xp,bp=profile_power(0,0,L,H)
    def expect_failure(fn):
        nonlocal rejected
        try:fn()
        except VerificationError:rejected+=1;return
        raise VerificationError('damaged mathematical certificate accepted')
    expect_failure(lambda:require(profile_tensor(0,0,L,H,F(9,7))==bp,
                                  'wrong integration factor'))
    wrong=P.copy();wrong[-1]+=1
    expect_failure(lambda:require(bp[-1]==scale(wrong,F(1,2268)),'wrong boundary polynomial'))
    desired=record['topology']['accepted'][1:]
    expect_failure(lambda:require(topology()['accepted']==desired,'omitted full chart'))
    db=record['derivative_Bernstein'].copy();db[0]=-db[0]
    expect_failure(lambda:require(all(x<0 for x in db),'wrong derivative sign'))
    valid=canonical(record)
    damaged=copy.deepcopy(valid);damaged['profiles'].pop()
    expect_failure(lambda:fixture_matches(damaged,record))
    damaged=copy.deepcopy(valid);damaged['profiles'][0]['full_x_Bernstein'][-1]['B_power'][-1]='-6/2268'
    expect_failure(lambda:fixture_matches(damaged,record))
    damaged=copy.deepcopy(valid);damaged['profiles'][1]['full_x_Bernstein'][0]['full_B_Bernstein'][0]='0'
    expect_failure(lambda:fixture_matches(damaged,record))
    damaged=copy.deepcopy(valid);damaged['fine'][0]='23/10'
    expect_failure(lambda:fixture_matches(damaged,record))
    require(rejected==8,'negative control census fails')
    return {'mathematical_damages_rejected':4,'fixture_damages_rejected':4}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-fixture',type=Path)
    args=parser.parse_args()
    record=certificate()
    damages=rejection_controls(record)
    if args.write_fixture:
        args.write_fixture.write_text(json.dumps(canonical(record),sort_keys=True,indent=2)+'\n')
    else:
        try:fixture=json.loads(args.fixture.read_text())
        except (OSError,ValueError) as exc:raise VerificationError('fixture missing or malformed: '+str(exc)) from exc
        fixture_matches(fixture,record)
    summary={'status':'PASS','full_profiles':15,'complete_x_controls':76,
             'positive_B_controls':600,'algebraic_zero':1,'all_endpoint_profiles':2,
             'full_power_tensor_routes_and_inverses':15,'direct_rational_controls':4,
             'root_derivative_controls':7,**damages,
             'record_sha256':hashlib.sha256(encoded(record)).hexdigest()}
    print(json.dumps(summary,sort_keys=True))
    return 0


if __name__=='__main__':
    try:raise SystemExit(main())
    except (VerificationError,ValueError,ArithmeticError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
