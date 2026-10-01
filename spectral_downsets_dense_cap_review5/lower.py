"""Independent compact certificates for every literal matrix direction.

The ordinary proof in REVIEW.md justifies the complete decomposition:
constants plus layer-sum-zero pairs/triples in the star-killing factor K.
Positive pair eigenvalues and a strict triple Schur margin prove lower PSD
and rank; a three-layer operator-norm comparison proves upper PSD and rank.
This is not dense elimination or numerical spectrum fitting.
"""
from fractions import Fraction as F
from exact import need, matvec, psd_rank


def certify(V,Q,Qm,E,v,lam,w):
    N=len(V);m=v*(v-1)//2;b=lam*v*(v-1)//6;r=lam*(v-1)//2;s=v+r
    k=(v-2)*(v-3)//2;eta=F(1,8*v*v)
    layers=[[i for i,A in enumerate(V) if A.bit_count()==j] for j in range(4)]
    need(list(map(len,layers))==[1,v,m,b], 'wrong complete layer dimensions')
    # Invariance of the full constant-layer subspace is checked literally.
    for A in (Q,Qm):
        for rows in layers:
            for cols in layers:
                totals=[sum(A[i][j] for j in cols) for i in rows]
                need(len(set(totals))==1,'constant-layer subspace not invariant')
    # Factor K is determined by its pair/triple principal block, already
    # checked entrywise in audit.matrices, and annihilation of all stars.
    C=[[sum(Q[i][j]-1 for i in layers[x] for j in layers[y]) for y in (2,3)] for x in (2,3)]
    need(C==[[4*b,-2*b],[-2*b,b]] and psd_rank(C)==1 and matvec(C,[1,2])==[0,0],
         'centered constant factor block')
    repaired=[[sum(Qm[i][j]-1 for i in layers[x] for j in layers[y]) for y in (0,2,3)] for x in (0,2,3)]
    expected=[[eta*m*k,eta*m*k,0],[eta*m*k,4*b+eta*m*k,-2*b],[0,-2*b,b]]
    need(repaired==expected and psd_rank(repaired)==2 and not any(matvec(repaired,[1,-1,-2])),
         'repaired constant factor block')
    c,d,t=w['c'],w['d'],w['t']
    alpha1=s-c*(v-3);alpha2=s+c
    margins={}
    for label,a1,a2 in [('centered',alpha1,alpha2),('repaired',alpha1-eta*(v-3),alpha2+eta)]:
        beta=t-d*d/a2
        red=t*F(v-6,v-2)+d*d*(v-4)**2/((v-2)*a1)
        mu=s-t-(r-lam)*red
        need(a1>0 and a2>0 and beta>0 and red>0 and mu>0,'nonpositive full-mode Schur certificate')
        margins[label]={'alpha1':str(a1),'alpha2':str(a2),'beta':str(beta),'red':str(red),'mu':str(mu)}
    result={'certificate':'complete constant/mean-zero factor and incidence Schur bound',
            'lower_ranks':{'centered_lower':N-v-1,'repaired_lower':N-v},
            'constant_factor_ranks':[1,2],'Schur_margins':margins,
            'full_constant_layer_invariance_checked':True}
    return result
