"""Independent audits of the adjacent-five and double-five-Q metric bridges."""
from itertools import combinations
import json
import sympy as sp
import metric as m

c,ONE,Z=m.c,m.ONE,m.Z

def determinant(rows):
    a,b,d=rows
    return a[0]*(b[1]*d[2]-b[2]*d[1])-a[1]*(b[0]*d[2]-b[2]*d[0])+a[2]*(b[0]*d[1]-b[1]*d[0])


def cramer(coords, labels):
    rows=[tuple((ONE-c)*x+c*sum(coords[i],Z) for x in coords[i]) for i in labels]
    d=determinant(rows)
    nums=[]
    for j in range(3):
        replaced=[tuple(c if k==j else row[k] for k in range(3)) for row in rows]
        nums.append(determinant(replaced))
    # adjugate is built by cofactors, not by division by the determinant.
    adj=[]
    for i in range(3):
        ar=[]
        for j in range(3):
            minor=[[rows[r][s] for s in range(3) if s!=i] for r in range(3) if r!=j]
            ar.append((-1)**(i+j)*(minor[0][0]*minor[1][1]-minor[0][1]*minor[1][0]))
        adj.append(ar)
    for i in range(3):
        for j in range(3):
            m.equal(sum((adj[i][k]*rows[k][j] for k in range(3)),Z), d if i==j else Z,'adjugate identity')
        m.equal(c*sum(adj[i],Z),nums[i],'Cramer numerators')
    return m.dot(nums,nums)-d*d


def distinct_pairs(coords,exceptions=(),name='patch'):
    counts={'contacts':0,'positive_gaps':0,'exceptional_distinct':0}
    for i,j in combinations(sorted(coords),2):
        gap=c-m.dot(coords[i],coords[j])
        if not gap:counts['contacts']+=1
        elif (i,j) in exceptions:
            m.certify(ONE-m.dot(coords[i],coords[j]),name+f'_distinct_{i}_{j}',1)
            counts['exceptional_distinct']+=1
        else:
            m.certify(gap,name+f'_gap_{i}_{j}',1);counts['positive_gaps']+=1
    return counts


def adjacent():
    a={1:(ONE,Z,Z),6:(Z,ONE,Z),7:(Z,Z,ONE)}
    for new,x,y,old in [(2,1,6,7),(0,1,2,6),(3,0,1,2),(4,0,3,1),(5,0,4,3)]:
        a[new]=m.reflect(a[x],a[y],a[old])
    for new,f,x,y in [(8,0,2,5),(9,1,3,7),(10,2,6,8),(11,3,4,9),(12,4,5,11),(13,6,7,10)]:
        a[new]=m.opposite(a[f],a[x],a[y],f'adj_Q{new}')
    m.audit(a,'adjacent')
    exceptions=((8,12),(9,13),(10,12),(11,13))
    counts=distinct_pairs(a,exceptions,'adj')
    m.require(counts=={'contacts':25,'positive_gaps':62,'exceptional_distinct':4},'adjacent complete91 pairs')
    gap_a=c-m.dot(a[8],a[12]);gap_b=c-m.dot(a[10],a[12])
    m.equal(gap_a,c-m.dot(a[9],a[13]),'classA gaps')
    m.equal(gap_b,c-m.dot(a[11],a[13]),'classB gaps')
    results=[]
    expected=[c*c*(1-3*c*c+2*c**3),c+4*c*c-6*c**3-34*c**4+7*c**5+86*c**6-18*c**7-80*c**8+40*c**9]
    for index,(gap,labels) in enumerate([(gap_a,(10,11,12)),(gap_b,(8,9,12))]):
        g=cramer(a,labels)
        m.strict_polynomial(g.denom)
        p,q=m.polynomial(gap.numer),m.polynomial(g.numer)
        gcd=sp.gcd(p,q).monic()
        expected_gcd=m.polynomial(expected[index].numer).monic()
        m.require(gcd==expected_gcd,'independently computed printed gcd')
        s,t,h=sp.gcdex(p,q)
        m.require(s*p+t*q==h and h.monic()==gcd,'independent Bezout identity')
        cert=m.certify(m.K.from_expr(gcd.as_expr()),'adj_gcd_'+str(index))
        results.append({'neighbor_triple':list(labels),'gcd_coefficients':cert['numerator']['coefficients'],
                        'gcd_Sturm_variations':cert['numerator']['Sturm_variations'],'Bezout_identity_verified':True})
    return {'complete_pair_counts':counts,'classes':results}


