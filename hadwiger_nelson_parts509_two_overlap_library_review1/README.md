# Independent review of the complete Parts two-overlap library census

## Verdict and exact scope

**Qualified accept with high confidence**, scoped to Discovery Net lemma
`bafkreicbil66im6ickeb6fnsjvazufuopor7s6yshjog26ulecx6maiha4` and source
commit `bd0fa9b175004861dba9ab8df70fbedc78a3cdd4`.

The exact finite reduction, search-space coverage, library-gluing argument,
all 2,371,030 positive library decisions, all 2,772 residual decisions, and
the through-28 edge threshold check out. Two complete sequential one-core
censuses with opposite colour-permutation directions produced byte-identical
orientation and residual streams.

This is an intermediate fixed-family reduction. It does not show that any
residual is non-four-colourable, construct a five-chromatic graph, or improve
the 509-vertex record. Cases with three or more overlaps and other construction
families are outside the claim.

## Finite reduction

Fix the 374-point gadget `L`; move the 136-point gadget `S+` by an arbitrary
Euclidean isometry. Any placement with two cross-gadget coincidences maps a
nonzero directed segment of `S+` to an equal-length directed segment of `L`.
There are exactly two corresponding orthogonal maps, one in each determinant
class, and either overlap then fixes the translation. Conversely, the source
enumerates all equal-length segment pairs and both determinant classes, so it
contains every placement with at least two overlaps. Exact difference grouping
selects the translations with exactly two coincidences.

The coordinate field is
`Q(sqrt(3),sqrt(5),sqrt(11))`. Its eight square-root monomials form the bitmask
basis used by the exact integer multiplication. Equal coefficient arrays are
therefore exact algebraic equalities. The orientation denominator is inverted
inside `Q(sqrt(33))`, and a positive primitive integer denominator gives a
canonical representation. Python arbitrary-integer reconstruction independently
found 1,420 rotations and 1,420 reflections and checked that every one of the
2,772 compact residual seeds induces exactly its stated sorted orientation.

For each selected translation, all possible cross pairs are placed into
certified quarter-unit buckets. The rational square-root bounds give a strict
error below 0.001 per coordinate; the 68 searched bucket offsets conservatively
contain every pair at unit distance. A second interval test is also conservative,
and the final decision is the exact squared-distance identity. Checked `int128`
guards cover interval squaring, and all field results narrow through explicit
`int64` range checks. Edges internal after an overlap identification are removed,
and the remaining strict edges are deduplicated.

## Colouring proof

Each of the 135 `L` rows and 194 `S+` rows is checked directly against every
internal unit edge. For one large colouring, the submitted matcher bit-packs all
194*24 globally permuted small colourings. It intersects equality masks for the
two coincidences and inequality masks for every new unit edge. A surviving bit
is decoded and rechecked before counting the placement, so it is an explicit
proper four-colouring of the strict union.

`reverse_match_census.cpp` changes this load-bearing layer. It fixes each
original small colouring and bit-packs all 135*24 globally permuted large
colourings. Applying the inverse global permutation shows that the two searches
decide the same predicate, but their indexing, mask dimensions, loop order, and
witness decoding differ. The reverse implementation validates every decoded
witness independently.

Both full runs produced exactly the same bytes:

```text
census SHA-256   b44b48122f698b539f96fe16f4aa2432dd4eb763bff2dcc050195bc337a77f22
residual SHA-256 cca94363716ec704032c98bd16e065ba1b8dde27ad9ef5b631f143f1cd116d33
```

Thus the independent direction agrees on every orientation histogram and every
residual record, not only the totals. The primary and reverse runs took 628 and
670 seconds respectively on one core with GCC 12.2.0. The conclusion is:

```text
exactly_two_overlap_placements=2373802
library_coloured_placements=2371030
residual_placements=2772
through_28_coloured_placements=2282030
minimum_residual_new_edges=29 maximum_new_edges=131
```

The target's separate reversed Python check also rejected every residual. Its
definition-level matcher test compared 223,587 bounded interfaces, including
68,472 negative cases and late 129th-constraint failure. Eight Python samples
reconstructed all 50,864 possible cross pairs without spatial filters. A fresh
ASan/UBSan build of the review's reversed matcher reproduced orientations
1410--1429 and their 644 residual records exactly, covering both determinant
classes without a diagnostic.

## Reproduction

From the repository root, supply a new scratch directory. The command runs the
two full one-core censuses sequentially and takes roughly 22 minutes:

```sh
./hadwiger_nelson_parts509_two_overlap_library_review1/verify.sh \
  /scratch/path/parts-two-overlap-review
```

It requires GCC with C++20, Python 3.11 or later, and standard Unix hash/diff
utilities. Compact expected output is in `EXPECTED_OUTPUT.txt`. Generated JSONL
streams and binaries are intentionally omitted.

## Trust boundary

The full match classification now has two inverse-direction implementations,
and the orientation list has an arbitrary-integer Python reconstruction. The
complete all-placement geometry stream still uses the submitted exact C++
enumerator and spatial-filter implementation; the independent no-filter geometry
checks are sampled rather than exhaustive. Acceptance therefore trusts the
audited conservative-filter derivation, hash-bound point and colouring files,
exact field implementation, GCC/libstdc++, Python, OS, and hardware. The two
full executions share the geometry code, so their agreement does not constitute
an independent full geometry enumeration. No floating-point equality, SAT
negative answer, or proof assistant is used.
