"""Multiplicity-sensitive exact Pasch defect certificates.

The unbounded ordinary proof is in PASCH_MULTIPLICITY_BOUND.md. Existing
simple designs, v>=7 and lambda>=2; a legal move forces q=v-2-lambda>=1.
The dimension-free budget uses mu=min(lambda,q), not a design census.
The explicit sharp_fixture attains the budget 14 at mu=4.
six-downset-2, researcher. Standard library; assertions enabled.
"""
from fractions import Fraction as F
from itertools import combinations,product
from content_psd import content_psd_rank
from cyclic13_spectral import initial_point_certificate,comparison_data
from pasch_defect import switch_update
from uniform_lambda_small import parameters
from uniform_lambda_small import centered_certificate as ordinary_centered
from uniform_lambda_small import maximal_certificate as ordinary_maximal

ALPHA=(0,2,4,5,6,7,8)


def degree_certificate(v,lam,kappa=None):
    parameters(v,lam);assert v>=7
    q=v-2-lam;assert q>=1,'A full triple design has no legal move'
    mu=min(lam,q)
    if kappa is None:
        if mu==1:kappa=F(0)
        elif mu==2:kappa=F(22,3)
        elif mu==3:kappa=F(34,3)
        elif mu==4:kappa=F(14)
        else:
            kappa=10
            while kappa*(kappa-8)<48*mu-108:kappa+=1
            kappa=F(kappa)
    kappa=F(kappa);assert kappa>=0
    margins={}
    if mu==1:
        assert kappa>=0
    elif mu==2:
        for e in range(4):
            margin=kappa*(kappa-ALPHA[e])-2*(24-6*e)
            assert kappa>=ALPHA[e] and margin>=0
            margins[str(e)]=margin
    else:
        assert kappa>=10 and kappa*(kappa-8)>=48*mu-108
        margins['uniform']=kappa*(kappa-8)-(48*mu-108)
    return {'v':v,'lambda':lam,'q':q,'mu':mu,'kappa':kappa,
            'comparison_margins':margins,'inside_norm_table':ALPHA}


def norm_forms(T,G,kappa):
    """Schur equivalent to both kappa*K +/- Delta PSD, for kappa>0."""
    kappa=F(kappa);assert kappa>0
    return [[[kappa*kappa*int(i==j)+sign*2*kappa*(T[i][j]+T[j][i])-2*G[i][j]
              for j in range(3)]for i in range(3)]for sign in (-1,1)]


def degree_update(v,lam,blocks,groups,reverse=False,kappa=None):
    """Literal legal update plus pair-capacity, trace and norm certificates."""
    cert=degree_certificate(v,lam,kappa)
    new,Z,Delta,info=switch_update(v,lam,blocks,groups,reverse)
    T=info['T'];outside=sorted(map(int,info['outside_rows']))
    O=[info['outside_rows'][str(x)]for x in outside]
    G=[[sum(row[i]*row[j]for row in O)for j in range(3)]for i in range(3)]
    U=set(blocks);complement=lam>cert['q'];local=[]
    c=[sum(abs(T[j][k])for j in range(3))for k in range(3)]
    for k in range(3):
        i,j=[a for a in range(3)if a!=k]
        u=[int(sum(1<<x for x in (*groups[i],y))in U)for y in groups[j]]
        z=[int(sum(1<<x for x in (*groups[j],y))in U)for y in groups[i]]
        if complement:u=[1-b for b in u];z=[1-b for b in z]
        n=sum(u)+sum(z)
        assert c[k]==abs(u[0]-u[1])+abs(z[0]-z[1])
        assert c[k]<=n<=4-c[k]
        sets=[];signs=[]
        for a,b in product(range(2),repeat=2):
            pair=(1<<groups[i][a])|(1<<groups[j][b])
            xs={x for x in outside if ((pair|(1<<x))in U)!=complement}
            assert len(xs)==cert['mu']-1-u[b]-z[a]
            sets.append(xs)
            signs.append((-1 if (a+b)%2==0 else 1)*(-1 if reverse else 1)*(-1 if complement else 1))
        assert all(sum(sign*int(x in xs)for sign,xs in zip(signs,sets))==O[row][k]
                   for row,x in enumerate(outside))
        l1=sum(abs(row[k])for row in O)
        square_bound=8*(cert['mu']-1)-4*n-2*int(c[k]>0)
        assert l1<=4*(cert['mu']-1)-2*n and G[k][k]<=square_bound
        local.append({'inside_extra_bits':u+z,'inside_extra_count':n,'column_support_count':c[k],
                      'outside_completion_counts':[len(xs)for xs in sets],
                      'outside_column_l1':l1,'outside_column_square':G[k][k],
                      'outside_column_square_bound':square_bound})
    e=sum(c);p=sum(z>0 for z in c);alpha=ALPHA[e]
    M=24*(cert['mu']-1)-4*e-2*p
    assert sum(G[i][i]for i in range(3))<=M
    if cert['mu']==1:assert e==0 and not any(z for row in O for z in row) and not any(z for row in Delta for z in row)
    else:
        if cert['mu']==2:assert max(c)<=1
        assert cert['kappa']>=alpha and cert['kappa']*(cert['kappa']-alpha)>=2*M
    ranks=[]
    if cert['kappa']:
        for form in norm_forms(T,G,cert['kappa']):ranks.append(content_psd_rank(form))
    info.update(degree_certificate=cert,complement_for_capacity=complement,
        local_columns=local,e=e,p=p,inside_norm_bound=alpha,outside_Gram=G,
        outside_trace=sum(G[i][i]for i in range(3)),outside_trace_bound=M,
        scalar_comparison_margin=cert['kappa']*(cert['kappa']-alpha)-2*M,
        signed_three_by_three_norm_ranks=ranks)
    return new,Z,Delta,info


