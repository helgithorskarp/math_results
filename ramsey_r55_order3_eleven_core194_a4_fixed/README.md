# Core194 has no blue empty fixed pair

All **27 complete fixed-attachment cases of moving type (4,1,2)** are UNSAT,
with full DRAT checked in production and against fresh reconstructed inputs.
This excludes the last moving type in the BLUE empty-pair cover. Together
with the earlier complete moving-type closures, **no blue empty fixed pair
can occur in the four-versus-seven Core194 family**.

Consequently the empty fixed vertices form a **red clique of size two,
three or four**: the reviewed multiplicity theorem gives at least two,
and a fifth would form a forbidden red K5. This is an immediate corollary
of the blue-branch closure, not a red-branch search.

The RED-pair branch, whole Core194 and all **17 whole classes / 9,153 labels**
remain open, including Core194's 81 labels. No target graph or Ramsey-bound
improvement is claimed. The new 27-profile proof remains **not independently reviewed**. An
independent acceptance of the inherited a=5 closure arrived after the
3257 content cutoff; the late review update below records the resolved gate.
[boundary.json](boundary.json) records the exact scope.

## Complete decisions

| Fixed counts | Red degrees | Solve seconds | First full replay seconds | RAT core lemmas | Proof bytes |
|---|---|---:|---:|---:|---:|
| (0, 3, 5) | (18, 23) | 0.382189 | 1.669529 | 0 | 4,918,559 |
| (0, 4, 4) | (19, 22) | 0.381671 | 1.670639 | 0 | 4,757,216 |
| (0, 5, 3) | (20, 21) | 0.430949 | 1.619017 | 3 | 4,574,169 |
| (0, 6, 2) | (21, 20) | 0.429511 | 1.570406 | 3 | 4,275,579 |
| (0, 7, 1) | (22, 19) | 0.43104 | 1.468633 | 6 | 3,908,288 |
| (0, 8, 0) | (23, 18) | 0.377218 | 1.419364 | 6 | 3,480,642 |
| (1, 2, 5) | (18, 24) | 0.381259 | 1.569837 | 0 | 4,663,492 |
| (1, 3, 4) | (19, 23) | 0.380693 | 1.569942 | 0 | 4,522,220 |
| (1, 4, 3) | (20, 22) | 1.033948 | 1.720394 | 12 | 4,851,834 |
| (1, 5, 2) | (21, 21) | 0.429721 | 1.519668 | 3 | 4,086,837 |
| (1, 6, 1) | (22, 20) | 0.428399 | 1.418976 | 0 | 3,734,779 |
| (1, 7, 0) | (23, 19) | 0.376552 | 1.369153 | 3 | 3,309,443 |
| (2, 2, 4) | (19, 24) | 0.380294 | 1.519528 | 0 | 4,256,025 |
| (2, 3, 3) | (20, 23) | 2.342225 | 2.42285 | 42 | 5,947,603 |
| (2, 4, 2) | (21, 22) | 1.98731 | 2.372518 | 65 | 4,932,808 |
| (2, 5, 1) | (22, 21) | 0.428538 | 1.419443 | 9 | 3,511,664 |
| (2, 6, 0) | (23, 20) | 0.43352 | 1.369253 | 9 | 3,130,721 |
| (3, 2, 3) | (20, 24) | 1.032134 | 1.620461 | 12 | 4,234,287 |
| (3, 3, 2) | (21, 23) | 1.937783 | 2.42257 | 77 | 5,082,171 |
| (3, 4, 1) | (22, 22) | 1.134076 | 1.870753 | 14 | 4,869,273 |
| (3, 5, 0) | (23, 21) | 0.676667 | 1.36911 | 9 | 3,020,907 |
| (4, 2, 2) | (21, 24) | 2.488595 | 2.52346 | 80 | 4,810,872 |
| (4, 3, 1) | (22, 23) | 4.350541 | 3.225636 | 57 | 5,982,343 |
| (4, 4, 0) | (23, 22) | 1.233239 | 1.920595 | 37 | 4,201,520 |
| (5, 2, 1) | (22, 24) | 3.644721 | 3.12502 | 34 | 5,467,780 |
| (5, 3, 0) | (23, 23) | 2.08446 | 2.120864 | 12 | 3,988,291 |
| (6, 2, 0) | (23, 24) | 3.899042 | 3.1747 | 12 | 6,648,210 |

The production runner recorded 74.750031 seconds; fresh optimized
verification recorded 131.004608 seconds. **27 solver calls and 54 full
proof replays** completed, with no UNKNOWN or SAT. 21 proof cores contain
RAT lemmas; 6 have zero. All checks used full DRAT with RAT enabled.
The historical coarse (4,1,2) UNKNOWN90 and direct BLUE UNKNOWN60 records
remain unchanged; the complete new cover/refutations supersede their open
status for hypothetical graphs, without repeating those coarse calls.

