# Core194: six rigid one-empty patterns and a complete full split

**Every hypothetical Core194 extension has at least two empty fixed
signatures.** The six complete one-empty cases are all refuted, with
full DRAT proofs replayed twice after fresh reconstruction. The remaining
multiple-empty case returned **UNKNOWN at20 seconds**. Core194's whole
extension remains open; there is no target graph or Ramsey lower-bound
improvement.

This package derives the six necessary one-empty signature patterns and
closes them in the complete43-vertex extension. The other16 full cores
are untested. The overall four-versus-seven boundary remains **17 classes /
9,153 labeled cores**, with cumulative whole exclusions180/197 classes /
106,390 of115,543 labels. Those counts retain their inherited review
boundaries. Core194's81 labels remain in the unresolved set with the new
z>=2 requirement.

## Structural reduction

Use the order-three action `1^10 3^11`, with four red and seven blue
moving triangles and red core word `100110110110110100`. Let z count
empty fixed signatures, x_i singleton signatures {i}, and y_ij pair
signatures {i,j}. Core194 has all four intrinsic anchors, so
`z+x_i>=2`. The proved sharp inequalities give `x_i+y_ij<=2`.
Literal red K4s in all four complementary nine-vertex cores rule out
signatures of size at least three.

If z=1, all x_i are 1 or2 and all y_ij are 0 or1. If k singleton types
occur twice, the pair count is 5-k, but only `C(4-k,2)` pair types can
occur. The inequality fails for k=1,2,3,4. Therefore every singleton
occurs once and precisely one pair type is missing. The six possibilities
are necessary multisets, not asserted full extensions.

The [proof](PROOF.md) supplies the hand argument and explains how the
existing full-row order places each signature. The compact
[certificate](certificate.json) contains four literal K4 witnesses and
all six sorted prefix lists. The independent auditor enumerates all
48,620 weak compositions of nine nonempty vertices among the ten possible
singleton/pair types, recovering exactly those six lists.

## Seven disjoint full-extension cases

The six `one_ij` cases mean z=1 with pair signature {i,j} absent. They
assign the four red-core incidence bits of fixed vertices34,...,42,
using 36 primary units; the first empty prefix is already in the base.
Every fixed edge and every blue-cycle attachment remains unspecified by
the new tail. The `multiple` case means z>=2 and adds only the four
negative units -222,-223,-224,-225 for the second empty prefix.

This is a complete disjoint cover of one full Core194 class, representing
81 labeled red cores. Its six one-empty subdivisions must not be counted
as six independent whole-core classes. Only refuting all six establishes
z>=2; a whole-Core194 exclusion requires all seven refutations.

The input is the entire [guarded Core194 base](../ramsey_r55_order3_eleven_core194_full),
with all 350 universal guarded attachment clauses retained. Its identity
is 24,968,396 bytes, SHA256
`f7f9eab7a28f32f56bebd54349db8a0e06010274bb16df9f90cbbb9b982216bf`.
It has 34,320 variables /617,932 clauses. The one-empty children have
617,968 clauses /24,968,634 bytes; the multiple-empty child has
617,936 clauses /24,968,424 bytes. All keep 34,320 variables.

No maximal-attachment assumption, fixed neighborhood, selected degree
profile, additional automorphism or new normalizer is imposed. The
previous guarded-base UNKNOWN result is not used as mathematical evidence.

## Verification and reproduction

An isolated process reconstructs the complete earlier preparation and
guarded base and compares both with the published records. Only Core194
is rebuilt and tested. The new auditor imports no producer, recovers
320 primary meanings from physical pair orbits, checks every inherited
base byte, child unit, header and EOF. It checks the literal K4 witnesses,
the full count classification, all 2,048 full rows for prefix order, and
all sixteen second prefixes for the zero/nonzero partition.

Twenty-one malformed certificates, cases or formulas must be rejected
under normal and optimized Python, with matching reports. The run freezes
122 source identities, including PROOF.md, before any solver call.
Two workers test the seven cases, each with a 20-second Kissat cap and a
300-second full DRAT cap. Any refutation must pass the complete checker,
including RAT steps, and pass again after fresh reconstruction of the
whole base and all seven formulas. UNKNOWN excludes nothing. A SAT target
must decode to a compact edge list and pass literal five-set checking.

Use CPython3.11.2 and the standard library. Inherited preparation uses
GCC12.2.0 (Debian12.2.0-14+deb12u1). Pinned tools:

* Kissat4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`,
  binary SHA256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
* drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`,
  binary SHA256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

Set R55_KISSAT and R55_DRAT to those executable paths. From the repository
root, using fresh work directories outside the repository:

