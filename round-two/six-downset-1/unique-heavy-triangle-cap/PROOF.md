# A structural cap for unique-heavy private triangle attachments

Actual author **six-downset-1 / researcher**, 2026-10-04.
Author-complete ordinary proof; **UNFORMALIZED and independently UNREVIEWED**.
Git history identifies the source commit. A graph record, when present,
is separate from the source release. Finite original controls are author
validation. The infinite and real quantifiers below are supplied by
the ordinary proof, not those controls.

Target: Spectral Chvatal Conjecture H of Ellis--Filmus--Friedgut,
Section4, <https://arxiv.org/html/2609.28404v1#S4>. The live primary
submission history was rechecked on2026-10-04 and still lists onlyv1,
submitted23September2026. General H and I are proposed there. Ordinary
H on private one-point attachments was already own9361/source
ca8d2e363536435ad034f08cf3845a6ffd276326. The two/three/four mark caps
are10270/10294/10316. Source9e7ada1cd3b0b966815e1711c9212e94dad2881f
supplies the credited retained-vector/scalar/mean recipes and repair
mechanism. Its cap certificate or review verdict is not imported.
The sealed private arbitrary-mark equal-light proof is a predecessor.
The new structural argument keeps EVERY old and light-mean direction,
allows unequal light counts, and uses a count-weighted original dual.
This is a strengthening of caps and ranks on a restricted family,
not a new assertion of ordinary H existence or historical priority.

## Statement

Let r,n,h,k1,...,k_(r-1) be INTEGERS satisfying

    r>=3, n>=max(4,r), h>k_g>=2 for each light group,
    F=h+sum_light k_g>=9.

Let X have size n and choose distinct marks x,y1,...,y_(r-1) in X.
Start with 2^X, attach h triangles at x and k_g triangles at y_g,
and take their downsets. A triangle is its mark plus a private pair;
ALL private pairs are mutually disjoint and outside X. Each triangle
adds three marked sets (mark+leaf1, mark+leaf2, mark+both) and three
private sets (leaf1, leaf2, both). The ACTUAL empty is retained with
its permitted loop. Set

    k0=h, q=2^(n-1), D0=3h, s=q+3h,
    L=sum_light k_g, F=h+L, m=3F, ell=m+1, N=2q+6F,
    P=I-J/N, J=11'.

The unique largest point star is heavy, of size s. Light old stars
have sizes q+3k_g, unmarked old stars q, and private stars4.

There is a RATIONAL symmetric supported stochastic seed M0 with
L0=sI+(N-s)M0>=0, lower rankN-2, and

    NI-L0 >= (N-2s)P=6L P,   rank(I-M0)=N-1.

The rationally defined repair line M_delta preserves support and row
sums. Its ENTIRE lower PSD interval, for REAL delta, is

    [0,6/kappa],
    kappa=1/(h mu_0)+1/S_L
          +4sum_light k_g mu_g^2/(S_L^2 beta_g), 0<kappa<25/68.

The scalar definitions are in Section2 and SCALAR-BOUNDS.md.
Lower ranks areN-2 at both endpoints andN-1 in the interior. For
EVERY REAL 0<delta<=1/8,

    NI-L_delta >= [6L-7delta]P,
    rank L_delta=rank(I-M_delta)=N-1.

The least eigenvalue -s/(N-s) and unit eigenvalue are simple.
At rational delta1/32 the original matrix is rational, with cap
(6L-7/32)P, at least(761/32)P in this domain; if r>=4 the minimum
floor is(1145/32)P. The construction respects leaf swaps, permutations
of the facets within each group, permutations of unmarked old points,
and exchanges of light groups of EQUAL counts. It does not assume
full light permutation symmetry for unequal counts.

No entrywise nonnegativity, overlapping private pairs, n<max(4,r),
F<9, general H/I, or optimal upper repair interval is asserted. There
is no cap assertion at the distant lower endpoint6/kappa.

## 1. Every retained vector and mandatory intersection

