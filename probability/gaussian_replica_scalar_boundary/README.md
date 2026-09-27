# A structural boundary for scalar replica certificates

The [author proof](PROOF.md) constructs, for **every finite K>=12**, a
continuous signed profile satisfying all of the following simultaneously:

- a positive common lift measure with the Gaussian square-root moment relation;
- decreasing, strictly log-convex replica values, hence **every** accepted
  retained-interaction inequality at every base and added-block size;
- strictly positive beta differences of all orders q<=K at every index;
- all smooth PC2 curvature tests and the absolute bound |H|<=7/50;
- exponential replica decay, a strict peak cutoff, the normalized replica
  cap (m-1)B_m<1, and the hinge derivative bound u|H'(u)|<1.

Nevertheless the profile has an explicit negative interval. Its normalized
beta averages are negative along an infinite sequence with both indices
growing. That sequence can lie inside **any prescribed wedge q<=c(j+2),
c>0**. A rational producer gives a specific, finite (usually enormous)
negative beta index using the analytic bounds; it does not sum that row.

This is a countermodel to an implication between **scalar constraints**.
No Gaussian input law or iid replica cloud realizing the model is supplied
or claimed. This is not a counterexample to majorisation or to any team theorem.
It does not rule out proving a single further fixed beta diagonal from the
current inequalities. It rules out obtaining a universal linear wedge from those
inequalities, even after adding any fixed finite number of signed diagonals.
Sublinear regions and peak-dependent apertures are not excluded.

The implication is a concrete boundary for the analytic lane: such a wedge
requires an additional averaged constraint or a realizability property of
actual replicas. No isolated row13 certificate, pointwise-kernel failure,
or new geometric sufficient class is claimed. The unrestricted Gaussian
question remains open; this complete author argument awaits independent review.

Reproduce with CPython3.11 or later, standard library only:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B verify.py --produce --order 12 --b 1/4
python3 -B verify.py --produce --order 12 --wedge 1/10
sha256sum -c SHA256SUMS
```

[EXPECTED.json](EXPECTED.json) records exact finite controls. The universal
parameter ranges, Laplace/Abel identity and beta probability bound are proved
in the manuscript, not inferred from numerical tests. The producer uses
rational Taylor bounds for its index; no enormous alternating sum, numerical
quadrature, optimization solver, external data or large certificate is needed.
Attribution and the distinction from earlier obstructions are in
[SOURCES.md](SOURCES.md).
