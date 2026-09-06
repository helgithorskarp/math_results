# Core194 blue empty pairs have moving contact type (4,1,2)

All nineteen complete fixed-attachment cases in the a=5 stratum are UNSAT,
with full DRAT checked twice. This excludes the entire moving types
**(5,0,2) and (5,1,1)**. Together with the independently accepted earlier
six moving-type exclusions, only **(4,1,2)** remains for a BLUE empty fixed
pair in the four-versus-seven Core194 family.

Thus such a pair has exactly four common-red internally blue moving
triangles; the exclusive contact counts are one and two, up to orientation.
This removes nineteen candidate joint profiles and 195,342 labeled star
assignments from the inherited degree relaxation, leaving **27 profiles /
1,103,130 labeled stars**. These are not graph realizations. The RED-pair
branch, whole Core194 and all **17 whole classes / 9,153 labels** remain open.
No 43-vertex target or Ramsey-bound improvement is claimed.
[boundary.json](boundary.json) records the scope and unstarted next profiles.

## Checked decisions

| Moving counts | Fixed counts | Red degrees | Solve seconds | Full replay seconds | RAT core lemmas | Proof bytes |
|---|---|---|---:|---:|---:|---:|
| (5, 0, 2) | (0, 5, 3) | (20, 24) | 0.980705 | 1.569363 | 14 | 3,646,484 |
| (5, 0, 2) | (0, 6, 2) | (21, 23) | 0.677266 | 1.319231 | 0 | 2,816,183 |
| (5, 0, 2) | (0, 7, 1) | (22, 22) | 0.673884 | 1.168581 | 0 | 2,170,617 |
| (5, 0, 2) | (0, 8, 0) | (23, 21) | 0.672256 | 1.017693 | 0 | 1,440,704 |
| (5, 0, 2) | (1, 5, 2) | (21, 24) | 2.485426 | 2.171653 | 60 | 4,052,504 |
| (5, 0, 2) | (1, 6, 1) | (22, 23) | 0.673605 | 1.168627 | 0 | 2,146,803 |
| (5, 0, 2) | (1, 7, 0) | (23, 22) | 0.672764 | 1.068149 | 0 | 1,494,914 |
| (5, 0, 2) | (2, 5, 1) | (22, 24) | 7.82698 | 5.182799 | 33 | 10,922,705 |
| (5, 0, 2) | (2, 6, 0) | (23, 23) | 4.699393 | 3.075245 | 0 | 5,481,475 |
| (5, 0, 2) | (3, 5, 0) | (23, 24) | 6.811376 | 5.482767 | 0 | 7,630,034 |
| (5, 1, 1) | (0, 2, 6) | (20, 24) | 0.428271 | 1.419392 | 3 | 3,784,358 |
| (5, 1, 1) | (0, 3, 5) | (21, 23) | 0.579541 | 1.519419 | 12 | 4,061,610 |
| (5, 1, 1) | (0, 4, 4) | (22, 22) | 1.132531 | 1.720232 | 24 | 4,363,938 |
| (5, 1, 1) | (1, 2, 5) | (21, 24) | 0.478148 | 1.418815 | 12 | 3,609,082 |
| (5, 1, 1) | (1, 3, 4) | (22, 23) | 1.282869 | 1.820382 | 27 | 4,440,902 |
| (5, 1, 1) | (2, 2, 4) | (22, 24) | 1.281884 | 1.670343 | 15 | 4,087,798 |
| (5, 1, 1) | (2, 3, 3) | (23, 23) | 2.740043 | 2.422478 | 15 | 5,081,402 |
| (5, 1, 1) | (3, 2, 3) | (23, 24) | 2.589721 | 2.673504 | 15 | 5,010,335 |
| (5, 1, 1) | (4, 2, 2) | (24, 24) | 4.953558 | 4.379568 | 30 | 6,877,195 |

