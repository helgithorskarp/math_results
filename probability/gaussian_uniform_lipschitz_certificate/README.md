# Uniform eventual Gaussian majorisation from a Lipschitz bound

**Complete author proof; independent acceptance pending.**

For every bounded source law in R3 with centered radius R and positive
scatter `V=E|X-E X|^2`, and **every map with Lipschitz constant at most 1/6**,
full Gaussian majorisation holds simultaneously at every threshold and
every variance `s>=33792R^4/V`.

No covariance floor, martingale witness, minimum weight or atom bound is
required. The main [theorem](PROOF.md) allows every fixed Lipschitz bound
below `1/sqrt(27)`: a rational factor `0<q<1` satisfying

```
27 |y_i-y_j|^2 <= q^2 |x_i-x_j|^2
```

certifies all thresholds at `s>=4224R^4/((1-q)V)`. The universal spherical
comparison is `S_Y(lambda)<=q S_X(lambda)`, proved by symmetrizing independent
copies and averaging over orthonormal frames. No spherical quadrature enters.

This is a uniform map/law family at sufficiently large variance. It does
not settle unrestricted majorisation or imply a new Kneser--Poulsen result.
The preceding covariance/damping corollary is included; the more general
martingale route retains complementary scope. See [HANDOFF.md](HANDOFF.md)
and [SOURCES.md](SOURCES.md).

## Reproduction

Use standard-library CPython 3.11 or later. From this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B certificate.py FAMILY_INPUT.json
python3 -B verify.py --input FAMILY_INPUT.json --certificate FAMILY_CERTIFICATE.json
sha256sum -c SHA256SUMS
```

The control runs match [EXPECTED.json](EXPECTED.json) and print
`UNIFORM_LIPSCHITZ_ALL_THRESHOLD_PASS`. The producer matches
[FAMILY_CERTIFICATE.json](FAMILY_CERTIFICATE.json). Its separate supplied-record
checker imports no producer code and reconstructs scatter and radius using
ordered-pair identities.

Input fields are `sources`, `targets`, `weights`, `variance` and optional
`factor`. Numbers must be integers or rational strings. The producer computes
the exact maximum squared-distance ratio beta. When no factor is supplied,
it uses `(1+27 beta)/2`, valid for beta<1/27. Zero masses are removed.

`SIGNED_ALL_THRESHOLDS` includes the supplied variance.
`UNRESOLVED_AT_REQUESTED_VARIANCE` certifies only the future interval recorded
in the certificate. `UNRESOLVED` makes no sign assertion.
`ISOMETRIC_ZERO` and `POINT_TARGET_ALL_VARIANCES` are the elementary cases.
Failure of this sufficient test is not a Gaussian counterexample.

The witness has constant size, with O(n^2) exact operations and O(n) storage.
Bit cost depends on the rational inputs. Controls include singular source
covariance, extremely small weights, a whole thin-source parameter family
outside all endpoint martingale couplings, zero loss, exact factor boundaries
and damaged records. Their purpose is certificate validation; the uniform
theorem rests on the written proof and its accepted analytic endpoint.
