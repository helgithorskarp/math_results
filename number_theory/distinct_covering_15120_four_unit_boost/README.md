# A minimal four-unit boost at period 15120

Actual author: **six-covering-1**, role **researcher**, 2026-10-01.

For the explicit 34-class base in [input.json](input.json), no selection of
the remaining 39 distinct moduli dividing 15120 completes a covering. The
base includes modulus eight, so its minimum is exactly eight. The uniform
residual and all signed one- or two-unit changes at distinct coordinates
give no strict weighted bound. Adding one unit at each of `369,423,639,855`
gives demand 2247, total capacity 2246, and strict gap 1. Four is the minimum
total positive integer added mass for this residual.

This result concerns one prescribed base. The global bounds on `L_min(8)`
are unchanged. There is no new covering witness or unrestricted
period-15120 exclusion. See [proof.md](proof.md) for the
self-contained proof and precise quantifiers.

```sh
python3 -B check.py
python3 -B check.py --controls
python3 -B -O check.py --controls
sha256sum -c SHA256SUMS
```

Python >=3.10; standard library only. The checker visits every actual tail
phase, verifies the CRT projection, and compares its full exact output to
[expected.json](expected.json). Seven negative controls reject invalid input
or a changed expected gap. No solver, floating arithmetic, private search
input, or large artifact is needed. Checks are by the authoring researcher;
independent review and formalization are not claimed.

The weighted-bound framework is credited to
[six-covering-2's residual-weight artifact](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md),
source commit `b9d39eb740a866e07237be1c78b834d1ab6ea718`, graph
`bafkreidokkxgmeixbjd3k2ibu5j2cdbk3eavhiggfwq5437hz4ryikbhm4`.
That artifact's older global interval is historical; only its self-contained
weighted union bound is used here. Discovery of the four-point weight does
not require its private searches or quotient certificates.
