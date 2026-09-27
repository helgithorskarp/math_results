# An unbounded Gaussian beta region

The [author proof](PROOF.md) establishes, for every bounded R3 probability
law, every 1-Lipschitz image, and every Gaussian variance,

```
b_(j+k,j) >= 0 whenever k>=1 and j+2>=30720 k^3.
```

The sign is strict unless every support distance is preserved. The signed
width therefore grows without bound with the cube root of the base count.
This is a single parametric theorem, with no support-size or radius restriction.
The constant is conservative; no optimality is claimed.

The analytic mechanism localizes the negative part of a derivative polynomial
near a mode of a genuine Gaussian location mixture. A radial polynomial with
one sign change has a positive Gamma(3) average; every displacement of the
marked Gaussian pair preserves that sign. The argument controls all orders
and all real base counts above the stated bound. It uses more than the
scalar replica constraints and does not assert conditional-kernel positivity.

This is a complete author argument awaiting independent review. It does not
complete every base of the eighth diagonal, prove full majorisation, or give
a new Kneser--Poulsen consequence. The covered beta laws approach the endpoint
u=1 rather than every interior threshold. Existing seven-factor and finite-row
results remain credited in [SOURCES.md](SOURCES.md).

## Reproduction

Use CPython 3.11 or later, standard library only. From this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
python3 -B verify.py --base 15728640 --order 8
python3 -B verify.py --base 15728639 --order 8
```

The full audit compares its exact record to [EXPECTED.json](EXPECTED.json)
and reports `CUBIC_BETA_ANALYTIC_CONTROLS_PASS`. It checks polynomial/Gamma
identities through order24,72 constant controls,72 Gaussian product identities,
36 independent noncentral Gaussian calibrations, and12 rejection/boundary
controls. The last two commands return `CUBIC_REGION_CERTIFIED` and
`NOT_COVERED`. The latter means only that this theorem's sufficient guard fails.

The index consumer assumes the mathematical bounded-law/contraction hypotheses;
it does not infer them from indices. The written localization, integration,
one-crossing argument and universal quantifiers are the proof. Finite exact
checks support that proof; they are not a numerical cover of all laws or orders.
No solver, quadrature, external package, dataset or large certificate is used.
[DEPENDENCIES.json](DEPENDENCIES.json) records source provenance; the checker
needs only this packet. [SHA256SUMS](SHA256SUMS) pins its public bytes.
