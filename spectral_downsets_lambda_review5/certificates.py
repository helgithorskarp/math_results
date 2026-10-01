"""Independent compact certificates for every literal matrix direction.

The ordinary proof in REVIEW.md justifies the complete decomposition:
constants plus layer-sum-zero pairs/triples in the star-killing factor K.
Positive pair eigenvalues and a strict triple Schur margin prove lower PSD
and rank; a three-layer operator-norm comparison proves upper PSD and rank.
This is not dense elimination or numerical spectrum fitting.
"""
from fractions import Fraction as F
from exact import need, matvec, psd_rank


def certify(V,Q,Qm,E,v,lam,w,dense):
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
    if not dense:
        return result
    need(lam==v-3 and v>=13,'wrong dense complement domain')
    # Check every literal upper-block identity; no author constructor is used.
    points=[V[i].bit_length()-1 for i in layers[1]]
    pairs=[V[i] for i in layers[2]];blocks=[V[i] for i in layers[3]]
    U=set(blocks)
    P=[[int(A >> x & 1) for A in pairs] for x in points]
    B=[[int(A >> x & 1) for A in blocks] for x in points]
    R=[[int(A&T==A) for T in blocks] for A in pairs]
    Cp=[[int(not(A >> x & 1) and (A|(1<<x)) not in U) for A in pairs] for x in points]
    rp=F(v-1,2)
    need(all(sum(R[i])==lam for i in range(m)) and all(sum(R[i][j] for i in range(m))==3 for j in range(b)),
         'pair/block norm normalization')
    need(all(sum(Cp[i][z]*Cp[j][z] for z in range(m))==rp*(i==j) for i in range(v) for j in range(v)),
         'missing STS completion Gram identity')
    for x,ii in enumerate(layers[1]):
        for y,jj in enumerate(layers[1]):
            need(Q[ii][jj]==(s+F(lam,3))*(x==y)-F(lam,3),'zero-defect point block')
        for z,jj in enumerate(layers[2]):
            need(Q[ii][jj]==(d-w['w'])*P[x][z]+d*Cp[x][z]+w['w']-d,'complement point/pair block')
        for z,jj in enumerate(layers[3]):
            cpR=sum(Cp[x][i]*R[i][z] for i in range(m))
            need(Q[ii][jj]==(w['h']-3*t)*(1-B[x][z])+t*cpR,'complement point/block block')
    for z,ii in enumerate(layers[2]):
        for zz,jj in enumerate(layers[3]):
            need(Q[ii][jj]==d*(R[z][zz]-(pairs[z]&blocks[zz]).bit_count()+1),'pair/block upper identity')
    need(abs(d-w['w'])<1 and abs(w['h']-3*t)<2 and 0<c<F(4,3) and 0<d<2 and 0<t<2,
         'dense weight norm bounds')
    need(F(v*v,9)>v and F(3,2)**2>2 and F(5,2)**2>6 and lam<v and lam>8
         and F(2*v-5,2)**2>(v-2)*(v-3),'dense radical-square comparisons')
    bound=F(v*v+8*v-18);delta=N-bound
    comparison=[[s+F(lam,3),F(5*v,6),F(4*v)],
                [F(5*v,6),s+F(4,3),F(lam*v,2)],
                [F(4*v),F(lam*v,2),s+6*lam-2]]
    gap=[[bound*(i==j)-comparison[i][j] for j in range(3)] for i in range(3)]
    need(all(gap[i][i]>sum(abs(gap[i][j]) for j in range(3) if j!=i) for i in range(3))
         and psd_rank(gap)==3,'dense operator-norm comparison not strict')
    need(bound>F(lam*(v+7),6)+1 and delta>F(v*v,4),'dense full constant eigenvalue or buffer')
    trade_norm=max(sum(abs(x) for x in row) for row in E)
    need(trade_norm==4*m*k and eta*trade_norm<delta/2,'repair upper-norm loss too large')
    const_ranks={}
    for label,A,buffer in [('centered_buffered_upper',Q,delta),('repaired_buffered_upper',Qm,delta/2)]:
        # The four-dimensional literal restriction also audits the empty loop
        # and metric of the layer constants; raw all-one layer indicators form
        # a congruence basis, so no unjustified Euclidean normalization occurs.
        G=[]
        for i,I in enumerate(layers):
            row=[]
            for j,J in enumerate(layers):
                diagonal=len(I)*(i==j)
                row.append(N*diagonal-sum(A[x][y] for x in I for y in J)
                           -buffer*(diagonal-F(len(I)*len(J),N)))
            G.append(row)
        need(psd_rank(G)==3 and not any(matvec(G,[1]*4)),'full constant buffered-upper restriction')
        const_ranks[label]=3
    result['upper']={'certificate':'literal full block identities, strict3x3 norm comparison and4x4 constant congruences',
                     'centered_cap':str(bound),'delta':str(delta),'repaired_upper_buffer':str(delta/2),
                     'upper_ranks':{'centered_buffered_upper':N-1,'repaired_buffered_upper':N-1},
                     'row_norm_margins':[str(gap[i][i]-sum(abs(gap[i][j]) for j in range(3) if j!=i)) for i in range(3)],
                     'literal_constant_restriction_ranks':const_ranks,'trade_upper_loss':str(eta*trade_norm)}
    return result
