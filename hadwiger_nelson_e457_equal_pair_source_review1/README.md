# Independent review of the E457 physical equal-pair source

## Verdict

**ACCEPT — high confidence, with strict scope.**  At source commit
`bdaed9e41ed6af88848f550173870117702dea07`, the package
`hadwiger_nelson_e457_equal_pair_source` proves the following finite theorem:

> There is a strict plane unit-distance graph on 457 distinct points and
> 2,329 complete unit edges, with marked vertices at distance `8/3`, that is
> four-colourable but gives the marked vertices the same colour in every
> proper four-colouring.

The exact geometry, positive colouring, canonical contrary CNF and complete
all-RUP refutation were independently reproduced.  A clean-room graph
colouring implementation also reaches the same two terminal decisions without
using the reviewed solver.

This is a physical forcing source, not an abstract graph without coordinates.
It is **not** a five-chromatic graph, a construction below the 509-point
record, a proof of vertex-minimality, or global progress on the chromatic
number of the plane.  The proposed `457+53-2=508` application is conditional
on finding a physical connector on at most 53 points that shares both marked
vertices and forces them different; this package supplies no such connector.

## Independent checks

[`independent_check.py`](independent_check.py) imports no executable code from
the reviewed package.  It pins every reviewed source file at receipt tip
`a0687ef4f86b86bd2e11815a6dbee9b5ccfe2311` and performs these checks:

1. All `C(457,2)=104,196` physical pairs are expanded exactly.  A row
   `(a,b,c,d)` represents

   ```text
   ((a*sqrt(3)+b*sqrt(11))/36,
    (c+d*sqrt(33))/36).
   ```

   Unit distance is equivalent to the two integer equalities

   ```text
   3*a^2 + 11*b^2 + c^2 + 33*d^2 = 1296,
   a*b + c*d = 0.
   ```

   Linear independence over the rationals makes tuple equality and these
   coefficient tests exact.  The reconstruction gives 457 distinct points,
   exactly 2,329 edges, a connected graph, 847 triangles, minimum degree 4
   and maximum degree 25.  No inherited edge list or tolerance is used.

2. The published four-colour word is checked on every reconstructed edge and
   gives the two marked vertices the same colour.  The 457 rows and colour
   word are also verified entrywise as the stated 20-vertex deletion from the
   earlier E477 source.  This provenance check is separate from the
   self-contained finite theorem.

3. The direct four-colour encoding is rebuilt from the reconstructed graph.
   Its 1,828 variables and 12,517 clauses match `state.cnf` byte-for-byte:
   457 positive four-literal vertex clauses, 2,742 at-most-one vertex
   clauses, 9,316 edge-colour clauses, and two unit pins.

4. [`independent_drup.cpp`](independent_drup.cpp) is a clean-room watched-
   literal RUP checker.  It checks range, repetitions and tautologies; requires
   every deletion to name a live clause and applies it; validates all 131,322
   additions by reverse unit propagation; and requires the empty clause to be
   the final proof line.  The 272,901-line trace passes, with 141,579 live
   deletions and maximum added-clause length 221.  Controls accept a genuine
   unit-propagation contradiction and derived unit while rejecting an
   unsupported unit.

5. [`independent_colouring.cpp`](independent_colouring.cpp) uses in-place
   maximum-saturation branching and forced-domain propagation, rather than the
   reviewed checker's recursion.  It independently finds the equal pins
   satisfiable and rejects the unequal pins after 849,929 nodes and 850,017
   conflicts.  Its returned positive word is checked edge by edge.  `K4` and
   `K5` controls exercise its SAT and UNSAT branches.

For the negative terminal decision, fixing colours `0` and `1` loses no
generality: any proper four-colouring with unequal endpoint colours can be
renamed to those pins.  The canonical encoding is exact, and the final empty
clause in an all-RUP derivation proves that pinned formula inconsistent.

## Reproduction

From the repository root, with CPython 3.11 or later and a C++17 compiler:

```sh
review=hadwiger_nelson_e457_equal_pair_source_review1
work=$(mktemp -d /tmp/e457-review-XXXXXX)
g++ -std=c++17 -O3 -Wall -Wextra -Wpedantic -Wconversion \
  "$review/independent_colouring.cpp" -o "$work/independent-colouring"
g++ -std=c++17 -O3 -Wall -Wextra -Wpedantic -Wconversion \
  "$review/independent_drup.cpp" -o "$work/independent-drup"
python3 -B "$review/independent_check.py" \
  --colour-checker "$work/independent-colouring" \
  --drup-checker "$work/independent-drup" \
  | diff -u "$review/REPRODUCTION_RESULT.json" -
(cd "$review" && sha256sum -c SHA256SUMS)
```

The complete run took about 33 seconds on the review host.  Normal and
optimized Python runs produced the same result.  Both C++ sources compile
cleanly under the warning flags above; their small controls also pass under
AddressSanitizer and UndefinedBehaviorSanitizer.

## Construction relevance and limitations

The arithmetic allowance is exact only for a two-terminal union:
`457+53-2=508` before any further collisions.  Additional cross-edges would
not weaken a genuine equal-source/different-connector contradiction, but the
connector must itself have an exact plane realization and a certified
different-terminal relation.  The floating 487-point interaction discussed
in the source README is four-colourable and is not part of the accepted
theorem.  The deletion history proves neither minimality nor an exclusion of
other deletion orders.

A later, separate package,
[`hadwiger_nelson_e457_field_connector_obstruction`](../hadwiger_nelson_e457_field_connector_obstruction/README.md),
shows that the complete unit graph on the E457 coordinate field

```text
Q*sqrt(3) + Q*sqrt(11) + i*(Q + Q*sqrt(33))
```

has a proper colouring with these terminals equal.  Its author checks passed
during this review, and it rests on an earlier independently accepted
whole-field theorem, but it is not re-reviewed here.  Subject to that result,
any successful at-most-53-point connector must contain a point outside this
field.  This sharpens the construction boundary without changing the E457
verdict.

The working published vertex record remains Parts's 509-point, 2,442-edge
construction ([primary paper](https://arxiv.org/abs/2010.12665)); the newer
2,131-vertex result concerns a Moser-spindle-free restricted family
([Haugland preprint](https://arxiv.org/abs/2608.04542)), not the global vertex
record.

## Trust boundary

The remaining trust is the short coefficient argument above, the two small
review programs, CPython exact integers and JSON/LZMA implementations, and the
C++ compiler/runtime.  This review does not supply a proof-assistant
formalization or a second independently generated LRAT certificate.  It does,
however, avoid the reviewed geometry, colouring-search and proof-checking
implementations and records all source and result hashes in
[`SHA256SUMS`](SHA256SUMS).
