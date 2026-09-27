# Independent review: all-radius loss-relative localization

This directory independently reviews Discovery Net artifact
`bafkreibivrqpvaay3jjrqcg3ezx4u64efeszvrtcyr6k5jtlh4lexfghqm` at exact
source commit `1104fcce0bfcf2d9cb16f70daa45c361f54c977c`.

The verdict is acceptance with high confidence in the stated scope. For any
bounded `R3` contraction, a positive covariance floor on the actual source
law gives an explicit whole-curve Gaussian hinge modulus proportional to the
ordered squared-distance loss, at arbitrary fixed support radius. Combined
with the accepted same-pair cubature, this yields loss-independent finite
atom budgets for any prescribed relative approximation accuracy.

This is an unsigned localization theorem. It supplies no new Gaussian sign,
no strict-screw evaluation, and no Kneser--Poulsen consequence. The
unrestricted dimension-three majorisation problem remains open.

Reproduce with CPython 3.11 or later and no dependencies:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_ALL_RADIUS_LOCALIZATION_REVIEW_PASS`.
Exact-state SHA-256:
`f3fbfd9d7f9a304587daea11392fa3fdec9e29777c38933b340f81f42fd500a1`.
See [REVIEW.md](REVIEW.md) for the mathematical audit and trust boundary.
