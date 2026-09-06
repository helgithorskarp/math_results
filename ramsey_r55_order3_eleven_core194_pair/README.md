# Core194 empty-pair lemma and complete pair-color test

For a blue edge between two empty-signature vertices of Core194,
**there are no common blue fixed neighbors**. In the full eleven-cycle
action, their common blue neighborhood is exactly the twelve red-core
vertices. This local statement has a solver-free certificate and small
validation graphs. Both complete red/blue pair tests returned **UNKNOWN
at20 seconds**; fresh reconstruction passed. No further full branch or
whole core is excluded. No target graph or Ramsey lower-bound improvement
is asserted.

The frontier remains **17 full classes /9,153 labeled cores**, with
cumulative whole exclusions180/197 classes /106,390 of115,543 labels.
Core194's81 labels remain open with the preceding z>=2 requirement.
Those counts retain their historical review boundaries.

## Local lemma, exact scope and witnesses

The red core comprises four red triangles C0,...,C3, with cross word
`100110110110110100` in pair order01,02,03,12,13,23. Fixed vertices are
uniform to each triangle; an empty signature means blue adjacency to
all twelve core vertices. If u,v form a blue empty pair and a third
fixed f is blue to both, then f cannot miss two red triangles: a blue
cross-edge between those triangles completes a blue K5 with u,v,f.
Thus f would need a signature of size at least three. But each three-
triangle subcore of Core194 has a red K4, so that signature completes
a red K5. This contradiction proves the zero bound.

The [proof](PROOF.md) supplies the exact witnesses and transfer. The
[certificate](certificate.json) lists a monochromatic five-set for
each of the sixteen possible signatures of f: eleven blue obstructions
for signatures of size at most two and five red obstructions for larger
signatures. This local lemma requires no degree bound or global order43.

The [blue-pair14 fixture](blue_pair14.edges) has42 red edges and no
monochromatic K5, attaining zero common blue fixed neighbors. The
[red-pair15 fixture](red_pair15.edges) has43 red edges and no monochromatic
K5 but one common blue fixed neighbor, showing that the blue-edge
hypothesis is essential. Both retain the order-three action on the
four core triangles. They are small validation graphs, not targets.

Each edge list starts with the number of vertices and then lists every
red edge as an increasing pair; every other pair is blue. The standalone
auditor imports no producer or solver. It checks the exact core, empty
signatures, pair colors, action invariance, common neighbors, all5,005
five-sets of the two fixtures, and160 literal edges of the sixteen
obstruction witnesses.

The seven internally blue moving triangles in a full extension cannot
be blue to both endpoints of a blue pair: each would complete a blue
K5. These clauses already occur in the full parent. Combined with the
zero-common-fixed lemma, they leave precisely the twelve core vertices
as common blue neighbors. This is a proved consequence, not a selected
external neighborhood assumption.

## Complete full-color split

The preceding [multiplicity closure](../ramsey_r55_order3_eleven_core194_multiplicity)
requires at least two empty fixed signatures. Existing full-row ordering
makes vertices33,34 empty. Their edge has primary index166. The red case
appends only166; the blue case appends -166 and the eight binary clauses
`x_(33,f) OR x_(34,f)` for f=35,...,42, encoding the new lemma. Their
primary pairs are(167,175),...,(174,182). The blue-branch clauses are not
imposed on the red branch, and no new ordering is used.

The two color alternatives form a complete disjoint split of the
remaining full Core194 class, representing81 labeled cores. The local
lemma applies to every blue empty pair. A computational restriction on
the first ordered pair must not be generalized to all empty-pair colors
without an additional proof. Refuting both full cases would exclude
Core194; one refutation would restrict only the surviving normalized
first-pair branch.

The entire multiple-empty base has34,320 variables /617,936 clauses,
24,968,424 bytes, SHA256
`214cbdad727ec3f48e97e62246134b341719277981119bd6b89baa5475b2dbb4`.
It retains all parent clauses, core units, intrinsic anchors, sharp pair
cuts, both empty prefixes and350 guarded attachment clauses. Every body
byte is preserved. No new variable, normalizer or degree profile is added.

| Pair color | Clauses | Bytes | Complete formula SHA256 |
|---|---:|---:|---|
| Blue | 617,945 | 24,968,511 | `21b9a5e9d4b4ddb9e91388abf6bc45d87488f356adbcbc70fb60d752ad5f13e1` |
| Red | 617,937 | 24,968,430 | `941df55fb7a26c64b1e72dfdff819d3cad15409a5eb83521a57ac2e353562224` |

## Reproduction and checking

For the local lemma and small witnesses alone, CPython3.11.2 and the
standard library suffice. From the repository root, using a fresh
external output path:

```bash
python3 -B ramsey_r55_order3_eleven_core194_pair/audit.py --local \
  --certificate ramsey_r55_order3_eleven_core194_pair/certificate.json \
  --fixtures ramsey_r55_order3_eleven_core194_pair \
  --report /scratch/r55-c194-pair-local.json
cmp /scratch/r55-c194-pair-local.json \
  ramsey_r55_order3_eleven_core194_pair/local_verification.json
```

`cube.py --work EXTERNAL` regenerates the local certificate and both
edge lists deterministically without running a solver. Full preparation
reconstructs all inherited preparation and the multiple formula in an
isolated namespace, without rerunning old solver cases. The separate
auditor derives320 primary meanings from physical43-vertex pair orbits,
checks every base byte, new clause, header and EOF, and locates all seven
moving-cycle clauses already present in the base.

