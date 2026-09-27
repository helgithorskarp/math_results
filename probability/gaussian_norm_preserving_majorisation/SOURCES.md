# Sources, dependencies, and scope

All primary links below were inspected on 27 September 2026. Negative
literature search does not establish historical priority. Source publication
and exact finite checks do not constitute independent acceptance.

## Sole target

G. Aishwarya and D. Li, *Gaussian Convolution, Internal Energies, and the
Kneser--Poulsen Conjecture*, [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
Conjecture 1.1 supplies the target; Theorems 1.2--1.4 distinguish the known
planar, pressure-class, and continuous-contraction results. The present
argument directly signs all hinges under the additional anchor equality.
It does not assume an admissible continuous motion or claim the unrestricted
dimension-three conjecture.

Campaign root5950:
`bafkreifx5vhi7azxuu4chant6r4c7vvgjsypwdoob4ug7ea2nmzctlsrhu`.

## Essential analytic dependency

R1, *Positive spherical sinc comparison: arbitrary R3 contractions and
eventual Gaussian majorisation*, graph6494:
`bafkreiapfugbtlssf2f2h4luaequrpulv7vzk5iz37m3lzvnftl47shyja`.

[Proof, Lemma 1](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_spherical_sinc_comparison/PROOF.md).
Verified source commit `9c50ebb1b3543cd5c1886ba45f6f782ce2481853`.
The exact proof bytes are pinned in [INPUTS.json](INPUTS.json).
It was independently accepted at graph6506 during preparation:
`bafkreig2wqpuyfeltfh2chd37dapwfssfyligckobxeofqat6lccdrgopu`.
The [review](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_spherical_sinc_comparison_review2/REVIEW.md),
source `0be7c96ba05427ddba39a7db6d6036fbdd534aea`, specifically checks the
operator identity and its C2 extension. Its exact bytes are also pinned.
It does not accept any of the new consequences in the present package.

We use the positive C2 operator difference, not R1's eventual-majorisation
endpoint or finite mean-width tail. R1 applies it to affine-equivariant
submodular functions and proves arbitrary-contraction spherical log-MGF
sign. Our equal-norm cancellation instead allows arbitrary supermodular
functions, producing actual hinges at every spatial radius. The operator
identity itself is credited to R1's campaign contribution and its classical
Kirchhoff/Duhamel background, without a historical-newness claim.

## Primary geometric comparison

K. Bezdek and R. Connelly, *The Kneser--Poulsen Conjecture for Spherical
Polytopes*, Discrete Comput. Geom. 32 (2004), 101--106,
[author-hosted manuscript](https://pi.math.cornell.edu/~connelly/pdf/10.1007_s00454-004-0831-1.pdf).
Theorem 1 and Corollary 1 concern hemispheres in every spherical dimension.
They do not supply the arbitrary cap radii asserted here in dimension two.

I. Gorbovickis, *The central set and its application to the Kneser--Poulsen
conjecture*, [arXiv:1511.08134v3](https://arxiv.org/html/1511.08134v3).
Theorem 1.2 assumes that a union of spherical disks has simply connected
interior. Corollary 1.3 treats connected intersections, and Corollary 1.4
gives the corresponding large-cap union and small-cap intersection cases.
Our Theorem D imposes none of these conditions. This is a claimed extension
of the searched results, not an assertion of externally reviewed priority.

K. Bezdek, Z. Langi and M. Naszodi, *Selected topics from the theory of
intersections of balls*, [arXiv:2411.10302v2](https://arxiv.org/html/2411.10302v2),
Section 2, especially Theorem 2.12. This recent primary author survey again
records the hemisphere comparison in arbitrary spherical dimension, along
with continuous-contraction results. It supports the distinction between
our cap claim and those stated results, not a comprehensive novelty verdict.

## Durable class landscape and interfaces

R2's [balanced-loss finite certificate](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_balanced_loss_certificate/PROOF.md),
source `91c63ff5a464f725ea6bee38290e56df594f1c60`, graph6504
`bafkreihaxhapv7kvng2yatxu2unok44m3v3vxwvp47mdgxkfvuqlxvzmgy`, is a separate
all-variance route through a straight contracting motion after alignment.
Its guard uses k*delta_min>=4F. Our equal-norm guard permits tight pairs
with nonzero loss elsewhere and makes no alignment-motion premise.
This is a scope comparison, not a proof dependency or a universal
noninclusion theorem about motion classes.

R8's [small-target theorem](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_uniform_small_target/PROOF.md),
graph6482 `bafkreicraiysc263oz6hqlgbjtv57fg2gq35ce5alltnbozu2iszl5ucou`,
and the [R3/R8 cutoff consolidation](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_mean_loss_margin/CUTOFF_CONSOLIDATION.md)
are preserved. Neither is used to sign the new class. The bounded-law limit
here is written out with approximations on the original support; no finite
certificate is silently promoted to all diffuse measures.

The minimal finite-input and bounded-law interfaces are in README.md.
Unrelated cubic nut-graph work and all earlier campaign artifacts remain
at their existing durable checkpoints.
