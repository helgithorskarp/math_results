# How the normal, meridian, and screw classes fit together

This is a mathematical consolidation of the existing positive geometric
portfolio for the dimension-three Gaussian-majorisation question. It proves
precise relations between the classes, records their different domain
requirements, and separates reviewed correctness from historical priority.
It adds no twist schedule and claims no new Kneser--Poulsen headline.

[CLASSIFICATION.md](CLASSIFICATION.md) establishes four useful facts:

1. On the same complete normal rays over the same convex core, the common-profile
   and directional-affine representations intersect exactly in a single constant
   normal factor. Alternating their accepted constructions already gives many
   profiles depending jointly on distance and direction.
2. A rotation-invariant convex normal contraction is a meridian contraction.
   The converse has an exact formulation when the fixed-point set is precisely
   the stated core; that qualification cannot be dropped.
3. On a full disk cylinder, the rotation-equivariant part of the affine-slice
   class is exactly complex scalar multiplication on each slice. Its intersection
   with azimuth-preserving meridian maps has real nonnegative scalar factors.
   The local contraction condition includes variable modulus, phase, and axial
   folding, with a separate statement at unit modulus.
4. Full-ray, full-orbit, full-prism, and rigid-region extension hypotheses are
   different. Finite endpoint tests and failure of one displayed representation
   do not settle membership in another class or its composition closure.

The geometric conclusions remain those of the cited source theorems: every
Gaussian variance and threshold for every bounded input law on the domain,
and both ball-volume comparisons for arbitrary individual radii. The input
law need not share the map's rotational symmetry.

The comparison arguments here are written author deductions, not an independent
review of the underlying theorems. Common and directional normal, meridian,
twisted-meridian, and affine-slice sources have independent correctness acceptance.
At the recorded graph snapshot, the positive rigid screw and cylindrical
sources remain author proofs. Historical priority remains unresolved throughout
this comparison; the unrestricted R3 problem remains open.

[SOURCES.json](SOURCES.json) pins the source files, graph references, independent
reviews, and observed Git commits. No older theorem packet is modified.

Reproduce the consolidation by checking the four proofs in CLASSIFICATION.md
against those source hypotheses. From the repository root, the following
optional integrity command checks this packet's three substantive files:

```bash
cd probability/gaussian_geometric_portfolio
sha256sum -c SHA256SUMS
```

Expected: `README.md: OK`, `CLASSIFICATION.md: OK`, `SOURCES.json: OK`.
There is no computational theorem, solver, external dataset, generated search
output, or omitted certificate. Hashes verify bytes, not the mathematics.
