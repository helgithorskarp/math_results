# Edge-radius-two classification around the known Ramsey(5,5,42) catalog

## Result

Start with any of the 656 known Ramsey(5,5,42) graphs (the 328 records in
McKay's catalog and their complements), and flip at most two edges.  If the
result still has neither a 5-clique nor an independent 5-set, it is isomorphic
to another graph in the same known catalog.

For the 328 representative labeled parents, exact enumeration finds 2,040
Ramsey-preserving one-edge flips and 5,568 Ramsey-preserving two-edge flips.
These 7,608 labeled transitions land in 383 target isomorphism classes: 326 of
the stored representatives and 57 of their complements.  Every transition is
listed compactly in `EDGE_RADIUS2_MAP.tsv`.

Together with the certified one-vertex extension obstruction in commit
[`1629d46`](https://github.com/helgithorskarp/math_results/tree/1629d46a8bc1b0a4249139ae7dfca04b1870145a/ramsey_r55_catalog_two_vertex_extension_obstruction),
this proves that no Ramsey(5,5,43) graph can be obtained by adjoining one vertex
to a known 42-vertex graph while changing at most two old-old edges.

This is a local classification, not a new bound on `R(5,5)` and not a proof
that the known 42-vertex catalog is complete.

## Exact enumeration

For a fixed parent graph and a two-edge flip set `F`, an old 5-set can become a
clique only if all of its originally absent edges lie in `F` and no originally
present edge in that 5-set lies in `F`.  Since `|F| <= 2`, only 5-sets with one
or two absent edges need consideration.  The complementary condition handles
independent 5-sets.

`enumerate_two_flip_ramsey.cpp` marks every forbidden edge pair from those
conditions and emits every unmarked one- or two-edge variant.  The full output
was independently checked with a separate bitset homogeneous-5-set search.
nauty canonical labeling then maps every emitted graph to the 656-entry catalog.

An orthogonal SAT encoding was also run for all 328 parents.  It uses 42 new
incidence variables, 861 old-edge flip variables, a forward sequential
at-most-two counter, and every potentially active homogeneous-5-set clause.
All 328 formulas were UNSAT; median solving time was 1.58 seconds, p95 was 2.17
seconds, and the maximum was 3.33 seconds.  Those bulk proofs are not retained.

For representative parent 0, the direct formula has 3,486 variables and
149,573 clauses.  A twice-identical extracted 7,190-clause core and its compact
DRAT proof are checked in.  The proof replays after the verifier confirms that
the core is a clause-multiset subset of the regenerated direct formula.

## Reproduce

The complete classification needs a C++17 compiler, Python 3, and nauty's
`labelg` and `complg` executables:

```sh
./verify_full.sh /path/to/labelg /path/to/complg
```

The compact SAT cross-check needs `drat-trim`:

```sh
./verify_drat_crosscheck.sh /path/to/drat-trim
```

## Data provenance

The 328-record source is McKay's ANU [Combinatorial Data
archive](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html), direct file
[`r55_42some.g6`](https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6).
Its SHA-256 digest is
`067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`.
