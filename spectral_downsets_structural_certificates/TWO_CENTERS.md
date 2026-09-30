# Capped certificates for two adjacent centers and independent leaves

Author: **six-downset-1**, role **researcher**, 2026-09-30.
Status: ordinary written infinite proof with separate exact rational checks.
No formalization, independent review, or historical priority is claimed.

## 1. Family and theorem

Let B_t, t>=1, be the rank-two downset containing empty, the singletons
of two centers a,b and t leaves c_i, the center edge e={a,b}, and the
spokes x_i={a,c_i}, y_i={b,c_i}. Equivalently its generating graph is
K_2 joined to t independent vertices. Then

```
N=3t+4,       s=t+2,       rho=s/(N-s)=(t+2)/(2t+2).
```

The two center stars attain s. Leaf stars have size three, attaining s
only at t=1, when the graph is K_3.

**Theorem.** Every B_t has the explicit rational symmetric matrix below,
with row sum one, zero entries on intersecting sets, and

```
-rho I <= M <= I.
```

Its upper endpoint is simple. Its lower endpoint has multiplicity
d(t)=3 for t>=2 and d(1)=4. Its Hoffman PSD rank is N-d(t).
This rank is maximal among H certificates whose nonempty core is centered;
no maximal-rank assertion for all H certificates is made.

Consequently every h-fold power on disjoint supports has a capped rational
H certificate with

```
N_h=(3t+4)^h,  s_h=(t+2)(3t+4)^(h-1),
rank((N_h-s_h)M_h+s_h I)=N_h-h*d(t).
```

Every finite mixed product of these families is also covered. If its leaf
counts are t_j, put t_*=min_j t_j and N_prod=product_j(3t_j+4). Then

```
s_prod=N_prod*(t_*+2)/(3t_*+4),
PSD nullity=sum_{j:t_j=t_*} d(t_j).
```

If t_*>=2, the only maximum intersecting families of this mixed product
are the two center-coordinate stars from each factor attaining t_*.
In particular B_t^h, t>=2, has exactly 2h maximum intersecting families.
If t_*=1 and c factors attain it, there are exactly 4c maximum families:
the lifts of the three coordinate stars or the three-edge triangle family
from one such factor.

The source [two_centers.py](two_centers.py) constructs the core and lifts
it. [verify_two_centers.py](verify_two_centers.py) checks the full matrices,
the direct weights, all invariant blocks and compact products exactly.
Finite checks validate the implementation; they are not the infinite proof.

## 2. Core and direct weights

Index the core C by all 3t+3 nonempty members. Set every diagonal to t+1,
and C[A,B]=-1 whenever distinct A,B intersect. The remaining unordered
entries are precisely:

| Disjoint pair type | C entry |
| --- | ---: |
| a,b | -1 |
| center singleton, leaf singleton | -1/t |
| distinct leaf singletons | -(t+1)/t |
| center singleton, opposite-center spoke | 2/t |
| leaf singleton, center edge e | (t+1)/t |
| leaf singleton c_i, spoke x_j or y_j, i!=j | 0 |
| spokes x_i,y_j, i!=j | 2/t |

There are no other disjoint nonempty pair types. Let
E=[-1^T;I], Q=ECE^T, L=Q+J, and M=(L-sI)/(N-s), as in
[PROOF.md, Section 2](PROOF.md). Counts give C1=0. For example its row
sums at a,e,c_i,x_i respectively are

```
(t+1)-1-1-t-1+2 = 0,
(t+1)-2-2t+(t+1) = 0,
(t+1)-(t-1)(t+1)/t-2/t+(t+1)/t-2 = 0,
(t+1)-(t-1)-1-1+2/t-1+2(t-1)/t-1 = 0.
```

Here the a row's four negative contributions include the center edge,
the t own-center spokes, and the t leaf-singleton weights. Rows at b,y_i
follow by symmetry. The two center-star indicators are also killed:
their within-star rows sum to (t+1)-(t+1)=0; on an outside center,
outside spoke, or leaf singleton the sums are respectively
-1-1+t*(2/t), 2/t-2+2(t-1)/t, and -1/t+(t+1)/t-1.

Centering makes Q's empty row zero. The direct entry formula for M is
therefore empty diagonal -1/2, empty-to-nonempty weight 1/[2(t+1)],
nonempty diagonals and intersecting positions zero, and these disjoint
weights:

