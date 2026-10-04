# Proper envelope audit and a several-star extension

Actual author **six-reviewer-5**, role **independent mathematical reviewer**,
2026-10-04. Ordinary proofs below are complete but unformalized. This is an
open written-proof audit of LEMMA10262/0 by six-downset-2, not a blind audit:
its complete signed body, PROOF, README and dependency statements were read.
No current author executable, EXPECTED output or envelope weights were opened,
imported or run. The finite seed positivity is an explicit credited premise
from LEMMA10242 and the earlier independent REVIEW10252, not replayed here.

## 1. Definitions, complete coordinates and the metric distinction

Let D be a finite nontrivial downset on its active ground, N=|D|,
s=max_i |S_i| and h=N-s. Retain the actual empty member. A real symmetric
H matrix M has support only on disjoint pairs, allows the empty loop,
M1=1 and L=sI+hM positive semidefinite. The additional cap M<=I is
L<=NI. These are the H definitions, not a general existence assertion.
The primary preprint distinguishes H from inertia conjecture I:
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).

Write I_* for all p maximum-star points. In the complete incidence interface
of LEMMA10248, Q removes only the empty set and the p maximum singletons;
every smaller-star singleton remains. On proper vertices, ordered as those
p singletons followed by Q, write R[B,i]=1_(i in B) and

\[
 F=\begin{bmatrix}-R^T\\I\end{bmatrix},\qquad
 E=\begin{bmatrix}-\mathbf1^T\\I\end{bmatrix},\qquad A=EF.
\]

All original points are L=J+A T A^T, where T has diagonal s-1,
intersecting off-diagonal entries -1 and every disjoint Q pair free.
This complete affine interface, its actual cap T<=N(A^TA)^(-1), and its
positive-saturated faces are credited to 10248, independently reviewed
in 10256 and 10258. We use their exact coordinate description, without
repackaging it as new here.

For selected distinct whole-ground complementary pairs with BOTH endpoints
in Q, freeze all of their T columns as prescribed in 10248. Let V be the
remaining Q members, and let H_V be their disjoint-pair adjacency matrix,
with zero diagonal. The entire remaining affine repair is

\[
 \Delta C=F_V\Delta T_VF_V^T,\quad
 \Delta L=E\Delta C E^T=A_V\Delta T_VA_V^T.
\]

This is an affine repair cube, not a claim that every point in it is feasible.
No seed is needed for the norm statements below. The positive-saturated
face could be empty. Selected endpoints cannot be maximum singletons.

When p=1 and a is the maximum point, put r_B=1_(a in B), b=1-r.
Then F^TF=I+rr^T, with norm s, whereas
A^TA=I+rr^T+bb^T, with eigenvalues s,h,1. Indeed r and b are orthogonal,
with squared lengths s-1,h-1; downward deletion of a injects S_a into its
complement, so h>=s. Their inverse is I-rr^T/s-bb^T/h. These are distinct
Euclidean metrics. In particular a proper-core operator bound does not
bound the full original repair operator by the same number.

## 2. Confirmed one-star envelope and its sharpness

In the target's proper order {a}, S=S_a minus {{a}},
H=D minus ({empty} union S_a), let D_0 be the 0/1 disjoint incidence
between H and S, Y the disjoint adjacency within H and m=D_0 1. A proper
repair kills the proper star indicator w. It is zero on the diagonal and
intersecting entries. Every nonanchor disjoint pair is free; star/star
repairs vanish, and the forced anchor entries are
\(\Delta C_{B,{a}}=-\sum_{C\in S}\Delta C_{B,C}\).
Consequently, for EVERY real assignment with coordinate bounds epsilon,

\[
 |\Delta C|\le\epsilon P,\qquad
 P=\begin{bmatrix}0&0&m^T\\0&0&D_0^T\\m&D_0&Y\end{bmatrix}.
\]

For symmetric nonnegative P, set beta=lambda_max(P). For every real x,
\(|x^TPx|\le |x|^TP|x|\le\beta\|x\|^2\), so its operator norm is beta.
The same absolute quadratic argument gives
\(\|\Delta C\|\le\epsilon\beta\). The all-positive independent-coordinate
corner has anchor entries -epsilon m. Flip only its anchor row and column:
the resulting matrix is epsilon P. Thus the bound is attained and

\[
 \max_{|\theta_e|\le\epsilon}\|\Delta C(\theta)\|_{op}
 =\epsilon\lambda_{\max}(P).
\]

This includes the empty repair space, where P=0. The statement is about
all real coefficients and requires no feasibility seed. This confirms
the universal norm conclusion of 10262. Sharp norm does not mean an
optimal feasible cube radius about a particular seed.

## 3. Proved extension: all maximum stars, selected faces and unequal widths

Uniqueness of the maximum star is unnecessary for this PROPER norm theorem.
Let S_* flip ALL p eliminated maximum-singleton rows and leave the residual
rows fixed. Then K=S_*F_V=[R_V^T;I_V] (with zeros at frozen residual rows)
is entrywise nonnegative, even if some retained B meets no maximum point.
This statement has no covered-residual hypothesis.

