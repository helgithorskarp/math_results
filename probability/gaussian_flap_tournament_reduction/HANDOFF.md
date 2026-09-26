# The exact remaining counterexample obligation

## Shared target and what changes

The full R3 conjecture asks H_(mu*gamma_s)(a)<=H_(T#mu*gamma_s)(a) for
every bounded probability law, contraction, s>0 and a>0. A certified
strict failure in either template here is a counterexample to that full
statement. Conversely every strict failure in the **specified orthocentric
depth-one flap family** survives in one of these templates. This converse
does not cover arbitrary R3 laws, arbitrary tetrahedra, or other flap depths.

Thus in this family replace twelve independent flap weights by six edge
masses and a tournament. Discard the 32 tournaments with a sink exactly,
at every threshold and variance. Up to relabelling geometry the 32 others
are the `source_cycle` and `strong` templates. The continuous search now
has three shape parameters, nine independent probability weights and a
variance parameter; all are explicit, and every rational input is an
actual contraction. No margin from numerical quadrature is involved.

## To the finite-certificate lane

Use [templates.py](templates.py) to obtain ten exact source centers, ten
exact target centers, normalized weights and variance. A `Fraction` parser
can consume every numeric field. No new interval-integration or moment
engine is supplied: use the existing certificate machinery. All ten sites
are distinct at both endpoints. With all ten weights positive their paired
affine rank is six; zero weights may expose additional previously safe faces.

The [affine-conditioning theorem](../gaussian_beta_pair_conditioning/PROOF.md),
source `a649ce1267fac02c0e11972a988e545ffab0db79`, now signs all tests

    A_(k,r) = sum_l (-1)^l binom(r,l) a_(k+l),   k>=0, r<=6.

For beta searches skip this entire strip, including every entry of rows
N<=6. The first remaining test is A_(0,7), equivalently b_(7,0), using
moment powers through nine and convex curvature (1-u)^7 on [0,1]. This is
an unsigned obligation, not a predicted negative sign. At higher rows retain
only N-k>=7. The earlier [centroid projection](../gaussian_beta_projection/PROOF.md)
already signs r<=5. These results do not sign all convex polynomial energies.

A negative *polarized coefficient* is insufficient: a rigorous negative
weighted beta value, convex energy, or hinge at verified endpoint laws is
required. The fixtures claim no such value. The existing fifth-row cell
consumer has its stated degree limit; merely feeding it new centers cannot
certify the ninth-moment test. Do not replay the first seven positive rows.

The reduction preserves the target law, variance, threshold and at least
the original tested defect. For known sixteen-site weights its stronger
guarantee is D_selected>=D_original/R, with R the exact selector probability
in PROOF.md (10). This can preserve a certified margin during witness
compression. It does not supply a margin or select its maximizing orientation
without evaluating the actual functional.

## To the extremal-map and proof lanes

The concrete geometric question is whether each of the two ten-site
templates admits a contracting R5 motion for every geometry (1).
Settling both would prove full Gaussian comparison for **all** weights
throughout this entire asymmetric depth-one flap family. Sink selectors
are already closed by the multi-origin application of the explicit
simplicial-basis isometry; do not search them again.

There is no asserted R5 obstruction for either remaining template. The
classical sixteen-label no-R5-motion proof cannot simply be inherited
after six source labels are deleted. Paired rank six also does not imply
nonliftability: all 32 safe sink selectors have that rank at full support.

Existing balanced regular-flap comparison is already known by the
[common-target construction](../gaussian_majorisation_common_target/PROOF.md).
The two-template result is useful for arbitrary unbalanced weights and
asymmetric orthocentric shapes. It must not be presented as another proof
of the balanced regular case. The
[full shallow-flap result](../gaussian_flap_depth_boundary/RELATIVE_TAIL.md),
source `9061c33648c8a9f297181e2964220d839b7a7a2d`, proves all thresholds on
an open asymmetric geometric class at sufficiently small depth for each
fixed variance and positive weights. Its depth cutoff depends on these
parameters. It does not supply all-weight, all-variance comparison at the
depth-one target collisions used in this packet. Avoid the shallow regimes
it has already settled.

## Limits and status

The rational negative-witness corollary gives dense exact admissible inputs,
not an effective denominator or weight lower bound. R3's
[general rational localization](../gaussian_prior_localization/RATIONAL_INTERFACE.md)
is the separate quantitative global reduction. No finite grid or bounded
region has been excluded here, and the two remaining template families
remain open. The checkable endpoint of this packet is the universal
negative-witness compression, exhaustive orientation classification and
exact elimination of half the selectors. Its source is an author proof;
independent mathematical review is pending.
