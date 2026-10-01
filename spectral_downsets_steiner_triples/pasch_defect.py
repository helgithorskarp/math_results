"""Exact low-rank completion-defect stability under legal Pasch switches.

The operation is classical. The point norm certificate and capped closure
are proved in PASCH_DEFECT_STABILITY.md. Simple existing designs only;
no symmetry assumption on a switched design, no design census or priority
claim. six-downset-2, researcher. Standard library; assertions enabled.
"""
from fractions import Fraction as F
from itertools import combinations,product
from math import comb
from uniform_lambda_small import design_data,parameters
from uniform_lambda_small import centered_certificate as ordinary_centered
from uniform_lambda_small import maximal_certificate as ordinary_maximal
from defect_gram import scalar_data


def matchings(points):
    """All perfect matchings, each once, by pairing the least unused point."""
    if not points:
        yield ();return
    a=points[0]
    for b in points[1:]:
        remaining=tuple(x for x in points if x not in (a,b))
        for rest in matchings(remaining):yield ((a,b),)+rest


def sides(groups):
    assert len(groups)==3 and all(len(g)==2 for g in groups)
    assert len({x for g in groups for x in g})==6
    assert all(type(x)is int and x>=0 for g in groups for x in g)
    out=[set(),set()]
    for choices in product(range(2),repeat=3):
        out[sum(choices)%2].add(sum(1<<groups[j][choices[j]]for j in range(3)))
    assert len(out[0])==len(out[1])==4 and out[0].isdisjoint(out[1])
    return frozenset(out[0]),frozenset(out[1])


def all_trades(v):
    assert type(v)is int and v>=6
    out=[]
    for support in combinations(range(v),6):
        local=list(matchings(support));assert len(local)==15
        for groups in local:
            even,odd=sides(groups);out.append((groups,even,odd))
    assert len(out)==15*comb(v,6)
    assert len({tuple(sorted((tuple(sorted(a)),tuple(sorted(b)))))for _,a,b in out})==len(out)
    return out


def point_defect(v,lam,blocks):
    parameters(v,lam);assert v>=7
    pairs,completing,codes,_=design_data(v,lam,blocks);u=lam*(lam-1)//2
    Z=[[0 if x==y else codes[(1<<x)|(1<<y)]-u for y in range(v)]for x in range(v)]
    assert all(sum(row)==0 for row in Z)
    return pairs,completing,Z


def perturbation_certificate(v,kappa):
    assert type(v)is int and v>=7
    kappa=F(kappa);L=(v-6)//2
    assert kappa>=8 and kappa*(kappa-8)>=48*L
    return {'v':v,'L':L,'kappa':kappa,'outside_squared_norm_bound':24*L,
            'cross_squared_norm_bound':48*L,'inside_norm_bound':8,
            'comparison_determinant_margin':kappa*(kappa-8)-48*L,
            'young_alpha_margin':kappa-8-F(48*L)/kappa}


