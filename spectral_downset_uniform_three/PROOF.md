# Uniform rank-three downsets: all-orders capped certificates and the sharp four-point kernel

Author: **six-downset-3**, role **researcher**, 2026-09-30.

For every integer n>=5 this note constructs an explicit rational capped
Spectral Chvatal H matrix for

    D_n={A subset of [n]: |A|<=3},
    N=1+n+binomial(n,2)+binomial(n,3)=(n^3+5n+6)/6,
    s=1+(n-1)+binomial(n-1,2)=(n^2-n+2)/2.

Its lower slack L=(N-s)M+sI has rank **N-n**, the largest possible rank
among all real H matrices, and the unit eigenvalue of M is simple. The n
coordinate stars are its only maximum intersecting families.

At n=4 the H matrix is unique. It is an explicit capped matrix of maximal lower-slack rank
**7=N-8**, with simple unit endpoint. Exactly twelve families are maximum:
four stars and eight nonstars described below. This is a sharp exceptional
kernel, so the rank N-n conclusion is deliberately restricted to n>=5.

All nonempty finite mixed products of these factors also have explicit
rational capped H matrices, maximal lower-slack rank, and complete equality
classification. If n_* is the least factor order and c counts factors of
that order, their ranks and numbers of maximum families are respectively

| Critical factor order | Maximal rank | Maximum families |
| --- | ---: | ---: |
| n_*=4 | N_product-8c | 12c cylinders, including 4c stars |
| n_*>=5 | N_product-n_*c | n_*c coordinate stars |

These are written, unformalized proofs with exact rational-function identity
certificates and implementation checks. No independent review of this new
all-orders formula is claimed. General H and I remain open.

## 1. Definitions, attribution and the exact increment

An H matrix is real symmetric, indexed by the full downset including the
empty set, satisfies M1=1, vanishes whenever A intersects B, and satisfies
L=(N-s)M+sI positive semidefinite. The empty vertex has an allowed loop.
The additional cap M<=I is equivalent to L<=NI. Signed disjoint-pair
entries are allowed; the construction is not asserted nonnegative.

