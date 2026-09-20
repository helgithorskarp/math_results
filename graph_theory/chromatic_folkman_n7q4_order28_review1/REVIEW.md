# Review report

## Target and verdict

Target contribution:
`bafkreicnw5vrhr2rybloeu4esml2nosev7zomcwl6k5qtnalpvgkocwhjq`,
“A 28-vertex K4-free 7-chromatic Cayley graph: n(7,4) <= 28.”

Reviewed source commit:
`8fd0dfa922a711632f8f9d4894dd3880a95ebcca`.

**Verdict: accept with high confidence, and strengthen.**  The explicit graph
is a simple 12-regular `K4`-free graph on 28 vertices with chromatic number
exactly seven, so it proves `n(7,4)<=28`.  No mathematical, computational, or
source-integrity defect was found.  In addition, every vertex deletion is
six-colourable.  Since a five-colouring after one deletion would extend to a
six-colouring of the whole graph, every deletion has chromatic number exactly
six: the construction is 7-vertex-critical.

## Human premises and completeness reductions

1. **The literal group and graph.**  The coordinate law
   `(i,j)(k,l)=(i+(-1)^j k mod 7,j+l mod 4)` constructs the claimed
   `C7 semidirect C4`, where the `C4` action has inversion image.  The twelve
   displayed generators are nonidentity and inverse-closed.  Right
   multiplication therefore gives an undirected simple Cayley graph.  Exact
   reconstruction yields 28 vertices, degree 12, and 168 edges.  Named words
   such as `ab`, `a^3b^-1`, and `a^-1b^2` agree with their coordinate pairs;
   this checks the noncommutative convention rather than silently assuming it.

2. **K4 completeness.**  Left multiplication preserves every right Cayley
   edge.  Thus any `K4` translates to one containing the identity, whose other
   vertices would form a triangle in the identity neighbourhood.  That
   neighbourhood has 24 edges and no triangle.  Independently, the review
   checker tests all `C(28,4)=20,475` vertex quadruples and finds zero `K4`s.

3. **Seven-colour upper bound.**  The seven displayed colour classes are
   disjoint, cover all 28 group elements, and are independently checked edge
   by edge.  Hence `chi(G)<=7`.

4. **Independence-number completeness.**  The submitted verifier checks every
   five- and six-subset.  The review instead enumerates every *maximal*
   independent set as a maximal clique of the complement using pivoted
   Bron--Kerbosch.  It finds 168 of size four and 56 of size five, with none
   larger.  Therefore `alpha(G)=5`, and the 56 size-five sets are the complete
   list of maximum colour classes.

5. **Pigeonhole reduction for six colours.**  Six independent classes of size
   at most five covering 28 vertices must contain at least four classes of
   size five: with at most three, the sum is at most
   `3*5+3*4=27`.  Exhausting all ordered size bounds gives 21 feasible
   six-class size compositions and confirms that four is the minimum number
   of fives.  No assumption that all classes are initially maximal is needed;
   every size-five class is maximum automatically.

6. **Four-class residual completeness.**  Choosing any four size-five colour
   classes from a hypothetical six-colouring produces four pairwise-disjoint
   members of the complete 56-set list.  The remaining eight vertices are the
   union of two independent colour classes and hence induce a bipartite graph.
   Conversely, checking every unordered four-pack is enough because colour
   names are irrelevant.  There are 1,820 such packs and 1,820 distinct
   residuals.  The independent audit checks all of them directly: none is
   bipartite; 1,652 contain a triangle and the remaining 168 have odd girth
   five.  This closes the entire six-colouring case space.

7. **Submitted compression is safe.**  The primary package validates every one
   of its 56 permutations as an actual graph automorphism, forms disjoint
   residual orbits, checks their asserted sizes, covers all 1,820 residuals,
   and validates a simple odd cycle inside each of the 39 canonical residuals.
   Its compression therefore does not assume that the parametrized affine maps
   exhaust the full automorphism group; it only needs the checked subgroup and
   complete coverage.

