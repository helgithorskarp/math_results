"""Exact23-orbit Gram reduction; no changed published allocation guard."""
from math import comb
from fractions import Fraction as F
from matrices import domain,entry,table,require,digest,KAPPA,TRADE,LOWER_FLOOR,CAP_FLOOR
from exact import schur_psd,polynomial_psd


def key(A):return A&7,(A&248).bit_count(),(A>>8).bit_count()


def grams(q,kappa=KAPPA,t=TRADE):
    require(type(q) is int and 19<=q<=23,'new finite23-orbit q19..23')
    X=domain(q)[1:];N=len(X)+1;s=3*q+4;w=table(q)
    groups={}
    for A in X:groups.setdefault(key(A),[]).append(A)
    keys=sorted(groups);size=[len(groups[k]) for k in keys]
    require(len(keys)==23 and all(len(groups[k])==comb(5,k[1])*comb(q-5,k[2]) for k in keys),
            'complete independent outside orbit census')
    G=[[size[i]*sum(entry(groups[a][0],B,s,w,kappa,t) for B in groups[b])
        for b in keys] for i,a in enumerate(keys)]
    H=[[F(N*size[i]*int(i==j)-size[i]*size[j])-G[i][j] for j in range(23)] for i in range(23)]
    require(all(G[i][j]==G[j][i] and H[i][j]==H[j][i] for i in range(23) for j in range(23)),
            'weighted original Gram symmetry')
    return X,keys,size,G,H


def verify(q,C,U):
    X,keys,size,G,H=grams(q);N=len(X)+1;s=3*q+4
    groups=[[i for i,A in enumerate(X) if key(A)==k] for k in keys]
    for orig,small in ((C,G),(U,H)):
        require(all(sum(orig[i][j] for i in a for j in b)==small[h][r]
                    for h,a in enumerate(groups) for r,b in enumerate(groups)),
                'every independent full-pair original Gram entry')
    star=[F(bool(k[0]&1)) for k in keys]
    require(sum(size[i]*star[i] for i in range(23))==s,'Gram star norm')
    lower=[[G[i][j]-LOWER_FLOOR*(size[i]*int(i==j)-size[i]*star[i]*size[j]*star[j]/s)
            for j in range(23)] for i in range(23)]
    upper=[[H[i][j]-CAP_FLOOR*size[i]*int(i==j) for j in range(23)] for i in range(23)]
    require(schur_psd(lower)==22,'strict lower floor off the one-dimensional star kernel')
    require(schur_psd(upper)==23,'strict cap floor in the entire fixed space')
    poly=[polynomial_psd(A) for A in (G,H)]
    require([p[0] for p in poly]==[22,23],'separate exact characteristic-polynomial ranks')
    require(0<LOWER_FLOOR<=KAPPA/2 and 0<CAP_FLOOR<N-2*s,'outside-complement floors')
    # The standard difference basis spans the orthogonal complement of
    # orbit indicators; every trade coordinate is a singleton orbit.
    trade_masks={1,2,4,3,5}
    require(all(len(g)==1 for k,g in zip(keys,groups) if k[0] in trade_masks and k[1:]==(0,0)),
            'entire repair support in the fixed space')
    differences=sum(len(g)-1 for g in groups)
    require(differences==N-1-23,'complete outside-complement dimension')
    return {'q':q,'N':N,'orbit_count':23,'orbit_keys':[list(k) for k in keys],'orbit_sizes':size,
            'complement_dimension':differences,'whole_lower_rank':N-1,'whole_cap_rank':N-1,
            'lower_nonempty_floor':str(LOWER_FLOOR),'physical_projected_cap_floor':str(CAP_FLOOR),
            'complement_lower_floor':str(KAPPA/2),'complement_cap_floor':N-2*s,
            'all_full_pair_Gram_entries_match':True,
            'Gram_digest':digest([[[str(x) for x in row] for row in A] for A in (G,H)]),
            'characteristic_checks':[{'rank':p[0],'coefficient_digest':p[1],'denominator':p[2]} for p in poly],
            'trust_boundary':'ordinary complete orbit decomposition and published undeleted spectral floors; no independent peer review'}
