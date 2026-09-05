# Saved block colourings versus the fixed Parts partner

**Result:** eleven of the 44 distinct saved interface patterns from the
preceding rigid-block pilot are blocked by the original small partner S,
even though all 44 lie outside the old large-block relation. Complete DRAT
proofs check the eleven exclusions. They represent eleven different colour
orbits, adding 66 normalized blocked patterns beyond the old 120.

Of all 49 saved full block colourings, **38 extend to S and eleven do not**.
All full-colouring verdicts agree with their interface-only verdicts.
This proves a specific defect in using membership in the old 120-pattern
relation as the sole acceptance criterion: some outside patterns are
already incompatible with S. It does **not** show that any tested block
union S is non-four-colourable. Failure to extend one fixed colouring does
not exclude a different colouring of the same graph.

The finite audit is complete. No replacement search, further deletion,
new seed, enlarged pool, or large-graph solver query was run. A canonical
encoding of the actual composition was generated and its equivalence
proved below, but it remains unsolved. There is no record improvement,
new block on at most 373 vertices, or closure of the full finite family.

## Input and exact geometry

The parent is
[the single rigid-block pilot](../hadwiger_nelson_parts509_rigid_block_core_pilot/README.md),
source `917b4bfb1bf33317e4a192749268bb4b223b35ec`, Discovery Net
`bafkreifa5bxjpld3jz7tnm2rt3l6cdf6afa5mkhdkdbhsybia5d6u3dhy4`.
Its 49 saved SAT colourings are committed here as compact explicit
[fixtures](fixtures.json), with omitted ambient labels and a colour string
on the remaining labels in increasing order. Their provenance is pinned
by the original local transcript hash; the new checker verifies every
colouring directly, so the transcript itself is not required.

Use L={0,...,373}, S={374,...,508}, and the parent's ambient A: L plus
602 completion points, using label 509+i for completion row i. These are
all rows in the pinned first-level completion list with no sqrt(5)
coefficient and at least four original 509-point neighbours. The ambient
has 976 vertices and 6406 unit edges. The original 19-vertex interface I is

```
[0,243,244,245,344,345,346,357,358,359,360,361,362,
 363,364,365,366,367,368].
```

Normalize colour0 at vertex 0. The old relation R comprises all six
permutations of colours 1,2,3 applied to the 20 canonical rows on I minus{0}.
This gives 120 patterns. The original interface theorem certifies that
every member of R is blocked by S; its accepted review is an imported
premise only when combining the old and new blocked families. Neither
the earlier leak-map statements nor the parent's large DRAT proof is a
premise of the new eleven exclusions.

Coordinates are exact at denominator288 in the subset basis
(1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)).
The inherited builder recomputes the ambient unit edges and 306418
completion incidences. A different published multiplication routine scans
all 131760 A-to-S pairs and 9045 S pairs. It finds 552 S edges and 36 cross
edges: the original 30, plus exactly

```
(556,433), (571,475), (572,429),
(584,431), (604,479), (686,477).
```

Thus A union S consists of 1111 distinct points with 6994 unit edges. The
label convention above matters: other filtered completion pools relabel
their points. No geometric completeness beyond this pinned finite ambient
is asserted.

## Two finite extension tests

For a fixed proper colouring c of T contained in A, the available list at
s in S is the complement in{0,1,2,3} of the colours of its retained T
neighbours. A proper S colouring choosing from these lists is equivalent
to an extension of c over all cross edges. The interface-only test uses
just the original 30 cross edges; the full test uses every retained edge
from the 36-edge list. The checker reconstructs lists both by bit masking
and by direct set subtraction, and checks positive extensions on the
actual graph edges.

| Test | Cases | Checked SAT | Checked UNSAT | Unknown |
|---|---:|---:|---:|---:|
| Distinct saved interface patterns |44|33|11|0|
| Saved full block colourings |49|38|11|0|

Deduplication by the complete S-list CNF yields88 distinct instances,
66 SAT and 22 UNSAT. The five repeated cases have identical list formulas.
All negative cases use complete DRAT proofs; none is inferred from a
timeout or an unchecked native UNSAT report. Each S formula has 540 colour
variables,135 at-least-one clauses,2208 edge clauses, and one negative
unit for each unavailable colour. At-most-one clauses are unnecessary:
choosing any true colour at each vertex gives a proper list-colouring.

The blocked interface queries are
5,7,74,76,77,90,94,96,97,122,124. Their explicit patterns, source colourings,
colour-orbit representatives, proof identities and positive S colourings
are in [certificate.json](certificate.json) and the fixtures. Permuting
colours 1,2,3 fixes the origin and gives 66 distinct new blocked patterns,
disjoint from R. Combined with the imported20-class blocking theorem,
this gives at least 186 blocked patterns in31 orbits. It does not classify
all blocked patterns. In particular, the next search should not merely
append these66 patterns to an ever-growing surrogate library.

