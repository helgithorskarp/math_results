# Component-parity and alternating-cycle normal forms

All graphs in the main theorem are finite and connected.  Parallel edges do
not cause a problem, although the conjectural application is to simple
bridgeless cubic graphs.  A loop created by contraction contributes two to
the degree of its quotient vertex.

For an edge set `S`, say that `S` **contains an odd cut** if there is a
nonempty proper vertex set `X` such that `delta_G(X)` is a subset of `S` and
has odd cardinality.

## 1. The general cut-compression lemma

Let `G` be any connected graph and `S` a subset of its edges.  Form `R_S` by
contracting each component of `G-S`; the edges of `S` become edges of this
multigraph, possibly loops.

**Lemma.** The following are equivalent.

1. `S` contains no odd cut of `G`.
2. Every vertex of `R_S` has even degree.
3. Every component `K` of `G-S` is incident with an even number of edges of
   `S` having their other endpoint outside `K`.

**Proof.** Conditions 2 and 3 are the same statement.  If a component `K`
has odd boundary, its boundary is an odd cut contained in `S`.

Conversely, suppose `delta_G(X)` is contained in `S`.  No edge of `G-S`
crosses the cut, so `X` is a union of components of `G-S`.  It therefore
corresponds to a vertex set `U` of `R_S`, and

```text
|delta_G(X)| = |delta_{R_S}(U)|
             = sum_{u in U} deg_{R_S}(u)  (mod 2).
```

If every quotient degree is even, this cut is even.  This proves all three
conditions equivalent.  Notice that loops disappear from cuts and
contribute two to degrees, consistently on both sides.  QED.

Thus a proposed pair of perfect matchings has a linear-size certificate for
all of its odd-cut constraints: contract the components after deleting the
intersection and check quotient degrees.

## 2. The cubic two-factor normal form

Let `G` be a connected cubic graph and let `M,N` be perfect matchings.  Put

```text
F = G-M,             S = M intersection N,
A = M-N = M-S.
```

The graph `F` is a disjoint union of cycles.  Let `Q_M` be the multigraph
obtained by contracting each cycle of `F`; every edge of `M` becomes an edge
of `Q_M`.  A matching edge with both endpoints on the same `F`-cycle becomes
a loop.  Let `Q_M[A]` be the spanning subgraph whose edge multiset is `A`.
Call a vertex of `Q_M` odd when its contracted `F`-cycle has odd length.

**Theorem (component-parity normal form).** The following are equivalent.

1. `M intersection N` contains no odd cut of `G`.
2. Every connected component of `Q_M[A]` contains an even number of odd
   vertices of `Q_M`.

**Proof.** Since the edge partition of `G` is `E(G)=E(F) disjoint_union M`,

```text
G-S = F union A.
```

Consequently, contracting each `F`-cycle gives a bijection between the
components of `G-S` and the components of `Q_M[A]`.

For a component `K` of `Q_M[A]`, all quotient edges leaving `K` belong to
`M-A=S`.  The handshaking identity gives

```text
|delta_{Q_M}(K)| = sum_{v in K} deg_{Q_M}(v)  (mod 2).
```

The degree of the vertex obtained from an `F`-cycle `C` is exactly `|C|`:
each vertex of `C` is incident with one edge of `M`, and a quotient loop is
counted twice.  Hence the right side is the number of odd `F`-cycles in `K`,
modulo two.

By the general cut-compression lemma, `S` contains no odd cut exactly when
every component of `G-S`, equivalently every component of `Q_M[A]`, has even
`S`-boundary.  The displayed parity identity turns this into condition 2.
QED.

This proof also gives the obstruction explicitly.  If a component of
`Q_M[A]` contains an odd number of odd contracted cycles, the union of the
corresponding vertices of `G` has an odd boundary contained in `M intersection
N`.

## 3. Canonical alternating-cycle form

For two perfect matchings, `M symmetric_difference N` is canonically a
vertex-disjoint union of even cycles whose edges alternate between `M` and
`N`.  Conversely, toggling `M` on any vertex-disjoint collection `P` of
`M`-alternating cycles produces the perfect matching

```text
N = M symmetric_difference E(P).
```

In this correspondence, `A=M-N` consists exactly of the `M`-edges on `P`.
The theorem therefore yields the following exact reformulation.

**Corollary (alternating-cycle-packing normal form).** Fix a perfect matching
`M`.  Perfect matchings `N` are in bijection with vertex-disjoint packings of
`M`-alternating cycles.  Under this bijection, `M intersection N` contains no
odd cut if and only if every component traced in `Q_M` by the `M`-edges of
the packing contains an even number of odd `F`-cycles.

This is an equivalence, not only a sufficient condition.

## 4. A parameter-uniform sufficient mechanism

**Corollary (odd-cycle-transversal alternating cycle).** Suppose `G` has a
perfect matching `M` and an `M`-alternating cycle `C` meeting every odd cycle
of `F=G-M`.  Then

```text
N = M symmetric_difference E(C)
```

is a perfect matching and `M intersection N` contains no odd cut.

**Proof.** The image of `C` after contracting the cycles of `F` is connected.
Thus all odd vertices of `Q_M` lie in one component of `Q_M[M intersection
E(C)]`; every other component is an isolated even vertex.  The number of odd
cycles in any 2-factor on an even number of vertices is even.  Hence the
distinguished component also contains an even number of odd vertices.  The
component-parity theorem applies.  QED.

The same conclusion holds for any alternating-cycle packing whose quotient
components each meet an even number of odd cycles.  The one-cycle statement
is singled out because it is a direct, readily checkable structural target
with no bound on the oddness or order of `G`.

As a small illustration, take the standard Petersen 2-factor consisting of
two 5-cycles and let `M` be the five edges between them.  The pair `M,M`
fails: `A` is empty, so the two isolated quotient vertices each contain one
odd cycle, and the five edges of `M` form the exposed odd cut.  For any other
perfect matching `N` of the Petersen graph, `M symmetric_difference N` is a
single alternating cycle meeting both 5-cycles, so the transversal corollary
certifies the pair `M,N`.  This example is illustrative, not used in the
proof.

## Scope

- The theorem does not assert that the required alternating-cycle packing
  always exists.
- It does not prove Fan--Raspaud or Berge--Fulkerson.
- Bridgelessness is unnecessary for the equivalence, but is part of the open
  conjecture to which it applies.
- The Python audit is finite corroboration only and is not used in any step
  of the universal proof.
