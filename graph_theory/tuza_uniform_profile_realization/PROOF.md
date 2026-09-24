# Uniform realization of robust triangle profiles

Complete author proof, awaiting independent mathematical review. The deep
existence input is Keevash's generalized partite **family** decomposition
theorem. The contribution is the tagged-family specialization, its explicit
integer role allocation, and the resulting uniform region of linear loss.
No new proof of the imported theorem or absolute priority claim is made.

All graphs are finite and simple. Write nu(G) for the maximum number of
edge-disjoint triangles and nu*(G) for the full fractional packing optimum.

## 1. A uniform theorem with an explicit boundary

A mixed template has d nonempty vertex classes. Each class is a clique or
independent set; each distinct pair is completely joined or empty. Let their
sizes be n_i, let N=sum n_i, and let E be its supported edge types. The
capacity of e=ij is b_e=n_i n_j for i<j, or b_ii=binom(n_i,2) for a clique
class. Triangle types are multisets of three types whose three pair types
are supported. A pattern P is either an allowed triangle type or a supported
single-edge type. Let a_eP count its edges of type e.

A full decomposition profile is a nonnegative real vector z satisfying

    sum_P a_eP z_P=b_e  for every e.                         (1)

Its triangle coordinates are a fractional packing profile; its single-edge
coordinates are the unused capacities. When n_i>=3, averaging each triangle
coordinate over actual triangles of its type gives a fractional packing.
Conversely, averaging and aggregating an actual fractional packing gives
(1). Thus optimizing the sum of triangle coordinates is exactly the full
fractional packing LP, including all repeated-type triangles.

Fix an integer d>=1 and real alpha,epsilon>0. Let

    M=binom(d+2,3)+binom(d+1,2),
    lambda=8M/alpha,   U=ceil(lambda+4M).                    (2)

There are at most M patterns. The hypotheses below are empty unless the
parameters permit the indicated class sizes and profile masses.

**Theorem 1 (uniform robust-profile realization).** There is
N_0=N_0(d,alpha,epsilon) such that the following holds. Suppose G has at most
d mixed classes, every n_i>=alpha N, and a profile (1) in which every positive
coordinate satisfies z_P>=epsilon N^2. Coordinates equal to zero are allowed.
For N>=N_0, G has a triangle packing containing exactly

    floor((1-lambda/N)z_T)                                 (3)

triangles of each positive triangle type T, and none of its zero types.

If W is the sum of the triangle coordinates, the packing size is at least

    W-(lambda/6)N-M.                                      (4)

In particular, if some optimal profile satisfies the hypotheses, then

    0<=nu*(G)-nu(G)<=(lambda/6)N+M.                        (5)

The threshold is uniform over all class-size ratios and all profile values
satisfying alpha and epsilon. It does not depend on denominators or require
a fixed ray. The coefficient in (5) depends only on d and alpha, but N_0
also depends on epsilon. No claim is made as positive coordinates become
o(N^2) or nonempty class sizes become o(N). In particular this is not an
unrestricted O_d(N) theorem. The general threshold remains existential.

The rest of Sections 2-6 proves Theorem 1. An edgeless graph is immediate,
so assume at least one supported edge. Increase N_0 throughout as needed.

## 2. Realizing small complement degrees

We use an elementary bounded-degree realization lemma, with a deliberately
loose threshold.

**Lemma 2.** Let U>=1 and L_0=8(U+1)^2.

(a) Two integer degree lists, each of length at least L_0, with entries in
[1,U] and equal sums, are realized by a simple bipartite graph.

(b) An integer degree list of length at least L_0, with entries in [1,U]
and even sum, is realized by a simple graph.

*Proof.* For (a), choose a bipartite graph with as many edges as possible
subject to the stated upper degree bounds. If it does not realize the
lists, choose a deficient vertex a on the left and b on the right. Equal
sums guarantee deficiencies on both sides. All deficient right vertices
are adjacent to a, or an edge could be added. There are at most U of them,
so the current edge count is at least L_0-U. At most 2U(U+1) edges have
a left endpoint in N(b) union {a} or a right endpoint in N(a) union {b}.
Since L_0-U>2U(U+1), there is an edge cd outside these restrictions.
Replace cd by ad and cb. These are new distinct edges, c and d retain their
degrees, and a and b each gain one. This increases the edge count, a
contradiction.