On the full old cube use the Gram

    sI+(q-D0)C_complement-J_(2q).

On Walsh characters it has eigenvalues0 on the constant,2q on every
nonconstant even character (dimensionq-1), and2D0 on every odd
character (dimensionq). Its only kernel is the constant; deleting the
empty gives a positive definite proper old Gram of dimension2q-1.
Choose full old vectors g_A of sum0. For proper old sets,

    g_A.g_B=s[A=B]+(q-D0)[B=X\A]-1.

Write G=sum_proper_old g_A=-g_old_empty and
H_a=-sum_(A contains a)g_A. Direct Walsh summation gives

    G^2=s-1, H_a^2=qD0, H_a.H_b=0 for a!=b,
    G.H_a=-D0, g_A.H_a=D0(1-2[a in A]).

The FULL old frame has eigenvalues2q and2D0 on its even and odd
physical spaces. The even/odd squared norms of G areq-1 andD0.
Every one of these old directions is retained.

For each group of size k=k_g take an orthogonal B space with

    B_i.B_j=(s/3)([i=j]-1/h).

The heavy space is a simplex of dimensionh-1 and sum0. Each light
space is positive definite of dimensionk<h. Its mean Bbar_g has
norm s(h-k)/(3hk)>0. All light means are mutually orthogonal.
Btilde_i=B_i-Bbar_g has Gram(s/3)([i=j]-1/k) and sum0.
Each facet has independent T_i1,T_i2,T_i3 of sum0 with Gram
s([a=b]-1/3), rank2. Old, B and different facet T spaces are
orthogonal. Define marked vectors

    V_ia=H_g/D0+B_i+T_ia.

Their norms are s-1. Every pair of different marked sets with the
same mark has inner product-1; different marks are disjoint. If
an old set contains the mark, its marked pairing is-1 by the
H formula. These exhaust all mandatory old/marked positions.
Old rows span old space, facet differences span all T, and marked
facet means after subtracting old parts span all B. Thus the retained
span has dimension

    (2q-1)+(F-1)+2F=2q+m-2.

Its2q+m-1 retained rows have the sole heavy-star relation: their
old heavy-star sum is-H_x and heavy marked sum isH_x.

## 2. Actual centroid and all count-dependent scalars

The retained-row sum isK=G+W, where

    W=H_x+sum_light(k_g/h)H_g+3sum_light k_g Bbar_g.

We have G.W=-m and
W^2=ms-9sum_groups k_g^2. Hence, exactly,

    K^2=qell+9sum_light k_g(h-k_g)+3h-6F-1.

Put z0=-K/ell and c0=z0^2. For a marked row of group g,

    z0.V_g=-(s-3k_g-1)/ell,
    R_g=1+z0.V_g=[ell+1-q-3(h-k_g)]/ell.

The common vector is orthogonal to all T and Btilde. Define

    mu_g=(s-3)/3-c0-9R_g^2/[2s(k_g-1)],
    alpha_g=2s-27(2k_g-3)R_g^2/[s(k_g-1)],
    beta_g=2s/3-3(k_g+3)R_g^2/[s(k_g-1)],
    S=sum_groups k_g mu_g, S_L=sum_light k_g mu_g,
    nu_g=mu_g+k_g mu_g^2/[S(k_g-1)].

SCALAR-BOUNDS.md proves ordinary real-parameter inequalities, valid
here because q>=8, h>=3, k_g>=2, F>=9:

    0<c0<s/27+1/4, |R_g|/s<1/17,
    mu_g-s/5>1123/9180, mu_g<s/3,
    s<alpha_g<=2s, s/2<beta_g<=2s/3,
    Fs/5<S<Fs/3, Ls/5<S_L<Ls/3,
    0<nu_g<37s/81<s/2, 0<kappa<25/68.

This identifies the pure scalar functions with the original geometry;
no count grid supplies their infinite quantifiers.

## 3. All private rows, actual empty and exactly two core kernels

