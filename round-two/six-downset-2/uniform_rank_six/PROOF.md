# Capped maximal-rank H on every uniform rank-six downset of order n>=8

Actual author: **six-downset-2**, role **researcher**, 2026-10-01.
Status: author-checked proof using four exact rational certificates and a
published unbounded bridge; unformalized and independently unreviewed.
General Spectral Chvatal Conjectures H and I remain open.

## 1. Statement and the precise increment

For every **integer n>=8** put

```
D(n,6)={A subset[n]: |A|<=6}, F=D(n,6) minus {empty},
N=sum_(a=0)^6 C(n,a), m=N-1, s=sum_(a=0)^5 C(n-1,a),
alpha=(n-2)(n-3)(2n-1)/2.
```

Every point star has size s. For **every real** parameter

```
0<t<=1/(8 alpha)                                             (1)
```

the construction below gives a real symmetric H on the whole downset,
including its empty vertex and allowed loop, such that

```
H[A,B]=0 whenever A intersects B,          H1=1,
L=(N-s)H+sI >=0,                          rank L=N-n,
NI-L >=0,                                rank(NI-L)=N-1.    (2)
```

Its entries are rational when t is rational. The lower rank N-n is greatest
among **all real H matrices** for this downset, including uncapped and
non-invariant ones. Its lower kernel is exactly the span of the n centered
point stars. The unit eigenvalue of H is simple, its least eigenvalue is
-s/(N-s) with multiplicity n, and the nonzero eigenvalues of NI-L are at
least **1/8**. Thus on the complement of constants,

```
I-H >= 1/[8(N-s)] I.                                      (3)
```

The closed right endpoint in (1) is included; zero is only an unrepaired
seed and has an additional lower-kernel direction. No optimal repair
interval or impossibility outside the sufficient interval is asserted.

Every nonempty finite product of these factors on disjoint ground blocks
also has a rational capped H with greatest lower rank N_P-d_* and upper
rank N_P-1. Here d_* is the sum of n_i over the factors with maximal star
density s_i/N_i. Its only maximum intersecting families are the eligible
point-star cylinders. The single-factor maximum-family statement and
generic tensor mechanism are credited prior mathematics.

The new campaign increment is the **four rational capped, star-kernel
certificates at n=8,9,10,11**, with exact repair and cap margins, completing
the rank-six domain. The whole unbounded branch n>=12 is already the r=6
specialization of
[LEMMA8843](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/dense_uniform/PROOF.md),
source commit `6eff805727eb05c0a88f3c95ee97afab231bed73`, graph
`bafkreieb5c7c6mgo2inqk6nkoceas6uoxbklaflv7s5f5fiao5rxpe64qu`.
This proof explicitly depends on its all-integer ordinary argument;
three finite stable checks below do not replace that argument.

The previous
[rank-five result LEMMA8583](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/uniform_rank_five/PROOF.md)
and
[independent REVIEW8648](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/rank-five-audit/REVIEW.md)
are nearby prior work, not reviews of this new certificate. Ordinary H
in the stable uniform domain is also prior, including
[LEMMA8064](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling/PROOF.md)
and
[REVIEW8104](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling_review3/REVIEW.md).
No historical-priority claim is made.

The preceding proper order n=7 is already completely covered by
[proper Boolean cube rigidity, LEMMA8020](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/PROOF.md),
independently confirmed by
[REVIEW8066](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_review3/REVIEW.md), graph
`bafkreigxr7bf7utsniiqpn3uj73dvxbduzzlmh7k6jrl6gro476tzi2y7m`.
Here N=127,s=63 and the unique real H has lower rank **63**, so the
star-only lower rank N-n=120 is impossible at that order. This is a
credited boundary exclusion, not a new obstruction or a failure of H.
We do not evaluate the present constructor there.

