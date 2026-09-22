# Optimal clique cores for two-neighborhood split graphs

All graphs in this note are finite, simple, and unweighted. A triangle edge
cover is a set of edges meeting every triangle; its minimum size is denoted
by `tau(G)`. A triangle packing consists of edge-disjoint triangles and has
maximum size `nu(G)`. A clique core means the edges surviving inside a
specified clique part, not the whole surviving graph.

## Main theorem and scope

Let `V(G)=C disjoint-union I` be a split partition. Vertices of `I` of degree
at most one can be discarded. Suppose the remaining vertices of `I` have
at most two distinct neighborhoods in `C`.

**Theorem 1.** There is a minimum triangle edge cover `D` for which
`G[C]-D` is bipartite. The cover number and a compact optimal-cover
certificate can be computed using `O(|C|^3)` integer arithmetic operations,
without expanding the multiplicities of the two neighborhood types.

**Theorem 2.** The number two in Theorem 1 is best possible. For each integer
`t>=2` there is a split graph with exactly three active neighborhood types
and clique order `2t+3` such that imposing bipartiteness on the surviving
clique core increases the minimum cover size by exactly one.

These theorems are uniform in clique order and neighborhood multiplicity.
They do **not** prove Tuza's inequality `tau(G)<=2 nu(G)`, even for the
two-type class. They eliminate the arbitrary triangle-free clique-core
optimization from its covering side; a packing/exchange theorem is still
needed. The assertion that the **whole** surviving graph can be bipartite
is false even with two types; see Section 6.

## 1. Two protected independent sets

For `A,B subset C`, let

    J(A,B) = K_C - ( E(K_A) union E(K_B) ).

Put `X=A intersect B`, `Y=A\B`, `Z=B\A`, and `W=C\(A union B)`, with
sizes `x,y,z,w`, respectively. Thus

    J(A,B) = K_W join (K_{Y,Z} disjoint-union I_X).

**Lemma 3.** A largest triangle-free spanning subgraph of `J(A,B)` can be
chosen bipartite. Consequently its edge count equals `MaxCut(J(A,B))`.

### Proof

Take a triangle-free spanning subgraph `F` of maximum edge count. Each of
`X,Y,Z` is an independent set in the host, and its vertices have identical
allowed neighbors. Within one such class, choose a vertex of maximum
degree in `F` and replace every other vertex of the class by its false twin:
give it exactly the chosen vertex's neighborhood, with no internal edges.

This is permitted by the host, keeps the graph triangle-free, and cannot
decrease its edge count. Triangle-freeness follows because the neighborhood
of a vertex in a triangle-free graph is independent. Performing this for
`X,Y,Z` in sequence preserves the classes already made homogeneous: all
vertices of an earlier class had the same adjacency to every representative
of a later one. We therefore still have an edge-maximal triangle-free
subgraph in which each of `X,Y,Z` is a false-twin class. Empty classes cause
no difficulty.

Among such edge-maximal subgraphs, choose one maximizing

    sum_Q |Q|^2,

where `Q` runs over the false-twin equivalence classes of vertices of `W`,
using their neighborhoods in the **whole** graph `F`.

We claim that any two nonadjacent vertices of `W` are false twins. Otherwise
let `Q,R` be their distinct false-twin classes. There are no edges between
`Q` and `R`. Their representative degrees must be equal: if not, cloning
the lower-degree class to a representative of the higher-degree class
strictly increases the edge count. Such cloning is always allowed because
every vertex of `W` is universal in the host. It also preserves the
homogeneity of `X,Y,Z` and triangle-freeness.

When the degrees are equal, cloning all of `Q` to `R` preserves the edge
count and merges `Q,R`. No other false-twin class is split: its vertices
had identical adjacency to both classes and are changed identically.
Thus the displayed sum strictly increases, a contradiction.

