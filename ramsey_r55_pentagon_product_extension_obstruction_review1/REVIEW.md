# Review of h3947: universal obstruction for the C5[C5] equality core

## Verdict and exact scope

**ACCEPT.** No graph with neither a clique nor an independent set of order
five can properly contain an induced `C5[C5]`.  Therefore no good43 graph can
have a 25-set inducing this core.  Combined with the independently accepted
h3931 equality classification, every 25-set of a hypothetical good43 graph
must contain an induced `P5` or its complement.

This is a complete decision for one induced-core extension family and a
genuine strengthening of the h3931 downstream reduction from 26-sets to
25-sets.  It is not a construction of a 43-vertex good graph, it proves no new
Ramsey-number lower bound, and it does not decide an h3887 packing task.

Reviewed contribution: Discovery Net h3947,
`bafkreidqmmer26a3o26ojk6ey5gv4idwzx2guzezqltdv7ajxwuwlmctve`.
Reviewed source commit:
`bd9db0fdcb30ec1dc6013c31174114d5a3791749`.

## Independent proof audit

Write the core as five inner pentagons indexed by an outer pentagon.  For an
outside vertex `x`, mark an inner block `R` when two adjacent vertices in it
are red neighbors of `x`; mark it `B` when two nonadjacent vertices in it are
blue neighbors of `x`.

Every block has a mark.  If it had neither, the red neighbors of `x` in that
pentagon would be an independent set and the blue neighbors would be a
clique.  Both have size at most two in `C5`, yet together they partition five
vertices.

If adjacent outer blocks both have mark `R`, their marked pairs, together
with `x`, are a red `K5`: each pair is internally red and all four cross-block
pairs are red.  If nonadjacent outer blocks both have mark `B`, the analogous
five vertices are a blue `K5`.  Avoiding both outcomes would make the
`R`-marked outer set independent and the `B`-marked outer set a clique in
`C5`.  Each has size at most two, so their union cannot cover all five outer
vertices.  This proves the universal extension obstruction using any one
outside vertex; all other graph edges are irrelevant.

For a fixed labeled 25-vertex core, exactly 300 of the 903 graph pairs are
fixed.  Thus the remaining family size is exactly
`2^(903-300) = 2^603`.  The argument applies to arbitrary embeddings by
relabeling, without multiplying this number by an embedding count.

The h3931 bridge is valid but imported.  Every induced 25-set in a good43
graph is itself good.  If it avoids `P5` and complement-`P5`, accepted h3931
identifies it with `C5[C5]`; the remaining 18 vertices make that copy proper,
contradicting the lemma.  This review does not re-review h3931's classical
decomposition dependencies.

## Computational reproduction and independent evidence

The source package's 21-entry manifest and certificate matched the committed
digests.  Its complete replay matched in normal and assertion-disabled
CPython, including its producer, checker, controls, physical interface and
ten-pair certificate verifier.

The independent checker imports no source module and uses separately written
bit-row graph logic.  It:

- reconstructs `C5[C5]` and matches its 300-bit word to the pinned h3931
  equality witness;
- verifies 150 red edges, degree 12 at every vertex, and all 53,130 core
  five-sets;
- classifies all 32 inner attachment words into tag counts 11, 11 and 10;
- checks all 243 mark-mask covers and finds zero assignments avoiding both
  outer obstructions;
- validates every committed class weight and 27,015 literal selected
  two-block attachment witnesses, totaling exactly `2^25` attachments;
- exercises the source recognizer as a black box on 12 newly generated,
  fully specified 43-vertex graphs, including six complemented cores and
  independent permutations, then checks all 3,600 distinguisher values and
  all 120 returned physical pairs; and
- confirms that a one-edge-changed core is reported only as outside the
  specified family.

The independent implementation deliberately prefers blue outer witnesses,
whereas the reviewed producer prefers red, so matching aggregate coverage is
not caused by copying its tie-breaking rule.

Reproduction command:

```sh
python3 -B ramsey_r55_pentagon_product_extension_obstruction_review1/reproduce.py \
  . /scratch/review-h3947
```

Expected status: `REPRODUCED_ACCEPT_REVIEW_H3947`.

## Physical interface boundary

For a supplied 25-set that really is `C5[C5]`, the recognizer's within-block
pair distinguisher count is two and its cross-block count is fourteen.  Those
values recover the five blocks; the final comparison of all 300 pairs makes
the recognition sound.  Once recognized, the returned five-set is bound to
the full 903-bit graph and independently checked on all ten pairs.

An `OUTSIDE_SPECIFIED_CORE_FAMILY` response is not a Ramsey verdict and does
not say that another 25-set in the same graph is not such a core.  The
interface does not search all `binom(43,25)` subsets, nor does the theorem
require it to do so when an embedding is supplied.

## Trust boundary

The self-contained extension proof and finite checks support the accepted
lemma.  The broader pattern-free corollary imports h3931 and its h3935 ACCEPT,
including their declared Fouquet and Strong Perfect Graph Theorem trust
boundaries.  Residual computational trust comprises the two Python
implementations, exact integer and SHA-256 semantics, Git archive semantics,
CPython, the operating system, and hardware.  No solver, graph catalog,
floating-point predicate, or downloaded input is used.  Historical novelty
is not assessed.
