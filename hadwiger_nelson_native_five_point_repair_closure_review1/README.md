# Independent review: native B503 plus five host-point closure

## Verdict

**ACCEPT, high confidence, at target commit
`eec9c1061dcbc4bc63e7cbaad44553ce4f47996d`.** For the explicit 503-point
base `B` and 3,919-point native contact host `H`, every induced strict
unit-distance graph on `B union S`, with `S` contained in `H minus B` and
`|S| <= 5`, is four-colourable.

This is a useful negative result for one record-repair architecture. It does
not produce a five-chromatic graph, improve Parts' 509-vertex record, or
exclude changing the base, deleting a base point, or using points outside
this host. A later author-side package at commit `c418ae6` claims the stronger
six-addition closure; that new theorem is outside this review.
[REVIEW.md](REVIEW.md) gives the exact scope,
proof audit and limitations.

The standalone [independent_check.py](independent_check.py) imports no code
from the target package. It regenerates the exact host through the byte-pinned
checker from the already accepted independent review of the parent geometry,
checks all 7,677,321 physical pairs and all 126 partial colourings, grows
connected sets by a new canonical-tuple recurrence, and closes the remaining
weighted transversal after safe mask-dominance reduction.

## Reproduce

CPython 3.11 and only the standard library are needed for the independent
check:

```sh
python3 -B \
  hadwiger_nelson_native_five_point_repair_closure_review1/independent_check.py \
  --work /tmp/hn-native-five-independent --check-expected

python3 -B \
  hadwiger_nelson_native_five_point_repair_closure_review1/controls.py \
  --work /tmp/hn-native-five-controls
```

The full independent replay took 181 seconds and at most 437,236 KiB RSS on
the review host. Its stable result is [EXPECTED.json](EXPECTED.json). It
enumerates 1,856,054 distinct degree-qualified connected five-sets, checks
264,431,623 rare-bit completion candidates in the largest residual stage,
and rejects the final cost-five cover after 564,453 pair-pair cases.

The target's own normal and undefined-behaviour-sanitized replays also passed:

```sh
python3 -B hadwiger_nelson_native_five_point_repair_closure/verify.py \
  --work /tmp/hn-native-five-target

python3 -O -B hadwiger_nelson_native_five_point_repair_closure/verify.py \
  --work /tmp/hn-native-five-target-ubsan --sanitize --skip-python-cover

python3 -B hadwiger_nelson_native_five_point_repair_closure/controls.py \
  --work /tmp/hn-native-five-target-controls
```

The reviewer additionally compiled and ran the target's non-default full ESU
enumerator on the generated `tree-input.txt`. It found 1,856,054 qualified
connected five-sets and zero omission-cover survivors. After numerical
sorting, its complete triple and quadruple files were byte-identical to the
spanning-tree files, with hashes recorded in [VALIDATION.json](VALIDATION.json).

## Evidence boundary

The certificate's partial colourings are positive witnesses. The enumeration
and cover computations prove that every hypothetical counterexample is
contained in at least one such witness support; no claim that the 126 words
enumerate every four-colouring is made or needed. No SAT timeout, MILP status,
floating comparison, or abstract non-geometric graph is used in the accepted
theorem.

The ordinary Python/C++ executions, exact-arithmetic source, positive words,
and finite enumeration arguments remain the trust boundary. This review is
not a proof-assistant formalization.
