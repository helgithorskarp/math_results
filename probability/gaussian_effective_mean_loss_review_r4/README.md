# Independent review of the effective Gaussian mean-loss guard

[REVIEW.md](REVIEW.md) accepts R3's
[effective mean-loss theorem](../gaussian_effective_mean_loss/PROOF.md)
in its stated scope. The source commit and ten public inputs are pinned
in [TARGET_INPUTS.json](TARGET_INPUTS.json).

The theorem supplies an explicit cutoff at every fixed radius, positive
covariance floor and positive lower threshold, allowing rare finite moves.
Its dyadic corollary is

```text
centered radius <= sqrt(s)/2, Cov(X)/s>=2^-15 I,
0<=d=E Delta_raw/s<=2^-360
  => H(u)>=2^-40 d on [1/64,1/2], H(u)>=0 for u>=1/64.
```

The review audits the interval-slice sign, all seven cutoff inequalities,
the unbalanced eight-site parameter family, and the 19-pair guard
preservation. [PROJECTION_CONTROL.md](PROJECTION_CONTROL.md) preserves a
separately derived, coarser proof using background projection and actual-set
polarization. It is supplementary author mathematics, not another claimed
advance or a replacement for the target's sharper cutoff.

Covariance collapse, positive loss outside the guard, low thresholds,
and unrestricted dimension-three majorisation remain unresolved. No new
Kneser--Poulsen conclusion or historical priority is asserted.
[SOURCES.md](SOURCES.md) identifies the shared dependencies.

Reproduce with standard-library CPython 3.11 or later:

```sh
cd probability/gaussian_effective_mean_loss_review_r4
python3 -B independent_check.py
python3 -B -O independent_check.py
python3 -B projection_controls.py
python3 -B -O projection_controls.py
sha256sum -c SHA256SUMS
```

Expected results are `EFFECTIVE_MEAN_LOSS_R4_REVIEW_PASS` and
`EXPLICIT_RARE_MOVE_CONTROLS_PASS`, matching [EXPECTED.json](EXPECTED.json)
and [PROJECTION_EXPECTED.json](PROJECTION_EXPECTED.json), respectively.
Neither checker imports target code. Both use exact standard-library
arithmetic, reject adverse controls, and leave the continuum analytic
claims as written mathematics. No quadrature, solver or large data is used.