For each group, abbreviatek=k_g,R=R_g and define

    B2=s(k-1)/(3k), a_g=R/(2B2), b_g=-2a_g, c_g=9R/(2s),
    P_i1=z0+a_g Btilde_i+c_g T_i2,
    P_i2=z0+a_g Btilde_i+c_g T_i1,
    P_i3=z0+b_g Btilde_i+c_g/(k-1)sum_(j!=i)T_j3.

The compulsory marked/private pairings are
z0.V+a_gB2-c_gs/3=-1 and z0.V+b_gB2=-1.
Set

    etaL=s-1-c0-a_g^2B2-2sc_g^2/3,
    etaF=s-1-c0-b_g^2B2-2sc_g^2/[3(k-1)],
    p0=-1-c0-a_gb_gB2.

Expanding gives mu=(2p0+etaF)/3,
alpha=2(2etaL-p0-etaF), beta=etaF-mu, exactly the functions above.
Give residual facet means M_i Gram with diagonalmu_g,
within-group off -k_gmu_g^2/[S(k_g-1)], and cross-group off
-mu_gmu_t/S. Every row sum is0. All off-diagonal entries are
negative, so this is a connected weighted graph Laplacian of rankF-1
with sole kernel ones. Its group contrast metric isnu_g.

Add independent WA_i,WF_i of squared normsalpha_g,beta_g,
orthogonal to all preceding spaces. Define

    W_i1=M_i+(WA_i-WF_i)/2,
    W_i2=M_i+(-WA_i-WF_i)/2,
    W_i3=M_i+WF_i, U_ia=P_ia+W_ia.

The identities mu+alpha/4+beta/4=etaL, mu+beta=etaF and
mu-beta/2=p0 give every private norm s-1 and every private
leaf/full pairing-1. The two leaves are disjoint. Private sets in
different facets, and all old/private pairs, are disjoint, so all
mandatory original nonempty positions are now paid. Residual span
has dimension(F-1)+2F=m-1, sole relation sumW=0.

The identities2a_g+b_g=0 and cancellation of every T term yield
sum_private P=mz0. Thus the total proper-row sum is
K+mz0=-z0: z0 is the ACTUAL empty vector, not a prescribed loop.
Retained rows span their entire retained space and subtracting their
projections from U gives all residual W. The complete proper Gram C
therefore has

    rank C=(2q+m-2)+(m-1)=N-3.

Its exactly two kernels are the heavy-star indicatorchi andrho,
where rho=m/ell on old/marked rows and1 on private rows. The latter
relation is(m/ell)K+mz0=0; independence follows on private rows.

Define the actual negative-row-sum lift

    Q00=1'C1, Q0A=-(C1)_A, QAB=CAB.

It is the full Gram includingz0, with Q1=0 and rankQ=N-3.
L0=J+Q and M0=(L0-sI)/(N-s) are rational: for example the separated
basis of geometry.py has rational metric and rational row coordinates
in every declared integer case. Original nonempty intersections and
diagonals give the required zero entries of M0; empty entries and its
loop come from the lift. Thus M0 is symmetric, supported, stochastic,
L0>=0 and rankL0=N-2.

## 4. Exhaustive physical decomposition

For a physical vector v the FULL frame form is
S(v,v)=sum_(A in D)(row_A.v)^2, including ACTUAL empty. Nonzero
eigenvalues of Q are eigenvalues of this frame operator. Use these
exhaustive orthogonal physical sectors:

1. FIRST: ALL old directions and each of the r-1 light B means,
   dimension2q+r-2, handled as a whole in Section5.
2. Each facet's two leaf-odd directions(T_i1-T_i2,WA_i), dimension2F,
   with metricdiag(2s,alpha_g).
3. Each group's k_g-1 facet-standard four-blocks
   (Btilde_t,TS_t,WF_t,M_t), TS_i=T_i1+T_i2-2T_i3. Orthogonal
   profiles t=(1,...,1,-j,0,...), j=1,...,k_g-1 exhaust its zero-sum
   facet space. Metric isdiag(2s/3,12s,2beta_g,2nu_g) times
   sum(t_i^2)/2. Totaldimension4(F-r).
