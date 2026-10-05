# Exact optimal individual weights for the fixed q18 Schur/dual certificate

Actual **six-downset-3 / researcher**, 2026-10-05. Complete ordinary
author proof, **UNFORMALIZED and independently UNREVIEWED**. This is
one component of the credited self-contained combined source. NEW
reader delivery observations are in [VALIDATION.json](VALIDATION.json);
source integrity, computational reproduction, mathematical proof and
actual graph commitment are separate. No original-candidate PSD factor
or peer executable is imported.

## Premises and scope

Use exactly the fixed carrier, comparison and rational witness in the
source-published [NS-fiber proof](https://github.com/helgithorskarp/math_results/blob/782bc9042896c0f3887b1807dbd991f75fa13c9b/round-two/six-downset-3/q18-ns-fiber-obstruction/PROOF.md).
Its actual downset consists of all sets of size at most two on
{a,b,c} union Z union W, with |Z|=|W|=9, and triples containing at least
two core points, except bcZ. The empty vertex and loop are retained.
There are N=278 actual vertices and a unique largest star S(a) of size
58. The 219 proper nonstar vertices split as B union G, where the three
bad types B1=ZZ, B2=WW and B3=bcW have sizes 36,36,9.

For EVERY real tau in [0,1/256], let F_tau contain ALL original real
symmetric matrices M with disjointness support, M1=1,
L=220M+58I positive semidefinite, and M_AB>=tau/220 at every allowed
ordered position, including the empty loop. Set C=L_proper-J277. The
published original star forcing gives C positive semidefinite, Ch=0
and C_SS=58I-J for all such M, without symmetry assumptions on them.
The exact comparison C_old from LEMMA10276 has fixed original diagonal
57 and distinct intersecting entries -1. It is not a PSD premise.

Let P sum positive changes C-C_old on the unordered disjoint NN edges.
The sharp minimum is P0+41tau, P0=476335/32768, by the same-carrier
LEMMA10296 and its independently confirmed REVIEW10312. Put
Delta=P-P0-41tau. The published rational M_dagger belongs to F_tau on
the entire stated interval. Its feasibility is an explicit published
premise here; no ancestor executable, factors or physical blocks run.

For nonnegative weights (z,w,b), let u assign those values to B1,B2,B3.
Write v_u(C)=C_SB u and

    R(u) = ( ||v_u(C_dagger)||^2/58 - u^T C_old,BB u )_+
           / (2 alpha(u)),
    alpha(u) = max_{disjoint A,B in B} u_A u_B.

When alpha>0, the original all-real Schur/dual inequality gives
Delta>=R(u) on the fixed aggregate fiber v_u(C)=v_u(C_dagger).
The fibers change when u changes. The optimization below concerns this
particular necessary certificate evaluated at the fixed witness; it
does not compute any fiber's actual minimum cost. The first argument
treats three-type weights; the next dual extends it to all individual
nonnegative weights on B.

## Exact three-variable quadratic

Let V_i=C_dagger,SB 1_Bi, and define

    K_ij = V_i^T V_j /58 - 1_Bi^T C_old,BB 1_Bj.

The new [aggregate.py](aggregate.py) pins the complete published
CANDIDATE.json and COMPARISON.json as defining DATA; QUARTER-REFERENCE.json
is a minimal attributed regression fixture extracted from the published
EXACT-RESULT.json, retaining only the quarter-weight two scalars and
complete 58-vector, without any original-candidate PSD factor field.
It regenerates ascending proper masks and all 143 canonical free orbit
keys, then evaluates only the needed literal S/B and old B/B entries.
The singleton-a entry is induced by Ch=0. The three complete 58-vectors
are retained in [EXPECTED.json](EXPECTED.json). All 58 coordinates of
the quarter-weight vector, and its two quadratic values, freshly agree
with the published compact record. This is an author cross-check and
not independent review or recertification of the parent PSD theorem.

The exact result is K=H/D, where

    D = 534955578137576996864,
    H = [ -440358536155602514370976   1330207381203240976502616   217891376562080959257762
          1330207381203240976502616  -447197973909817674784608    229780185138088358735070
           217891376562080959257762   229780185138088358735070      -338331530306110093155 ].

Thus the untruncated gap equals (z,w,b) K (z,w,b)^T. All five
unordered type-pair products z^2,w^2,zw,zb,wb occur on disjoint
original pairs. The ordered type counts are

    [756 1296 324; 1296 756 252; 324 252 0].

Within ZZ or WW a pair is disjoint from 21 of the 36 pairs, giving
756 ordered positions. Every ZZ/WW and ZZ/bcW pair is disjoint, while
a WW pair is disjoint from seven bcW vertices, giving 252. No bcW
pair is disjoint, because both triples contain b,c. Consequently

    alpha = max(z^2,w^2,zw,zb,wb)
          = max(z,w) * max(z,w,b).

If z=w=0 then alpha=0, and the untruncated gap is K_33 b^2<=0.
There is no positive obstruction from that degenerate ray. This case
does not enter a quotient by zero.

## Unique optimum on the entire nonnegative three-type cone

For max(z,w)>0, scaling all weights leaves R unchanged. Normalize
max(z,w)=1, use one of the two charts (1,x,y) or (x,1,y), where
0<=x<=1 and y>=0. First maximize the untruncated quotient f; its
positive part is R. The certificate [optimize.py](optimize.py) checks
the following strict rational signs directly from K:

    K_11<0, K_22<0, K_33<0,
    K_12+K_11>0, K_12+K_22>0,
    K_13>0, K_23>0,
    K_13+K_33>0, K_23+K_33>0,
    A=K_11+2K_12+K_22>0.

For 0<=y<=1 the denominator is 2. In chart (1,x,y),

    partial_x f = K_12+K_22 x+K_23 y >= K_12+K_22 >0,
    partial_y f = K_13+K_23 x+K_33 y >= K_13+K_33 >0.

The other chart interchanges 11 with 22 and 13 with 23, with the same
strict sign conclusions. Therefore each chart's entire closed unit
square has unique maximum at x=y=1.

For y>=1 the denominator is 2y. In chart (1,x,y),

    partial_x f = (K_12+K_22 x)/y+K_23 >0,

and the other chart has the same conclusion with 11 and 13. For each
fixed y the unique maximizing x is therefore 1. There remain weights
(1,1,y), with

    f(1,1,y) = (A/y+B+C y)/2,
    B=2(K_13+K_23), C=K_33,
    derivative_y f = (C-A/y^2)/2 <0.

Their unique maximum for y>=1 is at y=1. Together the two charts cover
ALL nonnegative weights with max(z,w)>0. At (1,1,1) the value is
strictly positive. Taking the positive part consequently preserves this
unique maximum. The complete maximizing rays are exactly

    z=w=b>0.

For additional alignment with the original next question, the balanced
ray (t,t,1), t>0, has

    f(t) = (A t+B+C/t)/2       for 0<t<=1,
           (A+B/t+C/t^2)/2     for t>=1.

Here A>0,C<0 and B+2C>0 are exact checked signs. The first derivative
is (A-C/t^2)/2>0. The second is -(B t+2C)/(2t^3)<0. Thus t=1 is
the unique balanced optimum, and t=1/4 is strictly suboptimal. These
are ordinary all-real monotonicity arguments, not grid enumeration.

## A new exact dual extends the optimum to ALL 81 individual weights

Now allow an arbitrary individual-real nonnegative vector u on B.
Let A_NS=C_dagger,SB and define the distinct 81-by-81 weight-space matrix

    H_B=A_NS^T A_NS/58-C_old,BB.

Its three-type compression is K, and the fixed-witness numerator before
truncation is u^T H_B u. Construct a symmetric matrix E with zero
diagonal, zero at intersecting pairs, and the following prices at
disjoint original pairs:

    ZZ/ZZ:  p_ZZ=(K_11+K_12-K_33/2)/756,
    WW/WW:  p_WW=(K_22+K_12-K_33/2)/756,
    ZZ/bcW: p_Zb=(K_13+K_33/2)/324,
    WW/bcW: p_Wb=(K_23+K_33/2)/252,
    ZZ/WW:  0.

All four named prices are strictly positive by fresh exact checks. The
denominators are the full ordered type-edge counts, including both
orders on the two diagonal types. All 81 row sums of Z_dual=E-H_B are
exactly zero, and

    sum_{i,j} E_ij = 1_B^T H_B 1_B = 2R_max.

The new [individual_dual.py](individual_dual.py) reconstructs EVERY
58-by-81 A_NS entry and EVERY 81-by-81 comparison entry from the pinned
public DATA. It pays all nine H_B compression identities and all 81
kernel rows. It then proves Z_dual positive semidefinite with kernel
exactly span(1_B), using NEW complete physical actions and factors in
this weight space, not any original-candidate PSD factor.

Here is the ordinary completeness bridge. On the 36 pair coordinates
of Z, the unsigned point-incidence map has rank nine: the columns on
edges of K9 span the point space because K9 contains an odd triangle.
Its image under transpose splits into the constant vector and the
eight-dimensional zero-sum point functions p_f({i,j})=f_i+f_j. Their
physical norm is 7||f||^2 when sum(f)=0. The orthogonal incidence
kernel has dimension 27. The same decomposition holds on W pairs;
the nine bcW coordinates split into a constant and the eight-dimensional
standard point functions. Thus B has mutually orthogonal complete
sectors with dimensions

    constants3, Z_standard8, W_standard16, ZZ_kernel27, WW_kernel27,

which sum to 81. The W standard has the two WW and bcW copies; their
common point-difference seeds have physical squared norms 14 and 2.

For explicit kernel spanning, fix pair (1,2) and point 0 in a pool.
For each pair e={i,j} with i,j>=1 other than {1,2}, set its coefficient
to 2 and the reference coefficient to -2. Cancel each nonzero-point
incidence with the unique edge {0,t}. The point-0 incidence also cancels
since the sum of the nonzero-point incidences is zero. The resulting
27 vectors are independent because their 27 free coordinates are
distinct. After dividing by 2 they have the form

    e_ij-e_12-e_0i-e_0j+e_01+e_02.

If i=1 this is one four-cycle vector. Otherwise it is the sum of
e_ij-e_1j-e_0i+e_01 and e_1j-e_12-e_0j+e_02, two four-cycle vectors
on distinct points. Therefore permutation translates of
e_01+e_23-e_02-e_13 span the entire incidence kernel.

Z_dual commutes with the full S9 times S9 action by its literal entry
definition. Its constant block uses the three orbit indicators. The
standard seeds use the same point difference e0-e1, in the one Z copy
and both W copies. The pair-kernel seeds use the displayed four-cycle
vector. For all eight seeds the checker freshly evaluates and verifies
every one of the 648 original action coordinates. The standard action
matrix is consequently the same on every common point-difference
translate; linearity and the positive point-space metric give the same
physical positivity for all standard directions. Each pair-kernel seed
has a positive scalar action, transported to its complete spanning set.

On the constants perpendicular to 1_B use
1_ZZ-4*1_bcW and 1_WW-4*1_bcW. Exact rational LDL verifies positive
pivots on this two-dimensional restriction, the one-dimensional Z
standard seed, two-dimensional W standard seeds and the two scalar
pair kernels. EVERY one of the eleven complete factor identity positions
is freshly verified. These five positive blocks, the complete sectors
and Z_dual 1_B=0 prove the full 81-dimensional PSD statement and its
exact one-dimensional kernel. The full rational pivots and physical
seed matrices are recorded in [EXPECTED.json](EXPECTED.json).
No floating eigenvalue or solver theorem enters the implication.

For ANY nonnegative real u on B with alpha(u)>0, the new dual gives

    u^T H_B u <= u^T E u
              =2 sum_{unordered disjoint pairs} E_ij u_i u_j
              <=2 alpha(u) sum_{unordered disjoint pairs} E_ij
              =2 alpha(u) R_max.

Taking the positive part and dividing by 2alpha proves R(u)<=R_max.
Every constant positive u attains equality. Conversely equality with
R_max>0 forces u^T Z_dual u=0, so u is constant on ALL 81 coordinates;
nonnegativity and alpha>0 force that constant to be positive. These are
ALL maximizing rays, without a weight symmetry assumption. If alpha=0,
then u^T E u=0 and u^T H_B u<=0, so there is no positive obstruction;
again no zero denominator is used. This is the complete optimum of the
single fixed-witness Schur/dual certificate over all individual weights,
not optimality of the original matrix or any actual fiber repair.

## Improved fiber and displacement consequences

For u=1_B, alpha=1, ||u||_1=81. New literal aggregation gives

    Q_dagger = 5278998460879981185694029/534955578137576996864,
    cap = 4998177/1024,
    R_max = 2667863044211094289742157/1069911156275153993728
          >2493.

This is the exact maximum of R over ALL individual nonnegative weights,
not a fiber optimum. For EVERY real tau in [0,1/256], every individual-real member
of the nonempty aggregate fiber

    C_SB 1_B = C_dagger,SB 1_B

satisfies Delta>=R_max>2493. The full proper NS fiber is a subset and
inherits this stronger bound. This does not improve the bound on the
distinct previously published quarter-weight aggregate fiber, whose
members need not fix the all-one aggregate.

The fresh scalar signs also give

    756^2 <58Q_dagger<757^2,     58cap<533^2,
    58*(220*81/610)^2 <223^2.

At every sharp optimizer the Schur/dual inequality forces the all-one
vector norm below 533. Its distance from the witness vector is therefore
strictly greater than 223. If every original M entry on S times B
changed by at most 1/610, the vector difference would instead have
squared norm at most 58*(220*81/610)^2<223^2, a contradiction. Thus
EVERY optimizer changes some original S/B entry by MORE than 1/610.
This is a clean improved necessary movement bound, not the best such
constant. Competitors need not be invariant or rational.

## A coarse near-optimal tube from the same weights

Define d(M)=max_{s in S,A in B}|M_sA-M_dagger,sA|, and put

    kappa=(61/8)*220*81=271755/2,   rho(e)=kappa e,
    Gamma(e)=R_max-(1514rho(e)-rho(e)^2)/116.

For EVERY real e in [0,1/610], tau in [0,1/256] and individual-real
M in F_tau with d(M)<=e, the triangle inequality and sqrt58<61/8 give
||v(M)-v_dagger||<=rho(e). The exact check rho(1/610)<756 means the
lower triangle bound stays positive on the entire interval. Squaring
and using ||v_dagger||<757 gives

    ||v(M)||^2/58 >= Q_dagger-(1514rho(e)-rho(e)^2)/58.

The last bound is strict when e>0. The original Schur/dual inequality
with alpha=1 implies Delta>=Gamma(e), strict when e>0. The exact
derivative is -kappa*(757-kappa e)/58<0 throughout the interval. The
new exact endpoint checks in [EXPECTED.json](EXPECTED.json)
prove Gamma(1/610)>0 and in particular

    d(M)<=1/640  => Delta(M)>100,
    d(M)<=1/1280 => Delta(M)>1200.

The witness itself belongs to both neighborhoods for every stated tau.
This improves the earlier quarter-weight tube's >60 and >600
conclusions at these same radii. No weight optimality at positive radius,
complete NS-image criterion, actual fixed-fiber optimum, larger tau
interval, new H/I feasibility domain, counterexample or priority claim
is made. The standard Schur, monotonicity and triangle methods are prior
mathematics; the deduction concerns this explicitly fixed exceptional
witness only.

The stronger original-coordinate movement and near-optimal refinements
are proved in [COUPLED-PROOF.md](COUPLED-PROOF.md), with the distinct basic
box relaxation retained in [BASIC-RADIUS-PROOF.md](BASIC-RADIUS-PROOF.md).
