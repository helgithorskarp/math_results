# A spherical tail test for Gaussian majorisation

For bounded laws nu and omega in R^3, define

```
S_nu(lambda) = average over theta in S^2 of log E exp(lambda theta.X).
```

The [proof](PROOF.md) gives an explicit error bound connecting
`S_nu(lambda)-S_omega(lambda)` to the Gaussian hinge gap at variance `s`
and threshold

```
a_s = (2 pi s)^(-3/2) exp(-lambda^2 s/2).
```

For support radius `L`, put `A=lambda L` and `K(A)=4 A^2+3 A+3`.
When `lambda^2 s >= max(1,4A)`, the normalized hinge gap differs from
the spherical gap by at most `2 K(A)/(lambda^2 s)`. A strictly negative
spherical gap for a contraction would therefore give a counterexample
at **every sufficiently large variance**, with explicit thresholds.

For any fixed finite pair of configurations, comparing these spherical
functionals for every atom weight and every lambda is equivalent to
comparing the mean widths of convex hulls of the corresponding balls
for **every radius vector**. The equivalence uses the Gumbel maximum
identity and the zero-temperature limit of the logarithmic sum.

These are author proofs awaiting independent review. They provide a
necessary test and a conditional counterexample conversion. **No negative
spherical gap, full dimension-three theorem, or new Kneser--Poulsen case
is claimed.** The classical equal-radius mean-width theorem does not
establish the arbitrary-radius comparison required here.

Reproduce the compact audit with CPython 3.11 or later, standard library only:

```sh
python3 audit.py --check
python3 -O audit.py --check
sha256sum -c SHA256SUMS
```

`audit.py` checks the scaling and sign against an independently integrated
two-point Gaussian mixture. Its numerical calculations are floating-point
formula checks, **not rigorous enclosures**. Exact rational checks audit
the constants in the proof and the variance condition. No numerical
output is used as a universal proof premise. `EXPECTED.json` records the
small deterministic audit; no large search output or external data is needed.

[SOURCES.md](SOURCES.md) records the source problem, prior geometric
context, and the team results that explain which bridges remain open.
