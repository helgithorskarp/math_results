# Exact rational profiles and linear loss on fixed rays

Author proof, submitted for independent review. This is an application of
Keevash's generalized partite decomposition theorem, not a new proof of
that theorem or an absolute priority claim. All graphs are finite, simple
and undirected. Let nu(G) be the maximum number of edge-disjoint triangles
and nu*(G) the optimum of the fractional triangle-packing LP with capacity
one on every graph edge.

## 1. Statements and the finite profile

A mixed template has types 1,...,d, each declared a clique or independent
set. Every pair of distinct types is either completely joined or empty.
Write B_t for the graph with t vertices of each type. Independent types
with no incident edges may be deleted throughout.

Let E be the supported edge types: ij for a joined pair i<j, and ii for
a clique type. Set c_ij=1 and c_ii=1/2. An allowed triangle type T is a
multiset of three types for which all three pair types are supported.
Let a_eT be the multiplicity of edge type e among these three pairs.
For example a_ii,iii=3, while iij uses one ii and two ij edges.
Consider the rational polytope

    x_T >= 0,     sum_T a_eT x_T <= c_e  for every e in E.       (1)

Put P=max sum_T x_T. The polytope is bounded; if there are no allowed
triangles its objective is zero. A rational optimum exists.

Label each class of B_t by 0,...,t-1. Define J_t by retaining a supported
edge exactly when its endpoint labels differ. Thus each supported cross
pair loses one perfect matching, while a clique class remains K_t.
There are t(t-1)c_e edges of each type e. A vertex of type i has degree
vector (t-1)u_i, where u_i has coordinate one on each supported edge type
incident with i, including ii, and zero elsewhere.

**Theorem 1 (exact profile realization).** Fix a rational feasible x in
(1). Choose a positive integer D such that every D x_T and every D c_e
is integral. For all sufficiently large t with t=1 mod D, J_t has an
edge-disjoint triangle family containing exactly t(t-1)x_T triangles of
each type T. The threshold may depend on the template and x.

**Theorem 2 (linear rounding on each fixed ray).** Choose an optimal x
and D as above. For all sufficiently large t,

    0 <= nu*(B_t)-nu(B_t) <= (2D-1)P t.                        (2)

More generally, fix a mixed template, integer slopes a_i>=0 and fixed
integer offsets b_i. For class sizes a_i t+b_i that are nonnegative for
all sufficiently large integer t, its full fractional triangle-packing
integrality gap is O(t), equivalently O(N) when the graph order N grows.
The implied constant and starting order may depend on this fixed ray.
Rational slopes are included by clearing denominators and restricting
to parameter values for which the class sizes are integral. If all
slopes vanish, the graph is fixed and its gap is bounded.

This does not assert a uniform O_d(N) bound over arbitrary proportions,
vanishing classes or changing ray denominators.

**Theorem 3 (independent blowups).** Let F be an ordinary simple graph
and F[t] its balanced independent blowup. There is an integer D>=1 such
that for all sufficiently large multiples t of D,

    nu(F[t]) = nu*(F[t]) = t^2 nu*(F).                          (3)

More precisely, any rational feasible fractional packing profile x on
F is realized with t^2 x_T triangles of each type for every sufficiently
large multiple t of a denominator clearing all x_T.

**Theorem 4 (one finite certificate suffices).** If a packing in F[s]
has exactly s^2 nu*(F) triangles, an explicit cyclic Latin construction
gives equality in (3) at t=su for every integer u>=1. For every t>=1,

    nu*(F[t])-nu(F[t]) <= 2(s-1)nu*(F)t.                        (4)

Theorem 3 guarantees that some finite certificate exists. The present
argument supplies neither a practical bound on the first such s nor
an efficient general search for it.

## 2. The external decomposition theorem