It follows that `F[W]` is complete multipartite with each part a false-twin
class in the whole graph. It has at most two nonempty parts, since three
parts would contain a triangle.

If there are zero or one such parts, the entire graph is a blow-up of a
triangle-free graph on at most four vertices (the nonempty classes among
`X,Y,Z,W`). Every triangle-free graph on at most four vertices is bipartite.

Otherwise write the two parts as `P,Q`, with all `P-Q` edges present.
Each of `X,Y,Z` is adjacent to at most one of `P,Q`, or a triangle would
occur. The graph on the four classes `Y,Z,P,Q` is triangle-free and hence
bipartite. The class `X` has no neighbors in `Y,Z` and attaches to at most
one of `P,Q`, so it can be added to that bipartition. Thus `F` is bipartite.

Finally every cut is triangle-free, while the bipartite `F` is contained
in a cut of the host. The two optima are equal. QED.

## 2. An explicit three-expression host formula

For `l,r>=0` with `l+r<=k`, define

    B_k(l,r) = max { h(k-h) : l <= h <= k-r, h integer }.

It is evaluated by `h=max(l,min(floor(k/2),k-r))`. Define, with
`k=x+y+z+w`,

    f(x,y,z,w) = max {
        B_k(x+y+z,0),
        B_k(x+y,z) - xz,
        B_k(x+z,y) - xy
    }.

**Lemma 4.** The value in Lemma 3 is exactly `f(x,y,z,w)`.

### Proof

A maximum cut can be chosen with each independent host class `X,Y,Z`
monochromatic. With all other vertices fixed, each vertex in one of these
classes has the same cut gain from either side. Put the whole class on a
best side; doing this successively never decreases the cut.

If `Y,Z` have the same side, their mutual edges contribute nothing. For a
fixed split of `W`, all of `X,Y,Z` can instead be put together opposite a
larger part of `W`, without decreasing the cut. This gives the first term.

If `Y,Z` have opposite sides, `X` shares a side with one of them. With
`X,Y` together and `Z` opposite, all crossing pairs are allowed except the
`xz` pairs between `X,Z`; splitting `W` optimally gives the second term.
The other choice gives the third term. Each term is realized by the
described cut. QED.

## 3. From protected sets to minimum covers

Let the two neighborhoods be `S,T subset C`, of multiplicities `m,n`.
Write `q=binom(k,2)` for `k=|C|`.

For a fixed surviving triangle-free clique core `F`, the retained neighbors
of each independent-side vertex must be independent in `F`. Hence

    tau(G) = min_{F triangle-free on C}
       [ q-e(F) + m(|S|-alpha(F[S])) + n(|T|-alpha(F[T])) ].       (1)

This general split-graph cover reduction appears as Lemma 1, equation (3), in
Zeng [Z]; the elementary argument above also proves it directly. For
vertices of the same type, an optimal cover can always use the same
retained neighborhood.

Choose a minimizing `F` and maximum independent sets `A` of `F[S]` and
`B` of `F[T]`. Then `F subset J(A,B)`. Replacing `F` by a largest
triangle-free subgraph of `J(A,B)` cannot increase the cover cost: it
retains at least as many clique edges, and `A,B` remain independent.
Lemma 3 lets us make that replacement bipartite. The resulting cover is
therefore still minimum. This proves the structural assertion of Theorem 1.

For the exact formula, put

    a=|S\T|, b=|T\S|, c=|S intersect T|, d=|C\(S union T)|,
    k=a+b+c+d.

For `A subset S`, `B subset T`, their three sizes
`x=|A intersect B|`, `y=|A\B|`, `z=|B\A|` are feasible exactly when

    0 <= x <= c,  y,z >= 0,
    max(0,y-a) + max(0,z-b) <= c-x.                            (2)

