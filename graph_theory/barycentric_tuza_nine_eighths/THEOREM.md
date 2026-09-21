# Barycentric triangle packing with a 2-edge-connected facet dual

## 1. Definitions and statement

Let `T` be a finite nonempty pure two-dimensional abstract simplicial
complex.  Its facets are three-element sets, and every edge is assumed to
belong to at most two facets.  Let

```text
f = f_2(T)
```

and let `D=D(T)` be the **facet-dual graph**: its vertices are the facets of
`T`, and two are adjacent exactly when they share an edge.  Distinct
triangular facets cannot share two different edges, so `D` is simple and
subcubic.

Put `G=(sd T)^(1)`, the one-skeleton of the barycentric subdivision.  Write
`nu_triangle(G)` for the maximum number of edge-disjoint graph triangles and
`tau_triangle(G)` for the minimum number of graph edges meeting every graph
triangle.

**Theorem.** If `D` is 2-edge-connected, then

```text
kappa(T) <= floor(f/3),                              (1)
nu_triangle(G) >= 3f-floor(f/3),                    (2)
tau_triangle(G) = 3f <= (9/8)nu_triangle(G).        (3)
```

Here `kappa(T)` is the minimum number of facets whose deletion leaves a
coherently orientable family.  Coherence means that adjacent retained facets
induce opposite directions on their common edge.

## 2. Imported exact identities

Choose an arbitrary reference orientation on every facet.  Each edge of `D`
then carries a binary constraint: the two facet labels must differ when the
reference directions on their common edge agree, and must agree when those
directions oppose.  This gives a signed subcubic graph, well-defined up to
switching.

Deleting facets until the constraints are consistent is precisely vertex
frustration.  Sivaraman's theorem for subcubic signed graphs identifies
vertex frustration with the edge frustration index `F(D)`.

The earlier barycentric orientation-defect theorem proves

```text
tau_triangle(G)=tau_triangle*(G)=nu_triangle*(G)=3f,
nu_triangle(G)=3f-kappa(T).                         (4)
```

Thus only (1) is new here.  Once it is proved, (2) follows from (4), and

```text
nu_triangle(G) >= 3f-f/3 = 8f/3
```

gives (3).

## 3. Boundary parity

Call an edge of `T` a **boundary edge** when it belongs to exactly one facet.
Let `b` be their number and let `i` be the number of edges belonging to two
facets.  Internal edges are in bijection with dual edges, so

```text
i=|E(D)|,              3f=2i+b,
b=3f-2|E(D)|=sum_(F in V(D))(3-deg_D(F)).           (5)
```

**Lemma 1.** Every vertex of `T` is incident with an even number of boundary
edges.  In particular, `b` cannot equal one.

**Proof.** Fix a vertex `x`.  Let `t_x` be the number of facets containing
`x`, and let `i_x,b_x` count the internal and boundary edges incident with
`x`.  Count pairs `(F,e)` in which `F` contains `x` and `e` is one of the two
edges of `F` incident with `x`.  Counting first by facets and then by edges
gives

```text
2t_x=2i_x+b_x.
```

Hence `b_x` is even.  A single boundary edge would give boundary degree one
at each endpoint, a contradiction. `square`

## 4. Normalizing a closed triangle complex

Suppose `b=0`.  Every edge then belongs to exactly two facets.  For a vertex
`x`, its link is a finite 2-regular graph: each link vertex corresponds to an
edge incident with `x`, and the two facets containing that edge give it link
degree two.  Thus the link is a disjoint union of cycles.

Split `x` into one new vertex for each component of its link, and replace
`x` in the incident facets accordingly.  Performing this operation at every
vertex produces a closed triangulated surface `T_tilde`.  It has exactly the
same facets and shared facet-edges as `T`.  Consequently

```text
D(T_tilde)=D(T)
```

with the same signed orientation constraints.  Since `D` is connected,
`T_tilde` is connected.  This is the standard vertex normalization of a
two-dimensional pseudomanifold.

**Lemma 2.** A closed nonorientable triangulated surface has at least ten
triangular facets.

**Proof.** Let its numbers of vertices, edges, and facets be `v,e,f`.  Then
`3f=2e`.  Its Euler characteristic satisfies

```text
chi=v-e+f=v-f/2,
e=3(v-chi).
```

A connected closed nonorientable surface has `chi<=1`.  Its one-skeleton is
a simple graph, so

```text
3(v-1) <= e <= v(v-1)/2.
```

As `v>1`, this forces `v>=6`.  Therefore

```text
f=2(v-chi) >= 2(v-1) >= 10.
```

`square`

The signed constraint graph is balanced exactly when the normalized surface
is orientable: a balancing labels the facets with coherent orientations, and
conversely a surface orientation supplies those labels.  Thus an unbalanced
closed signed facet dual with fewer than ten facets is impossible.

## 5. Eliminating the five signed exceptions

Chen--Li--Wang prove that every 2-edge-connected simple signed subcubic graph
on `f` vertices satisfies

```text
F(D)<=f/3                                             (6)
```

apart from the five switching classes `Gamma_1,...,Gamma_5` displayed in
their Figure 1.

Their `Gamma_2` has four vertices of degree three and one of degree two.
If it were a facet dual, (5) would give exactly one boundary edge.  Lemma 1
rules this out, independently of its signs.

The other four underlying graphs are cubic.  `Gamma_1` has four vertices;
`Gamma_3,Gamma_4,Gamma_5` each have eight.  A complex having any of them as
facet dual would have no boundary edges.  All four signed classes have
positive frustration index, so their normalized surfaces would be
nonorientable.  Lemma 2 forbids this with four or eight facets.

No exceptional class is therefore realizable.  Inequality (6) applies to
the signed facet dual of `T`, and Sivaraman's equality gives

```text
kappa(T)=F(D)<=f/3.
```

Because `kappa(T)` is integral, this is (1).  Equations (2)--(3) now follow
from (4). `square`

## 6. Scope and proof/computation boundary

The theorem requires the facet-dual graph to be 2-edge-connected.  It does
not assert the `9/8` ratio for facet duals with bridges, higher edge
incidence, polygonal facets, or arbitrary graphs in Tuza's conjecture.

The proof uses two external structural theorems: Sivaraman's equality of
vertex and edge frustration for signed subcubic graphs, and the
Chen--Li--Wang five-exception bound.  Equation (4) is the previously accepted
barycentric packing theorem.  The boundary-parity and normalization
arguments eliminating every exception are self-contained here.

`verify.py` separately transcribes the five exceptions, computes their
frustration by definition, and checks every canonical signed side gluing.
That finite audit protects the figure transcription and local conventions;
it is not the proof of the universal reduction.
