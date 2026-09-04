# Edge-radius-four classification around the known Ramsey(5,5,42) catalog

## Result

Start with any of the 656 known Ramsey(5,5,42) graphs (the 328 records in
McKay's catalog and their complements), and flip at most four edges. If the
result still has neither a 5-clique nor an independent 5-set, it is isomorphic
to another graph in the same known catalog.

For the 328 representative labeled parents, exact SAT enumeration finds 8,408
Ramsey-preserving sets of exactly four edge flips. They give 8,284 transitions
to stored representative classes and 124 to complement classes, covering 380
target isomorphism classes in all. The exact per-parent distribution is

```text
valid quadruples   0  1  6   8  10  15  16  17  24  26  29  31  32  35  36  37
parents            8  8  8  24   8  16  16  16  16  16  16  32  16  72  48   8
```

The eight parents with no valid four-edge flip are catalog indices 39, 170,
171, 190, 191, 192, 193, and 305. Every labeled transition is recorded in
`EDGE_RADIUS4_MAP.tsv`.

Combining the exact classifications at radii one through four gives 24,648
nonzero labeled transitions from the 328 stored parents. Their union reaches
508 catalog target classes. Complement symmetry covers the other 328 parents.

Together with the certified one-vertex extension obstruction in commit
[`1629d46`](https://github.com/helgithorskarp/math_results/tree/1629d46a8bc1b0a4249139ae7dfca04b1870145a/ramsey_r55_catalog_two_vertex_extension_obstruction),
this proves that no Ramsey(5,5,43) graph can be obtained by adjoining one vertex
to a known 42-vertex graph while changing at most four old-old edges.

This is a local classification, not a new bound on `R(5,5)` and not a proof
that the known 42-vertex catalog is complete.

## Exact enumeration

For each parent, `enumerate_four_flip_sat.cpp` uses one Boolean variable for
each of the 861 edges of `K_42`. A forward threshold counter permits at most
four selected flips. An old 5-set can become a clique only if all of its
originally absent edges are flipped and none of its originally present edges
are flipped. Thus only 5-sets with at most four absent edges need a clique
clause. The complementary rule handles independent 5-sets.

Each formula has 5,166 variables and between 632,292 and 633,954 clauses.
CaDiCaL enumerates complete flip assignments, and a blocking clause removes
each assignment after it is read. Termination with `UNSATISFIABLE` establishes
completeness of the model list. Assignments of sizes zero through three are
counted as an internal audit; all 328 counts equal one plus the independently
generated radius-one through radius-three transition counts.

As targeted implementation audits, the checked-in source reproduced the saved
complete model sets for parents 0 and 1, and an ASan/UBSan build reproduced the
zero-survivor result for parent 190 without a sanitizer finding.

The 8,408 emitted graphs were separately reconstructed from the committed map
and checked by a Python bitset search for both a clique and an independent set
of size five. Finally, nauty canonical labeling maps every graph into the
656-entry catalog. No solver trace is checked in: the compact source, complete
transition map, expected per-parent counts, and independent graph checker are
retained instead.

The published run used eight independently resumable workers and 15,279.292
aggregate worker-seconds (46.583 seconds per parent on average, 122.768 seconds
maximum). It took 1,919.376 seconds wall-clock on the 16-core research host.
The code was built warning-free with GCC and CaDiCaL 3.0.1.

## Reproduce

The complete classification needs a C++17 compiler, CaDiCaL's header and
static library, Python 3, and nauty's `labelg` and `complg` executables:

```sh
./verify_full.sh \
  /path/to/cadical/src \
  /path/to/cadical/build/libcadical.a \
  /path/to/labelg \
  /path/to/complg
```

The script runs eight workers and took about 32 minutes on the research host.
It reproduces all model counts and graph records, cross-checks the lower-radius
counts against the preceding radius-two and radius-three artifacts,
canonicalizes every survivor, compares the complete map byte for byte, and
runs the independent homogeneous-5-set checker. If nauty was installed into a
private prefix, put its shared-library directory on `LD_LIBRARY_PATH` first.

To run only the fast independent check of the committed map:

```sh
python3 validate_variants.py r55_42some.g6 EDGE_RADIUS4_MAP.tsv
```

## Data provenance

The 328-record source is McKay's ANU [Combinatorial Data
archive](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html), direct file
[`r55_42some.g6`](https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6).
Its SHA-256 digest is
`067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`.
