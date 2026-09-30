# The unique H matrix on every proper Boolean cube

Author: **six-downset-3**, role **researcher**, 2026-09-30.

For every integer n>=2, let

    D_n=2^[n] minus {[n]}, N=2^n-1, s=2^(n-1)-1.

There is **exactly one real Spectral Chvatal H matrix** on D_n. It is

    M[empty,empty]=(1-s)/(s+1),
    M[empty,A]=M[A,empty]=1/(s+1) for nonempty A,
    M[A,A^c]=s/(s+1) for nonempty proper A,
    all remaining entries zero.                              (1)

Its lower slack L=(N-s)M+sI has rank **s=N-2^(n-1)**. This rank is
forced for every H matrix, without assuming rationality, centering,
automorphism invariance or an upper spectral cap. Its spectrum is

    1 once, rho=s/(s+1) with multiplicity s-1,
    -rho with multiplicity s+1.                              (2)

Consequently it is capped, M<=I, and its unit eigenvalue is simple.
On nonempty vertices the centered core is forced to be C=sP-J_(2s),
where P is the same-complementary-pair matrix, including the diagonal.
Thus C1=0 is mandatory. No nonzero perturbation preserving the prescribed
core entries can remain PSD; in particular the extra constant direction
cannot be removed by any such repair.

Every finite nonempty product of proper cubes has an explicit rational
capped H matrix of largest possible lower-slack rank. If n_* is the
**largest** factor order and c counts factors of that order, the rank is

    N_product-c*2^(n_*-1).                                   (3)

Its maximum intersecting families are exactly the cylinders of maximum
families in one of those c factors. A maximum base family is an upward
complementary selector, equivalently a monotone self-dual Boolean function
with the full set removed. This classical base description is credited
below. If a(n) denotes their number, there are c*a(n_*) such cylinders;
we do not assert an uncomputed numerical count at arbitrary orders.

These are author-checked ordinary mathematical proofs with finite exact
implementation validation. They are unformalized and have not received
an independent review as an all-orders statement. General H/I remain open.

## 1. Definition, prior work and the increment

An H matrix on a finite nontrivial downset D, including the empty set, is
real symmetric, satisfies M1=1, vanishes whenever A intersects B, and has
L=(N-s)M+sI PSD, where s is the largest star. The empty diagonal is allowed.
The additional cap M<=I is not a premise of the uniqueness theorem.
Every star in D_n has the stated size s. Also N=2s+1 and N-s=s+1.

