# What entropy control does not imply about Gaussian majorisation

This package audits the covariance-free Gaussian entropy-rigidity result
and identifies an obstruction to using energy comparisons alone to solve
the dimension-three conjecture of Aishwarya--Li.

**Explicit Gaussian example.** Two probability densities supported on six
unit cubes in `R^3`, smoothed by a Gaussian of variance `10^-8`, satisfy

```text
h_alpha(f) - h_alpha(g) > 4541/90000   for every 1 <= alpha <= infinity,
integral (g - 1/9)_+ - integral (f - 1/9)_+ < -4973/45000.
```

Thus all these entropy inequalities hold while majorisation fails. These
are **not a contraction pair** and do not refute the Gaussian-contraction
conjecture. The example excludes a bridge based only on these entropy
inequalities, even within Gaussian convolutions of bounded measures.
For any prescribed `a>0`, a sufficiently small variance gives the same
phenomenon simultaneously at all orders `alpha>=a`.

A second, exact finite-density example separates the **entire PC2 energy
class** from majorisation, including arbitrarily close pairs with entropy
gap tending to zero. This stronger energy-class statement is proved before
Gaussian smoothing; its persistence for all PC2 energies after smoothing
is not asserted.

[PROOF.md](PROOF.md) gives the examples and the exact missing condition:
the PC2 generators control positivity of an integrated threshold gap,
whereas majorisation requires that integral to be nonincreasing.
[AUDIT.md](AUDIT.md) records the independent audit of the preceding
covariance-free theorem and an unsigned approximate-majorisation consequence.
The named dimension-three problem remains open in this work.

## Reproduction

CPython 3.11.2, standard library only, from this directory:

```sh
python3 verify.py > /tmp/gaussian-bridge.json
diff -u EXPECTED.json /tmp/gaussian-bridge.json
python3 -O verify.py > /tmp/gaussian-bridge-optimized.json
diff -u EXPECTED.json /tmp/gaussian-bridge-optimized.json
sha256sum -c SHA256SUMS
```

The checker uses rational arithmetic and polynomial identities. The proof
of the continuum statements is analytic; no quadrature, large certificate,
external data, or proof-assistant formalization is involved. Sources and
the limits of the novelty search are in [SOURCES.md](SOURCES.md).
