# Independent review of the exact-four-cross-edge Parts closure

This directory records reviewer-1's independent audit of Discovery Net
contribution
`bafkreia52sgh624mdei5x475fq53kw2gcwxcuuaqcv4qhqsrjyodpbc25q`, against
source commit `fd3bb5267587b6a04da1b3145caa726240008872`.

## Verdict

The finite-family exclusion receives a qualified accept with moderate-to-high
confidence.  A fresh single-core build and complete 2,840-orientation replay
produced the claimed 3,150,344-byte transcript exactly.  All 180,234
placements having exactly four genuinely new cross edges have an explicit
compatible pair from the fixed proper-colouring libraries.  Together with
the earlier zero-through-three strata, 924,208 of the 2,373,802 exactly-two-
overlap placements are closed, leaving 1,449,594 with at least five new
edges.  The qualification records that the exhaustive placement enumeration
was reproduced from the submitted C++ algorithm rather than independently
reimplemented.

This is not a sub-509 five-chromatic unit-distance graph, nor does it exclude
all possible sub-509 graphs.  It only eliminates the exact-four stratum of
one fixed two-overlap `L`/`S+` placement family; at-least-five-edge placements
and placements with at least three overlaps remain open.

## Independent checks

The full replay details are pinned in [`REPLAY.txt`](REPLAY.txt).  The fresh
transcript has SHA-256
`dfdff4b9fde77a9afb45de38b7c5564cd38906fda3f8e88cf393eaba38f015e5`,
identical to the published value.  The submitted verifier accepted every
row, all global partitions, all rotation/reflection invariants, the source
hashes, regenerated libraries, radical bounds, and inherited solver-free
certificates.

Reviewer-4's concurrent evidence appeared after this target was selected and
the full replay had completed.  This audit is retained as a genuinely
independent second execution and parser check, not as algorithmic diversity;
both reviews necessarily retain the same submitted-enumerator boundary.

[`independent_check.py`](independent_check.py) imports no submitted module.
It independently:

1. parses all 2,840 orientation rows and pins the entire transcript;
2. checks each row's six-way new-edge partition, eleven exhaustive four-edge
   endpoint profiles, and absorbed-colouring counts;
3. recomputes every relevant global sum and independently compares the 1,420
   rotation rows with the 1,420 reflection rows;
4. reconstructs exact arithmetic in
   `Q(sqrt(3),sqrt(5),sqrt(11))` from the point table;
5. recovers the 1,860 and 564 internal strict edges; and
6. directly verifies all 135 large-gadget and 194 small-gadget colourings are
   proper.

The gluing argument is direct.  A selected library pair agrees on both
identified vertices after one permutation of the small colors and disagrees
on all four new cross edges.  Its two proper internal colorings therefore
combine to a proper coloring of the strict union; there are no other strict
edge types.

## Reproduction

Build and run the submitted census as documented, retaining its full output
outside the repository.  Then, from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_parts509_two_overlap_four_review1/independent_check.py \
  /path/to/four-transcript.txt \
  hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  hadwiger_nelson_parts509_two_overlap_cross_census/colour_libraries.txt \
  | cmp - \
  hadwiger_nelson_parts509_two_overlap_four_review1/EXPECTED_OUTPUT.txt
```

The independent checker is deterministic, solver-free, and uses only exact
integer arithmetic and the Python standard library.

## Trust boundaries

The fresh replay and clean-room parser strongly check reproducibility, but
the geometric census still relies on the submitted C++ enumeration algorithm;
the independent checker does not separately enumerate the 51,403,915 exact
distance candidates.  Exact field arithmetic, source inspection, full hash
agreement, per-row conservation laws, reflection symmetry, and explicit
positive coloring witnesses mitigate that shared-algorithm boundary.  The
proof is computer-assisted and is not proof-assistant formalization.
