# Gaussian contraction stability without a covariance hypothesis

For every probability law supported in a radius-`R` ball in `R^n`, every
1-Lipschitz map `T`, and every positive Renyi order, including Shannon and
infinity, the entropy lost after Gaussian smoothing controls the root mean
square distance from `T` to a rigid motion with exponent **1/4**. This
exponent is optimal. No positive covariance lower bound is required.

The proof gives dimension-free lower bounds for entropy loss in terms of
mean squared-distance loss, uniformly over entropy orders bounded away from
zero. Its geometric ingredient has the best possible constant:

```text
rho^2 <= sqrt(2n) R sqrt(D),
rho = inf_(Q in O(n), b) (E|T(X)-QX-b|^2)^(1/2),
D = E[|X-X'|^2-|T(X)-T(X')|^2].
```

A single sparse coordinate-folding family proves both the optimal constant
and the sharp entropy exponent, with an explicit second-order entropy
expansion at every order. The resulting `n^(1/4)` dimension growth is also
necessary for a uniform bound of this form.

**Status:** complete author proof, awaiting independent review; not
formalized. This generalizes the
[reviewed covariance-dependent result](../gaussian_contraction_rigidity/PROOF.md).
Qualitative entropy monotonicity, the contracting lift, and the
Powers–Stormer matrix inequality are credited prior work. Neither the
entropy constants nor historical priority is claimed optimal or settled.

Read [PROOF.md](PROOF.md) for statements and proofs,
[SOURCES.md](SOURCES.md) for attribution, and [VALIDATION.md](VALIDATION.md)
for the finite checks and their limits.

## Reproduction

CPython 3.11.2; Python standard library only. From this directory:

```sh
python3 verify.py > /tmp/gaussian-covariance-free.json
diff -u EXPECTED.json /tmp/gaussian-covariance-free.json
python3 -O verify.py > /tmp/gaussian-covariance-free-optimized.json
diff -u EXPECTED.json /tmp/gaussian-covariance-free-optimized.json
sha256sum -c SHA256SUMS
```

The program computes its results without reading `EXPECTED.json`. All
arithmetic is rational or integer, including explicit exponential and
logarithm enclosures. Formal exponential polynomials independently verify
the sparse-family Taylor coefficients using Gaussian replica integrals.
The universal theorem is established by the written analysis, not these
finite checks. No solver, external dataset, omitted certificate, or
floating-point inference is used.