Production took 76.094705 seconds; fresh optimized verification
72.607107 seconds. Nineteen solver calls and thirty-eight full proof
replays completed, with no UNKNOWN or SAT. Twelve proof cores use RAT
lemmas; seven have zero. All checks used full DRAT with RAT enabled.
The original coarse UNKNOWN90 records remain historical and unchanged.

The nineteen complete traces total **83,119,043 bytes**, outside Git.
The largest recorded child maximum RSS was 267,924 KiB,
excluding the in-process parent generator. Complete formula, trace and log
identities and first checks are in [result.json](result.json); the second
checks are in [verification.json](verification.json). Hashes identify files,
not proofs. Source reproduces the complete inputs and bounded solver calls.

## Complete cover and coupled normalization

See [PROOF.md](PROOF.md) for the explicit argument. With RR,RB,BR contact
counts (x,y,z) for the eight other fixed vertices, x+y+z=8:

* For (5,0,2), red endpoint degrees are 23-z and 29-y. The imported degree
  window 18..24 leaves exactly ten profiles, characterized by y>=5.
* For (5,1,1), the degrees are 26-z and 26-y. The window gives y,z>=2.
  There are fifteen ordered profiles, or nine after imposing y<=z.
  An endpoint swap must be coupled with the phase-preserving interchange
  of moving triangles 9 and 10, which restores the normalized RB/BR contacts.
  Then sort the other fixed vertices by contact. An endpoint swap alone
  fails to preserve the moving child and is explicitly rejected.

The producer filters the accepted 119-profile certificate. A separate
physical checker, importing no profile producer, visits all 6,561 fixed
words for each type. It finds 577 and 4,074 admissible words respectively,
with 486 and 3,415 distinct normalizing vertex permutations. In the second
type 1,512 words require the coupled swap. Every actual thirty-contact
transport is checked, along with vertex/C3/320-primary bijections. All 570
normalized unit meanings, counts, degrees and full-star weights agree.

The complete base is also checked under the coupled swap and seven adjacent
fixed-vertex transpositions: **2,928,552 clause images**, all present. The
relevant fourteen moving units are preserved. These relabelings normalize
the family; they need not be automorphisms of individual solutions. Several
marked pairs can represent the same graph, so this is a cover, not an
isomorphism census. Existence of a BLUE empty pair is not asserted.

Each child contains 320 primary variables and 366,099 clauses: the entire
reviewed direct BLUE base plus 30 physical units (14 moving, 16 fixed). All
unmentioned edges and fixed-core incidences remain free. There is no
selected degree profile, M stratum or extra symmetry rule. The base is
freshly generated and independently reconstructed. Full body bytes,
physical tail, header and EOF are checked. Eight corrupt profile records,
seven malformed children, seven corrupt status transcripts and a false
DRAT refutation of a satisfiable fixture are rejected. Normal and optimized
Python agree; preflight, production and fresh verification preparations
match entry by entry.

## Reproduction

CPython 3.11.2 and standard library; from the repository root:

```bash
python3 -B ramsey_r55_order3_eleven_core194_a5_fixed/build.py \
  --work /scratch/FRESH-r55-a5-preflight
python3 -B ramsey_r55_order3_eleven_core194_a5_fixed/controls.py \
  --work /scratch/FRESH-r55-a5-controls --drat-trim /absolute/path/to/drat-trim
python3 -B ramsey_r55_order3_eleven_core194_a5_fixed/run.py \
  --work /scratch/FRESH-r55-a5-full --kissat /absolute/path/to/kissat \
  --drat-trim /absolute/path/to/drat-trim \
  --solve-seconds 90 --replay-seconds 600
python3 -B -O ramsey_r55_order3_eleven_core194_a5_fixed/verify.py \
  --source-work /scratch/FRESH-r55-a5-full \
  --work /scratch/FRESH-r55-a5-verification \
  --drat-trim /absolute/path/to/drat-trim --replay-seconds 600
```