We use Peter Keevash, *Coloured and directed designs*, Definition 3.1
and Theorems 3.2 and 3.3 in the [author's manuscript](https://people.maths.ox.ac.uk/keevash/papers/lovasz70.pdf),
dated 15 October 2018, printed pages 7-8. The applicable specialization
is as follows. Fix a simple graph H and a partition of its vertices into
types. A sufficiently large graph supported on H's edge types, with
comparable part sizes, densities bounded below and sufficiently small
common-neighborhood relative error, has a type-respecting H-decomposition
if its local edge-count vectors satisfy the associated integer-lattice
divisibility conditions. These conditions occur at vertex-subset sizes
zero, one and two. The complete-host case is Theorem 3.3.

Neither connectedness of H nor distinct types on its vertices is a
hypothesis. Below we explicitly verify the relevant lattices, support,
part sizes, density and typicality. The imported theorem is the deep
existence step; the finite Python audit does not verify its proof.

## 3. Compiling a rational profile into a finite graph

For a fixed x and D, form a graph H as a disjoint union of:

- D x_T triangle components with vertex types T, for every T;
- D(c_e-sum_T a_eT x_T) single-edge components of type e, for every e.

All these multiplicities are nonnegative integers. Use fresh vertices
in every component, even when their assigned types coincide. Thus H is
a simple graph, not a graph with loops or parallel edges. Its partition
P_i consists of the vertices assigned type i. After deleting unsupported
isolated types, every P_i is nonempty. If the template has no edges, the
claims are immediate and no decomposition theorem is needed.

The edge-count vector of H is

    h = D c.                                                   (5)

For each type i, sum the edge-degree vectors over all v in P_i. A cross
edge incident with i is counted once, and an ii edge is counted twice.
Since D c_ii=D/2 and D c_ij=D, the resulting vector is

    sum_{v in P_i} deg_H(v) = D u_i.                           (6)

These two identities provide actual integer combinations in the required
lattices, so no unproved sufficiency rule for ordinary degree gcds is
being substituted for the multivariate divisibility condition.

## 4. Divisibility and typicality of J_t

For a subset A of vertices, let g(A) list, by supported edge type, the
numbers of host edges containing A. The lattice for its type-index is
generated by the corresponding vectors h(S) for all subsets S of V(H)
with that same type-index. For t=1 mod D:

- For A empty, g(A)=t(t-1)c=[t(t-1)/D]h. The multiplier is integral.
- For A={v} of type i, g(A)=(t-1)u_i is [(t-1)/D] times the sum in (6).
  Each summand is a permitted generator of this singleton-index lattice.
- For a pair A that is an edge, g(A) is the unit vector of its edge type.
  H contains an edge of that type by (5), giving this unit generator.
  For a nonedge A, the vector is zero.
- Subsets larger than two have zero vectors and cause no condition.

Thus J_t is (H,P)-divisible in the precise sense of Definition 3.1.

Its supported internal densities are 1, and its supported cross densities
are 1-1/t. Fix an integer h>=1. Consider a<=h distinct vertices whose
common neighbors are sought in a particular type j. If some input vertex
has an unsupported adjacency to j, both the actual common-neighbor count
and the required density product are zero. Otherwise, let b be the
number of distinct labels on the input vertices, and let z be the number
of these vertices outside type j. The exact count and the target are
respectively

    t-b,                  t(1-1/t)^z.                         (7)

For t>=2h both lie between t-a and t. Their difference is at most a,
and the target is at least t/2. The relative error is at most 2a/t.
This is (c,h)-typicality with c=2/t under Definition 3.1, whose permitted
relative error for a inputs is a c. The empty input set also satisfies
the identity exactly.

The graph H, hence the theorem's h and all its small constants, is fixed
before t grows. Choose the theorem's density lower bound to be 1/2.
All supported densities exceed this for large t; all parts have size t.
The required lower-density and upper-error inequalities hold eventually
because 2/t tends to zero and the theorem's negative power of t tends
to zero. Its large-order condition also holds eventually. Theorem 3.2
therefore yields a type-respecting H-decomposition of J_t.

By (5), the number of copies of H is t(t-1)/D. Keep the triangle
components in every copy and discard its single-edge components. The
copies share no edges, and the triangle components within one copy are
vertex-disjoint. The resulting packing has t(t-1)x_T triangles of each
type. This proves Theorem 1.

## 5. Fractional values and the linear bound

Aggregating any fractional packing of B_t by triangle type gives (1)
after division by t^2: the actual cross capacities are t^2, and each
clique capacity is binom(t,2)<=t^2/2. Therefore

    nu*(B_t) <= t^2 P.                                         (8)

In fact, for t>=3,

    nu*(J_t) = t(t-1)P.                                        (9)

For the lower bound, an allowed type T with multiplicities m_i has
(t)_3 / product_i(m_i!) actual triangles in J_t. Spread total mass
t(t-1)x_T equally among these triangles. Simultaneous permutations of
the labels act transitively on every supported edge type. Consequently
an edge of type e receives exactly

    sum_T a_eT x_T / c_e <= 1.

The upper bound in (9) is obtained by aggregating edge capacities.
Use an optimal x in this argument. No equality between nu*(B_t) and
its homogeneous upper bound t^2P is claimed for clique types.

For arbitrary large t, let s<=t be the largest integer with s=1 mod D.
Then s>=t-D+1, and J_s embeds in B_t. Once s exceeds the threshold of
Theorem 1, its packing and (8) imply

    nu*(B_t)-nu(B_t) <= [t^2-s(s-1)]P.

Writing b=t-s, where 0<=b<=D-1, the bracket equals
(2b+1)t-b(b+1) <= (2D-1)t. This proves (2).

For integer slopes a_i, replace type i by a_i clone types. If i was a
clique type, all its clone types are clique types and mutually joined;
if independent, they are independent and mutually unjoined. Inherit
all other adjacencies. The graph with sizes a_i t is exactly the balanced
mixed blowup of this larger fixed template. Zero slopes may be omitted.
This proves the zero-offset ray statement.

Adding or removing one vertex changes nu and nu* by at most half its
degree: in either an integral or fractional packing, each triangle
through the vertex consumes two incident edges. Compare graphs with
bounded offsets through their common induced subgraph obtained by
keeping the smaller class size at each type. If at most B vertices
are deleted from each graph, its fractional optimum differs by at most
BN/2 and its integral optimum by at most BN/2, using an upper bound N
for their orders. Thus their integrality gaps differ by O(BN). Here B
is fixed. This proves the offset statement and Theorem 2.

Linear order cannot in general be improved to o(N), even with one type.
For even N>=4, uniform triangle weight 1/(N-2) and uniform edge dual
weight 1/3 certify nu*(K_N)=binom(N,2)/3. Every integral packing leaves
at least one unused incident edge at each vertex, since N-1 is odd and
triangles use incident edges in pairs. At least N/2 edges are unused,
so nu*(K_N)-nu(K_N)>=N/6.

## 6. Exact independent blowups and finite lifting

For an ordinary graph F, triangle types are its actual triangles, c_e=1
for every edge, and P=nu*(F). Aggregate a fractional packing of F[t],
or lift a fractional packing of F by placing weight x_T/t on each of
its t^3 lifted triangles, to obtain

    nu*(F[t]) = t^2 nu*(F)  for every t>=1.                    (10)

Construct H from any rational feasible x as in Section 3, now taking
D to clear just the x_T. The host F[t] is a complete (H,P)-blowup. For
D dividing t, its global edge vector is (t^2/D)h, and its vertex vector
at type i is (t/D) times the sum in (6). The pair conditions are the
same unit-vector conditions as before. All parts have size t. Applying
Theorem 3.3 and retaining the triangle components gives precisely
t^2 x_T triangles of each type for sufficiently large such t. With an
optimal x this proves Theorem 3.

Now suppose a literal packing in F[s] attains s^2P. For each ordered
triangle (a,b,c) of that packing and each i,j in Z/uZ, put a triangle
on the three clones

    ((a,i), (b,j), (c,i+j)).                                  (11)

Every edge of each of the three complete bipartite pair blocks occurs
once: the missing index is uniquely recovered by addition or subtraction
in Z/uZ. Distinct triangles of the original packing use disjoint edges,
so their lifted families use disjoint pair blocks. Thus (11) packs
s^2 P u^2 triangles in F[s][u], which is isomorphic to F[su]. Equation
(10) proves equality at every multiple of s.

For arbitrary t>=1 put r=s floor(t/s). Embed this packing for F[r] into
F[t], interpreting r=0 as an empty packing. Since 0<=t-r<=s-1,

    nu*(F[t])-nu(F[t]) <= (t^2-r^2)P <= 2(s-1)Pt.

This proves Theorem 4 without any asymptotic threshold.

## 7. A second finite lifting rule

**Theorem 5 (substitution on labels).** Fix a mixed template. Suppose
J_s contains a packing of size s(s-1)P. If K_t has a K_s-decomposition,
then J_t contains a packing of size t(t-1)P. If the original packing
decomposes J_s completely, the substituted packing decomposes J_t.

For each block of the K_s-decomposition, order its s labels and insert
a copy of the certified J_s packing using these labels in every type.
Every edge of J_t has two distinct labels, and their pair lies in exactly
one block. Thus the copies have disjoint edge sets. The number of blocks
is t(t-1)/(s(s-1)), giving the asserted count; in the complete-decomposition
case every host edge is covered. This also proves the type-by-type version.

In particular, an exact decomposition of J_3 extends to every t=1 or 3
mod 6. We use Kirkman's classical existence theorem for Steiner triple
systems here; its statement is recalled in the primary research paper
of [Glock, Kuehn, Lo and Osthus](https://arxiv.org/abs/1802.04227).
At t=1 the host has no edges, so the conclusion is immediate. For a
supplied Steiner triple system, the substitution is entirely explicit.

## 8. Two compact instances

Let F have a clique on 0,1,2,3 and independent vertices 4,5,6,7,8 with
neighborhoods 012, 013, 03, 123, 23 respectively. This is the previously
reviewed nine-vertex seed, with 19 edges. The certificate assigns weight
1/2 to its eleven triangles meeting an independent vertex and supplies
a feasible edge dual of the same value 11/2. The checker enumerates
all fifteen triangle types, including the four clique-only triangles.
It also checks a literal 22-triangle packing on the 18 vertices of F[2].
By Theorem 4, for every u>=1,

    nu(F[2u]) = nu*(F[2u]) = 22u^2,

and for every t>=1 the gap is at most 11t. Balanced independent blowups
of this split seed need not themselves be split graphs.

For a mixed three-neighborhood-type example, take eight clique cells
indexed by bit masks 0,...,7, all mutually joined, and three independent
cells 8,9,10, where cell 8+j is joined to masks having bit j. There are
48 supported edge types and 150 triangle types. The supplied rational
profile and constant dual 1/3 certify P=44/3. With D=6, the packet H
consists of 88 triangle components and has no spare-edge components.
Theorem 1 already implies eventual decomposition at t=1 mod 6. More
concretely, the certificate contains an 88-triangle decomposition of
J_3, which has 33 vertices and 264 edges. The checker verifies every
edge directly. By Theorem 5, J_t has a triangle decomposition with
44t(t-1)/3 triangles for **every** t=1 or 3 mod 6, with no unknown
large-order threshold. The program constructs and checks substitutions
at orders 3, 7, 9, 15 and 31; universal admissible-order existence uses
Kirkman's theorem, not those five tests.

The unmodified B_t has 44t^2-4t edges, so the homogeneous profile is not
being confused with its finite-order fractional optimum. An explicit
all-scale consequence for this particular ray is

    nu*(B_t)-nu(B_t) <= (304/3)t   for every integer t>=1.

Indeed, let s<=t be the largest positive integer congruent to 1 or 3
mod 6. Then b=t-s<=3, the packing in J_s embeds into B_t, and the
elementary edge-count fractional upper bound gives a gap at most

    [44t^2-4t-44s(s-1)]/3
      = [(44(2b+1)-4)t-44b(b+1)]/3 <= (304/3)t.

The one-clique fixture P=1/6, D=6 provides a normalization control.
The executable checks are exact finite audits of profiles, packet
identities, local counts and the concrete Latin lifts. They are not an
independent proof of the universal decomposition step.