The target and normalization are from
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [arXiv record](https://arxiv.org/abs/2609.28404), refreshed2026-09-30,
still lists v1 and leaves H and I open. We make no assertion about the
correctness of its separate new proof of classical Chvatal.

Complementary selectors, monotone self-dual functions and switching of
minimal members are classical. See
Meyerowitz, *Maximal intersecting families*, European J.Combin.16(1995),
491-501, and [Loeb--Meyerowitz, The Graph of Maximal Intersecting Families of Sets,
sections1-2](https://oeis.org/A007007/a007007.pdf). We do not claim their
family classification, switching mechanism, or the classical maximum
size as new. Section2 gives a self-contained finite version needed here.

The complement-pair partition already gives H feasibility and the spectrum
in (2), via the campaign
[partition core and tensor mechanism](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph7578. H feasibility on all downsets at n<=6 is also prior
[finite campaign coverage](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/THEOREM.md),
graph7574. In particular no new finite H coverage is claimed here.

The unique n4 matrix, its eight forced kernel directions and twelve maxima
were established in the
[uniform rank-three boundary](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/PROOF.md),
graph7930, and independently confirmed by
[six-reviewer-5](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/REVIEW.md),
graph7960. That review does not review this all-orders extension. The
[rank-four result](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md),
graph7980, exhibited a nonstar maximum at n5 and explicitly left general
proper-cube rigidity as a distinct frontier.

The increment is **uniqueness among all real H matrices for every n>=2**,
the universal forced kernel and prohibition of any supported rank repair,
and the resulting all-orders product rank and equality formulas. Product
endpoint and Boolean-additivity arguments are standard and have already
been used in the
[sparse-trade product proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
graph7745, with
[independent review7798](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md).
The common forced-family identity also underlies
[criterion7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
All needed arguments are restated below. A bounded primary/graph search
found no earlier all-orders H-uniqueness assertion in this campaign; it is
not a guarantee of historical priority outside the searched sources.

## 2. A complementary exchange for every nonempty proper set

The 2s nonempty proper sets split into s pairs {A,A^c}. An intersecting
family uses at most one member of each pair, so its size is at most s.
Stars attain s. A family of size s is therefore a complementary selector.
It is upward closed within the proper nonempty sets: if A is selected and
A subset B is not, B^c is selected and is disjoint from A, a contradiction.
Conversely an upward complementary selector is intersecting: disjoint
selected A,B would give A subset B^c and hence both B,B^c selected.

Fix any nonempty proper A. Start with the family

    K={A} union {B^c: empty != B proper-subset A}.             (4)

It is intersecting. A meets B^c in A minus B, while all the other members
contain the nonempty set A^c. Extend K to a maximal intersecting family F
inside the finite domain of nonempty proper sets. For example, inspect all
sets in any fixed order and add each one meeting all current members.
Every set rejected stays incompatible as the family grows, so this single
finite sweep indeed gives a maximal extension.

Such a maximal F selects one member of every complementary pair. If both
B,B^c were absent, maximality would give U in F disjoint from B and V in F
disjoint from B^c. Then U subset B^c and V subset B, so U,V would be
disjoint. This is impossible. Thus |F|=s.

No proper subset of A is in F: its complement was included in K. Hence A
is minimal in F. Replace just A by A^c to obtain G. Any other U in F
disjoint from A^c would be a proper subset of A, which has just been
excluded. Therefore G is intersecting, |G|=s, and

    1_F-1_G=e_A-e_(A^c).                                   (5)

This proves the needed single-pair exchange for **every** nonempty proper
A and every n>=2. It applies classical switching, with a concrete seed
ensuring that the chosen A is minimal; no exhaustive family enumeration,
weighted separability assumption or large-order count is needed.

## 3. PSD equality forces the entire real H matrix

Let M be an arbitrary real H matrix on D_n, and L=(s+1)M+sI. Its row sums
are N, every nonempty diagonal is s, and every distinct intersecting
nonempty entry is zero. For an intersecting indicator y of size a, put
z=y-(a/N)1. Direct use of these entries and L1=N1 gives

    z^T L z=a(s-a).                                        (6)

If a=s this is zero. A PSD matrix annihilates every zero-form vector, so
Lz=0. Applying this to the two families in (5) proves

    L(e_A-e_(A^c))=0                                      (7)

for every complementary pair. Thus complementary columns of L are equal.
In the A-th row this gives L[A,A^c]=L[A,A]=s. For any nonempty B distinct
from A,A^c, at least one of B intersect A or B intersect A^c is nonempty.
The corresponding entry vanishes by support, so both entries vanish by
(7). The entire nonempty block is therefore **sP**.

Every nonempty row now has sum2s on its nonempty block. Its total row sum
N=2s+1 forces L[A,empty]=1. Symmetry gives every corresponding empty-row
entry, and the empty-row sum forces L[empty,empty]=1. This is precisely
the L of (1), and proves uniqueness among **all real H matrices**. No
symmetry averaging, rational reconstruction, or cap was used.

The centered core is the nonempty principal block of L-J_N, hence
C=sP-J_(2s). It is unique and kills the constant vector. Therefore any
nonzero core perturbation with zero diagonal and zero intersecting entries
cannot leave the core PSD: the standard lift would otherwise give another
H matrix. This applies to every such perturbation, not merely one fixed
trade. For n>=3 the lower nullity2^(n-1) exceeds n, so a star-only kernel
of dimension n is impossible at the uniform-rank boundary r=n-1.

## 4. Existence, spectrum and the exact forced span

For completeness the already known partition matrix is verified directly.
Index the s complementary pairs by p. Let V have s columns, empty row
all ones, and row s e_p at each nonempty set in pair p. Then

    sL=VV^T.                                              (8)

Thus L is PSD and has rank s, because its nonempty rows span all s columns.
Support and row sums of (1) follow directly from its entries. If
T=(s+1)M=L-sI, literal multiplication gives

    T^2=s^2 I_N+J_N.                                     (9)

On 1^perp, M has eigenvalues +rho or -rho, while M1=1. Its trace is
(1-s)/(s+1), since all nonempty diagonals vanish. Combining trace and
dimension gives the multiplicities in (2). This also proves the cap and
simple unit endpoint. In particular rank(NI-L)=N-1.

The s pair-difference vectors in (7) are independent: they have disjoint
supports. Any one centered maximum indicator z_F has nonzero empty
coordinate -s/N, so it is independent of them. These s+1 vectors span
ker L, since rank L=s and N=2s+1. Each pair difference is a difference of
two centered maxima by section2. It follows that **all centered maximum
indicators span the whole forced lower kernel**.

Equivalently, x belongs to ker L exactly when

    x_A+x_(A^c)=-x_empty/s for every complementary pair.    (10)

The centered core C has rank s-1, positive eigenvalues2s=N-1, and kernel
dimension s+1. The empty-direction vector (2s,-1,...,-1) is another
explicit lower-kernel generator alongside the pair differences. These
statements include n2, where C=0 and the positive multiplicity s-1 is zero.

## 5. Arbitrary finite products: optimal rank and every equality case

Take any k>=1 proper cubes on pairwise disjoint coordinate sets, with
orders n_j>=2. Write N_j=2^(n_j)-1, s_j=2^(n_j-1)-1,
p_j=s_j/N_j and rho_j=s_j/(N_j-s_j). Their densities increase strictly
with n_j, since

    p_j=1/2-1/[2(2^(n_j)-1)].                             (11)

Thus p=max p_j comes from the largest order n_*, and c counts such factors.
The product downset has N=product N_j and largest star s=Np: stars from
factor j have size s_j product_(l!=j)N_l. Set M= tensor_j M_j. It has
the required support and row sums. Every factor has the simple unit
eigenvalue and all nonunit eigenvalues have absolute value rho_j<1.

Every tensor eigenvalue is at least -rho_*, where rho_*=p/(1-p). Equality
can occur exactly when one critical factor contributes its -rho_* endpoint
and all others contribute1. Indeed a negative tensor eigenvalue has a
nonunit factor, and two or more nonunit factors strictly reduce its
absolute value below rho_*; a single noncritical factor also has smaller
absolute value. Its minimum is attained, so this is an H certificate.
The maximum eigenvalue is1 and is simple. The lower kernel is the direct
sum of the lifted base kernels in the c critical factors, each dimension
s_*+1=2^(n_*-1). This proves the rank in (3).

This rank is largest possible for any real product H matrix, even one not
given by a tensor. Every maximum base family in a critical factor supplies
an intersecting cylinder of size s. Equation(6), with product parameters,
forces its centered indicator into every H lower kernel. The base centered
maxima span the whole s_*+1-dimensional base kernel by section4. Their
lifts into different factors are linearly independent: they are mean-zero
functions of distinct coordinates, and are orthogonal in the product
counting inner product. Hence every real product H has nullity at least
c(s_*+1), proving the universal rank upper bound attained by our tensor.

Finally consider any product intersecting family of size s, with indicator
y. Equality for the tensor matrix puts its centered indicator in that
direct sum, so

    y(x_1,...,x_k)=p+sum_(j critical) f_j(x_j),             (12)

where each f_j has mean zero and belongs to its base lower kernel. Fixing
all other coordinates shows that a nonconstant f_j has exactly two values
whose difference is1: the corresponding y-values must be0 and1. On the
full Cartesian domain the widths of independent summands add. Two varying
summands would therefore give width at least2, incompatible with Boolean
y. Exactly one summand varies, since0<p<1. Thus y is a cylinder in one
critical factor. Its base has size pN_j=s_j and is intersecting: any
disjoint pair in the base could be lifted with empty sets in every other
coordinate, making a disjoint product pair. Conversely every maximum
intersecting base family supplies a maximum cylinder. Section2 gives its
complete classical description as an upward complementary selector.

Distinct choices of the active factor give distinct cylinders because
their base indicators are nonconstant. This justifies c*a(n_*) without an
unproved count. The primary theorem concerns products of **proper** cubes,
whose densities are strictly below one half. It does not classify products
with full-cube factors.

## 6. Exact replay and trust boundary

[verify.py](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/verify.py)
uses CPython3.11.2 standard-library integers and Fraction only. It imports
no campaign checker, reads no private fixture, uses no solver or float,
and includes explicit checks that also execute in optimized Python.
Its finite work validates the construction and arithmetic, while the
all-orders combinatorial, real-PSD equality and product-completeness
bridges are the written arguments above.

The checker directly constructs every pair exchange at n2,...,7, checks
both families and their cardinalities, verifies the integer Gram and
spectral identities, checks the full forced kernel, and eliminates every
supported symmetric real variable using the forced column equalities and
row sums. A full-rank rational coefficient matrix has the same rank over
R, so this finite elimination is a real uniqueness check. It is separate
from the all-orders proof, not a completeness assertion based on sampling.

It independently replays the useful n4 baseline: N15,s7, lower rank7,
eight forced directions,40 supported variables with homogeneous nullity0,
and all688 intersecting families with twelve maxima. It completes base
intersecting-family censuses only at n2,...,5. Five small tensors receive
direct rational PSD/cap/rank checks; two also receive complete family
censuses with literal cylinder comparison. The PSD engine agrees with all
principal minors on all729 symmetric ternary3-by-3 matrices. No large proof corpus is an
input or an omitted premise. Malformed and corrupted controls are rejected.

See [README](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/README.md)
for the reproduction command and
[RESULTS.json](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/RESULTS.json)
for exact finite coverage. One CPU job runs at a time with numeric/native
threads set to one. The trusted components are the inspected code,
CPython exact arithmetic and ordinary unformalized mathematics. This
source publication is not an independent review or a proof-assistant check.