| Disjoint nonempty pair type | M entry |
| --- | ---: |
| a,b | 0 |
| center singleton, leaf singleton | (t-1)/[2t(t+1)] |
| distinct leaf singletons | -1/[2t(t+1)] |
| center singleton, opposite spoke; or x_i,y_j with i!=j | (t+2)/[2t(t+1)] |
| leaf singleton, center edge | (2t+1)/[2t(t+1)] |
| leaf singleton, nonincident spoke | 1/[2(t+1)] |

Thus the only negative off-diagonal weights are between distinct leaf
singletons. The empty loop is signed and is allowed in Conjecture H.
At t=1 this is exactly the previously proved uniform three-coordinate
rank-two incidence matrix, after relabeling.

## 3. Complete invariant decomposition and both inequalities

The action S_2 x S_t swaps the centers and permutes the leaves. Split the
real nonempty coordinate space into center-antisymmetric and symmetric
spaces, then leaf-constant and leaf-centered spaces. The following are
orthogonal invariant spaces; their dimensions exhaust 3t+3.

The center-antisymmetric space is spanned by a-b and x_i-y_i. On the
leaf-centered part its scalar is

```
kappa=t+3+2/t,
```

with multiplicity t-1. On the orthonormal constant basis
(a-b)/sqrt(2), sum_i(x_i-y_i)/sqrt(2t), the block is

```
(1+2/t) [[t,-sqrt(t)],[-sqrt(t),1]].
```

It has eigenvalues zero and kappa. Thus this entire (t+1)-dimensional
space has positive eigenvalue kappa with multiplicity t and one zero.
For every t>=1, N-kappa=2t+1-2/t>0.

The symmetric leaf-centered space has dimension 2(t-1). It consists of
the leaf singleton level and the symmetric spoke level. On each common
leaf-centered coefficient direction its orthonormal block is

```
H_t = [[(t+1)^2/t, -sqrt(2)],
       [-sqrt(2), t+1-2/t]].
```

It is absent at t=1. For t>=2 the second diagonal is at least t and the
first is at least t+2, so det H_t >= t(t+2)-2>0. Both diagonals are
positive, proving positive definiteness. Its trace is 2t+3-1/t<N;
therefore each positive eigenvalue is strictly below N.

The remaining four-dimensional symmetric leaf-constant space has
orthonormal basis

```
(a+b)/sqrt(2), e, sum_i c_i/sqrt(t), sum_i(x_i+y_i)/sqrt(2t).
```

Its block is

```
T_t =
[[t,              -sqrt(2),       -sqrt(2/t),       (2-t)/sqrt(t)],
 [-sqrt(2),       t+1,            (t+1)/sqrt(t),    -sqrt(2t)],
 [-sqrt(2/t),     (t+1)/sqrt(t),   (t+1)/t,          -sqrt(2)],
 [(2-t)/sqrt(t),  -sqrt(2t),       -sqrt(2),          3-2/t]].
```

This is B K B^T, where

```
K = [[t,-sqrt(2)],[-sqrt(2),t+1]],
B = [[1,0],[0,1],[0,1/sqrt(t)],[-1/sqrt(t),-sqrt(2/t)]].
```

Since det K=t(t+1)-2=(t+2)(t-1), it is positive definite for t>=2
and PSD of rank one at t=1. B has full column rank. Consequently T_t
has rank two for t>=2 and rank one at t=1. Its trace is 2t+5-1/t<N,
because N-trace=t-1+1/t>0. Every nonzero eigenvalue is below N.

The dimensions (t+1)+2(t-1)+4=3t+3 prove completeness. Thus C>=0,
rank C=3t for t>=2 and rank C=2 at t=1, and all its eigenvalues are
strictly below N. No numerical eigenvalue estimate enters this argument.

For the cap use U=NI-J-C. Because C1=0, U acts as the scalar
N-(N-1)=1 on the constant direction and as NI-C on its orthogonal
complement. The previous strict bounds give U>0. The published identity
(N-s)(I-M)=EUE^T now proves M<=I and rank(I-M)=N-1, hence a simple
upper endpoint. C>=0 proves L=ECE^T+J>=0. Since the range of E is
orthogonal to constants and E has full column rank, rank L=rank C+1.
This gives exactly the stated lower-endpoint multiplicities.

## 4. Forced signs, centered rank and failed inherited templates

The sign statement has a converse obstruction. Take any centered H core
for B_t, not necessarily invariant. Choose its Gram vectors u_A, all
of squared norm t+1. The two maximum-star kernels give

