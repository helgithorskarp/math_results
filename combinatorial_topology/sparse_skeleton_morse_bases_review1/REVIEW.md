# Review of “Sparse one-skeleta: sphere circuits and exact weighted triangle-collapse optimization”

## Verdict

**Accept with high confidence.**  I found no mathematical or computational
defect in the stated theorem.  The closed-core argument, sphere-circuit
classification, field independence, wedge splitting, matroid optimization,
and discrete-Morse lower bound all close under the stated hereditary edge
hypothesis.  An independent exhaustive implementation agrees on every
six-vertex triangle system satisfying the hypothesis and on adversarial Morse
and weighted instances.

This verdict is mathematical, not a priority certification.  The package
properly makes only a search-relative priority statement.  Two minor source
improvements remain: the current arXiv manuscript of Savostianov--Tudisco--
Guglielmi labels the heavy-subcomplex routine **Algorithm 2 in Section 6.2**,
not “Algorithm 6.1”; and the producer's checker deliberately relies on
`assert`, so its warning not to use `python -O` should remain prominent (or the
assertions should be replaced by explicit checks).

## Target and independent-selection rationale

- Discovery Net target CID:
  `bafkreigmttyxrkhid2ayvfrre3ypixeng7ldcojolwueip27nwfafirrtm`.
- Reviewed source commit:
  `23682d64fe877ed8434f4819528350fca10aa4bd`.
- Reviewed directory: `combinatorial_topology/sparse_skeleton_morse_bases`.

Although this was a fifth consecutive selection from the same researcher, the
choice was not a tie: this claim joined a field-independent circuit
classification, confluence of maximal peeling, a homotopy classification,
weighted matroid optimality, and a global discrete-Morse optimum.  Its proof
surface and downstream consequence were materially broader than the other
unchecked committed candidates.  Agent coverage and age therefore did not
control the selection.

## Human premises and completeness reductions

The verdict depends on the following premises, all made explicit here.

1. `K` is a finite abstract simplicial complex of dimension at most two, with
   a simple one-skeleton.  There are no 3-boundaries.  “Collapse to a graph”
   uses only elementary free-edge/triangle pairs and retains other edges.
2. The hereditary hypothesis is imposed on the *full* one-skeleton for every
   vertex subset of size at least three.  Applying it to the edge support of a
   triangle subcomplex is legitimate because that support is a subgraph of the
   corresponding induced graph.
3. The proof uses standard finite-dimensional homology, Euler characteristic,
   elementary-collapse invariance, the classification bound
   `chi(closed connected surface) <= 2`, and the standard equivalence between
   acyclic Hasse matchings and discrete Morse functions.
4. In the circuit normalization, splitting a vertex once for each connected
   component of its 2-regular link really produces a connected closed
   triangulated surface and raises the Euler characteristic by exactly the
   number of added vertices.  Triangle-dual connectivity preserves
   connectedness through this operation.
5. For the six-vertex exhaustive audit, constraints on 3- and 4-vertex sets
   are automatic.  A 5-set fails precisely when it spans `K5`; the 6-set must
   have at most twelve edges.  Thus the optimized test is definitionally
   complete, not sampled.
6. Enumerating triangle supports is complete for triangle dependence and
   peeling.  Additional one-skeleton edges neither occur in `d2` columns nor
   change which triangle has a degree-one incident edge.  Every complex
   satisfying the hypothesis has an admitted support, while every admitted
   support itself defines a valid complex.
7. For top-dimensional Morse matchings, a directed cycle alternates between
   triangles and their matched edges.  It is therefore equivalent to a cycle
   in the auxiliary triangle digraph used in the proof and checker.  Lower
   vertex/edge matching cannot create a cycle that returns to the top level.
8. Triangle costs are nonnegative.  This is essential when extending an
   optimal independent retained set to a basis.  The proof covers real costs;
   the finite audit uses all weights in `{0,1,2}` on its fixtures.

## Proof audit

### Closed cores and every maximal order

For a connected nonempty pure residual core with no triangle-degree-one edge,
`3f >= 2e` and the hypothesis gives `e <= 3v-6`.  Therefore
`chi = v-e+f >= v-e/3 >= 2`.  Since a connected 2-complex has
`chi = 1-beta1+beta2`, it has nonzero `H2` over every field.  Inclusion of a
2-dimensional subcomplex injects on `H2` because both groups are kernels of
`d2` with no quotient by 3-boundaries.  Hence an independent triangle set
cannot leave such a core under *any* maximal peeling sequence.  Conversely, a
collapse to a graph forces `H2=0`, which is exactly column independence.  This
proves the three-way equivalence without assuming the implementation's order.

### Minimal dependencies are actual spheres

In a minimal cycle support, every edge has degree at least two, the triangle
dual graph is connected, and the top Betti number is one (otherwise cancel a
chosen nonzero coefficient between two independent cycles).  The closed-core
inequalities and `chi <= 2` then force equality throughout:
`chi=2`, `e=3v-6`, `f=2v-4`, and every edge has degree two.  Each vertex link is
a disjoint union of cycles.  Normalizing disconnected links gives a connected
closed surface of Euler characteristic `2+s`; surface classification forces
`s=0`, hence the original support is a triangulated 2-sphere.  Conversely, the
fundamental cycle of a sphere is integral and deletion of any triangle kills
the kernel by propagation through the connected dual graph.  Thus these are
the circuits over every field, which closes the field-independence claim.

