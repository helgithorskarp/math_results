"""Generic contact identity and positive/negative geometric controls."""
from census import A,load,require,prime_data,modular_offsets,circle_polynomial,local_tables,colour,PRIMES
from itertools import combinations
from fractions import Fraction as Q
import json
from math import lcm
import audit as independent


def symbolic():
    M=load('polynomials','hadwiger_nelson_cross_six_cycle/identities.py',
           '2c0b7986b5da71c06f5d152a4c83c0c6196c2cdac3942cab6243f5da0541e370')
    a,b,c,d,e,f,g,h,s,t,eps=M.variables('a b c d e f g h s t eps')
    X,Y,XX,YY,D=(a,b),(c,d),(e,f),(g,h),(s,t)
    def plus(x,y):return tuple(a+b for a,b in zip(x,y))
    def minus(x,y):return tuple(a-b for a,b in zip(x,y))
    def scale(x,n):return tuple(n*a for a in x)
    def mul(x,y):
        a,b=x;c,d=y
        return a*c-b*d,a*d+b*c-b*d
    def bar(x):return x[0]-x[1],-x[1]
    def norm(x):return x[0]*x[0]-x[0]*x[1]+x[1]*x[1],0
    def F(x,y):return minus(minus(plus(norm(x),scale(norm(y),4)),mul(D,mul(bar(x),y))),(eps,0))
    left=minus(mul(mul(D,mul(bar(XX),bar(X))),minus(YY,Y)),
               mul(mul(bar(XX),bar(X)),minus(XX,X)))
    right=minus(scale(minus(mul(norm(YY),bar(X)),mul(norm(Y),bar(XX))),4),
                scale(minus(bar(X),bar(XX)),eps))
    right=plus(right,minus(mul(F(X,Y),bar(XX)),mul(F(XX,YY),bar(X))))
    require(all(not (M.P(x)-M.P(y)).terms for x,y in zip(left,right)),'generic divided-difference identity failed')
    return {'coefficient_identities':2,'left_terms':[len(M.P(x).terms) for x in left]}


def geometry():
    old=load('small_witness','hadwiger_nelson_first_negative_trace/verify.py',
             '6e670f2658a04380576a3f842b968eca7f2e0ae0b0641b636d58932f4065d845')
    P,S,witness=old.obstruction()
    P,S=[[A.sub(x,G[0]) for x in G] for G in (P,S)]
    n=len(S);tables=local_tables(P,S);ids=[i*n+j for i,j in witness]
    require([len(P),len(S)]==[13,7],'positive control changed')
    for place in (0,1):
        keys=[tuple((tables[1][place][j][c]-2*tables[0][place][i][c])%8 for c in (0,1)) for i,j in witness]
        require(len(set(keys))==1,'genuine unit contacts rejected by congruence')
        require({colour(tables,0,place,i) for i,j in witness}==set(range(4)),'control not saturated')
    pair_checks=[]
    for (i,j),(ii,jj) in combinations(witness,2):
        dp,dq=A.sub(P[ii],P[i]),A.sub(S[jj],S[j])
        require(A.C.residue(dp)!=0,'control source residues coincide')
        require(A.C.residue(A.scale(dq,Q(1,2)))!=0,'pair valuations not shifted by one')
        require(A.C.depth(A.scale(A.sub(dq,A.scale(dp,2)),Q(1,8)))==0,'contact congruence failed')
        pair_checks.append([i,j,ii,jj])
    modular=[]
    L=lcm(*(x.denominator for G in (P,S) for pt in G for x in pt))
    IP,IS=[[tuple(int(x*L) for x in pt) for pt in G] for G in (P,S)]
    for p in PRIMES:
        offsets=modular_offsets(P,S,p,prime_data(p))
        require(all(circle_polynomial(offsets,triple,p)==0 for triple in combinations(ids,3)),
                'unit-circle positive control rejected')
        paired=independent.modular_complex(IP,IS,p,prime_data(p),denominator=L)
        require(all(independent.heron(paired,triple,p)==0 for triple in combinations(ids,3)),
                'independent Heron positive control rejected')
        # Independent rational circles, and a collinear triple, exercise non-solutions too.
        positive=[(1,0),(-1,0),(0,1)]
        radius2=[(2*x,2*y) for x,y in positive]
        line=[(0,0),(1,0),(2,0)]
        require(circle_polynomial(positive,(0,1,2),p)==0,'rational unit circle rejected')
        require(circle_polynomial(radius2,(0,1,2),p)!=0,'radius-two negative control accepted')
        require(circle_polynomial(line,(0,1,2),p)!=0,'collinear negative control accepted')
        modular.append({'prime':p,'positive_witness_triples':4,'both_circle_formulas_pass':True,'unit_circle_pass':True,
                        'radius_two_rejected':True,'collinear_rejected':True})
    return {'saturation_witness_source_sizes':[13,7],'two_place_cells_pass':True,
            'matching_pair_differences_checked':len(pair_checks),'modular_controls':modular,
            'positive_control_does_not_establish_five_chromaticity':True}

if __name__=='__main__':print(json.dumps({'symbolic':symbolic(),'geometry':geometry()},indent=2))
