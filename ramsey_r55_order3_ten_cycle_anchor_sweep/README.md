# A minority matching in the remaining ten-cycle Ramsey type

The 98 published anchor profiles for an order-three automorphism of type
`1^13 3^10` have been reduced to **four unresolved profiles**, with **94
independently replayed DRAT exclusions**. After the preceding four-versus-six
internal-color reduction, every minority-color triangle must see the other
three minority triangles with own-color weights **1,2,2**. Consequently the
weight-one blocks pair the four minority triangles into a perfect matching.

The twelve minority vertices induce a 7-regular graph in their internal
color, and have full-graph degree at most 22 in that color. To the six
opposite-color triangles each minority triangle has weights one or two,
with **one through four weights equal to one**. [PROOF.md](PROOF.md) gives
the complete reduction, normalization, certificate bridge, and consequences.

**The ten-cycle type is still open.** The minimum remains ten moving
3-cycles, and no 43-vertex target or new Ramsey lower bound was found.
This result imposes no M=214 or fixed-degree-profile assumption.

## The four remaining cases

Indices refer to the unchanged, zero-based
[parent list](../ramsey_r55_order3_ten_cycle_obstruction/anchor_r4.json).

| index | weights to the other minority triangles | weights to opposite-color triangles |
|---:|---|---|
| 64 | 1,2,2 | 1,1,1,1,2,2 |
| 65 | 1,2,2 | 1,1,1,2,2,2 |
| 67 | 1,2,2 | 1,1,2,2,2,2 |
| 69 | 1,2,2 | 1,2,2,2,2,2 |

These cases reached the 30-second solver limit; none is asserted feasible
or excluded. They are also recorded in [survivors.json](survivors.json).
The normal form holds simultaneously at all four minority triangles,
because any one can be chosen as the anchor before relabeling. The sweep
itself fixes only one anchor in each formula; it does not yet add the new
matching condition as a global constraint.

## Reproduction

Requirements: Python 3.11+, C++17, Kissat 4.0.4, and drat-trim. Tested with
Python 3.11.2 and GCC 12.2.0 on Linux. Pinned tool sources:

* [Kissat](https://github.com/arminbiere/kissat), commit
  `8af8e56f174b778aef3aa45af9f739b2a5f492c2` (build: `./configure && make`).
* [drat-trim](https://github.com/marijnheule/drat-trim), commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` (build: `make`).

The reference binary hashes are in [result.json](result.json). Run from
this directory; all generated state must be outside the repository:

```sh
python3 sweep.py --work /tmp/r55-k10-sweep \
  --kissat /path/to/kissat/build/kissat --drat-trim /path/to/drat-trim/drat-trim
python3 extract.py --sweep /tmp/r55-k10-sweep --output /tmp/r55-k10-cores \
  --drat-trim /path/to/drat-trim/drat-trim
python3 verify.py --work /tmp/r55-k10-verify \
  --certificates /tmp/r55-k10-cores/certificates \
  --drat-trim /path/to/drat-trim/drat-trim
python3 controls.py --base /tmp/r55-k10-verify/base.cnf --work /tmp/r55-k10-controls
```

The sweep uses two workers, 30 seconds per solver call, and 120 seconds
per original-proof replay, with additional external watchdogs. It completed
all 98 cases in **533.3 seconds** on the research host. Its largest child's
peak resident memory was 495,824 KiB. The 98 generated CNFs total
3,556,523,466 bytes; original traces for the 94 exclusions total
1,024,998,768 bytes. Allow at least 6 GB of scratch space for the full
workflow, including incomplete traces from unresolved cases and extracted
certificates. Runtime depends on the machine; a timeout or failed replay
never becomes an exclusion.

Extraction replays each original proof, writes its used input clauses and
proof lemmas, and then checks the extracted pair separately. These pairs
total **88,243,113 bytes**, still too large for this source artifact. All
full CNFs, original traces, extracted cores/proofs, binaries and logs are
omitted from Git. **The default reproduction therefore requires proof
generation; the stored hashes alone are not evidence of UNSAT.** Existing
extracted pairs can be independently replayed without a SAT solver.

The final verifier reconstructs the full parent formula, checks the exact
membership of every extracted core clause in that parent's clauses or the
case's own 27 units, and replays all 94 proofs. Its report must have
`verified_indices` equal to all indices except 64,65,67,69,
`minority_matching_forced: true`, and `all_98_cubes_excluded: false`.
Eighteen extracted proofs have RAT lemmas in their checked core. These are
**general DRAT proofs**, including RAT and deletion semantics.

`result.json` pins both original and extracted reference hashes. A mismatch
is a failed reference reproduction; a different trace would need its own
full membership check and successful proof replay before use. No claim is
based on matching a hash without replay.

## Independent checks and dependency boundaries

The parent source is pinned in [parent_manifest.json](parent_manifest.json),
at commit `e5b7d67f4a43edb1b13ed1819e1a1fcb1e2487e5`. It is the sibling
[ten-cycle internal-color artifact](../ramsey_r55_order3_ten_cycle_obstruction).
Its Python generator uses modular block differences; its separate C++
checker constructs actual pair orbits and reconstructs every primary,
gate, counter, and normalization clause. The new layer preserves every
parent clause and adds exactly 27 checked anchor units per cube. Base:

```text
variables: 28950
clauses: 927000 (parent), 927027 (each cube)
parent SHA256: f01c990a1dae17fb7bc1cd633d785cd819ba9f4d1a1eeacd69b4034663af104e
```

The separate cube audit iterates actual unordered-pair orbits to recover
unit meanings. Two exact arithmetic enumerations give the same 98-vector
list, including all 5,599 feasible labeled weight vectors. All eight
three-bit phase patterns are checked. Actual graph relabelings cover all
210 choices of four red moving triangles, with noninternal orbit bits
drawn at fixed seed 55031098. This tests the code; the hand argument proves
coverage for all graphs. Auxiliary extension after relabeling is inherited
from the proved parent counters, not inferred from a syntactic renaming of
their variables.

Four changed cube layers are rejected: wrong anchor polarity, missing
unit, changed parent clause, and wrong header. The direct graph verifier
accepts the parent's literal 30-vertex positive control after inspecting
all 142,506 five-sets and rejects a complete five-vertex negative control.
It is also available to check any future decoded SAT candidate; no such
candidate was produced in this run.
A fake core with an otherwise valid clause outside the parent-plus-cube
formula is rejected even when its supplied hash matches the fake file.
The final 59.5-second replay checked 99,568 core-clause occurrences,
including 26,633 distinct obligations from the parent formula, before
confirming all 94 extracted proofs.

The new theorem imports the global degree window from R(4,5)=25 and the
parent's five other internal-color exclusions. Those older certificates
are not rerun by the commands above; their full reproduction is documented
in the parent directory. The earlier minimum-ten chain has an
[accepted independent review](../ramsey_r55_order3_nine_cycle_review1).
No independent peer review or proof-assistant formalization of this new
94-case result is claimed. The unformalized mathematical bridge, Python/C++
implementations, runtime/compiler, hardware, SHA-256, and DRAT checker
remain explicit trust boundaries.

## Checkpoint and next step

The sweep writes each case JSON and aggregate `sweep.json` atomically.
Creating `WORK/STOP` prevents new cases from starting while active solver
and certificate checks finish. Remove that file and use `--resume` with
the same tool paths, limits, and source to continue the same bounded pass.
Completed open cases stay open on resume; cached exclusions are replayed.
A larger solver limit or a different formula should use a new work directory.

The M=214 reproduction decision has already been completed by both
researchers; the teammate's
[independent audit](../ramsey_r55_m214_formulation_checkpoint) strengthens
that shared input without supplying a SAT/UNSAT verdict. Their M=217
seven-pattern cell/triangle frontier was not duplicated. The M=214-only
upper cycle bound from [the previous symmetry audit](../ramsey_r55_m214_symmetry_audit)
and the global minimum-ten bound are unchanged here.

The next symmetry step should use the **simultaneous perfect matching**
across all four minority triangles, with the four remaining anchor rows.
That is more specific than repeating the original 98 cases at a longer
timeout. Construct and audit any new global constraints and phase
normalization before trusting their UNSAT output. No such extension, new
stratum, or further case search was launched in this completed milestone.