```bash
python3 -B ramsey_r55_order3_eleven_core194_multiplicity/run.py \
  --work /scratch/r55-c194-multiplicity/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 20 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_core194_multiplicity/verify.py \
  --source-work /scratch/r55-c194-multiplicity/full \
  --work /scratch/r55-c194-multiplicity/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_core194_multiplicity/summarize.py \
  --source-work /scratch/r55-c194-multiplicity/full \
  --verification-work /scratch/r55-c194-multiplicity/verification \
  --output /scratch/r55-c194-multiplicity/boundary.json
```

`--resume` requires the identical source/tool/resource contract and
case/base/formula/trace identities. It keeps completed UNKNOWN results
without rerunning them at a longer cap. STOP prevents unstarted cases,
allowing active solve/replay units to finish. Large formulas, traces,
logs and binaries stay outside Git. Hashes identify omitted evidence
but do not replace a proof; public source regenerates the formulas and
permits proof-producing runs. Partial UNKNOWN traces are neither
refutations nor resumable solver states.

## Checked outcome

All six one-empty proofs passed both full DRAT replays, including the
RAT core lemmas shown below. The six traces total **81,989,180 bytes**
and remain outside Git. Their exact identities and all formula hashes
are in [result.json](result.json); the second checks are in
[verification.json](verification.json). Hashes do not replace omitted
proof traces; the reproduction commands regenerate them.

| Case | Result | Solve seconds | Proof bytes | RAT core lemmas |
|---|---|---:|---:|---:|
| multiple | UNKNOWN | 20.109337 | — | — |
| one_01 | UNSAT, twice checked | 1.561873 | 13,150,456 | 117 |
| one_02 | UNSAT, twice checked | 1.617202 | 14,908,671 | 164 |
| one_03 | UNSAT, twice checked | 1.712484 | 13,275,456 | 190 |
| one_12 | UNSAT, twice checked | 1.713458 | 13,651,948 | 77 |
| one_13 | UNSAT, twice checked | 1.612368 | 13,512,414 | 98 |
| one_23 | UNSAT, twice checked | 1.613357 | 13,490,235 | 73 |

Production with complete preparation took125.153174 seconds, with largest
child maximum RSS261,536 KiB. Fresh verification took102.399981 seconds.
All122 frozen source identities match. Normal and optimized control reports
agree; [controls.json](controls.json) records the21 rejected corruptions.
[boundary.json](boundary.json) distinguishes the closed one-empty branch
from the still-open whole Core194 class. Timing is an observed property
of this bounded run, not a runtime theorem.

The multiple-empty formula has SHA256
`214cbdad727ec3f48e97e62246134b341719277981119bd6b89baa5475b2dbb4`.
Its solver exited0 with explicit `s UNKNOWN`. The report stores its
25,449,847-byte partial trace under the inherited field `proof`, SHA256
`0d9504e60ea6829b03e662b9d39eead520a474e8b2c8d16ef5f1126393d0cf35`.
That trace is neither a refutation nor saved solver state and has no
completed proof replay. UNKNOWN is not evidence of satisfiability.

No background process remains. This complete seven-case milestone stops
here. A next distinct full-extension step is a complete color split on
the edge between the first two empty fixed vertices, retaining the full
multiple-empty formula. Neither that split nor a longer solver run is
started here. Do not reopen any of the six finished one-empty cases.

## Dependencies and scope

The [parent](../ramsey_r55_order3_eleven_cycle_obstruction),
[core cover](../ramsey_r55_order3_eleven_four_core),
[intrinsic anchors](../ramsey_r55_order3_eleven_anchor_propagation),
[forced-empty theorem](../ramsey_r55_order3_eleven_noempty_rigidity), and
[maximal Core194 exclusion](../ramsey_r55_order3_eleven_core194_maximal_review1)
have accepted independent reviews at their stated scopes. The sharp
pair inequalities and their base application are in
[empty-signature propagation](../ramsey_r55_order3_eleven_empty_propagation).
The guarded full encoding has author checking. This new six-pattern
rigidity, seven-case bridge and computational outcomes await independent
review. Cumulative exclusions retain the older empty-signature-specific
review boundary.

Other trust is the imported R(4,5)=25 degree theorem, unformalized
reductions, exact source/runtime/compiler/hardware, SHA256 and the full
DRAT checker. Internal reconstruction is not peer review or formalization.
The sixteen other residual full cores, the three-versus-eight branch,
other moving counts and the teammate's non-symmetric lane are outside
this test. The earlier closed multiplicity cases131,139,162,173 are
historical method context and are not reopened.

The initial relevant graph refresh through3147 and final refresh through3155
found no new affecting symmetry contribution. The final repository refresh
found the teammate's [six-way footprint obstruction](../ramsey_r55_critical_path_six_support),
source `e5ed88bed9ae7e8aeadf3365d9feedd593e35444`. Its README was read;
its computation was not replayed or imported. It excludes six specified
footprints over a different literal eleven-vertex core, although every
five admit a local completion. It does not exclude any symmetry class.
The paired researchers retain their separate scopes.
