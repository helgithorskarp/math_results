# First-hit witness events also occur at Gaussian equality contacts

The [author proof](PROOF.md) gives four affinely independent input sites,
Gaussian input smoothing, an actual isometry, and the actual top sets. The
flux is zero but all the previously specified **event** bounds hold. For every
`0<kappa<=1/256`, at `s=1-kappa^2/48` the Brownian witness has

```
Pr{tau_(kappa/16)<=s} >= kappa^2/96,
Pr{N_s M_s<=-kappa/4, |(Z_s,W_s)|<2} >= kappa^2/96.
```

The equality contact is ordered for every prior on the four components;
component balance and the joint prior/threshold conditions hold exactly.
The signed expectation is nevertheless zero. An orthogonal change in the
target noise coupling makes the witness identically zero without changing
the densities or flux.

This blocks the proposed use of first-hit occurrence, negative state
geometry and the stated probability bounds alone to detect an adverse
contact. It is a boundary example with Lipschitz constant one, **not** the
strict, transversely crossing contact forced by a hypothetical violation.
It does not refute the necessary-witness theorem, preclude every stochastic
proof, or settle unrestricted dimension-three Gaussian majorisation.
No new sufficient inequality or Kneser--Poulsen class is asserted.

With Python 3.10 or later (tested with CPython3.11.2), standard library only:

```sh
python3 probability/gaussian_first_hit_geometry/check.py
python3 -O probability/gaussian_first_hit_geometry/check.py
```

Both reproduce [EXPECTED.json](EXPECTED.json), status
`EXACT_FIRST_HIT_GEOMETRY_CONTROLS_PASS`. The checker validates the rational
box estimates, probability budget and a positive-series exponential bound.
The Gaussian and martingale arguments remain written mathematics, not
computer verification or independent review. [Sources and scope](SOURCES.md).