```
u_a+u_e+sum_i u_xi=0,   u_b+u_e+sum_i u_yi=0.
```

Subtract their sum from the centered total to obtain sum_i u_ci=u_e.
Its squared norm is t+1. For t>=2 the average ordered distinct
leaf-singleton Gram entry must therefore be

```
[(t+1)-t(t+1)]/[t(t-1)]=-(t+1)/t<-1.
```

The average corresponding M weight is -1/[2t(t+1)]. In particular every
centered H certificate has at least one negative leaf-singleton weight.
Our invariant formula attains this forced average entrywise and keeps
every other off-diagonal weight nonnegative. This does not exclude
noncentered nonnegative certificates.

For t>=2 the nonempty all-one vector and the two maximum-star indicators
are three independent core kernel vectors: leaf-singleton rows force
the all-one coefficient to vanish, and the two center singletons force
the other coefficients to vanish. Every centered core thus has nullity
at least three. At t=1 all three stars are maximum; they and the all-one
vector are independent, as singleton and pair rows show. Nullity is then
at least four. The constructed core attains both bounds. This proves
the rank assertion within the explicitly stated centered class.

For t>=2, B_t is the uniform D_{t+2} with all leaf pairs deleted. The
[regular-deletion formula](DELETIONS.md) gives inherited top Gram eigenvalue
4t-4/t. It exceeds N precisely for integer t>=5. In particular at t=5,
N=19,s=7, the inherited matrix has top M eigenvalue 61/60; the present
matrix repairs it. The other inherited cases t=2,3,4 pass the cap.
For every t>=2, N=3s-2 has residue s-2, neither zero nor one, so
every single-partition certificate also fails the cap criterion.
Both are obstructions to constructions, not to H or capped feasibility.

The present centered matrix is also outside the entire convex hull of
partition lifts, even if some mixtures have the cap. For any partition of
the N-1 nonempty members into s classes with sizes m_j,

```
1^T C_partition 1=s*sum_j m_j^2-(N-1)^2.
```

Integer balancing gives a lower bound r(s-r) when N-1=sq+r, 0<=r<s.
For B_t, t>=2, q=2,r=t-1, so this functional is at least 3(t-1)>0
for every partition and every convex mixture. Our centered core has value
zero. This is an application of the balancing argument recently written in
six-downset-3's [regular-six proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
source commit 8edf860dda7f604eeb0e3267c761d5b5c78d63d5, not a new claim
for that general argument. It separates the constructed core from that
convex hull; it does not rule out capped partition mixtures for B_t.

A companion consequence of the same deletion formula strengthens the
comparison in [FRIENDSHIP.md](FRIENDSHIP.md). For F_k, k>=2, the deleted
graph inside D_{2k+1} is K_{2k} minus a perfect matching. It has
2k(k-1) edges, deletion line degree 4k-6 and deleted Gram row sum
2(k+2)/(2k-1). Its inherited top Gram eigenvalue is

```
4(k-1)(k^2+3k+1)/(2k-1).
```

Subtracting N=5k+2 gives
[(k-2)(4k^2+6k+5)+8]/(2k-1)>0. Hence every F_k with k>=2 fails
that inherited cap, whereas the published centered friendship core
succeeds. Again this is a uniform separation of two explicit constructions.

## 5. Products, exceptional-factor handoff and scope

Apply the [conditional tensor mechanism](PROOF.md) to the capped factors.
The functions s/N=(t+2)/(3t+4) and rho(t)=(t+2)/(2t+2) are strictly
decreasing in t. Because rho<1, every eigenvalue besides the simple upper
endpoint has magnitude strictly below one. A negative product attains the
largest rho exactly when one factor is at a lower endpoint with maximal
rho and all others are at one. Three or more negative factors decrease
its magnitude; additional positive factors different from one do too.
This proves all tensor rank formulas in Section 1 without constructing
exponentially large matrices.

Here is the equality classification, including the triangle boundary.
For an intersecting family with indicator x and size a, support and row
sums give, with z=x-(a/N)1,

```
z^T L z=a(s-a).
```

Thus H bounds its size by s, and a=s forces z into ker L. In a product
the lower eigenspace is the direct sum of eligible one-factor lower
eigenspaces, with constants on all other factors, by the endpoint argument
above. Therefore its maximum-family indicator has the additive form
x(A_1,...,A_h)=c+sum_j f_j(A_j), where only factors attaining t_* can
be nonconstant.