def chain_data(v,lam,initial,sequence,gamma0,bound,kappa=None):
    sequence=list(sequence);gamma0=F(gamma0)
    Z,initial_info=initial_point_certificate(v,lam,initial,gamma0)
    stability=degree_certificate(v,lam,kappa)
    current=sorted(initial);updates=[]
    for groups,reverse in sequence:
        current,Z,Delta,info=degree_update(v,lam,current,groups,reverse,stability['kappa'])
        updates.append((Delta,info))
    gamma=gamma0+len(sequence)*stability['kappa']
    data=comparison_data(v,lam,gamma,bound)
    data.update(initial_point_certificate=initial_info,degree_certificate=stability)
    return current,Z,data,updates


def certificates(v,lam,initial,sequence,gamma0,bound,kappa=None,eta=None):
    blocks,Z,data,updates=chain_data(v,lam,initial,sequence,gamma0,bound,kappa)
    D,s,Qc=ordinary_centered(v,lam,blocks)
    if eta is None:eta=F(1,8*v*v)
    _,_,Qm,eta=ordinary_maximal(v,lam,blocks,(D,s,Qc),eta)
    return D,s,Qc,Qm,eta,blocks,Z,data,updates


def fixtures():
    from cyclic13_gram import orbit_partition,blocks_from_mask
    orbit,_=orbit_partition();base=blocks_from_mask(23768,orbit)
    path=[(((0,5),(1,4),(2,8)),True),(((0,5),(1,12),(2,3)),False),
          (((0,9),(1,5),(2,3)),True),(((0,3),(1,8),(2,7)),False),
          (((0,2),(1,5),(3,4)),True)]
    yield 4,20,164,23768,base,path[:3]
    triples={sum(1<<x for x in t)for t in combinations(range(13),3)}
    yield 7,20,238,23768,sorted(triples-set(base)),[(g,not r)for g,r in path]


def sharp_fixture():
    """Literal simple fourfold13 attaining norm14; no search is required.

    Six graph masks use the 21 lexicographically ordered pairs of range(7).
    Three A graphs have degrees (2,2,2,4,4,3,3), three B graphs have degrees
    (2,2,2,2,2,3,3). The checker verifies the decoded full design directly.
    """
    groups=((0,1),(2,3),(4,5));pairs=list(combinations(range(7),2))
    factors=(1482252,1681832,2001546,991329,418224,120368)
    H=((0,1,2),(0,1,3),(0,1,4),(0,2,3),(0,2,5),
       (1,2,4),(1,2,6),(0,3,5),(1,5,6),(2,4,6))
    U=set()
    def block(points):return sum(1<<x for x in points)
    for bits in product(range(2),repeat=3):
        if sum(bits)%2==0:U.add(block(groups[i][bits[i]]for i in range(3)))
    for i in range(3):
        for j in range(3):
            if i!=j:U.add(block((*groups[i],groups[j][0])))
    for i,j in combinations(range(3),2):
        for a,b in product(range(2),repeat=2):
            outside=(0,1)if (a+b)%2 else(2,)
            if a==b==1:outside+=(3,4)
            for x in outside:U.add(block((groups[i][a],groups[j][b],6+x)))
    for group in groups:
        for x in (5,6):U.add(block((*group,6+x)))
    for i in range(3):
        for which,mask in enumerate((factors[i],factors[3+i])):
            for bit,(a,b)in enumerate(pairs):
                if mask>>bit&1:U.add(block((groups[i][which],6+a,6+b)))
    for triple in H:U.add(block(6+x for x in triple))
    assert len(U)==104
    return sorted(U),groups,False,{'factor_masks':list(factors),
        'outside_only_triples':[list(t)for t in H],
        'integer_eigenvector':[7,-7,7,-7,7,-7,6,6,-6,-3,-3,0,0]}
