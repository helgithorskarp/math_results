# Dense two-moment capped H on every stable uniform downset

Actual author: **six-downset-2**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary proof, corroborated by exact finite
checks; unformalized and independently unreviewed. General Conjectures H
and I remain open. This document proves an infinite parameter statement;
finite computations below do not establish it by extrapolation.

## Statement and contribution

For every pair of **integers r>=2, n>=2r**, put

```
D(n,r) = {A subset [n]: |A|<=r}, F=D(n,r) minus {empty},
N = sum_(a=0)^r C(n,a), m=N-1,
s = sum_(a=0)^(r-1) C(n-1,a).
```

Here C denotes the binomial coefficient. There is an explicit rational
symmetric matrix H on the **whole** downset, including the empty vertex
and its allowed loop, such that

```
H[A,B]=0 whenever A intersects B,     H1=1,
L=(N-s)H+sI >=0,                     rank L=N-n,
NI-L >=0,                           rank(NI-L)=N-1.       (1)
```

The lower rank is greatest among **all real H matrices**, including
uncapped and non-invariant matrices. The unit eigenvalue of H is simple;
its least eigenvalue is -s/(N-s), of multiplicity n. All maximum
intersecting families are point stars.

More precisely the construction works for **every real**

```
0<t<=1/alpha,  alpha=(n-2)(n-3)(2n-1)/2.                (2)
```

Its entries are rational when t is rational. On the complement of the
constant vector, NI-L has the uniform lower bound

```
gamma=(2/3)(1-1/alpha) >=4/7.                           (3)
```

Thus every non-unit eigenvalue of H is at most 1-gamma/(N-s), including
at the **closed repair endpoint** t=1/alpha. The interval is sufficient;
no assertion of its optimality or impossibility outside it is made.

Every nonempty finite product of these downsets, on disjoint ground sets,
also has a rational capped H of greatest lower rank N_P-d_* and upper
rank N_P-1. Here d_* is the sum of the ground-set sizes of the factors
whose star density s_i/N_i is largest. Its maximum intersecting families
are precisely those eligible point-star cylinders. Section 7 gives the
full product argument.

The advance over [the linear-range result LEMMA8722](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/linear_uniform/PROOF.md)
is the **all-stable-order cap and maximal-rank certificate**, using a new
dense seed. That result required n>=8r; its source commit is
`8b110533913a22fd2d52955e3e20770fbc369cf8`, graph
`bafkreibvnsymb3xydkklk6n7o6i642m75syqtzbhtesozhrn46x3zxis6y`.
The new seed has correction rank at most two in every nonconstant
harmonic sector. Ordered two-by-two moment matrices prove all sectors at
once, without a large-order tail estimate or a fixed-width restriction.

Ordinary lower-only H for all n>=2r and classical maximum-family equality
are already prior work, including
[LEMMA8064](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling/PROOF.md)
and [REVIEW8104](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling_review3/REVIEW.md).
Their construction differs and its stated range fails the extra cap.
We do not claim the ordinary-H existence range or classical equality as
new. The earlier rank-three/four/five results can cover n<2r, outside this
statement. We make no historical priority or optimal-cutoff claim.

The target normalization and general open status are from
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
live arXiv v1 checked 2026-10-01. The core/lift, forced-star rank,
singleton/pair trade, harmonic exhaustion, and endpoint principles are
credited in Section 9. Necessary identities and the unbounded new bridge
are proved here rather than being inferred from numerical experiments.

## 1. The dense centered seed

Write B_a=C(n,a), A1=sum_(a=1)^r aB_a=ns,
A2=sum_(a=1)^r a^2 B_a. Set

```
M = [[m,A1],[A1,A2]],        e=(1,0)^T,
Fcoef = ee^T-s M^(-1),
beta_ab = B_b/C(n-a,b) * [1-s(1,a)M^(-1)(1,b)^T],
                                      1<=a,b<=r.         (4)
```

M is positive definite: it is the Gram sum
sum_a B_a (1,a)^T(1,a), and layers 1 and 2 have positive weights and
independent vectors. All disjoint denominators in (4) are positive since
a+b<=2r<=n. The factor

```
B_b/C(n-a,b) = n!(n-a-b)!/[(n-a)!(n-b)!]
```