Indeed, reserve `x` common vertices for the intersection. At least
`max(0,y-a)` of the `y` vertices and `max(0,z-b)` of the `z` vertices must
come from the remaining intersection cell, and these choices are disjoint.
Conversely choose exactly those minimum numbers there, then use the
appropriate exclusive cells for all remaining vertices. Condition (2)
guarantees that this is possible and implies `x+y+z<=k`.

We obtain the exact identity

    tau(G) = q + m(a+c) + n(b+c)
       - max_{(x,y,z) satisfying (2)}
           [ f(x,y,z,k-x-y-z) + m(x+y) + n(x+z) ].              (3)

For completeness, both directions of this optimization are important.
Every cover yields a surviving core and retained independent sets, so its
number of retained edges is at most a candidate on the right. Conversely,
any feasible triple is realized by actual sets `A,B`; Lemma 4 supplies a
triangle-free core with exactly `f` edges, and retaining precisely `A,B`
at their respective independent vertices produces a valid cover with the
stated size. No independence-number optimality of these chosen sets is
assumed in this converse.

There are `O(k^3)` feasible triples, each evaluated with three clamped
quadratic products. Arithmetic is on integers with bit length polynomial
in the input bit length, including binary-encoded `m,n`. The maximizing
triple, one of three cut modes, and the number of `W` vertices on its left
side form a constant-length certificate relative to the six input counts.
Materializing the cover itself additionally costs its output size.

## 4. Three types can force an odd clique core

Fix `t>=2`. Form a clique on

    C = {v,c,d} disjoint-union P disjoint-union Q,
    |P|=|Q|=t.

Use three independent-side neighborhood types

    S1 = P union {d},
    S2 = P union Q,
    S3 = {c} union Q,

each with multiplicity `M=binom(2t+3,2)+1` (any larger `M` also works).

Deleting all clique edges is a cover of size `q=binom(2t+3,2)`.
If a surviving clique core has even one edge inside any `Si`, each of
the `M` copies of that type must lose at least one spoke. Such a cover
costs at least `M>q`. Thus every minimum cover retains all spokes and
its clique core is contained in

    J = K_C - union_i E(K_Si).

The edges of `J` are all `2t+2` edges incident with `v`, the `t` edges
from `P` to `c`, the edge `cd`, and the `t` edges from `d` to `Q`.
In particular `e(J)=4t+3`.

Deleting `vc,vd` leaves the blow-up of the five-cycle

    v -- P -- c -- d -- Q -- v,

with `4t+1` edges. Two edge-disjoint triangles `vpc` and `vdq`, for
`p in P,q in Q`, show that at least two edges must be deleted from `J`
to make it triangle-free. Therefore

    max { e(F): F subset J triangle-free } = 4t+1.             (4)

The maximum cut of `J` is `4t`. To see this, fix the side of `v`; the
vertices of each of `P,Q` can be put together on a best side once the
sides of `c,d` are known. According as neither, exactly one, or both of
`c,d` are opposite `v`, the cut optimum is respectively

    4t,  3t+2,  2t+2.

For `t>=2` their maximum is `4t`.

It follows that the unrestricted minimum cover size is `q-4t-1`,
whereas requiring a bipartite clique core gives `q-4t`. Covers that remove
spokes while leaving some `Si` non-independent cost at least `M>q` and
cannot improve either optimum. If every `Si` is independent, removing
spokes is unnecessary. This proves Theorem 2, including the exact one-edge
gap for the restricted optimum.

## 5. What this changes in the Tuza problem

The unrestricted packing problem still requires simultaneous pairwise
edge-disjoint matchings, one for each independent vertex, on their
respective neighborhoods, together with a triangle packing of the
remaining clique edges. See Zeng [Z], Lemma 2, for that exact general
split-graph reduction. Formula (3) now removes all arbitrary triangle-free
cores from the covering side for two types.

There is a useful local constraint on a genuinely nonbipartite whole
residual arising from the normal form. Suppose `A` is wholly on one side
of the clique cut while `B` meets both sides in sets of sizes `x,z`;
the missing crossing rectangle has `xz` edges. For a globally optimal
certificate with `x,z>0`, one necessarily has

    n >= max(x,z).                                            (5)