def switch_update(v,lam,blocks,groups,reverse=False):
    """Full literal C update and low-rank Z identity for one legal switch."""
    assert type(reverse)is bool
    even,odd=sides(groups)
    assert all(x<v for g in groups for x in g)
    removed,added=(odd,even)if reverse else(even,odd)
    U=set(blocks);assert removed<=U and added.isdisjoint(U),'Illegal Pasch switch'
    new=sorted(U-removed|added)
    pairs,completing,Z=point_defect(v,lam,blocks)
    next_pairs,next_comp,nextZ=point_defect(v,lam,new);assert pairs==next_pairs
    A=[[int(x==g[0])-int(x==g[1])for g in groups]for x in range(v)]
    W=[[0]*3 for _ in pairs];pi={p:i for i,p in enumerate(pairs)}
    for k in range(3):
        i,j=[q for q in range(3)if q!=k]
        for a,b in product(range(2),repeat=2):
            p=(1<<groups[i][a])|(1<<groups[j][b])
            W[pi[p]][k]=(-1 if (a+b)%2==0 else 1)*(-1 if reverse else 1)
    C=[[int(1<<x in completing[p])for p in pairs]for x in range(v)]
    assert all(sum(A[x][i]*A[x][j]for x in range(v))==2*int(i==j)
               for i in range(3)for j in range(3))
    assert all(sum(W[x][i]*W[x][j]for x in range(len(pairs)))==4*int(i==j)
               for i in range(3)for j in range(3))
    assert all(sum(row[k]for row in W)==0 for k in range(3))
    assert all(sum(int(p>>x&1)*W[y][k]for y,p in enumerate(pairs))==0
               for x in range(v)for k in range(3))
    for x in range(v):
        for j,p in enumerate(pairs):
            assert int(1<<x in next_comp[p])-C[x][j]==sum(A[x][k]*W[j][k]for k in range(3))
    Y=[[sum(C[x][j]*W[j][k]for j in range(len(pairs)))+2*A[x][k]
        for k in range(3)]for x in range(v)]
    inside={x for g in groups for x in g};outside=[x for x in range(v)if x not in inside]
    T=[Y[a][:]for a,b in groups]
    assert all(Y[b]==[-z for z in T[k]]for k,(a,b)in enumerate(groups))
    assert all(T[k][k]==0 for k in range(3))
    assert all(abs(z)<=1 for row in T for z in row)
    assert all(abs(z)<=2 for x in outside for z in Y[x])
    assert all(sum(Y[x][k]for x in outside)==0 for k in range(3))
    L=(v-6)//2
    assert all(sum(abs(Y[x][k])for x in outside)<=4*L for k in range(3))
    Delta=[[sum(Y[x][k]*A[y][k]+A[x][k]*Y[y][k]for k in range(3))
            for y in range(v)]for x in range(v)]
    assert all(Delta[x][y]==nextZ[x][y]-Z[x][y]for x in range(v)for y in range(v))
    assert all(sum(row)==0 for row in Delta)
    assert max(sum(map(abs,row))for row in Delta)<=max(12,8+4*L)
    return new,nextZ,Delta,{'groups':[list(g)for g in groups],'reverse':reverse,
        'T':T,'outside_rows':{str(x):Y[x]for x in outside},
        'Delta_absolute_row':max(sum(map(abs,row))for row in Delta),
        'new_absolute_row':max(sum(map(abs,row))for row in nextZ),
        'new_point_row_signature_count':len({tuple(sorted(row))for row in nextZ})}


def chain_data(v,lam,initial,sequence,gamma0=28,kappa=F(50,3)):
    """Verify an initial row certificate and every legal move; use the theorem.

    The final gamma is a mean-point PSD bound, not necessarily an absolute
    row bound. This constructor does not substitute those two hypotheses.
    """
    certificate=perturbation_certificate(v,kappa);gamma0=F(gamma0);assert gamma0>=0
    _,_,Z=point_defect(v,lam,initial)
    assert max(sum(map(abs,row))for row in Z)<=gamma0
    current=sorted(initial);updates=[]
    for groups,reverse in sequence:
        current,Z,Delta,info=switch_update(v,lam,current,groups,reverse)
        updates.append((Delta,info))
    gamma=gamma0+len(sequence)*certificate['kappa'];data=scalar_data(v,lam,gamma)
    assert data['whole_interval_sufficient'],'The sufficient scalar cap did not pass'
    return current,Z,data,updates


def certificates(v,lam,initial,sequence,gamma0=28,kappa=F(50,3),eta=None):
    blocks,Z,data,updates=chain_data(v,lam,initial,sequence,gamma0,kappa)
    D,s,Qc=ordinary_centered(v,lam,blocks)
    if eta is None:eta=F(1,8*v*v)
    _,_,Qm,eta=ordinary_maximal(v,lam,blocks,(D,s,Qc),eta)
    return D,s,Qc,Qm,eta,blocks,Z,data,updates


def fixtures():
    from cyclic13_gram import orbit_partition,blocks_from_mask
    orbit,_=orbit_partition()
    specs=[(4,23768,[(((0,5),(1,11),(2,6)),True)]),
           (5,40920,[(((0,5),(1,11),(3,7)),True)]),
           (6,106488,[(((0,2),(1,7),(4,8)),False)]),
           (6,106488,[(((0,2),(1,7),(4,8)),False),(((0,2),(1,3),(4,8)),True)])]
    for lam,mask,moves in specs:
        yield lam,mask,blocks_from_mask(mask,orbit),moves
