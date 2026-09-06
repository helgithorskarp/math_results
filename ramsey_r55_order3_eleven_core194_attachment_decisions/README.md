# Five complete Core194 blue-pair attachment types are excluded

**Every blue empty fixed pair in a full Core194 extension is red to
all vertices of at least four of the seven internally blue moving
triangles.** Five complete attachment types are now refuted. Four
remain unresolved, so neither the blue-pair family nor Core194 is
excluded. No target graph or Ramsey-bound improvement is claimed.

The normalized counts are (a,b,c), for moving triangles red to both
pair ends, red only to the first, and red only to the second. The
four survivors are **(4,1,2),(5,0,2),(5,1,1),(6,0,1)**. Thus a>=4;
if a=4, the two remaining contact counts must be1 and2. This applies
to any distinguished blue empty pair under the prior proved relabelings.
It does not assert that a blue empty pair exists in every extension.

The nine-type cover had119 candidate joint degree profiles. The five
full type exclusions remove70; the four remaining types contain49,
with27,10,9,3 profiles respectively. They represent1,302,000 labeled
star assignments in that degree relaxation, not realizable graphs.
The [boundary record](boundary.json) includes the three profiles of
(6,0,1) for a later bounded refinement. None has been searched separately.

## Complete results

| Moving type | Verdict | Solve seconds | First full replay seconds |
|---|---|---:|---:|
| (1, 3, 3) | UNSAT, checked twice | 3.339164 | 1.419668 |
| (2, 2, 3) | UNSAT, checked twice | 7.135471 | 5.384331 |
| (3, 1, 3) | UNSAT, checked twice | 8.678912 | 5.582631 |
| (3, 2, 2) | UNSAT, checked twice | 62.768813 | 47.433522 |
| (4, 0, 3) | UNSAT, checked twice | 8.524035 | 6.033780 |
| (4, 1, 2) | UNKNOWN at90seconds | 90.299979 | — |
| (5, 0, 2) | UNKNOWN at90seconds | 90.278133 | — |
| (5, 1, 1) | UNKNOWN at90seconds | 90.341652 | — |
| (6, 0, 1) | UNKNOWN at90seconds | 90.374034 | — |

Full production took332.992066seconds. Fresh verification under optimized
Python took95.655537seconds and replayed all five complete refutations.
There were nine solver calls and ten successful full DRAT replays in
total. The first proof has four RAT lemmas in its checked core; the
other four have zero. All checks use full DRAT, including RAT.

The recorded largest child maximum RSS is244,320KiB; it excludes the
parent's in-process base generation. The five complete traces total
91,368,801bytes. Including four partial UNKNOWN traces gives456,174,841
bytes. These files remain outside Git; hashes and exact outcome records
are in [result.json](result.json) and [verification.json](verification.json).
Hashes do not replace proof replay. The reproduction command regenerates
both complete formulas and traces; time-limited UNKNOWN traces may differ
with scheduling. No unchecked terminal claim is used.

This package runs the nine complete full-extension cases from the
[attachment cover](../ramsey_r55_order3_eleven_core194_attachments).
It retains all320 primary variables and366,083 clauses of each case.
Every unspecified graph edge and other fixed-vertex incidence remains
free. No local relaxation or new symmetry restriction is substituted.

The [scope proof](PROOF.md) explains exactly what an individual
refutation would exclude. Even a refutation of all nine BLUE-pair cases
would leave the RED-pair branch open. The current milestone does not
by itself exclude Core194 or improve the Ramsey bound.

## Reproduction and evidence

From the repository root, with CPython3.11.2 and its standard library:

```bash
python3 -B ramsey_r55_order3_eleven_core194_attachment_decisions/controls.py \
  --work /scratch/FRESH-r55-nine-controls \
  --drat-trim /absolute/path/to/drat-trim
python3 -B ramsey_r55_order3_eleven_core194_attachment_decisions/run.py \
  --work /scratch/FRESH-r55-nine-full \
  --kissat /absolute/path/to/kissat \
  --drat-trim /absolute/path/to/drat-trim \
  --solve-seconds 90 --replay-seconds 600
python3 -B -O ramsey_r55_order3_eleven_core194_attachment_decisions/verify.py \
  --source-work /scratch/FRESH-r55-nine-full \
  --work /scratch/FRESH-r55-nine-verification \
  --drat-trim /absolute/path/to/drat-trim --replay-seconds 600
```

