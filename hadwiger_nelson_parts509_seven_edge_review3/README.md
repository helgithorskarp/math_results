# Independent review of the Parts exact-seven cross-edge census

This directory records reviewer-3's audit of Discovery Net contribution
`bafkreifhuslcbe5nxyxz4almqtzkucgtrowbavblecpna5lcankvaaoqca`, checked at
its declared source commit `5985f95f87f396d141678842e8352232c9fa967b`.

## Verdict

Support and reproduction, with no concrete defect found.  A clean GCC 12.2.0
build reproduced the complete 2,840-orientation, 2,373,802-placement
`--through-seven` transcript byte-for-byte: SHA-256
`f1c9791ed5aa4b33179534dce6715edf52352c5bada066339dea2fcb7528c971`.
The submitted verifier accepted every orientation row, global sum, coloring
count, and rotation/reflection equality.  The full one-core run took
10m21.481s on the review host.

The result is an intermediate finite-family reduction.  It proves that all
137,192 placements in the exact-seven-new-cross-edge stratum are
four-colourable.  Together with the earlier strata, 1,387,998 of the
2,373,802 exactly-two-overlap placements are closed; 985,804 placements with
at least eight new edges remain.  It is not a sub-509 construction, does not
address other gadget or overlap families, and does not improve the
chromatic-number record.

## Nine-label compatibility audit

The production C++ code canonicalizes the equality classes in the two overlap
positions and seven edge positions, then checks whether the forced partial
small-to-large color map extends injectively.  Hall's condition is necessary
and sufficient for that extension, and any injection between the used color
classes extends to a permutation of all four colors.  Independent
canonicalization of the two patterns is valid because existence of a color
permutation is invariant under composing with separate relabelings.

The target's `check_compatibility.py` builds a temporary harness around the
actual C++ table generator and compares its output to Python tables produced
by explicit injection enumeration.  Reviewer-3 ran this comparison with
temporary files redirected under reviewer storage.  It checked all
344,064 raw-pattern ranks and 130,447,851 Boolean table entries for seven,
eight, and nine labels, including false entries and padding bits, in 14.637s.
The result matched `expected_compatibility.txt` exactly.  The nine-label
portion contains 11,051 partitions and 19,185,603 compatible ordered pairs.

## Independent dense-row check

[`independent_dense_orientation.py`](independent_dense_orientation.py) checks
orientation 23, selected in advance because it and its reflected mate attain
the largest exact-seven count (450).  It reuses the independently published
Python exact-field geometry and backtracking matcher from reviewer-3's
preceding exact-three and exact-six audits, not the target census.  The checker
uses unbounded integers, validates every library coloring, scans a deliberately
wider 13 by 13 bucket neighborhood, and makes final unit-distance decisions by
exact field equality.

It reconstructs all 6,108 multiplicity-two translations, obtains the complete
edge-count vector `(33,65,122,213,297,381,399,450,4148)`, and finds a coloring
extension for all 450 exact-seven placements.  These values agree exactly with
transcript row 23.  The independent run took 18m16.081s on one core; its output
is pinned in [`EXPECTED_DENSE_OUTPUT.txt`](EXPECTED_DENSE_OUTPUT.txt).

## Reproduction

From the repository root:

```bash
src=hadwiger_nelson_parts509_two_overlap_cross_census
out=/scratch/research-team-v2/tmp/reviewer-3/parts509-seven-census.txt
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  "$src/census.cpp" -o /scratch/research-team-v2/tmp/reviewer-3/parts509-census
/scratch/research-team-v2/tmp/reviewer-3/parts509-census \
  hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  "$src/colour_libraries.txt" --through-seven > "$out"
sha256sum "$out"
PYTHONDONTWRITEBYTECODE=1 python3 "$src/verify.py" "$out" \
  | cmp - "$src/expected_verify.txt"

env TMPDIR=/scratch/research-team-v2/tmp/reviewer-3 \
  PYTHONDONTWRITEBYTECODE=1 python3 "$src/check_compatibility.py" \
  | cmp - "$src/expected_compatibility.txt"

PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_parts509_seven_edge_review3/independent_dense_orientation.py \
  hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  "$src/colour_libraries.txt" \
  | cmp - hadwiger_nelson_parts509_seven_edge_review3/EXPECTED_DENSE_OUTPUT.txt

cd hadwiger_nelson_parts509_seven_edge_review3
sha256sum -c SHA256SUMS
```

The target directory is unchanged from the declared source commit.  All
Python checks use only the standard library and are deterministic.

## Source audit

The exact-seven patch replaces production brute-force permutation tables with
the Hall predicate already described, widens the genuine-edge buffer and
cutoff from seven to eight, adds the nine-label table, and threads exact-seven
counters through row and global output.  Inspection found the forced-map
consistency checks, unused-target masks, Hall subset test, buffer bounds,
cutoff classification, pattern-rank and bitset directions, endpoint indexing,
and accumulator flow consistent.  Stopping upon an eighth genuine edge is
exhaustive for the zero-through-seven strata.

The inherited orientation construction, exact radical arithmetic, overlap
multiplicity rule, removal of overlap-induced internal edges, edge
deduplication, and certified interval filter followed by exact equality were
also rechecked in the preceding reviews and exercised by both computations.

## Trust boundaries

The full enumeration trusts the reviewed C++ source, GCC 12.2.0, ordinary
hardware execution, and the checked-in coordinate and coloring data.  The
independent implementation checks the maximally dense row 23, not the other
2,839 orientations; reflection symmetry and all remaining rows are checked
by the full transcript verifier.  Its exact-field and matching layers are
reused from preceding reviewer-3 evidence, while its seven-edge classification
is new.  The exhaustive table checker is structurally independent of the C++
Hall predicate but includes the production source in its harness.  No SAT
solver, floating-point predicate, random seed, or external graph
classification enters the result.
