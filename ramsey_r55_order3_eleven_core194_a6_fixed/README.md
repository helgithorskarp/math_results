# The complete Core194 moving type (6,0,1) is excluded

All three complete fixed-attachment cases are UNSAT, with full DRAT
checked in production and again against freshly reconstructed inputs.
The exhaustive cover therefore excludes the entire (6,0,1) moving type.
Combined with the now independently accepted five earlier exclusions,
a blue empty fixed pair has **four or five** common-red internally blue
moving triangles. Only **(4,1,2), (5,0,2), (5,1,1)** remain.

This removes one moving type and three candidate joint profiles, leaving
46 profiles and 1,298,472 labeled star assignments in the inherited degree
relaxation. These are not graph realizations. The RED-pair branch and all
17 whole classes / 9,153 labels remain open; no target graph or Ramsey-bound
improvement is claimed. [boundary.json](boundary.json) states the exact scope.

## Checked outcomes

| Fixed counts | Solve seconds | First full DRAT seconds | Proof bytes |
|---|---:|---:|---:|
| (0, 5, 3) | 5.407674 | 2.924122 | 7,495,271 |
| (0, 6, 2) | 0.724993 | 1.168186 | 2,236,029 |
| (1, 5, 2) | 2.637537 | 2.222343 | 4,185,567 |

Production took 25.193669 seconds. Fresh optimized verification
took 23.2873 seconds. Three solver calls and six full proof replays
completed; all three proof cores have zero RAT lemmas, although each check
used full DRAT with RAT enabled. No UNKNOWN occurred in this refinement.
The original coarse (6,0,1) UNKNOWN90 record is preserved, not repeated.

The largest recorded child maximum RSS was 244,580 KiB,
excluding the parent generator. The three complete proof traces total
13,916,867 bytes and remain outside Git. Complete formula/proof identities
and check records appear in [result.json](result.json) and
[verification.json](verification.json). Hashes identify files; they do not
replace proof replay. The source reproduces the complete inputs and calls.

This package tests the entire three-case fixed-attachment cover of the
previously unresolved moving type (6,0,1). It keeps the complete
43-vertex extension formula. No other moving type or longer old cap
is tested in this milestone.

For the distinguished BLUE empty fixed pair u,v, six internally blue
moving triangles are red to both endpoints; the seventh is blue to u
and red to v. Every other fixed vertex has contact RR, RB or BR. Their
multiplicities (x,y,z) sum to eight. Since the red endpoint degrees are
26-z and 29-y, the degree upper bound 24 forces z>=2 and y>=5.
The [complete proof](PROOF.md) gives exactly three cases:

| Fixed counts (RR,RB,BR) | Red degrees (u,v) | Labeled fixed words |
|---|---|---:|
| (0,5,3) | (23,24) | 56 |
| (0,6,2) | (24,23) | 28 |
| (1,5,2) | (24,24) | 168 |

The total is 252 of 6,561 no-BB fixed words for the specified normalized
moving assignment. The inherited full star weights are 784, 392, 2352,
totaling 3528. These are star counts, not graph realizations. The first
two degree pairs are not identified by an extra endpoint normalization.

The producer filters the prior 119-profile certificate. A separate
checker enumerates all fixed words using physical red degrees, verifies
all valid sorting maps (223 distinct vertex permutations), and checks
that they commute with C3 and induce bijections on the 320 primary
orbits. All 90 normalized unit meanings are reconstructed from physical
edges. Eight malformed profile certificates are rejected.

Each complete formula contains 320 primary variables and 366,099 clauses:
the entire accepted direct BLUE base and 30 units (14 moving, 16 fixed).
Unmentioned edges and fixed-core incidences remain free. The base is
freshly generated and independently reconstructed; every complete body
byte, physical tail, header and EOF is checked. Seven malformed full
children are rejected, including loss or sign changes of fixed units.

## Reproduction

With CPython 3.11.2 and its standard library, from the repository root:

```bash
python3 -B ramsey_r55_order3_eleven_core194_a6_fixed/build.py \
  --work /scratch/FRESH-r55-a6-preflight
python3 -B ramsey_r55_order3_eleven_core194_a6_fixed/controls.py \
  --work /scratch/FRESH-r55-a6-controls --drat-trim /absolute/path/to/drat-trim
python3 -B ramsey_r55_order3_eleven_core194_a6_fixed/run.py \
  --work /scratch/FRESH-r55-a6-full --kissat /absolute/path/to/kissat \
  --drat-trim /absolute/path/to/drat-trim \
  --solve-seconds 90 --replay-seconds 600
python3 -B -O ramsey_r55_order3_eleven_core194_a6_fixed/verify.py \
  --source-work /scratch/FRESH-r55-a6-full \
  --work /scratch/FRESH-r55-a6-verification \
  --drat-trim /absolute/path/to/drat-trim --replay-seconds 600
```

