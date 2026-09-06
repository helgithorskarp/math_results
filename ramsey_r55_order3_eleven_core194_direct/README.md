# A complete direct decision model for the Core194 empty-pair cases

Both complete direct pair-color cases returned **UNKNOWN at 60 seconds**.
No further branch or whole core is excluded; the four-versus-seven frontier remains
**17 classes / 9,153 labeled cores**, with Core194 still open.
No target graph or Ramsey lower-bound improvement is claimed.

This package gives a new, self-contained **320-variable** encoding of
each full Core194 pair-color case, with an independent reconstruction
of every clause. It contains only physical edge-orbit variables. The
mathematical result is an exact formulation and coverage proof; a
terminal graph or exclusion additionally requires checked solver evidence.

The [proof](PROOF.md) establishes the two-way equivalence between a
formula model and a Ramsey(5,5;43) coloring with the stated core, action
and distinguished empty pair. It also justifies covering every empty
pair of a given color, using a permutation of fixed vertices. The
previous full search formulas are not inputs to this reconstruction.

## Literal scope and complete clauses

The action is `(0 1 2)(3 4 5)...(30 31 32)`, with ten fixed vertices.
The first four moving triangles are internally red and the other seven
internally blue. The twelve-vertex Core194 has cross word
`100110110110110100` on cycle pairs 01,02,03,12,13,23, using offset
`(t-s) mod 3` on `3i+s,3j+t`. The distinguished fixed vertices 33,34
are blue to all twelve core vertices. Their edge is blue or red.

There are 165 moving cross-orbits, 45 fixed pairs, and 110 fixed-to-moving
orbits. All 320 variables directly denote red edge colors; 27 are fixed
by 18 core units, eight empty links and the pair-color unit. Internal
moving edges are constants. There are no auxiliary variables, degree
equations, signature quotas, selected external neighborhoods or ordering
constraints in this model.

For all 962,598 five-sets, the generator retains both monochromatic
prohibitions, simplifies the fixed colors, and deduplicates equal
clauses. Explicit units retain the 27 fixed primary values. In the blue
case it adds the eight proved binary clauses forbidding a common blue
fixed neighbor of the empty pair. The red case receives no such clauses.
The [earlier local proof](../ramsey_r55_order3_eleven_core194_pair)
is rederived here; an exhaustive sixteen-signature certificate is
reconstructed by the new checker.

| Pair color | Variables | Clauses | Formula bytes | SHA256 |
|---|---:|---:|---:|---|
| Blue | 320 | 366,069 | 14,883,777 | `f3314485280b2080f3459774b944e010beeb175788673d53703d60cba091e84c` |
| Red | 320 | 364,095 | 14,841,387 | `2aa575e6b988d788f57f98abaa3728518517adc02c795ef5f75458c459e85a72` |

The possible red/blue five-set counts after fixed-color substitution
are 454,199 / 655,371 in the blue-pair case and 457,300 / 646,149 in
the red-pair case. These collapse to 366,034 and 364,068 distinct Ramsey
clauses, respectively, before adding the 27 units and eight blue-case
consequences. These are clause counts, not counts of realizable graphs.

The [accepted two-empty-signature theorem](../ramsey_r55_order3_eleven_core194_multiplicity_review1)
ensures that any full Core194 extension contains a selectable empty
pair. Since the new encoding imposes no row order, any such pair can
be moved to vertices 33,34 by permuting only fixed vertices. A direct
refutation of one color would therefore forbid **every** empty pair
of that color. Both refutations would exclude all Core194 extensions.
The color cases are disjoint for a labeled distinguished pair; their
unlabeled graph families can overlap if a graph has empty pairs of both
colors. The older ordered-pair formulas do not have this latter scope
without an additional relabeling proof.

## Independent reconstruction and controls

`generate.py` uses explicit arithmetic orbit indices and all five-sets.
`check.py` imports no producer. It recovers variables by traversing the
action on all 903 physical pairs and uses a separate literal adjacency
mask representation of the twelve-vertex core. For each color it builds
the graph of edges still able to take that color, enumerates its possible
K5s by bit-intersection recursion, and recovers the forbidden free-edge
clauses. Every clause is compared, including the units and consequences,
with exact header, variable range, ordering, uniqueness and EOF checks.

`controls.py` rejects 16 corrupted full formulas, three malformed or
non-Ramsey small graphs, and five malformed primary models. It checks
all 903 decoded pair colors for a prescribed Boolean assignment against
physical orbit traversal. Both copied local fixtures pass literal
five-set enumeration, totaling 5,005 five-sets. Their detailed local
scope and previous checks remain in the earlier pair package.
Sixteen signatures of a putative common blue fixed neighbor each have
a literal monochromatic K5 obstruction, constructed by the new checker.
Normal and optimized Python must give identical reports.

The decoder requires all 320 primary values and a model terminator,
checks every formula clause, and writes a compact sorted edge list.
Any target is then checked separately against all 962,598 five-sets,
the fixed colors and the action. SAT solver acceptance alone is insufficient.
Every UNSAT result requires full DRAT replay including RAT steps, then
another replay against a fresh independently checked formula.

## Reproduction

CPython 3.11.2 and its standard library suffice for generation and
checking. From the repository root, create a fresh external work
directory, then generate and independently reconstruct either case:

