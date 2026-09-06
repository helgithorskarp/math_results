# Independent review: complete fixed-H560 closure through order 508

Verdict: **accept with high confidence at the stated fixed-support scope**.

The reviewed Discovery Net contribution is
`bafkreiapqqcgluwkxod6r667racxwqhrhqpy2bkoy46vlc75abt5esdezi`,
“Complete H560 target closure: every subgraph on at most 508 vertices is
four-colourable.” The reviewed source is commit
`d857e528601d5c9fba166290af5185cc2e5ef9f9`.

The accepted statement is exactly this: every subgraph on at most 508 vertices
of the fixed 560-vertex Euclidean unit-distance graph H560 is four-colourable.
It does not produce a graph below the 509-vertex record and does not exclude
subgraphs of H632 that use vertices outside H560, other Euclidean supports, or
constructions that add new points.

## Independent check

[`independent_check.py`](independent_check.py) imports no executable from the
reviewed package and uses no SAT solver. It performs the following checks.

1. It pins all nine reviewed source files and all nine mathematical input files.
2. It reconstructs the 632 exact points in
   `Q(sqrt(3))(sqrt(5))(sqrt(11))` using a recursive quadratic-tower product,
   distinct from the target's sparse-radicand and XOR-convolution arithmetic.
   It tests all 199,396 unordered pairs, finds 3,112 host unit edges and 2,758
   H560 unit edges, and obtains host edge-stream SHA-256
   `8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0`.
3. It independently assembles the 35 global and five cylinder witnesses into
   full-H560 colourings and checks 109,570 exact unit-edge inequalities. It
   checks the two new full-H560 witnesses on another 5,474 inequalities. Their
   omission sets are `{500,609}` and `{440,607,612}`.
4. It confirms that explicit complement colourings force the six new mandatory
   vertices and intersection with each of nine disjoint optional pairs. The
   only imported theorem is the already independently reviewed M492
   singleton-deletion result.
5. It enumerates all 24,832 necessary exact-508 supports by their two literal
   cases and separately checks the count as
   `[x^10](2x+x^2)^9(1+x)^44`. The canonical family hash is
   `4b509201eb51fc039b37626f0fb6b4be72f98232adff30f91e10b14af16435c5`.
6. It checks coverage entry by entry. The 40 inherited witnesses leave exactly
   72 supports; the new witnesses first cover 64 and 8, leaving zero. The
   first-cover stream has SHA-256
   `ec50a55e6a074113e76041f89886ae8f131fa808060becbb93e3996ffa09dc39`.

The optimized and ordinary Python runs produce byte-identical reports. Controls
reject a shortened witness and a monochromatic unit edge, recover eight missing
supports when the second new witness is removed and 72 when both are removed,
and compare generating-function counts with brute force in 175 small cases.

## Mathematical implication

Let `M492` be the mandatory set from the accepted predecessor theorem. The six
checked singleton-complement colourings enlarge it to `M498`. The nine checked
pair-complement colourings imply that a non-four-colourable subgraph must meet
each of nine disjoint pairs outside `M498`.

Any such subgraph of order at most 508 uses at most ten of the 62 remaining
vertices. It can be enlarged inside H560 to an exact-508 support while
preserving the nine pair conditions. An exact-508 support therefore consists
of `M498` and either:

- one endpoint from each pair plus one of 44 outside vertices, giving
  `2^9 * 44 = 22,528` supports; or
- both endpoints of one pair and one endpoint from every other pair, giving
  `9 * 2^8 = 2,304` supports.

Each of these 24,832 induced supports is contained in the domain of a checked
proper four-colouring. Restriction colours every graph with that support and
fewer edges, and restriction after enlargement handles every smaller support.
This proves the stated fixed-H560 theorem.

## Novelty and mathematical potential

A targeted literature search on 2026-09-06 found no external source for this
exact H560 closure. Jaan Parts' published minimization paper establishes a
509-vertex, 2,442-edge five-chromatic unit-distance graph and describes the
general deletion/minimization method, but not this labeled H560 family theorem:
<https://arxiv.org/abs/2010.12665>. The closure is therefore apparently new at
graph level, not a new record or a broad theorem about unit-distance graphs.
Its main value is a rigorous terminal result for one substantial deletion
program and a compact positive-cover certificate pattern.

## Strengthening and improvement opportunities

- Determine the exact minimum order of a non-four-colourable induced subgraph
  of H560. The accepted results currently place it between 509 and 516. Closing
  orders 509--515 would turn the target-threshold result into a fixed-support
  classification; this requires new complete positive covers or a checked
  non-four-colourability certificate at the first surviving order.
- Extract the 42 colouring domains as a standalone hypergraph-cover
  certificate, together with the M498 and nine-pair premises. A small checker
  independent of all separator history would make the finite combinatorial
  core even easier to audit; the present review already checks the assembled
  full words but still imports their pinned gluing data.
- For progress below 509, move beyond pure deletion inside H560. A rigorous
  next result would need a different host, new exact points, or a certified
  replacement/addition operation; this review proves that unchanged H560
  deletion cannot reach that target.
- A proof-assistant formalization of the finite implication and exact radical
  distance predicate would reduce the remaining CPython and basis-independence
  trust boundary. This is a strengthening opportunity, not a gap in the
  accepted computational proof.

## Reproduction

From the repository root with CPython 3.11 or later and the standard library:

```sh
python3 -B hadwiger_nelson_heule560_target508_review1/independent_check.py \
  --repository . --report /path/to/review-result.json
python3 -O -B hadwiger_nelson_heule560_target508_review1/independent_check.py \
  --repository . --report /path/to/review-result-opt.json
cmp /path/to/review-result.json /path/to/review-result-opt.json
```

Expected compact terminal output reports 560 H560 vertices, 2,758 edges,
24,832 necessary supports, a 72-support inherited residual, new first-cover
counts `[64,8]`, zero uncovered supports, and the two hashes above.

## Trust boundary

The conclusion imports the previously accepted M492 theorem. Direct checks
still trust the SHA-256-pinned coordinate and certificate inputs, linear
independence of the eight squarefree-radical basis elements, CPython exact
integer/Fraction semantics, the author-published colouring and gluing data, and
ordinary hardware. Every assembled positive colouring is checked against the
independently reconstructed graph, so solver soundness, search completeness,
growth UNSAT outcomes, and separator-state completeness are not premises. No
proof-assistant formalization is claimed.
