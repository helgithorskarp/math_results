# Fixed-profile H514 pilot leaves an exact 8,974-core family

**Computer-assisted lemma.** Of the 190,536 distinct unresolved H514 cores
in the [complete core reduction](../hadwiger_nelson_heule514_core_propagation),
**181,562 are four-colourable**. The exact remaining family consists of
**817 induced cores on 507 vertices and 8,157 on 508 vertices**.
A non-four-colourable subgraph of H514 on at most 508 vertices exists if
and only if a member of this specified 8,974-core family is non-four-colourable.
The remaining cases are unresolved; there is no record improvement or
complete closure of H514.

All 77 prespecified profile representatives are four-colourable. This
sampling statement alone does not decide their profiles. The much larger
closure follows from explicit positive certificates and a complete cover
audit over the whole input family. Sixteen of the 77 original profiles are
fully covered; 61 still contain unresolved cores.

## Exact support and inherited reduction

H514 is the fixed 514-point support with 2,526 complete unit edges from the
[interface certificate](../hadwiger_nelson_heule514_interface). The old 510
vertices are the increasing union labels marked `510` in the archived H510
certificate; the new vertices 510 through 513 are the exact completion
centres 170,436,1239,1527. Their induced graph is a path in that order.
Coordinates lie in the positive squarefree basis
`1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165`, with denominator 96.
No rounded distance predicate is used.

The interface's 516 positive omission cuts first reduced the target-order
question to 258,914 induced 508-vertex graphs. The preceding complete
4-core reduction proved 68,378 of those four-colourable and gave a bijection
from the remaining original candidates to 190,536 distinct induced cores.
A graph is four-colourable exactly when its 4-core is: restore vertices
peeled at degree at most three in reverse order. This inherited theorem is
an explicit premise of the new family equivalence. It is not rerun here.

The input core-omission stream has 4,493,362 bytes, SHA-256

`f00bfa52ad63aafb374150cff7917bd7c45716bee19cf416b350b2d0a16d1be2`.

Its rows are increasing tuples of omitted H514 indices, sorted by
`(tuple length, tuple)`, comma-separated decimal ASCII with one LF per row.
The parent [core census](../hadwiger_nelson_heule514_core_propagation/core_census.json)
defines 77 profiles by core order, number of omitted large-block vertices,
and the omission mask of the four new path vertices. Mask bit i means
vertex 510+i is omitted. These describe actual cores, not just the original
six-vertex omissions.

## Frozen bounded pilot

Before querying, [plan.json](plan.json) froze exactly the first-input-row
representative of every parent profile, in census order. The complete
77-candidate list is [candidates.json](candidates.json), SHA-256

`1a91c902abf46af848d9e37fb22e391bd49e1bfadab7f756c065a88e0cb6cd5f`.

Every representative retains the required 16 boundary vertices, so the
[verified optional-path projection](../hadwiger_nelson_heule514_path_projection)
applies. Each formula has 2,052 variables: four colour indicators for each
old vertex and twelve path-colour availability indicators. Retained old
vertices receive an at-least-one clause; retained old unit edges prohibit
equal colour indicators. The origin has colour zero. Availability variables
are equivalent to the conjunction of negated neighbour indicators for
colours one, two and three. The 37-clause optional-path kernel is specialized
to the selected new vertices. No new-vertex colour indicators remain.

There is no at-most-one clause on old indicators. Choosing the minimum true
indicator gives a proper old colouring; its actual available lists contain
the model's lists, so a path extension still exists. The producer finds a
lexicographic extension by dynamic programming. The independent raw audit
checks every possible retained path assignment by direct enumeration and
recovers the same candidate colouring.

The pilot used python-sat 1.8.dev24, CaDiCaL 1.9.5, Python 3.11.2 on Linux.
Each candidate received a fresh solver with default options and no
assumptions or retained learned clauses, a 100,000-conflict limit, at most
60 seconds wall time, and a 4 GiB address-space cap. The whole pilot had a
900-second cap and no retries. Formula hashes, clause counts and native
outcomes are in [cases.json](cases.json). Clause counts range from 10,310
to 10,502.

