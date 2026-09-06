# Four guarded full extensions: bounded unresolved checkpoint

**Cores 124,155,168,180 remain unresolved.** Each complete 43-vertex formula,
strengthened by 350 guarded attachment clauses, returned explicit UNKNOWN
at the 20-second Kissat cap. Fresh reconstruction verifies the inputs and
encoding, not an exclusion or satisfiability verdict. No target graph or
Ramsey lower-bound improvement is established.

The substantive reduction is the universal scope of the accepted local
24-vertex obstructions: **every fixed vertex blue to the four red moving
triangles is blue to at most three of the seven blue moving triangles**.
The [proof](PROOF.md) keeps the canonical red core pointwise and forgets
all fixed vertices in the local restriction. It therefore applies beyond
the first normalized fixed row. No full fixed-row relabeling is assumed.
An independent representation audit checks all ten fixed choices times
35 selected blue-cycle sets. This new universal transfer has author
checking and awaits independent review.

This completes the next step identified in the preceding
[guarded Core194 checkpoint](../ramsey_r55_order3_eleven_core194_full).
The four earlier tests used only the first-row bound and were also UNKNOWN.
Core159's whole exclusion is already independently accepted and is not
retested. The separate Core194 test is not repeated either.

The full four-versus-seven boundary stays **17 classes / 9,153 labeled
cores**, with cumulative exclusions 180/197 classes / 106,390 of 115,543
labels, importing the historical reduction chain and its review boundaries:

```text
92,97,118,119,124,155,164,168,180,182,185,186,190,191,192,193,194.
```

## Exact full strengthening

Use action `1^10 3^11`, red moving cycles C0,...,C3 and blue cycles C4,...,C10.
A positive primary L(f,i) is a red incidence from fixed f to moving cycle i,
with index `211+11*(f-33)+i`. For each f=33,...,42 and each four-subset S
of {4,...,10}, append

```
L(f,0) OR L(f,1) OR L(f,2) OR L(f,3) OR OR_(j in S) L(f,j).
```

Nonempty red-core signatures satisfy the tail automatically. An empty
signature activates the at-most-three-blue bound. Other fixed vertices
are not presumed empty. Every unrestricted base clause is retained, with
no new variables, fixed-edge units or normalizers. The tail has 350
positive eight-literal clauses and 11,900 bytes. Each formula changes
from **34,300 variables / 617,482 clauses** to **34,300 / 617,832**.

| Core | Literal red core | Labels | Intrinsic omitted-triangle anchors |
|---|---|---:|---|
| 124 | 000110110011101110 | 324 | 0,1 |
| 155 | 100100110001101110 | 648 | 0,1 |
| 168 | 100100110011110110 | 324 | 1,2 |
| 180 | 100100110101100110 | 648 | 0,1 |

The four cases cover 1,944 labeled red cores. Their unrestricted base
identities are in [cases.json](cases.json), derived from
[empty-signature propagation](../ramsey_r55_order3_eleven_empty_propagation).
The old maximal b=4 children, the local 84-variable formulas and the
earlier first-row-strengthened formulas are explicitly rejected as base
substitutes. Only the full original bases receive this new tail.

| Core | Complete guarded formula bytes | SHA256 |
|---|---:|---|
| 124 | 24,966,036 | `aa2c7467a03f90a5c15928f97de14b7d17478dafa089480f3832d990b8929bb1` |
| 155 | 24,966,037 | `e35006b8036d1ace932971ee003cba122c92d6159c64c81fa4d28699a28edf4f` |
| 168 | 24,966,036 | `f8a75c2ef4ed678b6849e29d4d89e4a232cdf6961556d65b052c774581d70d85` |
| 180 | 24,966,037 | `c33e562b8be68d05b8aeae7052dacd3fa81642f7c3191631703fe2f5db90105b` |

## Recorded computation and verification

The complete inherited parent and preparation are reconstructed in an
isolated namespace and compared entry by entry. Only the four selected
unrestricted bases are rebuilt. The auditor imports no producer, derives
320 primary meanings from literal 43-vertex pair orbits, and checks every
base byte, new clause, header and EOF.

Its 350 physical restriction maps preserve the red core pointwise, the
cyclic action, all 84 local cross-edge orbits and internal colors. Each
map forgets nineteen vertices; no fixed row is relabeled. Truth tables
check all 20,480 row assignments, retaining 1,984 patterns per row:
all 1,920 nonempty signatures and 64 empty signatures. The degree bridge
checks 65,536 moving/fixed incidence patterns, retaining all 17,728
admissible complementary patterns. Sixteen malformed case/formula inputs
are rejected under normal and optimized Python, whose reports agree.