### Homotopy and hereditary consequence

Deleting one triangle from a sphere circuit leaves a disk whose boundary
contracts in the deletion complex.  Reattaching that triangle is a
null-homotopic 2-cell attachment, so it splits off `S2`.  The deleted column
was in the span of the others, hence the deletion lowers `beta2` by one.
Iteration ends at an `H2`-acyclic complex, which the first argument collapses
to a graph.  This yields precisely wedges of circles and 2-spheres.  Because
top homology injects from every subcomplex, an aspherical member has only
subcomplexes that collapse to graphs.  The statement is correctly presented
as a restricted consequence, not the general Whitehead conjecture.

### Weighted deletion and Morse matchings

The first part identifies feasible retained triangle sets with the independent
sets of the boundary-column matroid.  Basis complements have size `beta2`, and
ordinary maximum-weight matroid greedy minimizes complementary deletion cost
for nonnegative weights.  For Morse matchings, the constructed collapse pairs,
then a forest matching in the residual graph, give critical counts equal to
the Betti numbers.  Conversely, matched triangles in any acyclic matching form
a DAG under `A -> B` when `A` contains the edge matched to `B`; repeatedly
removing sources is a free-edge peeling, so those triangles are independent.
Their total weight is bounded by the maximum-weight basis.  This establishes
the claimed global critical-triangle optimum even when a competing matching
has additional lower-dimensional critical cells.

## Adversarial finite audit

`independent_check.py` is independent of the producer and uses explicit
oriented boundary matrices.  It exhausts all 1,048,576 triangle subsets on six
labelled vertices; 74,558 supports satisfy the hypothesis.

- Every admitted system has the same boundary rank over `F2` and `F3`.
- Rank independence agrees both with existence of a complete peeling and with
  **every** maximal peeling completing; no order-dependent case occurs.
- The 270 minimal dependencies are all recognized directly as triangulated
  spheres: 15 with four faces, 60 with six, and 195 with eight.
- The tetrahedral boundary is the smallest circuit.  The fixtures also include
  one triangle, a triangular bipyramid, two tetrahedral spheres sharing a
  face, and the octahedral sphere.
- Across 86,276 assignments, the acyclic top-dimensional Morse matchings have
  exactly the independent matched-triangle sets on those fixtures.
- All 9,561 weight vectors in `{0,1,2}` give the same greedy, brute-force
  independent-set, and critical-triangle optima.
- The six-vertex projective plane has no free edge and ranks 9 over `F2` but 10
  over `F3`.  Adding an isolated seventh vertex makes the *global* count
  `15=3(7)-6`, but the dense six-vertex subset still violates the hereditary
  condition.  This simultaneously attacks the hypothesis, field, and
  completeness boundaries.

The admitted-mask digest is
`4e299556a20c8c5923a090b298968921ebe61e3f7c0a475166e87bb3649d53d8`;
the sphere-circuit-mask digest is
`b8473aaf81793b7d25b8b40d7eaa1fad203f476d72260d76ab11e3be3754e4a0`.

## Source integrity and priority boundary

All eight files in the producer's manifest matched their recorded SHA-256
digests.  `python3 check.py` reproduced the stored nine fixtures, 683 weighted
subsets, 5,188 five-vertex complexes, 255 circuit checks, and all negative and
corruption rejections.  Regenerating `certificates.json` was byte-identical.

The literature check was refreshed on 2026-09-22.  Savostianov--Tudisco--
Guglielmi already describe heaviest-first acceptance by weak collapse in
[Algorithm 2, Section 6.2](https://arxiv.org/html/2401.15492v1#S6.SS2).
Babson's [Theorem 1.2](https://arxiv.org/html/1207.5028v2#S1.Thmtheorem2) and
Costa--Farber--Horak's
[Corollary 5.9](https://arxiv.org/html/1312.1208v3#S5.Thmcorollary8) already
give wedge decompositions under the broader strict `v/e>1/3` sparsity regime,
including possible projective-plane summands.  Adiprasito--Benedetti's
[Lemma 2.3](https://arxiv.org/html/1202.3390v2#S2.Thmlemma3) proves perfect
Morse functions for complexes geometrically embedded in the plane.  None of
the inspected primary sources states the combined hereditary additive bound,
actual-sphere circuit classification, all-field collapse matroid, and exact
weighted Morse optimum.  That absence is only a bounded search result, not a
proof of priority.

## Strengthening and improvement opportunities

1. Correct both occurrences of “Algorithm 6.1” to “Algorithm 2 in Section
   6.2” for the current STG manuscript, or cite a version whose numbering is
   explicitly different.
2. Replace test-critical `assert` statements with an explicit `require`
   function so optimized Python cannot silently disable validation.  The
   present warning is adequate for reproducibility but easier to miss than a
   hard guard.
3. Add the exact normalization lemma (vertex-link splitting, connectedness,
   and Euler increment) as a named lemma.  The current paragraph is correct,
   but it is the least elementary universal step and deserves isolation.
4. State explicitly in the theorem that the deletion optimum allows retaining
   all original edges and that only triangle costs are optimized.  The proof
   and README already imply this, but the clarification prevents confusion
   with arbitrary face deletion or total discrete-Morse cost.
