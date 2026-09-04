# Edge-radius-five classification around the known Ramsey(5,5,42) catalog

## Result

Start with any of the 656 known Ramsey(5,5,42) graphs (the 328 records in
McKay's catalog and their complements), and flip at most five edges. If the
result still has neither a 5-clique nor an independent 5-set, it is isomorphic
to another graph in the same known catalog.

For the 328 representative labeled parents, exact SAT enumeration finds
6,224 Ramsey-preserving sets of exactly five edge flips. They give 6,154
transitions to stored representative classes and 70 to complement classes,
covering 346 target isomorphism classes. The exact per-parent
distribution is

```text
valid quintuples   0  1  2  4  5   8  14  20  21  22  23  27  28  33  36
parents           16  8 16  8  8  16  32  48   8  48  32  16  48   8  16
```

Every labeled transition is recorded in `EDGE_RADIUS5_MAP.tsv`. Combining the
exact classifications at radii one through five gives 30,872
nonzero labeled transitions from the 328 stored parents. Their union reaches
540 catalog target classes. Complement symmetry covers the
other 328 parents.

Together with the certified one-vertex extension obstruction in
[`ramsey_r55_catalog_two_vertex_extension_obstruction`](../ramsey_r55_catalog_two_vertex_extension_obstruction),
this proves that no Ramsey(5,5,43) graph can be obtained by adjoining one
vertex to a known 42-vertex graph while changing at most five old-old edges.

The classification also independently recovers the distance consequence in
the sibling target-specific
[`verify_known_r42_radius5.py`](../ramsey_r55_doubly_exact_anchor_propagation/verify_known_r42_radius5.py):
the Ramsey 42-vertex graph obtained by deleting the forced blue singleton in
that branch must be at edge-edit distance at least six from the known catalog.
The sibling proof is solver-free and restricted to its prescribed degree
sequence; the present result is a solver-based classification of every
Ramsey-preserving radius-five move, with no degree restriction.

This is a local classification, not a new bound on `R(5,5)` and not a proof
that the known 42-vertex catalog is complete.

## Exact reduction and enumeration

For each parent, `enumerate_five_flip_sat.cpp` uses one Boolean variable for
each of the 861 edges of `K_42`. A forward threshold counter permits at most
five selected flips. If a 5-set originally has `p` edges and `10-p` nonedges,
then it can become a clique only when all of its nonedges are flipped and none
of its edges are flipped. The complementary rule handles independent sets.
Since one of `p` and `10-p` is at most five, every 5-set contributes at least
one clause; a balanced five-edge 5-set contributes both clauses.

The resulting formulas have 6,027 variables and between 1,086,306 and
1,087,968 clauses before model blocking. CaDiCaL enumerates complete
flip assignments. A blocking clause over all 861 flip variables removes the
entire mathematical assignment, independent of the intentionally nonunique
counter auxiliaries. Termination with `UNSATISFIABLE` establishes completeness
of the model list under the solver trust boundary. Assignments of sizes zero
through four are counted as an internal audit; all 328 counts equal one plus
the independently published radius-one through radius-four transition counts.

The sequential counter is sound by induction: if at least `j` flips have been
selected through position `i`, its one-way implication clauses force threshold
variable `(i,j)`. Six selected flips therefore force the final forbidden
threshold. Conversely, for any assignment of weight at most five, setting a
threshold variable exactly when its prefix has the stated weight satisfies the
counter clauses. Thus the encoding preserves precisely the intended flip
assignments.

## Validation and trust boundary

The complete run used eight independently resumable one-parent workers. It
took 24,938.000 aggregate worker-seconds; the slowest parent took 190.761
seconds. The code was built warning-free with GCC
12.2.0 and CaDiCaL 3.0.1.

The checked-in source was rebuilt independently and reproduced the complete
saved model sets for parents 0 and 1 byte for byte. An ASan/UBSan build
reproduced the zero-survivor result for parent 190 without a sanitizer
finding. All 6,224 emitted graphs were independently reconstructed by
the standard-library Python bitset checker and tested for a 5-clique in both
colors. Finally, nauty 2.8.6 canonical labeling maps every graph into the 656
known catalog orientations.

No SAT proof trace is checked in. Completeness therefore trusts the explicit
C++ reduction, CaDiCaL's final UNSAT answers after model blocking, the compiler
and hardware. Direct witness validity is separately checked in Python;
catalog membership additionally trusts nauty. The compact source, complete
transition map, expected per-parent counts, hashes, and independent checker
are retained instead of bulky solver logs or traces.

## Reproduce

The complete classification needs a C++17 compiler, CaDiCaL's header and
static library, Python 3.11 or later, and nauty's `labelg` and `complg`:

```sh
./verify_full.sh \
  /path/to/cadical/src \
  /path/to/cadical/build/libcadical.a \
  /path/to/labelg \
  /path/to/complg
```

The script runs eight deterministic workers. It reproduces all model counts
and graph records, cross-checks every lower-radius count against the preceding
radius-two through radius-four maps, canonicalizes every survivor, compares
the complete transition map byte for byte, and runs the independent
homogeneous-5-set checker. If nauty was installed into a private prefix, put
its shared-library directories on `LD_LIBRARY_PATH` first.

To run only the fast direct check of the committed map:

```sh
python3 validate_variants.py r55_42some.g6 EDGE_RADIUS5_MAP.tsv
```

## Data provenance and scope

The 328-record input is McKay's ANU [Combinatorial Data
archive](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html), direct file
[`r55_42some.g6`](https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6).
Its SHA-256 digest is
`067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`.
McKay and Radziszowski describe the 656 known orientations and extensive
heuristic neighborhood searches in
[*Subgraph counting identities and Ramsey
numbers*](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf), but explicitly
state catalog completeness as a conjecture. Targeted primary-source and exact
phrase searches through 2026-09-04 found no published complete radius-five
transition classification. This search-relative observation is not a
historical priority claim.
