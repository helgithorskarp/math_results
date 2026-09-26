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

The [reference-test boundary](REFERENCE_MIXTURE_BOUNDARY.md) checks a
possible route to that missing sign. In an explicit two-cube example,
all isometric-reference source tests are convex, but every same-volume
probabilistic average of them stays at L1 distance at least 1/12 from a
mixed-law maximizing source test, with a positive source-integral deficit.
The example satisfies the known Gaussian comparison. The result rules
out this source-coverage step, including approximation by such averages;
it does not rule out reference slack or joint target-set arguments.

**Status:** the original reduction and interaction identity are accepted
by a [separate analytic review](../gaussian_uniform_set_review/REVIEW.md).
The reviewer authored the isometric-reference theorem and explicitly
excludes the optional corollary using it from independent acceptance.
The new reference-test boundary remains an author proof awaiting review.
These results do not establish the missing Gaussian sign. The full
question remains open. The class has unbounded component count and extent;
finite testing does not settle it. The reduction changes the map and law
and does not make a fixed-map optimizer uniform.

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
scope of the measure-preserving assertion. The reference-test boundary
is a written analytic proof and adds no computational premise to the
existing exact geometry audit.
