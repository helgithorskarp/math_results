# The four remaining ten-cycle extensions are excluded

All four surviving full-extension formulas for an order-three action
`1^13 3^10` returned UNSAT, and all four DRAT proofs passed replay.
The new ingredient is twelve unit clauses obtained from the independently
reviewed fixed-signature bound: the first three fixed vertices in the
existing normalization are blue to the entire twelve-vertex minority core.

Combined with the preceding internal-color, matching and phase reductions,
this closes the ten-moving-cycle type. Together with the earlier
minimum-ten result, an order-three automorphism of a hypothetical
Ramsey `(5,5;43)` graph must therefore have **at least eleven moving
3-cycles**. Eleven through fourteen remain open globally; in the separate
M=214 hard branch, only eleven or twelve remain after the existing
conditional upper bound. No 43-vertex graph or Ramsey lower-bound
improvement is claimed.

The **principal inherited trust boundary is the older four-versus-six
internal-color split**. Its five exclusions were internally reconstructed
and proof-checked, but the later independent reviews explicitly did not
rerun those five exclusions. This pass adds internally checked certificates
for the remaining four-versus-six branch, not an independent review of
that antecedent. Read the reduction and normalization in [PROOF.md](PROOF.md).

## Full-formula result

Each case contains 28,974 variables and 927,346 clauses. It preserves all
parent five-set constraints, auxiliary gates, and fixed-vertex degree
counters. Formula hashes, complete tool/source hashes, exact timing and
proof provenance are in [sweep_result.json](sweep_result.json).

| case | inherited anchor | solver seconds | full DRAT replay seconds | outcome |
|---:|---:|---:|---:|---|
| 0 | 64 | 82.785 | 78.979 | verified UNSAT |
| 1 | 65 | 101.303 | 107.430 | verified UNSAT |
| 2 | 67 | 43.809 | 48.728 | verified UNSAT |
| 3 | 69 | 39.195 | 46.521 | verified UNSAT |

The bounded run used two workers and 120-second solver and replay limits
per case. It completed in 323.004 seconds, with largest child peak RSS
495,876 KiB. Every case finished; none was classified by a timeout.
The four original traces total 288,130,873 bytes and remain outside Git.

## Reproduce

Use Python 3.11.2 (standard library), GCC 12.2.0, Kissat 4.0.4 from
source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim from
source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Run from this directory,
with the sibling dependency directories present. Set `KISSAT` and
`DRAT_TRIM` to the corresponding executable paths.

```bash
python3 solve.py --work /tmp/r55_k10_signature/full \
  --kissat "$KISSAT" --drat-trim "$DRAT_TRIM" \
  --workers 2 --solve-seconds 120 --replay-seconds 120
python3 check_layer.py --base /tmp/r55_k10_signature/full/base.cnf \
  --work /tmp/r55_k10_signature/full --report /tmp/r55_k10_signature/layer.json
cmp layer_result.json /tmp/r55_k10_signature/layer.json
python3 controls.py --base /tmp/r55_k10_signature/full/base.cnf \
  --cnf /tmp/r55_k10_signature/full/case_00.cnf \
  --work /tmp/r55_k10_signature/controls --report /tmp/r55_k10_signature/controls.json
cmp controls_result.json /tmp/r55_k10_signature/controls.json
python3 certificate.py extract --sweep /tmp/r55_k10_signature/full \
  --output /tmp/r55_k10_signature/compact --drat-trim "$DRAT_TRIM" \
  --workers 2 --replay-seconds 600
python3 certificate.py verify --work /tmp/r55_k10_signature/verification \
  --certificates /tmp/r55_k10_signature/compact/certificates \
  --manifest /tmp/r55_k10_signature/compact/manifest.json \
  --drat-trim "$DRAT_TRIM" --replay-seconds 600
python3 support_controls.py --base /tmp/r55_k10_signature/full/base.cnf \
  --certificates /tmp/r55_k10_signature/compact/certificates \
  --manifest /tmp/r55_k10_signature/compact/manifest.json \
  --work /tmp/r55_k10_signature/controls --report /tmp/r55_k10_signature/support.json
cmp support_controls_result.json /tmp/r55_k10_signature/support.json
sha256sum -c SHA256SUMS
```

The solver run regenerates the complete base and compiles its independent
C++ reconstruction checker with `-std=c++17 -O2 -Wall -Wextra -Wpedantic
-Werror`. Each extended formula then passes a byte-prefix and semantic
clause-multiset check. Five malformed-formula controls exercise that
checker. Normal and optimized Python checks give identical reports.
The separate support control adds an unsupported empty core axiom and
updates its recorded hash; the checker still rejects it at clause
membership, rather than merely rejecting a digest mismatch.

The deterministic four formula hashes must match. Wall-time limits,
resource totals and solver trace hashes can depend on the host. A timeout
is explicitly OPEN and does not reproduce an exclusion; repeat in a fresh
work directory with an adequate limit if necessary. `--resume` requires
the exact saved contract, replays completed exclusions, and retains OPEN
statuses. A `STOP` file in the work directory prevents starting new cases;
active cases finish their bounded run. Every case and aggregate report
is checkpointed atomically. A SAT result must decode to a literal
43-vertex edge list and pass all five-set checks before being reported.

## Certificate availability and scope

Generated formulas, original traces, extracted cores/traces and logs are
kept outside Git. This directory publishes their generators, independently
checked support, hashes and compact reports. Reproduction therefore
requires generating the omitted evidence; the reports alone are not
standalone certificates. General DRAT, including RAT steps and deletions,
is required, not an addition-only RUP checker.

The extracted cores and proofs total 258,440,394 bytes. Every one of
79,653 core-clause occurrences is justified by its case's layer or the
fully reconstructed base; 30,528 distinct base obligations occur. The
extracted proofs have respectively 1,029, 1,297, 773 and 878 RAT core
lemmas. [certificate_manifest.json](certificate_manifest.json) records
every core/proof hash. [verification_result.json](verification_result.json)
records the fresh reconstruction, support check and final four replays.

The new unit consequence has a hand proof backed by a reviewed lemma.
The parent literal formula reconstruction and the new layer checker
address encoding errors; drat-trim addresses proof validity. These checks
do not formalize the normalization or remove dependence on the source,
compiler/runtime, proof checker and hardware. The new four-case result
has not yet received an independent peer review.

This completes one milestone. No eleven-cycle search or new hard-branch
profile phase is started here. The next symmetry frontier is eleven
moving cycles, after this closure and its inherited dependencies receive
the appropriate review attention.
