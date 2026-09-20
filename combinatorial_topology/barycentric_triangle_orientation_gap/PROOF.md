# Triangle packing detects the orientation defect of a triangulation

Let $T$ be a finite nonempty pure two-dimensional abstract simplicial
complex. Assume each edge is contained in at most two triangular facets.
Write $f=f_2(T)$, and let $G$ be the one-skeleton of its barycentric
subdivision. Thus vertices of $G$ are nonempty faces of $T$, with two
vertices adjacent precisely when one face properly contains the other.

Let $\nu_\triangle(G)$ be the maximum number of pairwise edge-disjoint
graph triangles, and let $\tau_\triangle(G)$ be the minimum number of
graph edges meeting every graph triangle. Their fractional versions allow
nonnegative real triangle weights with total at most one on each edge,
and nonnegative real edge weights with total at least one on each triangle.

Orienting an original facet gives directions to its three boundary edges.
Call a family of oriented facets **coherent** if any two retained facets
sharing an edge induce opposite directions on that edge. Define

$$
\kappa(T)=\min\{|D|: \text{the facets outside }D
                         \text{ admit coherent orientations}\}.
$$

Deleting facets here means removing their orientation constraints; no
assumption that the remaining space is a manifold is made. Vertex links
may be disconnected or singular, and boundary edges are allowed.

## Theorem

Under these hypotheses,

$$
\boxed{\quad \tau_\triangle(G)=\tau_\triangle^*(G)
       =\nu_\triangle^*(G)=3f,
       \qquad \nu_\triangle(G)=3f-\kappa(T).\quad}
$$

In particular the integral packing-covering gap, and the additive
fractional-packing gap, are exactly $\kappa(T)$. For a triangulated
compact surface, possibly disconnected or with boundary, equality
$\tau_\triangle=\nu_\triangle$ holds precisely when every component is
orientable.

The constructive statement is stronger than the numerical lower bound:
**any** coherently oriented set of retained facets can be extended to a
packing using three flags per retained facet and two per deleted facet.

## 1. Flags and the conflict graph

Three pairwise comparable distinct nonempty faces of a two-dimensional
complex must have sizes $1,2,3$. Therefore every triangle of $G$ is
exactly a flag

$$
        (v,e,F),\qquad v\in e\subset F,
$$

where $F$ is an original triangular facet. There are six flags per
facet, hence $6f$ graph triangles. Make a graph $X$ on these flags,
joining two flags when the corresponding triangles of $G$ share a
graph edge. Then $\nu_\triangle(G)=\alpha(X)$.

Within one original facet $F$, two distinct flags conflict if they
have the same $v$ or the same $e$. Its six flags induce a six-cycle.
For each of the three sides $e\subset F$, the two flags
$(v,e,F)$, with $v$ an endpoint of $e$, form an adjacent pair;
these three pairs partition the hexagon.

Across two different facets $F,F'$, flags conflict only when they
have the same $v$ and $e$. Thus a shared original edge creates two
matching connections, one for each endpoint. By the edge-incidence
hypothesis, each side-pair meets at most one other hexagon. Boundary
sides have no external connection.

A six-cycle has independence number three, and its only independent
triples are its two alternating classes. If $F=(a,b,c)$ is oriented
in cyclic order, one class is

$$
 (a,ab,F),\quad (b,bc,F),\quad (c,ca,F).
$$

The other class encodes the opposite orientation. Across a shared
original edge, these triples do not conflict exactly when they choose
opposite endpoints, which is exactly the coherence condition.

## 2. Upper bound on packing

Consider any independent set $I$ of $X$. Call a facet full if its
hexagon contains three members of $I$, and let $D$ be the other
facets. The full facets carry coherent orientations by Section 1.
Consequently $|D|\ge\kappa(T)$, and each nonfull hexagon contributes
at most two flags. Therefore

$$
 |I|\le 3(f-|D|)+2|D|=3f-|D|\le 3f-\kappa(T).
$$

## 3. Greedy completion lemma and attainment

Start with any coherently oriented subfamily of facets and select its
alternating triples. Process the remaining facets in any order.
At a current hexagon, an already processed neighboring hexagon selects
at most one flag from its side-pair, because those two flags are adjacent.
It can therefore forbid at most one flag from the corresponding side-pair
of the current hexagon. There is at most one neighbor per side-pair.

At least one flag remains available in each of the three side-pairs, so
at least three of the six flags remain available. A six-cycle has no
triangle, so among any three of its vertices some two are nonadjacent.
Select such a pair. It has no conflict with any previously selected flag.
Future choices use the same rule, preserving independence.

