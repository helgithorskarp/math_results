# A Stirling wedge law for iterated Mycielski clique complexes

Let G be a finite connected simple K₄-free graph with n≥2 vertices. Write
K=Cl(G) for its clique complex. Thus K has dimension at most two. The
ordinary Mycielskian M(G) has old vertices v, independent clones v′, and an
apex a. It keeps the edges of G, joins v′ to every old neighbor of v, and
joins a to every clone. There are no other edges. Put M⁰(G)=G.

All homotopy equivalences below concern geometric realizations and are
ordinary, noncanonical equivalences. No equivariant or natural splitting
is claimed. In particular these are **clique complexes**, rather than
neighborhood, box, Hom, or independence complexes.

## 1. The all-iterate theorem

Let m and t be the numbers of edges and triangles of G. For each edge e,
let t_e be its number of incident triangles. Define

    e₀ = #{e : t_e=0},
    L_v = G[N_G(v)],       c_v = number of components of L_v,
    C = Σ_v c_v,
    D = Σ_v β₁(L_v) = 3t−2m+C,
    Y = Σ_e max(t_e−1,0) = 3t−(m−e₀).

Every L_v is a nonempty graph, possibly disconnected and with isolated
vertices. Its first Betti number here is its ordinary cycle rank. Both
D and Y are nonnegative integers.

Write S(N,r) for an ordinary Stirling number of the second kind, with
S(N,r)=0 for r>N. These count set partitions, not proper graph color
partitions.

**Theorem.** For every integer k≥0,

    Cl(Mᵏ(G)) ≃ K ∨ (∨^{R_k} S¹) ∨ (∨^{Q_k} S²),          (1)

where

    R_k = (C−1) S(k+1,2) + (2e₀+2n+1) S(k+1,3),
    Q_k = D S(k+1,2) + 2Y S(k+1,3) + 6t S(k+1,4).        (2)

An empty wedge contributes no summand. The copy of K in (1) retains its
full homotopy type, including any fundamental group or torsion; it is not
replaced by its Betti numbers. Formula (2) is computed from G without
constructing any exponentially growing iterate.

**Exact asphericity boundary.** For positive iterates:

* Cl(M(G)) is aspherical exactly when every L_v is a forest.
* Cl(M²(G)) is aspherical exactly when every edge of G belongs to at most
  one triangle.
* For every k≥3, Cl(Mᵏ(G)) is aspherical exactly when G is triangle-free.

In every positive case, the complex actually collapses to a graph by
triangle/free-edge elementary collapses. Every simplicial subcomplex also
collapses to a graph, and hence every connected such subcomplex is
aspherical. This gives a constructive inheritance statement for this
specific class, not a proof of Whitehead's general conjecture.

The first positive iterate that is nonaspherical is therefore 1 if D>0,
2 if D=0<Y, and 3 if D=Y=0<t. If t=0, there is no such iterate.

## 2. One-step cone decomposition

We first explain why this is a homotopy statement and not merely a
homology recurrence. Before adding a, the clique complex of M(G) is

    K ∪ ⋃_v (v′ * Cl(L_v)).                              (3)

Distinct clones are nonadjacent, so the new cones meet only inside K.
The attaching inclusion Cl(L_v)→K is nullhomotopic: the old vertex v
already supplies the cone v*Cl(L_v) inside K. A cone attached along a
nullhomotopic map is homotopy equivalent to a wedge with the unreduced
suspension of its base. This is the standard mapping-cone gluing fact
(Hatcher, Proposition 0.18).
It applies successively in (3), since each nullhomotopy stays inside the
original K, independently of all previously attached cones.

Consequently (3) has homotopy type

    K ∨ ⋁_v Σ Cl(L_v).

Since G is K₄-free, Cl(L_v)=L_v is one-dimensional. For a nonempty finite
graph L with c components and cycle rank d,

    ΣL ≃ (∨^{c−1} S¹) ∨ (∨^d S²).                       (4)

For example, collapse a spanning tree in each component; the suspension
of the remaining c basepoints gives c−1 circles, while each graph loop
suspends to a two-sphere. This also covers a graph consisting entirely
of isolated vertices. Using a reduced suspension without accounting for
disconnected components would incorrectly omit the circles.