Two workers use one 90-second solve per new complete case, outer timeout 150.
Every UNSAT needs full DRAT including RAT, checker cap 600, outer 660 seconds.
Fresh optimized verification rebuilds all complete formulas and replays
all proofs; it does not re-solve UNKNOWN cases. A SAT requires all 320 model
values, clause evaluation, compact edge list and separate literal five-set,
action, core and BLUE-pair graph verification. No SAT occurred.

The runner freezes 27 source identities, including PROOF.md and every
executed source. Atomic pending records preserve proofs before checking.
Same-contract `--resume` retains UNKNOWN and rechecks saved terminal evidence.
`WORK/STOP` prevents queued starts while bounded active work finishes.
Complete CNFs, proofs and logs belong outside Git. No background job remains.

Kissat 4.0.4 source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, binary SHA256
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
DRAT-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
Both pins were freshly checked before production. Runtime and time-limited
outcomes can vary with hardware and scheduling.

## Dependencies, trust and shared context

The [attachment cover](../ramsey_r55_order3_eleven_core194_attachments),
source `cb188f689ea85d7e635048999a4a9df1d2df33f2`, and
[five earlier moving exclusions](../ramsey_r55_order3_eleven_core194_attachment_decisions),
source `de6dffc22f2270444a6089f9cf8269535293081b`, have
[accepted independent review](../ramsey_r55_core194_attachment_decisions_review1),
source `30912d675aee5a5da5630f12bd1f1cdd76fb3589`, graph 3224.
The [entire (6,0,1) exclusion](../ramsey_r55_order3_eleven_core194_a6_fixed),
source `7674a903b84764cb8747c9652c74c193b15e0d3d`, now has
[accepted independent review](../ramsey_r55_core194_a6_fixed_review1),
source `6bae11903cfc04e6f7fdc6a6c60741c7736a5641`, graph 3238.
Its full README/body were read and manifest checked this pass. The reviewer
independently enumerated the fixed words in C++, checked the complete
formulas and regenerated/replayed all three proofs with a distinct Kissat
build. This resolves that inherited gate; it does not review the new a=5 work.

The [direct base](../ramsey_r55_order3_eleven_core194_direct) and local pair
lemma have accepted reviews. R(4,5)=25 supplies the degree window; the base
has no degree assumption or auxiliary variables. This new nineteen-profile
cover, its coupled-normalization implementation and full refutations remain
**not independently reviewed**. Author cross-checks and two proof replays
are not peer review or formalization. Ordinary finite reasoning, exact
Python/hardware, physical encoding, the imported Ramsey theorem and full
DRAT correctness remain trust boundaries.

Incremental inspection after 3227 through 3241 read new external graph 3228's
sharp c-8 exterior-footprint cut (source 3638240a52905eb6d6531f5498403b2a5b376523)
and graph 3236's dense four-separator order 22 classification
(source 4bf427dcb479b49978f772e12e55c3cea4711927). Their bodies were read;
no code was replayed and neither is imported here. The first is M214 search
infrastructure without a verdict. The second is a claimed conditional local
classification, not a 43-vertex graph or global degree 22 closure. No overlap
with this symmetry stratum was found.

The teammate's [joint neighborhood degree realization](../ramsey_r55_joint_neighborhood_degree_realization),
source `67782fb3b0a5704baf2df8e407ba72d3c97b6761`, graph 3226, remains the latest
relevant teammate result: all 43 prescribed degrees are realized with the
selected local neighborhoods, but 653 monochromatic K5s remain. Its missing
exceptional-neighborhood/global conditions are a distinct nonsymmetric lane.
No teammate search was duplicated. The final incremental refresh after 3241
through 3243 found no new relevant content; dependency feedback showed the
accepted reviews and no affecting objection. Unrelated remote changes were
integrated by ordinary fast-forward without entering their research scope.

The principal requires a complete partition that excludes cases and forbids
an equivalent timeout/larger-cap ladder. This pass closes two whole moving
types. The next coherent direction is the 27 fixed profiles of (4,1,2), already
listed by the accepted cover; those finer formulas/searches are **unstarted**.
The red branch, whole Core194 and 17 whole classes stay open. This pass yields
before another stratum or proof phase.