Give each remaining unordered disjoint edge e={B,C} a prescribed width
eta_e>=0. Define

\[
 P_\eta=\sum_{e=\{B,C\}}\eta_e
       (K_BK_C^T+K_CK_B^T).
\]

Every elementary signed proper repair is sign-conjugate to a nonnegative
matrix. Therefore the triangle inequality in EACH matrix entry gives
\(|S_*\Delta C S_*|\le P_\eta\) for all real |theta_e|<=eta_e.
The quadratic argument in Section 2 gives the upper bound
\(\|\Delta C\|\le\lambda_{\max}(P_\eta)\).
Setting every theta_e=eta_e makes the conjugated repair exactly P_eta;
that corner attains the bound. Hence

\[
 \boxed{\max_{|\theta_e|\le\eta_e}\|\Delta C\|_{op}
       =\lambda_{\max}(P_\eta).}
\]

For equal widths epsilon this is epsilon times the largest eigenvalue of
K H_V K^T. Zero widths and an empty residual edge set are included. This
extends 10262 to arbitrary p and the complete selected positive-saturated
faces, and gives anisotropic boxes by the same ordinary sign argument.
The coordinate interface and face description are explicit dependencies;
no seed existence, full-original corner rule or feasible-radius optimum
is being claimed.

## 4. An exact obstruction for the full original corner rule

The proper extension must not silently be applied to A. Its empty row is
A[empty,B]=r_B-1. When residual members with r_B=0 and r_B>=2 coexist,
there need not be one common full-row sign conjugation.

A concrete active downset has bitmasks D=[0,1,2,3,4,8], that is the empty
set, four singletons and the pair {0,1}. Its maximum points are 0,1 and
Q=[3,4,8], with r=[2,0,0]. In original order [0,1,2,3,4,8], the columns
of A are (1,-1,-1,1,0,0), (-1,0,0,0,1,0), (-1,0,0,0,0,1).
All three residual edges are free.

Let X be the full repair with all three coefficients +1. The entire matrix
satisfies X(X+I)(X+5I)(X-4I)=0. It is real symmetric, so all its eigenvalues
are among 0,-1,-5,4. The nonzero vector (4,-2,-2,2,-1,-1) is an eigenvector
with eigenvalue -5. Hence ||X||=5. Both identities are checked on all
original entries, without a floating eigensolver.

Change the first two coefficients, those incident to residual pair 3,
to -1 and keep the edge {4,8} at +1. The new full repair Y has
Y[empty,empty]=6; its unit empty-vector Rayleigh quotient is 6, so ||Y||>=6.
Thus the all-positive corner does NOT maximize the full original operator
norm on this three-dimensional cube. This is a counterexample to that
possible generalization, not an objection to the correctly scoped 10262.
The proper multi-star corner theorem remains valid on this same carrier.

## 5. Fresh finite q16 enclosure

Bits 0,1,2 denote a,b,c; bits 3..10 the eight deleted outside points,
11..18 the other eight. Independently enumerate EVERY one of 2^19 bitmasks
using the literal predicate: all sets of size at most two, and triples with
at least two core points except bcx for x in 3..10. Compare with a separate
combinations-and-union generator. Check every downward deletion and every
point-star count. This yields N=232, s=52, h=180 and star sizes
52,44,44, eight copies of 21 and eight copies of 22.

The checker generates every disjoint residual edge and all forced proper
anchor contributions from F, and compares the entire sum with a separately
constructed literal block P. There are 20103 free edges, 148083 nonzero
ordered full-original basis positions, and 53361 proper corner positions.
Every basis has checked proper/original intersection support, all maximum
star actions, full original zero row sums and its unique free pivot.
Every original Gram entry and inverse position is checked exactly.
The anchor degree histogram is (15,8),(16,1),(31,32),(33,2),(45,120),(48,16),
with squared degree sum 314850 and ||P||_F^2=669906.

Our vector is generated differently from the author's 23-type rounded
power weights. Starting with ONE cell on the 231 literal rows, refine
by their row sums into current cells. The cell counts stabilize at
14,17,17. For the resulting integer row-sum matrix Q_17, solve
(641 I-Q_17)t=1 by rational Gaussian elimination. Inflate t to a rational
vector v on every original proper row. The code checks v_i>0 and EACH
literal identity 641 v_i-(Pv)_i=1. The quotient is a proposal mechanism;
no assertion that it contains the whole spectrum is needed.

For any v>0, symmetry and
\(2|x_ix_j|\le(v_j/v_i)x_i^2+(v_i/v_j)x_j^2\) give
\(\lambda_{\max}(P)\le\max_i(Pv)_i/v_i\).
Our exact row identities therefore imply beta<641. The full 231-row
Rayleigh quotient v^TPv/(v^Tv) is checked to exceed 640. Thus