For (b), similarly maximize a simple graph subject to the upper bounds.
Its deficient vertices form a clique and hence number at most U+1. All
other vertices are saturated with degree at least one. Thus its edge count
is at least (L_0-U-1)/2>2U(U+1). If there are two distinct deficient
vertices a,b, some edge cd avoids N(a) union N(b) union {a,b}, since this
set is incident with at most 2U(U+1) edges. Replace cd by ac and bd,
again increasing the edge count. If only a is deficient, the even total
prescribed degree implies its deficiency is at least two. An edge cd
outside N(a) union {a} can be replaced by ac and ad. Both cases contradict
maximality. This proves the lemma. No degree-sequence theorem is imported.

## 3. Integer roles supply the entire local lattice

Put theta=1-lambda/N and m_P=floor(theta z_P) for each positive pattern;
omit zero patterns. Take N>=4lambda and N^2>=4/epsilon. Then

    m_P>=epsilon N^2/2>0.                                 (6)

For a type i occurring k_i(P) times in P, all its roles in that pattern
have the same local edge-type degree vector l_iP. For a triangle its
internal coordinate is k_i(P)-1 and its coordinate towards another type j
is k_j(P); the vector sums to two. For a single edge it sums to one.
There are no coordinates on unsupported edge types.

Distribute the m_P k_i(P) roles among the n_i vertices as evenly as possible.
Thus integers r_vP sum to m_P k_i(P) and each differs from
m_P k_i(P)/n_i by less than one. A quotient/remainder assignment suffices;
no compatibility between the different patterns is required. Define

    d_v=sum_P r_vP l_iP,  v in class i.                    (7)

These are proposed edge-type degrees, not an already realized triangle
family. In particular assigning roles does not silently assume the desired
packing. Equation (7) is an explicit integer combination of the vertex
vectors that will generate the required singleton lattice.

Let p_i,e be the actual complete-template degree at a type-i vertex:
n_j across a supported pair, or n_i-1 internally. Equation (1) gives

    sum_P [z_P k_i(P)/n_i] l_iP,e=p_i,e.                   (8)

Internal incidence is counted twice in deriving (8). For N>=3/alpha,
flooring m_P and rounding roles give, coordinatewise,

    theta p_i,e-4M <= d_v,e <= theta p_i,e+2M.              (9)

For the upper bound use m_P<=theta z_P and r_vP<m_P k_i/n_i+1.
For the lower bound use m_P>theta z_P-1, k_i<=3, n_i>=alpha N,
and every coordinate of l_iP at most two. Summing at most M terms proves
(9), including single edges and repeated triangle types.

The complementary degrees r_v,e=p_i,e-d_v,e are integers. Since
p_i,e>=alpha N-1>=alpha N/2 and p_i,e<=N, equations (2) and (9) imply

    1 <= 2M <= r_v,e <= lambda+4M <= U.                   (10)

On a cross pair the two lists of r_v,e have equal sums: the target number
of edges of that type on either side is

    b'_e=sum_P a_eP m_P.                                  (11)

On a clique class their sum is even, since it is n_i(n_i-1)-2b'_ii.
For n_i>=8(U+1)^2, apply Lemma 2 independently to every supported pair
and clique class. The resulting removed graph R has maximum degree at
most dU. Its complement G'=G-R has exactly the degree vectors (7) and
edge counts (11). All edges selected by Lemma 2 were available in G.

## 4. Auxiliary edges prescribe component counts

For every positive pattern P introduce two private types A_P,B_P of sizes

    a_P=ceil(m_P/N),  |B_P|=N.

Put a bipartite graph Z_P of exactly m_P edges on these types. Start with
the complete pair and delete q_P=a_P N-m_P<N edges

    (j mod a_P, j),  0<=j<q_P.                            (12)

Right endpoints in (12) are distinct. The removed degree is at most
ceil(2/epsilon) on either side, by (6). Also

    epsilon N/2 <= a_P <= N

