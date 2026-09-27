# Sources, dependencies, and claim boundary

Sources inspected 27 September 2026. The only problem source is
Aishwarya--Li, arXiv:2609.07041v2, as named by the human research contract.

## Primary literature

- G. Aishwarya and D. Li, *Gaussian Convolution, Internal Energies, and the
  Kneser--Poulsen Conjecture*, [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
  Theorem 1.4(i)(a) supplies sampled-density stochastic order for continuous
  contractions. The elementary two-dimensional Gaussian cancellation in
  PROOF.md converts this into the requested hinge order after the lift.
  Theorem 1.3 alone is not used to assert full dimension-three majorisation.
- K. Bezdek and R. Connelly, *Pushing disks apart--the Kneser--Poulsen
  conjecture in the plane*, J. reine angew. Math. 553 (2002), 221--236,
  [author PDF](https://pi.math.cornell.edu/~connelly/pdf/10.1515_crll.2002.101.pdf),
  [arXiv:math/0108098](https://arxiv.org/pdf/math/0108098).
  Theorem 1 supplies the arbitrary-radius volume transfer from dimension n+2.
  **Corollary 5 already contains our interpolation formula**, applied there
  to a partial common positive dilation. Corollaries 3--4 cover displacement
  rank two and at most n+3 sites. The present work claims none of these
  constructions or transfer results as new.
- K. Bezdek and M. Naszodi, *The Kneser--Poulsen conjecture for special
  contractions*, [arXiv:1701.05074](https://arxiv.org/pdf/1701.05074).
  The coordinatewise strong-contraction definition and Theorem 1.3 are the
  prior class used in the comparison. The separate uniform-contraction
  hypothesis is also checked on our example.
- K. Bezdek, *From the Kneser--Poulsen conjecture to ball-polyhedra*,
  [arXiv:0903.4846](https://arxiv.org/pdf/0903.4846), was consulted for the
  existing volume-transfer and contraction-class context.

The searched primary sources did not explicitly state the entire class of
nonnegative scalar 1-Lipschitz radius profiles, including order-reversing
profiles, with both conclusions of PROOF.md. This is a provisional priority
assessment, not an exhaustive literature theorem. The contribution is a broad
application of an old lift, with an exact radial sign decomposition. A prior
proof of this same full class would change its novelty status, not the proof.

## Durable team inputs

### Convex-core extension

[CONVEX_CORES.md](CONVEX_CORES.md) extends the whole radial profile result
from C={c} to every nonempty closed convex C. The new geometric input is
that two projection-normal terms in the distance identity have nonnegative
coefficients. Metric-projection facts are standard and proved explicitly;
no new projection theorem or general lift is claimed. The consequence for
reflecting a full parallel-body collar uses the exact hypotheses
K=C+aB and source points in C+2aB. It is not a claim about arbitrary reflected
projections without that restriction.

The predecessor is the original point-core contribution 6317,
`bafkreiequbwj2ms2eev5sydi5exukocl3ycgaryq5bcywqxypf367hgoui`,
source 78c08178239c5dabd91e4c46cfddd7ffb2e440f9. Its PROOF.md, check.py and
expected.json are preserved byte-for-byte. The new proof writes the full
normal-bundle identity and transfer argument, so it does not import an
unverified numerical sign from that predecessor.

The primary-source comparison above was refreshed for metric projections,
normal bundles, retractions and parallel bodies. It did not locate the
complete nonmonotone normal-profile theorem or its whole-collar consequence
in the compared texts. Historical priority remains provisional. Merely
proving a contraction is not claimed as a new KP transfer theorem.

The new checker is independent of check.py as code: it expands the full
nine-variable identity and compares actual four-dimensional lifted
coordinates for rational cube, segment, singleton, halfspace and whole-space
fixtures. Normal directions at faces, edges and corners, and degenerate core
cases, are included. It verifies finite examples and algebra, not the
quantifier over every convex set. Both normal and optimized Python agree.

### Earlier radial comparisons

The transfer identities are included in full in PROOF.md, so the new radial
sign does not assume any unproved team sign conjecture. The following sources
provide scope comparisons and the earlier use of Gaussian cancellation.

| Source | Role here |
|---|---|
| [Paired rank and Abel gap](../gaussian_majorisation_rank_abel/PROOF.md) | Rank-five sufficient class; our rational benchmark has paired rank six. |
| [Scalar transport-defect criterion](../gaussian_majorisation_scalar_defect/PROOF.md) | Earlier cancellation and a distinct one-scalar certificate, explicitly excluded for the benchmark. |
| [Axial cone rotations](../gaussian_axial_cone_rotations/PROOF.md) and [matrix paths](../gaussian_axial_cone_rotations/MATRIX_PATHS.md) | Preserved geometric flagships; the radial motion is a different global profile class. No audit or modification is made here. |
| [Disjoint cap reflections](../gaussian_disjoint_cap_reflections/PROOF.md) and [auxiliary cap certificates](../gaussian_cap_auxiliary_certificates/PROOF.md) | Accepted cap family, including arbitrary hemispherical cap counts and every four-cap instance. The radial map is not one of those displayed piecewise reflection maps. |
| [Orthocentric flap selectors](../gaussian_flap_selector_motion/PROOF.md) | Closed depth-one family, cited for the ownership boundary, not reopened. |
| [Finite-interval strong-chain closure](../gaussian_indecomposable_contractions/STRONG_CLOSURE.md) | Researcher 4's new approximation obstruction has its own finite-interval hypothesis. We make no corresponding strong-chain closure claim for the radial benchmark. |

The radial class supplies all variances, all bounded laws, and arbitrary
individual ball radii. It therefore enlarges the collection of explicit
positive geometric benchmarks. It does not assert strict containment of the
cap/flap/axial classes, or separation from every composition, limiting
procedure, nonlinear robustness theorem, or measure rematching.

Researcher 4 retains general extremal-map/deformation classification and
researcher 7 retains adversarial construction. This contribution concerns
the universal normal-bundle distance decomposition and its internal-energy and
ball-volume consequences. Neither the accepted R4 pair-action obstruction
nor R8's positive-error small-radius bound is used as a global sign input.

## Reproduction and trust

`check.py` uses only Python arbitrary-precision integers and Fraction.
The generic distance and derivative identities are checked by exact sparse
polynomial expansion in six independent variables. The finite tests cover
five profiles, zero radii, unchanged radii, collapsed targets, multiple folds,
and reversed radial order. Deliberately false hypotheses and one changed
polynomial are rejected. Normal and optimized Python have identical output.

These are author algebra checks. Analytic quantification over all profiles,
Gaussian measures and ball radii rests on PROOF.md and its explicitly cited
external theorems. No formalization or independent mathematical acceptance is
claimed. All substantive source and compact expected output are included.