This constructs three flags in each retained facet and two in every
other facet. Apply it after deleting an optimal set of $\kappa(T)$
facets to obtain an independent set of size $3f-\kappa(T)$.
Together with Section 2, this proves the packing formula. The completion
does not require solving another optimization problem once the coherent
subfamily has been supplied.

## 4. Integral and fractional covering

Every graph edge of $G$ has one of the forms
$\{v,e\}$, $\{e,F\}$, or $\{v,F\}$.
Their numbers of incident graph triangles are, respectively, the number
of original facets through $e$, two, and two. All are at most two.
There are $6f$ graph triangles, so any integral edge cover has size
at least $3f$. More strongly, assigning weight $1/2$ to every graph
triangle is a feasible fractional packing with weight $3f$.

Take all $3f$ edges $\{v,F\}$ with $v\in F$. Each flag contains
exactly one of these edges, so this is an integral triangle edge cover
of size $3f$. Weak LP duality now gives the full chain of equalities

$$
3f\le\nu_\triangle^*(G)\le\tau_\triangle^*(G)
   \le\tau_\triangle(G)\le3f.
$$

## 5. Signed dual interpretation: a known theorem, with proof

Choose a reference orientation for each facet. Let $H$ have one vertex
per facet and an edge for each shared original edge. It is a simple
subcubic graph: two distinct simplices cannot share two edges, and each
facet has only three sides. For adjacent facets $i,j$, put $b_{ij}=1$
if their reference directions on the shared edge agree, and $0$ if
they are opposite. Reversing reference orientation $i$ is signed-graph
switching. A binary assignment $x$ is coherent precisely when

$$
 x_i\mathbin\oplus x_j=b_{ij}
$$

on every edge. In standard signed-graph language, use sign
$(-1)^{b_{ij}}$; a coherently orientable subfamily is a balanced induced
subgraph. Hence $\kappa(T)$ is its vertex frustration number.

Let $\lambda$ be the minimum number of unsatisfied edge constraints
over all binary assignments. It equals the usual edge frustration index:
one may delete the unsatisfied edges of any assignment; conversely,
a balanced graph after edge deletion supplies an assignment violating
at most the deleted edges.

The equality $\kappa=\lambda$ for subcubic signed graphs is
**Sivaraman's Theorem 1 (2014)**, not a new result here. For completeness,
an elementary argument for the present simple-graph case follows.
An assignment with $\lambda$ unsatisfied edges becomes coherent after
deleting one endpoint of each such edge, so $\kappa\le\lambda$.
Conversely start with a coherent assignment after $\kappa$ vertices
have been deleted, and restore those vertices one at a time. At each
step choose the binary value satisfying a majority of the constraints
to already assigned neighbors. There are at most three such neighbors,
so at most one new unsatisfied edge is created. Each edge is assessed
once, when its second endpoint is assigned. Thus
$\lambda\le\kappa$, proving equality.

Our theorem consequently also identifies the packing deficit with the
least possible number of shared original edges whose induced facet
orientations agree, over orientations of **all** facets. This is a
combinatorial defect defined from the triangulation; no genus formula is
asserted.

An elementary, nonoptimal bound is $\kappa\le\lfloor f/2\rfloor$:
choose an assignment minimizing the number of unsatisfied edges.
If a vertex met more than half its incident edges unsatisfied, flipping
it would improve the assignment. In a subcubic graph, the unsatisfied
edges therefore form a matching. This gives
$\nu_\triangle(G)\ge\lceil5f/2\rceil$ and
$\tau_\triangle(G)\le(6/5)\nu_\triangle(G)$.
These are only elementary consequences, with no sharpness or best-bound
claim. Stronger signed-subcubic frustration bounds are known; see SOURCES.

## 6. Scope and a failed extension

For surfaces, coherent facet orientations are the usual definition of
orientability. The qualitative relation between orientability and
bipartiteness of the flag graph is classical. The quantitative
completion and deficit identity above are the contribution under study.
No claim about arbitrary graphs or the general Tuza conjecture follows.

The incidence assumption cannot simply be dropped. Let $T$ have facets
$\{a,b,c_i\}$, $i=1,2,3$, with distinct $c_i$. Its edge $ab$
belongs to three facets. In its barycentric graph, the two edges
$\{\{a\},\{a,b\}\}$ and $\{\{b\},\{a,b\}\}$, together with
$\{\{a,c_i\},\{a,b,c_i\}\}$ and
$\{\{b,c_i\},\{a,b,c_i\}\}$ for each $i$, cover every graph
triangle. This is eight edges, less than $3f=9$.

The proof is a finite combinatorial argument, not a proof-assistant
formalization. The exact checker independently constructs small graphs,
optimizes their packings, computes their orientation defects, and checks
the constructive witnesses. These finite checks corroborate the proof;
they are not the basis for its universal quantifier.