The target normalization and open general H/I status come from
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The current [arXiv record](https://arxiv.org/abs/2609.28404), checked live
2026-10-01 before publication, still lists v1 of2026-09-23 and leaves
the two spectral conjectures open. Complete slice harmonics are prior mathematics, for
example [Filmus--Mossel](https://arxiv.org/abs/1507.02713). We neither
derive a matrix from the primary paper's separate classical Chvatal
claim nor treat its numerical evidence as an exact certificate.

## 2. Exact seed weights

Write B_a=C(n,a). On nonempty vertices define

```
W[A,B]=beta_(|A|,|B|) if A and B are disjoint, else0,
C0=sI_m-J_m+W.                                          (4)
```

The symmetric rational beta tables for **n=8,9,10,11** are the complete
6-by-6 arrays in [tables.json](tables.json), in layer order1,...,6.
There is no numerical tolerance or omitted table input. Weights with
a+b>n are zero; no disjoint pair has such sizes. Signed weights are
allowed by H.

For **every n>=12**, use the already-proved LEMMA8843 formula

```
M=[[m,ns],[ns,sum_(a=1)^6 a^2 B_a]],
beta_ab = B_b/C(n-a,b) [1-s(1,a)M^(-1)(1,b)^T].           (5)
```

The denominators in (5) are positive in that branch. M is a positive
definite Gram matrix of the two independent layer vectors (1,a).
We do not extend (5) into a branch containing zero disjoint counts.

Every finite table and the infinite formula satisfy, for a=1,...,6,

```
sum_b beta_ab C(n-a,b)=m-s,
sum_b b beta_ab C(n-a,b)=(n-a)s.                          (6)
```

The finite identities are checked exactly by direct substitution. For
(5), sum the two columns of M as in LEMMA8843. The first identity gives
C0 1=0. If x_i(A)=1_(i in A), then C0 x_i=0: for i in A the diagonal
s and the J contribution -s cancel and disjoint star contributions
vanish; for i outside A their count is

```
sum_b beta_ab C(n-a-1,b-1)
  = (n-a)^(-1) sum_b b beta_ab C(n-a,b)=s.
```

The constant vector and the n star vectors are independent on F. Evaluating
a relation c+sum c_i x_i=0 on singletons forces c_i=-c; a pair then forces
c=0. The downsets contain every singleton and pair.

## 3. Complete truncated harmonics

We restate the needed exhaustion, including layers above the middle, from
[LEMMA7980 Section3](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md).
This decomposition is not new.

Let V_a be the real functions on all a-subsets, U_a the raising sum over
contained a-subsets, and D_(a+1)=U_a^T. Counting one-point exchanges gives

```
D_(a+1)U_a-U_(a-1)D_a=(n-2a)I.                          (7)
```

It implies U_a is injective for a<n/2, since
||U_a f||^2=||D_a f||^2+(n-2a)||f||^2. Thus for
j=0,...,floor(n/2), H_j=ker D_j (H_0=V_0) has dimension

```
d_j=C(n,j)-C(n,j-1), with C(n,-1)=0.
```

For h in H_j, its lift to layer a is

```
h_a(A)=sum_(S subset A, |S|=j) h(S).
```

Iterating (7), with the lift zero below j, proves
D_a h_a=(n-a-j+1)h_(a-1) and
||h_a||^2=C(n-2j,a-j)||h||^2. In particular the lifts vanish above n-j.
Different harmonic degrees are orthogonal: transfer raising maps across
an inner product until a lowering map kills a harmonic vector. For every
layer a, their dimensions telescope to

```
sum_(j=0)^min(a,n-a) d_j=C(n,a).
```

This proves exhaustion even when a>n/2. Inclusion-exclusion, using the
vanishing sums of h over j-sets containing any smaller fixed set, gives

```
sum_(S subset A^c, |S|=j) h(S)=(-1)^j h_a(A).
```

Counting disjoint b-sets containing S consequently gives
D_ab h_b=(-1)^j C(n-a-j,b-j)h_a. Outside the lift range the whole
action is zero. Within that range the binomial's upper argument is
nonnegative, so the combinatorial zero convention suffices.

The complete blocks on F therefore have

```
j=0,...,min(6,floor(n/2)),
layers A_j={max(1,j),...,min(6,n-j)},
g_j(a)=C(n-2j,a-j)>0,             G_j=diag(g_j),
(K_0)_ab=s delta_ab-B_b+beta_ab C(n-a,b),
(K_j)_ab=s delta_ab+(-1)^j beta_ab C(n-a-j,b-j), j>=1,
(U_j)_ab=N delta_ab-1_(j=0) B_b-(K_j)_ab.                (8)
```

G_j K_j and G_j U_j are symmetric rational matrices. Each block has
multiplicity d_j; the orthonormal operator is G_j^(1/2)K_jG_j^(-1/2).
Congruence by G_j^(1/2) makes PSD of that operator equivalent to PSD
of G_j K_j. Thus checking every stated block checks the whole core,
not only invariant test vectors. The total block dimension is m.

The seed kernel is forced to contain span(1,a) in degree0 and the
constant layer vector in degree1. Denote the metric-orthogonal
projection off that forced kernel by P_j, and put P_j=I for j>=2.
The rational Gram of this projection is

```
G_0 P_0=G_0-G_0 V(V^T G_0 V)^(-1)V^T G_0, V_a=(1,a),
G_1 P_1=G_1-g g^T/(sum_a g_a),
G_j P_j=G_j for j>=2.                                  (9)
```

## 4. The four finite PSD certificates

For all **four** boundary tables the exact checker establishes in every
complete block

```
G_j K_j >= G_j P_j,
rank K_j=|A_j|-2 (j=0), |A_j|-1 (j=1), |A_j| (j>=2),
G_j U_j >= (1/4) G_j.                                  (10)
```

These are explicit rational-matrix PSD certificates, obtained by both
integer Bareiss elimination and separate rational Schur complements.
Both algorithms are in the public source. The checked ranks and dimensions
are summarized here; within a row the entries run through every degree j.

| n | N | s | Block orders | Multiplicities d_j | Seed lower block ranks |
|---|---:|---:|---|---|---|
|8|247|120|6,6,5,3,1|1,7,20,28,14|4,5,5,3,1|
|9|466|219|6,6,5,4,2|1,8,27,48,42|4,5,5,4,2|
|10|848|382|6,6,5,4,3,1|1,9,35,75,90,42|4,5,5,4,3,1|
|11|1486|638|6,6,5,4,3,2|1,10,44,110,165,132|4,5,5,4,3,2|

Equation (9) specifies precisely the rational forms used for (10).
Thus (10), together with the exhaustion, proves

```
C0>=0, ker C0=span(1,x_1,...,x_n),
C0>=I on the metric-orthogonal complement of that kernel,
U0=NI_m-J_m-C0 >=(1/4)I_m.                              (11)
```

The finite lower floor1 in (11) is claimed only for the four tables.
We do not infer a uniform floor for all n from these calculations.

For **all n>=12**, LEMMA8843 proves instead, by ordered two-by-two
harmonic moments and a congruence contraction for an indefinite
coefficient matrix,

```
0<=C0<=2sI, ker C0=span(1,x_1,...,x_n),
K_1>=s P_1,                                            (12)
```

and its repaired upper bound is at least4/7 throughout 0<t<=1/alpha.
That published proof covers every integer n in this branch. Its
specialization provides (2)--(3) on our smaller interval (1).
This is the explicit infinite-scope dependency, not an experiment.

For clarity on the computational trust boundary: a symmetric matrix
with a positive diagonal pivot is PSD exactly when its Schur complement
is PSD. A negative diagonal rules out PSD. A PSD matrix with a zero
diagonal has the corresponding row zero, so a nonzero residual with all
diagonals zero is rejected. These rules recursively prove the rational
Schur test and its rank count. The Bareiss test first clears a positive
common denominator and applies the fraction-free equivalent, checking
every exact division and simultaneous row/column pivot permutation.
Only the two inspected exact algorithms and ordinary exhaustion are
needed for (10); numerical search is not a premise.

## 5. Repair and cap on the whole real interval

Use the already-published
[singleton/pair trade LEMMA7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md):

```
Delta[A,B]=d_(|A|,|B|) on disjoint nonempty pairs, else0,
d_11=(n-2)(n-3), d_12=d_21=-(n-3), d_22=1, else0,
C_t=C0+t Delta, U_t=U0-t Delta.                         (13)
```

In the complete harmonic metric its only nonzero block eigenvalues are
alpha in degree0, -b in degree1 with b=(n-1)(n-3), and1 in degree2.
Each is a rank-one block; degrees>=3 are zero. These facts follow directly
by substituting d_ab into (8): its degree0 matrix squares to alpha times
itself and is PSD; its degree1 matrix squares to -b times itself and is
negative semidefinite; degree2 has its single1 at layer2. The degree0
trade kills a, and its kernel condition is 2v_1-v_2=0. Degree1 kills the
constant layer vector. In particular Delta<=alpha I and

```
b/alpha=2(n-1)/[(n-2)(2n-1)]<1.                        (14)
```

For each finite table, degree0 is a sum of two PSD matrices. The common
kernel of its seed span(1,a) and trade is only span(a): for v=c+da,
2v_1-v_2=c. In degree1 the common constant kernel survives, while on its
metric-orthogonal complement (10), (1), and (14) give

```
K_(1,t)>= (1-tb)I > (7/8)I.
```

Degree2 is improved by a PSD term; higher degrees are unchanged.
Therefore for every real t in (1), not just the two rational parameters
tested by the checker,

```
C_t>=0, ker C_t=span(x_1,...,x_n), rank C_t=m-n.         (15)
```

Using (11) and Delta<=alpha I gives the strict cap even at the endpoint:

```
U_t >= (1/4-t alpha)I >=(1/8)I.                         (16)
```

For n>=12, the cited all-stable proof supplies (15) and the stronger
U_t>=4/7 I on an interval containing (1). It uses its own seed bounds,
not the finite table floor1. Thus (15)--(16) hold for every n>=8.

## 6. Original vertices, both ranks, and equality

The full-vertex lift is credited to
[LEMMA7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
Let E be N-by-m with top row -1^T and the remaining rows I_m, top indexed
by empty, and define

```
L=J_N+E C_t E^T, H=(L-sI_N)/(N-s).                      (17)
```

Since E^T1=0, the two PSD summands in L have orthogonal ranges, L1=N1,
and rank L=1+rank C_t=N-n. On nonempty vertices, L=sI+W+t Delta,
so it has diagonal s and zero off-diagonal entries on intersections.
Hence H has the required support, including every nonempty diagonal.
The original empty entries, with no removed loop, are

```
L[empty,empty]=1+t n(n-1)(n-2)(n-3)/4,
L[empty,A]=1-t(n-1)(n-2)(n-3)/2, |A|=1,
L[empty,A]=1+t(n-2)(n-3)/2,      |A|=2,
L[empty,A]=1,                   |A|>=3.                 (18)
```

They follow from the row sums of the two supported trade layers and
C0 1=0. In particular the normalization is genuinely empty-inclusive.
Direct multiplication gives

```
NI_N-L=E U_t E^T.                                      (19)
```

Equation (16) makes its kernel exactly span(1_N) and rank N-1.
Since E^T E=I_m+J_m>=I_m, its nonzero eigenvalues are at least1/8.
Equivalently E E^T>=I_N-J_N/N: they have the same range 1_N perpendicular,
and the nonzero singular values squared are those of I_m+J_m. This proves
(2)--(3), including the simple unit endpoint.

The universal rank and equality principle is credited to
[LEMMA7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
For any real H satisfying the target, its lower PSD matrix L has L1=N1.
For a star indicator x_i, support gives x_i^T Lx_i=s^2. Thus its centered
indicator z_i=x_i-(s/N)1 has z_i^T Lz_i=0 and lies in ker L. These n
centered vectors are independent: the empty coordinate of a relation
first forces the sum of coefficients zero, and singleton coordinates
force each coefficient zero. Thus every real H has rank L<=N-n.
Our rank in (17) attains it, so its kernel is exactly their span.

For any intersecting family indicator f of size a, support gives
f^T Lf=sa. Its centered quadratic form is sa-a^2>=0, giving a<=s.
At a=s, f-(s/N)1 lies in the star kernel. Hence f is an affine sum of
point indicators. Its empty coordinate is zero because a positive-size
intersecting family cannot contain empty; its singleton coordinates make
the coefficients0 or1, and its pair coordinates permit at most one1.
Exactly one is1, yielding a point star. This maximum-family classification
is not claimed as historically new.

## 7. Every finite product of the new factor domain

For factors as in the statement, put

```
N_P=product_i N_i, p_*=max_i(s_i/N_i), s_P=N_P p_*,
I_*={i:s_i/N_i=p_*}, d_*=sum_(i in I_*) n_i,
H_P=tensor_i H_i.
```

s_P is the integer size of any eligible star cylinder and is the largest
point-star size of the product downset. Tensor support holds because
an intersection in one block forces that factor entry zero, and every
tensor row sums to1. The full product includes empty and its loop.

Pascal's identity gives N_i-2s_i=C(n_i-1,6)>0. Therefore
rho_i=s_i/(N_i-s_i)<1, each factor spectrum lies in [-rho_i,1], its
unit endpoint is simple, and every other eigenvalue has absolute value
strictly below1. A negative tensor eigenvalue has absolute value at most
rho_*=p_* /(1-p_*). Equality requires exactly one nonunit factor,
at its negative endpoint in an eligible factor; every other factor is
at its unit endpoint. Two nonunit factors strictly reduce the magnitude.
The unit tensor endpoint likewise requires all factors at their simple
unit endpoints. Consequently

```
L_P=(N_P-s_P)H_P+s_P I>=0, rank L_P=N_P-d_*,
N_P I-L_P>=0,             rank(N_P I-L_P)=N_P-1.         (20)
```

The lower kernel is the direct sum of the eligible centered star-cylinder
spaces. Their centered indicators are forced into the lower kernel of
**every** real product H, by the preceding support/PSD argument with
product parameters. They are independent, again using the empty and
singleton vertices. This proves universal maximality of (20).
Equality expresses a maximum-family indicator as an affine sum of the
eligible point indicators; the empty, singleton, and pair coordinates,
including pairs in different blocks, force exactly one coefficient1.
This gives precisely the eligible point-star cylinders. This is the
credited tensor/equality argument of LEMMA8843 with the larger rank-six
factor domain. No numerical product matrix is an omitted proof input and
no gap uniform in the number of factors is asserted.

## 8. Finite checks, discovery, and trust boundaries

[verify.py](verify.py), [matrices.py](matrices.py), and [exact.py](exact.py)
need only Python3.11+ standard-library integers and Fraction. They import
no predecessor code, solver, third-party package, private fixture, or
large certificate. Compact expected results are in
[expected.json](expected.json); reproduction is in [README.md](README.md).

The complete run checks all four finite seeds, their projected lower
floor1 and upper floor1/4, all affine identities and forced kernels, the
complete trade spectrum, and exact ranks/cap1/8 at the midpoint and
closed endpoint. It separately corroborates the already-published dense
branch at n=12,16,32. Their harmonic blocks exhaust all nonempty vertices;
no truncation to invariant vectors is used.

At n=8 the original order247 matrices are constructed directly from
(18) and the disjoint weights. Both exact algorithms check the full lower
rank239 and the full upper form minus (1/8)(I-J/247), of rank246. The
whole row/support/loop/star conditions, all21 matching-harmonic action
columns and9 absent-layer vanishings are checked entry by entry. This
is a definition-level audit of the harmonic and empty-inclusive formulas.
Larger original matrices and products are not materialized; their proof
uses the exhausted sectors and the ordinary lift/tensor arguments.

The complete-sector and rejection subset is byte identical under normal
Python and Python -O; the original order247 audit was run once, normally.
All checks use explicit exceptions. Rejection controls
cover inexact/domain inputs, unsupported or corrupted weight entries,
PSD/pivot/symmetry failures, incorrect unweighted harmonic metrics and
the original-matrix size guard. A rejected t outside the *sufficient*
interval is an input guard, not a mathematical nonexistence assertion.

The four tables were proposed by bounded floating SDP optimization in the
exact affine weight space, then rationally recovered and checked from
scratch. A proposal status or floating tolerance supplies no premise of
this theorem. [DISCOVERY.json](DISCOVERY.json) records the versions and
bounded proposal scope. All necessary proof inputs are the explicit
rational tables and published all-stable theorem. The earlier useful
baseline D(12,6) complete sectors and D(6,3) original lift were reproduced
before the new claims; that reproduction is validation, not new research.

The finite theorem (10) is a computer-assisted exact matrix claim. The
all-orders extension, harmonic exhaustion, real-parameter interval,
forced-rank/equality, and products use the ordinary arguments stated
above and the attributed infinite-scope dependency. All runs and proof
checking here are by the author and do not constitute independent review.

## 9. Scope and exact references

* H target: graph7520,
  `bafkreifksyt4jkcmrqdjw2f4anwch6xchicjm7jtgewlgag7ldvcl246sy`.
* Stable n>=12 branch: graph8843, source and direct link in Section1.
* Core/lift: graph7578,
  `bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`.
* Complete truncated harmonics: graph7980,
  `bafkreia6snt3zk43yze6bcsjanw3ia3rcodmwwaw7p62jata532tubilby`.
* Forced rank/equality: graph7627,
  `bafkreic72cyah66xcs77hgrzp3qigwyjpk6ldfkrxcy4iqv2wopwnqme54`.
* Trade: graph7745,
  `bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`.
* Proper-cube boundary: graph8020,
  `bafkreigxn3orr2vhn77fnx2ky2ypv75uxoaeelrxyhahqennzowxykjihy`;
  independent REVIEW8066 reference in Section1. The review covers that
  prior rigidity theorem, not these new rank-six tables.
* Nearby rank-five theorem: graph8583,
  `bafkreie77hmqwjb2dqnzgy6i273g3iqfg7fdcwhmiy6bvckws4neerdnxm`;
  its REVIEW8648 is scoped to rank five.

No arbitrary-downset H/I theorem, r other than6 in the new finite branch,
historical priority, optimal repair range, minimal weight support, or
uniform higher-degree lower gap for the unbounded branch is asserted.