All **77 calls returned SAT**, with no UNKNOWN, UNSAT, unqueried candidate,
or worker failure. They used 55,424 conflicts in total; the maximum for one
candidate was 6,739. Summed native solve time was 2.7619 seconds; the entire
pilot including fresh processes took 13.7669 seconds. Maximum worker
`ru_maxrss` was 28,432 KiB. Wall limits were not approached. These resource
figures describe this run, not a bound for other graphs or solver builds.

Two initial solver-interface controls returned the known outcomes for
abstract K4 and K5 under four-colouring encodings, with the K4 model
checked directly. These controls are not Euclidean unit-distance
constructions. No negative target certificate is needed or claimed.

## Compact positive certificate and exact coverage

For each SAT candidate the producer directly checked the 514-character
colour string on every retained unit edge. It then greedily restored
omitted vertices in increasing index order, choosing the least available
colour, until no further restoration was possible. The 77 restored
witnesses produce 49 distinct omission cuts. Removing cuts which contain
another cut leaves just **15** minimal positive witnesses, stored in the
9,316-byte [certificate.json](certificate.json).

A row gives a complete proper four-colouring of H514 minus D, using `.` at
exactly the omitted vertices. Colours are `0,1,2,3`. Its source candidate
index records provenance. The minimal omission sets are:

| Size | Omission sets D |
|---:|---|
| 1 | {46}, {65}, {108}, {210}, {219}, {301}, {371}, {436}, {449} |
| 2 | {59,439}, {257,512}, {439,448}, {439,497} |
| 3 | {59,510,512}, {398,433,439} |

For any input core H514 minus O, a positive witness applies exactly when
**the entire set D is contained in O**. Restrict that proper colouring to
the core. Intersecting D without containing it is insufficient. The producer
tests this relation using integer bitmasks; the separate checker enumerates
all relevant tuple subsets of O and looks them up in a dictionary. Both
choose the least canonical certificate index.

All 190,536 coverage tags agree. Their one-byte stream uses indices 0 through
14 and 255 for uncovered; it has SHA-256

`d93df6d518372b170945f482654eb90cc066398db15c05e621a004f95fbeaa9d`.

The 181,562 covered cores represent about 95.29 percent of this input
family. The nine singleton witnesses also prove nine additional vertices
mandatory in any non-four-colourable H514 subgraph. Together with the
parent's 484 singleton forcings, there are now **493 forced vertices**.
The 21 still-free indices are recorded by the verifier; this does not
assert that any subgraph retaining all forced vertices is non-four-colourable.

For the new family equivalence, remove all these positively covered cores
from the parent's equivalent family. Every surviving core is itself a
unit-distance graph of order at most 508, proving the converse directly.
Combining this step with the preceding peeling result now certifies 249,940
of the original 258,914 target graphs four-colourable.

## Independent verification

[verify.py](verify.py) imports no pilot, cover routine, projected compiler,
path dynamic program or SAT package. The exact geometric checker it uses
reconstructs all 514 points and all 131,841 pair norms directly from the
pinned coordinate files. It independently recovers the large-block indices
from zero squarefree coefficients.

The audit checks:

- 37,651 retained-edge inequalities for the 15 compact witnesses;
- all 77 representative colourings by restriction, with 190,119 edge checks;
- every row, coverage tag and profile count of the 190,536-core input;
- the exact sorted 8,974-row survivor stream, including order and byte hash;
- three malformed-colouring rejection controls.

The optional raw-run audit independently reconstructs and matches all 77
actual formula byte streams. It checks all 77 Boolean models against
800,458 clauses, directly enumerates the retained path assignments, checks
382,890 candidate/restored edge inequalities, verifies all 326 restoration
steps and compares all 15 public witness source rows. Mathematical entries
in all 77 public case rows are matched; timings are not reproduction
invariants. The original archived runtime metadata was also matched to the
native output before publication.

The compact audit took about 2.8 seconds; including all archived native
models took about 4.7 seconds. [verification.json](verification.json) and
[validation.json](validation.json) preserve the exact recorded checks.
The proof of positive coverage needs only the compact witnesses, complete
unit-edge graph and exact coverage membership, not SAT solver soundness.
Author-run independent implementations are distinguished from separate-
author acceptance or proof-assistant formalization, neither of which is
claimed for this new result.

