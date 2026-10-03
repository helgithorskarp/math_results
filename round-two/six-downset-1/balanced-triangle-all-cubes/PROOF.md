# Balanced private triangles on every old cube of dimension at least three

Actual author **six-downset-1**, role **researcher**, 2026-10-03.
Author lemma with a complete ordinary argument and exact coefficient
certificate. The physical completeness, spectral and Schur arguments are
unformalized. Independent review and formalization remain pending.

The target is [Conjecture H, Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
A live abstract/version-history/Section 4 check on 2026-10-03 still found
September 23 v1 only, with H and I proposed. The paper's classical and
projection-packing proofs do not supply their tight matrices.

Ordinary H existence and greatest lower-rank attainment for the family below
are already prior9361: each private two-point input has star size 2 strictly
below q. The added result is the upper cap, simple unit eigenvalue and explicit
gap at that attained rank. The completed old-three-cube result is committed
10093/7, with [source960058d](https://github.com/helgithorskarp/math_results/blob/960058d192b80040f9e81385e0ca34e8b51f4f20/round-two/six-downset-1/balanced-triangle-cube-three/PROOF.md).
The balanced old-edge [sourceca801e8](https://github.com/helgithorskarp/math_results/blob/ca801e8e7f5ff26071a4cb59029cc07d447337c2/round-two/six-downset-1/balanced-triangle-edge/PROOF.md)
supplies the credited completion and repair mechanism; its rejected graph
candidate remains uncommitted and is not a graph premise. Prior9926/10046
concerns h triangles at one mark and ONE at the other, a different family.
No independent verdict for those carriers transfers here.

## Statement and family

Let n>=3 and h>=2 be integers. Let X be an n-point set with two distinct
marks x,y. Adjoin h triangles {x,a_i,b_i} and h triangles {y,c_i,d_i};
all 2h private pairs are mutually disjoint and outside X. Let the downset
be the union of 2^X and all the triangle downsets. Its ground has n+4h
points; its original vertices include the actual empty set and its loop.
Set

    q=2^(n-1), D=3h, s=q+D, w=s-1, ell=6h+1, N=2q+12h.

Each triangle contributes three private and three marked nonempty rows.
Exactly x,y have maximum stars of size s: every other old point has star
size q and every private point has star size 4. There is a rational matrix
M on ALL original vertices such that

    M=M^T, M1=1, M[A,B]=0 if A intersects B,
    L=(N-s)M+sI >=0,                  I-M>=0,
    rank L=N-2,                       rank(I-M)=N-1,
    ker L=span(chi_x-(s/N)1, chi_y-(s/N)1).

The eigenvalue 1 is simple. With P=I-J/N, L=J+Q_repaired, and the
explicit delta below,

    NP-Q_repaired >=(1-8delta)P,       1-8delta>3/4.

Thus the unit-M gap on 1-perp is at least (1-8delta)/(N-s). The attained
lower rank is greatest among ALL REAL ordinary H competitors, without
cap or invariance assumptions. The rank bound and ordinary attainment
are credited prior art; the additional cap extends the inspected n=3
balanced cap to every n>=3. No priority, cap optimality, arbitrary downset,
general H/I, unequal triangle counts, overlapping private pairs or h=1
claim is made. The separate old-edge source treats n=2; this proof uses
q>=4 and does not assert its q=2 singular decomposition.

## Complete old Gram

For the 2q-1 nonempty old sets use the credited prior9361 Gram

    A_D=(q+D)I+(q-D)P_old-J,

where P_old exchanges each proper complementary pair and has full-set
row zero. Let g_A be its rows, G=sum g_A, gF=g_X, and
Hx=-sum_(x in A)g_A, Hy=-sum_(y in A)g_A. Direct counts give

    G^2=gF^2=w, G.gF=D-q+1,
    Hx^2=Hy^2=qD, Hx.Hy=0,
    G.Hx=G.Hy=gF.Hx=gF.Hy=-D.

The orthogonal vectors

    E=G-gF, U=G+gF, R=Hx+Hy+G+gF, A=Hx-Hy

have squared norms 4(q-1),4D,2D(q-2),2qD. All are positive for q>=4.
Put K=G+Hx+Hy=E/2-U/2+R, so K^2=q-1+(2q-3)D.

For completeness, enumerate the q-1 proper complementary pairs
(A_j,X\A_j), and define p_j=g_Aj+g_complement, d_j=g_Aj-g_complement.
Then

    p_i.p_j=4q delta_ij-4, d_i.d_j=4D delta_ij,
    p_i.d_j=0, p_i.gF=-2, d_i.gF=0.

The p-contrast space sum t_j=0 has dimension q-2 and positive metric
4q sum t_j^2. It is orthogonal to E,U and every d_j. In the d-space,
R and A have coefficient vectors

    r_j=1-[x in A_j]-[y in A_j],
    a_j=[y in A_j]-[x in A_j].

Their supports are disjoint; coefficient squared norms are (q-2)/2 and
q/2. Their orthogonal complement has dimension q-3 and positive metric
4D sum t_j^2. Thus E,U,R,A and the two contrast spaces form an entire
independent positive decomposition of the old space:

    4+(q-2)+(q-3)=2q-1.

The old frame operator has eigenvalues 2q on the p-contrasts and 2D on
the d-complement. Indeed A_D applied to these coefficient vectors has
these eigenvalues, since J kills their coefficient sums and P_old acts
by +1 or -1. This identifies every old direction rather than projecting
away untouched directions.

## Marked rows and balanced private completion

For each mark independently introduce B_i with sum B_i=0 and
B_i.B_j=(s/3)(delta_ij-1/h). For every facet introduce T_i1,T_i2,T_i3
with sum zero and T_ia.T_ib=s(delta_ab-1/3). These spaces, both mark
groups, and the old space are mutually orthogonal. The marked rows are

    V_sigma,ia=Hsigma/D+B_sigma,i+T_sigma,ia.

Their norms are w, and all distinct rows in one mark group pair to -1.
Cross-mark rows pair to zero and are disjoint. Direct old counts give
g_A.Hsigma=D(1-2[sigma in A]); hence every required old/marked pairing
is -1. Required old/old pairings are also -1. These are Gram pairings;
the resulting disjoint entries of M may be signed.

The old/marked rows recover all old,B,T directions and have exactly
the two star relations

    sum_(x in A)g_A+sum V_x=0, sum_(y in A)g_A+sum V_y=0.

Their span has dimension 2q-1+2(h-1)+4h=2q+6h-3, and their sum is K.

Set

    z=-K/ell, B2=s(h-1)/(3h), c0=[q-1+(2q-3)D]/ell^2,
    a=3h(ell-q+1)/[2ell s(h-1)], b=-2a,
    c=9(ell-q+1)/(2ell s).

Within each mark group use private projections

    P_i1=z+aB_i+cT_i2, P_i2=z+aB_i+cT_i1,
    P_i3=z+bB_i+[c/(h-1)]sum_(j!=i)T_j3.

The other-facet sum is within that same group. Since z.V=-(q-1)/ell,

    -(q-1)/ell+aB2-cs/3=-1,
    -(q-1)/ell+bB2=-1.

These cover both required leaf/marked pairings and all three required
full-private/marked pairings in their facet. Other old/private and
cross-facet private pairs are disjoint, so impose no support constraint.
The B and T contributions cancel across ALL private rows: sum P=6hz.

Define exact residual scalars

    etaL=w-c0-a^2B2-2sc^2/3,
    etaF=w-c0-b^2B2-2sc^2/[3(h-1)],
    p=-1-c0-abB2,
    mu=(2p+etaF)/3,
    alpha=2(2etaL-p-etaF), beta=etaF-mu,
    nu=2h mu/(2h-1).

Use 2h facet means M_i with diagonal mu, off-diagonal -mu/(2h-1),
and sole relation sum M_i=0. Orthogonally add WA_i,WF_i of norms
alpha,beta, and put

    W_i1=M_i+(WA_i-WF_i)/2,
    W_i2=M_i+(-WA_i-WF_i)/2, W_i3=M_i+WF_i.

The signs below prove positivity and rank 6h-1, with sole relation
sum W=0. The identities

    mu+alpha/4+beta/4=etaL, mu+beta=etaF, mu-beta/2=p

give every private norm w and required intersecting leaf/full pairing
-1 for U_ia=P_ia+W_ia. Private leaves in one facet are disjoint, as
are private sets in different facets. All required support is covered.

The nonempty row span has dimension

    (2q+6h-3)+(6h-1)=2q+12h-4=N-4.

Their total is K+6hz=K/ell=-z. Thus the actual empty row is z, with
norm c0. The whole negative-row-sum Gram lift Q is PSD, Q1=0, and
rank Q=N-4. If C is the nonempty Gram, this lift is explicitly

    Q[empty,empty]=1^T C1,
    Q[empty,A]=-(C1)_A, Q[A,B]=C[A,B] for nonempty A,B.

Take L=J+Q and M=(L-sI)/(N-s). Every nonempty diagonal of L is s,
every required off-diagonal is zero, L1=N1, and L is PSD of rank N-3.
The actual empty loop is recomputed by the lift and is never discarded.

## Entire physical frame and every untouched old direction

For a physical vector v let S(v,v)=sum_(B in ORIGINAL downset)(g_B.v)^2,
including the actual empty row. Write Gamma for the physical metric.
To prove the seed cap floor1, prove (N-1)Gamma-S positive definite on
the ENTIRE N-4-dimensional row span.

Independent within-facet leaf swaps and within-mark facet permutations
preserve both forms. Each odd leaf character has basis
(T_i1-T_i2,WA_i) and metric diag(2s,alpha): there are 2h such blocks.
Write TS_i=T_i1+T_i2-2T_i3. Each within-mark contrast t with sum zero
has basis (B_t,TS_t,WF_t,M_t) with representative metric
diag(2s/3,12s,2beta,2nu), scaled by sum t_i^2/2. There are h-1 such
blocks per mark. The profiles (1,...,1,-k,0,...,0), k=1,...,h-1,
are a complete mutually orthogonal basis, with scale k(k+1)/2.

The remaining changed bases and metrics are

    even: E,U,R,sum TS,sum WF,
          diag(4(q-1),4D,2D(q-2),12hs,2h beta);
    odd:  A,sum_x TS-sum_y TS,sum_x WF-sum_y WF,sum_x M-sum_y M,
          diag(2qD,12hs,2h beta,2h nu).

There is no total facet-mean direction because sum M_i=0, and all B
sums vanish. Orthogonality of BOTH forms follows directly from their
symmetries: distinct leaf characters are killed by a leaf swap; each
leaf-even cross-facet form is diagonal-plus-constant under the mark's
full permutation group, whose constant part kills a contrast; cross-mark
entries are constant in both facet indices and kill either contrast.
The remaining sums split by mark exchange into even and odd spaces.
This argument also covers h=2, whose contrast space is one-dimensional.

Every extra old projection lies in span(G,Hx,Hy), orthogonal to the
p-contrasts and d-complement above. The old frame eigenvalues therefore
make those old spaces S-orthogonal to every changed direction as well.
Their cap multipliers are

    p-contrasts: N-1-2q=12h-1>0, dimension q-2;
    d-complement: N-1-2D=2q+6h-1>0, dimension q-3.

The total dimensions are

    2h*2+2(h-1)*4+5+4+(q-2)+(q-3)=N-4.

All metric factors are positive, so this is a complete independent
decomposition. No extra old contrast, star, kernel or empty contribution
has been removed by a quotient.

For explicit original-row accounting, the fixed-even coordinates of a
proper old row with r=[x in A]+[y in A] are
(1/[2(q-1)],0,(1-r)/(q-2),0,0). Counts for r=0,1,2 are q/2-1,q,q/2-1.
The full old row is (-1/2,1/2,0,0,0). Marked leaf/full rows have old
coordinates (0,-1/(2D),1/(2D)) and trace coordinates (1/(12h),0),
(-1/(6h),0), with counts 4h,2h. Private leaf/full old coordinates are
(-1/(2ell),1/(2ell),-1/ell), and trace coordinates
(c/(12h),-1/(4h)),(-c/(6h),1/(2h)), with counts 4h,2h.
The actual empty has those same old coordinates and trace zeros.

In the fixed-odd basis, the old r=1 rows have first coordinate +/-1/q,
q such rows; all other old rows have zero projection. Marked leaf/full
rows have coordinates
(1/(2D),1/(12h),0,0), (1/(2D),-1/(6h),0,0), with counts4h,2h.
Private leaf/full rows have coordinates
(0,c/(12h),-1/(4h),1/(2h)), (0,-c/(6h),1/(2h),1/(2h)), counts4h,2h.
All coordinates change sign in the y-group. The actual empty is even,
so contributes zero to this odd form. sectors.py sums every one of
these original row projections, as well as the leaf/standard rows.

## Closed aggregate forms and exact unbounded signs

The separate checker uses simplified residual scalars

    mu=(s-3)/3-c0-2sc^2/[9(h-1)],
    alpha=2s[1-2(2h-3)c^2/[3(h-1)]],
    beta=2s/3-4sc^2(h+3)/[27(h-1)].

Its leaf frame is
[[2s^2(1+c^2),-sc alpha],[-sc alpha,alpha^2/2]]. Its standard frame
is the sum of outer products of

    [s/3,s,0,0] x4, [s/3,-2s,0,0] x2,
    [as/3,cs,-beta/2,nu] x4,
    [bs/3,2cs/(h-1),beta,nu] x2.

independent.py expands those four aggregate rows into separate closed
entries, rather than importing the original-row projection code. Its
even old-three frame is

    [[4(q^2-1),-4D(q-1),0],[-4D(q-1),4D^2,0],[0,0,4D^2(q-2)]]
      +2D outer(0,-2,q-2)
      +(1/ell)outer(2(q-1),-2D,2D(q-2)).

The trace-two frame shared by even and odd sectors is

    [[12hs^2(1+c^2),-6hcs beta],[-6hcs beta,3h beta^2]].

Every old/trace cross entry cancels in the complete leaf/full sums.
The odd frame is the block sum of scalar 2qD(2D+q), that trace-two
frame, and scalar6h nu^2. The untouched representative metrics/frames
are (8q,16q^2) and (4D,8D^2).

All arithmetic is in characteristic-zero QQ(h,q). Original poles
h,h-1,ell,s,2h-1,q,q-1,q-2 are positive for auxiliary real h>=2,q>=4.
First divide each ORIGINAL cap row by its positive diagonal metric.
This divides each leading determinant by a positive product and
preserves its sign. Exact rational Gaussian elimination cancels known
factors before expanding polynomial numerators; the original Bareiss
and initially normalized Bareiss attempts exceeded the unchanged512-term
guard and are preserved as incomplete operational outcomes. No resource
limit was raised. Gaussian elimination completes within the same limits.

GAUSSIAN.json retains all66 normalized original entries, all20 pivots,
and all59 local elimination updates. The20 obligations are the3 scalar
signs and cap block sizes2,4,5,4,1,1. Composing every pivot numerator
with h=2+u,q=4+v gives432 strictly positive nonzero coefficients, with
positive constant term in every polynomial. Maximum total degree is15.
Every denominator factor has an independently checked positive shift.
Thus all pivots and every leading cap determinant are strictly positive
on the ENTIRE auxiliary real quadrant. The original cap matrices are
symmetric; Sylvester's criterion proves their positive definiteness.
Scalar positivity also proves all asserted physical metrics.

check_gaussian.py imports neither producer, recipe, sector module nor
factored-field arithmetic. Its separate integer/Fraction arithmetic
and closed forms verify all66 original rational-function coefficient
identities. Numerator/denominator bidegrees are propagated conservatively
through the independent expressions. After clearing denominators, a
global bound (32,9) is sufficient:330 distinct Cartesian nodes, hence
21,780 entry-node equalities, prove every original identity.

Each local update is verified as the polynomial identity

    pivot*before-pivot*after-left*right=0.

Known identical polynomial factors are cancelled exactly, and a positive
common denominator is cleared. Complete Cartesian grids with separately
computed bidegree bounds verify all59 identities on1,293 nodes. A
polynomial of bidegree at most(a,b) vanishing on(a+1)*(b+1) distinct
Cartesian nodes is identically zero: fix one variable, apply the
univariate root bound, then apply it to each coefficient in the other.
This proves QQ(h,q) identities; it is not finite sampling extrapolation.
All20 whole binomial compositions,432 signs,10 distinct positive
denominator polynomials and479 recorded positive-factor occurrences
are checked. The checker links every pivot and update to its complete
original working matrix, rejecting selected-prefix certificates.

Combining these signs with the COMPLETE physical decomposition gives
(N-1)Gamma-S>0 on the N-4-dimensional span for every integer n>=3,h>=2.
Nonzero eigenvalues of the whole Gram Q and its physical frame operator
coincide. On 1-perp, therefore,

    (N-1)P-Q >=0, hence NP-Q >=P.

The seed cap has rank N-1. Real h,q are used only for coefficient signs;
the original family, multiplicities and old contrast dimensions require
integer h>=2 and q=2^(n-1), integer n>=3.

## Original principal, inverse energy and full rank repair

Delete the old singleton rows x,y and the last y-private full row. The
retained original principal A_* has size N-4 and is positive definite.
The two old/marked relations have identity coefficients at x,y, so
deleting those leaves an independent old/marked basis of dimension
2q+6h-3. The sole private W relation is sum W=0; deleting one private
row leaves W dimension6h-1. Project a relation among retained original
rows onto W first: every retained private coefficient vanishes, after
which old/marked independence finishes the argument. The projections
P_i cannot add a hidden retained relation.

The deleted private row has coefficients -1 at every other private
row,0 at marked rows, and

    -(6h/ell)(1-[x in A]-[y in A])

at old row A. These are0 at the deleted x,y. This follows from
sum U=6hz=-6hK/ell. Let z_* be the retained coefficients and
b_*=A_*z_*. Its norm is w. If r is1 on the first x-private triple and
zero elsewhere, then r^T z_*=-3.

Eliminating the independent old/marked block leaves the private Schur
block equal to the W principal with its last row deleted. Extend r by
-3 at that deleted row to give sum zero. Its facet-mean component is
(1,1,1) on the first facet and(-1,-1,-1) on the last: squared length6
and W eigenvalue3nu. Its residual component is(1,1,-2) on the last
facet: squared length6 and W eigenvalue3beta/2. Its WA component is0.
Solving modulo the sole ones kernel and choosing deleted coordinate0
gives the principal inverse. Consequently

    kappa=r^T A_*^-1 r=2/nu+4/beta>0.

Take delta=1/[4(8+kappa)]. Increase by delta the three symmetric
pairings between the first x-private triple and the last y-private full
row. They are free disjoint pairs; A_* is unchanged. Its Schur complement
in the repaired retained-plus-last principal is

    w-(b_*+delta r)^T A_*^-1(b_*+delta r)
      =6delta-kappa delta^2>0,

since kappa delta<1/4. The two star relations have private coefficients0
and survive. Reinsert the old singletons through those relations. The
entire repaired core is PSD of rank N-3, with exactly the two original
star relations. Its negative-row-sum lift has rank N-3; adding J yields
rank L=N-2 and exactly the two centered star kernels.

The actual empty row and loop are recomputed by that WHOLE lift. Its
change is delta(uv^T+vu^T), where

    u=sum_(first x-private triple)e_i-3e_empty,
    v=e_last_y_private_full-e_empty.

Both lie in1-perp; u^2=12,v^2=2,u.v=3. The operator norm is
(3+2sqrt(6))delta<8delta<1/4. Hence

    NP-Q_repaired >=(1-8delta)P, 1-8delta>3/4.

This proves rank(I-M)=N-1, simple unit and the stated unit-M gap.
The whole-lift repair mechanism is credited to9723/9986, the balanced
old-edge source, and completed10093/7; the complete variable-q original
principal and frame hypotheses have been proved here.

For ANY REAL ordinary H matrix, a maximum star S satisfies L[S,S]=sI
and L1=N1. Its centered indicator has zero L-energy, so PSD places it
in ker L. The centered x,y stars are independent by their coordinates
at empty,{x},{y}. Thus every competitor has rank L<=N-2. Our repaired
matrix attains this credited ordinary optimum with the additional cap.

## Exact controls, reproducibility and trust

The unchanged probe.py and arithmetic/vector utilities are credited
copies of the sealed completed q4 source. Its n=4,h=2 control was first
run on the entire original matrix and saved before any new symbolic
formula. sector_control.py reconstructs ALL variable-q old contrast
directions by exact nullspace and rational orthogonalization, then
checks every internal and cross Gram/frame/cap position and full basis
independence. The full original checks include support, rows, actual
stars, actual empty, PSD/ranks, retained principal, inverse, Schur and
whole cap-floor equations:

    n4,h2: N40,s14,span36;1,600 original positions,
        Gram/frame1,296 each;internal300/cross3,588;
        repaired lower/cap38/39;
        SHA6090acd333a5cb22d5b0a28157eaa8cbc398068febcbd6fe0b15c59377d4602d.
    n4,h3: N52,s17,span48;2,704 original positions,
        Gram/frame2,304 each;internal420/cross6,492;
        repaired lower/cap50/51;
        SHAeacddfc093128206fb67681ee86fa89ba4feae61f826116ea1e659fa801b87f3.

These fixtures validate the reconstruction and coupled parameters; the
ordinary COMPLETE decomposition, degree-complete exact identities and
Schur arguments prove the unbounded statement. This is separate
same-author checking, not person-independent review or a proof assistant.

Generated outputs stay in ignored work/. Operational guards remain60s
per child,512 polynomial terms,32MiB packing, literal h<=10/n<=6/N<=80,
native threads1, serial mathematical child1,1CPU/2GiB scope. The literal
guards bound the finite implementation controls, not the proved theorem.
Source-only normal and optimized replays passed with ENTIRE15,239-byte
mathematical records equal, SHAe29cc3d35250caf9319a1b4ed471a5c05512e89656a21fecad43883ad4316126.
Every generated145,931-byte coefficient certificate equals the frozen source
byte for byte. All eight altered semantic certificates are rejected in each
mode; no timeout or killed process is counted as rejection. Max mathematical
child 5.17422s and peak 25632KiB.
The compact-JSON replay exposed a dictionary-order assumption, corrected
to exact form KEY SET; pivot/update LIST order and every coefficient
obligation remain exact. No formula or resource guard was changed.
This source packet supplies the portable complete certificate and its
[reproduction command](README.md). Original finite-control status strings
are retained to describe those routines alone. The uniform argument is
the complete ordinary proof above, unformalized and independently
unreviewed. [SOURCES.json](SOURCES.json) records credited copies and
[VALIDATION.json](VALIDATION.json) records the sealed source-only checks.
