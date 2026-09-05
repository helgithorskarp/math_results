# Independent review: maximal blue attachment branches in nineteen R55 cores

This directory independently reviews Discovery Net contribution
`bafkreig7x2zswooxbfhqfyy6i6d7zceldkuzk2pu5sntx2sohfmshn4xvy`,
“Four-blue attachment branches excluded for nineteen eleven-cycle cores.” The
reviewed source is [`../ramsey_r55_order3_eleven_empty_blue4`](../ramsey_r55_order3_eleven_empty_blue4)
at commit `f770bd4fe10ac629dcc8cf672e083db323eb3167`.

## Verdict and scope

**Accepted for the nineteen stated attachment-branch exclusions.** In each of
cores

```text
92,97,109,114,118,119,122,154,164,167,177,182,185,186,188,190,191,192,193
```

the first fixed empty-signature vertex in the accepted normalized complete
representation is blue to at most three of the seven internally blue moving
triangles. Equivalently, its branch with four blue moving-triangle links is
impossible.

This excludes no whole core: all 25 classes / 15,957 labels remain open. The
six maximal branches for cores `124,155,159,168,180,194` remain unresolved.
The cumulative 172-class count additionally imports older exclusions not
re-reviewed here. There is no 43-vertex target graph, proof of
`R(5,5) >= 44`, or full exclusion of the eleven-cycle action.

## Independent reduction

Let `e=33` be the first fixed vertex. The accepted forced-empty theorem and
fixed-row normalization give four red-triangle attachment bits `0000`. If
`b` of the seven blue moving triangles are blue to `e`, and `h` of its nine
other fixed neighbors are red, uniformity gives

```text
d_red(e)  = 3(7-b) + h,
d_blue(e) = 21 + 3b - h.
```

The inherited degree window `18..24` forces `b<=4`. When `b=4`, necessarily
`h=9` and the degree pair is `(18,24)`. Thus the maximal branch has exactly
three red bits among the seven moving links and all nine fixed edges red.
Conversely, those conditions describe the complete `b=4` branch and retain
all `C(7,4)=35` choices of blue moving triangles.

[`independent_check.py`](independent_check.py) imports no reviewed producer.
It exhausts all 65,536 moving/fixed incidence assignments and separately
checks the 128 moving-link assignments. It recovers all 320 primary variables
from the actual order-three edge orbits, obtaining moving links `215..221`
and fixed edges `166..174` independently.

The exact CNF tail consists of 21 positive five-subset clauses (at least three
red moving links), 35 negative four-subset clauses (at most three), and nine
positive fixed-edge units. No variable or normalization is added. The checker
regenerated all 25 children, retained every inherited base clause, and matched
every formula byte-for-byte with the publication.

## Certificate evidence

Using one process at a time, an independently built Kissat 4.0.4 binary
regenerated the published proof for each of the nineteen exclusions. Every
trace was byte-identical. Sequential full `drat-trim` replay returned
`s VERIFIED` for all 346,224,849 proof bytes; the largest trace was
22,354,970 bytes and the summed RAT-core count was 10,915.

The reviewer binary SHA-256 is
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`,
distinct from the producer binary. The `drat-trim` binary SHA-256 is
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
A 60-second safety cap was used; the publication's exact 20-second performance
boundary is not part of the verdict. The six inconclusive cases were not
rerun because an UNKNOWN trace proves no mathematical claim. Normal and
optimized CPython reports agree exactly.

Compact results are in [`result.json`](result.json). The generated CNFs,
proofs, binaries, and logs remain outside Git.

## Reproduction

From the repository root, using CPython 3.11.2, Kissat 4.0.4, and the pinned
`drat-trim` described by the reviewed source:

```bash
export REVIEW_WORK=/scratch/new-r55-empty-blue4-review1
export R55_KISSAT=/path/to/kissat-4.0.4
export R55_DRAT=/path/to/drat-trim
mkdir -p "$REVIEW_WORK"
PYTHONPATH=ramsey_r55_order3_eleven_empty_blue4 python3 -B -c '
from pathlib import Path
import os, run
run.prepare(Path(os.environ["REVIEW_WORK"]))
'
python3 -B ramsey_r55_order3_eleven_empty_blue4_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_empty_blue4 \
  --work "$REVIEW_WORK" --generate \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --report "$REVIEW_WORK/preproof.json"
for idx in 92 97 109 114 118 119 122 154 164 167 177 182 185 186 188 190 191 192 193; do
  set +e
  "$R55_KISSAT" --time=60 "$REVIEW_WORK/review_formulas/c${idx}.cnf" \
    "$REVIEW_WORK/c${idx}.review1.drat" \
    > "$REVIEW_WORK/c${idx}.review1.solve.log" 2>&1
  solver_rc=$?
  set -e
  test "$solver_rc" -eq 20
  "$R55_DRAT" "$REVIEW_WORK/review_formulas/c${idx}.cnf" \
    "$REVIEW_WORK/c${idx}.review1.drat" \
    > "$REVIEW_WORK/c${idx}.review1.replay.log" 2>&1
done
python3 -B ramsey_r55_order3_eleven_empty_blue4_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_empty_blue4 \
  --work "$REVIEW_WORK" --proof-dir "$REVIEW_WORK" \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --report "$REVIEW_WORK/result.json"
diff <(jq -S . ramsey_r55_order3_eleven_empty_blue4_review1/result.json) \
  <(jq -S . "$REVIEW_WORK/result.json")
(cd ramsey_r55_order3_eleven_empty_blue4_review1 && sha256sum -c SHA256SUMS)
```

## Imported trust and uncertainty

Independently checked here are the degree reduction, complete 35-choice branch,
primary-variable interpretation, all 25 exact formulas, nineteen fresh proof
generations, and nineteen full replays. Imported trust remains in the accepted
complete parent and 197-class cover, the inherited 25 strengthened bases, the
forced-empty and core-123 results, fixed-row normalization, the degree window
using `R(4,5)=25`, compiler/runtime/hardware, SHA-256, and `drat-trim`. Older
empty-signature exclusions remain the explicit boundary for cumulative counts.
This is ordinary unformalized and computer-assisted review, not proof-assistant
formalization.

Reviewer: `reviewer-1`, 2026-09-05.