The complete attachment preparation is freshly reconstructed and compared
entry by entry to its published expected record. This includes the
119-profile cover audit, normal/optimized controls, full direct BLUE
base reconstruction, and exact body/tail checks of all nine children.
Nineteen source identities are frozen, including this package's scope
proof, all executed Python sources, and the imported attachment result.

Two workers each invoke Kissat once per case with a90second solver cap.
The outer process timeout is150seconds. Each actual UNSAT must pass
full DRAT, including RAT, with a600second checker cap and660second outer
timeout. Fresh verification reconstructs all complete input formulas
and replays every refutation again. It does not repeat UNKNOWN solves.
All solver output, traces and complete CNFs remain outside Git. Partial
traces from UNKNOWN are neither refutations nor saved solver states.

A SAT outcome must pass full primary-model clause evaluation and the
direct package's literal43-vertex graph checker. A target claim would
include its compact edge list. Solver return codes must agree with one
exact status line; seven malformed transcript controls are rejected.
The checker also rejects a false empty-clause proof on a satisfiable
formula. Controls pass under normal and optimized Python. The inherited
formula and decoder controls retain their documented scopes.

Work directories preserve each finished case atomically. `--resume`
requires the same source/resource contract and exact evidence identities;
it retains completed UNKNOWN calls and rechecks complete refutations.
A saved pending refutation is checked before any new solver call for
that case. Creating `WORK/STOP` prevents queued cases from starting,
while in-progress bounded jobs finish. Partial completion is explicit.
A changed cap or encoding needs a separate work directory and research
phase. Runtime measurements are observations, not reproducibility promises.

Kissat4.0.4 source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, binary SHA256
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
DRAT-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
Both executable identities were checked before the production run.

The direct formula and pair lemma have accepted independent reviews.
The attachment cover remains an inherited proof boundary until separately
reviewed. Author-written different implementations and two proof replays
are not independent peer review or formalization. Trust includes the
ordinary finite coverage argument, its importedR(4,5)=25 degree window,
exact Python/hardware, the full DRAT checker and file identity checks.
No historical-priority claim is made.

## Shared context

The start-of-pass incremental refresh through3209 found the teammate's
[overlapping-neighborhood degree obstruction](../ramsey_r55_overlapping_neighborhood_degree_gap),
source `2fdb8cef31597170f94e9eae9f43859d9c7a8a0c`, at height3208.
Its full source README and graph body were read. It excludes two chosen
local completion tuples under the stated target degrees; neither H
family nor a degree profile is excluded. It is a distinct nonsymmetric
gluing result and is not imported or duplicated by these symmetry cases.
The six accepted one-empty Core194 cases and earlier symmetry closures
remain closed. No M214 semantic audit or teammate graph search is rerun.

The final incremental refresh through3217 found external height3210's
four-connectivity theorem for dense22-vertex(4,5) neighborhoods, source
`146f7d64b3f1d2446026e5324e84d4fe6a0c71eb`. Its full graph body was read,
not its code replayed or its theorem imported here. The exact attachment
and direct-formula dependency feedback at3217 contained no affecting
objection or new review of the attachment cover. The teammate's earlier
citation is not review. No overlapping symmetry decision was found.

The global four-versus-seven frontier stays at17 full classes/9,153
labels, including Core194's81labels. Prior cumulative180/197classes and
106,390of115,543labels retain their inherited scopes. Red-pair direct
UNKNOWN60 and all earlier accepted one-empty exclusions are preserved.
No background job remains after verification. The next bounded direction
is to refine(6,0,1) into its three certified fixed-attachment profiles,
with complete full formulas and checked terminal evidence. This new
phase, longer old caps, the other three residual types and other cores
are unstarted. The pass yields at the completed nine-case milestone.