def double_Q():
    base={0:(ONE,Z,Z),2:(Z,ONE,Z),4:(Z,Z,ONE)}
    for new,a,b,old in [(5,0,4,2),(6,0,5,4),(3,0,6,5)]:
        base[new]=m.reflect(base[a],base[b],base[old])
    base[1]=m.opposite(base[0],base[2],base[3],'double_Q1')
    positive=None
    for s in (-1,1):
        a=dict(base);a[7]=m.third(a[1],a[3],s)
        a[8]=m.reflect(a[1],a[7],a[3]);a[9]=m.reflect(a[1],a[8],a[7])
        endpoint=m.reflect(a[1],a[9],a[8]);m.audit(a,'double_seed')
        if s==-1:m.certify(ONE-m.dot(endpoint,a[2]),'double_negative_endpoint_difference',1)
        else:
            for x,y in zip(endpoint,a[2]):m.equal(x,y,'double_positive_endpoint_equality')
            positive=a
    a=positive;counts10=distinct_pairs(a,name='double10')
    m.require(counts10=={'contacts':18,'positive_gaps':27,'exceptional_distinct':0},'double10 pairs')
    for new,f,x,y in [(10,2,4,9),(11,3,6,7)]:
        a[new]=m.opposite(a[f],a[x],a[y],f'double_Q{new}')
    counts12=distinct_pairs(a,name='double12')
    m.require(counts12=={'contacts':22,'positive_gaps':44,'exceptional_distinct':0},'double12 pairs')
    for new,f,x,y in [(12,4,5,10),(13,9,8,10),(14,6,5,11)]:
        a[new]=m.opposite(a[f],a[x],a[y],f'double_Q{new}')
    m.audit(a,'double_full')
    m.certify(c-m.dot(a[12],a[14]),'double_alias_forced',-1)
    p=1+2*c-5*c*c-8*c**3+6*c**4+4*c**5
    d=1+3*c-3*c*c-11*c**3+4*c**4+12*c**5+2*c**6
    m.equal(a[12][1]-a[14][1],-2*c*p/d,'printed alias polynomial')
    m.certify(p,'double_P_left',1,m.L,sp.Rational(11,20))
    m.certify(p,'double_P_right',-1,sp.Rational(14,25),m.H)
    m.certify(ONE-m.dot(a[12],a[13]),'double_actual_distinct_12_13',1)
    m.certify(c-m.dot(a[12],a[13]),'double_forbidden_strip',-1,sp.Rational(11,20),sp.Rational(14,25))
    return {'ten_point_pairs':counts10,'twelve_point_pairs':counts12,
            'possible_alias_root_strip':['11/20','14/25'],'distinct_original_forbidden_pair':[12,13]}


def run():
    m.identities = m.coordinate_checks = m.coordinate_endpoint_zeros = 0
    m.sign_records.clear()
    a=adjacent();d=double_Q()
    selected={k:v for k,v in m.sign_records.items() if '_gap_' not in k and '_distinct_' not in k}
    return {'agent':'six-reviewer-4','role':'independent mathematical reviewer','sympy_version':sp.__version__,
            'identities':m.identities,'coordinate_denominator_checks':m.coordinate_checks,
            'adjacent_five_audit':a,'double_five_Q_audit':d,
            'strict_Sturm_certificates':selected,'all_pair_signs_checked':91+45+66,
            'scope':'Independent arithmetic bridges for original-fan disjointness. Written rotation, saturated-star and original-alias arguments are audited separately.'}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
