# Verification and physical interface

`reproduce.py` checks every package file against the manifest, recomputes
all mathematical evidence, compares the result with the compact expected
output, regenerates the fixture and checks its ten actual certificate
pairs. Status fields alone are never accepted as evidence.

The audit covers:

- All 64 K4 colorings, 16 outside four-contact signatures, eight mixed-triple
  signatures and the complete degree/distinguisher equality boundary.
- 212 exact spanning-word entries, using both subspace inversion and a
  positive dynamic program over actual labels and concrete spans; all 18
  raw, overlap and remaining fields across the six target stages.
- Every binary matrix of sizes 2x3, 3x3, 3x4, 4x3 and 4x4: 74,304 matrices
  and 150 exact rank/cap/overlap counts, with literal dense elimination.
- Every full-rank factor pair for shapes 2x3 at rank two and 3x3 at rank
  three: 28,476 pairs; the respective 42 and 168 physical matrices each
  have exactly 6 and 168 factorizations.
- 40 deterministic, deliberately rejected physical graphs, eight for each
  first-failing predicate; 40 paired elementary factor-basis changes.
- Every one of the 443 internal coordinates and 460 cross contacts, with
  explicit physical pair mapping. Surviving fixtures cover blue ranks five
  and six; a separate affine input demonstrates excluded blue rank four.
- 10,240 literal small-graph clique comparisons and 95 negative controls,
  including malformed factors, incomplete encodings, fabricated extra
  fields, out-of-family extraction and corrupt physical certificates.

All checks pass with normal and assertion-disabled CPython. The deterministic
evidence contains no timings. Runtime and memory are operational measurements,
recorded in the private publication checkpoint rather than expected theorem
data. No optimization, parallelism, numerical rounding, external library or
solver is required. Every arithmetic count uses unbounded Python integers.

## Input and consumer

`model.py` accepts exactly three fields:

- `rows`: 20 integer labels in 0..31 spanning F2^5;
- `columns`: 23 labels with the same domain and spanning requirement;
- `internal_hex`: exactly 111 lowercase hex digits encoding a number below
  2^443. Bit order is increasing unordered vertex pair, restricted to pairs
  wholly inside A or wholly inside B.

Cross edges are the F2 dot products. The physical output has `n:43` and
`red_hex`: 226 lowercase hex digits encoding a number below 2^903, with
bits ordered by increasing unordered vertex pair. Every absent edge is blue.

Classification first identifies whether the blue rank is at least five,
then checks the declared predicates in the order recorded in the exact
staged count. `keep:true` means only that these necessary predicates hold;
it is not a Ramsey verdict. Internal edges never alter this classification.

`extract.py` admits only a rejected member of the defined baseline and
finds a literal monochromatic five using exhaustive bitset clique search.
Its success guarantee on every such input rests on the universal proof,
not on exhaustive testing of all 43-vertex graphs. `verify.py` imports no
model, count, extractor, Ramsey result or saved status; it builds a dense
adjacency matrix and checks the ten certificate edges directly.

The fixtures and expected audit are small interface controls. No physical
fixture is offered as a construction candidate. A limited collection of
tests is not an exhaustive proof of every possible Python execution.