A Boolean-valued function of this additive form depends on at most one
factor. Indeed choose the independent minima of all f_j. Changing any
nonconstant factor to its maximum must change the output by exactly one,
since both outputs are Boolean and its range is positive. Two such factors
would change it by two, a contradiction. A proper nonempty family has a
nonconstant indicator, so it is the full lift of a subset in one eligible
factor. Its size forces that subset to have size s_j. It excludes the
factor's empty set, since the global empty tuple is excluded, and must be
intersecting: disjoint members in that factor, with empty members in every
other factor, would violate intersection in the product.

For B_t with t>=2, an intersecting rank-two family of size s=t+2>=4 has
a common point. To see the elementary rank-two fact, a singleton forces
a common point; otherwise three pairwise intersecting edges either have
a common point or form a triangle. A triangle has no fourth distinct
edge of size two meeting all three. If edges share a common point, an
edge omitting it meets at most two distinct edges of that star. Thus four
pairwise intersecting distinct sets of size at most two have a common
point. In B_t only the two center stars have the required size. In B_1,
a size-three family containing a singleton is one of the three stars;
without singletons it is exactly the three triangle edges. Their lifts
give precisely the counts in Section 1.

The standard Hoffman equality calculation and the principle of using
product kernels for extremizers also occur in the cited regular-six proof.
The present conclusion applies them to this new infinite rank-two factor
with its additional centered-kernel direction. It does not claim a new
general equality principle or a review of the companion result.

The stronger six-downset-3 certificate for D_* (N=32,s=11) now supplies
a capped factor with lower multiplicity six and simple upper endpoint.
See its [published capped proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/CAP_THEOREM.md),
source commit 145fedcf4a56269c398c1714c29567dce013ea23. The author checked
the base matrix and supplied the infinite proof; no independent review
is attributed to it here. Its exact base checker was replayed for this
handoff, including the hash and ranks, without rerunning the census.

As a concrete corollary, tensor B_t with D_*. Its family size is
32(3t+4), and its largest star is max(32(t+2),11(3t+4)). For t>=2,
the Hoffman PSD nullity of this tensor matrix is three for 2<=t<=19,
nine at t=20, and six for t>=21. Indeed the two endpoint ratios agree
exactly at t=20, since 32(t+2)-11(3t+4)=20-t. These are consequences
of the new factor and the existing tensor mechanism; no new claim about
the fractional optimum of this mixed family is made.

[Steiner-triple](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/CAPPED_PROOF.md)
and [two-STS(9)](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/TWO_STS9_PROOF.md)
capped matrices provide further complementary factors. An
[independent Steiner review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples_review1/REVIEW.md)
also gives endpoint and unequal-factor rank refinements in its own family;
that review does not certify the present result. Neither those structures
nor a finite census is a premise of this
two-center proof. The new family and the friendship repair are rank-two
structural results. General H, I and arbitrary rank-two cap feasibility
remain unresolved by this work.

## 6. Reproduction and literature

Run with CPython 3.11.2 and its standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify_two_centers.py --check
```

The compact expected output is [two_centers_expected.json](two_centers_expected.json).
The verifier compares the lifted core with the independent direct M entry
formula, checks support, row sums, actual stars, both full PSD bounds and
ranks, and checks rational basis images for every invariant block. It also
independently branches over every maximal clique of the base intersection
graph and compares the maximum families individually. In that branching,
chosen vertices form a clique; available vertices are all unprocessed
common neighbors and excluded vertices are its already processed common
neighbors. Branches on available neighbors outside a pivot neighborhood
exhaust all maximal extensions, because a maximal extension either contains
the pivot or contains a vertex not joined to it. Removing each processed
vertex from available and adding it to excluded prevents duplicates.
The initial state has every nonempty vertex available and none excluded,
so this gives complete base coverage, without an imported classification.
Its
finite input list and rejection controls are stated in that output.
The uniform positivity and completeness bridges are the written proof
above, not an inference from those finite checks. No numerical solver,
tolerance, omitted proof corpus or external classification is required.

Primary target: [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [current record](https://arxiv.org/abs/2609.28404) was refreshed on
2026-09-30 and lists v1 only, with H and I stated as conjectures. Its
classical Chvatal and projection-packing results are distinct. Standard
symmetry decomposition, Gram congruence and tensor spectra are not claimed
new in isolation. Bounded searches do not establish priority.
