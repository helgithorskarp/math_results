# Sources and positioning

All statements here concern bounded probability inputs in dimension three.
The main theorem is a complete author argument subject to independent
correctness review. A targeted search is not a historical priority audit.

1. **Named problem and external premise.** Gautam Aishwarya and Dongbin Li,
   [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
   Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
   Conjecture 1.1 and Theorem 1.4(i)(a), checked 26 September 2026.
   The stochastic comparison for sampled density values under a continuous
   contraction is the external analytic premise. Its continuity-only part
   applies; no C1 trajectory or volume-contracting-map assertion is used.

2. **Retained three-coordinate comparison.** The team's
   [rank/Abel proof, Theorem B](../gaussian_majorisation_rank_abel/PROOF.md),
   graph height 5964, source commit
   `f7c122d6a5ade217930d63da27e67f9a9e55a539`, supplies the
   Gamma(3/2) comparison and the precise density-value interpretation.
   The new proof repeats its reduction to item 1 so the dependency is
   inspectable. Its Theorem C disproves unsmoothed cancellation for general
   probability densities and remains compatible with our positive error.
   The paired-rank and lifting results are not new claims of this packet.

3. **Compact law frontier.** Researcher 3's
   [uniform localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md),
   graph height 6134, defines D and D_k and proves D_k increases to D with
   error below 4/k. We use its definitions and quantifiers. Our inequality
   applies to every admissible configuration, not to a sample or a rational
   grid. The proof of the unrestricted 7/50 bound itself does not require
   localization or its quantitative error.

4. **Compact moment frontier.** Researcher 8's
   [uniform moment budgets](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md),
   graph height 6150, identify beta averages with signed hinge averages and
   give B_k at N_k=2^16 k^8-2, with D-B_k below 5/k. These are the definitions
   used in our simultaneous coefficient lower bounds. We do not evaluate
   the alternating moment expression or claim a zero sign for its terms.
   This packet supplies an actual numerical bound on all rows, rather
   than a new interface requiring yet-uncomputed Gaussian coefficients.

The new ingredient is the verified one-dimensional shifted-Gamma envelope
and its uniform 7/50 consequence. The constants were deliberately rounded
to simple rationals. Neither their scalar optimality nor sharpness for
Gaussian mixtures is asserted. Floating linear programming helped select
them but is absent from the trusted chain and public replay requirements.

The disjoint-cap Gaussian/ball theorem is a separate exact positive result.
Its [positioning note](../gaussian_cap_auxiliary_certificates/POSITIONING.md)
preserves that source and records the new axial comparison boundary. No
cap-count extension, new fixture catalogue, or independent acceptance of
that theorem is supplied in this pass. It is not a premise of the present
unrestricted defect bound.

The central-flap and common-set routes retain different missing signs.
Our absolute constant supplies neither their all-threshold positivity nor
the threshold-dependent small-variance estimate needed to transfer a new
Kneser--Poulsen conclusion. In particular the campaign's headline objective
remains unfulfilled.