4. Each group's two traces(sumTS_i,sumWF_i), dimension2r,
   metricdiag(6k_gs,k_gbeta_g).
5. Residual group means, dimensionr-1; the r group sums have sole
   relation their total is0.

Their dimensions sum to(2q+r-2)+2F+4(F-r)+2r+(r-1)=N-3.
Metric cross terms vanish by the defined orthogonal spaces and
zero-sum profiles. Frame cross terms vanish on summing the ORIGINAL
rows: leaf-odd signs cancel, standard profiles sum0, each T/WF trace
has two leaf scores plus one full score summing0, all private FIRST
scores are the commonz0 score, and sumM=0. Old/marked FIRST scores
are constant within each group. These cancellations include ALL
private and actual-empty rows; no equal-light exchange is needed.
No quotient or profile multiplicity is substituted for the full span.

## 5. A structural Schur bound on the ENTIRE FIRST sector

Let j_g=H_g/D0+Bbar_g, with heavy Bbar0, and

    W=sum_groups 3k_g j_g, K=G+W,
    A=A_old_full+sum_groups 3k_g j_g tensor j_g.

Full old frame A_old_full has eigenvalues2q on even and2D0 on
odd directions. The old proper frame removes g_old_empty=-G.
Every private row and the ACTUAL empty has FIRST projection-K/ell.
Consequently the WHOLE FIRST frame is

    S_FIRST=A-G tensor G+(K tensor K)/ell.                 (1)

Put D=2sI_FIRST-A. Orthogonally split FIRST into old even directions,
old odd directions perpendicular to ALL r independent H_g, the
heavy H_x line and EACH light plane(H_g,Bbar_g). The first three
types have D eigenvalues6h,2q,q, respectively. On a light plane in
its physical orthonormal basis, witht=k_g/h in(0,1), D is

    [ q(2-t)                 -sqrt(qst(1-t)) ]
    [ -sqrt(qst(1-t))          s(1+t)        ].

Its determinant is EXACTLY2qs>0 and both diagonals are positive.
Thus D is positive definite on EVERY FIRST direction.

Let g=G.D^-1G, z=G.D^-1W, w=W.D^-1W. On a light plane W has
normalized coordinates(sqrt(3hq)t,sqrt(3k_gs(1-t))) and G has
coordinates(-sqrt(3h/q),0). Direct two-by-two inversion gives
light contributions3k_g to w and-3k_g/q to z. The heavy line
contributes3h and-3h/q. W has no other component, so

    w=m, z=-m/q,
    g=(q-1)/(6h)+3h/(2q)+3F/(2q^2)>=0.                    (2)

The last formula sums the even normq-1, the odd perpendicular norm
D0(1-r/q), the heavy line and ALL light planes. q>=r in the stated
integer domain; a zero-dimensional perpendicular space is harmless.
Only g>=0, rather than this formula, is needed for the next step.

Let B=D+G tensor G>0. Sherman--Morrison andK=G+W give

    K.B^-1K=g+2z+w-(g+z)^2/(1+g),
    ell-K.B^-1K=(1-z)^2/(1+g)=(1+m/q)^2/(1+g)>0.           (3)

The rank-one criterion now gives B-(K tensor K)/ell>0. By(1)
this is2sI_FIRST-S_FIRST. This argument pays the whole growing
FIRST space, including every unequal light plane and old parity
direction, without an invariant-only cap certificate.

## 6. Strict 2s bounds on all remaining physical sectors

Use |a_g|<3/17<3/13, |c_g|<9/34<9/26 and the scalar lemma.
In physical orthonormal coordinates, an anti block has diagonal
s(1+c_g^2),alpha_g/2 and off-diagonal magnitude at most|c_g|s.
A trace block has diagonal s(1+c_g^2),3beta_g/2 and off-diagonal
magnitude at most|c_g|s. Both absolute row sums are at most
(991/676)s<2s. For the trace calculation the ORIGINAL row
coordinates in its trace basis are

    marked leaf(1/(6k),0) count2k, full(-1/(3k),0) countk,
    private leaf(c_g/(6k),-1/(2k)) count2k,
    private full(-c_g/(3k),1/k) countk.

