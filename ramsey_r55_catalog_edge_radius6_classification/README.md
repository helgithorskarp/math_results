# Edge-radius-six classification around the known Ramsey(5,5,42) catalog

## Result

Start with any of the 656 known Ramsey(5,5,42) graphs (the 328 records in
McKay's catalog and their complements), and flip at most six edges. If the
result still has neither a 5-clique nor an independent 5-set, it is isomorphic
to another graph in the same known catalog.

For the 328 representative labeled parents, exact SAT enumeration finds
6,384 Ramsey-preserving sets of exactly six edge flips. They give 6,334
transitions to stored representative classes and 50 to complement classes,
covering 311 target isomorphism classes. The exact per-parent
distribution is

```text
valid sextuples    0   1   9  14  15  16  19  23  25  28  29  30  35  37  43  57
parents           40  16  40  32  32  16  32   8   8  24  16   8  16   8  16  16
```

The 40 parents with no valid six-edge flip are catalog indices

```text
39, 41, 170, 171, 173, 175, 176, 177, 178, 188,
190, 191, 192, 193, 225, 253, 254, 260, 261, 262,
263, 264, 267, 268, 269, 271, 273, 274, 275, 276,
281, 282, 285, 288, 290, 291, 294, 305, 326, 327.
```

Every labeled transition is recorded in
`EDGE_RADIUS6_MAP.tsv`. Combining the exact classifications at radii one
through six gives 37,256 nonzero labeled transitions from the 328 stored
parents. Their union reaches 552 catalog target classes: all 328 stored
classes and 224 complement classes. Twelve of these classes, two stored and
ten complement, are first reached at radius six. Complement symmetry covers
the other 328 parents.

Together with the certified two-new-vertex obstruction in
[`ramsey_r55_catalog_two_vertex_extension_obstruction`](../ramsey_r55_catalog_two_vertex_extension_obstruction),
this proves that no Ramsey(5,5,43) graph can be obtained by adjoining one
vertex to a known 42-vertex graph while changing at most six old-old edges.
Indeed, any such one-vertex extension would also extend a one-vertex deletion
of its 42-vertex catalog graph by two vertices.

The classification also independently recovers the radius-six
catalog-distance consequence in the sibling
[`ramsey_r55_doubly_exact_anchor_propagation`](../ramsey_r55_doubly_exact_anchor_propagation):
the Ramsey 42-vertex graph obtained by deleting the forced blue singleton in
that branch must be at edge-edit distance at least seven from the known
catalog. Otherwise the present radius-six classification would identify it
with a catalog graph, contradicting the extension obstruction. The sibling
proof directly enumerates the degree-compatible edit patterns in its
target-specific structural branch; the present result instead classifies all
Ramsey-preserving radius-six moves, with no degree restriction.

This is a local classification, not a new bound on `R(5,5)` and not a proof
that the known 42-vertex catalog is complete.

## Exact reduction and enumeration

For each parent, `enumerate_six_flip_sat.cpp` uses one Boolean variable for
each of the 861 edges of `K_42`. A forward threshold counter permits at most
six selected flips. If a 5-set originally has `p` edges and `10-p` nonedges,
then it can become a clique only when all of its nonedges are flipped and none
of its edges are flipped. A clique clause is therefore needed when
`10-p <= 6`. The complementary independent-set clause is needed when
`p <= 6`; five-sets with four, five, or six edges contribute both clauses.

The resulting formulas have 6,888 variables and between
1,453,820 and 1,456,572 clauses before model blocking.
CaDiCaL enumerates complete flip assignments. A blocking clause over all 861
flip variables removes the entire mathematical assignment, independent of
the intentionally nonunique counter auxiliaries. Termination with
`UNSATISFIABLE` establishes completeness of the model list under the solver
trust boundary. Assignments of sizes zero through five are counted as an
internal audit; all 328 counts equal one plus the independently published
radius-one through radius-five transition counts.

The sequential counter is sound by induction: if at least `j` flips have been
selected through position `i`, its one-way implication clauses force threshold
variable `(i,j)`. Seven selected flips therefore force the final forbidden
threshold. Conversely, for any assignment of weight at most six, setting a
threshold variable exactly when its prefix has the stated weight satisfies the
counter clauses. Thus the encoding preserves precisely the intended flip
assignments.

## Validation and trust boundary

The complete run used eight independently resumable one-parent workers. It
took 45,523.523 aggregate worker-seconds and 5,737.310 controller wall-seconds;
the slowest parent, index 241, took 212.205 seconds. The code was built
warning-free with GCC 12.2.0 and CaDiCaL 3.0.1.

The checked-in source was rebuilt independently and reproduced the complete
saved model sets for parents 0 and 1 byte for byte. An ASan/UBSan build
reproduced the zero-transition result for parent 190 without a sanitizer
finding.
The Python clause audit independently recounts all 850,668 five-sets of
parents 0 and 15 and matches their Ramsey-clause, counter-clause, total-clause,
and variable counts.
All 6,384 emitted graphs were independently reconstructed by the
standard-library Python bitset checker, compared byte for byte with the emitted
graph6 records, and tested for a 5-clique in both colors. Finally, nauty 2.8.6
canonical labeling maps every graph into the 656 known catalog orientations;
an optional NetworkX 3.5 VF2++ pass independently verifies every recorded
target isomorphism.

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
radius-two through radius-five maps, canonicalizes every survivor, compares
the complete transition map byte for byte, recomputes the all-radii transition
and target union, and runs the independent homogeneous-5-set checker. If nauty
was installed into a private prefix, put its shared-library directories on
`LD_LIBRARY_PATH` first.

To run only the fast direct check of the committed map:

```sh
python3 validate_variants.py r55_42some.g6 EDGE_RADIUS6_MAP.tsv
```

An optional orthogonal target-identity check uses NetworkX VF2++ instead of
nauty. In an isolated environment, install `requirements-networkx.txt` and
run:

```sh
python3 validate_targets_networkx.py r55_42some.g6 EDGE_RADIUS6_MAP.tsv
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
phrase searches through 2026-09-04 found no published complete radius-six
transition classification. This search-relative observation is not a
historical priority claim.
