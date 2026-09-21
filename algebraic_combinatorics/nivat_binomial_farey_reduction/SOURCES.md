# Primary sources and claim boundary

Checked 2026-09-21.

1. Jarkko Kari and Etienne Moutot, *Nivat's conjecture and pattern
   complexity in algebraic subshifts*, Theoretical Computer Science 777
   (2019), 379--386,
   [published article](https://www.sciencedirect.com/science/article/pii/S0304397519300088),
   DOI [10.1016/j.tcs.2018.12.029](https://doi.org/10.1016/j.tcs.2018.12.029),
   [arXiv:1806.07107](https://arxiv.org/abs/1806.07107), and
   [author manuscript](https://emoutot.perso.math.cnrs.fr/static/publi/karimoutot19.1.pdf).
   Their manuscript Theorem 10 proves GNP for the binary four-dot system;
   Corollary 9 covers defining polynomials whose line factors all have one
   direction. Manuscript Theorem 11 supplies the separated-sublattice
   counterexample. Their conclusion leaves characterization of GNP open and
   asks whether failure can occur for a reason other than a proper support
   sublattice.

2. Michal Szabados, *Nivat's conjecture holds for sums of two periodic
   configurations*,
   [arXiv:1710.05360](https://arxiv.org/abs/1710.05360).
   Theorem 1.1 proves the **rectangular** Nivat statement for sums of two
   periodic configurations. It does not establish the arbitrary-window GNP
   for sums of three directions considered here.

3. Pyry Herva and Jarkko Kari, *On the periodic decompositions of
   multidimensional configurations*,
   [arXiv:2409.14948](https://arxiv.org/abs/2409.14948).
   This gives current structural context for periodic decompositions. The
   elementary three-direction decomposition in this note is proved directly
   and does not import a theorem from that preprint.

4. Cleber F. Colle and Eduardo Garibaldi, *A Modular Structure Theorem for
   Minimal Periodic Decompositions and Periodicity of Configurations with
   `P_eta(4,n)<=4n`*,
   [arXiv:2606.10193](https://arxiv.org/abs/2606.10193).
   This is current rectangular-width context and is not a proof dependency.

5. The lattice-index criterion used as the input obstruction is documented,
   with proof and independent review, in
   [the preceding source package](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/nivat_four_dot_lattice).

The contribution here is the class-wide reduction for products of binary
translation binomials: nonprimitive vectors and repeated directions are
converted to bad index divisors; the remaining direction set is a Farey
clique; and the unique three-direction orbit is given an explicit kernel
decomposition. Searches of the sources above and targeted concept/formula
queries found no matching combined statement. The argument is elementary,
so no claim of exclusive priority is made.

The result does not decide the triangular six-dot GNP case, does not treat
general line polynomials, and does not prove or refute Nivat's original
rectangular conjecture.
