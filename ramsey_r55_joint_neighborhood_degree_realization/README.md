# Joint valid neighborhoods can realize all 43 target degrees

For the **specific H92** below, the two marked blue-neighborhood graphs
can be chosen jointly and embedded in a complete 43-vertex graph with
degree sequence `20^3 21^40`. This answers the compatibility question left
by the preceding two independently chosen, degree-overloaded tuples.
It is a graph realization, not just feasible degree margins.

**The witness is not Ramsey(5,5): it contains 442 red and 211 blue K5s.**
No whole H family, degree profile, or Ramsey bound is excluded. The
corresponding fixed-H93 test was UNKNOWN at 90 seconds, not UNSAT or SAT.
The earlier chosen-tuple obstructions remain correct and unchanged.

## Exact certificate and scope

`G92.json` specifies all 903 pairs by a canonical list of 450 red edges;
all other pairs are blue. Its SHA256 is
`394aee401f7e9d6843affc05968b305bad2f92cd328035c65b5b8a0da9619a3e`.
Degrees are 20 at vertices 0,1,38 and 21 at all other vertices.

H occupies 0,...,19, the central root is 38, and put
X=20,...,28, Y=29,...,37, Z=39,...,42. The central root is red precisely
to H. Inside H the marked vertices 0,1 are blue adjacent, with red
neighborhoods {10,11,12,13,18,19} and {14,15,16,17,18,19}.
Their remaining red neighbors are respectively Y union Z union {38}
and X union Z union {38}. These fix the original root-signature cells;
no contacts, graph automorphisms, or vertex-ordering assumptions are added.

H is the unchanged H92 from
[the central-neighborhood artifact](../ramsey_r55_critical_path_central_neighborhood),
source `0dd9c5e6d6418a991dc01e177e2b9d001cd38b91`, and has no red K4 or
blue K5. On W={2,...,9}, the BLUE lexicographic pair mask is 5388912.
The two actual blue neighborhoods of the marked vertices are:

| Anchor | H portion | New portion | Red / blue edges | Red K4 / blue K3 |
|---|---|---|---|---|
| 0 | 1,2,3,4,5,6,7,8,9,14,15,16,17 | X | 124 / 107 | 105 / 120 |
| 1 | 0,2,3,4,5,6,7,8,9,10,11,12,13 | Y | 124 / 107 | 103 / 119 |

Each is a complete 22-vertex graph with **no red K5 and no blue K4**.
In particular its blue cone is Ramsey(5,5;23). H with its central red
cone is Ramsey(5,5;21). These three simultaneously embedded cones are
not a full Ramsey43 certificate.

The local triangle counts `(red edges in red neighborhood,
blue edges in blue neighborhood)` are (93,107) at both marks and
(92,107) at the center. These are exact counts in the displayed graph,
not an assertion that all 43 vertices satisfy the hard-branch local caps.

For every w in W let x,y,z be its red degrees into X,Y,Z. The necessary
interface identity is z=20-d_H(w)-x-y, with 0<=z<=4. The new graph realizes
all eight equations with actual Z neighbors:

| w | d_H | x | y | z | Red Z neighbors |
|---|---:|---:|---:|---:|---|
| 2 | 9 | 5 | 5 | 1 | 42 |
| 3 | 10 | 5 | 5 | 0 | none |
| 4 | 10 | 5 | 5 | 0 | none |
| 5 | 9 | 4 | 6 | 1 | 40 |
| 6 | 11 | 4 | 4 | 1 | 40 |
| 7 | 10 | 6 | 4 | 0 | none |
| 8 | 8 | 5 | 5 | 2 | 40,42 |
| 9 | 7 | 6 | 6 | 1 | 42 |

This replaces the overload at W vertex3 in the preceding chosen H92
tuple; it does not repair that tuple while keeping its Q graphs fixed.

The union of H, both Q graphs and the fixed root stars on vertices0..38
has 552 colored pairs (279 red,273 blue), 189 uncolored pairs, and no
fully colored monochromatic K5. The complete graph additionally colors
all 351 pairs outside that partial union, including incidences to Z.
Consequently every one of its 653 monochromatic K5s uses at least one
of those 351 pairs. Unknown partial pairs are never treated as blue.