For a standard prototype t=(1,-1,0,...), the original row coordinates
in its four-block basis are

    marked leaf(1/2,1/12,0,0) count4,
    marked full(1/2,-1/6,0,0) count2,
    private leaf(a_g/2,c_g/12,-1/4,1/2) count4,
    private full(b_g/2,c_g/[6(k-1)],1/2,1/2) count2.

Changing the profile multiplies BOTH the metric and score form by
sum(t_i^2)/2, leaving the normalized frame unchanged. Thus these
calculations pay each of all k-1 copies. The normalized diagonals are

    s(1+2a_g^2), s[1+c_g^2/3+2c_g^2/(3(k-1)^2)],
    3beta_g/2, 3nu_g.

The only nonzero off-diagonal magnitudes are

    B-TS: s|a_gc_gz|sqrt(2)/3, B-WF: |a_g|sqrt(3s beta_g),
    TS-WF: |c_gz|sqrt(6s beta_g)/6,
    TS-M: |c_g|k sqrt(6s nu_g)/[3(k-1)], z=(k-3)/(k-1).

Here |z|<=1, k/(k-1)<=2, beta<=2s/3,
nu<37s/81<29s/57, sqrt(2)<3/2 and sqrt(58/19)<7/4.
The four absolute row sums are bounded, respectively, by

    (1009/676)s, (1135/676)s, (19/13)s, (1907/988)s,

all below2s. For example the first sum is at most
s[1+18/169+27/676+9/26]=1009s/676; the second is at most
s[1+81/676+27/676+3/26+21/52]=1135s/676.
Gershgorin for these symmetric normalized forms pays every physical
standard copy, including its positive profile scale.

Finally the full residual-mean Gram is a Laplacian with
diagonalmu_i<s/3; its largest eigenvalue is at most2max(mu_i)<2s/3.
The private frame on the aggregate mean sector is3 times this Gram,
so EVERY r-1 aggregate mode is below2s. Standard mean modes are
already paid in their coupled four-blocks.

Sections4--6 cover ALL N-3 positive physical directions. Therefore
Q is strictly below2sP on its positive span, and Q<=2sP globally.
Since L0=J+Q,

    NI-L0 >=(N-2s)P=6L P.

This is the ordinary infinite proof of the cap; no finite count
enumeration or floating-point estimate supplies its quantifiers.

## 7. Count-weighted original dual and ENTIRE lower PSD line

Let a be the heavy PRIVATE indicator divided by h. On each light
PRIVATE FULL row of group g put b=mu_g/S_L, with b=0 elsewhere.
Then sum a=3,sum b=1 and their supports are disjoint. Set

    p=a-3b, c=(a+3b)/6,
    C_delta=C+delta(ab'+ba')=C-delta pp'/6+6delta cc'.

All changed proper entries concern disjoint sets, and
p.chi=c.chi=p.rho=0,c.rho=1. Unequal groups require this weighted
b; an unweighted light-full average is not the defined candidate.

For M_x=sum_heavy M_i, the full residual Laplacian gives

    M_x^2=hmu_0S_L/S,
    M_x.M_heavy=mu_0S_L/S,
    M_x.M_light=-hmu_0mu_g/S.

The complete physical dual is

    Zdual=M_x/[hmu_0S_L/S]
          -2sum_light[mu_g/(S_Lbeta_g)]sum_(i in g)WF_i.

Its scores are1/h on every heavy private row,0 on every light
private leaf, and-3mu_g/S_L on every light private full row.
Every old, marked and ACTUAL empty score is0. Squaring gives

    ||Zdual||^2=1/(hmu_0)+1/S_L
               +4sum_light k_gmu_g^2/(S_L^2beta_g)=kappa.

All original proper rows span the full positive physical space.
Hence this is p'C^dagger p, with no reduced pseudoinverse bridge.

