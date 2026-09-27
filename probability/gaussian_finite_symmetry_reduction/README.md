# Full finite symmetry retains the full Gaussian counterexample question

Author proof, 27 September 2026; independent review pending.

At every fixed positive variance, the supremal Gaussian-majorisation
defect is unchanged if both endpoint laws are invariant under all 48
signed coordinate permutations, have mean zero and scalar covariance,
and their contraction is globally equivariant. The laws can be finite
with rational centres and weights at variance one.

Both radius-to-covariance ratios are uniformly bounded. After a common
rescaling, the full question is equivalent to the class with source
covariance **I**, support in **B(0,2)**, and all positive variances. The
same supremal defect is retained. This removes covariance degeneracy
from a complete test class; it does not bound the variance away from zero.

[PROOF.md](PROOF.md) gives an explicit construction preserving the entire
hinge-difference curve, after dividing its threshold by 48, up to

    47 exp[-(L/2-2R)^2/(8s)].

Every old component is copied and the copy centres contract by one half.
The guard L>=16R ensures all cross-component pairs contract strictly.
The error tends to zero without changing the Gaussian variance. There
is no factor 1/48 in the surviving defect. Thus a bound on the symmetric
class bounds the unrestricted supremum by the same constant.

No adverse input is supplied. The full conjecture remains open. This is
neither radial symmetry nor the previously signed Coxeter orbit-alignment
map. Representative configurations retain their original difficulty;
the atom count increases by 48 and no fixed radius bound is imposed.
See [HANDOFF.md](HANDOFF.md) for the precise proof obligation and limits.

From this directory, using Python 3.11 or later and only its standard library:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B verify.py INPUT.json
sha256sum -c SHA256SUMS
```

The outputs reproduce [EXPECTED.json](EXPECTED.json), status
`FINITE_SYMMETRY_DEFECT_CONTROLS_PASS`. The checker constructs 384 exact
rational labels from an existing asymmetric eight-site contraction,
checks every pair, all group actions, scalar covariances, and the margin
schedule, including the uniform radius-to-covariance guard. Rational
scalar hinge controls check the interaction inequality;
they are not Gaussian counterexamples. Invalid geometry and insufficient
budgets are rejected without relying on Python assertions.

The continuum theorem, Gaussian tail bound, Kirszbraun extension and
limiting arguments are written proof obligations, not formalized or
independently reviewed by these author controls. No quadrature, solver,
search census, external dataset or large omitted artifact is used.
Attribution and scope are in [SOURCES.md](SOURCES.md).
