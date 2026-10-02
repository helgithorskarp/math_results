# Two triangles and arbitrarily many distinct-mark pendants: capped H

Actual author **six-downset-1**, role **researcher**, 2026-10-02.
The uniform signs are exact rational polynomial certificates. The
surrounding real linear-algebra, exhaustive-space, lift and rank proofs
below are ordinary mathematics and **unformalized**. Independent review
of this result is not claimed; author normal/optimized agreement supplies
reproducibility rather than independent review.

## Statement and relation to prior work

For every integer **n>=4**, n-set X, integer **2<=l<=n-2**, mutually
distinct marks x_1,x_2,z_1,...,z_l in X, and mutually distinct private
points u_1,v_1,u_2,v_2,b_1,...,b_l outside X, let

    D=2^X union_i=1,2 2^{x_i,u_i,v_i} union_j=1,...,l 2^{z_j,b_j},
    q=2^(n-1), N=|D|=2q+12+2l, s=q+3, h=N-s.

There is an explicit rational symmetric matrix M on **all actual sets
of D, including empty**, such that

    M*1=1, M_AB=0 whenever A intersects B nontrivially,
    L=h*M+s*I >=0,
    h*(I-M) >= (3/4)*(I-J_N/N).

Its lower rank **N-2 is greatest among all real ordinary H matrices
on D**, without a cap, rationality, averaging or entry-sign assumption
on competitors. Rank(I-M)=N-1. The lower kernel is exactly the span of
the two centered maximum x_i-star indicators. In particular the least
eigenvalue of M is exactly -s/h and its weighted Hoffman bound is s.
The rational formulas and perturbation below specify M for every
parameter; finite allocation guards in the executable do not limit
the mathematical theorem.

Each triangle adds six sets u_i,x_iu_i,v_i,x_iv_i,u_iv_i,x_iu_iv_i;
each pendant adds b_j,z_jb_j. These additions give the stated N and a
downset. The two x_i-stars each have q+3 members, z_j-stars q+1, other
old stars q, triangle-private stars4 and pendant-private stars2.
Since q>=8, exactly the two x_i-stars are maximum. Relabeling preserves
the construction and covers every labeling in the statement.

Ordinary H and greatest lower rank for these strict private attachments
are prior [LEMMA9361](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/one-point-attachments/PROOF.md),
source `ca8d2e363536435ad034f08cf3845a6ffd276326`, independently confirmed
in [REVIEW9412](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/attachment-audit/REVIEW.md),
source `07e9cde0c4181ed67c565ef24ed366a34566b739`. Those conclusions
are credited prior work. The new conclusion is a **uniform cap at
greatest rank when both attachment counts are at least two, with the
triangle count fixed at two and the pendant count unbounded**.

The one-triangle/one-pendant cap is prior [LEMMA9408](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/mixed-facet-cap/PROOF.md),
source `f8255e1d617237421c32b3d1e13dd865bffd50c4`, independently checked
and refined in [REVIEW9444](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/mixed-cap-audit/PROOF.md),
source `0f395497f1c7a86564802e8c220865eda4b8d17c`. The
[all-triangle cap9540](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/triangle-profile-cap/PROOF.md),
source `8a32f730483ce09147db62d7eedbf0c097745b53`, supplies credited
exact tools and the triangle-standard structure. The
[one-triangle/unbounded-pendant cap9641](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/single-triangle-pendants-cap/PROOF.md),
source `674308fc8b647fc7ac68ae95ea0cc7a941e77c60`, supplies the fixed8
grouping/inverse mechanism. Its uniform cap does not imply this theorem.
Neither9540 nor9641 is asserted independently reviewed here.

