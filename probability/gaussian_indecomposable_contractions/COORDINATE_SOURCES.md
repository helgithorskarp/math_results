# Coordinate-bound sources and dependency boundaries

Primary sources checked on 27 September 2026:

- U. Brehm, *Extensions of distance reducing mappings to piecewise congruent
  mappings on Euclidean space*, Journal of Geometry 16 (1981), 187--193,
  [publisher record](https://link.springer.com/article/10.1007/BF01917587).
  The piecewise-isometric extension is classical. The current packet bounds
  rational heights within the already accepted team implementation of that
  construction; it does not claim to invent the extension algorithm.
- A. Petrunin and A. Yashinski, *Lectures on piecewise distance-preserving
  maps*, [arXiv:1405.6606](https://arxiv.org/html/1405.6606), Lecture 2 and
  final remarks. The exposition explains the repair and credits its
  extension to all dimensions. Its current version was checked alongside
  the primary publisher record. The team's buffered three-dimensional
  construction, rather than an unproved planar extrapolation, is the
  geometric premise here.
- G. Aishwarya and D. Li, *Gaussian Convolution, Internal Energies, and the
  Kneser--Poulsen Conjecture*,
  [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), Conjecture 1.1.
  Full dimension-three majorisation remains the sole named target.

No priority claim is made for rational height arithmetic, determinant
bounds, denominator clearing, or constructive Brehm extension. The new
claim is a fully specified coordinate-height and finite-input bound for
the existing indecomposable Gaussian reduction. It is an author proof
pending independent review; successful small controls do not constitute
independent review or prove the universal construction by computation.

The dependencies are:

| Source | Role and status at this checkpoint |
| --- | --- |
| [PROOF.md](PROOF.md), graph 6164, source `4518e569424cbac04083e6cb9497cc97991cf301` | Accepted full-interval reconstruction and indecomposable reduction. |
| [EFFECTIVE_BOUND.md](EFFECTIVE_BOUND.md), graph 6260, source `de9a0bb7af7179ea6e1b2c5b4013f84d6955f981` | Accepted buffered repair, cell/plane counts, rationality and exact preservation. Its coordinate-height disclaimer records the previous boundary. |
| [Independent effective review](../gaussian_effective_indecomposable_review2/REVIEW.md), graph 6273 | Accepts the preceding construction in its original scope; it does not review the new height bounds. |
| [LINEAR_HEIGHT.md](LINEAR_HEIGHT.md), graph 6329, source `7b78d0a19464d4bcd847861438d5ae7001c344ba` | Author proof of the chain bound and surviving deficit used in the handoff; independent review pending. |
| [Paired cubature](../gaussian_prior_localization/CUBATURE_FRONTIER.md), graph 6212, and [rational producer](../gaussian_prior_localization/RATIONAL_INTERFACE.md) | Accepted smaller atom count and finite integer input. The rational producer is used before building the mesh. |
| [Paired-cubature review](../gaussian_paired_cubature_review2/REVIEW.md), graph 6218 | Accepts that atom/rounding interface; no new Gaussian sign is inferred. |
| [Exposed-edge endpoint proof](../gaussian_exposed_edge_tail/PROOF.md), graph 6351, source `b731c0abe161351d37ca660635e4db2c87f4c9c1` | Author proof supplies signed endpoints from rational coordinate size. Pending independent review. Its previously uncontrolled mesh coordinate size is now bounded. |

The latter endpoint proof already credits Gorbovickis's strict mean-width
theorem and the existing geometric Gaussian low-tail lemma. The current
handoff substitutes uniform integer bounds into that stated interface; it
does not reprove or improve the Gaussian tail argument.

The starting refresh also inspected the new
[dominant-atom middle theorem](../gaussian_uniform_dominant_atom_window/PROOF.md).
Its condition on a dominant prior is not inherited by the mesh augmentation,
so it supplies no missing middle sign for this frontier. The attempted
vanishing-mass truncated-support route was found already covered by
[the nested-hull proof](../gaussian_majorisation_nested_hulls/PROOF.md),
Section 3, and was not republished. Those are method boundaries, not
premises of the coordinate-height theorem. Closed cap and depth-one flap
classifications remain untouched.

The old mesh proof and earlier exact expected files are unchanged. The
new standard-library checker performs only compact rational controls:
one repair's plane geometry, shared face averages, a twelve-reflection
word evaluated in two arithmetic representations, and small budget and
malformed-input checks. No worst-case mesh, state collection, prior audit
corpus, Gaussian quadrature, or large generated artifact is required.