Exactly 50 red K5s contain mark0,79 contain mark1, and33 blue K5s contain
the center. The remaining313 red/178 blue K5s avoid all three roots.
No K5 is counted twice in this partition, as the exact root-membership
masks in `verification.json` confirm. Thus the next missing local layer
is explicit: the red neighborhoods of both marks and the blue neighborhood
of the center. Even closing these would leave five-sets avoiding the roots.
This layer has **not** been searched here.

## Encoding and bounded outcome

For each supplied H, fix its190 pairs and all three root stars. There are
276 fixed pairs and627 free unordered pairs on43 vertices. A Boolean
variable per free pair means red. The formula includes exactly:

1. Every red-K5 and blue-K4 prohibition inside each actual marked blue
   neighborhood Q (their vertex sets are fixed by the root stars).
2. Exactly124 red edges in each Q.
3. All43 exact target degree equations, not merely individual bounds.

No Q witness is frozen. All288 formerly separate Q choices and all339
remaining unfixed completion pairs are decisions. No symmetry breaking
is used. In particular this is not the old fixed-tail descent, nor a
longer run of the parked joint-four-outside formula. The old3140 mixed-root
count cuts, other whole-graph K5 clauses, and all-vertex hard caps are NOT
asserted to be retained in this different necessary subsystem.

For the selected profile/root-star/cap guard, any target graph extending
the chosen H satisfies these clauses. Indeed each marked red neighborhood
has prescribed degree sum419. If p is its internal red edge count, the
red cross count is399-2p. The whole graph has450 red edges, so its blue
neighborhood has31+p red edges and200-p blue edges. The selected caps
p<=93 and200-p<=107 force p=93 and the Q edge total124. These caps are
conditional hypotheses, not new unconditional Ramsey bounds.

Conversely a satisfying assignment gives exactly this stated subsystem:
each clique clause rejects precisely the monochromatic set it names;
the sequential thresholds encode exact Boolean sums. The recurrence
`s[i,j] <=> s[i-1,j] OR (literal_i AND s[i-1,j-1])` uses exact four-clause
equivalences and boundary constants. It has a unique threshold extension
for any primary assignment. The copied `encoding.py` is byte-identical to
the parent (SHA256902f06f7bd3ec062aaa717743bd972ab0f3fcaaff43d3ade2197b4252820dbcd).
There is no claim this subsystem is sufficient for Ramsey43.

| Fixed H | Variables | Clauses | Solve seconds | Result |
|---|---:|---:|---:|---|
| H92 | 33,515 | 146,631 | 7.644022 | SAT, graph checked |
| H93 | 33,358 | 146,265 | 90.024975 | explicit UNKNOWN |

Both calls had90-second caps. CNF sizes are2,957,405 and2,958,269bytes;
hashes, degree rows, source identities and exact execution records are
in `run.json`. The largest child RSS was65,756KiB, excluding Python
generation. A fresh self-contained public-source H92 solve took7.789890s
and reproduced its CNF, graph and8,678,542-byte SAT trace bytewise. The
H93 formula was regenerated under optimized Python and byte-compared
without another solver call. Its105,126,721-byte partial trace is not a
refutation or restart state. There were three total solver calls, one
UNKNOWN call, zero UNKNOWN retries and zero proof replays. Timings are
observations, not promises. No UNSAT claim is made.

Kissat4.0.4 source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, binary SHA256
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
The generator checks the executable identity and requires an exact status
line matching the exit code. A complete SAT assignment is evaluated against
every clause before decoding. Reports marked graph-pending describe that
generator stage, subsequently completed by the separate graph checker.
CNFs, traces, logs and binaries stay outside Git. They are not proof premises
for the positive graph statement.

## Direct checks and reproduction

With CPython3.11.2 and the standard library, from the repository root:

