"""Regenerate both scalar fields from complete original rational identities.

All checks use stdlib rational polynomials. No saved symbolic field is
needed. Every cancellation is an exact multiplied-back division.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import portable_frame as f
import lower_branch as b
p=f.p;require=f.require
Q,K=p.Q,p.K
C,A,M,S=p.constant,p.add,p.mul,p.scale


def product(*xs):
    out=C(1)
    for x in xs:out=M(out,x)
    return out


def standard_polynomial():
    D,tab=f.z.clearing()
    tab={key:{power:value for power,value in v.items() if power[1]==0}
         for key,v in tab.items()}
    L=S(product(Q,A(Q,C(-1))),4)
    height=A(S(M(Q,Q),F(1,2)),S(Q,F(7,2)),C(4),S(K,-1))
    G=[]
    for i,t in enumerate(f.cap.c.TYPES):
        norm=S(A(Q,C(-2)),2) if t[1]==2 else C(2)
        row=[]
        for j,tt in enumerate(f.cap.c.TYPES):
            value=S(product(D,height,norm),len(f.cap.c.GROUPS[i])*int(i==j))
            count=sum(not(x&y) for x in f.cap.c.GROUPS[i] for y in f.cap.c.GROUPS[j])
            if count:
                outside=C(-2) if t[1]==tt[1]==1 else S(product(A(Q,C(-2)),A(Q,C(-3))),-2) if t[1]==tt[1]==2 else S(A(Q,C(-2)),-2)
                value=A(value,S(M(outside,tab[tuple(sorted((t,tt)))]),-count))
            row.append(p.divide(M(L,value),D))
        G.append(row)
    require(all(G[i][j]==G[j][i] for i in range(6) for j in range(6)),
            'ENTIRE independent full standard cap polynomial reciprocity')
    require(all(value.denominator==1 for row in G for poly in row for value in poly.values()),
            'EVERY independently cleared standard polynomial integer coefficient')
    wn=A(S(M(Q,Q),3),Q,C(-2));wd=product(Q,A(Q,C(-1)))
    for i,norm in enumerate((2,4,4,2)):
        for j in range(4):
            expected=S(M(L,height),norm) if i==j else S(p.divide(M(L,wn),wd),norm) if (i,j) in ((0,3),(3,0),(1,2),(2,1)) else C(0)
            require(G[i+2][j+2]==expected,
                    'EVERY q,k full standard two-core-pair identity coefficient')
    for i in range(2):
        for j,multiple in enumerate((1,2,2,1)):
            require(G[i][j+2]==S(G[i][5],multiple),
                    'EVERY q,k standard outside-to-core rank-one identity coefficient')
    B=f.submatrix(G,[0,1]);e=[G[0][5],G[1][5]]
    bd=A(M(B[0][0],B[1][1]),S(M(B[0][1],B[1][0]),-1))
    tn=A(product(e[0],e[0],B[1][1]),product(e[1],e[1],B[0][0]),
         S(product(e[0],e[1],B[0][1]),-2))
    td=M(L,bd)
    np=S(product(A(product(height,height,wd,wd),S(M(wn,wn),-1)),
                 A(product(height,wd,td),M(wn,td),S(M(tn,wd),-3))),2)
    dp=product(wd,wd,A(S(product(height,A(M(height,wd),wn),td),2),
                      S(product(A(S(M(height,wd),5),wn),tn),-1)))
    return G,L,np,dp


def positivity_record(poly,offset=3):
    shifted=b.substitute(poly,A(C(3*offset),S(Q,3),K),A(C(offset),Q))
    # Here Q is x and K is u: k=offset+x, q=3k+u.
    return {'count':len(shifted),'negative_count':sum(v<0 for v in shifted.values()),
            'positive_constant':shifted.get((0,0),F(0))>0,
            'entire_shifted_coefficients':f.record(shifted)}


def generated():
    G,L,np,dp=standard_polynomial()
    nu_factor=S(product(Q,A(Q,C(-1)),A(Q,C(-1))),16)
    nn,nd=p.divide(np,nu_factor),p.divide(dp,nu_factor)
    closed=json.loads((f.cap.BASE/'CLOSED-ZERO.json').read_text())
    numer={row['name']:f.z.dense(row['numerator']) for row in closed['rows']}
    denom={row['name']:f.z.dense(row['denominator']) for row in closed['rows']}
    ap=product(Q,K,numer['nu0'],numer['tau0'])
    aq=A(product(A(Q,S(K,-1)),numer['tau0'],denom['nu0']),
         product(K,numer['nu0'],denom['tau0']))
    a_factor=product(Q,A(Q,C(-1)),A(S(Q,3),C(5)),A(S(Q,3),C(5)))
    an,ad=p.divide(ap,a_factor),p.divide(aq,a_factor)
    require(all(value.denominator==1 for poly in (nn,nd,an,ad)
                for value in poly.values()),'ENTIRE regenerated scalar fields integral')
    return {'nu_U':{'numerator':f.record(nn),'denominator':f.record(nd)},
            'a0':{'numerator':f.record(an),'denominator':f.record(ad)}}


def fields(raw=None):
    if raw is None:raw=generated()
    nn,nd=(f.decode(raw['nu_U'][side]) for side in ('numerator','denominator'))
    an,ad=(f.decode(raw['a0'][side]) for side in ('numerator','denominator'))
    G,L,np,dp=standard_polynomial()
    require(M(nn,dp)==M(nd,np),'EVERY complete nu_U field identity coefficient')
    closed=json.loads((f.cap.BASE/'CLOSED-ZERO.json').read_text())
    numer={row['name']:f.z.dense(row['numerator']) for row in closed['rows']}
    denom={row['name']:f.z.dense(row['denominator']) for row in closed['rows']}
    ap=product(Q,K,numer['nu0'],numer['tau0'])
    aq=A(product(A(Q,S(K,-1)),numer['tau0'],denom['nu0']),
         product(K,numer['nu0'],denom['tau0']))
    require(M(an,aq)==M(ad,ap),'EVERY complete a0 field identity coefficient')
    afactor=p.divide(aq,ad)
    require(all(power[1]==0 for power in afactor),
            'whole a0 cancellation factor independentk')
    ashift=b.substitute(afactor,A(C(4),Q),K)
    require(ashift.get((0,0),0)>0 and all(v>=0 for v in ashift.values()),
            'EVERY q4+u a0 cancellation factor coefficient nonnegative')
    sign=positivity_record(nd)
    require(sign['negative_count']==0 and sign['positive_constant'],
            'EVERY nu_U denominator coefficient positive on whole q>=3k,k>=3 domain')
    controls=[]
    for q,k in ((9,3),(12,4),(21,7),(28,7),(100,20)):
        direct,details=f.cap.standard(q,k)
        require(p.evaluate(nd,q,k)>0 and p.evaluate(nn,q,k)==direct*p.evaluate(nd,q,k),
                'full independent original standard cap scalar control')
        for i in range(6):
            for j in range(6):
                require(p.evaluate(G[i][j],q,k)==p.evaluate(L,q,k)*details['standard_gram'][i][j],
                        'ALL independent full6 Gram control positions')
        controls.append([q,k,str(direct)])
    return {'actual_agent':'six-downset-3','role':'researcher',
            'whole_nu_U_coefficient_identity':True,'whole_a0_coefficient_identity':True,
            'whole_standard_rank_one_identities':True,
            'nu_U_positive_denominator':sign,'a0_denominator_positive_by_prior_raw_and_positive_factor':True,
            'complete_a0_cancellation_factor_shift4':f.record(ashift),
            'controls':controls,'complete_cleared_standard6':f.matrix_record(G),
            'CAS_not_imported':True,'every_division_multiplied_back':True,
            'ordinary_prior_fullspace_positivity_bridge_credited':True,
            'independent_person_review':False}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    value=fields();args.out.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'whole_two_field_identities':True,'nu_denominator_whole_shifted_coefficients':value['nu_U_positive_denominator']['count']}))
