# Full-core propagation of the two-empty-anchor theorem

Eight further eleven-cycle four-versus-seven core classes have no full
43-vertex Ramsey(5,5) extension, conditional on the preceding anchor theorem
and accepted parent reduction. **26 core classes remain open**, covering
16,605 labeled cores. The cumulative exclusion is **171 of 197** classes,
covering 98,938 of 115,543 locally valid labeled cores.

This package applies every two-empty-anchor constraint to all 34 starting
classes. Each test retains the complete 43-vertex formula, canonical
core, and existing fixed-vertex order. Every successful refutation has
full replay and a second replay after fresh complete reconstruction.

The ambient action has ten fixed vertices, four internally red moving
triangles and seven internally blue moving triangles. If z counts empty
four-bit fixed signatures and x_i counts singleton {i}, the preceding
anchor theorem gives `z+x_i>=2` whenever the three other red triangles
contain no blue triangle. There are 56 such applications across the
34 residual representatives. This package encodes the counts directly
with fresh indicators. It does not impose first-two-row units on a
non-prefix triple or add a new symmetry restriction.

[PROOF.md](PROOF.md) gives the complete mathematical implication,
indicator/count equivalence, unchanged normalization and trust boundary.
The full theorem being propagated is still pending independent review.
The computational outcome is not a 43-vertex construction or a Ramsey
lower-bound improvement, and the separate three-versus-eight branch
is untouched.

## Complete bounded outcome

The new whole-core exclusions are

```text
88, 102, 107, 138, 169, 172, 176, 196.
```

They cover 7,452 additional labeled cores. The remaining cases, all
explicit UNKNOWN at the fixed solver limit, are

```text
92, 97, 109, 114, 118, 119, 122, 123, 124, 154, 155, 159, 164,
167, 168, 177, 180, 182, 185, 186, 188, 190, 191, 192, 193, 194.
```

All 34 complete formulas were tested and freshly reconstructed. All
8 refutations passed full DRAT replay twice; all 26 UNKNOWN outcomes
remain open and imply no existence claim. Both three-versus-eight cores
and the minimum moving count eleven are unchanged. No target graph was
found. These are whole-core exclusions, not excluded signature subcases.

The fixed run used Kissat `--time=20`, two workers, and a 300-second limit
per full replay. It finished in 515.702146 seconds. Fresh reconstruction
and second replay took 151.570121 seconds. The 8 successful traces total
163,546,853 bytes, maximum 24,059,972; all contain RAT, with 6,077 RAT core
lemmas altogether. Largest reported child RSS was 261,544 KiB.
Normal and optimized Python controls and boundary summaries agree.

The next useful structural boundary is the presence or absence of an
empty FOUR-bit fixed signature. The current formulas retain all anchor
inequalities on both sides of that possible split. This package has
not begun that split, another sweep, or a longer timeout.

## Reproduce

From this directory, using CPython3.11.2, GCC12.2.0 and the tools below:

```bash
python3 -B run.py --work /scratch/new-r55-anchor-propagation/full \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim \
  --solve-seconds 20 --replay-seconds 300
python3 -B verify.py --source-work /scratch/new-r55-anchor-propagation/full \
  --work /scratch/new-r55-anchor-propagation/verification \
  --drat-trim /path/to/drat-trim --replay-seconds 300
python3 -B summarize.py --source /scratch/new-r55-anchor-propagation/full \
  --verification /scratch/new-r55-anchor-propagation/verification \
  --output /scratch/new-r55-anchor-propagation/boundary.json
python3 -O -B summarize.py --source /scratch/new-r55-anchor-propagation/full \
  --verification /scratch/new-r55-anchor-propagation/verification \
  --output /scratch/new-r55-anchor-propagation/boundary-optimized.json
cmp /scratch/new-r55-anchor-propagation/boundary.json \
  /scratch/new-r55-anchor-propagation/boundary-optimized.json
sha256sum -c SHA256SUMS
```

The run has exactly 34 cases and two workers. A STOP file in the external
work directory prevents further cases from starting while in-progress
cases finish their bounded solve and proof check. `--resume` requires
the unchanged contract and retained evidence; it preserves completed
UNKNOWN outcomes and replays saved refutations. Verification uses a
fresh directory and reconstructs every complete base and final formula.

