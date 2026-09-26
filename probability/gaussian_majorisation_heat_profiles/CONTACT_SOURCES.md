# Dependencies of the first-contact reduction

The named source remains Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2).
The paper was refreshed live on 26 September 2026. We do not claim a
resolution, an additional positive geometric class, or historical priority
for rearrangement, the heat equation, or a general first-contact argument.

The proposed contribution is the complete normalization of any bounded
failure into an ordered, transverse positive-time contact: a Gaussian
component in the input provides uniform volume-end control; the bulk
flux works through critical levels; and a Lipschitz scalar envelope allows
a generic target dilation to avoid a flat first crossing. The unresolved
contact sign is stated as an explicit equivalent condition, not assumed.

## Mathematical dependencies

- The [earlier heat-profile proof](PROOF.md), published at
  `007ec4fddd5566a57106a7b0464b34fa8d7ad8f2`, derives the regular-level
  equation and an exact coefficient obstruction. The new proof obtains
  its first-derivative identities directly by an envelope argument and
  does not extend its stopped diffusion representation through critical
  levels. No new coefficient-ordering claim is made.
- The [existing Gaussian rigidity proof](../gaussian_contraction_rigidity/PROOF.md),
  Theorem C and Section 5, contains the **same sharp posterior peak bound**
  used here, including arbitrary unbounded laws. This bound was rederived
  during exploration and then recognized as prior source; it is not a new
  result of this pass. Graph source:
  `bafkreiheirbfdiqq4igulat36rylgtda5zd2jc2ksdrif3qildy7ulnvy4`.
  Its independent acceptance is recorded at
  `bafkreibmhq6cg4rwvr2g5dbegsx47pglj4njuv6gjv3rp6tekly2lxe6ru` (5633);
  that acceptance does not review the new contact reduction.
- The [stability proof](../gaussian_majorisation_open_stability/PROOF.md),
  Section 4, gives strict target-homothety monotonicity and its posterior
  covariance integral. Graph source:
  `bafkreiaudc3oja6vhz7so5q5nc5ieqd7xcqvuxmnfa5jlu7dnnbpttgwhu` (6094).
  The present proof uses that strictness to perturb contacts; it does not
  reproduce the finite-certificate or stability theorem. The existing
  [bounded-law handoff](../gaussian_majorisation_open_stability/HANDOFF.md)
  correctly cautions that interior stability alone is not continuation
  through an unknown boundary.
- The [strict finite-witness reduction](../gaussian_majorisation_rank_abel/PROOF.md),
  Section 4, already gives finite strictly contracting witnesses if the
  full question fails. Graph source:
  `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu` (5964).
  We use this continuity step and state the additional Gaussian input
  regularization with an explicit error bound. Kirszbraun extension is
  classical, not a new assertion about extension maps.
- Leon Simon, [Introduction to Geometric Measure Theory](https://web.stanford.edu/class/math285/ts-gmt.pdf),
  Chapter 2, Theorem 1.4 and the area formula 3.4, supply Rademacher's
  theorem and the one-dimensional critical-image argument used for the
  scalar envelope. The same classical measure theory supplies volume
  decrease under a Lipschitz map. These pages were inspected directly.

## Team refresh and separation

Latest completed reports from lanes 2--8 and new public source were
inspected at the pass start and refreshed before publication. The fixed-atom
reduction (6112), axial robustness (6104), transverse matrix paths (6118),
ordered weights (6114), paired-layer result (6100), and failed counterexample
searches remain at their stated scopes. They do not supply the contact sign.

The new [rigid-mesh reduction](../gaussian_majorisation_extremal_maps/PROOF.md)
changes finite support to expose extreme map geometry. Our reduction
instead changes the input law to make the heat evolution begin with strict
order and controlled Gaussian tails. It neither analyzes meshes nor asserts
an extremal map minimizes a hinge on a fixed support.

The [all-prior set-transfer reduction](../gaussian_prior_localization/PROOF.md)
and [global endpoint criterion](../gaussian_majorisation_global_criterion/PROOF.md)
are complementary. This result concerns a first contact along actual heat
evolution, not a new endpoint transport criterion or finite prior optimizer.
The [finite orthogonal averaging obstruction](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md)
does not address this evolution. The
[relative-deficit obstruction](../gaussian_tail_deficit_obstruction/PROOF.md)
is not contradicted by the tail estimate: the latter uses a fixed positive
Gaussian input component and a globally strict Lipschitz constant, and its
cutoff deteriorates when either margin disappears.

The final refresh also read the new
[uniform defect localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md)
and [eight-lane interface](../gaussian_majorisation_global_criterion/INTERFACES.md).
The former bounds the size of an approximating finite witness by its
defect; no such quantitative size bound is needed or claimed for our
contact. The latter identified critical levels, volume boundaries, and
atomic initial time as obligations for this lane. The contact reduction
addresses those obligations by changing the starting law, without claiming
a global extension of the old stopped-diffusion formula. Researcher 7's
pass-10 searches yielded no certified negative hinge and are not a premise.
The refreshed graph had indexed through 6137: the earlier heat-profile
contribution was committed at 6130 with its body and all ten relations
verified. The mesh and localization contributions appeared at 6132 and
6134, respectively; the finite-certificate interface appeared at 6136.

## Validation and trust boundary

`contact_audit.py --check CONTACT_EXPECTED.json` is an exact finite audit
with Python integers and fractions. A degree-bounded tensor grid certifies
the cleared coefficient identity; the two other controls check constants
and the need for transverse crossing. No numerical integration or search
is evidence for the theorem, and no Gaussian contact was generated.

The universal proof uses Gaussian differentiation, the elementary envelope
argument, null analytic level sets, Gaussian tail bounds, compactness,
Kirszbraun extension, Rademacher's theorem and the one-dimensional area
formula. It is an ordinary mathematical proof, not proof-assistant output
or independent peer acceptance. The coefficient and scalar audits do not
verify those analytic bridges. The next substantive task is the flux sign
in Contact condition C; adding more test fixtures would not close it.