Two workers ran one bounded sweep. The actual solver times for cores
124,155,168,180 were 20.108375, 20.113037, 20.123488 and 20.124994 seconds.
Every run exited 0 with `s UNKNOWN`. Preparation and production took
113.961901 seconds; largest child maximum RSS was 261,436 KiB. The caps
describe this attempt, not a performance theorem.

Fresh verification took 70.624495 seconds. It rebuilds all four complete
bases and guarded formulas, repeats normal/optimized controls, and checks
the saved formula, trace and UNKNOWN identities. It does not rerun the
solver. All **101 transitive source identities** were frozen before
production and remain unchanged.

There are **zero completed proof replays**. The report schema calls each
partial trace identity `proof`, but these UNKNOWN traces are neither
refutations nor saved solver states. Their hashes and sizes are retained
in [result.json](result.json) solely for reproducibility. The configured
300-second full DRAT caps were unused. Neither partial traces nor timing
limits provide an exclusion.

Compact evidence is in [verification.json](verification.json),
[controls.json](controls.json) and [boundary.json](boundary.json).
The latter keeps all thirteen untested full classes and all four tested
UNKNOWN classes. Large CNFs, traces, logs and binaries remain outside Git.

## Reproduction

Use CPython 3.11.2; inherited preparation also uses GCC 12.2.0
(Debian 12.2.0-14+deb12u1). The pinned tools are:

* Kissat 4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`,
  binary SHA256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
* drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`,
  binary SHA256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

Set R55_KISSAT and R55_DRAT to those executable paths. From the repository
root, with fresh work directories outside the repository:

```bash
python3 -B ramsey_r55_order3_eleven_guarded_four/run.py \
  --work /scratch/r55-guarded-four/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 20 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_guarded_four/verify.py \
  --source-work /scratch/r55-guarded-four/full \
  --work /scratch/r55-guarded-four/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_guarded_four/summarize.py \
  --source-work /scratch/r55-guarded-four/full \
  --verification-work /scratch/r55-guarded-four/verification \
  --output /scratch/r55-guarded-four/boundary.json
```

Observed: `open=[124,155,168,180]`, `excluded=[]`, zero proof replays,
17 remaining full classes and 9,153 labels. Time-limited outcomes can
differ across machines. Any later UNSAT outcome requires a complete
full DRAT check, including RAT steps, then a second check against a fresh
formula. Any SAT target requires a compact independently checked edge list.

`--resume` requires the identical source/tool/resource contract and saved
case, base, formula and trace identities. It retains completed UNKNOWN
cases without quietly starting a longer run. A STOP file prevents cases
not yet started while active solve/replay units finish. This sweep is
complete and no background process remains.

## Dependencies, coordination and next boundary

The local refutations have [accepted independent review](../ramsey_r55_order3_eleven_neighborhood24_review1),
source `32775f8609d663966c40c32a4207829421ef9dd9`, graph
`bafkreiddoyofmpkshge4j3a3dwkcxfg4jx2qog2wlxnzksr55mvmaja45a`.
The parent, core cover, intrinsic anchors and forced-empty theorem also
have accepted reviews at their stated scopes. The new universal bridge
and guarded encoding await independent review. Cumulative exclusions
retain the older empty-signature-specific review boundary. The imported
R(4,5)=25 degree theorem, unformalized reductions, exact source,
interpreter/compiler/hardware and SHA256 remain trusted. Internal checking
is not peer review or formalization.

The separately accepted [Core194 maximal-branch review](../ramsey_r55_order3_eleven_core194_maximal_review1)
was new shared evidence at this pass's start: source
`44efce73768f59707025523525b4996c3b82a5c4`, graph
`bafkreicymwtffggjysvwvrri5fxjesmvwx6mdudqi2rlhflap6h4dy5ati`, height 3128.
It resolves that historical review gap, but is not a premise for these
four local obstructions and does not exclude full Core194.

The final relevant refresh through height 3139 found the teammate's
[eleven-vertex triple-footprint cut](../ramsey_r55_critical_path_triple_cut),
source `a08de2fa3a3951ead2669b8878fa7ca498f3efb1`, graph
`bafkreibb5lrqtthudzltjujudbrzl77nlrif4yoe5g7elle765xisutllq`, height 3138.
Its elementary obstruction applies to its literal non-symmetric core.
It is not an exclusion of any of these seventeen symmetry classes and
is not imported into these formulas. Its scope was read; its computation
was not independently replayed here.

This bounded milestone ends with a universal necessary constraint and
four inconclusive full tests. Do not repeat the same cap merely to
generate another checkpoint. A next distinct full-extension direction is
a complete split by empty-signature multiplicity for a selected residual
core, retaining the proved guards and seeking a full checked refutation.
That split, a longer cap, and all other major phases remain unstarted.
The three-versus-eight branch, other moving counts and teammate's
non-symmetric lane are unchanged.