```bash
mkdir -p /scratch/FRESH-r55-direct
python3 -B ramsey_r55_order3_eleven_core194_direct/generate.py \
  --color blue --output /scratch/FRESH-r55-direct/blue.cnf
python3 -B ramsey_r55_order3_eleven_core194_direct/check.py \
  --color blue --formula /scratch/FRESH-r55-direct/blue.cnf \
  --report /scratch/FRESH-r55-direct/blue-check.json
```

Repeat with `red`. Then `controls.py --formulas EXTERNAL --work
FRESH_CONTROLS --report FRESH_REPORT` checks both formulas and all controls.
The full runner automatically repeats these controls under normal and
optimized Python before any solver call. Set R55_KISSAT and R55_DRAT
to the pinned executables:

```bash
python3 -B ramsey_r55_order3_eleven_core194_direct/run.py \
  --work /scratch/FRESH-r55-direct/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 60 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_core194_direct/verify.py \
  --source-work /scratch/FRESH-r55-direct/full \
  --work /scratch/FRESH-r55-direct/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
```

Kissat 4.0.4 source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`,
binary SHA256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`;
drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`,
binary SHA256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
The new Python formulation needs no C++ compiler; these external solvers
retain their build/runtime trust boundaries.

The runner freezes sixteen source identities, including PROOF.md,
before production. Nine belong to the new executable/proof/fixture
package and seven identify prerequisite evidence or boundary documents.
It imports no historical executable module. Two workers each receive
one 60-second solve; proof replay caps are 300 seconds. A `STOP` file
prevents unstarted cases; active bounded solves and replays finish.
`--resume` requires the exact source/tool/resource contract and retains
completed UNKNOWN cases without extending their caps. Partial traces
are not saved solver states. Formulas, traces, logs and executables
stay outside Git; compact source and reports are public.

## Dependencies and trust

The direct formulation equivalence for a distinguished pair uses only
its displayed graph definitions and elementary clique arguments. Its
application to every full Core194 extension imports the accepted z>=2
theorem, source `bd3c79a22191277b80d8c5eb2ed69584dae83da3`, reviewed in
`720d947164e053768ea0a9d97056e483ab8a24df` at Discovery Net height 3164.
That accepted theorem retains its own inherited reduction and proof
dependencies. Their old UNKNOWN runs are not premises. The statement
that the entire residual frontier has 17 classes / 9,153 labels imports
the previous core catalog and whole-exclusion review boundaries.

During this pass the preceding local blue-pair theorem and old exact
child tails also received an [accepted independent review](../ramsey_r55_order3_eleven_core194_pair_review1),
source `d59a572af02f942157d741ce1ae4be948e3b1e2e`. Its author independently
reconstructed the core and all sixteen signature obstructions, both
fixtures, all 131,072 guarded fixed-incidence patterns and both complete
old child formulas. The old base semantics remain inherited in that
review. No old UNKNOWN run was repeated. This review does not cover
the new direct formulation.

The new formulation, relabeling proof and checks await independent
review. Author-written independent implementations are not independent
peer review or formalization. Exact Python, solver/checker builds,
hardware, hashes for identity and unformalized reasoning remain trusted.
No performance or historical-priority claim is made.

## Observed decision and stopping point

Both runs exited 0 with explicit `s UNKNOWN`: blue after 60.230487 seconds
and red after 60.214729 seconds. Full production and preparation took
180.889378 seconds, with largest child maximum RSS 323,480 KiB. Fresh
complete reconstruction and repeated controls took 120.922062 seconds.
It repeated no solver call. All sixteen frozen identities still match.
No full proof replay occurred; the 300-second replay caps were unused.

| Pair | Partial trace bytes | SHA256 |
|---|---:|---|
| Blue | 63,917,566 | `1844d66c4886cf23a2de374e71025fb3f75d290964d665799aa8b618bfff61af` |
| Red | 60,537,873 | `241a70b9dfc8cd2cc1a214c5c18b5338c670118776fe397e35700370a1ee97c8` |

These partial traces are neither refutations nor solver restart states.
The measured time limits are not performance guarantees. The new compact
records are [result.json](result.json), [verification.json](verification.json),
[controls.json](controls.json) and [boundary.json](boundary.json).
Both pair colors and all 17 full classes remain open, at the stated
inherited scope. The direct formulas provide a separate complete backend,
not a new lower bound or evidence that either case is feasible.

The incremental graph scan from height 3167 through 3181 found the external
M214 selector-interface semantic review at 3170. It was read as a distinct
undecided handoff, without another audit or solver test. The final relevant
refresh through 3183 found the accepted old pair review at 3182,
`bafkreieftyw4i3dx2ihp66nbnmoia373qvj6yawcvzn6f7cexwdkbmolvi`.
Its report and full README were read and its manifest checked. The
teammate's joint three-outside realization remains a separate relaxation
with 588 monochromatic K5s, not a target or a premise here.

This milestone is complete, with no background process. Neither a longer
solve nor another direct core case has started. The next useful structural
question is a complete classification of how the distinguished empty pair
attaches to the seven blue moving triangles and eight other fixed vertices,
using the exact common-blue neighborhood and valid degree window. Any
resulting count cover and normalization need a new proof and independent
check before further full search. That phase is unstarted. The six finished
one-empty cases, old symmetry exclusions and M214 semantics comparison
remain closed or parked at their recorded scopes.
