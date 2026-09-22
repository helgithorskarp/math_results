# Two-scale fixed-point and excedance law for 123-avoiding permutations

For a uniform 123-avoiding permutation conditioned to have two fixed
points `a < b`, let `D = b-a` and let `E` be its number of excedances.
We prove

$$
\left(\frac D{\sqrt n},\frac{a+b-n-1}{n^{1/4}},
                  \frac{2E-n+2}{n^{1/4}}\right)
\Longrightarrow
\left(R,\sqrt{R/2}Z_1,\sqrt{R/2}Z_2\right),
$$

where `Z1,Z2` are independent standard normals independent of `R`, and
`R` has density `4*r^2*exp(-r^2)/sqrt(pi)` on the positive half-line.
The midpoint and excedance displacements fluctuate on the quarter-power
scale, inside the known square-root-scale separation of the fixed points.

[PROOF.md](PROOF.md) gives a uniform three-variable local limit, including
the lattice factor, and an `O(n^(-1/2))` total variation approximation by
two binomial variables conditioned on parity when `D/sqrt(n)` stays in
a compact subset of `(0,infinity)`. A global distance envelope supplies
tightness and justifies normalization. The infinite claim rests on this
analytic proof, not finite numerical extrapolation.

[SOURCES.md](SOURCES.md) credits Li's existing exact joint enumeration
and Hoffman--Rizzolo--Slivken's existing Brownian-excursion distance law.
The finer joint law and local theorem are apparently new relative to the
checked sources. Independent researcher review remains outstanding.

## Reproduce the finite checks

Python 3.11 or later, standard library only. From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py --check-expected
sha256sum -c SHA256SUMS
```

Expected status: `ALL_EXACT_CHECKS_PASSED`. The complete compact record
is [expected.json](expected.json). The checker compares literal forbidden
subsequence filtering through size nine with a separate maximum-insertion
generator; it audits every joint count through size twelve. It also checks
ballot counts against nonnegative-walk dynamic programming, the exact
ballot ratios and rational product, central maxima, the full parity lattice,
and Vandermonde normalization. Checks remain active with Python `-O`.

Files:

- [counts.py](counts.py): exact integer implementation of the prior kernel.
- [literal_audit.py](literal_audit.py): independent permutation and walk
  objects; imports no counting formula.
- [verify.py](verify.py): comparisons and deterministic record generation.
- [diagnostics.py](diagnostics.py): optional finite-size decimal diagnostics.

To inspect convergence of local ratios and total variation numerically:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 diagnostics.py
```

These diagnostics use exact counts followed by ordinary floating-point
conversion and exponential evaluation. They provide no interval bounds
and are not proof dependencies. At the smallest sizes a requested atom
can lie outside the finite support; the output labels this explicitly.
No solver, external data file, omitted
certificate, or large computation is required. The proof is not formalized;
its boundary ranges and convergence-rate limitations are stated explicitly.
