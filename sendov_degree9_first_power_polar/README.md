# A first-power reciprocal estimate in degree nine

Researcher: **six-sendov-1**, role **researcher**, 29 September 2026.

For a degree-nine complex polynomial whose roots lie in the closed unit disk,
write its critical points, counted with multiplicity, as `zeta_1,...,zeta_8`.
At every root `a`, with zero denominators interpreted as infinity, the proof
and exact rational checks here establish

\[
\sum_{j=1}^8\frac1{|a-\zeta_j|}>\frac{46643}{6250}=7.46288.
\]

They also establish the full first-power bound, strictly, whenever
`|a| <= rho`, where `rho` is the unique solution in `(0,1/2)` of

\[
\int_0^1\bigl(\rho+(1-\rho^2)t\bigr)^8\,dt=1.
\]

An exact bracket is `0.4398 < rho < 0.4399`. At `|a|=1` the non-strict
first-power bound `sum >= 8` follows from the classical reciprocal identity.
These results do **not** prove the first-power bound throughout the intervening
annulus. The scalar polar relaxation used for the uniform constant has an
optimal constant between `0.93286` and `0.93287`; this is a limitation of the
relaxation, not a polynomial counterexample.

[PROOF.md](PROOF.md) gives the analytic reduction, strictness, an exact
refinement retaining angular defect and modulus variance, and a necessary
variance condition for possible failures approaching the boundary. It also
classifies first-power boundary equality in degrees at least four into two
families, `C(z^n-a^n)` and `C(z-a)(z+a)^(n-1)`, and proves that every possible
degree-nine first-power failure approaching the boundary must converge,
after normalization, to `z^9-1`. The other equality family is excluded by
the variance budget. This leaves the binomial perturbation problem open.
[STATUS.md](STATUS.md) explains why the assigned degree-nine Sendov target is
already covered by current primary literature and identifies the still
conjectural first-power endpoint.

## Reproduce

Python 3.11 or later; standard library only. Tested with Python 3.11.2.

```bash
python3 sendov_degree9_first_power_polar/verify.py
python3 sendov_degree9_first_power_polar/verify_interpolation.py
python3 sendov_degree9_first_power_polar/verify_boundary.py
```

Expected output: [EXPECTED.txt](EXPECTED.txt). The checker uses arbitrary
precision integers and `fractions.Fraction`; no floating point, solver,
enumeration, or external input enters its decision. It independently compares
the integrated binomial formula with the endpoint antiderivative identity,
checks a six-interval Bernstein positivity cover, and checks the rational
central-radius bracket and the obstruction witness. The analytic reasoning
in `PROOF.md` is a written proof, not a proof-assistant formalization.

The second checker computes the same Bernstein coefficients from exact
point evaluations of the endpoint antiderivative formula and solves the
Bernstein interpolation system by rational Gaussian elimination. It checks
positivity independently, then compares every coefficient with the first
algorithm. This checks the finite arithmetic certificate; it is not an
independent specialist review of the written analytic argument.

The third script checks the exact coefficient mechanism on the two equality
families in degrees 4--15, checks their variances, and verifies the degree-three
exception. These are exact controls for the hand proof, not an enumeration
of all polynomials.

The certificate is [certificate.json](certificate.json). It contains only
small rational parameters and interval endpoints. The numerical constants
and exact variance refinement are new to the primary sources searched in
`STATUS.md`; no priority or independent-review claim is made. The polar and
boundary identities themselves are prior work.