for sufficiently large N, since every z_P<=N^2/2. Make no other auxiliary
adjacencies. The augmented host Gamma is G' disjoint from all Z_P; the
word 'disjoint' concerns vertex sets and edges, not the components of the
family members used to decompose it. Its order n satisfies

    N <= n <= C N,  C=1+2M.

Every type has size at least beta n, where

    beta=min(alpha,epsilon/2,1)/C.                        (13)

For each P let H_P consist of its original component and one edge between
A_P,B_P. Give the whole family a common vertex-role set, partitioned by
all original and auxiliary types, with at least three roles of each type.
Unused roles in each H_P are isolated. The number q of roles is fixed by
d, alpha, epsilon and the support, before N varies. Add more isolated roles
if needed so that the h(q) in the imported theorem satisfies h(q)>=1/beta.
The support has only finitely many possibilities for fixed d.

Use the complete type-respecting injection complex Phi on these q roles.
It is exactly adapted to the group of permutations preserving each role
part: a bijection of role subsets preserves allowed images precisely when
it preserves their types. Isolated roles, disconnected graphs and varying
numbers of edges per family member are allowed in the imported theorem.

The indexed divisibility conditions hold explicitly:

- At the empty set the host edge vector is sum_P m_P h_P: its original
  coordinates are (11), and its tag coordinate P is m_P.
- At an original vertex the vector is (7), a sum of appropriate H_P vertex
  generators with nonnegative integer coefficients.
- At an auxiliary vertex its vector is an integer multiple of the unit
  vector supplied by the corresponding tag-edge endpoint.
- At a host edge its pair vector is the corresponding unit vector, supplied
  by an H_P edge. For a nonedge it is zero; larger subsets give zero.

These are witnesses in the full indexed integer lattices. No reduction to
ordinary scalar parity is assumed in Theorem 1.

## 5. Checking the imported theorem's analytic hypotheses

