# A degree guard for the quantified Parts family

This package restricts the universally tested pool selections to those
whose selected vertices all have degree at least four in L union X.
The resulting family statement is equivalent to the previous exact
colouring dual: every selection of at most 134 pool points is
four-colourable beside the fixed 374-point L.

[PROOF.md](PROOF.md) gives the reduction, guarded CNF semantics and an
explicit colouring-extension argument. The degree condition is classical
and already appeared in the earlier shape and cover work. Its guarded
quantified implementation is the contribution here. **The revised full
formula is unsolved; no new family closure, lower bound or five-chromatic
graph is established.**

## Why the family quantifier matters

Any counterexample has an inclusion-minimal selected subset. Every vertex
of that subset has degree at least four, since a colouring after deleting
a vertex of degree at most three extends greedily. Equivalently, repeatedly
remove such vertices, colour the remaining graph, and restore them in
reverse order.

Individual skipped selections need not be four-colourable. The checker
includes K5 plus an isolated point: the new matrix accepts the whole set
through its degree guard, but the K5 subset still refutes the family.
It also checks that an **unselected** deficient vertex cannot enable escape.
These are abstract logical fixtures, not plane unit-distance graphs.

## Reproduce

From the repository root with Python 3.11 standard library:

```sh
python3 hadwiger_nelson_parts509_quantified_mindegree/verify_degree.py
```

Expected: `MINIMUM-DEGREE FAMILY REDUCTION CHECKS VERIFIED`, with 58
fixtures, 1131 selector assignments, 1131 fixed specializations and 910
checked lifted colourings. Direct graph-colouring search and edge counting
are compared with a parsed-CNF DPLL evaluator. [expected.json](expected.json)
contains the exact results and the non-equivalent pointwise examples.

The real original 509-vertex and deletion of vertex 397 fixed formulas are byte-identical
to their preceding controls. In particular, the original 509-vertex SAT instance
has the same hash as the previously independently checked DRAT input.
No new proof-generation run is needed or claimed. A published admissible
508-vertex residual selection is also replayed: all its 2402 strict edges,
degree conditions and fixed-matrix colouring pass.

Generate the new full formula locally:

```sh
python3 hadwiger_nelson_parts509_quantified_mindegree/encode_degree.py \
  --out /tmp/parts-degree508.qdimacs
```

It has **11843 variables and 92468 clauses**, with 303 universal selectors
followed by 11540 existential variables. Expected QDIMACS SHA-256:

```text
08e5a931743148cb50534d0d5e4d8cd5687137d229844148215a0a080c77c9d6
```

The 303-point universe and its labels are retained. Peeling the full pool
removes only global vertex 1302 and stops at 302 points; its exact neighbours
are in expected.json. This omission is already implied by the necessary
degree condition and is not a new geometric closure.

For native calibration of changed finite fixtures only:

```sh
python3 hadwiger_nelson_parts509_quantified_mindegree/calibrate.py \
  --solver /path/to/depqbf --work /tmp/parts-degree-controls --seconds 5
```

Use a fresh work directory. The producing Debian DepQBF 5.01-3 executable
agreed on all 48 changed controls: 25 true and 23 false. Ten byte-identical
base fixtures were skipped. The native workflow took about 0.22 seconds;
the exact binary hash and measurements are in
[calibration_summary.json](calibration_summary.json). Neither this command
nor the finite verifier solves the full family. Native verdicts calibrate
the implementation; the direct finite checks establish the small truths.

## Handoff and trust

The new formula adds an escape witness for a selected degree violation.
Each witness condition uses a small conditional sequential counter; every
ordinary colouring clause uses the common escape guard. The exact budget
counter stays unguarded. The encoding has more variables and clauses than
the previous formula; no performance improvement is asserted before a
new bounded family pilot.

This completes the reduction-and-validation milestone. The next useful
step is one bounded pilot of this changed formulation after coordination.
The previous unchanged 600-second configuration is not rerun here, and
the isolated cut/shrink loop remains paused. A native false result still
needs exact selection decoding and an independent non-four-colourability
certificate; a true result needs a checked quantified proof or complete
colouring strategy. A five-colouring is additionally required for a
five-chromatic record claim.

All input code/data is pinned in [manifest.json](manifest.json), including
the base dual and its transitive exact-geometry and interface dependencies.
The unformalized reduction and encoder, integer arithmetic, prior complete
interface theorem and imported SAT/DRAT evidence retain their explicit
trust boundaries. This is author verification, not external review.
Generated formulas and native logs remain local.