Kissat4.0.4 source: `8af8e56f174b778aef3aa45af9f739b2a5f492c2`.
drat-trim source: `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Compiler flags: `-std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror`.
Only the Python standard library is needed. Exact executable, source,
input, formula and trace hashes are in `result.json`. A changed host
may change a timeout outcome; every refutation still needs full replay.

## Source and compact evidence

- [cube.py](cube.py): pinned 34-case boundary, complete base reconstruction,
  fresh indicator definitions and all nine-subset count clauses.
- [audit.py](audit.py): independent literal core/application checks,
  primary edge-orbit meanings, complete formula comparison and controls;
  imports no producer.
- [run.py](run.py), [verify.py](verify.py): bounded full sweep and fresh
  reconstruction with second proof replay.
- [summarize.py](summarize.py): entrywise checked whole-core partition
  and exact labeled/cumulative counts.
- [cases.json](cases.json): the 34 specific cores, their exact original
  full-base hashes and all 56 applicable omitted indices.
- [result.json](result.json), [verification.json](verification.json),
  [boundary.json](boundary.json): the complete outcomes and evidence.
- [controls.json](controls.json), [inherited_anchors.json](inherited_anchors.json),
  [parent_controls.json](parent_controls.json): corruption controls,
  inherited literal anchor audit and parent checks.

All formulas retain the accepted 34,280-variable, 615,920-clause parent
plus eighteen core units. For each applicable complement, ten fresh
variables mean that a fixed vertex is blue to the whole complement.
Four clauses define each indicator, and ten positive nine-indicator
clauses require at least two true. There are ten new variables and
fifty new clauses per complement.

The resulting sizes are 34,290/615,988 (14 cases), 34,300/616,038
(19 cases), and 34,320/616,138 (one case), in variables/clauses.
All bases must match the original residual-sweep hashes. The full parent
is independently reconstructed from all 962,598 five-sets and 664 gate
rows by the inherited C++ auditor. The new Python auditor checks every
retained clause, core unit, new gate/count clause, fresh variable and EOF.
The Boolean checks cover all 16 gate assignments and all 1,024 indicator
vectors. Four case-list corruptions and eight formula corruptions are
rejected. Normal and optimized Python control reports agree.

Every successful refutation uses full DRAT replay against its exact
audited formula, followed by another replay after fresh reconstruction.
UNKNOWN traces remain incomplete search output and cannot certify
nonexistence or existence. SAT must decode to an edge list and pass the
inherited independent literal 43-vertex verifier before any target claim.

## Dependencies and limits

The parent and its counter/normalization bridge come from the accepted
[`ramsey_r55_order3_eleven_cycle_obstruction`](../ramsey_r55_order3_eleven_cycle_obstruction).
Complete marked-action coverage and the original full normalization
come from the accepted 197-class core cover. The 118-class blue-K4
exclusion and later 34-class sweep also have accepted independent reviews.

The newer seven- and four-core exclusions and their empty-signature
premise remain unreviewed dependencies of the starting 34-class boundary.
The universal theorem supplied by
[`ramsey_r55_order3_eleven_anchor_equality`](../ramsey_r55_order3_eleven_anchor_equality)
is an unreviewed premise of every new refutation here. Its two full
equality proofs were checked twice in the preceding package; this pass
imports that result and reruns its separate literal application checker.
It does not repeat the finished equality search.

The new count encoding and computational exclusions await independent
review. Further trust is imported R(4,5)=25, unformalized mathematics,
exact source semantics, compiler/runtime/hardware, SHA256 and full DRAT
checking. Internal reconstruction is not peer review or formalization.
The source plus compact reports reproduce the computation; large CNFs,
proof traces, logs and binaries remain outside Git. Hashes alone are not
refutations. The earlier unspecialized sweep used ten-second limits,
so no controlled speed comparison is claimed for this 20-second test.

This milestone ends after the complete bounded sweep, verification and
checkpoint. No additional core, signature stratum or larger timeout is
started here.
