# Edge-radius-three classification around the known Ramsey(5,5,42) catalog

## Result

Start with any of the 656 known Ramsey(5,5,42) graphs (the 328 records in
McKay's catalog and their complements), and flip at most three edges. If the
result still has neither a 5-clique nor an independent 5-set, it is isomorphic
to another graph in the same known catalog.

For the 328 representative labeled parents, exact SAT enumeration finds 8,632
Ramsey-preserving sets of exactly three edge flips. They give 8,496 transitions
to stored representative classes and 136 to complement classes, covering 389
target isomorphism classes in all. The exact per-parent distribution is

```text
number of valid triples    0   2   3  11  13  20  22  29   35  36
number of parents          4   4   8  16  24  48  32  48  128  16
```

The four parents with no valid three-edge flip are catalog indices
190, 191, 192, and 193. Every labeled transition is recorded compactly in
`EDGE_RADIUS3_MAP.tsv`.

Combining this result with the prior radius-one/radius-two classification gives
16,240 nonzero labeled transitions from the 328 stored parents at radius at
most three. Their union reaches 448 catalog target classes. Complement symmetry
covers the other 328 parents.

Together with the certified one-vertex extension obstruction in commit
[`1629d46`](https://github.com/helgithorskarp/math_results/tree/1629d46a8bc1b0a4249139ae7dfca04b1870145a/ramsey_r55_catalog_two_vertex_extension_obstruction),
this proves that no Ramsey(5,5,43) graph can be obtained by adjoining one vertex
to a known 42-vertex graph while changing at most three old-old edges.

This is a local classification, not a new bound on `R(5,5)` and not a proof
that the known 42-vertex catalog is complete.

## Exact enumeration

For each parent, `enumerate_three_flip_sat.cpp` uses one Boolean variable for
each of the 861 edges of `K_42`. A forward threshold counter permits at most
three selected flips. An old 5-set can become a clique only if all of its
originally absent edges are flipped and none of its originally present edges
are flipped. Thus, under the cardinality bound, only 5-sets with at most three
absent edges need a clique clause. The complementary rule handles independent
5-sets.

Each formula has 4,305 variables and between 263,688 and 266,440 clauses.
CaDiCaL enumerates complete flip assignments, and a blocking clause removes
each assignment after it is read. Termination with `UNSATISFIABLE` therefore
certifies completeness of the model list. Assignments of sizes zero, one, and
two are counted as an internal audit; all 328 counts equal one plus the
independently generated radius-one/radius-two transition counts.

The 8,632 emitted graphs were separately reconstructed from the committed map
and checked by a Python bitset search for both a clique and an independent set
of size five. Finally, nauty canonical labeling maps every graph into the
656-entry catalog. No solver output or proof trace is checked in: the compact
source, complete transition map, expected per-parent counts, and independent
graph checker are retained instead.

The published full run used eight stoppable workers and 7,170.360 aggregate
worker-seconds (21.861 seconds per parent on average, 45.468 seconds maximum).
The code was built warning-free with GCC and CaDiCaL 3.0.1.

## Reproduce

The complete classification needs a C++17 compiler, CaDiCaL's header and
static library, Python 3, and nauty's `labelg` and `complg` executables. For
example:

```sh
./verify_full.sh \
  /path/to/cadical/src \
  /path/to/cadical/build/libcadical.a \
  /path/to/labelg \
  /path/to/complg
```

The script runs eight workers and took about fifteen minutes wall-clock on the
16-core research host. It reproduces all model counts and graph records,
cross-checks the lower-radius counts against the preceding radius-two artifact,
canonicalizes every survivor, compares the complete map byte for byte, and
runs the independent homogeneous-5-set checker.

If nauty was installed into a private prefix, put the directory containing its
shared library on `LD_LIBRARY_PATH` before running the command.

To run only the fast independent check of the committed map:

```sh
python3 validate_variants.py r55_42some.g6 EDGE_RADIUS3_MAP.tsv
```

## Data provenance

The 328-record source is McKay's ANU [Combinatorial Data
archive](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html), direct file
[`r55_42some.g6`](https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6).
Its SHA-256 digest is
`067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`.