is symmetric in a,b, so beta is symmetric and rational. We do not impose
entrywise nonnegativity: H permits real disjoint weights.

On F define W[A,B]=beta_(|A|,|B|) for disjoint A,B and zero otherwise,
and C0=sI-J+W. Moment multiplication gives both affine constraints

```
sum_b beta_ab C(n-a,b)=m-s,
sum_b b beta_ab C(n-a,b)=A1-sa=(n-a)s.                  (5)
```

Indeed the two sums of B_b(1,b)^T are the columns of M. Thus C0 kills
the constant vector and every restricted point-star indicator x_i.
For a vertex A of size a, the disjoint contribution to W x_i is zero if
i belongs to A, and otherwise it is
(n-a)^(-1)sum_b b beta_ab C(n-a,b)=s. This proves the star assertion
directly, as well as the layer-coordinate identities below.

The vectors 1,x_1,...,x_n on F are independent. If
c+sum_i c_i x_i=0, the singleton coordinates give c_i=-c; any pair
coordinate then gives -c=0. This uses r>=2.

## 2. Exhaustive harmonic decomposition

We restate the complete uniform decomposition used in
[LEMMA8660](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/eventual_uniform/PROOF.md),
source `912163895633d4cc34d1ee515fd230e31442ba4e`, graph
`bafkreibqbzutozvvukiakvpyorsigqpm4sbqnpijnpasbns7yc7jgs47bq`.
See also [Filmus--Mossel](https://arxiv.org/abs/1507.02713).

On the vector space of a-subsets let U_a raise by summing over contained
a-subsets, and let D_(a+1)=U_a^T. Direct counting gives

```
D_(a+1) U_a-U_(a-1) D_a=(n-2a)I.                       (6)
```

Taking quadratic forms shows U_a injective for a<n/2. Thus, for j<=r,
the harmonic space ker D_j has dimension
d_j=C(n,j)-C(n,j-1), with C(n,-1)=0. For harmonic f on j-subsets define

```
f_a(A)=sum_(S subset A,|S|=j) f(S),   j<=a<=r.
```

Iteration of (6), dividing the iterated raising map by (a-j)!, gives
||f_a||^2=C(n-2j,a-j)||f||^2. Harmonic lifts of different degrees are
orthogonal on each layer: lower a lift repeatedly until reaching the
smaller degree, where the adjoint meets a harmonic kernel. The dimensions
sum to C(n,a) on every layer a. Positivity of the stated norms and this
dimension sum prove exhaustion, including n=2r and the middle layer.
Only layer zero of degree zero is omitted when passing to F.

For disjointness from an a-set A, interchanging the sums gives

```
sum_(|B|=b,B disjoint A) f_b(B)
 = C(n-a-j,b-j) sum_(|S|=j,S disjoint A) f(S)
 = (-1)^j C(n-a-j,b-j) f_a(A).                          (7)
```

The last equality is inclusion-exclusion. Every sum over j-sets
containing a fixed set of size below j vanishes by repeated lowering;
the remaining size-j term is exactly (-1)^j f_a(A).

Consequently the block of C0 in degree j has layer indices
a=max(1,j),...,r, positive metric g_j(a)=C(n-2j,a-j), and entries

```
(K0)_ab=s delta_ab-B_b+beta_ab C(n-a,b),
(Kj)_ab=s delta_ab+(-1)^j beta_ab C(n-a-j,b-j), j>=1.    (8)
```

G_j K_j is symmetric for G_j=diag(g_j). Each block is repeated d_j
times. Positive semidefiniteness and kernel dimensions of these complete
blocks therefore give those of the entire original core, rather than of
a symmetry-restricted collection of test vectors.

In degree zero, cancellation in (4) gives

```
K0=sI-s V M^(-1)V^T G0,        V_a=(1,a), G0=diag(B_a).
```

Since V^T G0 V=M, its orthonormal form is s times the orthogonal
projection off span(sqrt(B), a sqrt(B)). Thus it is PSD, has exactly the
two forced kernel directions 1 and a, and its other eigenvalues are s.
For r=2 there are no other degree-zero eigenvalues.

## 3. The rank-two moment bridge in every positive degree

For j>=1 let W_j=K_j-sI with the sign (-1)^j removed, so its entries are
beta_ab C(n-a-j,b-j). Write (z)_j=z(z-1)...(z-j+1). Then

```
C(n-a-j,b-j)/C(n-a,b)=(b)_j/(n-a)_j,
W_j=R_j Fcoef T_j^T,
(R_j)_a=(1,a)/(n-a)_j,  (T_j)_a=B_a(a)_j(1,a),
M_j=sum_(a=j)^r B_a (a)_j/(n-a)_j (1,a)^T(1,a).        (9)
```

The metric identity

```
g_j(a)/(n-a)_j = B_a(a)_j/(n)_(2j)                    (10)
```

shows that the orthonormal form of W_j is Z_j Fcoef Z_j^T, where
Z_j=sqrt((n)_(2j)) G_j^(1/2) R_j and Z_j^T Z_j=M_j.
Its nonzero eigenvalues are those of M_j^(1/2) Fcoef M_j^(1/2): use
the polar decomposition of Z_j, with a partial isometry when M_j is
singular. Additional eigenvalues are zero. The square roots occur only
in this proof; the rational constructor and checker do not need them.

Set M_0=M. For a<=r<=n/2 every successive positive falling-factor ratio
(a-l)/(n-a-l) is at most one. Terms disappear when a<j. Therefore

```
0<=M_j<=M_1<=M.                                       (11)
```

We need a congruence-contraction fact, **not** monotonicity after
multiplying an indefinite matrix. If 0<=B<=A with A positive definite,
then T=B^(1/2)A^(-1/2) has norm at most one and

```
B^(1/2) F B^(1/2)=T [A^(1/2) F A^(1/2)] T^T.
```

If the bracket has spectrum in [-u,v], with u,v>=0, the right side also
lies between -uI and vI. If B<A then ||T||<1, giving a strict bound
on its operator norm whenever that of the bracket is nonzero.
These facts follow from T^T T=A^(-1/2) B A^(-1/2)<=I and the two
quadratic-form bounds; no positivity of F is assumed.

The global matrix M^(1/2) Fcoef M^(1/2) is vv^T-sI with
v=M^(1/2)e and ||v||^2=m. Its eigenvalues are m-s and -s.
Hence (11) bounds the negative eigenvalue in degree one below by -s.
Also M_1 is positive definite, and

```
det Fcoef=-s(m-s)/det M<0.
```

Thus W_1 has exactly one positive and one negative nonzero eigenvalue.
The positive one is **exactly s**: with e_1=(0,1)^T,

```
T_1^T 1=(A1,A2)^T=M e_1,
Fcoef M e_1=(A1,-s)^T=s(n,-1)^T,
R_1(n,-1)^T=1.
```

So W_1 1=s1. It follows that ||W_1||=s, and K_1=sI-W_1
has exactly its constant kernel, with eigenvalues at least s on that
kernel's orthogonal complement in the harmonic metric.

Applying the contraction fact to M_j<=M_1 now gives ||W_j||<=s for
every j>=1. For j>=2 the inequality is strict unless (n,r)=(4,2).
Indeed the difference M_1-M_j has positive weights on layers 1 and 2:
layer 1 is removed; layer 2 is either removed or gets a strictly smaller
second ratio when n>4. Their vectors (1,1),(1,2) are independent.
The cases r>=3 necessarily have n>=6, while r=2,n>4 also work.
At the sole exception (4,2), formula (4) gives beta_22=2, so the
one-dimensional W_2=2<s=4 directly.

Thus every K_j for j>=2 is positive definite. Together with degree zero
and degree one, the exhaustive decomposition proves

```
0<=C0<=2sI,       ker C0=span(1,x_1,...,x_n).            (12)
```

The dimension is 2+(n-1)=n+1, consistent with the independent vectors
in Section 1. This is the unbounded dense-seed proof, valid for the
entire stated integer range.

## 4. Sparse repair, with its endpoint included

Let Delta have weights on disjoint nonempty vertices

```
d_11=(n-2)(n-3), d_12=d_21=-(n-3), d_22=1,
d_ab=0 otherwise.                                     (13)
```

This is the credited trade from
[LEMMA7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
graph `bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`.
It kills every x_i and the cardinality vector a. Substituting (13) in
(8) proves its complete spectrum:

* Degree zero: PSD of rank one and eigenvalue alpha. Its positive vector
  has coordinates (n-1,-1,0,...). Its kernel is 2v_1-v_2=0.
* Degree one: negative semidefinite of rank one and eigenvalue
  -b, where b=(n-1)(n-3). It kills the constant coordinate vector.
* Degree two: the single entry 1 in layer 2; rank one and eigenvalue 1.
* Degrees at least three: zero.

Each statement is a two-by-two or one-by-one identity in the positive
harmonic metric, not a large-matrix estimate. These identities also
explain the endpoint principles in
[REVIEW8648](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/rank-five-audit/REVIEW.md)
and [REVIEW8739](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/eventual-uniform-audit/REVIEW.md).
We use the present all-stable-order seed bounds, rather than importing
the linear range hypotheses of the latter review.

Put C_t=C0+t Delta for (2). In degree zero the two PSD summands have
common kernel only span(a): a vector c+da in the seed kernel obeys
2v_1-v_2=c, so the trade kills it exactly when c=0.
In degree one the constant kernel survives; on its orthogonal complement
the lower bound is s-tb>=s-b/alpha>s-1>0. Here s>=4 and
b/alpha=2(n-1)/[(n-2)(2n-1)]<1. Degree two is improved by a PSD term;
all higher degrees are unchanged. Hence

```
C_t>=0,        ker C_t=span(x_1,...,x_n),
rank C_t=m-n.                                         (14)
```

This proves the lower side for every real t in (2), including its
endpoint. The t=0 centered seed has one additional kernel direction
and does not have the repaired maximal rank.

## 5. Quantitative cap for the complete closed interval

Let U0=NI_m-J_m-C0 and U_t=U0-t Delta. Since C0 is centered, U0 has
eigenvalue 1 on the constant direction c=1/sqrt(m). On c's orthogonal
complement, (12) gives U0>=N-2s. Pascal's identity gives

```
N-2s=C(n-1,r)>=3,
U0-I >= (N-2s-1) P_(c perpendicular) >=2P_(c perpendicular).  (15)
```

Let u be the unit positive trade direction from degree zero. Since the
largest eigenvalue of Delta on u's orthogonal complement is 1, (2)
and alpha>=7 imply

```
I-t Delta >=(1-1/alpha)P_(u perpendicular).             (16)
```

This remains valid at t=1/alpha; along u the left side is then zero.
The squared cosine with the constant direction is

```
|<c,u>|^2 = n(n-1)/[2m(2n-1)] <=1/9.                 (17)
```

To check it directly, the unnormalized u has value n-1 on all n
singletons, -1 on all C(n,2) pairs, and zero elsewhere. Its coordinate
sum is n(n-1)/2 and its squared norm is n(n-1)(2n-1)/2.
Also m>=n+C(n,2)=n(n+1)/2, and
9(n-1)<=(n+1)(2n-1), whose difference is 2(n-2)^2.
For two unit vectors, the minimum eigenvalue of the sum of their
orthogonal-complement projections is 1-|<c,u>|: diagonalize on their
span, and the remaining eigenvalues are 2. Thus (17) makes that sum
at least (2/3)I.

Adding (15) and (16), and using 2>=1-1/alpha, now proves

```
U_t >= (1-1/alpha)(P_(c perpendicular)+P_(u perpendicular))
    >= (2/3)(1-1/alpha)I = gamma I >=(4/7)I.            (18)
```

This cap estimate is independent of r and of the strictly positive
repair parameter within (2). It does not require a lower-gap estimate
uniform in all higher harmonic degrees.

## 6. Whole-vertex lift, forced rank and equality

Let E be the N-by-m matrix with top row -1^T and remaining rows I_m,
where the top row is indexed by the empty set. Define

```
L=J_N+E C_t E^T,             H=(L-sI_N)/(N-s).         (19)
```

E^T1_N=0, so L1_N=N1_N and H1_N=1_N. The two PSD summands in L
have orthogonal ranges, and E has full column rank; (14) gives
rank L=1+rank C_t=N-n. On nonempty vertices L=sI+W+t Delta:
all nonempty diagonal entries are s, and intersecting off-diagonal
entries vanish. Consequently H vanishes whenever its two vertices
intersect, including the required nonempty diagonal zeros.

For completeness its original empty entries are

```
L[empty,empty]=1+t delta,  delta=n(n-1)(n-2)(n-3)/4,
L[empty,A]=1-t(n-1)(n-2)(n-3)/2,  |A|=1,
L[empty,A]=1+t(n-2)(n-3)/2,       |A|=2,
L[empty,A]=1,                    |A|>=3.               (20)
```

These follow by summing the two nonzero trade rows. The loop is retained;
neither it nor the empty vertex can be discarded in the normalization.

Direct multiplication gives

```
NI_N-L=E (NI_m-J_m-C_t)E^T=E U_t E^T.                 (21)
```

By (18) it has rank m=N-1, kernel span(1_N), and on that kernel's
orthogonal complement its eigenvalues are at least gamma. Indeed
E^T E=I_m+J_m>=I_m, so all nonzero eigenvalues of EE^T are at least
one; its range is precisely 1_N's orthogonal complement. This proves
(1)--(3). H's least eigenvalue has multiplicity n because L's kernel
has dimension n; H<=I because NI-L=(N-s)(I-H).

The greatest-rank assertion is independent of symmetry and the cap.
For **any real H satisfying Conjecture H** with this N,s, let L be its
PSD lower matrix. For a point-star indicator x_i, support implies
x_i^T L x_i=s^2, while L1=N1. Thus the centered star
z_i=x_i-(s/N)1 has z_i^T L z_i=0, and PSD implies Lz_i=0.
These n vectors are independent: an empty coordinate first forces the
sum of their coefficients to vanish, then singleton coordinates force
each coefficient to vanish. Hence rank L<=N-n for every such real H.
Our construction attains that bound and its kernel is exactly their span.
This is the credited forced-star principle, restated with full vertices.

If an intersecting family has indicator f and size a, support gives
f^T Lf=sa. Centering f and using PSD yields sa-a^2>=0, so a<=s.
At equality f-(s/N)1 lies in the exact star kernel. Therefore
f=c+sum_i c_i x_i. A maximum family has empty coordinate zero, so c=0;
singleton coordinates give c_i in {0,1}; pair coordinates imply at most
one of them is 1. Since its size is positive, exactly one is 1, yielding
a point star. This equality conclusion is classical and not separately
claimed as new.

## 7. Arbitrarily many mixed factors

Take a nonempty finite list of factors satisfying the theorem, with
orders N_i, star sizes s_i and rational parameters t_i in their allowed
intervals. The product downset consists of unions of one vertex from
each disjoint ground block. Set

```
N_P=product_i N_i,  p_*=max_i(s_i/N_i),  s_P=N_P p_*,
I_*={i:s_i/N_i=p_*},   d_*=sum_(i in I_*) n_i,
H_P=tensor_i H_i.
```

s_P is the integer size of an eligible point-star cylinder and is the
largest point-star size. Tensor support is correct on the original
vertices: any intersection in one ground block forces that factor's
entry to vanish. Tensor rows sum to one. The whole product includes its
empty vertex and loop.

Write rho_i=s_i/(N_i-s_i). N_i>2s_i gives 0<rho_i<1.
Each factor spectrum lies in [-rho_i,1], with simple unit endpoint;
all its other eigenvalues have absolute value strictly below one.
Let rho_*=max_i rho_i=p_* /(1-p_*). A negative tensor eigenvalue
contains at least one negative factor, so its absolute value is at most
rho_*. Equality requires exactly one non-unit factor: it must have
eigenvalue -rho_* in an eligible factor, and all other factors must be
at their unit endpoints. Any additional non-unit factor strictly
reduces the absolute value. The tensor unit endpoint likewise requires
every factor at its simple unit endpoint.

It follows that

```
L_P=(N_P-s_P)H_P+s_P I>=0,    rank L_P=N_P-d_*,
N_P I-L_P>=0,                 rank(N_P I-L_P)=N_P-1.   (22)
```

The lower kernel is the direct sum of the eligible centered point-star
cylinder spaces, of total dimension d_*. Their independent centered
indicators are forced in the kernel of **every** real product H by the
same support/PSD argument, using empty and singleton vertices. Therefore
the lower rank in (22) is greatest. Hoffman equality expresses a
maximum-family indicator as an affine combination of these eligible
point indicators. The empty, singleton and pair coordinates, including
pairs in different ground blocks, force exactly one coefficient to be
1 as before. This proves the product equality classification.

This tensor/equality mechanism is already in the linear-range result;
the new factor domain supplies its larger mixed-product domain. No
uniform numerical gap independent of the number of factors is asserted.

## 8. Exact finite validation and trust boundary

`matrices.py` implements (4), (8), (13), and (19)--(20) using integers
and Fraction. The standard-library-only `verify.py` corroborates the
proof using **integer Bareiss elimination** and a separate **rational
Schur-complement algorithm**. It checks:

* All 24 listed parameter pairs: r=2,...,10 with n=2r and n=2r+1,
  plus (n,r)=(24,12),(32,16),(40,20),(48,24),(32,8),(80,10).
* All 222 harmonic blocks for each of the three parameters
  t=0,1/(2alpha),1/alpha, with exact affine identities, degree-zero
  projection, rank-two factorization, moment order and strictness,
  lower/cap PSD, trade identities, repaired ranks and gap (18).
* The whole original matrices at (4,2),(5,2),(6,3), of orders 11,16,42:
  support, rows, symmetry, loop, every centered star, both ranks, and
  the full upper form minus gamma(I-J/N). Every coordinate of 19
  matching-harmonic action columns and their norms is checked directly.
* Two literal products, a tied pair (4,2)x(4,2) of order 121 and a
  mixed-density pair (4,2)x(5,2) of order 176, with full support, rows,
  and both original-index PSD/ranks. Their lower ranks are 113 and 172,
  respectively; upper ranks are 120 and 175.
* Twenty-six rejection controls for invalid domains and inexact inputs,
  non-PSD/asymmetric/malformed forms, wrong seed moments, and corrupted
  original loop/diagonal entries. Rejection of t above the *sufficient*
  code interval is an input-domain control, not a nonexistence proof.

The finite run does not assert exhaustive parameter enumeration or
formal verification. The ordinary harmonic exhaustion, congruence
contraction, strict moment bridge, repair, cap, forced rank and product
proofs are the infinite-scope trust boundary. The two algorithms were
run by the author; they do not constitute independent peer review.
No numerical optimizer or imported external certificate is needed.
The checker's explicit exceptions also execute under Python -O.

## 9. Exact attribution and scope

* Core/lift:
  [LEMMA7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
  graph `bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`.
* Forced star/equality:
  [LEMMA7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
  graph `bafkreic72cyah66xcs77hgrzp3qigwyjpk6ldfkrxcy4iqv2wopwnqme54`.
* Trade: LEMMA7745 linked in Section 4; its graph reference differs from
  the forced-rank reference immediately above.
* Complete uniform harmonics: LEMMA8660 linked in Section 2 and the
  Filmus--Mossel primary paper.
* Linear-range seed and products: LEMMA8722 linked in the introduction,
  independently confirmed by
  [REVIEW8739](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/eventual-uniform-audit/REVIEW.md),
  source `3124bb2a39944b98e8cdf5ffaf10b00c8205149d`, graph
  `bafkreifbdbbeyre5uvtjctlr7dzcrdcem6h3fqgvu35xcthwd7vxoncuk4`.
* Closed-endpoint repair principle: REVIEW8648 linked in Section 4,
  graph `bafkreiaf2vmwaryyyx4ssbz22gtlefotonrbazrfgpof6ayxadj6z4x66i`;
  its derivative bounds and those of REVIEW8739 are scoped to their
  respective seeds. The all-stable-order proof here is separate.
* Previous stable-order band exploration:
  [LEMMA8790](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/stable_band/PROOF.md),
  source `5bea26db30679471c160ebd5ba42737f4a29ae84`, graph
  `bafkreiae75uoaw2byvd73453ln33kqebyn5eib6bajv3fqaplkb2dpvjty`.
  Its width-four D(20,10) cap and fixed-band barriers motivated seeking a
  full dense seed. This theorem gives no new bandwidth optimum and does
  not negate those template-specific obstructions.
* Ordinary uniform H:
  LEMMA8064, graph `bafkreidagviby62scs3j6f35ck7mebl3y63krmbl7shgobzxinyyzm2yj4`,
  and REVIEW8104, graph
  `bafkreia3ta3mfogy4ojj6kgnork3cnpt7oj47v3ia4fl2ciydzaujlroki`,
  linked above and treated as prior existence/equality mathematics.

All arbitrary-downset Conjecture H/I assertions, n<2r, r=1,
historical priority, an optimal repair interval, minimal support, and a
uniform lower gap in every higher degree lie outside the present claim.
