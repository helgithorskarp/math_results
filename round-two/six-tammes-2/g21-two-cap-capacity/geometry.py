"""Exact algebra supporting both exhaustive core candidates and packing.

The ordinary two-plane/reflection proof is in PROOF.md. These ring
identities establish its displayed formulas, not an optimizer assumption.
"""
from polynomials import P,dot
from model import LABELS,CONTACTS,NORMAL,CUT,SECOND_NORMAL,SECOND_CUT,make,positive_factors
from algebra import require,primitive

def identities():
    t=P.var(0);Y,O,m=make(t);a=1+t;b=1-t;c=1+2*t;S=1-t*t;names=[]
    def zero(name,p):
        require(not p.c,'nonzero generic identity '+name);names.append(name)
    for i in LABELS:zero('unit-'+str(i),dot(Y[i],Y[i],t)-O*O)
    for i,j in CONTACTS:zero('contact-'+str(i)+'-'+str(j),dot(Y[i],Y[j],t)-t*O*O)
    reflections=((8,2,4,1),(10,1,2,4),(12,1,10,2),(0,5,7,12),
                 (11,0,5,7),(9,5,11,0),(6,0,11,5))
    for n,i,j,o in reflections:
        for k in range(3):zero('reflection-'+str(n)+'-'+str(k),a*(Y[n][k]+Y[o][k])-2*t*(Y[i][k]+Y[j][k]))
    dnum=dot(Y[9],Y[12],t);dn=2*m['Q4']-a**3
    for k in range(3):
        zero('generalized-reflection-5-'+str(k),(O*O+dnum)*(Y[5][k]+Y[10][k])-2*t*O*O*(Y[9][k]+Y[12][k]))
        zero('A-chain-7-'+str(k),a**3*Y[9][k]-4*t*t*(a+2*t)*Y[5][k]-a*(a*a-4*t*t)*Y[12][k]+4*t*m['L']*Y[7][k])
    zero('intrinsic9-12-formula',a**3*dnum-dn*O*O)
    zero('intrinsic9-12-from-A-chain',4*t**3*(1+3*t)-4*t*t*m['L']+a*b*(1+3*t)-dn)
    V=m['V'];B=m['B']
    zero('seed9-unit',dot(V,V,t)-a**6)
    zero('seed9-product10',dot(V,B[10],t)-t*a**5)
    zero('seed9-product12',dot(V,B[12],t)-dn*a*a)
    R9=[2*((t*a**3-t*dn)*B[10][j]+(dn-t*t*a**3)*B[12][j])-S*a*a*V[j] for j in range(3)];RD=a**5*S
    zero('other9-unit',dot(R9,R9,t)-RD*RD)
    zero('other9-product10',dot(R9,B[10],t)-t*RD*a*a)
    zero('other9-product12',a**3*dot(R9,B[12],t)-dn*RD*a*a)
    discriminant=a**6*(1-2*t*t)+2*t*t*a**3*dn-dn*dn
    zero('strict-two-solution-discriminant',discriminant-16*t*t*b*b*c*m['L']**2)
    e2=[t*0,t*0+1,t*0];badgap=dot(R9,e2,t)-t*RD
    factored=(5*t*t-1)*(1+7*t+7*t*t*b)
    zero('other9-packing2-strict-violation',a**5*badgap-b*factored*RD)
    zero('first-cap-normal-squared',dot([t*0+x for x in NORMAL],[t*0+x for x in NORMAL],t)-(621-620*t))
    zero('second-cap-normal-squared',dot([t*0+x for x in SECOND_NORMAL],[t*0+x for x in SECOND_NORMAL],t)-(233-232*t))
    gap68=primitive(t*O*O-dot(Y[6],Y[8],t),positive_factors(t));cubic=23*t**3+17*t*t+t-1
    zero('sole-core-packing-gap-factor',gap68-(3*t*t-1)*cubic)
    require(len(names)==73,'all73 generic normalization/contact/branch/cap identities')
    return {'generic_unit_identities':12,'literal_contact_identities':21,
            'all_generic_identities_actually_checked':73,'names':names,
            'other_candidate_exclusion':'(1-t)(5t^2-1)(1+7t+7t^2(1-t))/(1+t)^5>0',
            'two_candidate_Gram_discriminant':'16t^2(1-t)^2(1+2t)L^2/(1+t)^6>0',
            'core_feasibility_exact_condition':'3t^2-1>=0;44 other noncontact gaps strictly positive'}

def packing_obligations():
    t=P.var(0);Y,O,_=make(t);contacts=set(CONTACTS);known=positive_factors(t);count=0
    from itertools import combinations
    for i,j in combinations(LABELS,2):
        if (i,j) in contacts or (i,j)==(6,8):continue
        count+=1;yield 'strict-core-gap-'+str(i)+'-'+str(j),primitive(t*O*O-dot(Y[i],Y[j],t),known)
    require(count==44,'all44 nonexceptional core packing comparisons')