Two workers use one 90-second solver call per complete case, with a
150-second outer timeout. Every actual UNSAT must pass full DRAT including
RAT, with a 600-second checker cap and a 660-second outer timeout. Fresh
optimized verification reconstructs all three complete formulas and replays
every refutation again. It compares the full preparation entry by entry,
including normal versus optimized profile/formula controls. A solver exit
without checked evidence is not an exclusion; UNKNOWN is not feasibility.

A SAT outcome requires all 320 primary values, explicit clause evaluation,
a compact edge list and the separate direct package's literal five-set,
action, core and BLUE-pair graph checks. Seven malformed status transcripts
and an invalid refutation of a satisfiable fixture are rejected under
normal and optimized Python. No positive claim rests on an unchecked model.

The runner freezes 23 source identities, including PROOF.md and all executed
Python sources. Its atomic per-case records preserve pending refutations
before checking. Same-contract `--resume` retains explicit UNKNOWN and
rechecks saved terminal evidence. `WORK/STOP` prevents queued starts while
active bounded work finishes. It never turns partial coverage into a full
result. Complete CNFs, traces and logs belong outside Git.

Kissat 4.0.4 source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, binary SHA256
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
DRAT-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
Both executable hashes were checked before production. Time-limited traces
and runtime observations may vary with scheduling.

## Dependencies and coordination

The [prior full moving-type decisions](../ramsey_r55_order3_eleven_core194_attachment_decisions)
exclude five other types with checked complete proofs, source
`de6dffc22f2270444a6089f9cf8269535293081b`. This package does not repeat them.
The [attachment cover](../ramsey_r55_order3_eleven_core194_attachments),
source `cb188f689ea85d7e635048999a4a9df1d2df33f2`, supplies the original
normalization and expected profiles. The degree window imports R(4,5)=25.
This package gives an explicit specialized three-case proof and independently
checks every fixed word, relabeling and unit.

The direct base and local pair lemma have accepted independent reviews.
At the final refresh, independent review accepted the attachment cover and
five prior type exclusions. This NEW refinement and its full three-case
closure remain unreviewed independently. Author-written code
cross-checks and two full proof replays are not independent peer review or
formalization. Ordinary finite reasoning, exact Python/hardware, the physical
encoding, imported Ramsey theorem and full DRAT checker remain trusts.

The initial incremental graph inspection through 3223 read external 3222's
accepted M214 third-anchor coverage/encoding review, source
`96ef296e5690bc015bdfec08ac7e88e37cb22535`. It preserves representatives of
the reviewed base models; it does not certify the producer's orbit counts
or provide a solver verdict. Its full body was read, not its code replayed
or its premises imported here. No M214 semantic audit was repeated. At this initial cutoff the teammate had no new committed result since
3208. The later final refresh below supersedes that observation.

The principal's 05:35 coordination boundary forbids an equivalent timeout
or larger-cap ladder. This is one complete fixed-attachment classification.
If all three cases remain UNKNOWN, the next approach must change before
further Core194 variants. No subsequent phase is launched within this pass.


## Final shared evidence and stopping point

The refresh through height 3227 found an independent acceptance of the
nine-type cover and all five earlier exclusions at 3224:
[review source](../ramsey_r55_core194_attachment_decisions_review1),
`30912d675aee5a5da5630f12bd1f1cdd76fb3589`. Its full README/body were read and
manifest checked. The reviewer directly enumerated all 3^15 assignments in
C++, compared every profile weight and degree, checked all complete child
tails, and reproduced all five refutations with a distinct Kissat build and
full DRAT. This resolves the former cover/five-exclusion review gap; it does
not review the new three full fixed-profile formulas or proofs here.
The frozen proof/source contract predates that arriving review.

The teammate's new [joint neighborhood realization](../ramsey_r55_joint_neighborhood_degree_realization),
source `67782fb3b0a5704baf2df8e407ba72d3c97b6761`, appeared at 3226.
Its README/body were read and manifest checked. A chosen H92 now admits
joint Q choices and actual completion edges realizing all 43 target degrees,
while retaining the two valid local Q neighborhoods. Its full graph has
442 red and 211 blue K5s and is not a target. H93 remains UNKNOWN90.
This is a distinct nonsymmetric scope; neither its searches nor code were
replayed or imported into these symmetry formulas. Its next missing three
exceptional-neighborhood conditions remain the teammate's lane.

No affecting objection or overlapping (6,0,1) closure was found. All 23 frozen
source identities matched after successful verification. No background job
remains. The next natural bounded direction is the complete a=5 stratum:
ten certified fixed profiles for (5,0,2) and nine for (5,1,1). Those finer
formulas and searches are NOT STARTED. The (4,1,2) type has 27 candidate
profiles and stays open. The pass yields at this complete moving-type closure.
