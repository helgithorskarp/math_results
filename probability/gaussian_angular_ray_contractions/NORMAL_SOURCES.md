# Convex normal-bundle sources and evidence

The extension is a complete author proof, 27 September 2026, pending
independent review. The original angular theorem has independent correctness
acceptance6410, recorded in [ACCEPTANCE.md](ACCEPTANCE.md). That acceptance
does not review this extension. Historical priority remains unresolved.

The primary problem and transfer inputs, inspected again for this extension,
are G. Aishwarya and D. Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), and K. Bezdek and
R. Connelly, [Pushing disks apart--the Kneser--Poulsen conjecture in the
plane, Theorem1](https://arxiv.org/pdf/math/0108098). The respective sampled
density and arbitrary-radius volume transfers are established inputs.
The common problem remains the full bounded-law R3 majorisation question.


[NORMAL_BUNDLES.md](NORMAL_BUNDLES.md) extends the angular motion over any
closed convex core, on any selected Borel family of complete outward normal
rays. It characterizes every nonnegative map affine on those rays and fixing
the core: the same angular inequality is necessary and sufficient, and
parallel rays have the same factor. The necessity follows by scaling away
the projection offsets. For sufficiency the projection offsets contribute
two nonnegative terms whose scalar coefficients decrease during the lift.

The load-bearing team inputs are the homogeneous angular result, graph6402
`bafkreidy6wjmsnzoenmqqwo4kos36fwuvpj65gq5iioqownidek64axyaa`, and the
normal-bundle decomposition in the
[accepted convex-core result6331](../gaussian_radial_contractions/CONVEX_CORES.md),
`bafkreifktf3exjltqmj5gnt5wvhpqe2za3cbb7rkdnlt3ha774is52k2j4`, accepted by
[review6343](../gaussian_convex_core_review_frontier/REVIEW.md),
`bafkreieromtio62dcbcedmw5rl63emek3xwi4oca32hyzjvowdmq7ubasy`.
All seven original angular files are frozen with their exact hashes in
NORMAL_INPUTS.json; their original pending-review text is historical.
Both primary transfers remain
Aishwarya--Li Theorem1.4(i)(a) and Bezdek--Connelly Theorem1; they are not
new consequences proved from scratch here.

This changes the geometric class, rather than refining a numerical constant
or adding another finite witness. A ball core gives genuine joint dependence
on the original radius and direction. A cube has different projection base
points and gives a global nonexpansive map that no homogeneous ray formula
or common normal-profile formula over any convex core represents, in the
scopes explicitly proved. No all-composition or all-method separation is
asserted. The radial profile freedom in6331 and angular factor freedom here
are distinct; the unrestricted nonseparable radial problem is not solved.

The literature comparison concerns the displayed geometric class and the
same primary transfer sources above. Metric projection facts, the earlier
normal-distance decomposition, and the earlier angular lift are credited.
Historical novelty of the full combined class remains unresolved.

Reproduce with `python3 check_normal_bundles.py --check` and
`python3 -O check_normal_bundles.py --check` from this directory. Both print
`NORMAL_BUNDLE_AUTHOR_CHECKS_PASS`. The checker uses exact Fractions and
comparisons of quadratic surds by rational squaring. It checks366 pair
motions over cube, ball, halfspace, line, segment, point and whole-space
cores, using the angular factor and the zero/unit boundary factors.
Projection membership and normal incidence are checked for every fixture.
The controls include generic polynomial expansion, reversed-sign rejection,
false normals, unequal factors on parallel rays, and finite-sample offsets
that mask a forbidden full-ray factor pair. A corrupted expected-output file
is rejected as well. These are author checks, not independent review or a
proof by finite sampling; all universal quantifiers and transfers remain
explicit in NORMAL_BUNDLES.md.

The original SHA256SUMS is also frozen. NORMAL_SHA256SUMS records only the
new extension and acceptance-notice files. Use `sha256sum -c` on each
manifest from this directory. The normal checker does not import any code
from the angular checker. Its quadratic-surd comparisons are exact algebra,
not floating-point approximations or interval sampling.

The final team refresh incorporated the accepted angular and parity
theorems, the second prior-cell acceptance, R3's quartic loss-moment middle
guard, the logarithmic-noise polynomial theorem, and the mean-loss compactness
margin. None supplies a hidden sign premise here. In particular a moment
cone or a bounded threshold window does not imply our all-variance,
all-threshold conclusion. R4 retains extremal-map/deformation classification
and R7 retains adversarial searching. No new internal audit or finite-cell
certificate is claimed by this extension.
