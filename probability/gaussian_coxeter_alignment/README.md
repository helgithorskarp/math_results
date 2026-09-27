# Gaussian signs from alternating reflection-group orbits

The [author proof](PROOF.md) establishes full Gaussian majorisation,
at every variance and every threshold, when arbitrary bounded mixtures
of the two oriented halves of finite reflection-group orbits are aligned
to a common half. This includes nonabelian tetrahedral, octahedral and
icosahedral rotation orbits. Orbit masses and representatives may vary
arbitrarily, including diffuse mixtures. Uniformity within each rotation
orbit is required.

The same argument compares both unions and intersections of balls with
arbitrary radii constant within each orbit. An explicit family of actual
contractions has exactly two endpoint configurations in its full labelled
three-dimensional distance interval. It includes 48-site octahedral and
120-site icosahedral examples and an infinite dihedral-product family.
The proof signs all two-orbit priors and two independent ball radii for
these maps. It does not exclude alternative matchings or all R5 motions.

The algebraic sign uses a classical alternating chamber heat kernel and
extends the accepted [coordinate-parity theorem](../gaussian_parity_alignment/README.md).
Independent review is pending. The unrestricted R3 problem remains open.
See [SOURCES.md](SOURCES.md) for dependencies and novelty limits, and
[HANDOFF.md](HANDOFF.md) for the usable result.

From this directory, CPython 3.11 or later, standard library only:

```sh
python3 -B verify.py --check
python3 -B -O verify.py --check
sha256sum -c SHA256SUMS
```

Expected marker: `COXETER_ALIGNMENT_EXACT_CONTROLS_PASS`.
[EXPECTED.json](EXPECTED.json) is the deterministic exact record.
The checker verifies the complete 48-site contraction and structural
certificate in Q(sqrt(2)), finite Gaussian character identities, and
an expanding corrupted target. The analytic sign and uniform family theorem
are in the written proof; no numerical Gaussian integration is claimed.
