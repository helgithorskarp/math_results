# Historical scope of the angular and normal-bundle theorems

27 September 2026. This is a primary-source comparison of an already reviewed
result, not a new theorem or an independent priority review. **Correctness
has been accepted in the stated scope; historical priority remains open.**
The claim that this supplies a *historically new* Kneser--Poulsen class is
therefore still provisional. The unrestricted three-dimensional Gaussian
majorisation problem remains open.

## The precise candidate contribution

Fix a nonempty closed convex set C in R^n, n>=2, and a Borel selection E of
its complete unit outward normal rays. The domain contains C and every
p+ru with (p,u) in E and r>0. The map fixes C and takes

```text
T(p+ru) = p+r a(p,u)u,                 0 <= a(p,u) <= 1.
```

The factor is constant along each selected ray. Nonexpansiveness on this
entire domain is equivalent to the pair condition

```text
(u.v)(1-ab) <= sqrt((1-a^2)(1-b^2)).                    (P)
```

In particular, parallel normals must share a factor. For C={0} this is the
homogeneous angular-ray theorem. The claimed construction, for all points
simultaneously, is the raise

```text
F_theta(p+ru) = (p+r A_theta(a)u, r B_theta(a)),
A_theta(a) = (a+cos(theta))/(1+a cos(theta)),
B_theta(a) = sqrt(1-a^2)sin(theta)/(1+a cos(theta)),
0 <= theta <= pi/2,
```

followed by lowering the last coordinate with the first n coordinates
fixed. Every pair distance decreases. This uses one auxiliary coordinate;
it asserts neither minimal lifting dimension nor absence of another
motion in the original space.

The resulting conclusions are full majorisation for **every bounded law**
on the domain and every Gaussian variance, and both ball-volume comparisons
for **every finite selection of centers and every individual radius**.
The candidate contribution is this class-wide motion and characterization,
including its extension over convex cores. The general motion-to-volume
and motion-to-Gaussian transfers are established inputs.

See the reviewed [angular proof](PROOF.md),
[normal-bundle proof](NORMAL_BUNDLES.md), and
[acceptance record](REVIEW_STATUS.md). This note changes none of their
hypotheses or proofs.

## Closest primary antecedents