The problem and normalization are from
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [arXiv record](https://arxiv.org/abs/2609.28404), refreshed 2026-09-30,
lists v1 and leaves H and I open. Classical rank-three EKR bounds and
equality cases are prior literature, including
[Czabarka--Hurlbert--Kamat, Theorem 1.4](https://arxiv.org/pdf/1703.00494).
The star-only classical conclusion and the four-point exceptions are
credited context, not proposed new classical theorems.

Campaign inputs are the
[core lift and tensor mechanism](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph 7578; the
[maximal-rank star criterion](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
graph 7627; and the
[sparse rank trade and Boolean product classification](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
graph 7745. The latter mechanism has an
[independent review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md),
graph 7798. Its review does not establish this new input core.
For a self-contained argument, the needed lift, rank repair, and equality
steps are restated in sections 2, 5 and 7.

All downsets at n<=6 already have
[campaign finite H coverage](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/THEOREM.md). The n=7
uniform case is also one of the eleven
[point-transitive seven-point cases](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/POINT_TRANSITIVE_SEVEN_PROOF.md),
graph 7865, source 16cf47945715ac63afcfff4df4cf832e718aec47.
Its capped maximal rank was reproduced before this all-orders claim.
Those finite cases are baselines. The increment here is the all-orders
uniform rank-three rational formula, a complete harmonic reduction with
exact gap-one identities, the explicit rank-lifting parameter, and the
uniform product conclusion with its sharp four-point rank boundary.
No general priority is claimed for harmonic decomposition, Hoffman equality,
PSD perturbation, tensor spectra, or Boolean cylinders.

Harmonic analysis on Boolean slices has extensive primary literature; see
[Filmus, an orthogonal basis on a slice (2016)](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v23i1p23/pdf/)
and [Filmus--Mossel (2016)](https://arxiv.org/abs/1507.02713).
The short reduction below is proved directly and imports no representation
table. A bounded search did not locate this precise rational H formula;
that search is not a historical-priority guarantee.

## 2. The core and explicit formula

Index the nonempty vertices F first by layer, and let m=N-1. Put

    E=[-1_m^T; I_m],
    L=J_N+E C E^T,
    M=(L-sI_N)/(N-s),
    U=N I_m-J_m-C.

Here J is the all-ones matrix on its indicated domain. If C has diagonal
s-1 and entry -1 on distinct intersecting vertices, then M has the
required support. Since E^T1_N=0, L1_N=N1_N and M1_N=1_N.
The ranges of J_N and ECE^T are orthogonal, and E has full column rank.
Consequently L>=0 iff C>=0, and rank L=1+rank C. The exact identity

    E(N I_m-J_m)E^T=N I_N-J_N

gives N I_N-L=EUE^T. Thus U>0 gives the cap and a simple unit
eigenvalue of M. This reasoning includes the empty row and its loop.

For layers a,b in {1,2,3}, let D_ab be the rectangular disjointness matrix
between the two nonempty levels. Choose symmetric weights beta_ab and set

    C=sI_m-J_m+(beta_ab D_ab)_(a,b).

All prescribed core entries are then correct. For n>=6 use

    beta11=0,
    beta12=-(n-4)/(n-2),
    beta13=beta23=(n+3)/(n-3),
    beta22=2(4n-9)/((n-3)(n-2)),
    beta33=(n+1)/(n-5).                             (1)

At n=5 use the separate literal matrix

    beta=[[-1,1,3], [1,1,8], [3,8,0]].             (2)

The value beta33 in (2) is unused because two triples cannot be disjoint
on five points. Formula (1) has a true pole at n=5 and is not specialized
there by cancelling unrelated sector expressions.

Write x_i for the nonempty indicator of the i-th star. The six exact
linear equations for Cx_i=0 and C1_m=0 are

    sum_b beta_ab binomial(n-a-1,b-1)=s,
    sum_b beta_ab binomial(n-a,b)=N-1-s,       a=1,2,3.     (3)

In a row containing i the disjoint star sum is zero. In any other row of
size a it counts the b-sets containing i and disjoint from that row, giving
the first equation. Counting every disjoint b-set gives the second.
The right side is N-1-s because the core has N-1 vertices. Substitution
of (1) in Q(n), and direct substitution of (2), prove all six identities.

The n vectors x_i and 1_m are independent. A dependence evaluated at
singletons forces all star coefficients to be minus the constant
coefficient; evaluating at any pair forces that constant coefficient zero.
Thus the intended centered kernel has dimension n+1.

## 3. A complete harmonic reduction

For 0<=a<=3 let V_a be the real function space on the a-subsets, with its
ordinary counting inner product. Define raising and lowering by

    (U_a f)(A)=sum_(B subset A, |B|=a) f(B),
    D_(a+1)=U_a^T.

With U_-1 D_0 interpreted as zero, direct counting gives

    D_(a+1)U_a-U_(a-1)D_a=(n-2a)I_a.               (4)

The off-diagonal terms count the same exchange of one point; the two
diagonal counts differ by (n-a)-a. Hence U_a is injective for a<=2 and
n>=5, since

    ||U_a f||^2=||D_a f||^2+(n-2a)||f||^2.

Let H_0=V_0 and H_j=ker D_j for 1<=j<=3. Since D_j is surjective,

    dim H_j=binomial(n,j)-binomial(n,j-1),

with dim H_0=1. In particular H_3=0 when n=5.
For h in H_j and a>=j, define

    (W_(a,j)h)(A)=sum_(J subset A, |J|=j) h(J).

This equals U_(a-1)...U_j h/(a-j)!. Repeated use of (4) yields

    D_a W_(a,j)h=(n-a-j+1)W_(a-1,j)h,
    U_(a-1)W_(a-1,j)h=(a-j)W_(a,j)h,
    <W_(a,j)h,W_(a,j)k>=binomial(n-2j,a-j)<h,k>.   (5)

The first equation is interpreted as zero at a=j. The norm identity follows
inductively by adjointness and the two preceding equations. All its factors
are positive on nonzero sectors here. Different harmonic degrees are
orthogonal: moving the raising operators from the lower degree to the
other factor applies more lowering operators than are needed to reach
H_j, and the next lowering operator kills that vector. Finally

    sum_(j=0)^a dim H_j=binomial(n,a).

Thus these injective, orthogonal lifts exhaust each layer. This establishes
completeness, not just invariance of some candidate subspaces.

For h in H_j, the sum over j-sets containing any fixed R of size less than
j is zero, by iterating D_j h=0. Inclusion-exclusion therefore gives

    sum_(J subset A^c, |J|=j) h(J)=(-1)^j W_(a,j)h(A),

or zero if a<j. Counting b-sets disjoint from A that contain J proves

    D_ab W_(b,j)h=(-1)^j binomial(n-a-j,b-j)W_(a,j)h.    (6)

When the available complement is too small, the binomial count is zero.
For every nonzero sector here, its upper argument is nonnegative. The
otherwise singular j=3 sector at n=5 has multiplicity zero and is omitted.

For j>=1, every lifted vector has zero sum, so J_m kills it. In the
coefficient coordinates for layers a,b>=max(1,j), C is represented by

    (K_0)_ab=s delta_ab-binomial(n,b)+beta_ab binomial(n-a,b),
    (K_j)_ab=s delta_ab+(-1)^j beta_ab binomial(n-a-j,b-j), j>=1.   (7)

The sectors have sizes 3,3,2,1 and respective multiplicities dim H_j.
They are self-adjoint in the positive diagonal metrics

    G_j=diag_a binomial(n-2j,a-j),

because (5) describes the inherited inner product. Thus G_j K_j is
symmetric and each K_j has real eigenvalues. Equation (3) makes K_0 kill
(1,1,1) and (1,2,3), and makes K_1 kill (1,1,1). The first two follow
from C1_m=0 and C sum_i x_i=0; the latter from the zero-sum point-star
combinations. They can also be checked directly in (7).

## 4. Exact positivity and gap one

For n>=6 all following inequalities are strict:

* K_0 has one positive eigenvalue lambda_0, with 1<lambda_0<N-1.
* K_1 has a one-dimensional kernel and two eigenvalues in (1,N-1).
* Both K_2-I and (N-1)I-K_2 are positive definite in their inherited metric.
* The scalar K_3 lies in (1,N-1).

Here is the finite algebraic certificate for these infinite inequalities.
Let tau=trace K_1 and d be the sum of its principal two-by-two determinants.
The twelve margins checked by [verify.py](verify.py) are

| Names in the certificate | Exact quantities |
| --- | --- |
| C0_gap1, U0_gap1 | trace K_0-1; N-1-trace K_0 |
| C1_shift_trace, C1_shift_det | tau-2; d-tau+1 |
| U1_shift_trace, U1_shift_det | 2(N-1)-tau; (N-1)^2-(N-1)tau+d |
| C2_shift_diag, C2_shift_det | (K_2)_11-1; det(K_2-I) |
| U2_shift_diag, U2_shift_det | N-1-(K_2)_11; det((N-1)I-K_2) |
| C3_gap1, U3_gap1 | K_3-1; N-1-K_3 |

The explicit polynomial numerators and denominators after n=6+u are in
[POSITIVITY_CERTIFICATE.json](POSITIVITY_CERTIFICATE.json), with ascending
integer coefficients. Every numerator and denominator has nonnegative
coefficients and a strictly positive constant. Therefore every margin is
positive for **all real u>=0**. The checker independently derives (7),
forms each indicated trace/determinant over Q(u), and verifies exact
cross-multiplied identities with the certificate. It uses no interpolation,
numeric eigenvalue, CAS at runtime, or finite extrapolation.
For orientation,

    lambda_0=(n^2+5n-8)/2,
    tau=(n^3-2n^2-3n+8)/(n-2),
    d=n(n-4)(n-1)(n+3)(n^2-3n+4)/(4(n-3)(n-2)).

K_0's two independent null vectors and its positive trace give its exact
rank one. Write lambda,mu for K_1's other two real eigenvalues. The first
pair of K_1 margins are the sum and product of lambda-1,mu-1; positivity
of both forces both shifted eigenvalues positive. The upper margins are
the sum and product of N-1-lambda,N-1-mu, so both are positive too.
This also rules out any second zero eigenvalue. For K_2, conjugation by
G_2^(1/2) produces a symmetric matrix with the same diagonal entries and
determinant; the two-by-two Sylvester criterion applies to each shift.
The scalar K_3 margins finish the proof.

At n=5 the same reasoning uses ten literal positive margins. The nonzero
K_0 eigenvalue is 7; and

    K_1=[[12,-3,-9],[-1,9,-8],[-3,-8,11]],
    G_1=diag(1,3,3),
    trace K_1=32, d=245,
    K_2=[[12,8],[8,11]], G_2=I.

The ten margins in the table, omitting the absent K_3, are respectively
6,18; 30,214; 18,70; 11,46; 13,118. This separately verifies (2).

Combined with the complete decomposition, these arguments show for every
n>=5

    ker C=span(1_m,x_1,...,x_n),
    rank C=m-n-1,
    C>=P,                                              (8)

where P projects orthogonally onto this kernel's complement. For the upper
core U=N I_m-J_m-C, the constant vector has eigenvalue N-m=1. Every
other vector is orthogonal to the constant vector; U acts there as NI-C.
All positive C eigenvalues are below N-1, and its other eigenvalues are
zero. Hence

    U>=I_m.                                           (9)

These are exact lower and upper gap-one inequalities. They establish the
centered capped certificate of rank N-n-1 before the rank repair.

## 5. Explicit sparse rank repair

Let S=span(x_1,...,x_n). Define Delta to have zero diagonal and zero
intersecting entries; on disjoint nonempty vertices its only nonzero values
are

| Unordered layer sizes | Delta[A,B] |
| --- | ---: |
| 1,1 | (n-2)(n-3) |
| 1,2 | -(n-3) |
| 2,2 | 1 |

All rows involving triples vanish. This is the credited full-two-skeleton
trade. Each singleton row not containing a specified star coordinate has
one singleton contribution (n-2)(n-3) and n-2 pair contributions -(n-3),
which cancel. A pair row not containing it has one singleton contribution
-(n-3) and n-3 pair contributions 1. Thus Delta kills S. Direct row
counts give

    delta=1_m^T Delta 1_m=n(n-1)(n-2)(n-3)/4>0,
    ||Delta||_2<=B=3(n-1)(n-2)(n-3)/2.

The bound is the maximum absolute row sum, attained at a singleton.
Set

    epsilon=1/[12(n^2+5)(n-1)(n-2)(n-3)],
    C'=C+epsilon Delta.                              (10)

Then

    epsilon=delta/(8m B^2),
    epsilon B=1/[8(n^2+5)]<=1/4, epsilon<=1.

For completeness, let h be the orthogonal projection of 1_m onto S^perp.
It is nonzero because 1_m is outside S, and ||h||^2<=m. On
S^perp=span(h) plus R=(S+span(1_m))^perp, C' has the block form

    [epsilon a, epsilon b^T; epsilon b, C_R+epsilon D_R],
    a=delta/||h||^2>=delta/m, ||b||<=B, ||D_R||<=B.

By (8) its lower-right block is at least (1-epsilon B)I>=3I/4,
and its inverse has norm at most 2. Its Schur complement is at least

    epsilon(a-2epsilon B^2)
       >=epsilon(delta/m-delta/(4m))>0.

Thus C' is positive definite on S^perp and kills exactly S. By (9),

    U'=U-epsilon Delta>=(1-epsilon B)I>=3I/4>0.

The trade changes only allowed disjoint entries. The lift in section 2
therefore gives the claimed rational H matrix, with

    rank L'=1+(m-n)=N-n,
    rank(NI_N-L')=N-1.                              (11)

All denominators are nonzero in the stated ranges. This repair is derived
from the proved gaps, not from small-order numerical feasibility.

Every real H matrix has rank L<=N-n. For an intersecting indicator y of
size a, support and L1=N1 give

    (y-(a/N)1)^T L(y-(a/N)1)=a(s-a).                 (12)

Thus a<=s, and at equality its centered indicator belongs to ker L.
The n stars supply n independent such vectors: evaluating a dependence
first at the empty vertex and then at each singleton eliminates all
coefficients. Therefore (11) attains the universal rank upper bound.
At maximal rank a maximum indicator has centered form
sum_i b_i(1_star_i-(s/N)1). The empty equation gives sum_i b_i=1;
singleton equations give b_i in {0,1}. Precisely one is one, so it is
that star. This recovers the credited classical equality by a spectral
criterion.

## 6. The sharp four-point boundary

At n=4, D_4 consists of every proper subset, with N=15 and s=7. Its
fourteen nonempty members form seven complementary pairs. Let P_bin have
entry one when two members lie in the same such pair, including the
diagonal, and zero otherwise. The centered core

    C=7P_bin-J_14

has rank 6, its positive eigenvalues are all 14, and it kills the constant
vector. Its upper core U=15I-J-C=15I-7P_bin is positive definite, with
eigenvalues 1 and 15. Its lift gives exactly

    M[empty,empty]=-3/4,
    M[empty,A]=M[A,empty]=1/8 for nonempty A,
    M[A,A^c]=7/8 for nonempty A,
    all other entries zero.                        (13)

The spectrum is 1 once, 7/8 six times, and -7/8 eight times. This follows
by splitting the seven pairs into within-pair antisymmetric vectors, pair
constants of total zero, and the remaining empty/constant two-dimensional
space. The checker also verifies the full integer characteristic polynomial
of 8M exactly. Thus its lower slack has rank 7 and its unit eigenvalue is
simple.

Write S_i for the i-th coordinate star. Define B_i to be all four triples
together with the three pairs containing i, and T_i to be all four triples
together with the three pairs avoiding i. These twelve families are
distinct, intersecting and of size seven. They exhaust the maximum
families. A maximum family containing a singleton must be its star.
Otherwise it contains only pairs and triples. A pairwise-intersecting
edge set of K_4 has at most three edges, and at size three is either an
edge star or a triangle. Hence size seven forces all four triples and one
of those eight edge families.

The eight centered indicators of S_i,B_i are independent. In a dependence,
the empty row makes the sum of coefficients zero. Singleton rows make
every S_i coefficient zero. Pair rows then give b_i+b_j=0 for all six
pairs, forcing all B_i coefficients zero. These eight directions belong
to ker L for **every real H matrix**, by (12). Thus rank L<=15-8=7,
and (13) attains it. The other four directions add no obstruction:

    1_(T_i)=(1/2)sum_j 1_(B_j)-1_(B_i).

The same relation holds after centering. There is an additional useful
identity, with 1_F zero at the empty vertex:

    1_F=sum_i 1_(S_i)-(1/2)sum_i 1_(B_i).

After centering this is

    e_empty-(1/N)1=-sum_i z_(S_i)+(1/2)sum_i z_(B_i).

Thus **every H matrix is necessarily centered**: these forced null vectors
give L e_empty=1_N, and fix its entire empty row to (13). The empty
direction is already in the eight-dimensional nonstar/star span, so it
cannot be counted as a ninth independent obstruction.

In fact (13) is the unique real H matrix. The forced-star and forced-B_i
equations have the form M1_I=(7/8)(1-1_I). For a nonempty pair A and
i outside A, the only member of B_i disjoint from A is A^c. Its equation
therefore fixes M[A,A^c]=7/8. The star equations at those two outside
coordinates then force both possible pair/singleton entries to zero.
For a triple the only nonempty disjoint vertex is its complementary
singleton, so that entry is 7/8. Finally the star equation for a singleton
and another coordinate, with the now fixed triple and pair entries, forces
their singleton/singleton entry to zero. This exhausts all supported
nonempty entries; the empty row was fixed above. Uniqueness requires no
extra upper-cap hypothesis.

The full-two-skeleton trade also has a sharp obstruction here. For any
H core, y=1_(B_i) on F satisfies Cy=0, but

    y^T Delta y=0,   ||Delta y||^2=15>0.

Indeed its pair subfamily is intersecting, and Delta is zero on triples.
Delta y is zero at singleton i, is -2 at the other three singletons, is
1 at the three pairs avoiding i, and is zero elsewhere. Thus for every
real epsilon!=0, (C+epsilon Delta)y is nonzero while its quadratic form
on y remains zero. A PSD matrix cannot have that property. This does not
exclude alternative trades at other orders or refute H; it explains why
the exact-kernel premise of section 5 fails at this boundary.

The classical twelve-family description is prior context; these universal
centering, uniqueness, rank and fixed-trade deductions explain its spectral
consequences. The source check also exhausts all 16,384 subsets of the
fourteen nonempty vertices, recovers the twelve maxima, and checks that the
40-variable homogeneous support/row/forced-family system has nullity zero.

## 7. Arbitrary finite products, with exact ranks and equality

Every factor has 0<s<N/2, since

    N-2s=(n-1)(n-2)(n-3)/6>0 for n>=4.

Moreover its star density strictly decreases with n. With

    p_n=3(n^2-n+2)/[(n+1)(n^2-n+6)],

direct subtraction gives

    p_n-p_(n+1)
      =3(n-1)(n-2)(n^2+3n+6)
       /[(n+1)(n+2)(n^2-n+6)(n^2+n+6)]>0.          (14)

The checker verifies this identity over Q(u) at n=4+u; every factor is
positive throughout u>=0. Thus precisely the factors of minimum order are
critical, with maximum density p=p_(n_*).

For factors on disjoint ground sets form M_product by tensoring their
matrices. Its support and row sums follow entrywise; the actual largest
star size is s_product=p N_product. Set rho_j=s_j/(N_j-s_j), all less
than one, and rho=max rho_j. A base eigenvalue lies in [-rho_j,1], with
simple eigenvalue 1 and every other eigenvalue of absolute value below one.
Any negative tensor eigenvalue is at least -rho. Equality can occur only
with one critical factor at its lower endpoint and all other factors at
their unit endpoint: any extra nonunit factor strictly decreases magnitude.
Thus the tensor is capped H, with simple unit endpoint and lower-slack
nullity the sum of critical base nullities.

By sections 5 and 6 those nullities are n_j for n_j>=5 and 8 for n_j=4.
This proves the displayed product ranks. The centered maximum-family
indicators in each critical factor span its kernel; lifting them as
cylinders gives independent forced directions in every product H matrix.
Spans from distinct factors are orthogonal because each is mean zero and
depends on only its own factor. Hence these tensor ranks are maximal
among **all real H matrices**, not just tensor constructions.

To classify equality, a maximum indicator is necessarily of the form

    y(A_1,...,A_k)=p+sum_(j critical) f_j(A_j),

with each f_j of mean zero. If a summand is nonconstant, fixing every other
coordinate shows that its range width is exactly one, because y is Boolean.
On the full Cartesian domain the width of the sum is the sum of individual
widths, since extrema can be chosen independently. Consequently at most
one summand varies; at least one does because 0<p<1. So the family is a
cylinder over one critical factor. Its base size is s_j; it excludes the
empty set by the global empty coordinate. A disjoint pair in the base
would lift to a disjoint pair with every other coordinate empty, so its
base is intersecting and maximum. Conversely each base maximum gives
an intersecting cylinder of the correct size. Distinct bases and distinct
critical factors give distinct cylinders.

Sections 5 and 6 now give n_*c stars or 12c cylinders, respectively.
No dense product matrix or bounded factor count is used to prove these
quantified assertions. The ordinary Boolean and tensor arguments are
credited mechanisms, restated here to close the completeness bridge.

## 8. Exact verification, reproduction and trust boundary

[verify.py](verify.py) uses CPython 3.11+ and its standard library only.
It derives the twelve infinite positivity identities independently from
(1) and (7), with rational-function arithmetic implemented over Q(u).
Polynomial Euclidean gcd, exact division and cross multiplication verify
the identities; no CAS, interpolation or floating arithmetic is required.
There are 57 symbolic identities, including (3), metric symmetry, null
vectors, trade-parameter identities and (14).

Separately, at n=5,6,7,8 it constructs all vertices, the full dense cores,
both lifts, and their upper slacks. It checks downward closure, actual star
sizes, every support entry, all row sums, kernels, trade totals and norms,
and every stated rank by exact integer Bareiss Schur elimination. It also
constructs the exact kernel-complement projector from its rational Gram
inverse and verifies C>=P and U>=I directly on each full matrix. Negative
Schur diagonals or a zero diagonal with nonzero residual cause rejection;
all fraction-free divisions must be exact. It also computes complete
integer bases of every H_j and checks all lifted norm identities, sector
orthogonality, dimensions and every disjointness action for every basis
vector, including each full core block action. This direct finite audit is independent of the rational-function
coefficient calculation, but does not substitute for the all-orders proof
of completeness in section 3.

The n=4 audit verifies (13), its entire characteristic polynomial, the
independent forced-kernel Gram rank, forced centering and linear uniqueness,
the zero-form/nonzero-image trade obstruction, and all 2^14 subsets. Seven
rejection controls cover coefficient corruption, a nonpositive denominator
constant, indefiniteness, zero-form/nonzero-image, asymmetry, a damaged star
equation and the excluded rational pole. All checks survive Python -O.
[RESULTS.json](RESULTS.json) records deterministic matrix hashes and exact
parameters. Hashes serialize reduced rational entries as strings in compact
JSON. Vertex order is by increasing size, then lexicographic increasing
tuples of point indices; this order is distinct from sorting binary masks.

From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O spectral_downset_uniform_three/verify.py \
  --check spectral_downset_uniform_three/RESULTS.json
```

A completed optimized-Python check took 8.89 seconds and peaked at 26,196 KiB
RSS with one process, one CPU-intensive job, and native threads one. These
are measured local costs, not runtime guarantees.

The optional [derive.py](derive.py), requiring SymPy 1.14.0, regenerates the
positivity certificate from the six-variable centered linear system over
Q(n,t). It is discovery/reproduction code. Its output is checked by the
standard-library verifier; CAS correctness is not required for accepting
the published coefficient identities. No external fixture is needed for
the production check.

The trust boundary consists of these ordinary unformalized mathematical
arguments, inspected checker code, Python integer/Fraction arithmetic, and
the compact coefficient input whose exact identities are verified. The
finite validations are not claims to exhaustive arbitrary downset coverage.
No solver timeout, UNKNOWN, memory kill, numerical feasibility, private
data, large proof corpus, or unspecified analytic-completeness bridge is
used as proof. No historical-priority or independent-review claim is made.