## Exact composition formula for a future bounded test

The generated formula has four colour variables for each vertex of
A union S and one activation for each vertex of A. Guard the at-least-one
clause of every A vertex by its activation. Keep all S at-least-one
clauses and all 6994-edge colour exclusions unconditional. Assert the 19
interface activations and colour0 at vertex 0. There are no forbidden
interface-pattern clauses. For any fixed U contained in A with I contained
in U, assume the activations of U minus I positively; leave all other
activations unconstrained.

This formula under those assumptions is SAT **if and only if**
UD(U union S) is four-colourable. A normalized proper colouring yields a
Boolean model by setting every inactive vertex's colours and activation
false. Conversely every model supplies a nonempty colour domain for each
selected vertex and each S vertex. Choose colour0 at the origin and any
true colour elsewhere. The edge clauses make this a proper colouring.
Unselected vertices impose no hidden restriction, because their colour
variables may all be false. Normalization loses no ordinary colouring,
since global colour permutation can assign0 to the origin.

This equivalence covers every such selected U, independently of solver
outcomes. The desired cardinality restriction |U|<=373 is an **external
selection requirement**, not a clause in this activation formula. The
unassumed formula is not a cardinality-constrained synthesis problem or
a solved quantified formula. A future UNSAT certificate for a selected
U of that size would establish a non-four-colourable union on at most 508
points; no such U is produced here.

The canonical formula has 5420 variables and 29107 clauses,398989 bytes,
SHA256 `36bd979c9e8ce2fb6c07436137290fbf6d7c5edbd182dcd07edd3a0cc9dc8805`.
It was generated twice with byte-identical output, with no solver run.

## Reproduce

Use Python 3.11 (tested 3.11.2), Kissat 4.0.4 and drat-trim. Python code needs
only the standard library. The Kissat source revision used is
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`. Use a full repository checkout;
from this directory choose a fresh nonexistent work directory:

```bash
python3 -B controls.py
python3 -B run.py --work /scratch/fresh-partner-audit --kissat /path/to/kissat --drat-trim /path/to/drat-trim
python3 -B verify.py --proofs /scratch/fresh-partner-audit --drat-trim /path/to/drat-trim --composition-cnf /scratch/partner-composition.cnf
sha256sum -c SHA256SUMS
```

Expected final status:
`ALL 93 COMPATIBILITY CASES VERIFIED; 11 NEW BLOCKED COLOUR ORBITS`.
Without `--proofs` and `--drat-trim`, the verifier checks geometry and
positive witnesses and explicitly reports that negative proofs were not
checked. No proof is accepted on the basis of its hash alone. A different
valid proof of the same deterministic CNF is acceptable; original hash
matches are reported separately.

The run used one process with a 4GiB address-space limit and a 10-second
limit per small query. All 88 queries completed, with 6.04 seconds total
solver time and 7.30 seconds complete proof-checking time. Full elapsed
time, including exact geometry, was 36.67 seconds. Peak RSS was not
measured. The generated proofs total 864702 bytes; proofs and verbose
logs remain local and are regenerated by the commands. The new large
composition formula remains unsolved and is kept outside the repository.

The controls exhaust 16 instances of the production composition encoder
on tiny graphs and 192 fixed-colouring/list cases. Verification also
rechecks all 49 source colourings across 245187 retained edges and all
positive full extensions directly. See [verification.json](verification.json),
[expected_controls.json](expected_controls.json) and
[validation.json](validation.json). The new implementation checks were
run by the author, with shared coordinate parsing and source data;
external review of this contribution is not claimed. Trust includes
exact Python arithmetic, the encoding arguments, source/data identity,
the complete DRAT checker, and ordinary code/runtime correctness.

The shared handoff read at the start includes the accepted independent review
of HN-3's arbitrary-three-point extension theorem for two dense506 hosts,
source `1a96d0fd09ef3401c12fdea7af382b87821892dc`, Discovery Net
`bafkreihnrjs2uytuq2ghqy6lkz4ag2begcqao4u7n5jd2dcf3a3j4gvmda`
at height 2963. That separate geometric family is not a premise here.

The final repository fetch also brought HN-3's heptagon difference graph,
source `b42754c605b69877056555955ac7f72a56e824f3`: an exact four-colourable
421-point graph with 42 classified potential colourings. Its unrestricted
terminal-colouring claim remains unresolved. This distinct construction
was inspected as a handoff and supplies no premise for the present audit.

**Stopping decision:** the finite audit justifies replacing the old
relation-containment objective with actual S-composition compatibility
before considering another bounded synthesis pilot. It does not justify
more runtime on the unchanged old formula. No next search phase has
started; preserve this result and yield for coordination.
