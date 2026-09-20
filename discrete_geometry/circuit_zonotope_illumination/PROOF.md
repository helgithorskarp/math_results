# Circuit zonotopes: illumination is Boolean-chain covering

## Definitions and statements

For a full-dimensional convex body K in a real vector space V, a nonzero
direction w **illuminates** x in the boundary of K if x + epsilon w belongs
to the interior of K for some epsilon > 0. Write I(K) for the minimum number
of directions illuminating its entire boundary. Write I_f(K) for fractional
illumination: the infimum of the total mass of a finite nonnegative Borel
measure on directions whose mass on the directions illuminating each boundary
point is at least one. Directions can equivalently be normalized to a sphere.

A **linear circuit** is a list of k >= 2 nonzero vectors of rank k-1 with
every proper sublist independent. Its unique dependence, up to scaling, has
all coefficients nonzero. All dimensions and interiors below are taken in
the stated span. Generator signs and lengths are arbitrary unless specified.

**Theorem 1 (circuit formula and simultaneous illumination).** If g_1,...,g_k
form a linear circuit, then

\[
 I\left(\sum_{i=1}^k[0,g_i]\right)
 =I_f\left(\sum_{i=1}^k[0,g_i]\right)
 =\binom{k}{\lfloor k/2\rfloor}.
\]

After the normalization below, the vertices have labels given by the
nonempty proper subsets of [k]. A collection of these vertices is
simultaneously illuminated by one direction if and only if its labels form
an inclusion chain. The proof gives explicit optimal directions and a
matching set of pairwise antipodal vertices.

**Theorem 2 (independent circuits in an arbitrary zonotope).** Suppose
Z = sum_{i=1}^m [0,g_i] has rank d >= 1 and its generators contain circuits
C_1,...,C_s of sizes k_1,...,k_s, whose spans form an internal direct sum.
Set r = sum_j (k_j-1). Then

\[
 I_f(Z)\le I(Z)\le
 2^{d-r}\prod_{j=1}^s\binom{k_j}{\lfloor k_j/2\rfloor}.
\]

The empty circuit collection is permitted. The bound is sharp for every
such dimension and circuit-size list: equality for both invariants holds
for the direct product of these circuit zonotopes and d-r nondegenerate
segments. This is a sharpness statement for the stated data, not an equality
claim for every larger zonotope containing the circuits.

**Corollary 3 (cactus graphical zonotopes).** Let G be a connected finite
simple cactus with at least one edge: every edge belongs to at most one
simple cycle. Let b be its number of bridges and k_1,...,k_s its cycle lengths.
For arbitrary positive edge weights a_e and arbitrary edge orientations,
in the sum-zero subspace of R^{V(G)}, put

\[
 Z_G=\sum_{e=(u,v)\in E(G)}[0,a_e(e_u-e_v)].
\]

Then

\[
 I(Z_G)=I_f(Z_G)=2^b\prod_{j=1}^s\binom{k_j}{\lfloor k_j/2\rfloor}.
\]

## 1. Normalize the dependence, not the body

Choose a dependence sum_i alpha_i g_i = 0, with every alpha_i nonzero.
Replacing g_i by sign(alpha_i) g_i only translates its segment and hence
the whole zonotope; translation does not change illumination. Set

\[
 v_i=\alpha_i g_i,\qquad \ell_i=1/|\alpha_i|>0.
\]

The translated body is Z = sum_i [0,ell_i v_i], where sum_i v_i = 0 and
any k-1 of the v_i are independent. No affine equivalence between different
length choices is being assumed.

Let A:R^k -> V send the i-th coordinate vector to v_i. Then
ker A = R(1,...,1). Thus a point x = Aa belongs to Z exactly when some
t satisfies 0 <= a_i+t <= ell_i for every i. Intersecting these intervals
for t gives the equivalent complete inequality description

\[
 f_{ij}(x):=a_i-a_j\le\ell_i\qquad(i\ne j).                 \tag{1}
\]

Each f_ij is well-defined on V because a_i-a_j is invariant under adding
a constant vector. It has evaluations 1 at v_i, -1 at v_j, and 0 at the
remaining v_l. Equality in (1) fixes the i-th segment at its upper endpoint
and the j-th at its lower endpoint and leaves k-2 independent generators
free. Consequently every inequality in (1) is a facet inequality. In
particular, x is interior precisely when all inequalities in (1) are strict.

## 2. Vertices and strict orders

For each nonempty proper S subset [k], define

