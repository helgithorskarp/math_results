# Triangles, prisms, and critical co-gem/bull-free graphs

All graphs are finite and simple. All forbidden configurations are induced.
A **gem** is a four-vertex path together with a vertex adjacent to all four
path vertices. A **bull** is a triangle with two pendant vertices attached
to different triangle vertices. A **co-gem** is the complement of a gem,
equivalently `P4 + P1`. The bull is self-complementary.

A **triangular prism** consists of triangles
`A = {a0,a1,a2}` and `B = {b0,b1,b2}`, with exactly the three edges
`ai bi` between them. Its complement is `C6`.

## Results and proof status

**Theorem 1 (replacement).** Let `T` be any triangle in a (gem,bull)-free
graph `H`. Delete `T`, add a vertex `p`, and join `p` to exactly those
remaining vertices having at least two neighbors in `T`. The resulting
graph is (gem,bull)-free.

This operation is defined by the stated neighborhood rule; it is not
ordinary edge contraction.

**Theorem 2 (prism component).** Every connected (gem,bull)-free graph
containing an induced triangular prism is perfect.

**Corollary 3 (critical exclusion).** For every positive integer `k`, every
`k`-vertex-critical (co-gem,bull)-free graph is `C6`-free, with no bound on
its order.

Theorem 1 and two local prism facts below use a complete finite obstruction
certificate. Everything extending them to arbitrary orders is proved here.
The certificate is checked by a separate implementation using adjacency
matrices and the definitions of gem and bull. Neither the argument nor the
checker depends on SAT output, a graph catalogue, or floating-point arithmetic.
This is a computer-assisted proof, not a proof-assistant formalization or an
independent peer review.

## 1. Completeness of the finite certificate

In `generate.py`, the fixed labeled forbidden graphs on `0,1,2,3,4` are:

* gem: edges `01,12,23,40,41,42,43`;
* bull: edges `01,12,20,03,14`.

No isomorphism quotient is used on the inputs. The generator recognizes
forbidden subgraphs by the edge codes of all permutations of these graphs.
The checker does not import these codes or the generator. It recognizes
a gem by a universal vertex whose remaining four vertices have degrees
`1,1,2,2`, and a bull by a triangle and two nonadjacent pendant vertices
with distinct neighbors on that triangle. On four vertices, the degree
sequence `1,1,2,2` characterizes a path.

### 1.1 The triangle replacement

If replacement creates a forbidden induced graph `F`, that graph must use
the new vertex `p`. Choose an isomorphism to one of the two labeled forbidden
graphs and let `r` be the label corresponding to `p`. There are two choices
of `F` and five choices of `r`.

Its other four vertices induce exactly `F-r`. In the original graph, retain
these four vertices and the three vertices of `T`. These seven vertices have
fixed edges inside each of the two sets. The only choices are the four
neighborhoods into `T`. For a vertex adjacent to `r` in `F`, that neighborhood
has size two or three; otherwise it has size zero or one. In each case there
are exactly four choices. Thus exactly `2 * 5 * 4^4 = 2560` assignments cover
every possible new forbidden graph, including those with arbitrary labels
and arbitrary vertices elsewhere in `H`.

For each assignment the certificate identifies five of the original seven
vertices inducing a gem or bull. Verification of every entry contradicts
the assumption on `H` and proves Theorem 1.

The ten rows of the `majority` field are ordered first by gem/bull, then by
`r=0,...,4`. The four vertices of `F-r` keep their increasing original order
and receive new labels `0,...,3`; triangle vertices receive labels `4,5,6`.
A neighborhood in the triangle is a three-bit integer. The choices in each
coordinate are `(0,1,2,4)` or `(3,5,6,7)`, in that order. Each row enumerates
the Cartesian product lexicographically, so the last coordinate changes
fastest. There are 256 entries per row.

### 1.2 Prism neighborhoods

Fix the prism with `A={0,1,2}`, `B={3,4,5}` and matching `03,14,25`.
For a vertex `x` outside the prism let `s` be its six-bit neighborhood mask,
where bit `j` represents vertex `j`. There are exactly 64 possibilities.
The `attachment` field provides a forbidden witness for every mask except

```
0, 3, 5, 6, 7, 14, 15, 21, 23, 24, 28,
35, 39, 40, 42, 48, 49, 56, 57, 58, 60.
```

The checker also verifies directly that each listed mask creates neither
forbidden graph. In every nonzero listed mask, exactly one of `A` and `B`
contains at least two neighbors of `x`. Consequently:

**Lemma 4.** Every vertex with a neighbor in an induced prism in a
(gem,bull)-free graph has at least two neighbors in exactly one of its
two distinguished triangles.

### 1.3 A prism dominates its component

Consider a prism on labels `0,...,5`, a vertex `x=6` anticomplete to the
prism, and an adjacent vertex `y=7` having some neighbor in the prism.
Only the nonempty neighborhood of `y` in the prism is unspecified: there
are exactly 63 choices. The `isolation` field supplies a gem or bull in
each of these eight-vertex graphs.

**Lemma 5.** Every induced prism dominates its connected component in a
(gem,bull)-free graph.

Indeed, if a vertex in that component has distance at least two from the
prism, a shortest path supplies an edge `xy` with `x` anticomplete to the
prism and `y` having a neighbor there. One of the 63 verified witnesses
is a contradiction. The argument covers paths of any length.

### 1.4 Certificate encoding and counts

