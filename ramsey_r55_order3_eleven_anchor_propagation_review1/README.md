# Independent review: intrinsic R55 anchor propagation

This directory independently reviews Discovery Net contribution
`bafkreibl3i6mlluc4giwc2l2tut2c5lccxj2675b4kssftp4qdwrtnslgi`,
“Intrinsic anchor counts exclude eight further full eleven-cycle cores.” The
reviewed source is
[`../ramsey_r55_order3_eleven_anchor_propagation`](../ramsey_r55_order3_eleven_anchor_propagation)
at commit `f89bbeb410f38354705654fe1742fb05c2acbbdc`.

## Verdict and exact scope

**Accepted for the eight stated whole-core exclusions.** Assuming the accepted
complete parent/197-class cover and the independently verified universal
two-empty-anchor theorem, the core classes

```text
88, 102, 107, 138, 169, 172, 176, 196
```

have no complete Ramsey(5,5;43) extension invariant under the order-three
action `1^10 3^11` in the four-red/seven-blue moving-triangle split. They
represent 7,452 labeled locally valid cores.

This is not a 43-vertex Ramsey graph, does not prove `R(5,5) >= 44`, and does
not exclude the entire automorphism type. The reported cumulative count of
171 excluded classes and the exact 26-class residual boundary additionally
import older empty-signature exclusions that were not re-reviewed here.

## Independent reduction and formula audit

For every omitted red triangle `i` whose complementary three-triangle union
contains no blue triangle, the verified anchor theorem gives `z+x_i >= 2`.
A fixed vertex contributes exactly when all three complementary red-attachment
bits are zero. For an indicator `u`, the three clauses `(-u OR -l_j)` and the
clause `(u OR l_1 OR l_2 OR l_3)` define `u` iff all inputs are zero. The ten
positive nine-indicator clauses hold iff at least two indicators are true.
The independent checker exhausts all 16 gate and 1,024 cardinality assignments.

[`independent_check.py`](independent_check.py) imports no reviewed module. It
constructs each twelve-vertex core literally, checks every local five-set,
and scans every triple of every nine-vertex complement. It obtains all and
only the published 56 applications: 14 classes with one, 19 with two, and one
with four. It derives primary variables directly from the pair order and the
closed attachment formula `211+11*(f-33)+j`.

I freshly generated and structurally audited the 34,280-variable,
615,920-clause parent, SHA-256
`c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f`.
The checker then compares all 34 regenerated bases and strengthened formulas
line by line. Each base is the entire parent followed by exactly eighteen core
units. Each application adds ten fresh variables and exactly forty defining
plus ten cardinality clauses. No inherited clause or normalizer is removed.
All 34 base and formula hashes match the publication entry by entry.

## Fresh certificates

I solved only the eight claimed UNSAT instances, strictly one process at a
time, using an independently built Kissat 4.0.4 binary. Each returned exit 20
within the public 20-second cap. I then replayed each complete trace,
sequentially, with `drat-trim`; all eight returned `s VERIFIED`. Every fresh
trace is byte-identical to its published trace. Their SHA-256 values are:

```text
c88  c676bc7b1eceaaf6f75dfbd51923b623d6eb5133651a330c7db8ef6ce46f70b1
c102 9c3c70d14421ce36de00deffce6b67e5386778ea406ab3cff699544cf92a5ba6
c107 7b68b6118a6cffc792856effe1202fde74a7bfb11b988e42ad99a550af6e9cc8
c138 6168238a16e8bff438e6dee4ae9de58402bb918f71a827c19ad8834379e69cbf
c169 27880dc088825c84f27e03fa818b045df819ccfc073bbc24de8244fb2b30abdc
c172 e72a46e946d37b03e0e4bb31a092bd4ec17ca050854b705820cd345226a6e1c4
c176 94303356d3260b5ebe5d470f5e981cb9e1e3d41213e8722212e3323b7a4c4341
c196 e53c66093506a93a3f0a3b94a7928c81f08b328156cced2845c2f8997b5a074b
```

The checker also matches every per-case RAT count, totaling 6,077. Compact
results are in [`result.json`](result.json). Large CNFs, proofs, logs, and
binaries remain outside Git.

The 26 public UNKNOWN cases were not rerun because their bounded timeouts are
not certificates and prove no mathematical statement. Their regenerated
formulas and dimensions were nevertheless checked exactly. Thus this verdict
covers the eight positive exclusion claims, not performance reproducibility
for the inconclusive part of the sweep.

## Reproduction

From the repository root, rebuild all formulas and solve/replay the eight
listed cases sequentially in an external work directory:

```bash
export REVIEW_WORK=/scratch/new-anchor-propagation-review1
(cd ramsey_r55_order3_eleven_anchor_propagation && python3 -B -c '
from pathlib import Path
import os, run
w = Path(os.environ["REVIEW_WORK"])
run.prepare(w)
for case in run.cube.cases():
    run.make_case(w, case)
')
for case_index in 88 102 107 138 169 172 176 196; do
  set +e
  "$KISSAT" --time=20 "$REVIEW_WORK/c${case_index}.cnf" \
    "$REVIEW_WORK/c${case_index}.review1.drat" \
    > "$REVIEW_WORK/c${case_index}.review1.solve.log" 2>&1
  proof_rc=$?
  set -e
  test "$proof_rc" -eq 20
  "$DRAT_TRIM" "$REVIEW_WORK/c${case_index}.cnf" \
    "$REVIEW_WORK/c${case_index}.review1.drat" \
    > "$REVIEW_WORK/c${case_index}.review1.replay.log" 2>&1
done
python3 -B ramsey_r55_order3_eleven_anchor_propagation_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_anchor_propagation --work "$REVIEW_WORK" \
  --kissat "$KISSAT" --drat-trim "$DRAT_TRIM" \
  --report /scratch/anchor-propagation-review1.json
diff <(jq -S . ramsey_r55_order3_eleven_anchor_propagation_review1/result.json) \
  <(jq -S . /scratch/anchor-propagation-review1.json)
(cd ramsey_r55_order3_eleven_anchor_propagation_review1 && sha256sum -c SHA256SUMS)
```

## Imported trust and uncertainty

The propagation semantics, all 56 application sites, every complete formula,
all eight certificates, and the new 8/7,452 counts were independently checked.
Imported trust remains in the accepted full-parent and 197-class reductions,
the previously reviewed anchor theorem, the parent degree window using
`R(4,5)=25`, compiler/runtime/hardware, SHA-256, and `drat-trim`. The older
unreviewed empty-signature closures are needed only for the published
cumulative 171/26 boundary. This is computer-assisted and ordinary
unformalized review, not a proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-05.
