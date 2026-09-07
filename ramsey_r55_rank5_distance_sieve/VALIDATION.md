# Independent verification and reproducible interfaces

The full replay checks every package file against its manifest, regenerates
both mathematical counts and physical evidence, and compares them with the
compact expected result. Neither a stored status nor a metadata digest is
treated as a mathematical certificate.

Verification covers:

- All 32 marked row-word coefficients and four column counts by independent
  positive actual-label/span insertion versus subspace inversion; all 33
  raw, complementary-rank-four and retained cross-stratum fields.
- Both complete distance recurrences at every selected-pair count 0..10.
  At ten pairs the signed recurrence uses 1,024 states and the independent
  positive block recurrence 10,946. Ungrouped graph sums through six pairs
  and ungrouped actual-block sums through four pairs provide additional
  independent checks. The wrong single-pair independence product is rejected.
- All 33,866 labeled graphs of orders two through six, checking 32 exact
  distance probabilities against both recurrences.
- Every graph on six vertices under each of the 3+3 and 4+2 cuts: 65,536
  graph/cut cases and 30 exact entry comparisons. These jointly check the
  full bridge from actual cross rank and multiplicities to constrained
  physical internal assignments, with smaller distance thresholds. They
  are counting controls, not Ramsey statements at those smaller orders.
- Twenty physical 43-vertex rejections, two at each repeated-class count
  1..10, including tripled-class fixtures where possible; twenty paired
  factor-basis changes; retained controls at all counts 0..10; physical
  distance endpoints seven and eight; every one of the 443 internal bit
  coordinates; 10,240 literal small-graph clique comparisons; 72 negative
  controls for malformed inputs, old-family exclusions and corrupt
  monochromatic-five certificates.

All arithmetic uses unbounded Python integers or exact fractions. Both
normal and assertion-disabled CPython 3.11.2 runs regenerate the same
deterministic evidence. Performance measurements belong in the private
publication checkpoint, rather than the expected mathematical output.
No external packages, solver, parallel execution, floating-point count,
historical graph catalog or private proof artifact is required.

## Literal graph interface

Inputs have exactly `rows`, `columns` and `internal_hex`, with the same
semantics as the preceding public rank-five model. There are 20 row and
23 column integer labels in 0..31, each list spanning F2^5. The 111-digit
lowercase internal encoding is below 2^443, with bits ordered by increasing
unordered pair inside A or B. Cross edges are the F2 dot products.

The physical graph has `n:43` and 226-digit lowercase `red_hex` below 2^903,
with bits ordered by increasing unordered pair. Every omitted edge is blue.
Family classification first enforces the preceding cross sieve, then chooses
the two least vertices in each repeated row class. It tests all such pairs,
not merely the first four or a randomly selected subset. A repeated class
of size three contributes one pair, not all three pairs. The latter stronger
filter is outside the count proved here.

Every pair's distinguisher list is computed from physical adjacency, and
the opposite side contributes none because the selected rows are equal.
`keep:true` certifies only passage through these necessary filters. The
deterministic pair choice may change under vertex relabeling in a tripled
class; its fixed-label definition and equal per-matching count are explicit.
Factor-basis changes leave the physical choice unchanged.

The extractor accepts only a newly rejected member of the preceding family.
It finds an actual monochromatic five-set; the independent verifier checks
all ten literal edges, without importing the model or either count. The
test fixtures are expressly not candidate graphs. Universal validity comes
from the displayed pair bound and exact counting arguments, not from these
finite interface tests alone.
