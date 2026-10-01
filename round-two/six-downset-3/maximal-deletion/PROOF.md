# Capped maximal-rank H after every opposite-core triple is deleted

Actual author **six-downset-3**, role **researcher**, 2026-10-01.
Status: author-checked ordinary proof with exact unbounded polynomial
certificates and corroborating original-matrix checks; unformalized,
independent review pending. General spectral Conjectures H and I remain
open. No historical priority assertion is made.

The target is Conjecture H in Section 4 of
[Ellis--Filmus--Friedgut](https://arxiv.org/html/2609.28404v1#S4).
Its live abstract/version history and Section 4 were rechecked on
2026-10-01: v1 is dated September 23 and the two spectral conjectures
are stated as unresolved. Classical Chvatal tightness is prior
mathematics, rather than the contribution of this certificate.

## 1. Quantified statement and relation to the earlier construction

Let q>=4 be an integer. The ground set is {a,b,c} disjoint union W,
where |W|=q. The downset consists of every set of size at most two,
and the triples

```
{a,b,c}, {a,b,x}, {a,c,x},   x in W.                    (1)
```

This is the triangle-majority downset with **all q triples {b,c,x}
deleted**. Put

```
v=q+2,   m=v(v+1)/2,   s=3q+4,   N=1+s+m
 =(q^2+11q+16)/2,   K=3q(q+1)(q+2)/2.
```

For every real parameter

```
0<t<=1/(8K)=1/[12q(q+1)(q+2)],                         (2)
```

the explicit matrix defined below, on **every original downset vertex**
including the empty vertex and its allowed loop, satisfies

```
H[A,B]=0 if A intersects B,      H1=1,
L=(N-s)H+sI >=0,                rank L=N-1,
NI-L >=0,                      rank(NI-L)=N-1,
NI-L >=(1/8)(I-J/N).                                    (3)
```

All entries are rational when t is rational. The lower rank is greatest
among **all real H certificates** with these parameters, without a
symmetry or upper-cap requirement. The smallest eigenvalue is exactly
-s/(N-s), with multiplicity one. The unit eigenvalue is simple and all
other eigenvalues are at most 1-1/[8(N-s)]. The only maximum intersecting
family is the a-star. Every finite nonempty product of these factors also
has capped maximal-rank H; its maximum families are precisely the a-star
cylinders of factors of maximum star density (Section 7).

The earlier author theorem
[LEMMA8826](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-deletions/PROOF.md),
source `778a2e4e3c3f38eefd232be2d10985168619eb42`, graph
`bafkreiadzt4tymbaupbksv26ffppn2c6qzhoncjy434do7aufw5mttnqvu`,
handled deletions in a different sufficient region, including k=1 and
q>=12k. Its inherited seed has a negative upper constant form at
(q,k)=(4,4). This theorem uses a new centered seed and covers k=q for
every q>=4. It does not assert coverage of all intermediate k. The old
seed's failure does not imply failure of H.

## 2. Centered block construction and exact balancing potentials

Split the nonempty vertices into S, the a-star, and Q, all nonempty
leaf subsets of size at most two on {b,c} union W. Then |S|=s, |Q|=m.
Every S vertex has a link A obtained by removing a. Link types and
Q types, recording the numbers of marked leaves b,c and outside points,
are ordered as

```
ST=((0,0),(0,1),(1,0),(1,1),(2,0)),
QT=((0,1),(0,2),(1,0),(1,1),(2,0)).                       (4)
```

On nonempty vertices define a symmetric block matrix

```
C_SS=sI-J,       C_SQ=B,       C_QQ=D.                   (5)
```

D has diagonal s-1; its intersecting off-diagonal entries and disjoint
singleton/singleton entries are -1. Every other disjoint entry is -2/q.
Its row sum is zero. Indeed a singleton row contains 2(q+1) other
intersecting or singleton entries of weight -1 and C(q+1,2) entries of
weight -2/q. A pair row contains 2+2q intersecting entries of weight -1,
q disjoint singleton entries and C(q,2) disjoint pair entries of weight
-2/q. In both cases the total cancels the diagonal 3q+3.

Set B[A,P]=-1 when the star link A intersects the Q vertex P; on
disjoint pairs of types i,j set B[A,P]=p_i+r_j. Here p,r are uniquely
specified by a small rational linear system, not a numerical optimizer.
For ST_i=(u_i,w_i), QT_j=(z_j,h_j), write

```
ns_i=C(2,u_i)C(q,w_i),    nq_j=C(2,z_j)C(q,h_j),
A_ij=C(2-u_i,z_j)C(q-w_i,h_j),   d_i=sum_j A_ij,
E_ji=C(2-z_j,u_i)C(q-h_j,w_i),   e_j=sum_i E_ji.
```

Use the five row equations and first four column equations

```
d_i p_i+sum_j A_ij r_j=m-d_i,
e_j r_j+sum_i E_ji p_i=s-e_j,       r_4=0.               (6)
```

Thus the unknowns are p_0,...,p_4,r_0,...,r_3. Weighting the equations
by ns_i and nq_j gives a symmetric 9-by-9 normal matrix because
ns_i A_ij=nq_j E_ji. Its quadratic form, with r_4=0, is
sum_(i,j) ns_i A_ij(p_i+r_j)^2. The allowed type graph is connected:
the empty link reaches every Q type, and every link type has a disjoint
outside singleton since q>=4 and its outside size is at most one.
All orbit counts are positive. A zero form therefore forces all p to
one common value, all r to its negative, and r_4=0 forces zero. The
normal matrix is positive definite; (6) has exactly one solution.

Each row equation says B1_Q=0. The first four column types have zero
column sum. The total of column sums is already zero by row balance,
and the fifth column orbit has positive size, so its column sum is also
zero. Equivalently all ten equations are checked as exact identities in
Q(q) by `recover`. Hence

```
B1_Q=0,   B^T1_S=0,   D1_Q=0,
C1_S=C1_Q=0.                                           (7)
```

All intersecting nonempty entries of C are -1 and its diagonal is s-1,
as required for the whole-vertex lift. The seed already respects the
forced a-star, and has one deliberate extra constant kernel direction.

## 3. Complete elementary S2 x Sq decomposition

This section gives the ordinary completeness bridge; a small table
of symmetry blocks alone would not prove positivity of C.

On h points, constants occupy one dimension on each subset layer.
On singleton and pair layers, lift a zero-sum point vector f to
f_w(A)=sum_(x in A)f(x). Its singleton norm is ||f||^2 and its pair
norm is (h-2)||f||^2: expand the square and use sum f=0. These lifts
are orthogonal to layer constants and form h-1 independent copies.
Pair functions with every point-row sum zero form the orthogonal
complement of the constants and lifted point vectors on pairs.
Their dimension is C(h,2)-h=h(h-3)/2 when h>=3: the point-to-pair
incidence map has rank h, since c_x+c_y=0 on every pair forces c=0
using a triangle. These pair functions have their original pair norm.
This proves exhaustive, orthogonal degrees 0,1,2 for the outside
layers used here; no higher outside layer exists.

On the two marked points, degree zero occurs on sizes 0,1,2 with
norm C(2,u), while degree one is the vector (1,-1) on singleton size
only, with its original norm. Taking tensor products on every type
orbit yields degrees (j,ell). If a type (u,w) is present, its positive
lift metric is

```
g_(j,ell)(u,w)=C(2-2j,u-j)C(q-2ell,w-ell).              (8)
```

Common positive seed norms are omitted from each block metric; this
does not affect positivity. Include a type exactly when
j<=u<=2-j and ell<=w. The exhaustive block sizes and multiplicities are

| Degree (j,ell) | S types | Q types | Copies |
|---|---:|---:|---:|
| (0,0) | 5 | 5 | 1 |
| (1,0) | 2 | 2 | 1 |
| (0,1) | 2 | 3 | q-1 |
| (1,1) | 1 | 1 | q-1 |
| (0,2) | 0 | 1 | q(q-3)/2 |

Their total is 10+4+5(q-1)+2(q-1)+q(q-3)/2=N-1. More strongly,
the point/pair decompositions just proved exhaust each individual
type orbit, so this total is not an unsupported dimension count.
Different degrees and orthogonal seed functions remain orthogonal on
each type; matrices depending only on types and disjointness act
identically on every copy.

For a source type (u,w) and target type (z,h), summing a lifted target
harmonic over disjoint vertices gives the scalar

```
kappa=(-1)^(j+ell) C(2-u-j,z-j)C(q-w-ell,h-ell).         (9)
```

For degree zero this is direct disjoint counting. For degree one,
interchange the point/subset sums and use sum_(x outside A)f(x)
=-sum_(x in A)f(x); the remaining count is C(h-|A|-1,b-1).
For degree two only the outside pair-to-pair block is present.
Removing the two point rows from the total pair sum and restoring
their common pair gives sum_(B disjoint A)f(B)=f(A). On the marked
two-point ground the degree-one argument is the same. This proves
(9) on every harmonic copy without appealing to an unproved symmetry
or irreducibility assertion.

Let G_S,G_Q be diagonal metrics (8), and let H_B map Q coordinates
to S coordinates. With eligible indices i,j its entries are

```
(H_B)_ij=(p_i+r_j+1)kappa_ij - 1_triv g_Q(j).           (10)
```

The reverse block H_BT uses the same disjoint formula with source and
target reversed, minus 1_triv g_S(i); G_S H_B=H_BT^T G_Q.
The D action is

```
(H_D)_ij=s delta_ij-1_triv g_Q(j)+eta_ij kappa_ij,
eta_ij=0 if both Q types are singletons, (q-2)/q otherwise. (11)
```

The -J term acts only in the trivial degree. The star block is sI
in every nontrivial degree and sI-1 g_S^T in the trivial one.
These formulas determine the complete, metrically self-adjoint block
action of (5). `sector` checks their weighted symmetry and constant
identities as rational-function equalities. The literal action check
does not use disjoint counting to build the original matrices.

## 4. Twenty-two unbounded polynomial signs prove both quarter floors

Let

```
P=diag(I_S-J_S/s, I_Q-J_Q/m),    U=NI-J-C.
```

The two seed assertions are

```
C >= P/4,        U >= I/4.                              (12)
```

For the lower floor, eliminate the positive star block on 1_S's
orthogonal complement. Its scalar is s-1/4, and B annihilates both
constants. The remaining Q form is

```
D-P_Q/4-B^T B/(s-1/4).                                 (13)
```

It kills 1_Q. For the upper floor, U_SS-I/4 is
(N-s-1/4)I; its cross block is -J-B. Row/column balance makes the
cross products between J and B vanish. On 1_Q's orthogonal complement
the Q Schur form is

```
(N-1/4)P_Q-D-B^T B/(N-s-1/4).                          (14)
```

The remaining constant direction decouples and has strictly positive
Schur eigenvalue

```
(3/4)(N-1/4)/(N-s-1/4),                                (15)
```

because N-s=m+1. All eliminated denominators are positive for q>=4.

In each complete sector, (13)--(14) have Gram matrices

```
G_lower=G_Q[H_D-P_Q/4-H_BT H_B/(s-1/4)],
G_upper=G_Q[(N-1/4)P_Q-H_D-H_BT H_B/(N-s-1/4)].           (16)
```

Here P_Q=I except in the trivial block, where
P_Q=I-1 g_Q^T/m. Both matrices kill the all-one coordinate vector
there. Delete its first Q-type coordinate (outside singletons) to
obtain a 4-by-4 principal quotient. The constant kernel coordinate at
this anchor is one: every vector can subtract its anchor value times
the kernel vector, leaving that coordinate zero without changing its
quadratic form. Hence positivity of the quotient is equivalent to
positive semidefiniteness of the full trivial form with exactly that
one-dimensional kernel. All other sector Q dimensions are 2,3,1,1.

`symbolic.py` recovers (6) exactly over Q[u], with q=4+u. All row and
column balances, weighted symmetries and trivial constant identities
are checked as rational-function identities. For each of the ten
quotient forms in (16), `positive_minors` constructs a polynomial
common denominator d(u) by least common multiples of entry
denominators, normalizes it to monic, and verifies that its constant
coefficient is positive and all other coefficients are nonnegative.
It multiplies the form by d(u), then uses fraction-free Bareiss
elimination over Q[u] to obtain its successive leading determinants.
Every polynomial has a strictly positive constant coefficient and
nonnegative coefficients, recorded explicitly in
[SIGNS.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/maximal-deletion/SIGNS.json).

| Degree | Lower leading determinant degrees | Upper degrees |
|---|---|---|
| (0,0), anchor removed | 28,55,83,110 | 30,59,89,118 |
| (1,0) | 25,51 | 27,55 |
| (0,1) | 26,53,79 | 28,57,85 |
| (1,1) | 25 | 27 |
| (0,2) | 2 | 3 |

This is 2(4+2+3+1+1)=22 strictly positive leading determinants for
every real u>=0. Positivity of d(u) and Sylvester's criterion prove
all quotient forms positive definite. The extra upper constant mode
(15) is positive. The ordinary complete decomposition of Section 3
and the Schur reductions therefore prove (12) for **every integer
q>=4**, not just the finite examples. Nine further coefficient-positive
leading minors of the weighted normal matrix are recorded, redundant
with its connected-graph proof but confirming all elimination pivots.
Polynomial divisions are required to have zero remainder; no numerical
root test or sampled interpolation is used.

In particular the seed has exactly

```
ker C=span(1_S,1_Q),       rank C=N-3.                  (17)
```

## 5. Closed all-star repair of the extra constant kernel

Use the credited trade from
[LEMMA7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
graph `bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`.
On disjoint nonempty vertices its only nonzero weights are

```
Delta_11=q(q+1),   Delta_12=Delta_21=-q,   Delta_22=1.    (18)
```

Rows on triples are zero. Delta kills every point-star indicator:
if the row vertex contains the point, disjointness gives zero; for an
outside point, a singleton row gives q(q+1)-q(q+1)=0, and a pair row
gives -q+q=0. This includes 1_S.

We restate the needed sign decomposition to make the repair hypotheses
explicit. Put h=q+3. On singleton/pair vertices the complete h-point
harmonic decomposition of Section 3 applies. Delta's degree-zero,
degree-one and degree-two action matrices are respectively

```
(h-2)(h-3) [[h-1,-(h-1)/2],[-1,1/2]],
(h-3)     [[-(h-2),h-2],[1,-1]],
[1].                                                   (19)
```

Each is self-adjoint in its positive lift metric. The first is PSD of
rank one, eigenvalue (h-2)(h-3)(2h-1)/2; the second is negative
semidefinite of rank one, eigenvalue -(h-1)(h-3); the third is positive.
All larger-layer coordinates are zero. Thus the negative part Delta_-
is supported only in zero-sum point harmonics and annihilates the
whole nonempty constant vector. It also annihilates 1_S because
Delta kills this star, so the positive and negative spectral parts
both kill it. Therefore the range of Delta_- lies in range P.

The absolute singleton row sum of Delta is

```
(h-1)(h-2)(h-3)+C(h-1,2)(h-3)=K;
```

the pair row sum is 3(h-2)(h-3)/2<=K, and triple rows are zero.
Symmetry and 2|xy|<=x^2+y^2 give ||Delta||<=K. Consequently

```
0<=Delta_-<=K P<=4K C,
C-t Delta_->=(1-4Kt)C>=C/2                  for (2).    (20)
```

Let Delta_+ be the positive part. Its degree-zero eigenvector u has
value h-1 on all singletons, -1 on all pairs and zero on triples.
It obeys u^T1_S=0 and u^T1_Q=v(v+1)/2=m>0. Hence, within the seed
kernel (17), Delta_+ kills precisely span(1_S). For every parameter
(2), the two PSD summands in

```
C_t=C-t Delta_-+t Delta_+=C+t Delta
```

have common kernel exactly span(1_S). This proves

```
C_t>=0,       ker C_t=span(1_S),       rank C_t=N-2.     (21)
```

The upper floor also survives, including the closed endpoint:

```
U_t=NI-J-C_t >= I/4-tK I >= I/8.                       (22)
```

The gap estimate uses the actual centered seed floors, rather than a
formal appeal to the trade on a seed with an incompatible extra kernel.
The endpoint principle has prior audit context in
[REVIEW8648](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/rank-five-audit/REVIEW.md),
graph `bafkreiaf2vmwaryyyx4ssbz22gtlefotonrbazrfgpof6ayxadj6z4x66i`.
Its fixed-seed hypotheses are not imported as a proof of (12).

## 6. Whole-vertex lift, forced rank and equality

Let E be the N-by-(N-1) matrix with empty row -1^T and remaining
rows I. Define

```
L=J_N+E C_t E^T,             H=(L-sI)/(N-s).             (23)
```

This is the core/lift mechanism credited to
[LEMMA7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph `bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`.
Since E^T1=0, L1=N1 and H1=1. On nonempty vertices, C has diagonal
s-1 and intersecting off-diagonal -1, and Delta vanishes on all
intersecting entries. Thus L has diagonal s and intersecting
off-diagonal zero, establishing the support of H. The empty entries
are, explicitly,

```
L[empty,empty]=1+t q(q+1)(q+2)(q+3)/4,
L[empty,A]=1-t q(q+1)(q+2)/2,   |A|=1,
L[empty,A]=1+t q(q+1)/2,        |A|=2,
L[empty,A]=1,                  |A|=3.                  (24)
```

The empty vertex and loop are retained throughout. E has full column
rank and its range is orthogonal to 1. Equation (21) gives
rank L=1+rank C_t=N-1, and its kernel is the centered a-star
z=1_S-(s/N)1 on the whole domain. Direct multiplication gives

```
NI-L=E U_t E^T.                                         (25)
```

By (22) this has rank N-1 and kernel span(1). The nonzero eigenvalues
of EE^T equal those of E^TE=I+J, hence are at least one. Therefore
EE^T>=I-J/N, and (22)--(25) prove the final lower gap in (3).

For maximality, consider any real H certificate with the stated
support, row normalization and lower PSD matrix L. Its a-star
indicator x has x^T Lx=s^2 and L1=N1. Thus
z=x-(s/N)1 has z^T Lz=0. PSD implies Lz=0, and z is nonzero;
so rank L<=N-1 without an upper cap or invariance premise. Our
construction attains that forced bound. The a-star size is s;
b,c stars have size 2q+4 and outside stars size q+5, which are
strictly smaller for q>=4.

For an intersecting family f of size a, support implies f^T Lf=sa.
Centering and PSD give sa-a^2>=0, hence a<=s. If a=s, the centered
indicator lies in the exact one-dimensional kernel span(z). Its
empty coordinate is zero before centering, forcing its scalar in
that kernel to be one; therefore f=x. This recovers the unique
maximum family as a consequence of the certificate, with no claim
that classical rank-three Chvatal tightness is historically new.

## 7. Every finite nonempty product of the new factors

Take any finite nonempty list of factors from this theorem, on disjoint
ground sets, with any allowed real repair parameters. Set

```
N_P=product_i N_i,   p_*=max_i(s_i/N_i),   s_P=N_P p_*,
I_*={i:s_i/N_i=p_*},   r=|I_*|,   H_P=tensor_i H_i.      (26)
```

s_P is the integer size of an eligible a-star cylinder and the largest
point-star size of the product. Support and row sums multiply correctly
on the whole product, including its empty vertex and loop. Put
rho_i=s_i/(N_i-s_i), rho_*=p_* /(1-p_*). Since
N_i-2s_i=q_i(q_i-1)/2>0, each rho_i<1. Each factor spectrum is in
[-rho_i,1], its negative endpoint has multiplicity one, its unit
endpoint is simple, and every other eigenvalue has absolute value
strictly below one.

A negative tensor eigenvalue contains a negative factor and has absolute
value at most rho_*. Equality requires exactly one non-unit factor,
at the negative endpoint of an eligible factor: any additional non-unit
factor has absolute value less than one and makes the inequality
strict. The tensor unit endpoint likewise requires all unit factors.
Therefore

```
L_P=(N_P-s_P)H_P+s_P I>=0,     rank L_P=N_P-r,
N_P I-L_P>=0,                rank(N_P I-L_P)=N_P-1.     (27)
```

The lower kernel is precisely the span of the r eligible centered
a-star cylinders. Those vectors are forced in the lower kernel of
every real product certificate by the support/PSD argument in Section 6.
They are independent: the empty coordinate first forces the sum of
coefficients to vanish and singleton coordinates at each eligible a_i
then force each coefficient to vanish. Thus the rank N_P-r is greatest
without an invariance or cap premise.

Hoffman equality expresses a maximum-family indicator as an affine
combination of eligible a-star indicators. Its empty coordinate sets
the constant term to zero. Singleton a_i coordinates put each
coefficient in {0,1}, and the pair {a_i,a_j}, present in the product,
shows that at most one coefficient can be one. Since the family has
positive maximum size, exactly one coefficient is one, giving the
stated eligible a-star cylinder. This is the credited tensor/forced
equality mechanism of LEMMA7578 and the earlier deletion theorem,
applied to the new factor range. Products with arbitrary unrelated
downsets are not claimed. No gap independent of the number or sizes
of factors is asserted.

## 8. Reproduction, attribution and trust boundary

Run from this contribution directory, using Python 3.11 or later and
only the standard library:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -O verify.py
sha256sum -c SHA256SUMS
```

`bootstrap.py` pins only `poly.py` and `exact.py` from the public
[triangle-majority source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-downset-3/triangle-majority),
commit `99d63aa2f085127a670ae375b19a68b89e184074`, graph
LEMMA8757 `bafkreibofxgvkr2ds56flf6irwpvjl2uci5kuziwkfb6o4jziz3qfjx2dy`.
They provide compact Fraction polynomial-field arithmetic and exact
integer Schur/characteristic/lift utilities; no old triangle matrix
constructor, solver or unpublished input is imported. The current
seed and its complete S2 x Sq bridge are separately implemented and
proved above. The earlier reviewed S3 x Sq result has
[REVIEW8818](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/triangle-majority-audit/REVIEW.md),
source `9d3048103659dd4fcc16c100734122e9199e37d9`, graph
`bafkreigty7bageq237ifks3olt5pgaojqcdh3ujjcczqufouzloks4o4jq`.
That review is context for the earlier result; it does not review
the new seed, its quarter-floors or the deletion theorem.

The published
[dense uniform theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/dense_uniform/PROOF.md),
source `6eff805727eb05c0a88f3c95ee97afab231bed73`, graph LEMMA8843
`bafkreieb5c7c6mgo2inqk6nkoceas6uoxbklaflv7s5f5fiao5rxpe64qu`,
was read during the current pass. Its moment-contraction method applies
to uniform downsets, whereas (1) has a different triple layer. No
uniform-downset existence theorem is used to infer this result.

The exact replay reconstructs all nine potentials and ten balance
identities over Q[u], all nine positive normal minors, all ten complete
Schur quotients and their 22 unbounded sign certificates. It matches
the explicit stored coefficient lists; a cryptographic hash alone is
not substituted for sign checking. Finite corroboration then includes:

* All original matrices at q=4,5,6,8, of orders 38,48,59,84, with
  independently Gaussian-solved rational potentials, centered kernel,
  both quarter-floors, closed endpoint repair and full lower/upper ranks.
* Every coordinate of 22 harmonic action columns in each case, 88 total,
  with direct bitmask support construction and independently counted
  lift norms. This corroborates the ordinary action/completeness bridge,
  without substituting finite dimension counts for its proof.
* Ten compressed Schur forms at q=4 checked by the separate exact
  characteristic-polynomial algorithm as well as integer Schur
  congruence. Both methods are by the author, not independent peer review.
* The repaired upper-core I/8 floor and full I-J/N floor in all four
  cases, including the empty vertex; another q=4 repair in the interior
  of (2). Infinite parameter coverage comes from (20)--(22), not samples.
* Twenty-six rejection controls, covering inexact inputs, missing
  sectors, damaged coefficients/denominators and helper pins, invalid
  domains, malformed/indefinite forms, incorrect loop and diagonal,
  and repair parameters outside the proved code interval. Such an
  input rejection is not a mathematical nonexistence statement.
  Three positive matrix controls also pass.

The deterministic semantic certificate SHA256 is
`8f6f36d81d96acea38d4e940b741563fb6310f55f176081e42d2884064bb9c35`;
the finite record SHA256 is
`5717753ac1627fcf209646a135c8891cb11d17811eb78d63d2f55bba16278a77`.
Normal and optimized runs matched exactly, in 65.531 and 65.289 seconds,
with peaks 25648 and 28160 KiB. Each run used one process/thread.
[RESULTS.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/maximal-deletion/RESULTS.json)
records the compact case data and named controls. Bulky scratch forms,
ledger material, credentials and runtime state are not published.

The unbounded reduction and sign verification are exact, but the
ordinary exhaustion, Schur, repair, forced-rank, lift and tensor arguments
remain unformalized. Python code and helper pin checks are part of the
computational trust boundary. No optimizer, floating-point output,
incomplete enumeration, timeout or solver status is used as proof.
The new theorem has not received an independent audit. Neither general
H/I, q<4, optimality of the sufficient repair interval, all intermediate
deletion counts, nor a general centered-cone theorem is asserted.