For delta>0 work modulochi and split RanC from its remaining null
directionrho. Completing the square in its rho coefficient leaves
C-delta pp'/6 on RanC and a positive square6delta(cc') alongrho.
The rank-one PSD criterion is delta kappa<=6. Core rank isN-2 for
0<delta<6/kappa andN-3 at delta=6/kappa, alsoN-3 at0. The actual
lift preserves core rank; adding J increases it by one. Thus lower
ranks areN-1 in the interior andN-2 at both endpoints.

For delta<0, rho has negative energy6delta. For delta>6/kappa,
choose any proper x with Cx=p and x'p=kappa, and put
v=x-(c'x)rho. Then c'v=0,p'v=kappa and

    v'C_delta v=kappa-delta kappa^2/6<0.

Such x exists by the full original dual/span. Embed a proper vector
with empty coordinate0 and center it by ones; the ACTUAL lift has
the same energy and J vanishes. These prove both outside directions
of this candidate's exact lower interval, not mathematical H absence.

## 8. Original lifted cap, all real repairs and greatest ranks

Let A=(-3,a),B=(-1,b) include ACTUAL empty coordinates. The full
lift perturbation isdelta(AB'+BA') and annihilatesones. Its exact
norm for delta>=0 isdelta(A.B+||A||||B||). By the scalar lemma,

    A.B=3, ||A||^2=9+3/h<=10,
    ||B||^2=1+sum_light k_gmu_g^2/S_L^2<17/12,
    ||A||^2||B||^2<85/6<16.

Thus its norm is strictly below7delta. The seed cap yields

    NI-L_delta >=[6L-7delta]P.

Since kappa<25/68, every real0<delta<=1/8 is strictly inside the
lower interval. The upper floor is at least185/8>0 because L>=4.
Lower and upper ranks are consequently bothN-1. The centered
heavy-star indicator is the surviving lower kernel, so the least
eigenvalue -s/(N-s) is simple; the upper kernel is ones, giving
simple unit eigenvalue. For rational delta1/32 all entries remain
rational. Permutation symmetries follow from group sizes, sums,
means and the weight mu_g/S_L; equal counts have equal weights.

## Exact finite validation and delivery boundary

geometry.py produces a NEW separated rational physical basis, without
importing a predecessor executable or certificate. reader.py imports
no producer and reconstructs the entire literal downset. It checks ALL
original support and actual-loop positions, full positive physical
metric/span/2s cap, both whole FIRST inverse products, the original
Schur margin, weighted dual scores, kernel relations, repaired lifts,
selected original caps and outside-line negative witnesses. Exact
positive forms use full fraction-free leading-minor elimination;
assertions and floating-point arithmetic are not proof gates.

The declared controls are n4,(4,3,2),N70, n4,(5,2,2),N70 and
n4,(3,2,2,2),N70. The second covers the minimum light-total L4;
the third freshly reproduces the ENTIRE proper C and seed M0 of
source9e7ada1c, with full hashes recorded by the reader; it transports
no old cap, certificate or review verdict. These are finite author
controls by different calculations, not independent mathematical
review or all-count enumeration. The generic support, span, physical
multiplicities, real Schur/rank and weighted-dual bridges are the
ordinary proof above and SCALAR-BOUNDS.md.

Literal original guards stay n<=6,h<=10,N<=80 BEFORE construction,
one native thread and one intensive child,60s per math child,32MiB
packing. No input polynomials are used; the512-term guard is not
increased. Minimal original r5N98, balanced-fourN88 and first unequal
r4N82 are NOT constructed. The unequal control uses r3 with n4 and
F9, within the theorem's explicit domain. The completed source-only
normal/optimized/cold and semantic adverse gates are recorded separately
in VALIDATION.json and EXPECTED.json. They are author validation of the
ordinary proof. PROVENANCE.json records reversible publication-status
edits to the three documents; all four programs and both complete
evidence files preserve the paid sealed bytes. Source publication,
graph commitment and independent review remain separate facts.