The complete new traces total **121,167,533 bytes**, outside Git. The
largest recorded child maximum RSS was 267,000 KiB, excluding
the in-process parent generator. [result.json](result.json) contains every
formula, trace and log identity and first check; [verification.json](verification.json)
contains all second checks. Hashes identify files and do not replace replay.

## Exact cover and validation

The [proof](PROOF.md) fixes the usual C3 action, four red and seven blue
moving triangles, Core194 word 100110110110110100 and a BLUE empty pair
u=33,v=34. The accepted pair theorem forbids BB contact outside the core.
For the normalized moving counts (RR,RB,BR)=(4,1,2), let (x,y,z) count
contacts among the eight other fixed vertices. The red endpoint degrees
are 23-z and 26-y. R(4,5)=25 gives the degree window 18..24, equivalent to
x+y+z=8, y>=2, z<=5. There are exactly **27 triples**.

For this ordered moving assignment, exactly **5,253 of 6,561** fixed words
meet the window. The count can also be obtained by subtracting the words
with zero or one RB contact, then the 28 words with y=2,z=6. The inherited
full-star weight is 105 moving placements times two orientations times
5,253, or **1,103,130**. These are star assignments, not graph realizations.
Together with the earlier closures, all 119 joint degree profiles in the
original nine-type BLUE cover are now excluded as full extensions.

Because b<c, the endpoint orientation is already fixed. Sorting vertices
35,...,42 by RR,RB,BR preserves all moving vertices, u,v and their fourteen
moving units. No further endpoint swap or identification of y,z is used.
These are family relabelings, not individual-graph automorphism claims;
multiple choices of marked pair make this a cover, not an isomorphism census.

The producer filters the accepted 119-profile certificate. A separate
physical checker imports no profile producer, visits every fixed word,
computes literal degrees and verifies every actual thirty-contact sorting
map. There are **4,019 distinct sorting permutations**. Every map is checked
as a vertex/C3/320-primary bijection; all **810** normalized physical unit
meanings, counts, degrees and weights match. Seven adjacent fixed
transpositions preserve every complete base clause: **2,562,483 clause
images** are checked, along with the moving units.

Each child has **320 primary variables / 366,099 clauses**, retaining the
entire reviewed direct BLUE base plus 30 physical units (14 moving, 16 fixed).
All unmentioned edges and fixed-core incidences remain free. There is no
selected degree profile, M stratum, added symmetry rule or local relaxation.
Fresh arithmetic/full-five-set generation and physical-orbit/possible-clique
reconstruction agree on the complete base. Every body byte, tail, header and
EOF is checked. Preflight, production and fresh optimized preparations
agree entrywise. Eight corrupt profile certificates, seven malformed full
children, seven corrupt solver transcripts and a false DRAT refutation of
a satisfiable fixture are rejected; normal and optimized controls agree.

## Reproduction and safe state

With CPython 3.11.2 and its standard library, from repository root:

```bash
python3 -B ramsey_r55_order3_eleven_core194_a4_fixed/build.py \
  --work /scratch/FRESH-r55-a4-preflight
python3 -B ramsey_r55_order3_eleven_core194_a4_fixed/controls.py \
  --work /scratch/FRESH-r55-a4-controls --drat-trim /absolute/path/to/drat-trim
python3 -B ramsey_r55_order3_eleven_core194_a4_fixed/run.py \
  --work /scratch/FRESH-r55-a4-full --kissat /absolute/path/to/kissat \
  --drat-trim /absolute/path/to/drat-trim \
  --solve-seconds 90 --replay-seconds 600
python3 -B -O ramsey_r55_order3_eleven_core194_a4_fixed/verify.py \
  --source-work /scratch/FRESH-r55-a4-full \
  --work /scratch/FRESH-r55-a4-verification \
  --drat-trim /absolute/path/to/drat-trim --replay-seconds 600
```

Two workers use one 90-second solve per new complete case, outer cap 150.
Every actual UNSAT needs full DRAT including RAT, cap 600, outer cap 660.
The fresh optimized verifier reconstructs every complete input and replays
every refutation. UNKNOWN proves nothing. A SAT requires a complete
320-primary model, explicit clause evaluation, compact edge list and
separate literal five-set/action/core/pair verification. No SAT occurred.

The runner freezes **35 source identities**, including PROOF.md and every
executed source, plus the a5/a6 and multiplicity proof dependencies. Pending
proofs are saved before checking. Same-contract `--resume` retains UNKNOWN
and rechecks saved evidence; `WORK/STOP` prevents queued starts while bounded
active work finishes. No source changed after the production contract.
No background job or pending proof remains. Complete CNFs, proofs and logs
belong outside Git. No red-branch computation has started.

Kissat 4.0.4 source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, binary SHA256
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
DRAT-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
Both pins were freshly checked before production. Runtime can vary by host.

## Dependencies and independent review boundary

