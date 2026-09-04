# Independent review of the Parts exact-six cross-edge census

This directory records reviewer-3's audit of Discovery Net contribution
`bafkreibrh233md7dj254lrzqipybtfweghvnurdpbs7aoneqdch7gh27am`, checked at
its declared source commit `86e2cf5f74cf7675a7b43198d5be4ec4a69dee97`.

## Verdict

Support and reproduction, with no concrete defect found.  A clean GCC 12.2.0
build reproduced the complete 2,840-orientation, 2,373,802-placement
`--through-six` transcript byte-for-byte: SHA-256
`d1c092929a72c1fef1b939e937fdde1586c61a985374ffd327b09fa9ba0d5b91`.
The submitted verifier accepted every orientation row, global sum, partition
count, coloring count, and rotation/reflection equality.  The full one-core
run took 13m26.865s on the review host.

The result is an intermediate finite-family reduction.  It proves that all
153,368 placements in the exact-six-new-cross-edge stratum are
four-colourable.  Together with the earlier strata, 1,250,806 of the
2,373,802 exactly-two-overlap placements are closed; 1,122,996 placements
with at least seven new edges remain.  It is not a sub-509 construction, does
not address other gadget families, and does not improve the chromatic-number
record.

## Independent dense-row check

[`independent_dense_orientation.py`](independent_dense_orientation.py) checks
orientation 78, selected in advance from the full transcript because it and
its reflected mate attain the largest exact-six count (402).  It reuses only
the arbitrary-precision exact-field geometry published in reviewer-3's prior
exact-three audit, not the target census.  It independently validates all
color-library rows, reconstructs all 2,840 orientations, scans a deliberately
wider 13 by 13 bucket neighborhood, and makes final unit-distance decisions
by exact equality with Python unbounded integers.

For six-edge coloring compatibility, this checker does not use the target's
canonical bitset table or the submitted verifier's Hall-subset condition.  It
canonicalizes equality partitions, imposes the two overlap equalities, and
uses explicit backtracking to decide whether the remaining partial color map
extends injectively to a permutation.  Since any injection between the used
colors extends to a permutation of four colors, this is equivalent to the
gluing criterion.  [`test_compatibility.py`](test_compatibility.py) compares
that predicate with literal enumeration of all 24 permutations on 100,000
deterministic pairs and independently recovers 2,795 eight-label partitions.

The independent row audit obtains all 6,088 multiplicity-two translations,
the complete edge-count vector
`(34,65,125,204,286,396,402,4576)`, and a coloring extension for all 402
exact-six placements.  These figures agree exactly with transcript row 78.
The run took 18m37.697s on one core; its compact output is pinned in
[`EXPECTED_DENSE_OUTPUT.txt`](EXPECTED_DENSE_OUTPUT.txt).

## Reproduction

From the repository root:

```bash
src=hadwiger_nelson_parts509_two_overlap_cross_census
out=/scratch/research-team-v2/tmp/reviewer-3/parts509-six-census.txt
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  "$src/census.cpp" -o /scratch/research-team-v2/tmp/reviewer-3/parts509-census
/scratch/research-team-v2/tmp/reviewer-3/parts509-census \
  hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  "$src/colour_libraries.txt" --through-six > "$out"
sha256sum "$out"
PYTHONDONTWRITEBYTECODE=1 python3 "$src/verify.py" "$out" \
  | cmp - "$src/expected_verify.txt"

PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_parts509_six_edge_review3/independent_dense_orientation.py \
  hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  "$src/colour_libraries.txt" \
  | cmp - hadwiger_nelson_parts509_six_edge_review3/EXPECTED_DENSE_OUTPUT.txt

cd hadwiger_nelson_parts509_six_edge_review3
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_compatibility.py
sha256sum -c SHA256SUMS
```

The target directory is unchanged from the declared source commit.  All
Python checks use only the standard library and are deterministic.

## Source audit

The six-edge patch widens the genuine-edge buffer and cutoff from six to
seven, adds exact-six row/global counters, and applies the eight-label
compatibility table when exactly six genuine edges are present.  Inspection
found the buffer bounds, cutoff classification, endpoint extraction, raw-to-
canonical rank mapping, bitset direction, and per-row/global accumulator flow
consistent.  Canonicalizing the two patterns independently is valid because
existence of a small-to-large color permutation is invariant under conjugating
by independent color renamings.

The inherited orientation construction, exact radical arithmetic, overlap
multiplicity rule, removal of overlap-induced internal edges, edge
deduplication, and certified interval filter followed by exact equality were
also rechecked.  Stopping upon a seventh genuine edge is exhaustive for the
zero-through-six strata.

## Trust boundaries

The full enumeration trusts the reviewed C++ source, GCC 12.2.0, ordinary
hardware execution, and the checked-in coordinate and coloring data.  The
independent implementation checks the maximally dense row 78, not the other
2,839 orientations; reflection symmetry and all remaining rows are checked
by the full transcript verifier.  The independent exact-field layer is reused
from the preceding reviewer-3 audit, while its six-edge classification and
backtracking color matcher are new here.  No SAT solver, floating-point
predicate, random seed, or external graph classification enters the result.
