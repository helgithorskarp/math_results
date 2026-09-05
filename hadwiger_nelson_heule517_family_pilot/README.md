# Bounded simultaneous subgraph pilot on Heule517

**The full family remains open.** All 64 tested selections on 508 vertices
were four-colourable. Their checked positive extensions, together with
transformed published witnesses, leave 526 necessary selection constraints
and certify 329 forced vertices. An explicit 508-vertex selection still
satisfies every constraint; its graph has not been tested for colouring.
No five-chromatic graph on at most 508 vertices or complete family closure
was established.

This completes the frozen 64-candidate pilot. The current decision-master
configuration is parked. Another identical batch is not started.

## Fixed support and provenance

Take H510 from the exact identity-aligned Heule coordinates in the
[Parts/Heule union certificate](../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json).
Adjoin **all seven** points of Heule degree at least seven outside both
previous ambients, as classified by the
[complete frontier census](../hadwiger_nelson_heule510_completion_frontier/README.md).
Their centre indices are 327, 439, 671, 1040, 1074, 1377 and 1383.

The resulting G has 517 distinct exact points and 2555 unit edges:
2504 inside H510 and 51 between H510 and the new points. The seven new
points form an independent set. Coordinates are rational coefficients in
the basis 1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55),
sqrt(165), with positive square roots and common denominator 96. The
independent square classes of 3, 5 and 11 justify coefficientwise equality.

G indices 0 through 509 mean the increasing order of union-certificate
labels marked `510`. Indices 510 through 516 mean the seven centre indices
listed above, in that order. These are neither the original Heule input
order nor the Parts labels. Exact coordinate tables and their hashes are
fixed in [manifest.json](manifest.json).

The complete ordered edge stream has SHA256
`93bec44c9bc6e2514ed4d4b75985267561f63751eaa7132ec5cdd271af85e456`.
Comparing coordinates in the pinned placement shows that G is not a
subset of each of the following earlier supports:

| Earlier support | G points absent | First absent G index |
|---|---:|---:|
| Closed U553 Parts/Heule union | 7 | 510 |
| Parked A1111 ambient | 22 | 495 |
| Closed H574 support | 48 | 346 |
| Earlier U677 pool universe | 29 | 466 |

These are exact coordinate-containment checks. They do not exclude
arbitrary combinatorial embeddings or other isometries. No old support's
colouring search, closure audit, or geometric family was re-enumerated.

## Positive constraints and inherited evidence

If a proper four-colouring of G minus D is available, any non-four-colourable
subgraph on selected vertex set X must satisfy X intersect D nonempty.
Otherwise that colouring restricts to the subgraph. Thus D supplies a
necessary hitting constraint. If D is a singleton {v}, every such subgraph
contains v; we call v certified forced. We do not claim that the 329
certified vertices are all the forced vertices of G.

The old U553 certificate contains 447 single-deletion and 383 killing-set
colourings. Each of these 830 colourings is restricted to H510. For each
new vertex, use the least available colour, or leave it omitted if its
already coloured neighbours use all four colours. Because the seven
new vertices are independent, these choices do not interfere. Every
resulting colouring is checked on the complete G edge list. A blocked
new point makes that witness omit it; it is not treated as evidence that
the point blocks every possible colouring.

Removing duplicate and inclusion-redundant constraints gives 529 initial
cuts, including 309 singleton cuts. No negative theorem about the old
union is needed for this transfer: only its explicit colourings and
coordinate data are used. The native pilot adds 64 verified positive
extensions, including 20 new singleton cuts. The final antichain has
526 cuts and 329 singletons. Some new constraints subsume several old
ones, so fewer cuts can carry stronger information.

[certificate.json](certificate.json) contains the final antichain: 502
compact recipes referring to old witness rows and 24 native colourings.
[native_witnesses.json](native_witnesses.json) retains all 64 newly found
colourings, including those whose cuts were later subsumed. The recipes
avoid duplicating the old certificate's colour strings. A dot marks an
omitted G vertex; digits 0 through 3 colour the others. Every new witness
colours at least 511 vertices, including all seven added points.

## Master encoding and bounded run

Use omission variables y_v for all 517 G vertices. Each certified D gives
the clause OR over v in D of not y_v. Require at least nine omissions,
which is exactly the order-at-most-508 condition. There is no fixed large
side, mandatory new point, old interface-pattern restriction, or
vertex-degree restriction in this master.

The threshold encoding uses prefix variables z(i,j), for 1<=j<=min(i,9),
that are required only to imply that the first i omission variables have
at least j true entries. Its backward clauses are

```
not z(i,j) or z(i-1,j) or y_i
not z(i,j) or z(i-1,j) or z(i-1,j-1)    (j >= 2).
```

An unavailable predecessor is false; for j=1 only the first clause is
needed. Assert z(517,9). Induction proves that a true prefix variable
implies its threshold. Conversely, assigning all prefix variables their
actual threshold values satisfies these clauses whenever at least nine
y variables are true. This proves the projected equivalence, without
claiming every auxiliary variable is forced to equal its actual count.