Truth tables inspect all131,072 assignments of the pair edge and the
sixteen other fixed incidences. All65,536 red-pair patterns are retained,
and exactly3^8=6,561 blue-pair patterns satisfy the new bound. Twenty-two
malformed local certificates, cases, fixtures or formulas must be
rejected. Normal and optimized Python reports agree. The run freezes
132 source identities, including PROOF.md, before any solver call.

The full computation uses GCC12.2.0 (Debian12.2.0-14+deb12u1) in inherited
preparation and these pinned executables:

* Kissat4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`,
  binary SHA256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
* drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`,
  binary SHA256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

Set R55_KISSAT and R55_DRAT to those executable paths. From the repository
root, using fresh work directories outside Git:

```bash
python3 -B ramsey_r55_order3_eleven_core194_pair/run.py \
  --work /scratch/r55-c194-pair/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 20 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_core194_pair/verify.py \
  --source-work /scratch/r55-c194-pair/full \
  --work /scratch/r55-c194-pair/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_core194_pair/summarize.py \
  --source-work /scratch/r55-c194-pair/full \
  --verification-work /scratch/r55-c194-pair/verification \
  --output /scratch/r55-c194-pair/boundary.json
```

Two workers run one20-second solve per color. An UNSAT outcome must pass
full DRAT checking including RAT steps, then pass again against a fresh
complete formula. A SAT target must decode to a compact edge list and
pass literal five-set checking. UNKNOWN is inconclusive; its partial
trace is neither a refutation nor resumable solver state. Time-limited
outcomes may vary between machines.

`--resume` requires the same source/tool/resource contract and saved
case/base/formula/trace identities, and retains completed UNKNOWN cases
without extending the cap. STOP prevents unstarted cases while active
solve/replay units finish. Large formulas, traces, logs and binaries
remain outside Git. Hashes identify omitted evidence but do not replace
a checked proof.

## Observed full outcomes and stopping point

Both solver runs exited0 with explicit `s UNKNOWN`: blue after20.149136
seconds and red after20.116356 seconds. Production with complete preparation
took119.192895 seconds, with largest child maximum RSS261,564 KiB.
Fresh complete reconstruction and control repetition took126.807813 seconds.
It rebuilt both full formulas and matched the stored inputs/outcomes,
without rerunning the solvers. All132 frozen source identities match.
No full proof replay was performed; the configured300-second replay cap
was unused. Timing is an observation of this bounded run, not a theorem.

The report schema calls each partial trace identity `proof`. These are
not refutations or resumable solver states:

| Pair | Partial trace bytes | SHA256 |
|---|---:|---|
| Blue | 24,579,914 | `daacbb42c582fdc0677ec46a4c7ae672471348d5c91d81a11e7a9ed389b61397` |
| Red | 24,890,496 | `08ef393f2bc08c851255290c405ad2d081dfbfc00fcf325c24db821c5139d1b4` |

Exact records are in [result.json](result.json),
[verification.json](verification.json), [controls.json](controls.json),
[local_verification.json](local_verification.json), and
[boundary.json](boundary.json). The last retains both pair-color branches
and all seventeen full classes. The local proof is independently checkable
by literal finite inspection; it does not rely on these UNKNOWN runs.

This coherent milestone is complete. No background process remains.
Do not rerun the same caps or reopen the six finished one-empty cases.
A next distinct direction is a direct encoding of the complete pair cases
using only primary edge-orbit variables, with literal Ramsey clauses and
the proved pair consequences. Its completeness and decoding would require
fresh independent checks. That encoding and any further solve are unstarted.

## Dependencies and claim scope

The local lemma and small fixtures can be checked without the historical
full search chain. Full exclusions additionally import the preceding
one-empty closure and guarded base. During this pass the
[one-empty closure received independent acceptance](../ramsey_r55_order3_eleven_core194_multiplicity_review1),
source `720d947164e053768ea0a9d97056e483ab8a24df`, graph
`bafkreid2tpcg4oo36dyn43tjhr7cjoo2leknbrdglzh53by4kdnx2tdcke`, height3164.
The reviewer reconstructed the six-pattern classification and all seven
formulas, regenerated the six byte-identical proofs with a different
Kissat build, and fully replayed all RAT steps. This accepts z>=2, not
any further Core194 exclusion. The guarded full encoding retains its
stated inherited trust boundaries. The parent, core cover, intrinsic
anchors, forced-empty theorem and maximal Core194 exclusion also have
accepted independent reviews at their stated scopes. New local and full claims await independent review. Cumulative
counts retain older empty-signature-specific review boundaries.

The [earlier three-versus-eight empty-pair argument](../ramsey_r55_order3_eleven_empty_pair) is method context;
its weaker fixed-neighbor bound is not copied into this four-triangle
core. The new proof establishes the exact zero bound and its blue guard
directly. Other trust comprises imported R(4,5)=25 in the full parent,
unformalized reductions, exact source/runtime/compiler/hardware, SHA256
and any full DRAT replay. Internal checking is not peer review or formalization.

The sixteen other residual four-versus-seven cores, the three-versus-eight
branch, other moving counts and the teammate's non-symmetric lane are
outside this test. The six completed one-empty Core194 cases remain
closed and are not rerun.

The initial incremental graph refresh through3163 located the teammate's
six-footprint contribution at3156, already known from its repository source:
`bafkreihibj5pskqwplkygs4fqr47avsmxw2vsbtlgeflhznlio47uuej7y`.
Its body was read; it concerns a different literal core and is not imported.
The final relevant refresh through3167 found the accepted multiplicity
review above and no conflicting symmetry result. The paired research lanes
remain distinct.
