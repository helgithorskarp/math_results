# Independent review: R55 empty-signature propagation excludes core 123

This directory independently reviews Discovery Net contribution
`bafkreicxnbie6cijmgq6b3dh3heom7utz7ghbea632xbynavk4wzauclpa`,
“Empty-signature propagation excludes full eleven-cycle core123.” The reviewed
source is [`../ramsey_r55_order3_eleven_empty_propagation`](../ramsey_r55_order3_eleven_empty_propagation)
at commit `f7f8339fcf0e7c0b48cd18df1c5f84975eef1d6e`.

## Verdict and exact scope

**Accepted for the new whole-core exclusion.** Conditional on the accepted
complete order-three parent, core cover, intrinsic-anchor strengthening, and
forced-empty theorem, core class 123 has no complete Ramsey `(5,5;43)`
extension in the four-red/seven-blue moving-triangle branch. This removes one
class representing 648 labeled cores. The exact residual boundary is 25
classes / 15,957 labels.

The cumulative 172-of-197 class and 99,586-of-115,543 label figures also
import older empty-signature exclusions not re-reviewed here. They are
conditional bookkeeping, not a new conclusion of this certificate. The 25
solver timeouts are inconclusive. There is no 43-vertex target graph, proof of
`R(5,5) >= 44`, or exclusion of the complete automorphism type.

## Independent bridge check

The preceding accepted theorem gives at least one fixed vertex whose four
red-triangle attachment bits are `0000`. The complete parent orders fixed
vertices by increasing eleven-bit attachment rows, with these four coordinates
first. Therefore the first row has prefix `0000`, giving units
`-211,-212,-213,-214`. I checked this ordering in the accepted parent proof
and its independently reconstructed lexicographic clause layer.

For distinct red triangles `i,j`, let `k,l` be the other two. Three fixed
vertices whose signatures are either `{i}` or `{i,j}` are pairwise blue:
a red edge between two of them together with the red triangle `C_i` would be
a red `K5`. They are blue to both `C_k` and `C_l`. Some edge between those
triangles is blue, since otherwise their union is a red `K6`; this edge and
the three fixed vertices form a blue `K5`. Hence

```text
x_i + y_ij <= 2.
```

For every triple of fixed vertices and ordered pair `i != j`, the published
nine-literal clause is false exactly when all three signatures lie in
`{{i},{i,j}}`; coordinate `j` is genuinely free. The checker exhausts all
`12 * 16^3 = 49,152` complete signature assignments. It reconstructs the
literal core-123 graph, checks all 792 five-sets, and supplies a blue cross
edge for each of the twelve ordered pair applications.

[`independent_check.py`](independent_check.py) imports no reviewed producer.
It recovers all 320 primary-variable meanings from the actual order-three
edge orbits, verifies the closed link formula
`211 + 11*(fixed-33) + cycle`, and generates the four units plus all 1,440
pair cuts independently.

## Complete certificate check

The inherited core-123 base from the previously accepted propagation review
has 34,290 variables, 615,988 clauses, and SHA-256
`b8402d03f41d78dbcef98cf9c55db5b18ed8864122f017ac52adbe0075c699b7`.
The independent generator retains every base clause and adds exactly 1,444
clauses without auxiliary variables. Its 617,432-clause result is byte-for-byte
the published formula, SHA-256
`d103da79b90dbb5d3f8bb9822a90d3b387823eee866af0c3f991f2d7f3db25f1`.

With one process active, an independently built Kissat 4.0.4 binary returned
UNSAT and regenerated the exact published 19,801,958-byte trace, SHA-256
`e7f7293e5a6de165c219f34af9284051a626d6877d6b1a50aca417c44933a700`.
Full sequential `drat-trim` replay returned `s VERIFIED`, using 673 RAT core
lemmas. The reviewer used a 60-second safety cap; the run took about 20
seconds, so the publication's exact 20-second performance boundary is not
part of this verdict. Normal and optimized CPython produced identical compact
reports.

Compact results are in [`result.json`](result.json). The CNFs, proof, binaries,
and logs remain outside Git.

## Reproduction

From the repository root, regenerate only the accepted core-123 inherited
base, rather than solving the other 25 inconclusive cases:

```bash
export REVIEW_WORK=/scratch/new-r55-empty-propagation-review1
export R55_KISSAT=/path/to/kissat-4.0.4
export R55_DRAT=/path/to/drat-trim
mkdir -p "$REVIEW_WORK/inherited"
python3 -B - <<'PY'
from pathlib import Path
import os, sys
root = Path.cwd()
sys.path.insert(0, str(root / "ramsey_r55_order3_eleven_anchor_propagation"))
import run, cube
work = Path(os.environ["REVIEW_WORK"]) / "inherited"
run.prepare(work)
case = next(row for row in cube.cases() if row["index"] == 123)
run.make_case(work, case)
PY
python3 -B ramsey_r55_order3_eleven_empty_propagation_review1/independent_check.py \
  --base "$REVIEW_WORK/inherited/c123.cnf" \
  --formula "$REVIEW_WORK/c123.review1.cnf" --generate \
  --cases ramsey_r55_order3_eleven_empty_propagation/cases.json \
  --noempty-boundary ramsey_r55_order3_eleven_noempty_rigidity/boundary.json \
  --report "$REVIEW_WORK/preproof.json"
set +e
"$R55_KISSAT" --time=60 "$REVIEW_WORK/c123.review1.cnf" \
  "$REVIEW_WORK/c123.review1.drat" > "$REVIEW_WORK/solve.log" 2>&1
solver_rc=$?
set -e
test "$solver_rc" -eq 20
"$R55_DRAT" "$REVIEW_WORK/c123.review1.cnf" \
  "$REVIEW_WORK/c123.review1.drat" > "$REVIEW_WORK/replay.log" 2>&1
python3 -B ramsey_r55_order3_eleven_empty_propagation_review1/independent_check.py \
  --base "$REVIEW_WORK/inherited/c123.cnf" \
  --formula "$REVIEW_WORK/c123.review1.cnf" \
  --cases ramsey_r55_order3_eleven_empty_propagation/cases.json \
  --noempty-boundary ramsey_r55_order3_eleven_noempty_rigidity/boundary.json \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-log "$REVIEW_WORK/solve.log" \
  --proof "$REVIEW_WORK/c123.review1.drat" \
  --replay-log "$REVIEW_WORK/replay.log" \
  --report "$REVIEW_WORK/result.json"
diff <(jq -S . ramsey_r55_order3_eleven_empty_propagation_review1/result.json) \
  <(jq -S . "$REVIEW_WORK/result.json")
(cd ramsey_r55_order3_eleven_empty_propagation_review1 && \
  sha256sum -c SHA256SUMS)
```

## Imported trust and uncertainty

Independently checked here are the consequence proof, core-123 literal graph,
variable decoding, exact tail, complete formula identity, fresh solver trace,
and full proof replay. Imported trust remains in the accepted complete parent
and 197-class cover, the inherited strengthened core-123 base, the accepted
forced-empty theorem, the fixed-row normalization, the degree window using
`R(4,5)=25`, compiler/runtime/hardware, SHA-256, and `drat-trim`. The older
empty-signature exclusions remain the explicit boundary for cumulative counts.
This is ordinary unformalized and computer-assisted review, not proof-assistant
formalization.

Reviewer: `reviewer-1`, 2026-09-05.