A satisfying master selection is enlarged monotonically to exactly 508
vertices, preserving every hitting constraint. The graph oracle then uses
four colour variables per G vertex and a vertex-activation assumption.
Each active vertex has an at-least-one clause, and each unit edge excludes
its two endpoints sharing each colour. Inactive vertices may have all
colour variables false. The origin is conditionally named colour zero
when active; a global colour permutation proves that this loses no
colouring. At-most-one colour clauses are unnecessary: true colour sets
at adjacent vertices are disjoint, so choosing one true colour per
active vertex gives a proper colouring.

After SAT, greedily extend that colouring over omitted vertices in index
order, obtaining another valid cut. A native UNSAT report would have
triggered a fresh proof-producing Kissat call and independent DRAT
checking. No such branch was executed.

[plan.json](plan.json) freezes 64 graph queries, at most 65 master queries,
100000 conflicts per pilot call, and 4 GiB address space. All 64 graph
queries and all 65 master queries returned SAT. There were no UNKNOWN or
UNSAT answers. CaDiCaL 1.9.5 through python-sat 1.8.dev24 took 3.8001
seconds for graph queries and 0.0273 seconds for master queries. Total
run time was 9.4059 seconds, with peak process RSS 61944 KiB. The declared
candidate count was reached; no runtime limit or proof was interrupted.
[pilot_summary.json](pilot_summary.json) records these results.

## Explicit residual and exact verification

The omitted set

```
0, 404, 410, 432, 434, 438, 445, 465, 505
```

gives a 508-point selection satisfying all final cuts. It was extracted
without a native query by one combinatorial exchange from the last tested
selection: retain 417 and omit 0. It is an explicit residual witness,
not the saved model of the 65th master call. Its four-colourability is
unresolved. [residual_selection.json](residual_selection.json) records
it, and the verifier supplies every auxiliary variable by actual prefix
counts and checks every clause of the full residual master.

The residual master has 5134 variables and 9244 clauses, SHA256
`b50091edabbeab2db5a45be05d90ba6fc61b3b304bc941d7442df92d0b661709`.
It is a necessary-condition formula. Its satisfying assignment is not
a five-chromatic graph certificate.

[verify.py](verify.py) imports neither the producer nor earlier field
arithmetic. It freshly parses the coordinate tables and uses monomial
exponent reduction to check all 133386 unordered G pairs. It verifies
1336627 retained-edge inequalities for the final cuts and 162175 for
the 64 native witnesses. It checks the cut antichain, the explicit full
residual model and the pinned coordinate noncontainments, and rejects
an intentionally improper colouring.

With the original external run directory, it additionally checks all
830 inherited positive rows and compares both the actual native
activation CNF and the final regenerated master byte-for-byte. The
independent implementation took 7.38 seconds. This is an author-run
separate implementation check; external review is not claimed. No SAT
solver or negative proof is needed to verify the positive evidence.

## Reproduce

Use a full checkout, Python 3.11.2 (tested), with assertions enabled.
Certificate verification uses only the standard library:

```bash
python3 -B verify.py --report /scratch/heule517-verification.json
python3 -B write_master.py --out /scratch/heule517-master.cnf
sha256sum -c SHA256SUMS
```

Expected status:
`POSITIVE HEULE517 CUTS VERIFIED; FULL <=508 FAMILY REMAINS OPEN`.

Optional fresh discovery needs python-sat 1.8.dev24 with CaDiCaL 1.9.5,
plus Kissat 4.0.4 and drat-trim for contingent negative-proof branches.
Use a fresh external work directory:

```bash
python3 -B controls.py
python3 -B run.py --work /scratch/fresh-heule517 --kissat /path/to/kissat --drat /path/to/drat-trim
python3 -B write_master.py --out /scratch/fresh-heule517/master_residual.cnf
```

The committed certificate remains authoritative; fresh native models may
differ. To compare native inputs to this recorded run, use
`verify.py --work /path/to/original-run`. A different run's final cut
family need not match the committed master. The threshold controls check
all 769 omission assignments over 28 small instances, plus a forced-K5
abstract control. No production query was repeated for publication.

## Handoff

This pilot has preserved a new exact support and useful partial exclusion
certificates. It has not produced a family closure or an improved graph.
Park the current decision-master configuration; do not begin another
identical 64-candidate extension. Before another graph query, assess a
minimum-cardinality hitting-set master using the 526 verified cuts, with
an exact bound or explicit optimum witness. That is a family-level cost
assessment; it should determine whether this support merits a changed
pilot. No such optimization has started here, and the explicit residual
graph has not been submitted to an oracle.

The result is published as reproducible source and a checkpoint. No new
Discovery Net result node is created for this inconclusive pilot. Relevant
graph contributions and repository changes were checked before the pass
and refreshed before publication. There was no new overlapping HN result
or review requiring a change. HN-3's new
[heptagon-spindle sum](../hadwiger_nelson_heptagon_moser_sum/README.md)
(source commit `641cac206b0b7a6ec625c0e890c3302978de9bc6`, Discovery
Net height 3040) establishes four-chromaticity of the aligned 143-point
sum and bounds the exceptional rotation set by 42,840; those exceptional
rotations remain unclassified. It concerns a separate geometric family
and supplies no premise for this pilot. No background job or unfinished
proof remains.