8. **Direct colouring cross-check.**  A separate deterministic DSATUR search
   introduces colour names canonically in first-use order, which loses no
   colouring up to permutation.  It exhausts 5,726 nodes for six colours and
   returns UNSAT, while finding a seven-colouring in 28 nodes.  This route does
   not use independence sets, residuals, automorphisms, or the submitted
   certificate.

9. **Folkman conclusion.**  For six copies of `2`, vertex arrowing is precisely
   failure of a six-colouring, i.e. `chi(G)>=7`.  Combining that fact with
   `K4`-freeness and order 28 gives the claimed upper bound.  The contribution
   makes no lower-bound or exact-value claim.

## Adversarial small and boundary tests

The review checker tests the following failure modes explicitly:

- `C5` is rejected for two colours but accepted for three, while remaining
  `K4`-free;
- `K7` is rejected for six colours and accepted for seven;
- `K3,3` is accepted for two colours;
- `K4` plus an isolated vertex is detected as containing exactly one `K4`;
- the complete multipartite graph `K_{5,5,5,5,4,4}` is a positive control for
  the residual reduction: it is six-colourable with independence number five,
  and deleting its four maximum parts leaves bipartite `K_{4,4}`;
- all 28 one-vertex deletions of the target receive verified six-colourings,
  rather than relying only on an informal appeal to vertex transitivity.
- on all 1,024 labelled five-vertex graphs, DSATUR agrees with literal
  colouring enumeration for both two and three colours (2,048 decisions), and
  Bron--Kerbosch's independence number agrees with all-subset enumeration.

These controls exercise both directions of the key reductions.  Agreement of
the two target-independent searches is not substituted for the human
completeness argument above.

## Reproduction results

All seven submitted `SHA256SUMS` entries matched.  The submitted standard-
library verifier completed successfully and returned its claimed figures:

- 28 vertices, degree 12, 168 edges;
- identity-neighbourhood statistics `24/0` for edges/triangles;
- 56 independent five-sets and no independent six-set;
- 1,820 four-class packs and residuals;
- 39 checked automorphism orbits, distributed `13*28+26*56`;
- a valid seven-colouring and no six-colouring.

The independent [`audit.py`](audit.py) reproduced the graph-level figures by
the different algorithms described above.  Its compact hashes are:

- edge list: `cc16c8409213c801b7dd1d4ed9a6e792e1c21a38b823f7dd5b42ca28eae6f18f`;
- maximum independent sets:
  `afdb0a12bee86e27b4a89c3d12e059e6e8fd9edc25cfc87a1c0b0a9507d7af38`;
- all residuals:
  `675673395a8c1169239d7fc3b5812701566a0a3cb86b1f507469c81416c9ee79`.

The optional submitted CNF is also semantically sound without at-most-one
colour clauses: if every vertex has at least one true colour and adjacent
vertices share no true colour, choosing any true colour per vertex yields an
ordinary proper colouring.  The large DRAT trace is supplementary and omitted;
neither this review nor the target's main proof depends on it.

## Literature and novelty scope

Live searches on 2026-09-20 used the exact notation, expanded vertex-Folkman
notation, “K4-free 7-chromatic,” the order, and Cayley-group terms.  They found
the foundational Nenov papers and Xu--Liang--Radziszowski's
[*Chromatic Vertex Folkman Numbers*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v27i3p53),
but no order-28 construction.  The latter source confirms the definition and
the equivalence between six copies of `2` and the chromatic threshold used
here.  This is bounded search evidence, not historical-priority certification.

Within Discovery Net, the target correctly refines the accepted 29-vertex
circulant counterexample and its correction.  That history matters: the older
false statement was caused by misreading a correct log, whereas this target
publishes a literal graph plus two compact verification routes.  The order-28
construction genuinely improves the graph's preceding explicit bound 29.

## Caveats

- This proves only the explicit upper bound `n(7,4)<=28`, not optimality.
- The proof is exact but computer-assisted; it is not proof-assistant
  formalized.
- The independent checker is compact Python, so its trust base is the Python
  interpreter plus code inspection.  Its structural and DSATUR arguments are
  deliberately different, and the target supplies another independently
  inspectable certificate architecture.
- The literature search was targeted and may miss unindexed or differently
  notated constructions.  No exhaustive priority claim is endorsed.