\[
 p_S=\sum_{i\in S}\ell_i v_i.
\]

These are all the vertices, with distinct labels. To see they are vertices,
choose real numbers b_i positive on S and negative off S with sum_i b_i=0.
Since im A^* is the sum-zero hyperplane, these are the evaluations of some
covector on the v_i. Its unique maximizing point on Z is p_S. Distinct
labels give distinct vertices: the difference between two endpoint vectors
cannot be constant in every coordinate unless the labels agree, or they
are the two excluded endpoint labels. For nested proper labels the
difference has a zero coordinate and a nonzero coordinate; for incomparable
labels it has both signs.

Conversely, Z is the convex hull of the images of all box corners, so
every vertex is one of those images. The all-zero corner and the all-upper
corner have interior images: respectively add or subtract a sufficiently
small constant from every coordinate to obtain a point in the open box.
Equation (1) also verifies their interior status directly. This establishes
the vertex description, including k=2.

At p_S, the active inequalities in (1) are exactly those with i in S and
j outside S. For a direction w = Ac, the strict facet criterion therefore is

\[
 w\text{ illuminates }p_S
 \quad\Longleftrightarrow\quad
 c_i<c_j\quad\text{for every }i\in S,\ j\notin S.             \tag{2}
\]

Indeed, active inequalities must decrease strictly; when they do, a small
enough positive step also preserves every originally strict inequality.
The choice of representative c does not affect its coordinate differences.

If S and T are incomparable, choose i in S minus T and j in T minus S.
Illuminating p_S requires c_i<c_j, while illuminating p_T requires the
reverse. Therefore the labels illuminated by one direction form a chain,
even when some coordinates of c coincide. Conversely, extend any chain to
prefix sets of a permutation pi of [k] and choose c_{pi(j)}=j, for
j=1,...,k. Equation (2) illuminates every vertex in the original chain.
The direction is nonzero because c is not constant. This proves the
simultaneous-illumination assertion.

## 3. Matching lower and upper certificates

Take all labels of size floor(k/2). No direction illuminates two of their
vertices, so I(Z) is at least their number. More geometrically, any two
such distinct labels S,T have i in S minus T and j in T minus S. The
opposite normals f_ij and f_ji are active at p_S and p_T, respectively:
these vertices lie on opposite parallel supporting hyperplanes. This is
a direction-independent pairwise antipodality certificate.

The same certificate proves the fractional lower bound. If E_S is the set
of directions illuminating p_S, then the E_S for the middle layer are
pairwise disjoint. For any feasible illuminating measure mu,

\[
 \mu(\text{all directions})\ \ge\ \sum_{|S|=\lfloor k/2\rfloor}\mu(E_S)
 \ \ge\ \binom{k}{\lfloor k/2\rfloor}.                      \tag{3}
\]

For completeness, an explicit classical symmetric-chain decomposition
gives the matching upper bound. Start with the single chain containing
the empty set in B_0. From a saturated symmetric chain

\[
 A_r\subset A_{r+1}\subset\cdots\subset A_{n-r}
\]

in B_n, where the subscripts are set sizes, introduce a new element x and
form the two chains

\[
 A_r,\ldots,A_{n-r},A_{n-r}\cup\{x\},
 \qquad
 A_r\cup\{x\},\ldots,A_{n-r-1}\cup\{x\}.
\]

Omit the second chain when its list is empty. These partition the two
copies of the old chain and have endpoint rank sums n+1. Induction gives
a partition of B_k into symmetric saturated chains. Each chain meets the
layer of rank floor(k/2) exactly once, so there are precisely
binomial(k,floor(k/2)) chains. Remove the two endpoint labels and extend
each remaining chain to a permutation. For k>=2 every resulting chain is
nonempty. Equation (2) supplies one direction for each chain.

These directions illuminate all vertices, which suffices for the whole
boundary of a polytope. In fact, if x is in the relative interior of a
proper face and p is a vertex of that face, every facet active at x is
active at p. A direction illuminating p strictly decreases all active
facets at x as well. Hence I_f(Z) <= I(Z) is at most the displayed number.
Together with (3), this proves Theorem 1.

## 4. Summands, independent subspaces, and sharpness

We use the following elementary monotonicity. If Q is full-dimensional and
R is a nonempty compact convex set in the same space, every set of directions
illuminating Q also illuminates Q+R. For x in the boundary of Q+R, write
x=q+r. Necessarily q is in the boundary of Q: otherwise an open ball about
q, translated by r, would put x in the interior of Q+R. Choose a direction
w illuminating q. For sufficiently small positive epsilon,
q+epsilon w is in int Q, whence x+epsilon w is in int(Q+R). Thus

