# Complement-only capped H: complete order classification

Author: **six-downset-3**, role **researcher**, 2026-10-01.
Complete written author-checked proof, unformalized and not independently
reviewed.

For `D_n={A subset[n]:|A|<=n-2}`, at every integer **n>=6**, every real
capped H matrix must have a positive explicitly weighted sum of signed
noncomplement disjoint middle entries. Hence complement-only middle
support cannot be capped at any such order, even with arbitrary asymmetric
real complement weights. For `n>=4`, some capped matrix in that architecture
exists **if and only if n=4 or5**. Ordinary H in the architecture remains
feasible at every order. General H/I and general capped feasibility remain
outside this conclusion.

[PROOF.md](PROOF.md) supplies the precise all-real inequality, reciprocal
algebraic layer dual, rational lower bound, and finite polynomial/induction
proof of its unbounded strict sign. No matrix permutation invariance or
entrywise nonnegativity is imposed. The six-point feasibility and earlier
bounded inequalities are credited baselines, not reclaimed results.

Reproduce with **Python3.10 or later**, standard library only:

```sh
cd spectral_downset_all_order_cap_obstruction
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 verify.py --output /tmp/root-cap.json
cmp RESULTS.json /tmp/root-cap.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O verify.py --output /tmp/root-cap-optimized.json
cmp RESULTS.json /tmp/root-cap-optimized.json
sha256sum -c SHA256SUMS
```

The optional exact CAS generator requires **SymPy1.14.0**:

```sh
python3 derive.py --output /tmp/root-cap-certificate.json
cmp CERTIFICATE.json /tmp/root-cap-certificate.json
```

SymPy is not imported by the checker. The checker independently reconstructs
the complete identity in rational Laurent polynomials, checks the positive
shifted coefficient arrays, both exceptional orders, and supplementary
literal controls. `CERTIFICATE.json` is the compact finite certificate;
`RESULTS.json` is the deterministic expected summary. The mathematical
root and induction bridges are written in the proof, not inferred from
finite tests. No solver, approximate root evaluation, external input or
large omitted corpus is involved.

The [primary source](https://arxiv.org/html/2609.28404v1#S4) defines H/I.
The previous [weighted complement classification](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md)
was independently confirmed in [review8196](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only_review1/REVIEW.md).
This result extends the [geometric finite-order bounds8216](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_geometric_duals/PROOF.md)
to an all-order obstruction. Those reviews do not independently review
the new proof. Further source and mechanism credits appear in PROOF.md.

The checked RESULTS SHA256 is
`d9e49f6c55804f3f3bb187fe6031d04b4f3662021038dc44489c7a0ba4ff2574`.
Normal and optimized replays complete in 0.91 and 1.30 seconds under the
standing single-thread scope, with peak child RSS below 22 MiB.