| Primary source and exact location | Established input or comparison |
|---|---|
| Bezdek--Connelly, *Pushing disks apart* (2002), [preprint](https://arxiv.org/pdf/math/0108098v1), Lemma 1, Theorem 1, Corollaries 3--5 | The leapfrog motion uses 2n dimensions; low displacement rank and at most n+3 centers give older positive cases. Theorem 1 transfers piecewise-smooth motions in n+2 dimensions to arbitrary-radius union and intersection inequalities. Corollary 5 supplies an n+1-dimensional motion for a common partial dilation: each center is fixed or multiplied by the same lambda>1. Its motion compresses displacement to one scalar norm. These are credited antecedents, not claims of this packet. |
| Csikos, *On the Volume of the Union of Balls* (1998), [publisher PDF](https://link.springer.com/content/pdf/10.1007/PL00009395.pdf), Theorems 4.1, 4.2 and 5.4 | The moving-center derivative formula proves union-volume monotonicity for motions in the original dimension, with the last theorem allowing merely continuous trajectories. It presupposes a contracting motion; it does not provide the displayed angular construction. Its role in the classical volume argument is credited. |
| Bezdek--Naszodi, *The Kneser--Poulsen conjecture for special contractions*, [arXiv:1701.05074v4](https://arxiv.org/html/1701.05074v4), Sections 1.1--1.2, Theorems 1.1--1.3 | Uniform contraction requires one number separating all target distances from all source distances. Strong contraction requires contraction in every fixed coordinate; Theorem 1.3 permits different unconditional bodies. Condition (P) imposes neither premise. The reviewed global angular example fails the direct strong-coordinate condition even after independent changes of frames. This does not rule out compositions of older positive maps or special finite restrictions. |
| Aishwarya--Alam--Li--Myroshnychenko--Zatarain-Vera, *Entropic exercises around the Kneser--Poulsen conjecture* (2023), [arXiv:2210.12842v2](https://arxiv.org/html/2210.12842v2), Theorem 2.4, Corollary 2.6, Theorem 2.9 and Corollary 2.11 | The first gives majorisation for radially symmetric unimodal source and noise under arbitrary contractions. The second permits affine contractions with log-concave source and radially symmetric log-concave noise. The last two address strong contractions and gradients of smooth convex functions with additional unconditional/log-concave assumptions. Those restrictions differ from arbitrary bounded priors. Radial symmetry of a probability law must not be confused with preservation of rays by a map. |
| Aishwarya--Li, *The Kneser--Poulsen phenomena for entropy* (2025), [arXiv:2409.03664v3](https://arxiv.org/html/2409.03664v3), Theorems 1.5--1.6, Propositions 2.5--2.6 and proof of Theorem 1.6 | Arbitrary contractions already preserve all Renyi-entropy comparisons for bounded laws. Smooth contracting motions also give full majorisation, via Gaussian convolution of the velocity field and a volume-contracting transport. That smooth transport is an antecedent of the stronger sampled-density statement used here. The entropy comparisons for arbitrary endpoint contractions alone do not supply the required all-hinge order. |
| Aishwarya--Li, *Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture*, [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), Theorem 1.4 and discussion following Theorem 1.5 | This is the sole problem source and the exact reviewed Gaussian transfer. The authors explicitly credit the smooth transport antecedent to their 2025 work and establish the sampled-density order under continuity alone. They explicitly state that at most two auxiliary dimensions suffice for full majorisation after Gaussian marginalisation. Neither that principle nor the pressure hierarchy is new here. |
| Gorbovickis, *The central set and its application to the Kneser--Poulsen conjecture*, [arXiv:1511.08134v1](https://arxiv.org/pdf/1511.08134v1), Theorem 1.2 and Section 4.1 | The theorem concerns disks with simply connected union interior in the spherical and hyperbolic planes. Its normal segments run inward from a smooth region's boundary to its central set. That normal-bundle terminology concerns a different construction from complete outward normal rays of a fixed convex core. The source gives no statement of (P) or the displayed motion. |

The last-column distinctions compare explicit statements and mechanisms.
They are not proofs that no combination of earlier results could imply the
reviewed class.

## Two qualifications to the partial-dilation comparison

Different admissible ray factors do **not** make our theorem a formal
generalization of every finite partial-dilation instance. For example, fix
x=(1,0,0) and send y=(4,3,0) to y/2. Squared distance drops from 18 to 13/4.
Reversing this operation is a partial dilation. But at the prescribed
origin its factors a=1 and b=1/2 have u.v=4/5, so the left side of (P) is
2/5 and the right side is zero. The corresponding complete-ray map is
not nonexpansive. This is a domain distinction, not a counterexample to
either theorem or an exclusion of alternative representations.

Conversely, [PROOF.md, Section 6](PROOF.md) already gives an admissible
two-ray pair for which the scalar norm-displacement interpolation is not
monotone. This separates those two displayed formulas. A two-center
example cannot establish a new Kneser--Poulsen case: small center sets
already satisfy older theorems. Failure of that formula also does not
exclude a different classical motion or a composition argument.

## What is already contained in team work

The angular construction is original graph6402; its correctness reviews are
[6410](../gaussian_angular_ray_review_frontier/REVIEW.md) and
[6416](../gaussian_angular_ray_contractions_review2/REVIEW.md).
The convex extension is original graph6418, accepted by
[6424](../gaussian_directional_normal_bundle_review2/REVIEW.md). These
reviews establish correctness within scope, not historical priority.

The extension combines that angular motion with the projection-offset
decomposition of the accepted
[common normal-profile result6331](../gaussian_radial_contractions/CONVEX_CORES.md).
It contains the homogeneous angular class by taking C={0}. It does not
contain all of6331: that earlier result allows a common nonlinear radial
profile and radial-order reversal. The reviewed cube example separates
the displayed homogeneous and common-profile representations in the
precise scopes proved there. No separation from all compositions is claimed.
Metric projection and one common constant normal factor are elementary
overlap cases, not the novelty candidate.

The [axial/matrix-path portfolio](../gaussian_axial_cone_rotations/REVIEW_GUIDE.md)
and the accepted cap/flap work are preserved. No containment of all those
classes is asserted. The present theorem does not decide R4's general
deformation/classification problem or R7's adversarial finite configurations.
Arbitrary tangential motion, signed factors, nonlinear direction-and-radius
dependence, and contraction checked only at selected radial samples remain
outside this theorem.

## Priority assessment and reproducibility

No equivalent complete angular/normal class was located in the primary
passages listed above. That is a bounded finding, **not a certification of
priority**. Search terms included the full Kneser--Poulsen name with
"radial contractions", "partial dilations", "normal bundle", "rays",
"homothetic", and "variable dilation". Bibliographies in the 2009 Bezdek
and 2025 Bezdek--Langi--Naszodi surveys were used as discovery aids, not as
proofs of absence. Primary Alexander (1985) full-text access failed at the
publisher; its formula (8) was therefore not directly inspected. The
leapfrog attribution above is verified in Bezdek--Connelly, Section 2.
Neither an exhaustive forward-citation search nor a classification of
compositions of older classes has been completed.

The defensible portfolio wording is: **an independently correctness-reviewed
geometric class with full Gaussian majorisation and arbitrary-radius
Kneser--Poulsen consequences, whose historical priority remains unresolved.**
The candidate novelty resides in the uniform motion and combined class,
not the transfer machinery, projection, common dilation, or entropy order.

[PRIORITY_SOURCES.json](PRIORITY_SOURCES.json) records the checked versions,
passages, access status and selected source hashes. Reproduce the literature
comparison by opening those versions at those locations and comparing their
hypotheses with (P), not by treating an absent keyword as evidence of absence.
This is a written bibliographic assessment; no numerical experiment or
new certificate is being offered as proof. The existing exact checkers and
review manifests remain unchanged. To verify this note's two-file record:

```sh
cd probability/gaussian_angular_ray_contractions
sha256sum -c PRIORITY_SHA256SUMS
```

Downloaded articles and private search output are not distributed in this
packet. Source links, versions and theorem locations are the reproducible
evidence; hashes identify particular retrieved bytes and do not guarantee
that a publisher will preserve its HTML rendering.