The primary target is [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version history](https://arxiv.org/abs/2609.28404) was checked live
on2026-10-02 and lists only v1, September23. The authors prove the
classical and projection-packing statements and propose H and I as
unresolved spectral strengthenings. This result concerns the stated
attachment family, not general H or I, arbitrary private-attachment cap
closure, arbitrary triangle count, the l=1 case, an optimal gap or a
historical priority claim.

## The whole original lift and old cube

For a Gram core C indexed by all nonempty actual members, with
diagonal s-1 and C_AB=-1 for distinct intersecting sets, put

    E0=[-1';I_(N-1)], Q=E0*C*E0', L=J_N+Q, M=(L-s*I)/h.

The empty vector is the negative sum of **all** nonempty vectors.
Consequently Q1=0, L1=N1, all mandatory entries of M vanish, and
rank(L)=1+rank(C) when C>=0. The empty loop is allowed and determined
by this lift. If the complete physical frame
F=sum_{A in D}|a_A><a_A| satisfies F<=(N-1)I on its full span, the
RR'/R'R identity gives Q<=(N-1)P, P=I-J_N/N. Thus

    h*(I-M)=N*P-Q >=P.

These are whole-space statements. A centered quotient check without
the actual empty contribution would not establish them.

On the old nonempty cube take

    C0=(q+3)I+(q-3)Pc-J,

where Pc pairs proper nonempty complements and is zero on the full
set. Write g_A for old coefficient vectors, G=sum g_A, f=g_X and
H_i=-sum_{A contains i}g_A. Direct cube counting gives

    G^2=f^2=q+2, G.f=4-q,
    H_i.H_j=3q*[i=j], G.H_i=f.H_i=-3,
    H_i.g_A=3(1-2[i in A]).

The old space is an orthogonal direct sum of a q-2 dimensional
pair-constant zero-sum space of eigenvalue2q, a q-1 dimensional
pair-antisymmetric space of eigenvalue6, and the plane
gp=(G-f)/2,h0=-(G+f)/2 of Gram diag(q-1,3). This exhausts2q-1
dimensions and proves C0 PD. Put A_i=H_i-h0; then
A_i.A_j=3(q*[i=j]-1). The l+2 marked A_i are independent since
q>l+2. Untouched dimensions are q-2 and q-l-3, with complete-frame
eigenvalues2q and6; every new and empty vector is orthogonal to them.

The old-frame bilinear on gp,h0 is
[[q^2-1,3(q-1)],[3(q-1),9]]. On the marked A_i span it is6 times
its Gram. Applying C0 to the displayed coefficient vectors verifies
these identities for every old cube, without an untested-order premise.

## Projections and a strictly balanced private residual

For each triangle take an independent plane T_i1,T_i2,T_i3 with
Gram s(I3-J3/3) and sum zero; put h_i=H_xi/3 and
V_ia=h_i+T_ia. For each pendant take an independent Z_j of norm2s/3
and put V_j=H_zj/3+Z_j. All new planes/lines are mutually orthogonal
and orthogonal to the old space. These marked vectors have norm
w=q+2 and all mandatory marked and old/marked products.

Set hbar=(h_1+h_2)/2, vbar=sum_j V_j/l,

    m=l+6, ell=l+7, t=l+1, rho=(q-1)/(q+1),
    E=hbar-rho*vbar, D_i=h_i-hbar, J_j=V_j-vbar,
    K=G+6*hbar+l*vbar.

These contrast spaces and the T planes are mutually orthogonal, and

    K^2=ell*q-10, K.h_i=q-1, K.V_j=q+1,
    K.E=K.D_i=K.J_j=K.T_ia=0,
    E^2=q/6+rho^2*w/l, D_i^2=q/6, J_j^2=w*(l-1)/l.

Use the rational scalars

    d=3(q-ell-1)/(ell*q), g=(q-ell+1)/(ell*w),
    Fp=-g/rho, A=(-d-l*Fp/2)/2, a=-d/3,
    ast=2*a-A, c=(a-d)*q/s,
    p_i1=-K/ell+A*E+ast*D_i+c*T_i2,
    p_i2=-K/ell+A*E+ast*D_i+c*T_i1,
    p_i3=-K/ell+d*E+d*D_i+(c/t)*T_(other triangle),3,
    p_j=-K/ell+Fp*E+g*J_j+(c/t)*(T_13+T_23).

Their sum is -mK/ell: 2A+d+lFp/2=0, sum D_i=sum J_j=0,
and the transfer terms cancel c(T_i1+T_i2)=-cT_i3.
For a mandatory triangle leaf pairing the contrast product is
(a*q-c*s)/3=dq/3; for a full private pairing it is dq/3.
Thus -(q-1)/ell+dq/3=-1. For a pendant,
-(q+1)/ell+gw=-1; the Fp and J_j parts contribute exactly gw.
This verifies every mandatory private/marked product.

With e2=E^2 and common=(ell*q-10)/ell^2, define

    etaL=w-common-A^2*e2-ast^2*q/6-2s*c^2/3,
    etaF=w-common-d^2*e2-d^2*q/6-2s*c^2/(3t^2),
    etaP=w-common-Fp^2*e2-g^2*w*(l-1)/l-4s*c^2/(3t^2),
    pair=-1-common-A*d*e2-ast*d*q/6,
    mu=(2pair+etaF)/3,
    alpha=2(2etaL-pair-etaF), beta=etaF-mu,
    Cmean=1/[2(l/(6mu)+6/(l etaP)+m/q)],
    a_mean=(l Cmean-3mu)/3,
    b_mean=(6 Cmean-etaP)/(l-1),
    nuT=mu-a_mean=2mu-l Cmean/3,
    nuL=etaP-b_mean=(l etaP-6 Cmean)/(l-1).

The exact certificates below prove etaL,etaF,etaP,mu,alpha,beta>0
and, more quantitatively, **mu>q/6 and etaP>2q/3**. The harmonic
choice gives

    0<Cmean<min(3mu/l, l etaP/12, q/(2m)),
    nuT>mu>0, nuL>l etaP/[2(l-1)]>0.

The needed lower bound is

    Cmean>Cfloor=lq/[2(2l^2+6l+9)] >=2q/(29l).

The first inequality follows by bounding both terms of1/Cmean using
the proved residual floors. The second is equivalent to
29l^2-4(2l^2+6l+9)=3(7l+6)(l-2)>=0. Therefore

    nuT<nuT_hat=2mu-2q/87,
    nuL<nuL_hat=l etaP/(l-1), Cmean<C_hat=q/(2m).

The first upper bound is positive since mu>q/6 implies
nuT_hat>9q/29. These inequalities avoid expanding the harmonic
denominator in the cap certificates. Using nuT_hat=2mu alone is
insufficient for this uniform triangle-standard certificate.

Construct means M_i with diagonal mu and off-diagonal a_mean,
pendant means N_j with diagonal etaP and off-diagonal b_mean,
and cross M_i.N_j=-Cmean. Independently take WA_i,WF_i of norms
alpha,beta, all internal spaces mutually orthogonal and orthogonal
to the means. Define

    W_i1=M_i+(WA_i-WF_i)/2,
    W_i2=M_i+(-WA_i-WF_i)/2, W_i3=M_i+WF_i.

The actual private-row Gram W of these six vectors and the l N_j
is PSD, with kernel exactly1_m. Its orthogonal types have positive
eigenvalues alpha/2 and3beta/2 for each triangle, 3nuT for the
triangle-mean contrast, nuL with multiplicity l-1, and m Cmean
for the one nonzero fixed mean. Row sums are zero by
3mu+3a_mean-l Cmean=0 and etaP+(l-1)b_mean-6 Cmean=0.
These eigenvalues and the zero fixed mean exhaust m dimensions.

For actual private sets use U_ia=p_ia+W_ia and U_j=p_j+N_j.
Their norms are w. Within a triangle W_i1.W_i3=W_i2.W_i3=pair,
so all mandatory private/private products are -1. Different private
groups are disjoint, as are old/private sets. The listed pairings,
old/marked products and the diagonals exhaust all intersection types.
The nonempty vectors sum to K/ell, so the **actual empty seed vector
is -K/ell**, of norm(ell*q-10)/ell^2.

## The exhaustive cap decomposition

The changed old span has l+4 dimensions, marked residuals l+4,
and private residuals l+5, for a total **3l+13**. With
TA_i=T_i1-T_i2 and TS_i=T_i1+T_i2-2T_i3, leaf exchange and class
permutation give two anti2 blocks, one fixed8, one triangle-standard4,
and l-1 pendant-standard3 blocks:

    2*2+8+4+3(l-1)=3l+13.

They are mutually orthogonal in both Gram and complete frame. For
zero-sum pendant coefficient vectors all products depend only on
their dot product; the standard matrix tensors the positive metric
on that full coefficient space. This proves all l-1 copies at once,
including l=2, rather than assuming a difference basis is orthogonal.
Together with both untouched old spaces the decomposition exhausts
the entire seed span.

On any physical basis with Gram Gamma and complete-frame bilinear F,
the cap is (N-1)Gamma-F. For anti2, Gamma=diag(2s,alpha), and
congruence gives

    [[(N-1)/(2s)-(1+c^2)/2, c/2],
     [c/2, (N-1)/alpha-1/2]].

For pendant-standard3, Gamma=diag(6q,4s/3,2nuL). Subtracting the
old frame and marked update gives the positive diagonal
diag(6q(N-7),4s(N-1)/3,2nuL(N-1)), with remaining updates
2[(q,2s/3,0)]+2[(gq,2sg/3,nuL)]. Its equivalent Schur2 is

    B=q/[6(N-7)]+s/[3(N-1)],
    [[1/2-B,-gB],[-gB,1/2-g^2 B-nuL/[2(N-1)]]].

Replacing nuL by nuL_hat subtracts a positive diagonal matrix, so
the certified substituted test suffices for the actual one.

For triangle-standard4, Gamma=diag(6q,12s,2nuT,2beta). The two
marked groups give exactly diagonal frame additions6q^2 and12s^2.
The remaining cap is the positive diagonal

    D0=diag(6q(N-q-7),12s(N-q-4),2nuT(N-1),2beta(N-1))

minus4[uL]+2[uF], where the actual inner-product images are

    uL=(ast*q,c*s,nuT,-beta/2),
    uF=(d*q,2c*s/t,nuT,beta).

Its Schur2 is diag(1/4,1/2)-U'D0^(-1)U. Canceling the Gram norms
before multiplication gives, with tq=N-q-7,ts=N-q-4,H=N-1,

    LL=ast^2*q/(6tq)+c^2*s/(12ts)+nuT/(2H)+beta/(8H),
    FF=d^2*q/(6tq)+c^2*s/(3t^2 ts)+nuT/(2H)+beta/(2H),
    LF=ast*d*q/(6tq)+c^2*s/(6t ts)+nuT/(2H)-beta/(4H),
    S2=[[1/4-LL,-LF],[-LF,1/2-FF]].

Using nuT_hat subtracts (nuT_hat-nuT)J2/(2H), a PSD matrix.
The substituted2-test is uniformly PD by the exact certificate.
All16 diagonal/update positions and all4 canceled Schur positions
are separately checked against the original sector formulas.

## Fixed8: complete grouping and bounded inverse

Use basis(gp,h0,sum_i A_xi,sum_j A_zj,sum_i TS_i,sum_j Z_j,
sum_i WF_i,sum_i M_i). Its Gram has diagonals

    q-1,3,6(q-2),3l(q-l),12s,2ls/3,2beta,2l Cmean/3,

and only off-diagonal entries Gamma23=Gamma32=-6l. The old A-plane
determinant is18lq(q-l-2)>0. Let F0 be the old-frame bilinear.
With [a]=|a><a| in physical operator notation, the complete frame is

    Ffixed=F0+[TS]/12+6[hbar]+l[vbar]+[K]/ell
                      +(6m/l)[Zp]+(4/3)[Dint],
    Zp=-(l Fp/6)E+(cl/(18t))TS+Msum/2,
    Dint=(A-d)E+c(t+2)TS/(12t)-3WFsum/4.

For a proof, the fixed leaf/full private vectors have weighted mean
-K/ell+Zp and difference Dint. Their counts4:2 give6 times the
mean square plus4/3 times the difference square. The fixed pendant
private vector is -K/ell-6Zp/l. Group these means with multiplicities
6:l and include **actual empty [-K/ell]**; the result is[K]/ell
plus(6m/l)[Zp]. The marked triangle vectors give6[hbar]+[TS]/12,
and the marked pendants l[vbar]. This proves every weight/cancellation.

First subtract F0+[TS]/12. The TS gap is H-s>0. The old gp/h0
cap block has first pivot(q-1)(N-q-2)>0 and determinant3(q-1)J>0,
where J=(N-q-2)(N-4)-3(q-1). The old A-plane gap is N-7>0,
and the pendant Z gap is H>0. On old-plus-Z5 the inverse pairing is

    I0(a,b)=[(q-1)(N-4)a0b0+3(q-1)(a0b1+a1b0)
                           +3(N-q-2)a1b1]/J
          +3[2(q-2)a2b2-2l(a2b3+a3b2)+l(q-l)a3b3]/(N-7)
          +(2ls/3)a4b4/H.

Take columns hbar=(0,1/3,1/6,0,0),
vbar=(0,1/3,0,1/(3l),1/l),K=(1,(l+3)/3,1,1/3,1),
E=hbar-rho*vbar and

    S3=diag(1/6,1/l,ell)-I0(columns,columns), b=I0(columns,E).

Schur complements say S3>0 iff subtracting6[hbar]+l[vbar]+[K]/ell
leaves a PD base A5. The exact inverse quadratic is
tau=I0(E,E)+b'S3^(-1)b. We prove **tau<Tb=m/(6l)**.
Form [[S3,b],[b',Tb-I0(E,E)]], add(1,-rho,0) of the first3
coordinates to the last, then change first3 to
(hbar-vbar,6hbar+l*vbar,K-6hbar-l*vbar). The change determinant is m.
The transformed first3 block is

    [[aa,zz,0],[zz,bb,cc],[0,cc,dd]],
    D=N-7,H=N-1,A0=N-q-2,
    aa=[m-q(l+2)/D-4s/H]/(6l), zz=2(2l+5)/(D H),
    bb=m-m^2 A0/(3J)-[(l+18)q-m^2]/(3D)-2ls/(3H),
    cc=-m[1-(2l+11)/J],
    dd=2m+1-[(q-1)(N-10)+3A0]/J.

The last cross is(1/6+rho/l,1-rho,rho-1), and last diagonal
Tb+1/6+rho^2/l. All nine first-block and four augmented identities
are checked symbolically. Four uniform positive leading minors give
S3>0 and tau<Tb by congruence and the Schur complement.

Only the final Zp,Dint updates remain. Put

    aZ=-l Fp/6,bZ=cl/(18t),dE=A-d,bD=c(t+2)/(12t),
    T=12s/(H-s),
    ZZ=aZ^2*tau+bZ^2*T+l Cmean/(6H),
    DD=dE^2*tau+bD^2*T+9beta/(8H),
    ZD=aZ*dE*tau+bZ*bD*T,
    Sfinal=diag(l/(6m),3/4)-[[ZZ,ZD],[ZD,DD]].

Orthogonality of TS,WFsum,Msum and A5 proves these inverse pairings.
Replace tau by Tb and Cmean by C_hat. Each replacement subtracts
a PSD matrix from Sfinal: respectively(Tb-tau)(aZ,dE)(aZ,dE)'
and l(C_hat-Cmean)diag(1,0)/(6H). The substituted2-test is uniformly
PD. It therefore proves the entire fixed8 cap, including empty.

## Exact uniform signs and parameter coverage

Every sign uses Q[u,v], l=2+u,q=4l+v,u,v>=0. Each denominator and
clearing/removal factor has nonnegative coefficients and positive
constant. Positive row multipliers preserve leading determinant signs.
Exact Bareiss divisions compute the determinant polynomials, and an
independent Fraction Gaussian determinant agrees on every point of
the Cartesian grid determined by separate degree bounds.

| Quantity/test | Positive coefficient counts | Full identity-grid points |
|---|---:|---:|
| etaL,etaF,etaP,mu,alpha,beta numerators |99,63,56,35,81,63|Direct exact formulas|
| mu-q/6,etaP-2q/3 numerators |35,56|Direct exact formulas|
| anti2 leading minors |12,162|15,228|
| substituted pendant-standard Schur2 |14,132|20,187|
| substituted triangle-standard Schur2 |156,506|234,759|
| fixed base/inverse augmented4 |14,63,110,150|20,99,180,252|
| substituted fixed final Schur2 |90,410|126,600|

Thus488 norm/floor coefficients and1819 minor coefficients are
positive, and2720 full-grid points prove the determinant identities.
Positive constant and nonnegative coefficients prove strict signs on
the entire quadrant; Sylvester's criterion gives the stated PD tests.
The engine is also checked against separate direct Fraction convolution
and exact multiplication-back controls. The506-term determinant stays
within the unchanged512-term guard; no resource threshold was raised.

Every actual parameter lies in this quadrant. Since n>=l+2,
q>=2^(l+1)>=4l for all integers l>=2. The second inequality is
equality at l2 and follows inductively by doubling, since8l>=4(l+1).
There are no actual exceptions. Also q>l+2 and H>max(2q,6), so
all old Gram factors and untouched cap gaps are strictly positive.

The full exhaustive decomposition proves the **whole seed gap>=1**.
Its old/marked base rank is2q+3+l and private residual rank l+5,
so core rank is2q+8+2l=N-4, lower rank N-3 and upper rank N-1.
No quotient, finite pilot, heuristic eigenvalue or solver output is
being used to infer these unbounded conclusions.

## Explicit repair and the universally greatest rank

Delete the last pendant row of W to obtain a PD principal matrix A,
and let u0 indicate the first three triangle private rows. Its inverse
quadratic is

    kappa=u0'A^(-1)u0=1/(2nuT)+9(l-1)/(l nuL)+3/(2l Cmean)>0.

For a proof extend u0 to y=u0-3e_last, which sums to zero. Its
triangle-standard, pendant-standard and fixed-mean squared lengths
are3/2,9(l-1)/l and3m/(2l). Divide by the respective W eigenvalues
3nuT,nuL,m Cmean. Internal components vanish. A kernel shift
identifies this pseudoinverse quadratic with the deleted inverse
quadratic. Independent exact Gaussian deleted solves verify it in
each complete literal fixture.

Choose delta=1/[12N(1+kappa)] and add it to the three symmetric
core pairs between u_1,v_1,u_1v_1 and the last pendant b_l.
All are actual disjoint pairs. Every mandatory core entry and
nonempty norm is preserved. The balanced old cross column is-A1,
so the repaired residual Schur complement is exactly
6delta-kappa*delta^2>0. W becomes PD, increasing core rank by one
to N-3 and lower rank to **N-2**.

The symmetric core change has maximum absolute row sum3delta and
norm at most3delta. Since ||E0||^2=N, the whole Q change has norm
at most3Ndelta<1/4 and vanishes on1. The seed gap>=1 becomes at
least3/4 on1-perp. **Recompute the entire empty row and loop by the
lift after repair**; the old balanced empty vector cannot be retained.

For any real ordinary H competitor let f_i indicate a maximum
x_i-star and z_i=f_i-(s/N)1. All M entries on that star vanish.
Regularity gives L1=N1, and
z_i'Lz_i=s^2-2s^2+s^2=0. PSD then gives Lz_i=0. The two z_i
are independent: evaluating a relation at empty first gives the sum
of its coefficients zero, and at old singleton{x_1} gives the first
coefficient zero. Thus rank(L)<=N-2 for every such competitor.
The repaired construction attains the bound and its kernel is exactly
their span. Its cap gap makes1 the simple unit eigenvector of M,
so rank(I-M)=N-1. This proves the all-real rank assertion without
transferring a restricted-ansatz obstruction to H.

## Reproduction and trust boundary

The standalone [runner](verify.py) uses only Python3's standard library.
[RESULTS.json](RESULTS.json) retains all control data and fingerprints,
plus a hash of the **entire mathematical record including every
generated coefficient**. All coefficients and clearing factors are
regenerated and checked at replay; no external corpus is needed.
See [README](README.md) for commands and source provenance.

Eight fixed controls check512 grouped frame positions,128 triangle
diagonal/update positions and32 canceled Schur positions. Independent
Gaussian5 inverse quadratics agree exactly with the Schur3 expressions.
Four full actual fixtures(n,l)=(4,2),(5,2),(5,3),(6,2), with
N32,48,50,80, check372 reduced Gram/frame entries each,1567 complete
changed Gram/frame entries each,115 actual untouched eigenactions,
and12228 whole positions per seed/repaired matrix. Both centered
maximum-star kernels are verified. The prior9408 baseline is reproduced
at every225 core and16 residual position and credited as prior validation.
Nineteen semantic rejection controls remain active under -O.

Finite controls validate the formulas. Infinite coverage rests on the
ordinary complete-space, grouping, inverse, repair and rank proofs plus
the exact polynomial signs. Author normal/optimized agreement is not
independent mathematical review or formalization. A timeout, UNKNOWN,
incomplete enumeration, memory kill or algebra guard failure would be
an operational limit, not mathematical nonexistence.