We use Peter Keevash, *Coloured and directed designs*, the
[author manuscript](https://people.maths.ox.ac.uk/keevash/papers/lovasz70.pdf)
dated 15 October 2018. The relevant definitions are 4.3-4.5, 5.11, 5.12
and 5.14, and the existence result is Theorem 5.15, printed page 19.
For a fixed family of simple graphs on a common partitioned role set,
that theorem gives a part-respecting decomposition from indexed divisibility,
regularity with comparable positive embedding weights, bounded-rank
extendability, and sufficiently large comparable host parts. We apply it
with one edge color. The following verifies regularity and extendability;
the theorem itself is the explicit external trust boundary.

Let q_j be the number of roles of type j and

    L=product_j (n_j)_(q_j),

where the falling factorials include all auxiliary classes. Give each valid
embedding of H_P the weight

    y_P=a_P N/L.                                         (14)

First temporarily restore R, retaining the tag graphs Z_P. For a fixed tag
edge of P, there are exactly L/(a_P N) embeddings using it, so its load is
one. Among all L complete type-respecting embeddings, precisely the
fraction m_P/(a_P N) uses an edge of Z_P. Their total weight is m_P.
Symmetry in each original vertex class then gives every original edge of
type e the load b'_e/b_e. This computation counts all role automorphisms
and isolated-role completions; no embedding multiplicity is suppressed.

Now restrict to embeddings whose original component survives in G'.
Original base loads are at least 1-2U/(alpha N), by (10). If P is a single
edge, an embedding using a surviving original edge loses no other original
edge. If it is a triangle, a surviving edge belongs to at most 2dU triangles
destroyed by R. The effective weight on an actual triangle of type T is
m_T/C_T, where C_T is the number of original triangles of that type.
For large N,

    C_T>=alpha^3 N^3/48,  m_T<=N^2/2,

so this weight is at most 24/(alpha^3 N). Thus every surviving original
edge has load in [1-c_N,1], where

    c_N=50dU/(alpha^3 N).                                 (15)

For a tag edge, the original component is uniformly distributed among
copies of its type. The fraction destroyed is at most the sum of the
removed fractions of its at most three edges, hence at most 6U/(alpha N),
which is also bounded by (15). Every edge of Gamma therefore has load in
[1-c_N,1].

For large n, (beta n/2)^q<=L<=n^q. Equations (6), (13) and (14) imply

    [epsilon/(2C^2)] n^(2-q) <= y_P
       <= (2/beta)^q n^(2-q).                            (16)

These bounds hold for every valid embedding, not just on average.

For extendability, the supported pairs of Gamma are complete except for
a graph of maximum degree at most

    Delta=max(dU,ceil(2/epsilon)).

Consider any extension of the bounded rank h in the source definition.
At most qh vertices are involved. Greedily map the unfixed vertices into
their prescribed types. At each step, at most qh already used vertices
and qh Delta forbidden neighbors are excluded. A part of size at least
beta n therefore offers at least beta n/2 choices for large n. An extension
with v new vertices has at least (beta/2)^(qh) n^v choices. Unsupported
edge indices are undefined in the extendability condition, exactly as
stipulated before Theorem 5.15; no nonedge is required to be an edge.

Choose a fixed omega>0 smaller than the lower constants in (16), the
reciprocal upper constant there, (beta/2)^(qh), and the theorem's omega_0.
For sufficiently large n, n^(-delta)<omega and c_N<=omega^(h^20).
Thus the regularity and extension hypotheses hold, and the part-size
condition follows from h>=1/beta. All choices are uniform for fixed
d,alpha,epsilon; taking a maximum over the finitely many templates and
supports gives one N_0.

## 6. Extracting the packing

Theorem 5.15 decomposes Gamma into the family H_P. Only H_P uses tag pair
A_P,B_P, and every such copy uses exactly one edge of Z_P. Consequently
there are **exactly m_P copies of H_P**. Keep the original triangle
components; discard original single-edge components and all auxiliary
edges. The retained triangles are edge-disjoint in G', hence in G, and
have the counts (3).

For at most M triangle types, summing floors loses at most M. Also
W<=|E(G)|/3<=N^2/6. Hence sum_T m_T>=theta W-M>=W-lambda N/6-M,
proving Theorem 1 and its full-LP consequence.

The construction does not provide a practical finite N_0 or an efficient
implementation of Keevash's decomposition. The explicit role counts and
tag graphs are auxiliary certificates for the reduction, not a claimed
large-order triangle packing produced by the code.

## 7. A sharper exact criterion for split templates

A split template has clique classes forming a complete core and independent
classes joined to specified nonempty subsets of the core classes. Suppose
all classes have size at least alpha N, and (1) has **no spare edges** and
positive mass at least epsilon N^2 on **every** allowed triangle type.
The following conclusion is stronger than just rounding that profile.

**Theorem 3.** For sufficiently large N, uniformly under these conditions,
G has a triangle decomposition if and only if every vertex has even degree
and 3 divides |E(G)|. The same sufficiency holds for G-R when R has any
fixed bounded maximum degree and G-R satisfies those two conditions.
The threshold for this resilience statement may additionally depend on
that degree bound.

Use the family of single triangles of all allowed types, with a common
isolated-padded role set as before. We show that the indexed integer
conditions impose no additional restrictions.

For the global lattice, let b be any integer supported edge-type vector
with even type degrees (loops counted twice) and edge sum divisible by three.
For an independent type h choose a clique neighbor p. For each other
neighbor j, subtract b_hj copies of triangle(h,p,j), eliminating hj.
The residual hp entry is even by type-h parity; eliminate it with half
that many copies of triangle(h,p,p). All coefficients here may be negative.
Repeat to remove all independent-type edges.

Among the remaining clique types fix pivot 0. Eliminate each cross pair ij with
distinct nonpivot i,j by triangle(0,i,j). Each residual 0i is then even, so eliminate
it using triangle(0,i,i). Only loop entries remain. The signed difference
triangle(0,i,i)-triangle(0,0,i) equals the loop vector ii-00; use it to move
all loop mass to 00. The final entry is a multiple of three and is removed
by triangle(0,0,0). This proves sufficiency in the global lattice. Necessity
of these congruences follows by counting each triangle's incidences.

For a clique type i, the vectors 2e_ii and e_ii+e_ij generate exactly the
integer incident-type vectors of even coordinate sum. For an independent
type h, fix a clique neighbor p; the vectors 2e_hp and e_hp+e_hj have the
same property. These are actual vertex vectors of allowed triangle types.
Thus even degree at every actual vertex supplies the singleton conditions.
It also supplies global type-degree parity by summing within classes.
Every supported edge has a triangle type supplying its unit pair vector.

Distribute each profile mass equally among its actual triangles. The loads
are exactly one. With L the count of full role embeddings, an embedding
of type T has weight x_T/L; role automorphisms and padding give this formula
exactly as in Section 5. These weights are between positive constant
multiples of N^(2-q). Removing bounded-degree R changes loads by O(1/N).
The same greedy extension argument applies. Keevash's Theorem 5.15 gives
the desired decomposition. Ordinary parity and edge-count necessity is
immediate, proving Theorem 3.

**Corollary 4 (economical linear loss in this region).** If the core has k
vertices and the independent side p vertices, then for sufficiently large N,

    nu*(G)-nu(G) <= [p+floor(k/2)+5]/3 <= (N+5)/3.          (17)

For each odd-degree independent vertex, remove one core edge incident with
it, choosing a neighbor with the smallest current number of such removals.
Every such neighborhood has size at least alpha N, so each core vertex is
chosen at most floor(1/alpha)+1 times. Now the number of remaining odd-degree
core vertices is even; remove a matching on them. If the remaining edge
count is 1 or 2 modulo three, remove respectively a 4- or 5-cycle in the
remaining core. Such a cycle exists for k>=5: on four or five selected
core vertices the only missing core edges form a matching, relabelable
as a subset of {01,23}. Orders (0,2,1,3) and (0,2,1,3,4) give the required
cycles. These deletions preserve even degrees.

The total removed edges are at most p+floor(k/2)+5 and their maximum
degree is at most floor(1/alpha)+4. Apply Theorem 3 to the residual graph.
The positive profile gives nu*(G)=|E(G)|/3, and the residual decomposition
then proves (17).

## 8. An explicit varying-proportion region and a finite example

Consider the Boolean split template with clique types 0,...,7 and independent
types 8,9,10, where 8+j sees the masks with bit j. The certificate supplies
an exact homogeneous decomposition profile x^0 on all 150 triangle types:

    A x^0=c,  c_ii=1/2, c_ij=1,
    min_T x^0_T=1/26,  sum_T x^0_T=44/3.

For a split template an explicit right inverse of A sends a loop unit e_ii
to (1/3)iii, and a cross unit e_ij, choosing clique endpoint i, to
(1/2)iij-(1/6)iii. For this 11-type template, its maximum absolute row sum
is at most 2. Let t>=1000 and take **arbitrary integer** class sizes

    (999/1000)t <= n_i <= (1001/1000)t.                    (18)

The normalized cross capacities differ from one by at most 2001/10^6;
the normalized internal capacities differ from one half by at most
10005/10^7+1001/(2000t). Both are less than 1/104. Apply the right inverse
to this capacity perturbation. The corrected profile x/t^2 has all its
coordinates at least 1/26-2/104=1/52. It is an exact decomposition profile.
Also n_i/N>=1/12 and x_T/N^2>=1/7000 (the latter uses
N/t<=11011/1000). Thus Theorems 3 and 4 apply uniformly to the whole box
(18) once t exceeds one fixed existential threshold, independently of
how the integer proportions vary inside it. Parity and edge count modulo
three are the only exact-decomposition obstructions in this region.
The convenient bound t>=1000 certifies profile positivity; it is **not**
a claimed bound for the imported existence threshold.

As a separate finite certificate, the unmodified Boolean split graph with
class sizes (5,4,4,4,4,4,4,4,4,4,4) has 45 vertices and 720 edges. The
published 240-triangle family covers each edge exactly once. This graph
is neither the diagonal-deleted host of the earlier package nor an instance
covered by the asserted large-t cutoff. Its decomposition is checked directly.

The exact audit validates the finite profiles, role and lattice identities,
degree realizations, tag-weight normalization, cleanup and literal packing.
It does not prove the universal imported theorem or identify N_0. Independent
review of this new reduction is pending.