## Exact unresolved checkpoint

The surviving canonical core-omission stream has **8,974 rows**, **215,488
bytes**, and SHA-256

`8f0448c4d9f9cdd0c7f7d1fa1e69aef3ab6d7a368b0cfc6782ea7debedb8a38e`.

| Core order | Unresolved cores |
|---:|---:|
| 507 | 817 |
| 508 | 8,157 |

All 77 original profiles and their remaining counts are in
[coverage.json](coverage.json). A residual row means only that none of the
15 new positive certificates applies; its chromatic status is unknown.
There is no unreported negative proof trace.

## Reproduction and files

Python's standard library suffices for the positive theorem. From the
repository root, first obtain the parent core stream and graph packet using
the commands in the [core-reduction README](../hadwiger_nelson_heule514_core_propagation/README.md).
Do not repeat that census when the checked files are already available.
With the parent work directory at `/tmp/hn514-core`:

```sh
python3 -B hadwiger_nelson_heule514_profile_pilot/verify.py --frontier /tmp/hn514-core/core_omissions.txt --work /tmp/hn514-profile-check
```

This reconstructs the exact survivor and tag streams independently from the
public certificate. It does not call a solver. To replay the historical
search with an interpreter containing python-sat 1.8.dev24:

```sh
/path/to/pysat-python -B hadwiger_nelson_heule514_profile_pilot/controls.py --out /tmp/hn514-profile-controls
/path/to/pysat-python -B hadwiger_nelson_heule514_profile_pilot/pilot.py --graph /tmp/hn514-core/graph.txt --out /tmp/hn514-profile-run
python3 -B hadwiger_nelson_heule514_profile_pilot/cover.py --pilot /tmp/hn514-profile-run --frontier /tmp/hn514-core/core_omissions.txt --inputs /tmp/hn514-core/inputs.json
python3 -B hadwiger_nelson_heule514_profile_pilot/verify.py --frontier /tmp/hn514-core/core_omissions.txt --work /tmp/hn514-profile-recheck --pilot /tmp/hn514-profile-run
```

Pilot and control output directories must be new. Optional raw auditing
expects the recorded mathematical outcomes and deterministic colour choices;
a different solver build may find different valid colourings. The compact
certificate audit is independent of such search variations.

[manifest.json](manifest.json) pins inherited inputs and method sources;
[SHA256SUMS](SHA256SUMS) pins this package. Full CNFs, native models, raw
restored witnesses, logs, coverage tags and survivor streams remain local
and regenerate. They are not published as large exhaustive-search dumps.
The public package contains substantive generators, the independent
checker, the fixed candidate list, concise case statistics, 15 compact
colourings and complete profile counts.

The remaining trust boundary is exact coordinate transcription and basis
independence, inherited family equivalence, ordinary restriction/peeling
arguments, complete finite execution, integer/file semantics and faithful
certificate parsing. There is no floating-point edge predicate and no
unverified UNSAT assertion in the theorem.

## Family-level decision and shared context

This completes the frozen 77-profile pilot and its complete whole-family
cover audit. The 8,974-core remainder and 493 mandatory vertices justify
one **complete decision attempt on the entire remaining finite family**,
not another sample or deletion-stratum ladder. Freeze that full input and
bounds at the next pass. Every closure case must have a checked colouring
or a contained checked positive cut; any negative target needs a fresh,
independently checked proof and exact graph verification before a record
claim. UNKNOWN outcomes remain explicit and do not authorize runtime
extension. No query in that next phase has begun.

The incremental shared refresh read HN-3's
[all-contact Moser extension](../hadwiger_nelson_moser_all_terminal_contacts)
and its [accepted independent review](../hadwiger_nelson_moser_all_terminal_contacts_review1).
They close spindle-disjoint terminal-only full-gadget assemblies below 509
under private-interior hypotheses. They supply no H514 premise, and their
geometric lane is not duplicated here. No new objection was found in the
inspected core-reduction or path-projection neighbourhoods.

No background job or unfinished proof remains. The campaign's target graph
has not been established by this pass. Yield before starting the complete
remaining-family decision.
