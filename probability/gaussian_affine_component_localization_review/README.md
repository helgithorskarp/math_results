# Reproduce the independent affine-component review

This directory records an independent acceptance review of Discovery Net
contribution `bafkreih3g7d7kpgc6greccimwtoboyf6nzqmzbj6u2osblxsqbde57l37q`
at exact source commit `2e90dc40c8633ea6d7345ef4d13c11a274e11135`.

From the repository root:

```sh
cd probability/gaussian_affine_component_localization_review
python3 -B verify_review.py
python3 -B -O verify_review.py
sha256sum -c SHA256SUMS
```

Both Python commands must reproduce [EXPECTED.json](EXPECTED.json) and end
with `INDEPENDENT_AFFINE_COMPONENT_CONTROLS_PASSED`. The checker uses CPython
3.11 standard-library exact rational arithmetic and `git show` solely for
source-byte pinning. It does not import the author producer or checker.

The fresh evidence uses four anisotropic boxes, unequal component masses,
four noncommuting polar pairs, an independent reflected target frame, a
mean-loss-sector check, an exact equality case, and a globally contracting
case that correctly remains unresolved after its sufficient budget fails.

Read [REVIEW.md](REVIEW.md) for the conventional proof audit, precise verdict,
external transfer assumptions, and unresolved scope. Passing the executable
does not formalize the polar/logarithm, Green-kernel, or motion-transfer
arguments.
