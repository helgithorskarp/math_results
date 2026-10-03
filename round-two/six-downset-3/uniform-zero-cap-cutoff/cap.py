"""Full-permutation original cap reduction at the zero endpoint.

Ordinary theorem domain: integer k>=3,q>=3k and every deletion subset.
Finite exact controls calibrate the normalizations; they are not a
uniform positivity theorem for the canonical repaired cap.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import hashlib,json,sys

BASE=Path(__file__).resolve().parent
import coefficient as c
import recovery as v
r,require=c.r,c.require

GROUPS=((1,),(2,4),(3,5),(0,),(0,),(1,),(2,4),(6,),(7,),(3,5),(6,))
TYPES=((1,0),(1,0),(2,0),(0,1),(0,2),(1,1),(1,1),(2,0),(3,0),(2,1),(2,1))


def full_trivial_gram(q,k):
    N,s=r.parameters(q,k)
    size=[len(gs)*comb(q,t[1]) for gs,t in zip(GROUPS,TYPES)]
    tab=r.table(q)
    G=[]
    for i,t in enumerate(TYPES):
        row=[]
        for j,tt in enumerate(TYPES):
            count=sum(not(a&b) for a in GROUPS[i] for b in GROUPS[j])
            value=F((N-s)*size[i]*int(i==j))
            if count:
                base,_=tab[tuple(sorted((t,tt)))]
                value-=count*comb(q,t[1])*comb(q-t[1],tt[1])*base
            row.append(value)
        G.append(row)
    require(all(G[i][j]==G[j][i] for i in range(11) for j in range(11)),
            'EVERY original full11 cap Gram reciprocity position')
    return G,size


def standard(q,k):
    N,s=r.parameters(q,k)
    lower=c.standard_gram(q,F(0))
    norms=(2,2*(q-2),2,4,4,2)
    G=[[F(N*norms[i]*int(i==j))-lower[i][j] for j in range(6)] for i in range(6)]
    S,B,Y=r.schur(G,[5],list(range(5)))
    nu=S[0][0]/2
    require(nu>0 and r.schur_psd(G)==6,'whole full nontrivial cap positivity')
    height=F(N-s);w=F(s-F(3*q+2,q),q-1)
    A=r.submatrix(G,[0,1]);e=[G[0][5],G[1][5]]
    theta=sum(x*y[0] for x,y in zip(e,r.solve(A,[[x] for x in e])))
    formula=2*(height*height-w*w)*(height+w-3*theta)/(2*height*(height+w)-(5*height+w)*theta)
    require(nu==formula and height>w>0 and height+w-3*theta>0,
            'whole standard cap two-dimensional plus core-pair identity')
    return nu,{'standard_gram':G,'theta_U':theta,'nu_U':nu,'two_dimensional_formula':formula,
               'full_standard_solve_sha256':r.exact.digest(r.encode(Y))}


def reduced(q,k,t=F(0),sigma=F(0)):
    require(type(q) is int and type(k) is int and k>=3 and q>=3*k,
            'whole cap reduction domain integerk>=3,q>=3k')
    G,size=full_trivial_gram(q,k)
    short,B,Y=r.schur(G,[0,1,2,10],list(range(3,10)))
    require(r.schur_psd(B)==7,'complete seven-family untouched full cap positive')
    anchor=r.submatrix(short,[0,1,2])
    cross=[short[i][3]/q for i in range(3)]
    tau=short[3][3]/q
    nu,standard_record=standard(q,k)
    remaining=q-k
    denominator=nu+(tau-nu)*F(remaining,q)
    require(denominator>0,'ENTIRE surviving target denominator positive')
    unrepaired=[[anchor[i][j]-F(remaining)*cross[i]*cross[j]/denominator for j in range(3)] for i in range(3)]
    repair=[[F(0),2*t,F(0)],[2*t,2*sigma,-2*t],[F(0),-2*t,F(0)]]
    actual=r.subtract(unrepaired,repair)
    return actual,{'q':q,'k':k,'full_even_family_sizes':size,
                   'full_four_family_schur':short,'anchor':anchor,'cross_per_original_target':cross,
                   'tau_U':tau,'nu_U':nu,'remaining_target_count':remaining,
                   'target_denominator':denominator,'repair_even':repair,
                   'full_seven_solve_sha256':r.exact.digest(r.encode(Y)),
                   'untouched_seven_sha256':r.exact.digest(r.encode(B)),
                   'standard':standard_record,'even_cap':actual,
                   'tau_U_not_assumed_positive':True}


def direct(q,k,t=F(0),sigma=F(0)):
    D=r.forms(q,k);_,U=r.evaluate(D,F(0),t,sigma)
    T=[D['keys'].index(key) for key in r.T_KEYS]
    O=[i for i in range(23) if i not in T]
    S,_,_=r.schur(U,T,O)
    even,_=v.cap_parts(S)
    return even


def control(q,k):
    a0,_,_=v.zero_coefficients(q,k)
    delta=min(F(1,4),a0/8)
    t,sigma=a0/4,-3*a0/8+delta
    rows=[]
    for tt,ss in ((F(0),F(0)),(t,sigma),(F(-3,7),F(5,9))):
        G,record=reduced(q,k,tt,ss)
        require(G==direct(q,k,tt,ss),'ALL full-permutation removal and original23 even cap positions')
        rows.append(record)
    return {'q':q,'k':k,'rows':rows,'all_three_original_repair_controls_match':True,
            'controls_not_uniform_positivity':True}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    value=[control(q,k) for q,k in ((9,3),(12,4),(21,7),(28,7),(33,8),(100,20))]
    args.out.write_text(json.dumps(r.encode(value),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'complete_cap_removal_controls':len(value),'each_original_position_matched':True}))