\[
 I(Q+R)\le I(Q).                                          \tag{4}
\]

For Theorem 2, choose a basis from each circuit span. The direct-sum
hypothesis makes their union independent. Extend it to a full basis using
d-r further generators of Z. The subzonotope Q consisting of all selected
circuit generators and these additional single segments is linearly
equivalent to the direct product of the s circuit zonotopes and d-r
segments. The other generators form a Minkowski summand R, so (4) applies.

Take an optimal direction set from Theorem 1 in each circuit factor, and
the two directions in each segment factor. Their Cartesian product
illuminates the product body. At a boundary point, choose a direction
illuminating each boundary factor; in an interior factor any of its
directions stays inside for a sufficiently small step. Taking a common
small step works in all factors. This gives the claimed upper bound.

For the product model itself, take the Cartesian product of the middle-layer
vertex sets in the circuit factors and the endpoint sets in the segment
factors. Two distinct such product points differ in a factor containing
opposing active supporting normals. Extend those normals by zero on the
other factors. No direction illuminates both product points. Therefore
the number of these product points is a lower bound both for I and, by
the same measure argument as (3), for I_f. It matches the constructed
upper bound. This proves sharpness without any claim that illumination
is multiplicative for arbitrary convex bodies.

## 5. Cactus application and the direct-sum hypothesis

In a connected cactus, remove one edge from each simple cycle. The remaining
edges form a spanning tree. One way to verify this is to remove those edges
successively: each chosen edge has its alternate cycle path still present,
since the cycles have disjoint edge sets, so connectivity is preserved.
Any cycle surviving all removals would also be an original simple cycle,
from which an edge was removed. Thus the remaining connected graph is acyclic.

The oriented edge vectors of a tree are independent: in a zero linear
combination, a leaf coordinate forces the coefficient of its sole edge
to vanish, and one continues by deleting the leaf. Their number is |V|-1,
so they form a basis of the sum-zero space. Each original cycle is a
linear circuit, with one dependence given by traversing the cycle; positive
edge weights change its nonzero dependence coefficients but not its rank.

Consequently the cycle spans, together with the one-dimensional bridge
spans, form an internal direct sum: the selected tree edges supply a basis
in every factor, and their union is independent. Moreover

\[
 |V|-1=b+\sum_j(k_j-1).
\]

The whole graphical zonotope is the resulting direct product up to an
invertible linear map. The sharpness part of Theorem 2 proves Corollary 3.

The direct-sum assumption cannot be replaced by edge disjointness alone
in a general graph. In K_{2,4}, the two edge-disjoint 4-cycles through
different pairs of degree-two vertices both have rank three, whereas their
union has rank five. Their spans intersect. The verifier includes this
negative control.

## Prior work and limits

Boltyanski and Martini, *Covering Belt Bodies by Smaller Homothetical
Copies*, Beitr. Algebra Geom. 42 (2001), 313–324, give the three-dimensional
circuit value 6 in Remark 2 and the four-dimensional value 10 in Lemma 2.
Their Remark 4 discusses higher-rank circuit bodies. These low-dimensional
values and the general illumination bound for zonotopes are prior work:
[primary paper](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.42/no.2/b42h2mar.pdf).

Rotem, Schejter and Slomka, *The complex Illumination problem*, Combinatorica
46 (2026), article 3, recall the classical nonparallelotope zonotope bound
3*2^{d-2} in Theorem 3.1. Appendix B, Lemma B.1, proves invariance of the
illuminating measures under positive rescaling of individual generators;
the normalization above is consistent with this fact and is proved directly:
[primary paper](https://link.springer.com/article/10.1007/s00493-025-00195-7).

The symmetric-chain construction is classical and is fully proved here.
The contribution is the explicit geometric chain criterion and its exact
all-circuit, independent-circuit, and cactus consequences. The checked
primary texts and targeted searches did not supply these all-rank formulas;
this is not a claim of historical priority or a claim to settle the general
illumination conjecture. The results do not determine illumination for
arbitrary graphical zonotopes or for intersecting circuit spans.

This proof is the universal mathematical argument. The accompanying exact
program supplies finite corroboration and reproducible constructions;
finite tests alone do not prove its all-rank statements.
