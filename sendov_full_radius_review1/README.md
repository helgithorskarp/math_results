# Independent full-radius Sendov energy review

Actual agent **six-reviewer-1**, role **independent mathematical reviewer**.
[REVIEW.md](REVIEW.md) confirms the degree-nine full-disk small-energy
minimizers and true stability for every marked radius5/8<=a<=1, with
explicit sufficient uniform cost coefficients and a simpler fine-support
proof. The unrestricted first-power Tang--Zhang endpoint remains open.
Thresholds are existential; the proof is ordinary and unformalized.

From repository root, CPython3.11+ standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 python3 -B sendov_full_radius_review1/audit.py \
  --check sendov_full_radius_review1/expected.json
```

The checker derives the full radius/moment/mean/inward quartic from a simple
far-root secular equation and full matrix-word traces. It reads no author
code or fixture. Complete [expected.json](expected.json) records17 symbolic identities and
48 independent integer Gaussian trace controls (65 equalities),8 full linear compression
basis controls and5 damaged-expression rejections. Normal and optimized
output are byte-identical. Mathematical uniformity and completeness are
proved in the review, not inferred from these controls.

Optional entrywise comparison of16 complete author coefficient records:

```sh
python3 -B -O sendov_full_radius_review1/compare_coefficients.py
```

This requires the original author expected.json at the exact hash recorded
in [provenance.json](provenance.json). [coefficient_comparison.json](coefficient_comparison.json)
records the completed comparison. Author executable code is not imported.
[SHA256SUMS](SHA256SUMS) covers compact source. No large generated data,
external package, solver, private operational state or credentials is needed.
