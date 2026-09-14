# Moser--Golomb double-neighbour dockings have neutral low-arity interfaces

## Result

Let `M` be the standard seven-point Moser spindle, and let `D` be the complete
set of eighteen external points having at least two unit neighbours in `M`.
The imported exact source theorem proves that every point of `D` has exactly
two such neighbours.

Let `G` be the standard ten-point Golomb graph.  This package enumerates every
direct or reflected isometry `f` for which two distinct vertices of `f(G)`
are two distinct points of `D`.  After exact transformation deduplication
there are 972 placements.  On each collision-merged support `M union f(G)`,
the complete strict unit-distance graph has all of the following properties:

- it has 12--17 distinct physical points and 23--36 unit edges;
- it has chromatic number exactly four;
- every proper four-colouring of `M` extends to the union;
- every proper four-colouring of `f(G)` extends to the union; and
- every physical nonedge admits a proper four-colouring with equal endpoint
  colours and another with different endpoint colours.

Thus neither complete component projection is restricted, and no physical
pair carries a relation beyond its bare edge/nonedge relation.  The result
retires this exact high-contact docking mechanism.  It does **not** rule out
higher-arity relations on mixed terminals, arbitrary Moser--Golomb placements,
other atoms, or later contacts not forced by this docking rule.

This is a restricted construction-family exclusion, not a five-chromatic
graph and not progress on the published 509-vertex record by itself.

## Why the census is complete

Every qualifying isometry maps an unordered pair of Golomb vertices to an
equal-distance unordered pair of `D`.  Conversely, each such pair match,
either endpoint correspondence, and either determinant sign determines one
isometry.  The exact enumeration has 1,188 recipes and 972 distinct
transformations.  The nine distance classes appearing in both pair spectra
are all included.

The specified docking vertices contribute four formal Moser contacts because
each has exactly two Moser neighbours.  Other unit contacts and as many as
five incidental Moser--Golomb collisions are not inferred from the recipe:
the verifier merges all seventeen formal addresses by exact coordinate
equality and tests every remaining physical pair for unit distance.

## Relation certificate

Fix the first unit triangle of each source to colours `0,1,2`.  There are 16
canonical proper Moser patterns and 95 canonical proper Golomb patterns,
representing all proper labelled four-colourings up to a global colour
permutation.  The verifier constructs and directly checks all
`972*(16+95)=107,892` extensions.

For a physical nonedge `uv`, equality is feasible exactly when the normalized
pin `c(u)=c(v)=0` extends, and inequality is feasible exactly when
`c(u)=0,c(v)=1` extends; global palette permutations justify the normalization.
Both extensions are constructed for all 87,024 nonedge instances, giving
174,048 checked positive words.  Unit edges are different in every proper
colouring by definition.  The Moser subgraph has no three-colouring by direct
exhaustion, while the positive words supply four-colourings, proving the exact
chromatic-number statement.

The three stream hashes in `expected.json` bind the complete collision/edge
inventory and the deterministic positive words without storing a multi-
megabyte witness table.

## Reproduce

CPython 3.11 or later and the standard library suffice.  From the repository
root:

```sh
python3 -B hadwiger_nelson_moser_golomb_double_neighbour_docking/verify.py --check-expected
python3 -O -B hadwiger_nelson_moser_golomb_double_neighbour_docking/verify.py --check-expected
sha256sum -c hadwiger_nelson_moser_golomb_double_neighbour_docking/SHA256SUMS
```

The verifier imports only the data file
`hadwiger_nelson_moser_all_terminal_contacts/certificate.json`, whose bytes
are pinned to SHA-256
`bddb9275204535cccce1d66bd2ad1415040a6807fdffb7902dec31fd57126a98`.
That source was introduced at commit
`061fb2c248515bf6c7385304d2ea53187de4a44c`; the present verifier rechecks the
eighteen docking points and their two-neighbour property.  The Golomb
coordinates are embedded directly.

All coordinate operations use `Fraction` arithmetic in
`Q(sqrt(3),sqrt(11))`.  There is no floating-point predicate, native solver,
negative solver answer, external data download, private input, or omitted
proof trace.  The exact arithmetic, exhaustive enumeration, backtracking
implementation, hash functions, CPython runtime, and ordinary hardware are
trust boundaries.  This is author-side evidence pending independent review.

## Construction disposition

The architecture was chosen because mapping two Golomb vertices into `D`
guarantees at least four component-cross contact incidences while using only
12--17 points.  The complete unrestricted tests show that even this density
does not alter either component's colouring relation or produce a two-pin
driver.  Adding copies, changing to a one-contact family, or mining a host is
not licensed by this neutral result.

The current comparison remains Parts' genuine 509-point, 2,442-edge strict
plane unit-distance graph.  No historical-priority or smallest-exclusion
claim is made here.
