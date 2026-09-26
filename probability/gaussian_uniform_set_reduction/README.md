# Uniform lattice sets suffice for the full Gaussian question

The [author proof](PROOF.md) reduces the unrestricted three-dimensional
Gaussian-majorisation question to uniform measures on finite unions of
disjoint unit lattice cubes. Each cube is sent by an integer translation
to its labelled target cube. The map preserves volume on its support, and
the two initial densities are equimeasurable.

For source and target center differences u and v, contraction of the
**whole cubes** is exactly

    |u|^2-|v|^2 >= 2 ||u-v||_1.

It suffices to test strictly positive slack, integer-square Gaussian
variances and positive rational hinge thresholds. Any hypothetical strict
violation in the original problem survives in this class, with arbitrarily
small loss. The supremal positive defect is unchanged.

All conditional component gaps are zero by translation invariance. The
remaining full-question obligation is therefore exactly interaction
monotonicity for these identical rigid packets. This does not restore the
false ordering for arbitrary packets under random grid shifts.

**Status:** complete author proof, independent review pending. This is an
exact reduction, not a positive comparison theorem or a counterexample.
The full question remains open. The class has unbounded component count
and extent; finite testing does not settle it. The reduction changes the
map and law and does not make a fixed-map optimizer uniform.

Run with standard-library Python 3.11+ from this directory:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

[EXPECTED.json](EXPECTED.json) records exact whole-cube and corner checks
for an eight-cube example with paired affine rank six and a three-label
weight-splitting example. The controls distinguish a false center-only
criterion, its nonstrict boundary, and a successful dilation. They do not
compute Gaussian hinge signs. The approximation and equivalence depend on
the written proof, not on those finite controls.

See [SOURCES.md](SOURCES.md) for attribution, team interfaces and the
scope of the measure-preserving assertion.
