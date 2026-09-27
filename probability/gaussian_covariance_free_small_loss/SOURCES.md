# Attribution, dependency boundary and certification handoff

The sole problem source is Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), Conjecture 1.1
in dimension three. The primary text was refreshed on 27 September 2026.
The Gaussian posterior identities, doubled-dimensional contraction path,
replica integrals and lower-dimensional continuous-contraction comparisons
are credited antecedents. No historical-priority claim is made.

## Proof inputs

1. [Covariance-free rigidity](../gaussian_contraction_covariance_free/PROOF.md),
   graph5940 `bafkreiaqwmlvkptgqb2dhefwh3qa7u6wtwb2wmftshhcu3oknknoiwq2bu`,
   source `a264d277a51683479424060972dafb44123db597`.
   Only the matrix-geometric bound `E|TX-X|^2<=sqrt(6)R sqrt(D)` after
   optimal alignment is used. Section 2 recalls its proof, including the
   singular-safe classical square-root trace inequality. Its entropy
   theorem is not imported. [Audit5952](../gaussian_majorisation_bridge_barrier/AUDIT.md),
   `bafkreibohj2zayll2fnt5zmiug23fkkai6oy4mv3mhinmh5etuxvgzofxq`, source
   `fc25eff113b59c72fa820def81698e914a80d15b`, independently accepted that
   earlier source. The present author performed that older independent
   audit; it is not an independent review of this new result.

2. [Loss-normalized R6 coarea/Abel framework](../gaussian_loss_normalized_hinges/PROOF.md),
   graph6325 `bafkreif2b3e5sw6dumihujzhpul4uce3p7v4elvfpyz77miocxodmytq24`,
   source `a68810063b8ad53dda046c68552a14e76f8d3f07`, accepted6333
   `bafkreieyqbx7j34qcop5tdz46qgtub5jcvo3rz3cxzdc6d4uspcshm6uo4`.
   The exact normalization `32 pi^3` and half-Abel identification are
   credited and rederived locally in Section 5. The previous argument used
   full six-dimensional convexity at small radius. The new proof needs
   convexity only in three transverse directions, obtained from mean loss
   at arbitrary fixed radius, and proves the required signed derivative.

3. [Motion/chain strictness, Section 2](../gaussian_motion_chain_strictness/PROOF.md),
   graph6572 `bafkreicizul3qsqtcswwmkamba2obcajavxaa4oz6wsbrsste3svibbypq`,
   source `ef6ba3fd50f790468405b3da22f0a93fee60a4f6`.
   Only its universal reverse-posterior upper peak budget and circumradius
   observation enter the strict margin (Theorem B). The new non-strict
   theorem does not need this input. That author proof is pending review;
   no motion/chain hypothesis or unreviewed openness theorem is imported.

4. [Covariance-boundary theorem](../gaussian_covariance_boundary/PROOF.md),
   graph6454 `bafkreibispqtfpr3v5zk6n3pnjxql25oaznxpt6tdtzu4r6gecbjycdiwq`,
   source `262439aa29c2ce7f7f14b7ab1bdd85c92bd13338`.
   [Acceptance6466](../gaussian_covariance_boundary_review2/REVIEW.md),
   `bafkreihvqwr5ol5mk4kt3capq6qhmohfg54zxl6kjmzqfz2v5kles6z4ja`, source
   `ea22701250fb1aeba92919413a0c8b4d785ffe90`, also audited its necessary
   target-peak dependency. It enters only Corollary C: substitute the new
   loss-floor index N into its existing covariance schedule. Its old
   projection mechanism and covariance-boundary sign are not new here.

The first eight records in [DEPENDENCIES.json](DEPENDENCIES.json) pin the
four proof sources, applicable reviews, and the R3 consumer. The ninth pins
the newly available R3 independent review. Each source hash was matched
against `git show` at its recorded revision. The checker verifies bytes
without importing any teammate code. Source identity is not proof checking.

## Minimal durable handoff to R2 and R3

R3's [all-radius loss-relative localization](../gaussian_all_radius_loss_localization/PROOF.md),
graph6576 `bafkreibivrqpvaay3jjrqcg3ezx4u64efeszvrtcyr6k5jtlh4lexfghqm`,
source `1104fcce0bfcf2d9cb16f70daa45c361f54c977c`, is now independently
accepted at [review6578](../gaussian_all_radius_loss_localization_review2/REVIEW.md),
`bafkreidli7x7h2uqouhy2hqylp3h3vo6qfjlimawtlpw5f6vhy5rc3eazq`, source
`24fce7dc389c0e634549ba50d12076ebde570d3a`. Its actual source covariance
floor remains essential. Our theorem supplies such a floor on the residual
adverse frontier via Corollary C; it does not remove the premise from that
localization theorem on arbitrary inputs. Its
[same-pair finite interface](../gaussian_all_radius_loss_localization/HANDOFF.md)
then retains loss and the actual covariance while approximating the hinge
curve. R2 still needs an actual signed interior certificate; no uncomputed
beta row or absolute error is assigned a sign.

The new schedule can be checked before any cubature: `N(R,j)` bounds the
loss below which the whole positive-threshold slab is signed. If it fails,
the old covariance-boundary guard is available. Any remaining adverse input
has both `d>2^-N` and `Cov(X)/s,Cov(Y)/s>2^-L_cov I`. These are uniform
over laws, weights, and support sizes at fixed R,j. No extra perturbation
neighborhood, target-size restriction, or interface construction is needed.

## Adjacent progress and limits

- R1's [universal upper-density window](../gaussian_universal_peak_window/PROOF.md)
  signs `u>=exp(-2^-32)` without radius/loss restrictions, using a
  six-dimensional marked-pair chart and spherical Helmholtz estimate.
  It was read at refresh and is not a premise here. Our threshold cutoff
  can be arbitrary and our radius bounded, at the cost of a small-loss
  premise; the new cancellation uses three aligned transverse directions.
- R2's [mixed-chain family certificate](../gaussian_chain_stability_certificate/PROOF.md)
  consumes graph6572 to give all-threshold prior/cloud/variance families
  with separate width and mass guards. It is not duplicated or subsumed:
  the present theorem has no chain premise but no uniform low endpoint.
- R7's [finite-symmetry reduction](../gaussian_finite_symmetry_reduction/HANDOFF.md)
  retains the unrestricted question with isotropic sources and all positive
  variances. It does not give a common normalized radius or a variance
  floor. Thus it is compatible with, but not closed by, this fixed-R,j
  boundary theorem. No adverse contact or counterexample is supplied here.

The substantive increment is the uniform covariance-free small-loss sign
and its loss-linear margin. The old 16-label simplex-flap geometry is only
an exact degenerating-prior control. The low endpoint and residual compact
interior remain open, as does the full R3 conjecture and any new
Kneser--Poulsen consequence. Independent review of this proof is pending.
