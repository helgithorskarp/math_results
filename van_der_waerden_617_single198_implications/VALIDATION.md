# Exact replay and regeneration

Actual agent **six-vdw-3**, role **researcher**. Validation date2026-10-01.
All mathematical arithmetic uses Python integers and standard libraries.
No numerical library or solver participates in the published proof or its
fresh generation. The separate checker imports no proposer.

Frozen replay and all controls passed with CPython3.11.2 in4.473 seconds,
peak RSS24168KiB. CPython3.11.2 with`-O` also passed in4.667 seconds,
peak RSS26464KiB. The exact checkers use explicit exceptions for proof
guards, so optimized execution retains them.

Fresh regeneration with isolated CPython3.12.14 passed in57.663 seconds,
peak child RSS66080KiB. All ten final compact proofs matched the frozen
bytes, including the complete entry-level decoded rows. Each raw proposal
and each pruned proposal was exactly checked before comparison. The two
representations are square-enumeration/bit-mask proposals and
Euler-character/actual-AP/dictionary verification. Every job ran serially
with one thread. The scoped proposal windows remained eight seconds and
400 probes; no CPU, memory or process limit was changed.

Each run rejected the same87 corruptions or incomplete proofs. These cover
wrong geometry and capacities, malformed APs and weights, missing terminal
ancestors, wrong inferred bits, duplicate seeds, hidden opposite-class caps
or roots, missing trial contradictions, wrong discharged literals,
unscoped nested trials, unrestricted-class terminals, Boolean tags and
extra premises. Every compact row round-trips entry by entry.

Independent small finite models checked2982 nonnegative-defect budget
inferences,18342 packing/forcing-set transfer inequalities and250 actual
AP-free reflection/complement count identities with poles. The21574 model
checks are supporting tests; the written lemma and exact full-size
certificates establish the mathematical claim.

[validation.json](validation.json) gives exact times, versions, hashes,
proof counts and fresh case comparisons. [controls-expected.json](controls-expected.json)
records the87 rejected cases and model counts. [expected.json](expected.json)
contains the complete deterministic mathematical result.

From repository root:

```sh
python3 van_der_waerden_617_single198_implications/reproduce.py \
  --work /tmp/vdw617-single198-replay
python3 -O van_der_waerden_617_single198_implications/reproduce.py \
  --work /tmp/vdw617-single198-optimized
python3 van_der_waerden_617_single198_implications/reproduce.py \
  --fresh --work /tmp/vdw617-single198-fresh
```

The612-phase combination imports prior mathematical proofs and pins their
unchanged summaries. It does not independently replay those prior families.
The new ten results and all selected base coefficients are replayed here.
Same-author separate checking and fresh regeneration do not constitute
external independent peer review or proof-assistant formalization.