All entries are bytes encoded as lowercase hexadecimal. The value
`2*j+t` names the `j`th five-element subset, starting with zero and in
lexicographic order, and its forbidden type `t` (`0=gem`, `1=bull`).
The neighborhood field uses `255` for the allowed masks. The checker
requires exact field names, dimensions, and encodings, rejects an invalid
witness, and checks every allowed neighborhood directly.

The certificate covers 2560 replacement cases, 64 attachment cases, and
63 isolation cases. It verifies `2560 + 43 + 63 = 2666` obstruction
witnesses and the 21 allowed attachments. No inference rests just on a
matching aggregate count.

## 2. A parity obstruction of unbounded length

**Lemma 6.** In a (gem,bull)-free graph, an induced odd cycle of length at
least five cannot have two nonadjacent outside vertices `p,q` such that
each cycle vertex is adjacent to exactly one of `p,q`.

Color each cycle vertex by its neighbor in `{p,q}`. If the cycle is
monochromatic, its color vertex and four consecutive cycle vertices induce
a gem. Otherwise, consider the maximal monochromatic runs around the cycle.
Their number is even, because their colors alternate cyclically.

A run of length at least four gives a gem with its color vertex and four
consecutive vertices. A run of length exactly two, say `u,v`, gives a bull:
its color vertex together with `u,v` is the triangle, and the cycle vertices
immediately before and after the run are the pendant vertices. They have
the other color, and are nonadjacent because the cycle has length at least
five. Thus each run has length one or three. An even number of odd run
lengths has even total length, a contradiction. This proves the lemma for
all odd lengths, without a finite length cutoff.

## 3. Disjoint copies and perfection

**Lemma 7.** Replacing vertices by nonempty independent sets of false twins
preserves the class of (gem,bull)-free graphs.

Neither the gem nor the bull has two nonadjacent vertices with identical
neighborhoods. An induced forbidden graph using two copies of one original
vertex would have such a pair. Otherwise projection to the original vertices
is injective and gives an induced forbidden graph in the original graph.
This proves the lemma. In particular, one may keep each old vertex and add
an independent copy of it.

We now prove Theorem 2. Suppose a connected (gem,bull)-free graph `H`
contains a prism and is not perfect. An odd antihole of length at least
seven contains a gem: in its complementary cycle, take four consecutive
vertices and a vertex anticomplete to those four. For cycle labels
`0,...,m-1`, the vertices `0,1,2,3,5` work for every `m>=7`.
The complement of their `P4+P1` is a gem. The Strong Perfect Graph Theorem
therefore supplies an induced odd hole `C` in `H`, of length at least five
(a five-antihole is itself a five-hole).

The hole and prism may overlap. Apply Lemma 7 to give each of the six prism
vertices a fresh false-twin copy, retaining all original vertices. The six
new copies induce a prism `P` disjoint from the unchanged hole `C`.
The graph stays connected and (gem,bull)-free. By Lemma 5, every vertex of
`C` has a neighbor in `P`, and Lemma 4 says it has a majority of neighbors
in exactly one of the two triangles `A,B` of `P`.

Replace `A` by `p` using Theorem 1. Each vertex of `B` originally had exactly
one neighbor in `A`, so `p` is anticomplete to `B`. Next replace `B` by `q`.
Both resulting graphs remain (gem,bull)-free. The vertices `p,q` are
nonadjacent, the hole `C` is unchanged, and every vertex of `C` is adjacent
to exactly one of `p,q`. This contradicts Lemma 6. Theorem 2 follows.

The only external structural theorem used in this proof is the
[Strong Perfect Graph Theorem](https://annals.math.princeton.edu/2006/164-1/p02).
It also implies closure of perfect graphs under complementation, since
the absence of odd holes and odd antiholes is symmetric under complementation.

## 4. Consequence for vertex-critical graphs

A nonempty graph `G` is `k`-vertex-critical if `chi(G)=k` and deletion of
any vertex lowers the chromatic number. Suppose such a (co-gem,bull)-free
graph contains `C6`. Its complement `H` is (gem,bull)-free and contains the
complementary prism. Let `M` be the vertex set of the component of `H`
containing this prism. Theorem 2 makes `H[M]` perfect, and hence `G[M]`
perfect.

Distinct components of `H` correspond to complete join factors of `G`.
Chromatic number adds across a join, so vertex-criticality of `G` forces
each of its nonempty join factors, in particular `G[M]`, to be vertex-critical.
A perfect vertex-critical graph is a clique: a maximum clique already
requires all its colors, so any vertex outside it could be deleted without
lowering chromatic number. But `G[M]` contains the original induced `C6`,
contradicting that it is a clique. This proves Corollary 3.

## 5. Exact relation to the research target

The accepted target is equality of the critical (co-gem,bull)-free class
with the critical `(P3+P1)`-free class, for every `k`. The earlier
[critical amplification theorem](../proof.md) already proves equality
after adding `P5`-freeness. Corollary 3 now removes **every** `C6`-containing
candidate, at every chromatic number and order. It does not remove all
`P5`-containing candidates. The remaining task is the all-order
`(co-gem,bull,C6)`-free critical case containing `P5`; the full equality and
the unrestricted `k=7` decision remain open in this work.

A tempting shortcut is invalid: an induced `P3 a-b-c` plus an isolated
vertex `u`, with incomparable neighborhoods of `a,c`, need not extend to
a `C6` in a (co-gem,bull)-free graph. Take triangles `{a,b,x}` and `{b,c,y}`
sharing only `b`, together with isolated `u`. This graph has no `P4`, bull,
or `C6`, but `N(a)={b,x}` and `N(c)={b,y}` are incomparable. It is not
critical. In particular, one cannot use this shortcut to upgrade Corollary 3
to the full target. No such upgrade is claimed.