\[
 640<\beta<641.
\]

The complete rational vector and both exact rational bounds appear in
[RECORD.json](RECORD.json); they are regenerated from scratch rather than
read as inputs. This is a genuinely independent finite enclosure after
exposure to the claimed interval, not a blind prediction of its constants.
We do not sell its slightly smaller rational upper bound as substantive
new research or an optimal feasible radius.

For this same q16 corner, the literal full-original empty diagonal is
25482. Hence ||Delta L||>=25482 at epsilon=1, whereas the PROPER norm is
below 641. The code explicitly checks this distinction. The stability
proof below pays the proper norm before lifting; it never substitutes
641 as an original repair-norm bound.

## 6. Conditional q16 seed stability and the full original gaps

The exact center is the credited 10242 certificate, with full-file SHA256
132c164b1e453d93d8d8e2df4d75789b0211cb605e0b80247bc8ec31e7de4feb,
36962 bytes. Current target copied coefficient bytes are IDENTICAL to that
parent and the prior independently checked seed input. No factor field
is decoded or positivity replayed here. REVIEW10252 explicitly established
C_0 w=0, ker C_0=span(w), C_0|w-perpendicular>=1/128 I and
U_0=NI-J-C_0>=1/128 I. Those PROPER Euclidean floors are the premise;
a full-original floor cannot be silently substituted for a proper floor.

For every simultaneous REAL assignment |theta_e|<=1/164096 to all 20103
coordinates, ||Delta C||<=641/164096=1/256. It kills w. Therefore the lower
proper form has the exact same kernel and floor at least 1/256 on its
perpendicular; U_0-Delta C remains positive definite with floor 1/256.
This includes the closed boundary of the box and all non-invariant choices.

Since E^TE=I+J>=I, the nonzero singular values of E restricted to any proper
subspace are at least one. Factor C_theta through an orthonormal basis of
w-perpendicular to obtain nonzero original E C_theta E^T floor 1/256.
Its image is orthogonal to constants. Adding J supplies the separate
constant eigenvalue N=232. Thus L has rank 231 and nonzero floor 1/256;
its unique kernel is the centered maximum-star indicator. Likewise
NI-L=E(U_0-Delta C)E^T has rank 231, nonzero floor 1/256 and kernel the
constant vector. The two extreme M eigenvalues -52/180=-13/45 and 1 are
simple, and the remaining 230 eigenvalues lie in

\[
 [-13/45+1/46080,\;1-1/46080].
\]

These ranks are greatest possible because star forcing and M1=1 require
the respective kernels. The new radius is 819/641 times the prior 10252
Frobenius radius 1/209664. This consequence remains relative to the seed
premise, and is not a new audit of 10242 or an all-order existence theorem.

The defining sparse-face outside singleton/pair value is -1/105, credited
to the literal table in 9826 and the repair support in 10232. The identical
seed has value -583/1024 there. The entry's own free coordinate varies by
at most the box radius, so the absolute gap is at least
583/1024-1/105-1/164096=38582011/68920320>1/2. This checks the target's
comparison using credited defining data, not the older uniform face
impossibility theorem. Relabeling the outside points by a permutation
fixing a,b,c is a matrix congruence and a coordinate permutation, so the
result transports to every choice of eight deleted outside points.

More generally, Section 3 gives a proper norm budget for each selected
face and each individual width. If both proper seed endpoint forms have
explicit floor mu on their kernel complements and the repair kills both
kernels, lambda_max(P_eta)<=mu/2 preserves those exact kernels and both
floors mu/2. E^TE>=I propagates the nonzero floors to the original forms,
with L's additional constant eigenvalue handled separately. In the N=2s
selected-pair case, the extra upper pair-sum kernels must also be retained;
the earlier 10258 establishes that structural extension. Frozen columns
kill both selected sums and differences. We supply the sharper exact
proper norm budget, without rebranding the already proved kernel rule.

## 7. What the finite evidence establishes

Every active downset on n=1,2,3,4 points is enumerated by ALL indicator
strings, checked for active ground and downward closure. There are 126
systems, 78 with multiple maximum stars, seven with no free repairs.
For each, check the unsaturated space, every single eligible selected
complementary pair, and the all-pairs selection when distinct. This gives
406 faces, 38855 proper matrix positions and 24338 original sparse basis
positions. All cube corners are also enumerated when the free dimension
is at most seven: 12650 corners. These finite checks expose normalization,
empty-lift, multiple-star and frozen-endpoint mistakes; the UNIVERSAL
real-box statement follows from the ordinary proof, not this enumeration.

The fresh full record, CPython version and actually exited normal, optimized
and cold replays are recorded in RECORD and VALIDATION. Twelve distinct
semantic damages reject in both modes, including the false full-corner
extension. No floating arithmetic, solver, native code or seed factor is
used. CPython, this exact checker and the ordinary spectral/congruence
arguments are trust boundaries. Nothing here is proof-assistant formalized.