The [original attachment cover](../ramsey_r55_order3_eleven_core194_attachments)
and [five earlier moving exclusions](../ramsey_r55_order3_eleven_core194_attachment_decisions)
have [accepted independent review](../ramsey_r55_core194_attachment_decisions_review1)
at graph 3224, source `30912d675aee5a5da5630f12bd1f1cdd76fb3589`.
The [complete (6,0,1) closure](../ramsey_r55_order3_eleven_core194_a6_fixed)
has [accepted independent review](../ramsey_r55_core194_a6_fixed_review1)
at graph 3238, source `6bae11903cfc04e6f7fdc6a6c60741c7736a5641`.
The [complete a=5 closure](../ramsey_r55_order3_eleven_core194_a5_fixed),
source `d16e57aa17b0dc1382bdec946df3c3e97cb353f9`, graph 3246, now has
[accepted independent review](../ramsey_r55_core194_a5_fixed_review1) at 3258.
The new a4 work remains independently unreviewed.

The [direct base](../ramsey_r55_order3_eleven_core194_direct) and
[BLUE pair theorem](../ramsey_r55_order3_eleven_core194_pair) have accepted
reviews. The [multiplicity theorem](../ramsey_r55_order3_eleven_core194_multiplicity)
and its [accepted review](../ramsey_r55_order3_eleven_core194_multiplicity_review1)
prove at least two empty fixed vertices, conditional on their reviewed
inherited chain. Their scope was re-read and review manifest checked here;
no old enumeration or solver call was repeated. The upper bound four after
blue-branch closure is simply the no-red-K5 condition.

The combined blue-branch theorem uses the complete attachment cover,
earlier refutations, new normalization/refutations and R(4,5)=25. Ordinary
finite counting and relabeling, exact Python/hardware, physical encoding,
the imported Ramsey theorem and full DRAT correctness remain trusts.
Author cross-checks and two replays are not peer review or formalization.
No unrestricted Core194 or R(5,5) conclusion is inferred.

## Shared evidence and stopping point

Initial incremental inspection after 3243 through 3255, skipping own 3246,
read external 3244's independent acceptance of the dense four-separator
order-22 family (source `090f667fc53c3e85e81af360ddbd12d974348ae4`) and
3254's sharp c-5 BLUE exterior-pair footprint bound (source
`895ee89e6fd56efeafcdb74fb9caef268978ebd1`). The first imports primary
catalogue completeness and leaves all 630 exterior edges free; its global
completions remain open. The second adds 74,958 guarded M214 rows and has
no solver verdict. Both new bodies were read; neither code was replayed
or imported into this symmetry proof.

The final refresh after 3255 through 3257 found the teammate's
[exact 104-edge degree projection](../ramsey_r55_antipodal_degree_projection),
source `40a6cd7ffbe45892bd52e3dfcdbb086f1b5afbfd`, graph 3256.
Its full README/body were read and manifest checked. It replaces three
degree-only blocks of a fixed H92 six-neighborhood subsystem with exact
binary-matrix feasibility conditions and an integral-flow lift, leaving
523 physical edge decisions. It has no SAT/UNSAT verdict, exclusion or
measured speedup. The old fixture and its degree lift both violate 202
local clauses; the lifted graph has 637 monochromatic K5s and is not a
candidate solution. The projection does not preserve omitted full-graph
K5 predicates. Its backend/lift work remains the distinct teammate lane;
no code or search was duplicated here.

Exact dependency feedback through 3257 showed no affecting objection,
a5 review or overlapping blue-branch closure. The latest teammate commit
was integrated by ordinary fast-forward; unrelated remote work was not
researched. The principal's bounded-partition milestone is met by a whole
color branch closure. This pass yields before any further red-branch phase.

The next structural direction is a complete RED empty-clique reduction
using possible cardinalities two, three and four. The BLUE no-BB lemma
and nine-type attachment cover **must not be transferred to a RED pair**;
new red-branch formulas must permit contacts not excluded by a separate
proof. No such reduction, finer formula or search is started here.


## Late review update, after source publication

Independent review of the entire a=5 closure was discovered while confirming
publication. Source `30889e084f821e22ad2471cc6187e7ce21b0f9eb`, graph
`bafkreih5qmqfy2nesjxk575ihc5cuw4mffckjndra2ve6llvdbi36lpca4` at 3258,
accepts both moving types and all nineteen refinements. The full README/body
were read and manifest checked. Standalone C++ counts, independent physical
unit reconstruction and 3,294,621 complete clause images validate the coupled
normalization. A distinct reviewer Kissat build regenerated all nineteen
proofs byte-identically; full DRAT passed, with twelve RAT-using cores.

This resolves the inherited a5 review boundary; it does not review this new
a4 closure. The frozen PROOF.md, source contract and original graph body
retain their historically correct 3257-cutoff wording. All 35 frozen source
identities and all formula/proof records remain unchanged. Only review-status
documentation is updated, and a post-publication citation links the new review.
No solver or further research phase is started by this update.
