# Primary sources and claim boundary

Checked 2026-09-21.

1. Jarkko Kari and Etienne Moutot, *Nivat's conjecture and pattern complexity
   in algebraic subshifts*, Theoretical Computer Science 777 (2019), 379--386,
   [published article](https://doi.org/10.1016/j.tcs.2018.12.029),
   [arXiv:1806.07107](https://arxiv.org/abs/1806.07107).
   Their Theorem 11 (journal numbering; Theorem 10 in the manuscript) proves
   the generalized Nivat property for the binary four-dot system.  Its proof
   establishes the stronger input used here: a four-dot configuration whose
   `0,1` integer lift has a nonzero annihilator is periodic.

2. Jarkko Kari and Michal Szabados, *An algebraic geometric approach to
   Nivat's conjecture*, Information and Computation 271 (2020), 104481,
   [published article](https://doi.org/10.1016/j.ic.2019.104481),
   [arXiv:1510.00177](https://arxiv.org/abs/1510.00177).
   The low-complexity annihilator lemma supplies a nonzero Laurent-polynomial
   annihilator for an integer-valued configuration with
   `P_c(D)<=|D|`.  The elementary integer-coefficient form needed here is also
   used explicitly by Kari--Moutot.

3. Pyry Herva and Jarkko Kari, *On the periodic decompositions of
   multidimensional configurations*,
   [arXiv:2409.14948](https://arxiv.org/abs/2409.14948), revised 2026-05-27.
   This is current context for annihilators and periodic decompositions.  The
   finite-period pointwise-multiplier lemma here is proved directly by an
   orbit norm and does not invoke its main theorems.

4. The prerequisite Farey-triangle class reduction and directional-rank/gcd
   theorem are the adjacent source packages
   [nivat_binomial_farey_reduction](../nivat_binomial_farey_reduction/) and
   [nivat_triangle_directional_rank](../nivat_triangle_directional_rank/).

Targeted searches of these primary sources and current arXiv records used
the terms “generalized Nivat property”, “periodic perturbation/mask”,
“pointwise product”, and “annihilator”.  No statement matching the
periodic-XOR stability lemma or the complete rank-two Farey-triangle
conclusion was found.  The contribution is therefore presented as a short
search-relative structural deduction, not as a claim of exclusive
historical priority.

The result is for arbitrary finite windows, but only for the rank-two stratum
of the binary Farey-triangle kernel.  It neither resolves the rank-three
stratum nor proves or refutes the original rectangular Nivat conjecture.
