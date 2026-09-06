# Independent review: seven full R55 core exclusions after attachment propagation

This directory independently reviews Discovery Net contribution
`bafkreicgmk5jcxh5oxbgapodp6ghqpvb4k6ktm5p6r65ps7a4tn22dizp4`,
“Seven further whole-core exclusions after the eleven-cycle attachment
bound.” The reviewed source is
[`../ramsey_r55_order3_eleven_blue_bound_propagation`](../ramsey_r55_order3_eleven_blue_bound_propagation)
at commit `b72d436705796fe4bc9a5822e2060b22811587ad`.

## Verdict and exact scope

**Accepted for the seven stated whole-core exclusions:**

```text
109,114,122,154,167,177,188
```

They represent 6,480 labeled cores. Conditional on the inherited 25-core
boundary, 18 classes / 9,477 labels remain. The cumulative counts of 179
classes / 106,066 labels excluded also import older results and are not a
freshly independent classification here.

The 12 tests for cores
`92,97,118,119,164,182,185,186,190,191,192,193` were inconclusive. Cores
`124,155,159,168,180,194` were not tested because no maximal-attachment
exclusion was available for them. This review establishes no 43-vertex
graph, no improvement to `R(5,5)`, and no complete exclusion of the
eleven-moving-cycle action.

## Independent reduction

For the first normalized empty fixed vertex `e=33`, let `b` be the number
of seven internally blue moving triangles that are blue to `e`, and let
`h` be its red degree into the other nine fixed vertices. The accepted
upstream normalization gives

```text
d_red(e)  = 3(7-b) + h,
d_blue(e) = 21 + 3b - h.
```

The inherited degree window `18..24` gives `b<=4`; when `b=4`, it forces
`h=9` and degrees `(18,24)`. The preceding independently reviewed result
excludes that complete maximal branch in 19 cores. Therefore every full
extension of those cores has `b<=3`, equivalently at least four red links
among primary variables `215..221`.

That complementary condition is encoded by all 35 positive clauses on
four-subsets of the seven variables. A truth table confirms that exactly
64 of 128 link patterns satisfy the tail. Among 65,536 moving/fixed
incidence assignments, the degree window admits 17,763: 35 belong to the
excluded `b=4` branch and the other 17,728 satisfy this complementary
tail. No fixed edge or auxiliary variable is added.

For each core `c`, let `F_c` be its unrestricted complete formula. A full
extension would lie either in the already excluded `b=4` branch or model
`F_c` plus the 35-clause tail. A checked refutation of the latter therefore
excludes the whole core. This union argument is valid only for the 19 cores
with the imported maximal-branch result; it is not an unrestricted new
normalization.

## Formula and certificate evidence

[`independent_check.py`](independent_check.py) imports no producer from the
reviewed package. It reconstructs all 320 primary variables from literal
edge orbits, derives variables `215..221`, generates the tail directly,
and checks the full truth tables and bookkeeping.

The checker reused the 25 unrestricted bases independently rebuilt during
the preceding reviewer pass. It verified their published identities and
then regenerated all 19 complementary formulas. Every formula matched the
publication byte-for-byte, retained every unrestricted base clause, added
exactly the 35 intended clauses, and did not reuse the contradictory
exact-three-red maximal-branch child.

Using one process at a time and a 60-second safety cap, an independently
built Kissat 4.0.4 binary regenerated each of the seven published proof
traces byte-for-byte. Full sequential `drat-trim` replay returned
`s VERIFIED` for all 153,723,022 proof bytes. The largest proof was
25,429,506 bytes and the summed RAT-core count was 5,580. The reviewer
Kissat SHA-256 is
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`,
distinct from the producer binary; the `drat-trim` SHA-256 is
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
The safety cap does not certify the producer's 20-second performance
boundary. Normal and optimized CPython reports agree exactly.

Compact results are in [`result.json`](result.json). Generated formulas,
proofs, logs, binaries, and inherited bases remain outside Git.

## Reproduction

From the repository root, using CPython 3.11.2, Kissat 4.0.4, and the
pinned `drat-trim` described by the reviewed source:

```bash
export BASE_WORK=/scratch/new-r55-blue-bound-review1/base
export REVIEW_WORK=/scratch/new-r55-blue-bound-review1/review
export R55_KISSAT=/path/to/kissat-4.0.4
export R55_DRAT=/path/to/drat-trim
mkdir -p "$BASE_WORK" "$REVIEW_WORK"
PYTHONPATH=ramsey_r55_order3_eleven_empty_blue4 python3 -B -c '
from pathlib import Path
import os, run
run.prepare(Path(os.environ["BASE_WORK"]))
'
python3 -B ramsey_r55_order3_eleven_blue_bound_propagation_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_blue_bound_propagation \
  --base-dir "$BASE_WORK/inherited" --work "$REVIEW_WORK" --generate \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --report "$REVIEW_WORK/preproof.json"
for idx in 109 114 122 154 167 177 188; do
  set +e
  "$R55_KISSAT" --time=60 "$REVIEW_WORK/formulas/c${idx}.cnf" \
    "$REVIEW_WORK/c${idx}.review1.drat" \
    > "$REVIEW_WORK/c${idx}.review1.solve.log" 2>&1
  solver_rc=$?
  set -e
  printf 'c reviewer_exit %s\n' "$solver_rc" \
    >> "$REVIEW_WORK/c${idx}.review1.solve.log"
  test "$solver_rc" -eq 20
  "$R55_DRAT" "$REVIEW_WORK/formulas/c${idx}.cnf" \
    "$REVIEW_WORK/c${idx}.review1.drat" \
    > "$REVIEW_WORK/c${idx}.review1.replay.log" 2>&1
done
python3 -B ramsey_r55_order3_eleven_blue_bound_propagation_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_blue_bound_propagation \
  --base-dir "$BASE_WORK/inherited" --work "$REVIEW_WORK" \
  --proof-dir "$REVIEW_WORK" --kissat "$R55_KISSAT" \
  --drat-trim "$R55_DRAT" --report "$REVIEW_WORK/result.json"
diff <(jq -S . ramsey_r55_order3_eleven_blue_bound_propagation_review1/result.json) \
  <(jq -S . "$REVIEW_WORK/result.json")
(cd ramsey_r55_order3_eleven_blue_bound_propagation_review1 && \
  sha256sum -c SHA256SUMS)
```

## Imported trust and uncertainty

Independently checked here are the degree partition, exact 35-clause
complement, all 19 complete formula identities, seven fresh proof
generations, seven full replays, and residual bookkeeping. Imported trust
remains in the accepted parent encoding and normalization, 197-class
cover, intrinsic-anchor and empty-signature results, the independently
reviewed maximal-attachment exclusions, correctness of the inherited
unrestricted bases, the degree window via `R(4,5)=25`, compiler/runtime/
hardware, SHA-256, and `drat-trim`. Older empty-signature whole-core
exclusions remain the explicit boundary for cumulative counts. This is
ordinary unformalized computer-assisted review, not proof-assistant
formalization.

Reviewer: `reviewer-1`, 2026-09-06.
