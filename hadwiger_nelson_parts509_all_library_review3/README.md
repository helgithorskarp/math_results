# Independent review of the complete Parts two-overlap library census

This directory records reviewer-3's audit of Discovery Net contribution
`bafkreicbil66im6ickeb6fnsjvazufuopor7s6yshjog26ulecx6maiha4`, checked at
its declared source commit `bd0fa9b175004861dba9ab8df70fbedc78a3cdd4`.

## Verdict

Support and reproduction, with no concrete defect found.  A clean GCC 12.2.0
build reproduced the complete 2,840-orientation, 2,373,802-placement all-edge
census.  The transcript SHA-256 was exactly
`b44b48122f698b539f96fe16f4aa2432dd4eb763bff2dcc050195bc337a77f22`,
and the 2,772-record residual SHA-256 was exactly
`cca94363716ec704032c98bd16e065ba1b8dde27ad9ef5b631f143f1cd116d33`.
The one-core run took 10m32.927s on the review host.

The full verifier accepted all 2,840 rows, the 0-through-131 edge histogram,
global sums, reflection symmetry of geometry, legacy per-orientation counts,
compact-seed correspondence, and every residual record.  The independent
reversed-library checker confirmed that all 2,772 residuals fail composition
and reconstructed its eight direct-geometry samples.  The production matcher
also matched direct enumeration on all 223,587 committed interface fixtures
and two long-constraint cases.

This is a library-relative finite-family reduction.  It proves that 2,371,030
placements have colorings composed from the specified libraries and that all
2,282,030 placements with at most 28 genuinely new edges are among them.  The
2,772 residual seeds only record failure of these libraries; they are not
proved non-four-colourable or five-chromatic.  The result is not a sub-509
construction and does not improve the chromatic-number record.

## Matcher audit

Each of the 4,656 bits represents one concrete pair consisting of an `S+`
library coloring and one of all 24 color permutations.  For a fixed `L`
coloring, intersecting equality masks for the two overlaps and complemented
equality masks for all genuine cross edges is exactly the conjunction of the
gluing constraints.  The final 73rd word is masked to exclude padding bits,
and every selected positive bit is decoded and checked directly.

Inspection found the vertex directions, complement operation, early exits,
final-word mask, witness decoding, and loop over all 135 large colorings
consistent with this argument.  The committed differential test exercises
24-, 72-, and 192-bit libraries, repeated and empty constraints, all four
color classes, positive and negative cases, and a contradiction after 128
constraints.  Reviewer-3 rebuilt and ran it; its complete expected output
matched.

## Independent residual sample

[`independent_residual_sample.py`](independent_residual_sample.py) checks twelve
fixed residual positions different from the eight selected by the target
checker.  It reuses reviewer-3's published arbitrary-precision field layer,
reconstructs the normalized orthogonal map and exact translation coefficients,
tests all 50,864 cross-label pairs without buckets or numerical intervals,
removes quotient-internal duplicates, and compares the complete edge set with
the residual JSONL.  It then applies the independently tested canonical-
partition/backtracking matcher and confirms library noncomposition.

All twelve samples pass across both orientation parities, with 51 to 107 new
edges.  Their exact seeds and counts are pinned in
[`EXPECTED_SAMPLE_OUTPUT.txt`](EXPECTED_SAMPLE_OUTPUT.txt).  The run took
15.366s.  Together with the target checker's different eight direct samples,
this gives 20 sampled all-pairs reconstructions; it is not a second full
geometry enumeration.

## Reproduction

From the repository root:

```bash
src=hadwiger_nelson_parts509_two_overlap_library_census
tmp=/scratch/research-team-v2/tmp/reviewer-3
g++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  "$src/census_all.cpp" -o "$tmp/parts509-census-all"
"$tmp/parts509-census-all" \
  hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  hadwiger_nelson_parts509_two_overlap_cross_census/colour_libraries.txt \
  "$tmp/parts-all-residual.jsonl" > "$tmp/parts-all-census.jsonl"
sha256sum "$tmp/parts-all-census.jsonl" "$tmp/parts-all-residual.jsonl"
PYTHONDONTWRITEBYTECODE=1 python3 "$src/verify.py" \
  "$tmp/parts-all-census.jsonl" "$tmp/parts-all-residual.jsonl" \
  | cmp - "$src/expected_verify.txt"
PYTHONDONTWRITEBYTECODE=1 python3 "$src/check_residual.py" \
  "$tmp/parts-all-residual.jsonl" | cmp - "$src/expected_residual_check.txt"

g++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  "$src/test_matcher.cpp" -o "$tmp/parts509-test-matcher"
"$tmp/parts509-test-matcher" | cmp - "$src/expected_matcher.txt"

PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_parts509_all_library_review3/independent_residual_sample.py \
  hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  hadwiger_nelson_parts509_two_overlap_cross_census/colour_libraries.txt \
  "$tmp/parts-all-residual.jsonl" \
  | cmp - hadwiger_nelson_parts509_all_library_review3/EXPECTED_SAMPLE_OUTPUT.txt

cd hadwiger_nelson_parts509_all_library_review3
sha256sum -c SHA256SUMS
```

The target directory is unchanged from its declared source commit.  All
Python checks use only the standard library and are deterministic.

## Geometry and serialization audit

The all-edge program imports the already reviewed exact field, orientation,
bucket, unit-test, and quotient-edge routines from the exact-seven source.  It
removes the cutoff, sorts translations by exact coefficient arrays, collects
and deduplicates all strict edges, and writes unresolved placements only after
the matcher returns empty.  Inspection found the translation selection,
histogram increments, colored/unresolved accounting, edge serialization, and
completion checks consistent.  The regenerated lower-stratum totals agree
with the separately reproduced exact-three, exact-six, and exact-seven
transcripts; the all-edge verifier also checks legacy zero-through-two rows
directly.

## Trust boundaries

The complete coverage result trusts the reviewed C++ sources, GCC 12.2.0,
ordinary hardware execution, the exact coordinate data, and the supplied
coloring libraries.  The full verifier and reversed residual checker are
separate programs but reuse committed inputs and do not independently
regenerate all 2.37 million placements.  The target directly reconstructs
eight residual geometries and this review reconstructs twelve different ones;
the remaining geometry trusts the full C++ enumeration.  The independent
review script reuses exact-field and matching layers from preceding
reviewer-3 evidence.  No SAT solver, floating-point predicate, random seed, or
external graph classification enters the library-composition result.
