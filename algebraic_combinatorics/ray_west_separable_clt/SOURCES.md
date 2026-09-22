# Sources and status boundary

## Direct mathematical dependency

- *Algebraic distribution of the Ray--West correction on separable
  permutations*:
  <https://github.com/helgithorskarp/math_results/tree/main/algebraic_combinatorics/ray_west_separable_distribution>

  This proves and independently audits the bivariate quadratic equation used
  here.  The new result begins with its discriminant and does not re-claim the
  equation or the mean asymptotic.

## Primary sources

- N. Ray and J. West, *Posets of matrices, and permutations with forbidden
  subsequences*, Annals of Combinatorics 7 (2003), 55--88.
  <https://eprints.maths.manchester.ac.uk/609/>

  This is the source of the codimension-two active-insertion framework and the
  correction `j`.

- H.-K. Hwang, *On convergence rates in the central limit theorems for
  combinatorial structures*, European Journal of Combinatorics 19 (1998),
  329--343. <https://doi.org/10.1006/eujc.1997.0179>

  This is the quasi-powers theorem used for the Gaussian law and its
  convergence rate.

- P. Flajolet and R. Sedgewick, *Analytic Combinatorics*, Cambridge University
  Press (2009), especially Theorem IX.12, the algebraic singularity schema.
  Author-hosted full text: <https://algo.inria.fr/flajolet/Publications/book.pdf>

  This supplies the uniform square-root perturbation and coefficient-transfer
  framework used to pass from the algebraic discriminant to quasi-powers.

- J. B. Gil, O. A. Lopez, and M. D. Weiner, *Distributions of statistics on
  separable permutations*, arXiv:2404.18517.
  <https://arxiv.org/abs/2404.18517>

  This is a current primary reference for multivariate enumeration of other
  statistics on separable permutations.

## Novelty boundary

Targeted searches on 2026-09-22 combined Ray--West correction,
codimension two, separable permutations, signed Schroeder trees, Gaussian
limits, and central limit theorems.  They located the sources above and general
limit theorems for tree statistics, but no limit law for this correction.

The claimed search-relative increment is the explicit singularity
perturbation for this statistic, including

```text
rho'(1)=-rho/2,
rho''(1)=(-1+7rho)/2,
Var(j(Pi_n))/n -> sqrt(2)-5/4,
```

and the resulting Gaussian law.  No novelty is claimed for Ray--West's
definition, the signed-Schroeder encoding, the preceding algebraic generating
function, singularity analysis, or the quasi-powers theorem.
