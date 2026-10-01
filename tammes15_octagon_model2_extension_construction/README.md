# Exact fifteen-point extension of octagon model2

Author: **six-tammes-2**, role: **researcher**, 2026-10-01.

At cosine `59479/100000`, the eight-point thirteen-contact core from the
[earlier exclusion](https://github.com/helgithorskarp/math_results/blob/main/tammes15_octagon_model2_lower_strip_exclusion/PROOF.md)
admits seven additional unit points. The compact rational certificate
checks all 15 units and 105 pairs. Precisely the thirteen core contacts are
equalities; the remaining 92 inequalities are strict.

Together with that earlier exclusion, the prescribed core's fifteen-point
extension threshold satisfies `0.593 < kappa <= 0.59479`; [PROOF.md](PROOF.md)
defines kappa and proves attainment and the bracket. This does not improve
the global Tammes-15 bounds or assert any global or conditional optimum.

From the repository root, run:

```bash
python3 -B tammes15_octagon_model2_extension_construction/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B tammes15_octagon_model2_extension_construction/audit_native.py
```

The primary checker needs only the Python standard library. The separate
audit needs SymPy, tested with Python 3.11.2 and SymPy 1.14.0. The checkers
run sequentially in under one second in the author's constrained workspace;
they use no optimization, search output, private input or external data.

[certificate.json](certificate.json) is the complete witness.
[check.py](check.py) uses explicit core coefficients and rational chart
formulas. [audit_native.py](audit_native.py) independently encodes the core
as contact reflections, the extras as tangent stereographic images, and
the metric as all nine Gram entries. This is same-author validation;
independent peer review and formalization are pending.

[EXPECTED.json](EXPECTED.json) records the matching exact summaries.
Certificate SHA256:

```text
7d0d28d35f79595c446f96aeb98dd4ce774177fc7fcc6dc987f7ee46e48dd94a
```

No proof corpora or floating discovery data are required or included. All
published files are listed in [SHA256SUMS](SHA256SUMS).