If `z>n`, stop protecting the `x` retained `B` vertices on the `A` side
and restore their `xz` crossing edges. The retained-edge objective changes
by `x(z-n)>0`, contradicting optimality. Similarly, unprotecting the `z`
vertices on the other side gives a gain `z(x-n)` if `x>n`.
The restored clique core is still bipartite and respects the surviving
protected neighborhoods, so both comparisons are legitimate.

Under (5), that rectangle can be packed completely using the `n` vertices
of type `T`: a complete bipartite graph `K_{x,z}` has a decomposition into
`max(x,z)` matchings, each assigned to a distinct center. Explicitly, pad
the smaller side to size `h=max(x,z)`, use the matchings pairing index `i`
on one side with index `i+j mod h` on the other for `j=0,...,h-1`, and then
discard pairs involving padded vertices. Distinct matching edges give
edge-disjoint centered triangles. This is a reusable packing certificate
for the exceptional rectangle, **not** a packing of the remaining cover.

The unresolved step is to combine these rectangle triangles with a packing
of the remaining edges that pays for the rest of (3), or to prove a
different uniform matching/exchange inequality. No claim about that step
is made here.

## 6. Whole-graph bipartiteness is not implied

Let `C={u,a,b}`, with three independent vertices of neighborhood `{u,a}`
and three of neighborhood `{u,b}`. Deleting `ua,ub` gives a cover of size
two; two edge-disjoint triangles show optimality. The graph has 15 edges
and maximum cut 12, so making the **whole** residual bipartite costs three.
The computation of this cut can also be done by fixing the colors of the
three clique vertices and choosing the best side for each twin class.
Its optimal clique core has the single edge `ab` and is of course bipartite.

## 7. Provenance, status, and verification

This note arose from the Discovery Net Tuza problem node
`bafkreidlaiqmklxw4swbqbmre6xqxf66u57ttopv4xo7q4guwe43i6rcei`.
The current primary-source status was checked on 2026-09-22. The retrieved
sources establish the threshold case [B], a minimum-degree condition for
split graphs [C], and a computer-assisted two-type theorem when the clique
part has order eight [Z]. None of those statements supplies the above
unbounded-order cover normal form. A targeted search did not locate this
specific extremal formula or its sharp three-type boundary; this is not
a comprehensive priority claim.

The universal theorems rely on the written symmetrization argument, not
on computation, an external solver, or a cutoff. `cover.py` implements
(3) and reconstructs certificates. `verify.py` compares it with all
triangle-free clique cores on a small regression domain, uses direct
triangle-hitting recursion on smaller full graphs, and checks the first
few members of the analytically proved obstruction family. These tests
can find errors but do not establish unbounded quantifiers. There is no
formal proof-assistant verification or independent peer review claimed.

### Primary references

- [B] M. Bonamy, Ł. Bożyk, A. Grzesik, M. Hatzel, T. Masařík, J. Novotná,
  K. Okrasa, *Tuza's Conjecture for Threshold Graphs*, DMTCS 24:1 (2022),
  article 24. [Published paper](https://dmtcs.episciences.org/9916/pdf).
- [C] L. Chahua, J. Gutierrez, *On Tuza's conjecture in dense graphs*,
  Discrete Applied Mathematics 377 (2025), 225–233.
  [Authors' manuscript](https://arxiv.org/abs/2405.11409),
  [published article](https://doi.org/10.1016/j.dam.2025.06.049).
- [Z] Z. Zeng, *Tuza's Conjecture for Split Graphs with an Eight-Vertex
  Clique Part and Two Neighborhood Types*, preprint, version 1,
  posted 2026-08-19. Not peer reviewed.
  [Primary manuscript](https://www.preprints.org/manuscript/202608.1304).
