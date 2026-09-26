# Full Gaussian majorisation from three common-target components

This proves **every Gaussian variance and every density threshold** for
uniform tetrahedral flaps with an arbitrary fixed tetrahedral background,
arbitrary core mass, and arbitrary bounded radial law. It also proves a
full-dimensional neighborhood of unequal ray weights, which may vary
measurably with radius. The general dimension-three conjecture remains open.

For the twelve directions `v = +/-e_i +/-e_j`, the original contraction
sends `r v` to `r v_i v_j e_k`, with `k` the missing coordinate, and fixes
the solid tetrahedron `P_h` defined in [PROOF.md](PROOF.md). Radii satisfy
`2h <= r <= L < infinity`. If the conditional ray weights obey

```text
sum_v |p_v(r) - 1/12| <= 1/72
```

almost everywhere in the radial law, every hinge of the smoothed source
is at most the corresponding hinge of its smoothed image. No lower bound
on the Gaussian variance or smallness of the ray mass is imposed.

The main mechanism is short. For each coordinate `i`, reweight the four
rays perpendicular to it by `1/6` each, and the other eight by `1/24` each.
Researcher 6's coordinate-preserving maps send all three reweighted laws
to the same uniform law on six axis points. Their average is the original
uniform ray law. Add the same arbitrary core law to all components, apply
the planar theorem to each, and use convexity on the source density.
A nonnegative-flow perturbation proves the neighborhood of unequal weights.

This removes the variance restriction from the uniform-background family
in the team's [eventual endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md).
It builds on the [fixed-core map](../gaussian_majorisation_fixed_core/PROOF.md).
The latter already proves the corresponding support-level ball-volume
case; this packet does not claim a new Kneser--Poulsen inequality.
Its obstruction to a single core-fixing rank-five realization remains
valid and is made quantitative throughout the new neighborhood.

There is also a sharp boundary to this bridge. For a finite contraction
with distinct image sites, every deterministic common-target source
decomposition is trivial: all component source laws equal the original
law. Applied to researcher 7's nine-point example with distinct weights,
this rules out every finite mixture of five-dimensionally liftable
deterministic contractions. It does not refute Gaussian majorisation.

- [Proof and exact assumptions](PROOF.md)
- [Sources, dependency commits, and novelty boundary](SOURCES.md)
- [Exact supplementary checker](verify.py)
- [Expected audit record](EXPECTED.json)

From the repository root, with CPython 3.11 or later and no packages:

```sh
python3 probability/gaussian_majorisation_common_target/verify.py --check
python3 -O probability/gaussian_majorisation_common_target/verify.py --check
cd probability/gaussian_majorisation_common_target
sha256sum -c SHA256SUMS
```

Expected checker output:

```text
PASS 9bc0a746e865b4eae14451d44ce7f5c49f7dab3994de402186f7f888728c3268
```

Validation used CPython 3.11.2 and 3.12.14. The checker derives 576 exact ray-pair
polynomial deficits, checks 192 core inequalities, verifies the common
target and the connected 30-vertex incidence graph, audits the tree
correction on a basis, and verifies all 132 vertices of the zero-sum
L1 ball. It also checks varying weights on two radial shells with an
asymmetric core and rejects an incorrect common-target certificate.
It checks the nine-point labels, distinct weights, and the strict convexity
identity behind the injective-target obstruction. All arithmetic is integer
or `Fraction`; checks remain active under `-O`.
Runtime is under one second on the publication machine.

The universal theorem is an analytic author proof, conditional on the
cited planar theorem and standard Kirszbraun extension. These finite
checks supplement that proof; they are not independent mathematical
review or proof-assistant formalization. No Gaussian quadrature, solver,
large generated certificate, or external checker dependency is required.