The apex adds precisely n edges from a new vertex to n points of the
already connected space (3). The first is a contractible whisker; each
of the remaining n−1 edges adds a circle up to homotopy. No two-simplex
contains a because clones are independent. Combining these observations,

    Cl(M(G)) ≃ K ∨ (∨^{C−1} S¹) ∨ (∨^D S²).             (5)

Indeed, the circle count is n−1+Σ_v(c_v−1)=C−1. For the sphere count,
Σ_v |E(L_v)|=3t and Σ_v |V(L_v)|=2m, giving D=3t−2m+C.

The mapping-cone and graph-gluing facts are classical. The construction
checks their hypotheses, including nonempty bases, connected ambient space,
simultaneous nullhomotopies, and the absence of apex triangles.

## 3. Link structure and statistic recurrences

For any graph F, let Sh(F) retain F and add an independent clone of each
vertex adjacent to its old neighbors, with no apex. The vertex links in
M(G) have the following exact graph descriptions:

    L_(old v) = Sh(L_v),
    L_(clone v′) = L_v ⊔ {a},
    L_a = the edgeless graph on n clones.                (6)

For an isolated vertex of F, Sh(F) has two isolated vertices. For a
nontrivial connected component of F, Sh(F) is connected: the old copy is
connected and each clone meets it. Thus

    c(Sh(F)) = c(F) + i(F),

where i(F) counts isolated vertices. A neighbor u is isolated in L_v
exactly when uv lies in no triangle. Hence Σ_v i(L_v)=2e₀.

Every triangle of M(G) is either an old triangle or obtained from an old
triangle by replacing exactly one of its three vertices by its clone.
There are four choices. K₄-freeness is preserved: an all-old K₄ would
already lie in G, a K₄ with one clone would give a K₄ in G after replacing
that clone by its old vertex, and a K₄ cannot contain two clones or a.
Connectedness is preserved as well.

For an old edge e, its triangle multiplicity becomes 2t_e; for either
mixed lift of e it is t_e. Apex edges lie in no triangle. Therefore the
statistics n_j,m_j,t_j,e_j,C_j of Mʲ(G), with e_j denoting its e₀ statistic,
satisfy

    n_(j+1) = 2n_j+1,
    m_(j+1) = 3m_j+n_j,
    t_(j+1) = 4t_j,
    e_(j+1) = 3e_j+n_j,
    C_(j+1) = 2C_j+2e_j+2n_j.                           (7)

These are structural identities for all G in the stated domain, not
extrapolations from sampled iterates.

## 4. Solving the iteration

By (5), each step adds C_j−1 circles and D_j=3t_j−2m_j+C_j two-spheres.
Induction using (7) gives

    n_j = (n+1)2^j−1,
    m_j = (m+n+1/2)3^j−(n+1)2^j+1/2,
    e_j = (e₀+n+1/2)3^j−(n+1)2^j+1/2,
    C_j = (2e₀+2n+1)3^j+(C−2e₀−2n−2)2^j+1,
    D_j = 3t4^j−2(m−e₀)3^j+(C−2e₀)2^j.                (8)

Summing for 0≤j<k,

    R_k = (2e₀+2n+1)(3^k−1)/2
          +(C−2e₀−2n−2)(2^k−1),
    Q_k = t(4^k−1)−(m−e₀)(3^k−1)+(C−2e₀)(2^k−1).

The classical identities

    S(k+1,2) = 2^k−1,
    2 S(k+1,3) = 3^k−2·2^k+1,
    6 S(k+1,4) = 4^k−3·3^k+3·2^k−1

follow, for instance, by assigning k elements to r boxes with one box
distinguished and all the other r−1 boxes nonempty, then dividing by
(r−1)! to forget their labels. Substituting the
definitions of D and Y produces exactly (2). All coefficients in (2) are
nonnegative; there is no cancellation concealed in the asphericity test.
This proves (1) for every k≥0. ∎

## 5. Asphericity and actual collapses

If Q_k>0, (1) has a two-sphere as a retract, so its second homotopy group
is nonzero. A vanishing H₂ argument alone would not suffice in the other
direction. We instead prove a collapse statement.

Suppose D=0. Every graph L_v is a forest. Any subcomplex of K containing
a triangle has a triangle/free-edge pair: otherwise each edge of every
triangle would lie in at least two triangles. At any incident vertex, its
nonempty link subgraph would then have minimum degree at least two and
would contain a cycle, contradicting the forest condition. Removing such
pairs until no triangles remain collapses K to a graph.

