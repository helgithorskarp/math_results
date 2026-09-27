# Dependencies, overlap and trust

The sole problem source is Aishwarya--Li,
[arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), Conjecture 1.1
in dimension three, refreshed live for this pass. Full bounded-law Gaussian
majorisation remains open. No historical-priority claim is made for the
elementary convexity and perturbation inequalities used here.

## Analytic premises

R2's [dilated-martingale proof](../gaussian_dilated_martingale_certificate/PROOF.md),
original6464, and its
[independent acceptance6480](../gaussian_dilated_martingale_review/REVIEW.md)
supply the endpoint-coupling Jensen mechanism and the unperturbed cutoff.
Their finite affine-density witness is reused with attribution. The small
`TUBE_INPUT.json` fixture uses R2's eight-site reference from
[FAMILY_INPUT.json](../gaussian_dilated_martingale_certificate/FAMILY_INPUT.json);
its spatial and relative-prior budgets are new. This fixture is calibration,
not the claimed new class.

The [spherical-gap endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md),
original6032, with
[independent acceptance6048](../gaussian_majorisation_eventual_endpoint_review2/README.md),
is the analytic sign consumer. Its tail error is at most 44R^2/s on the
required parameter ray, and its high-noise window overlaps that tail.
We import the accepted conclusion, not replay or independently reaccept
the underlying Gaussian integrations. Its radius may be taken about any
source-ball center. Translation invariance and Kirszbraun justify the
unchanged reference-mean anchor after perturbation.

## Material overlap checked

R8's [bounded-law stability](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md),
original6102, already gives qualitative openness of strict bounded-law
comparisons under suitable endpoint controls. This note does not claim
openness itself as new. The extra content is one explicit, mass-free
spatial/prior budget obtained from a linear spherical reserve on the
ENTIRE unbounded parameter ray. It transfers a finite reference witness
to a whole contracting family and gives the exact variance cutoff.

R2's newer [uniform strong-map theorem](../gaussian_uniform_lipschitz_certificate/PROOF.md),
original6486, [accepted6490](../gaussian_uniform_lipschitz_review/REVIEW.md),
removes the coupling requirement for every map with Lipschitz constant
below 1/sqrt(27), at sufficiently large variance. Our perturbed maps can
have preserved pairs and thus Lipschitz constant one. Conversely, this
note does not claim that every pair admitted by that theorem has a useful
nearby martingale reference. The conditions are complementary.

R8's concurrent [small-target theorem](../gaussian_uniform_small_target/PROOF.md),
original6482, pending review at preparation, gives uniform all-threshold
majorisation at every fixed variance with a positive covariance floor
and a sufficiently small target. Our budget does not require that floor,
or its extremely small target radius. The exact control in PROOF.md
separates these displayed sufficient schedules at its stated variance;
it is already positive by a classical continuous contraction. No novel
geometric example is claimed. The continuous-contraction
comparison is given in Section 3 of the primary Aishwarya--Li manuscript
linked above.

The [same-pair cubature](../gaussian_prior_localization/CUBATURE_FRONTIER.md)
and [loss-preserving variant](../gaussian_prior_localization/LOSS_CUBATURE.md)
retain their accepted scope6212/6218 and6364/6380. They preserve selected
moments but do not supply the spatial cover needed to lift a newly found
reference certificate. The new finite-cover implication explicitly
requires that additional cover. The accepted uniform-middle and moving
small-loss results remain unchanged. In particular the
[old endpoint-join obstruction6478](../gaussian_endpoint_join_obstruction/PROOF.md)
is not bypassed within its tiny-loss regime; this proof uses a different
global spherical reserve at a different sufficient parameter domain.

At the final source refresh R1's [universal spherical sinc comparison](../gaussian_spherical_sinc_comparison/PROOF.md)
appeared at source `9c50ebb1b3543cd5c1886ba45f6f782ce2481853`.
Its author proof claims a universal spherical sign, eventual full
majorisation for every finite contraction, and a quantitative eventual
bound for every fixed Lipschitz constant below one. Independent review is
pending. The [handoff](HANDOFF.md) records the direct conditional consumer:
replace the coupling-derived e by 1-c for a strictly contracting reference.
This new source is context, not a premise of the proved martingale transfer
or of the exact finite certificates. In particular this note does not
claim that only strongly damped maps now have an eventual theorem.

## Reproducible boundary

`INPUTS.json` records exact dependency file commits, SHA256 values and
reader links. `verify.py` reads those historical bytes through `git show`,
so later changes to main do not silently change the audited premises.
The producer uses exact `fractions.Fraction` arithmetic. Its reference
coupling check needs O(n^2) rational operations and O(n) storage. The
supplied-record checker is deliberately separate from the producer and
uses ordered-pair identities and an explicit coupling matrix; its storage
is O(n^2). Bit cost depends on the input rationals.

The exact controls check coupling marginals and barycenters, scalar guards,
the zero-reserve boundary, translation/scaling, arbitrarily small positive
weights in a singular example, a nonmartingale contraction with a preserved
pair, and rejection of malformed inputs and records. They are author
checks, not independent peer review or a formal proof. The continuum
transport, convexity and endpoint arguments remain written mathematics.
The actual perturbed support contraction and any user-supplied cover are
explicit obligations; the producer cannot infer them from four radii or
from a cubature alone. No private input, floating-point sign, quadrature,
solver, large corpus or hidden certificate is needed for reproduction.
