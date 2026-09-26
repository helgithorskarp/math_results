# An exact obstruction to positive endpoint scatter certificates

For the two-point collapse `{ -e1, e1 } -> {0}` with equal masses, the
actual Gaussian beta `b_(7,0)` is **strictly positive at every variance**.
Nevertheless, after full endpoint and weight averaging, its integrated
scatter spectrum is negative on the explicit interval `[33/25,27/20]`.
An exact derivative certificate proves that `b_(7,0)(tau)/tau^2` has **no
representation as a Laplace transform of a nonnegative measure**, where
`tau=1/s` is inverse variance.

[PROOF.md](PROOF.md) explains the finite reduction and what it excludes:
the proposed scatter-order route to signs at all variances. It does not
exclude other endpoint couplings or refute Gaussian majorisation. The first
generally unsigned beta and the full R3 conjecture remain open.

Author proof; independent review pending. This is a method obstruction,
not a new positive class, an extra edge strip, or a negative Gaussian beta.

From this directory, with Python 3.11 or later and only its standard library:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Expected: `ENDPOINT_SCATTER_OBSTRUCTION_EXACT_PASS`.
[The compact certificate](CERTIFICATE.json) contains the exact radical
expressions, outward rational bounds, negative interval and compressed
Gamma-concentration witness. [EXPECTED.json](EXPECTED.json) pins its hash.
The code checks all 1020 ordered replica assignments against 52 binomial terms,
then checks every knot in the claimed interval and three corrupt certificates.
It uses no numerical Gaussian integration, symbolic differentiation of the
large derivative order, external data or sibling code. These are author
checks; Gaussian integration, differentiation and Jensen's inequality remain
written mathematical premises. The checks take under a second on the author's
host. [SOURCES.md](SOURCES.md) records the current dependency context.