The same conclusion holds for Cl(M(G)). In each cone v′*L_v, root every
tree component of L_v and peel its leaves. A leaf edge xy gives the
triangle v′xy with free edge v′y; remove the pair and continue toward the
root. The cone eventually leaves one edge from v′ to each component root.
The old base is never removed during these operations. Edges to a lie in
no triangles and cannot obstruct freeness. After processing all clones,
all remaining triangles lie in K. Apply its preceding triangle/free-edge
collapse sequence. Thus Cl(M(G)) collapses to a graph when D=0.

Any triangle/free-edge collapse sequence in a two-dimensional simplicial
complex restricts to every subcomplex: perform a listed removal when its
triangle is present, and skip it otherwise. A present triangle brings its
edge with it, and that edge remains free since the subcomplex has no extra
cofaces. A retained edge from a skipped step cannot be in a later triangle,
by its original freeness. All subcomplex triangles are eventually removed.
This proves the stated hereditary collapse conclusion.

For positive k, Q_k=0 implies D=0 because S(k+1,2)>0. Moreover Q_k is the
sum of the nonnegative D_j, so D_(k−1)=0. Apply the collapse argument to
the last step M(M^(k−1)(G)). Hence Q_k=0 is sufficient for asphericity
and for hereditary collapse, as well as necessary.

Finally,

    Q_1=D,       Q_2=3D+2Y,       Q_3=7D+12Y+6t.          (9)

Here Y=0 means every edge belongs to at most one triangle. In that case
every L_v is a matching with possible isolated vertices, so D=0.
Conversely D=Y=0 certainly implies Y=0. For k≥3, S(k+1,4)>0, so Q_k=0
requires t=0; triangle-free graphs have D=Y=t=0. This proves all of the
asphericity assertions and the exact first-failure classification. ∎

As a quantitative structural consequence, Q_3≥6t, with equality exactly
when every edge belongs to at most one triangle. Thus triangles cannot
postpone the creation of sphere summands beyond three iterations.

## 6. Sharp examples and the dimension boundary

All three failure times occur even when the starting clique complex is
contractible.

* For the four-rim wheel W₄, D=1, so the first iterate contains a sphere
  summand. Its initial clique complex is a cone on a four-cycle.
* For the diamond K₄ minus an edge, D=0 and Y=1. The first iterate is a
  wedge of three circles; the second is a wedge of 18 circles and two
  two-spheres. The initial complex is two triangles sharing an edge.
* For K₃, D=Y=0 and t=1. The first two iterates are wedges of two and
  13 circles, respectively. The third is a wedge of 56 circles and six
  two-spheres. This makes the universal three-step bound sharp.

K₄-freeness cannot be omitted from (2) or the forest criterion. For G=K₄,
the links are filled triangles, not one-dimensional cycles. Each cone in
(3) attaches along a contractible complex, so Cl(M(K₄)) is a wedge of
three circles. Treating its links as graphs would incorrectly predict
four sphere summands. The code rejects this input for the stated theorem
and independently checks it as an out-of-domain control.

## 7. Evidence and novelty boundary

The proof uses elementary mapping-cone gluing, graph suspensions, link
incidence and classical Stirling identities. Those tools, and the Mycielski
construction itself, are prior mathematics. The assertion under study is
the exact all-iterate clique-complex wedge law and its sharp local
asphericity and collapse classification. Bounded primary-source searches
did not locate this statement; historical priority is unestablished.
See SOURCES.md for the distinctions from related Mycielski topology.

`construct.py` evaluates (2), builds ordinary lifts, and produces legal
triangle/free-edge traces. `verify.py` independently builds lifts through an
all-pairs adjacency predicate, enumerates cliques and computes boundary
ranks, checks each statistic recurrence, and replays every collapse pair.
It checks 709 connected K₄-free labelled bases among all graphs on two
through five vertices; six named fixtures through three iterations; and
a flag projective-plane fixture over both F₂ and F₃ to retain the torsion
distinction. Finite-field agreement does not establish an integral homotopy
equivalence. That equivalence and the arbitrary-k claim are proved above.

The checks are author corroboration, not independent peer review or a
proof-assistant formalization. No general asphericity decision algorithm,
equivariant splitting, higher-dimensional classification, generalized-height
Mycielski theorem, or resolution of Whitehead's conjecture is claimed.
