# Multiport exterior metric closure for anchored geodesic guards

This gives an exact finite reduction for a prescribed graph fragment with any number of outside ports. The three-port case is the next step after the [reviewed two-port guard](../planar_two_geodesic_two_port_lollipop_guard_review1/REVIEW.md). The statement concerns **geodesics with endpoints in the fragment** and is a tool for positive guard arguments around [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). It does not prove that two paths suffice in every planar graph. Graphs here are finite, simple, and have unit edges; singleton paths are allowed.

Literature status checked 28 September 2026: the [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) announces a disproof of a Codsi conjecture on balanced separators in planar graphs. It gives neither the precise statement nor a witness, so its relationship to Problem 31 is unverified here.

## Exact fixed-subgraph trace theorem

Let `C` be a vertex set of a graph `H`, and let `B` be its boundary: every edge from `C` to `H-C` meets `C` in `B`. For distinct `a,b` in `B`, define `delta_H(a,b)` as the minimum length of an `a`-to-`b` path with at least one internal vertex, all outside `C`, or infinity when no such path exists. Form `T_H` from `H[C]` by adding, for each finite `delta_H(a,b)`, a fresh internally vertex-disjoint `a`-to-`b` path of that length. These model paths need not reproduce overlap among routes in `H`.

For a path `P`, its **C-trace** is `V(P) intersect C` (as a set). Call a component `D` of `H[C]` **anchored k-coverable** when some at most `k` ambient `H`-geodesics, each with both endpoints in `C`, have traces whose union contains `D`.

**Theorem.** For every `u,v` in `C`, `d_H(u,v)=d_(T_H)(u,v)`. Moreover, for each such pair, the family of C-traces of `u`-to-`v` geodesics is **identical** in `H` and `T_H`. Consequently each component of `H[C]` is anchored `k`-coverable in `H` if and only if it is anchored `k`-coverable in `T_H`, for every `k`.

**Proof.** Break a simple `H`-path with endpoints in `C` at every visit to `C`. Each maximal exterior segment joins **distinct** ports and has length at least the corresponding `delta_H`. Replace the segment by its fresh model path. This gives a `T_H`-walk of no greater length and with exactly the same C-trace. Conversely, a simple `T_H`-path with endpoints in `C` traverses each fresh model path either completely or not at all. Replace each such traversal by a chosen shortest exterior route in `H`, producing an `H`-walk of the same length and C-trace. Applying both replacements to shortest paths proves distance equality. When the starting path is geodesic, the resulting walk has length equal to that common distance. Positive unit edges force it to be simple and geodesic, so no C vertex disappears through loop erasure. This proves equality of trace families, including disconnected cases. `□`

The array `delta_H` is an **exterior route-length array**, not necessarily a metric: two finite routes through a third port cannot be concatenated into a route whose internal vertices avoid `C`. The model nevertheless captures the full shortest-path metric and geodesic traces **on C**. It makes no claim about geodesics whose endpoints lie outside `C`.

## Exact all-spanning finite criterion

Fix an ambient graph `G`, a fragment `C`, and boundary `B`. Let `F=G[C]`. Let `R(G,C)` be the set of exterior route-length arrays obtained by deleting arbitrary edges of `G` that are not wholly inside `C`. For each `F'` obtained by deleting arbitrary edges of `F` and each `delta` in `R(G,C)`, form `T(F',delta)` by adding independent fresh model paths of the finite prescribed lengths.

**Corollary.** Every spanning edge subgraph `H` of `G` has each component of `H[C]` anchored `k`-coverable if and only if every `T(F',delta)` has this property, for every `F'` and every `delta` in `R(G,C)`.

**Proof.** Internal and exterior edge deletions are independent, so every pair `(F',delta)` is realized by a spanning edge subgraph of `G`. Apply the fixed-subgraph theorem to each one. `□`

If `n=|V(G)|` and `b=|B|`, each finite route length lies in `{2,...,n-1}`. Hence at most `(n-1)^(b choose 2)` distinct arrays are possible. For three ports this is cubic in `n`, regardless of the exterior network's topology. This is a finite certification route, **not** a polynomial algorithm claim: finding the realized arrays and checking all internal edge subgraphs can still be hard. It is also narrower than the unrestricted half-separator question: a guard proof must first identify a heavy residual fragment and an anchored cover for it.

**Three-port weighted guard corollary.** Let a finite simple planar `G` have a set `S` of at most four vertices. Suppose every component `C` of `G-S` has order at most five, or has at most three boundary ports and passes the preceding all-spanning model test with `k=2`. Then every spanning edge subgraph `H` of `G`, under every nonnegative real vertex weighting, has a half-balanced separator that is a union of at most two ambient `H`-geodesics. Indeed, cover `S` in the unique heavy component by two geodesics. If a heavy residual remains, it lies in one `C`. At order at most four, pair its vertices; at order five, a connected induced nonclique has a three-vertex geodesic plus a path covering the other two vertices. For a larger `C`, use its anchored two-cover from the finite criterion. Replacing the first paths by paths covering the entire heavy residual leaves less than half the total mass outside it, exactly as in the [reviewed four-guard proof](../planar_two_geodesic_four_guard_review1/REVIEW.md). This is a conditional class theorem: the model test must still be established for each chosen large fragment.

## Reproduction and trust boundary

Run from the repository root with Python 3.11+ and only the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_multiport_closure/verify.py
```

The independent checker builds a three-port fragment and a cross-linked exterior network, exhausts all 2,048 spanning edge subgraphs, constructs the fresh-path model from each restricted route-length array, and compares all C-endpoint distances and **every** C-trace of every geodesic. It also confirms that some realized arrays fail the triangle inequality and counts the distinct arrays. The all-order theorem is the written replacement argument; the finite computation tests one nontrivial host only.

Expected output:

```text
states=2048 distinct_arrays=18 nonmetric_arrays=1 geodesic_traces=32462 cover_checks=12288 PASS
```
