# Independent review of the Parts exact-three cross-edge census

This directory records reviewer-3's audit of Discovery Net contribution
`bafkreiblx25dmbpnwvhqhl2h65x7x342g5razibwpnleozukgt7kzkhnse`, checked at
its declared source commit `dc18d4db7878fdd4169cb830f2606a128394d633`.

## Verdict

Support and reproduction, with no concrete defect found.  A clean GCC 12.2.0
build reproduced the complete 2,840-orientation, 2,373,802-placement
`--through-three` transcript byte-for-byte: SHA-256
`6a1903a823aa4712ffc76107b038e2ab2f78a844651bcdc4c47264ed94513f2c`.
The submitted verifier accepted that transcript and reproduced all global and
topology subtotals.  The full run took 10m45.878s wall time on the review host.

The result is an intermediate finite-family reduction.  It proves that all
180,216 placements in the exact-three-new-cross-edge stratum are
four-colourable, leaving 1,629,828 placements with at least four new cross
edges at this stage.  It is not a sub-509 construction, does not exclude
placements outside the fixed Parts `L`/`S+` exactly-two-overlap family, and
does not by itself improve the chromatic-number record.

## Independent re-derivation

[`independent_orientation_check.py`](independent_orientation_check.py) is a
separately written standard-library implementation.  It does not import the
target census.  It parses the 509 exact coordinates, represents
`Q(sqrt(3),sqrt(5),sqrt(11))` with unbounded Python integers, reconstructs all
2,840 forced orthogonal orientations, searches a deliberately wider 13 by 13
bucket neighborhood, and performs final unit-distance tests by exact field
equality.  It independently parses the raw colouring libraries and tests all
24 permutations of the four colour names when gluing the two gadget
colourings.

The two audited orientations were fixed in advance as transcript rows 114
and 1541, the rotation/reflection pair with the maximum observed
exact-three count.  For each row the independent implementation finds 3,890
double-overlap translations, category counts
`(216,473,496,471,2234)`, topology counts
`(46,22,3,126,187,87)`, and a colouring extension for all 471 exact-three
placements.  These records agree field-for-field with the full transcript.
The independent run took 46m30.764s wall time on one core; its output is
pinned in [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).

## Reproduction

The shared source directory was subsequently extended for later strata, so
reproduce the reviewed target from the pinned commit in a detached worktree:

```bash
src=/scratch/research-team-v2/tmp/reviewer-3/parts509-three-source
out=/scratch/research-team-v2/tmp/reviewer-3/parts509-three-census.txt
git worktree add --detach "$src" dc18d4db7878fdd4169cb830f2606a128394d633
cd "$src/hadwiger_nelson_parts509_two_overlap_cross_census"
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic census.cpp -o census
./census \
  ../hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  colour_libraries.txt --through-three > "$out"
sha256sum "$out"
PYTHONDONTWRITEBYTECODE=1 python3 verify.py "$out" | cmp - expected_verify.txt
```

From the current repository root, run the independent dense-row audit with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_parts509_three_edge_review3/independent_orientation_check.py \
  hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  hadwiger_nelson_parts509_two_overlap_cross_census/colour_libraries.txt \
  | cmp - hadwiger_nelson_parts509_three_edge_review3/EXPECTED_OUTPUT.txt
sha256sum -c hadwiger_nelson_parts509_three_edge_review3/SHA256SUMS
```

The checker uses only the Python standard library and is deterministic.  The
listed coordinate and colouring-library inputs have not changed since the
reviewed commit.

## Mathematical and implementation audit

For a fixed orthogonal image of `S+`, a translation producing two overlap
pairs is exactly a cross-difference value of multiplicity two.  Unit-separated
cross-difference values give every strict cross edge after discarding pairs
that become internal edges through either identification.  Deduplicating the
remaining endpoint pairs yields the genuinely new cross-edge graph.  For
three such edges, agreement on the two overlap colours and disagreement on
the three edge endpoints is exactly the condition that two proper internal
gadget colourings glue to a proper colouring of the strict quotient union.

Inspection of `census.cpp` found the orientation construction, radical-field
normalization, overlap multiplicity test, duplicate-edge handling, conservative
interval filter, exact final equality, topology classification, and 24-colour-
permutation compatibility test consistent with this reduction.  Stopping at
a fourth genuine edge is exhaustive for the zero-through-three strata.

## Trust boundaries

The complete enumeration trusts the reviewed C++ source, GCC 12.2.0, ordinary
hardware execution, and the checked-in exact coordinate and colouring data.
The independent audit reduces implementation correlation for two maximally
dense rows but does not independently rerun the other 2,838 orientations.
Both paths trust the supplied colouring libraries as candidate data; the
target verifier independently reconstructs them and checks all 135 `L` and
194 `S+` rows against the 1,860 and 564 internal edges.  No SAT solver,
floating-point predicate, random seed, or external classification is used in
the exact-three conclusion.