```bash
python3 -B ramsey_r55_joint_neighborhood_degree_realization/check.py --report /scratch/FRESH-joint-check.json
python3 -B -O ramsey_r55_joint_neighborhood_degree_realization/check.py --report /scratch/FRESH-joint-check-O.json
python3 -B ramsey_r55_joint_neighborhood_degree_realization/controls.py --report /scratch/FRESH-joint-controls.json
```

The outputs equal `verification.json` and `controls.json` bytewise.
`check.py` imports neither the producer, encoder, solver, nor any earlier
research module. It derives the actual neighborhoods from the full graph,
checks every root contact and degree, and compares literal subset/pair
enumeration against recursive bit-intersection clique lists. Comparison
is entrywise, including all653 global K5s,208 red K4s and239 blue triangles
in Q, all forbidden local lists, and all partial-union five-sets.
There are962,598 five-sets on43 vertices per color and575,757 on39.
Both degree implementations also agree. Normal/optimized reports and the
fresh replay graph's report are byte-identical.

Ten malformed graph inputs are rejected. One additional balanced four-edge
edit entirely inside X preserves every degree, both Q densities and all
fixed contacts but creates both a red K5 and a blue K4 in Q0; it is rejected
at the Ramsey check. Its two color witnesses are recorded separately,
not counted as two distinct edits. Seven malformed solver transcripts are
rejected and three valid status controls pass. Controls are identical
under normal/optimized Python. These are author-written cross-checks,
not independent peer review or proof-assistant formalization.

Optional regeneration of the positive witness:

```bash
python3 -B ramsey_r55_joint_neighborhood_degree_realization/generate.py \
  --work /scratch/FRESH-joint-replay --kissat /absolute/path/to/kissat --seconds 90 --density 92
python3 -B ramsey_r55_joint_neighborhood_degree_realization/check.py \
  --work /scratch/FRESH-joint-replay --report /scratch/FRESH-joint-replay-check.json
```

`--density 93 --emit-only` reconstructs the undecided second formula without
a solver call; default generation tests both cases. Work/report paths must
be fresh. Exact graph checks do not require a solver or trust its encoding.
Trust for the existence statement is ordinary finite reasoning, exact
Python/hardware, graph interpretation and file identities. The checker
algorithms are based on the same conventional primitives used in the
parent checker, but are separate from the producing encoding. No priority
claim is made.

## Coordination and next boundary

The input H artifacts and
[preceding chosen-tuple obstruction](../ramsey_r55_overlapping_neighborhood_degree_gap)
(source `2fdb8cef31597170f94e9eae9f43859d9c7a8a0c`, DN3208) are preserved.
The start-of-pass refresh through3219 read teammate3218, source
`de6dffc22f2270444a6089f9cf8269535293081b`: five complete Core194 blue-pair
types excluded, four UNKNOWN, no new whole core closure (17/9,153 remain).
That symmetry work was not imported or duplicated. Its citation of our
previous artifact is not review. External3210's dense-neighborhood
four-connectivity theorem was read as context only; no proof/code replay
or additional connectivity restriction was imported.

The final incremental refresh through3223 found external3222's review of
the M214 third-anchor coverage/encoding interface, source
`96ef296e5690bc015bdfec08ac7e88e37cb22535`. Its scoped acceptance leaves all
389 roots undecided and does not certify the incidence census or newly
review the reviewer's own upstream results. It was read, not re-audited or
used as a premise. No affecting feedback appeared on the current ancestors.
The required pre-push Git fetch then found
[the independent Core194 attachment review](../ramsey_r55_core194_attachment_decisions_review1),
source `30912d675aee5a5da5630f12bd1f1cdd76fb3589`. Its README was read:
the nine-type cover and five exclusions are accepted within the BLUE-pair
branch, with four types and the RED-pair branch still unresolved. It was
not replayed here and changes no premise of this nonsymmetric witness.

The next bounded direction is a joint graph-level test of the missing
three exceptional-neighborhood Ramsey conditions, keeping the Q and
completion edges variable. Do not freeze or descend on this653-K5 graph,
infer H93 infeasibility from UNKNOWN, or repeat that call with a longer cap.
All other branch/profile/census scopes remain unchanged. No next layer,
new H, new density, or background job has begun. This milestone yields here.
